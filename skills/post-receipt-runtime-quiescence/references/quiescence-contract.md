# Quiescence Contract

Record:

- verified receipt timestamp;
- fixed quiescence duration;
- earliest permitted validation timestamp;
- validation start timestamp;
- runtime identity;
- implementation launch count;
- post-receipt interruption classification;
- regression test that pins the interval.

The interval is a control-plane readiness guard, not an additional implementation timeout and not a success oracle.
