# Pull Request Convergence Record

Use `overlapping-pr-convergence.v1` with one current remote default-branch SHA and tree.

For each PR record its head SHA, the base SHA used to build it, stable intended change IDs, the subset already present in default, the remaining subset, semantic-conflict observation, exact-head CI state, and requested action.

The expected classifications and actions are:

| Condition | Classification | Action |
| --- | --- | --- |
| A semantic conflict exists | `CONFLICT_REVIEW_REQUIRED` | `manual_conflict_review` |
| All intended changes are in default | `ALREADY_IN_BASE` | `close_without_merge` |
| Present and remaining subsets are both non-empty | `REMAINING_DELTA` | `rebuild_remaining_delta` |
| No overlap, but the PR base is stale | `REBASE_REQUIRED` | `rebase_and_retest` |
| No overlap, current base, exact-head CI passes | `READY` | `review_ready` |

Require provider readback, content-digest verification, preserved history, no force update, and no merge performed by the reconciliation step.
