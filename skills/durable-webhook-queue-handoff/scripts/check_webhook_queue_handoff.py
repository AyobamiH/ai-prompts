#!/usr/bin/env python3
import json, sys
from pathlib import Path

def fail(msgs, msg):
    msgs.append(msg)

def main():
    if len(sys.argv) != 2:
        print("usage: check_webhook_queue_handoff.py MANIFEST.json", file=sys.stderr)
        return 2
    d = json.loads(Path(sys.argv[1]).read_text())
    f=[]
    if d.get("schema") != "durable-webhook-queue-handoff.v1": fail(f,"unsupported schema")
    for k in ("signed_delivery","finding_upserted","queue_setup_awaited_before_accept","queue_failure_recorded_locally","fallback_reconciliation","duplicate_deliveries_one_run"):
        if d.get(k) is not True: fail(f,f"{k} must be true")
    if d.get("execution_awaited_before_accept") is not False: fail(f,"webhook must not await execution")
    if not d.get("dedupe_key"): fail(f,"dedupe_key required")
    claim=d.get("atomic_claim") or {}
    if claim.get("from") != "OPEN" or claim.get("to") != "REPAIR_QUEUED" or not claim.get("run_id"):
        fail(f,"atomic OPEN -> REPAIR_QUEUED claim with run_id required")
    if d.get("provider_retry_used_for_queue_failure") is not False:
        fail(f,"provider retry must not be the recovery mechanism after a claimed queue failure")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2))
    return 0 if not f else 1
if __name__=="__main__":
    raise SystemExit(main())
