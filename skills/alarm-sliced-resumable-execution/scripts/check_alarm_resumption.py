#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2:
        print("usage: check_alarm_resumption.py MANIFEST.json", file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text()); f=[]
    if d.get("schema")!="alarm-sliced-resumable-execution.v1": f.append("unsupported schema")
    for k in ("checkpoint_persisted","read_only_reconciliation","schedules_next_alarm","recognized_checkpoint_only","unrelated_unsettled_fail_closed","stops_after_terminal"):
        if d.get(k) is not True: f.append(f"{k} must be true")
    if d.get("launch_attempts") != 1: f.append("exactly one implementation launch required")
    if d.get("long_wait_inside_alarm") is not False: f.append("alarm invocation must not hold the full long wait")
    if d.get("relaunch_on_resume") is not False: f.append("resume cannot relaunch implementation")
    if d.get("reconciliation_slices_per_alarm") != 1: f.append("exactly one bounded reconciliation slice per alarm required")
    if d.get("unknown_effect_outcome")!="AMBIGUOUS_EFFECT": f.append("unknown effect boundary must fail closed as AMBIGUOUS_EFFECT")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2)); return 0 if not f else 1
if __name__=="__main__": raise SystemExit(main())
