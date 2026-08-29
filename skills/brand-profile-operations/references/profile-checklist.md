# Brand Profile Operations Checklist

## Account-separation decision

Before creating a page or profile, answer:

- Is the audience distinct from existing accounts?
- Is the buying intent different?
- Does the product have stable onboarding and a public destination?
- Is there a recurring supply of native content?
- Can the operator maintain replies, messages, assets, and facts?
- Would a product page or parent-brand section work better for now?

Return `create`, `defer`, or `keep under parent`.

## Profile specification

```yaml
provider: linkedin | instagram | threads | other
account_id: provider-id
brand_id: stable-brand-id
display_name: Exact public name
handle: exact-handle
tagline: one-line positioning
about: full approved text
category: provider category
website: verified URL
action: provider action and destination
location: verified location or service area
founded: verified year or null
phone: verified value or null
specialties: []
messaging_enabled: true | false
logo:
  source_hash: sha256
  rendered_hash: sha256
banner:
  source_hash: sha256
  rendered_hash: sha256
intentionally_blank: []
```

## Save strategy

- Save small logical sections when the provider form has fragile validation.
- Re-read the saved value from the editor after every section.
- Reopen the public page after major fields or media.
- Keep the existing live asset until the replacement is saved.
- Record provider errors and the exact asset attempted.
- Do not interpret upload completion as applied media.

## Final verification

Compare public state against every non-null specification field. Return:

- verified live fields;
- pending-review fields;
- failed fields with provider evidence;
- intentionally blank fields and reasons;
- preserved existing fields or assets;
- canonical public profile URL.
