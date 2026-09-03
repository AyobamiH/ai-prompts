# Runtime Ladder Record

Freeze the baseline:

- package/runtime image versions;
- transport;
- keep-alive/lifetime settings;
- session policy;
- process-launch mode;
- agent version and exact command;
- timeout;
- verifier and publication semantics.

Each experiment records:

- one changed field with previous and next values;
- exact repair head and deployment;
- fresh canary ID;
- observed failure or success boundary;
- invariant-test result.

Do not compare experiments whose workload subject changed.
