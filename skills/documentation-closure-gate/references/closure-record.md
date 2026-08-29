# Documentation Closure Record

```json
{
  "schema_version": "1",
  "commit": "0123456789abcdef0123456789abcdef01234567",
  "implementation": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
  "documentation": {
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "status": "pass",
    "changed": ["CHANGELOG.md", "docs/CURRENT-STATUS.md"]
  },
  "ci": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
  "deployment": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
  "live_verification": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
  "evidence": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"}
}
```

For a true no-document-impact change, replace `changed` with a non-empty `no_impact_rationale`. The helper only checks that a rationale exists. Repository-specific policy should determine whether the rationale is credible for the changed paths.

## Closure report

Record:

- Exact commit and any modeled subject transitions
- Changed paths and documentation classification
- Validation and CI identifiers
- Artifact and deployment identifiers
- Live observation time and target
- Evidence record locator and digest
- Remaining limitations

Do not create a source commit merely to append evidence after the final CI run unless the new commit will be revalidated.
