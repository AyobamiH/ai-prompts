# Successor Canary Record

For each predecessor record:

- run ID and terminal classification;
- exact deployed source and runtime subject;
- whether an effect was admitted;
- explicit `immutable: true`;
- explicit `relaunch_allowed: false`.

For the repair record:

- base and repair head;
- exact required CI result;
- merge and deployment identifiers;
- preserved invariants.

For the successor:

- fresh issue and run IDs;
- branch and PR identity;
- exact-head CI;
- independent verifier contract and decision;
- final DoneState-like terminal state;
- whether the proof PR remained unmerged.
