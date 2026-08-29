# Product Site Launch Gates

## 1. Product truth

- current capabilities and roadmap are separated;
- product relationships and trust boundaries are accurate;
- evidence links are current;
- pricing, availability, support, privacy, and legal claims are verified or omitted.

## 2. Information architecture

At minimum, route decisions exist for:

- home;
- each product;
- use cases;
- how it works;
- evidence or trust;
- documentation or getting started;
- company;
- support or contact;
- privacy and terms.

Only create pages with a real user job. Do not inflate the sitemap with empty placeholders.

## 3. Design quality

- visual direction follows the product rather than an AI-design stereotype;
- typography and spacing form a coherent system;
- product proof is visible, not replaced by generic illustrations;
- motion explains hierarchy or state;
- mobile layouts are intentionally designed;
- focus, hover, error, loading, and reduced-motion states exist.

## 4. Technical quality

- clean production build;
- no critical console or runtime errors;
- all launch routes return expected status and content;
- forms and primary CTAs work;
- responsive layouts verified at representative widths;
- keyboard navigation and visible focus work;
- contrast and semantics meet the chosen accessibility target;
- performance checked on the deployed build;
- metadata, canonical URLs, sitemap, robots, and structured data are valid;
- analytics records a test event without exposing secrets.

## 5. Source and deployment

- source is committed on the intended branch;
- the pushed commit matches the built source;
- saved deployment version identifies that commit;
- provider reports a successful deployment;
- public readback matches the expected version;
- rollback or last-known-good version is known.

## 6. Domain and TLS

- exact hostname confirmed;
- DNS target matches the hosting provider;
- domain validation active;
- TLS certificate valid;
- apex and `www` behaviour deliberate;
- HTTP redirects to HTTPS;
- canonical host redirect works;
- no previous site is overwritten without explicit authority and recovery plan.

## State vocabulary

Use the highest proven state only:

```text
planned
designed
implemented
build_passed
version_saved
deployed
domain_connected
publicly_verified
```

A launch is complete only at `publicly_verified` with all critical gates passing.
