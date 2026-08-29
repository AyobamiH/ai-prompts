# Domain Challenge Record

Record:

- App-directory draft identifier
- Provider challenge identifier if available
- Target hostname
- Exact public path
- Challenge value digest
- Challenge expiry
- Source commit
- CI run and conclusion
- Deployment identifier
- Public response status, content type, body digest, and checked time
- Provider verification result and time
- Retention or removal decision

## Route contract

```text
GET <exact challenge path>
status: 200
body: <exact challenge value>
authentication: none
redirects: none
dynamic user data: none
```

Reject a response with HTML wrappers, JSON quoting when raw text is required, trailing explanatory text, authentication redirects, or a body from another draft.

## Cleanup

Follow current provider requirements. If the path must remain available, keep it documented and isolated. If removal is allowed, remove it through the normal exact-commit release process and verify the removal publicly. Do not remove it immediately merely because the verification button succeeded.
