#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2:
        print("usage: check_successor_canary.py MANIFEST.json", file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text()); f=[]
    if d.get("schema")!="immutable-successor-canary.v1": f.append("unsupported schema")
    preds=d.get("predecessors") or []
    if not preds: f.append("at least one predecessor required")
    pred_ids=set()
    for p in preds:
        rid=p.get("run_id")
        if not rid: f.append("predecessor run_id required")
        else: pred_ids.add(rid)
        if p.get("immutable") is not True: f.append(f"predecessor {rid} must be immutable")
        if p.get("relaunch_allowed") is not False: f.append(f"predecessor {rid} must forbid relaunch")
        if p.get("terminal_state") not in {"FAILED_SAFE","AMBIGUOUS_EFFECT","BLOCKED_CAPABILITY","FAILED"}:
            f.append(f"predecessor {rid} must have a preserved terminal state")
    repair=d.get("repair") or {}
    for k in ("exact_head_ci_green","merged","deployed"):
        if repair.get(k) is not True: f.append(f"repair {k} must be true")
    if not repair.get("exact_head") or not repair.get("deployment_id"): f.append("repair exact_head and deployment_id required")
    s=d.get("successor") or {}
    if not s.get("run_id") or s.get("run_id") in pred_ids: f.append("successor run_id must be fresh")
    chain=s.get("proof_chain") or {}
    for k in ("durable_run","implementation_receipt","validation","branch","pull_request","exact_head_ci","independent_verifier","terminal_verified"):
        if chain.get(k) is not True: f.append(f"successor proof missing {k}")
    if s.get("canary_pr_unmerged") is not True: f.append("proof canary PR must remain unmerged")
    if s.get("claimed_success_before_verification") is not False: f.append("success cannot be claimed before verification")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2)); return 0 if not f else 1
if __name__=="__main__": raise SystemExit(main())
