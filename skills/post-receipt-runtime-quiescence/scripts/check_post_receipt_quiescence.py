#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2:
        print("usage: check_post_receipt_quiescence.py MANIFEST.json", file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text()); f=[]
    if d.get("schema")!="post-receipt-runtime-quiescence.v1": f.append("unsupported schema")
    if d.get("receipt_verified") is not True: f.append("terminal receipt must be verified first")
    q=d.get("quiescence_seconds")
    if not isinstance(q,(int,float)) or q <= 0 or q > 300: f.append("quiescence_seconds must be bounded and positive")
    if d.get("fixed_interval") is not True: f.append("quiescence interval must be fixed/versioned")
    if d.get("validation_started_after_quiescence") is not True: f.append("validation must start after quiescence")
    if d.get("implementation_launch_attempts") != 1: f.append("no implementation relaunch is allowed")
    if d.get("regression_pins_interval") is not True: f.append("regression must pin the interval")
    if d.get("runtime_close_invalidates_receipt") is not False: f.append("runtime close must not invalidate verified receipt")
    if d.get("post_receipt_runtime_error_outcome") not in {"BLOCKED_CAPABILITY","NONE"}:
        f.append("post-receipt runtime interruption must be classified separately")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2)); return 0 if not f else 1
if __name__=="__main__": raise SystemExit(main())
