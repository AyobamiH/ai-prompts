# Resume Checkpoint

Record:

- durable action-intent digest;
- run and action IDs;
- runtime identity;
- receipt path and deadline;
- launch-attempt count;
- last reconciliation time and result;
- next alarm time;
- lease/fencing identity;
- explicit safe-resume class.

The checkpoint contains no secret values and cannot authorize a second implementation launch.
