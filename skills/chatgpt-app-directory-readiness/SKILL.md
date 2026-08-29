---
name: chatgpt-app-directory-readiness
description: "Prepare and verify a ChatGPT app directory draft or review handoff across listing metadata, MCP connectivity, authentication, trust pages, icons, data declarations, tests, and exact-release evidence. Use when creating or repairing an OpenAI app-directory listing, deciding whether a draft is review-ready, or separating saved-draft status from submitted, approved, and published states."
---

# Chatgpt App Directory Readiness

Build the evidence packet before entering owner attestations or submitting for review. Saving a form is not publication.

## Workflow

1. Resolve the exact app release subject, public MCP endpoint, publisher identity, support contact, and intended listing state.
2. Confirm the connected MCP exposes the intended current tool surface and authentication model.
3. Prepare truthful name, description, category, prompts, capabilities, limitations, data-use declarations, and support details.
4. Verify public health, privacy, terms, deletion, and support surfaces against actual implementation.
5. Prepare directory and composer icons in the required formats and dimensions. Check file type after generation or conversion.
6. Test at least one complete positive path and meaningful negative paths such as missing authentication, missing scope, invalid input, denied authority, and unavailable verifier.
7. Bind test results, documentation, and deployment evidence to the exact release subject.
8. Fill and save the draft without accepting final attestations or submitting unless the user explicitly authorizes those actions.
9. Record domain verification, OAuth consent, icon upload, review submission, approval, and publication as separate transitions.
10. Produce a handoff containing completed fields, evidence, remaining owner actions, and known blockers.

## State vocabulary

Use `LOCAL_PREPARED`, `DRAFT_SAVED`, `DOMAIN_VERIFIED`, `OAUTH_CONNECTED`, `REVIEW_READY`, `SUBMITTED`, `APPROVED`, `PUBLISHED`, and `BLOCKED`. Do not collapse them into “done.”

## Stop conditions

Stop before final legal attestations, review submission, public publication, new OAuth scopes, or data-use claims that require the verified owner. Never invent publisher identity, retention terms, or support details.

Use [references/directory-handoff.md](references/directory-handoff.md) for the evidence pack. Run `python scripts/check_directory_manifest.py MANIFEST.json` for the compact readiness manifest.
