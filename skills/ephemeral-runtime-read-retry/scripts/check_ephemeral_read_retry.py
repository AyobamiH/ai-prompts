#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2:
        print("usage: check_ephemeral_read_retry.py MANIFEST.json", file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text()); f=[]
    if d.get("schema")!="ephemeral-runtime-read-retry.v1": f.append("unsupported schema")
    if d.get("operation_class")!="read_only_idempotent": f.append("operation must be read_only_idempotent")
    if d.get("credential_free") is not True: f.append("read path must be credential-free")
    attempts=d.get("attempts") or []
    max_attempts=d.get("max_attempts")
    if not isinstance(max_attempts,int) or max_attempts < 1 or max_attempts > 5: f.append("max_attempts must be 1..5")
    if len(attempts) > (max_attempts or 0): f.append("attempt list exceeds max_attempts")
    ids=[a.get("runtime_id") for a in attempts]
    if not ids or None in ids or len(ids)!=len(set(ids)): f.append("each attempt requires a distinct runtime_id")
    for a in attempts[:-1]:
        if a.get("succeeded") is False and a.get("failed_runtime_retired") is not True:
            f.append("failed runtimes must be retired before retry")
    backoff=d.get("backoff_seconds") or []
    if any((not isinstance(x,(int,float)) or x < 0 or x > 30) for x in backoff): f.append("backoff must be bounded to <=30s")
    if d.get("mutation_retry_allowed") is not False: f.append("mutation retry must remain disabled")
    if d.get("successful_runtime_promoted") is not True: f.append("successful runtime promotion must be explicit")
    if d.get("single_logical_action") is not True: f.append("retries must remain one logical action")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2)); return 0 if not f else 1
if __name__=="__main__": raise SystemExit(main())
