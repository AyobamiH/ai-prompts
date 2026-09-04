---
name: job-application-metadata-scrub
description: "Prepare a DOCX CV, resume, cover letter, or other job-application document for external submission by removing authoring provenance and review metadata while preserving intentional content and proving the cleaned package. Use when a user asks to remove metadata, author names, generator traces, comments, revision identifiers, or AI-tool breadcrumbs from a Word application file."
---

# Job Application Metadata Scrub

Produce a clean submission copy, not a promise that authorship detectors cannot make inferences.

## Boundary

- Remove hidden package provenance: core and extended document properties, custom properties, preview thumbnails, ZIP entry timestamps, and Word revision-session identifiers.
- Preserve visible CV content, hyperlinks, media, styles, and truthful references to AI technologies in the applicant's experience.
- Do not rewrite prose to evade AI detection. Do not describe the result as "undetectable" or "guaranteed human-written".
- Do not treat visible terms such as OpenAI, Anthropic, Codex, Claude, MCP, or AI as metadata when they are intentional qualifications or project evidence.
- Do not silently discard reviewer comments or tracked changes. They can contain substantive edits. Stop and require explicit finalisation with the appropriate document-review workflow first.

## Workflow

1. Keep the source file unchanged and choose a distinct output filename.
2. Audit the source:

   ```bash
   python scripts/scrub_docx_metadata.py application.docx --audit
   ```

3. If comments or tracked changes are reported, stop. Ask whether to accept or reject revisions and whether to remove comments. Complete that review decision before scrubbing.
4. Create the cleaned copy:

   ```bash
   python scripts/scrub_docx_metadata.py application.docx --out application-clean.docx
   ```

5. Require the script's post-scrub audit to report `clean: true` and `content_preserved: true`.
6. Render the cleaned DOCX and inspect every page. Metadata removal is not complete delivery if the document package opens but the layout is damaged.
7. Report exactly what was removed, any warnings, and the cleaned filename. Never claim that visible content was changed unless a separate authorised edit occurred.

## Passing evidence

A submission copy passes only when:

- it is a valid DOCX package with its main document intact;
- core and extended properties contain no child values;
- custom document properties and preview thumbnails are absent;
- no Word `rsid*`, paragraph ID, or text ID attributes remain;
- no comment, people, or tracked-change parts remain;
- metadata-only parts contain no known AI authoring-tool markers;
- all ZIP entry timestamps are normalised;
- story-part text and document relationships match the source; and
- the cleaned file passes final render inspection.

The helper is deliberately fail-closed around review artifacts and does not redact names, phone numbers, email addresses, or other visible CV content.
