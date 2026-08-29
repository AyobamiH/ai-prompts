# npm Release Checklist

## Identity

- Package and version
- Source repository and full commit
- Intended dist-tag and access level
- Node and npm versions

## Package review

- `npm pkg get` values are correct
- Exports and types resolve
- Runtime dependencies are declared in `dependencies`
- Development-only packages are excluded from runtime dependencies
- `files` allowlist or `.npmignore` has been reviewed
- Lifecycle scripts are necessary and documented
- Licence file is included

## Artifact review

- Tarball filename and SHA-512 integrity
- File list reviewed
- Secret scan passed
- Clean tarball install passed
- Public import or CLI smoke passed

## Publication and readback

- Authentication method recorded without credential material
- Publish command and outcome
- Registry version exists
- Dist-tag points to the intended version
- Registry integrity matches downloaded artifact
- Clean registry install passed
- Git tag and release point to the source commit

## Ambiguous publish recovery

If the client times out or disconnects, query the exact package version first. If present, verify it. If absent, reauthenticate and publish. Never increment the version solely because the client response was lost.
