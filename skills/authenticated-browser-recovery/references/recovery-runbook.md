# Authenticated Browser Recovery Runbook

## Classify the last state

### Staged

Fields or media are visible in the composer and no submit action occurred. Safe recovery may reconstruct missing fields from the frozen payload.

### Submitted

The provider clearly acknowledged the action. Move to readback. Do not reopen and submit again.

### Rejected

The provider clearly rejected the action and readback finds no object. Record the reason. Repair only within existing authority.

### Ambiguous

The UI disappeared, network failed, tab crashed, or response was lost after submit may have occurred. Search provider state and possible duplicates. Never infer absence from an empty composer.

## Recovery steps

1. Record provider, account, target, frozen payload hash, prior state, and time window.
2. Reconnect to the existing authenticated session.
3. Inspect account selector, current page URL, visible success or error notices, drafts, recent objects, and provider history.
4. If the state is staged, restore only missing fields and validate the entire form.
5. If the state is submitted or ambiguous, perform readback or duplicate discovery before mutation.
6. If an upload failed before submit, inspect file signature and provider limits. Try one justified derivative or the full-resolution crop route.
7. Capture final provider state and public readback.

## Retry limits

A second attempt is justified only when new evidence identifies a correctable, non-ambiguous cause and duplicate side effects are controlled. Stop after repeated identical failure. Report the exact blocker and preserve the live state.

## Stop conditions

Stop and ask for user action when:

- the provider requires account or sign-in choice;
- acceptance of terms or a legal representation is required;
- CAPTCHA or anti-bot challenge appears;
- the available account differs from the approved account;
- permissions are insufficient;
- recovery would delete or overwrite a working public object without a safe replacement;
- the requested consequence exceeds the frozen approval.

Do not reveal or repurpose credentials. Use only the browser's advertised authentication mechanism.
