---
name: google-business-profile-post
description: "Prepare, validate, publish, and verify a Google Business Profile update with required branded media, local-outcome copy, CTA, tracked destination, duplicate protection, and provider-status readback. Use for GBP post workflows, not general Google Business Profile administration."
---

# Google Business Profile Post

Treat copy, image, CTA, and destination as one publication payload. For this workflow, a purpose-built image is required for every post unless the operator explicitly changes that standing rule.

## Prepare

1. Confirm the exact business location/profile and intended local audience.
2. Start from one customer problem or outcome. Avoid generic announcements and unsupported local claims.
3. Validate the destination route, tracking parameters, CTA type, and mobile landing experience.
4. Create or select a branded image for this post. Validate its real MIME type, size, dimensions, aspect ratio, safe crop, legibility, and relationship to the copy.
5. Freeze the complete payload and obtain approval through `approval-safe-social-publishing`.

## Publish

- Restore all composer fields after any upload or UI transition, because Google may preserve media while losing text or CTA state.
- Compare the visible composer against the frozen payload immediately before submit.
- Submit once. Do not interpret a disabled button, empty-content error, upload completion, or request acceptance as publication.
- If Google reports `submitted for review`, report exactly that and wait for public or provider readback.
- Check for an existing matching update before any retry.

## Verify

A live claim requires evidence that the expected update appears on the correct business profile with matching copy, image, CTA, and destination. Preserve the provider state and canonical public surface when available.

Read [references/gbp-checklist.md](references/gbp-checklist.md) before staging or verifying a post.
