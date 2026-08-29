# Google Business Profile Post Checklist

## Identity

- correct Google account;
- correct business profile and location;
- correct local audience and service area;
- no cross-brand account confusion.

## Copy

- one customer problem or outcome;
- no unsupported superlatives, prices, availability, or location claims;
- copy fits current provider rules without silent truncation;
- call to action matches the actual landing page;
- spelling and business name are correct.

## Image

- purpose-built for this post;
- source and rendered hashes recorded;
- actual MIME type matches extension;
- current provider limits satisfied;
- important content is crop-safe;
- overlay is legible on mobile;
- image supports the copy and does not introduce new claims.

## Destination

- HTTPS loads successfully;
- intended route exists;
- mobile layout works;
- CTA action is possible;
- tracking parameters are valid and do not break the route;
- redirect resolves to the expected brand.

## Pre-submit

- frozen payload fingerprint matches approval;
- copy remains present after media upload;
- image preview is correct;
- CTA and destination remain present;
- no existing matching post or unresolved attempt;
- submit control is enabled without a hidden validation error.

## Readback

Record one of:

- `verified_published`;
- `submitted_for_review`;
- `provider_rejected`;
- `confirmed_absent`;
- `reconciliation_required`.

For `verified_published`, compare business identity, copy, image, CTA, destination, and visible timestamp. For `submitted_for_review`, schedule or perform a later status check rather than resubmitting.
