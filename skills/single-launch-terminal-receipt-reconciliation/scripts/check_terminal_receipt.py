#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2:
        print("usage: check_terminal_receipt.py MANIFEST.json", file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text()); f=[]
    if d.get("schema")!="single-launch-terminal-receipt.v1": f.append("unsupported schema")
    if d.get("intent_persisted_before_launch") is not True: f.append("intent must be persisted before launch")
    if d.get("launch_attempts") != 1: f.append("exactly one launch attempt required")
    if d.get("relaunch_after_ack_loss") is not False: f.append("relaunch after acknowledgement loss is forbidden")
    if d.get("completion_oracle")!="terminal_receipt": f.append("terminal receipt must be sole completion oracle")
    if d.get("process_registry_is_completion_oracle") is not False: f.append("process registry cannot be completion authority")
    r=d.get("receipt") or {}
    if r.get("schema")!="donestate.implementation-receipt.v1": f.append("receipt schema mismatch")
    for k in ("outside_workspace","atomic_write","terminal","verified_binding"):
        if r.get(k) is not True: f.append(f"receipt {k} must be true")
    bind=r.get("bindings") or {}
    for k in ("run_id","action_id","repository","base_subject"):
        if not bind.get(k): f.append(f"receipt binding {k} required")
    if d.get("missing_receipt_outcome")!="AMBIGUOUS_EFFECT": f.append("missing receipt must become AMBIGUOUS_EFFECT")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2)); return 0 if not f else 1
if __name__=="__main__": raise SystemExit(main())
