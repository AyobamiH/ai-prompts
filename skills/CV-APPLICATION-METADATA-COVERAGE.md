# CV Application Metadata Scrub Coverage

Snapshot date: 2026-09-04.

Primary evidence surface: the generated `Ayobami_John_Haastrup_CV.docx` used for the current job application, inspected as an OOXML package after its first metadata-cleaning pass.

This record separates hidden document provenance from visible, truthful CV content. It does not claim that a document can be made "AI-undetectable" or that metadata removal changes authorship.

## Observed state

- `docProps/core.xml` contained no property values.
- `docProps/app.xml` contained no extended-property values.
- No `docProps/custom.xml`, comment parts, people parts, tracked changes, reviewer authors, or known AI-tool markers remained in metadata-only surfaces.
- Intentional visible references to AI, OpenAI Codex, Claude Code, Anthropic APIs, MCP, and AI-assisted engineering remained part of the applicant's stated skills and project experience.
- A cached preview thumbnail remained.
- ZIP entries retained the document-generation timestamp.
- 329 Word revision-session elements remained in style parts even though story-part `rsid*` attributes had already been removed.

## Newly packaged contract

`job-application-metadata-scrub` extends the generic DOCX privacy pass into a submission-specific boundary:

- audit before mutation;
- preserve the source and write a distinct cleaned copy;
- clear core and extended properties rather than checking only author fields;
- remove custom properties and preview thumbnails with their package relationships;
- normalise ZIP entry timestamps;
- remove Word revision-session attributes and elements across every Word XML part;
- scan metadata-only surfaces for known generator markers without misclassifying visible technology qualifications;
- refuse unresolved comments and tracked changes instead of silently changing the intended final CV;
- prove story text and document relationships are unchanged; and
- require render inspection after the structural audit passes.

## Forward test

The helper passed two standard-library regression cases:

1. It removed seeded ChatGPT/python-docx properties, custom properties, a preview, timestamps, and revision identifiers while preserving visible text.
2. It refused a fixture containing unresolved tracked changes.

It then processed the live CV copy and reported:

- `clean: true`;
- `content_preserved: true`;
- one preview removed;
- 329 revision identifiers removed;
- no residual metadata markers, review parts, tracked changes, custom properties, or property values; and
- normalised ZIP timestamps.

Both pages rendered successfully after scrubbing. The before-and-after PNG SHA-256 values matched exactly for page 1 and page 2, proving that the cleaned package did not change the rendered CV.

## Deduplication decision

The generic document privacy helper already covered creator, last-modified-by, custom properties, and story-part revision attributes. This skill does not copy that capability as a renamed wrapper. It adds the job-application-specific decision boundary, broader hidden-provenance coverage, fail-closed review handling, content invariants, and render-equivalence evidence that materially change safe execution.
