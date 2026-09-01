# Authorized Real-Data Record

Use `authorized-real-data-pilot.v1` and choose `dataset_approved`, `pilot_executed`, or `market_evidence` as the target state.

The dataset section records a stable ID, jurisdiction, owner-supplied/licensed/public source kind, immutable source reference, acquisition time, SHA-256 checksum, provenance reference, rights basis, allowed purpose, retention days, deletion path, classification, schema-validation result, target-market relevance, and approval reference.

Record separate approvals for rights, use, retention, and no shared training. Require tenant isolation and minimization; set `shared_training_use` and `raw_records_in_manifest` to false.

Pilot execution records authorized real users, non-founder users, completed tasks, a predefined baseline and outcome metric, and preserved failures. Five real users and ten tasks support only the bounded label `MARKET_EVIDENCE_READY`; keep `product_market_fit_claimed` false.
