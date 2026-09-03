# Retry Contract

Record:

- logical action ID and operation class;
- maximum attempts;
- backoff sequence;
- runtime identity per attempt;
- destruction/retirement of failed runtimes;
- credential presence on the read path;
- successful runtime promotion rule;
- terminal fail-safe state;
- explicit prohibition on mutation retry.

A provider error alone does not justify adding credentials or making a mutating operation retryable.
