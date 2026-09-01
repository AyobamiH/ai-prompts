# Environment Isolation Manifest

For each environment record non-secret identifiers only:

- environment and provider account;
- service, project, or Worker name;
- configuration path and endpoint;
- deployment workflow and trigger;
- credential source identifier and explicit secret target;
- exact credential-bearing steps and exact mutation steps;
- confirmation that checkout, dependency installation, validation, and all job-wide contexts receive no provider credentials;
- OAuth app, marketplace listing, tenant, database, and queue identities where applicable;
- expected public and protected route behavior;
- last exact deployment identifier and live probe time.

## Preflight

Reject duplicate service names, endpoints, credential targets, or mutable aliases across environments unless the provider proves they are intentionally shared. Reject unresolved defaults, implicit current-context targeting, secret values in the manifest, writes without an exact environment parameter, job-wide provider credentials, or credentials exposed to checkout, dependency installation, or validation. Every credential-bearing step must be a member of the declared mutation-step set.

## Recovery evidence

After suspected cross-targeting, verify production and non-production independently. Record known-good source, deployment identifiers, target-name logs, route probes, credential-validation outcomes without values, and removal of temporary recovery triggers.
