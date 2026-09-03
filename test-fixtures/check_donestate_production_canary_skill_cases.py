#!/usr/bin/env python3
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    fixture_path = Path(__file__).with_name("donestate-production-canary-skill-cases.json")
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    failures = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for name, case in data.get("cases", {}).items():
            script = repo / case["script"]
            module = load_module(script, f"skill_{name}")
            for label, expected in (("pass", 0), ("refuse", 1)):
                manifest = tmp / f"{name}-{label}.json"
                manifest.write_text(json.dumps(case[label]), encoding="utf-8")
                previous = sys.argv
                try:
                    sys.argv = [str(script), str(manifest)]
                    actual = module.main()
                finally:
                    sys.argv = previous
                if actual != expected:
                    failures.append({"skill": name, "case": label, "expected": expected, "actual": actual})
    verdict = "READY" if not failures else "REFUSED"
    print(json.dumps({"verdict": verdict, "failures": failures}, indent=2))
    return 0 if not failures else 1

if __name__ == "__main__":
    raise SystemExit(main())
