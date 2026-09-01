# Environment Isolation Manifest

For each environment record non-secret identifiers only:

- environment and provider account;
- service, project, or Worker name;
- configuration path and endpoint;
- deployment workflow and trigger;
- credential source identifier and explicit secret target;
- OAuth app, marketplace listing, tenant, database, and queue identities where applicable;
- expected public and protected route behavior;
- last exact deployment identifier and live probe time.

## Preflight

Reject duplicate service names, endpoints, credential targets, or mutable aliases across environments unless the provider proves they are intentionally shared. Reject unresolved defaults, implicit current-context targeting, secret values in the manifest, and writes without an exact environment parameter.

## Recovery evidence

After suspected cross-targeting, verify production and non-production independently. Record known-good source, deployment identifiers, target-name logs, route probes, credential-validation outcomes without values, and removal of temporary recovery triggers.
