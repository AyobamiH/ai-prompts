# CI Trigger Diagnosis

## Evidence packet

- Repository, branch, commit, authoring mechanism, and changed paths
- Expected workflows and allowed events
- Workflow definitions at the relevant revision
- Branch and path filter evaluation
- Commit message skip directives
- Repository Actions state and workflow permissions
- Check suites, statuses, and runs for the exact SHA
- Ruleset and required-check names
- Fork or pull-request context
- Selected recovery and why it preserves the release subject

## Compact observation

```json
{
  "commit": "0123456789abcdef0123456789abcdef01234567",
  "expected_workflows": ["CI", "Deploy"],
  "observed_runs": [
    {
      "workflow": "CI",
      "head_sha": "0123456789abcdef0123456789abcdef01234567",
      "event": "pull_request",
      "status": "completed",
      "conclusion": "success",
      "run_id": "123"
    }
  ]
}
```

## Recovery selection

Prefer a supported existing trigger that exercises the intended workflow on the exact subject. If the workflow itself needs repair, treat that as a new implementation change with its own review and validation. Do not backfill a status manually unless the repository's trusted CI system is explicitly designed to do so.
