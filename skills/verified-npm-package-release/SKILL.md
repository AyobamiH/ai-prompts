---
name: verified-npm-package-release
description: "Prepare, publish, and independently verify an npm package release with aligned versions, metadata, provenance, artifact contents, authentication, and install behavior. Use for initial or subsequent npm releases, package publication debugging, registry-auth handoffs, or verifying that a public package matches the intended Git commit."
---

# Verified npm Package Release

Treat publication as an external effect. Verify the registry result from a clean consumer environment instead of trusting the publish command alone.

## Workflow

1. Resolve the release commit and confirm the working tree contains only intended changes.
2. Check package name ownership, access level, licence, repository, bugs, homepage, engines, exports, types, files, and publish configuration.
3. Align `package.json`, lockfile, changelog, source version constants, documentation, and Git tag.
4. Run clean install, format, lint, types, tests, build, and package-specific checks.
5. Run `npm pack --dry-run` or create a local tarball. Inspect every included file and test installation from that tarball.
6. Scan the packed artifact for credentials, local state, development fixtures, oversized files, and missing runtime files.
7. Prefer trusted publishing or a scoped automation token. For interactive authentication, pause for the user to complete the registry flow and never request the token in chat.
8. Publish once. Do not retry an ambiguous publication until registry readback establishes whether the version exists.
9. Read back package metadata and integrity from the registry.
10. Install the exact published version in a new temporary consumer, import or execute the public entry point, and compare expected exports.
11. Create or verify the Git tag and release record against the same source commit.

## Rules

- Never republish an existing version.
- Do not use `latest` readback as proof when publishing a non-latest dist-tag.
- Do not claim provenance unless a valid attestation is present and verified.
- Redact registry configuration and tokens from output.
- Record what was verified separately from what was merely configured.

Use [references/npm-release-checklist.md](references/npm-release-checklist.md) for the release record.
