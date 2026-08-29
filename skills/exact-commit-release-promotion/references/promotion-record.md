# Promotion Record

## Required identifiers

- Repository and default branch
- Candidate branch and commit
- Review or pull request identifier
- Merge commit or release subject
- CI provider, workflow, run, and conclusion
- Artifact name and digest
- Deployment environment and immutable deployment identifier
- Live verification observation and time
- Evidence record and release identifier

## Compact manifest

```json
{
  "schema_version": "1",
  "commit": "0123456789abcdef0123456789abcdef01234567",
  "required_stages": [
    "validation",
    "documentation",
    "ci",
    "deployment",
    "live_verification",
    "evidence"
  ],
  "stages": {
    "validation": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
    "documentation": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
    "ci": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
    "deployment": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
    "live_verification": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"},
    "evidence": {"commit": "0123456789abcdef0123456789abcdef01234567", "status": "pass"}
  }
}
```

A real release record should add provider-specific run URLs, digests, timestamps, and verifier identities. URLs are locators, not immutable proof by themselves.
