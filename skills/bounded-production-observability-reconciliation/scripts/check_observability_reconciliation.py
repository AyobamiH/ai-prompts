#!/usr/bin/env python3
import json, sys
from pathlib import Path
def main():
    if len(sys.argv)!=2:
        print("usage: check_observability_reconciliation.py MANIFEST.json", file=sys.stderr); return 2
    d=json.loads(Path(sys.argv[1]).read_text()); f=[]
    if d.get("schema")!="bounded-production-observability-reconciliation.v1": f.append("unsupported schema")
    for k in ("source_sha","deployment_id","window_start","window_end"):
        if not d.get(k): f.append(f"{k} required")
    if not (d.get("needles") or []): f.append("at least one raw needle required")
    stages=d.get("stages") or []
    if len(stages)<2: f.append("ordered stages required")
    names=[s.get("name") for s in stages]
    if None in names or len(names)!=len(set(names)): f.append("stage names must be unique")
    unresolved=d.get("first_unresolved_stage")
    if unresolved and unresolved not in names: f.append("first_unresolved_stage must name an ordered stage")
    if d.get("secrets_redacted") is not True: f.append("secrets must be redacted")
    if d.get("mutations_during_reconciliation") is not False: f.append("reconciliation must remain non-mutating")
    if d.get("mixed_subjects") is not False: f.append("do not mix runs or deployments")
    verdict="READY" if not f else "REFUSED"
    print(json.dumps({"verdict":verdict,"failures":f}, indent=2)); return 0 if not f else 1
if __name__=="__main__": raise SystemExit(main())
