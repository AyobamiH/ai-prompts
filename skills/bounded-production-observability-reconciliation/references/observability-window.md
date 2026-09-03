# Observability Window

Record:

- source SHA and provider deployment/runtime version;
- issue/request and run IDs;
- exact start/end timestamps;
- raw needles used;
- ordered stages and observed timestamps;
- first unresolved stage;
- secret-redaction assertion;
- explicit `mutations_during_reconciliation: false`.

A later successful stage may justify revisiting an earlier missing log, but it does not authorize mixing another run or deployment into the same evidence record.
