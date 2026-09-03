#!/usr/bin/env python3
import json, sys, re
from pathlib import Path
UUID=r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
def main():
    if len(sys.argv)!=2:
        print("usage: check_branch_retirement.py MANIFEST.json", file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text()); f=[]
    if d.get("schema")!="verified-run-branch-retirement.v1": f.append("unsupported schema")
    branch=d.get("branch") or ""
    prefix=re.escape(d.get("prefix") or "")
    if not prefix or not re.fullmatch(prefix+r"/"+UUID, branch): f.append("branch must exactly match prefix/<uuid-v4>")
    if d.get("run_state")!="VERIFIED": f.append("run must be independently VERIFIED")
    if d.get("objective_class")!="maintenance_pr": f.append("objective_class must be maintenance_pr")
    if d.get("pr_closed") is not True or d.get("pr_merged") is not True: f.append("PR must be closed and merged")
    for k in ("head_repo_is_selected_repo","sealed_subject_matches","queued_finding_present","authenticated_close_trigger","periodic_reconciliation","preserve_nonverified_history"):
        if d.get(k) is not True: f.append(f"{k} must be true")
    if d.get("retirement_failure_changes_verification") is not False: f.append("cleanup failure cannot change verification")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2)); return 0 if not f else 1
if __name__=="__main__": raise SystemExit(main())
