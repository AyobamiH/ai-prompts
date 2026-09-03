#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2:
        print("usage: check_runtime_ladder.py MANIFEST.json", file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text()); f=[]
    if d.get("schema")!="managed-runtime-one-variable-recovery.v1": f.append("unsupported schema")
    if d.get("compatibility_aligned") is not True: f.append("compatibility invariants must be aligned first")
    if not d.get("frozen_workload_digest"): f.append("frozen workload digest required")
    ex=d.get("experiments") or []
    if not ex: f.append("at least one experiment required")
    canaries=[]
    for i,e in enumerate(ex,1):
        changes=e.get("changed_fields") or {}
        if len(changes)!=1: f.append(f"experiment {i} must change exactly one field")
        if e.get("invariants_tested") is not True: f.append(f"experiment {i} invariants not tested")
        if not e.get("exact_head") or not e.get("deployment_id"): f.append(f"experiment {i} exact head/deployment required")
        if not e.get("canary_id"): f.append(f"experiment {i} canary_id required")
        else: canaries.append(e["canary_id"])
        if e.get("workload_digest") != d.get("frozen_workload_digest"): f.append(f"experiment {i} changed the workload")
    if len(canaries)!=len(set(canaries)): f.append("each experiment requires a fresh canary")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2)); return 0 if not f else 1
if __name__=="__main__": raise SystemExit(main())
