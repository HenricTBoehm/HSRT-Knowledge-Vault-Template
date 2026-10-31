# Governed knowledge pilot

This empty pilot demonstrates a **source → proposed representation → human admission → limited wiki standing** workflow. It does **not** implement research authority or a security enforcement boundary.

## Layers

- `RAW/`: pointers to **your external source system**, no imported source corpus. `source-register.md` is intentionally empty.
- `OKF/`: a standalone, currently empty **OKF v0.2 candidate bundle**. Its root `index.md` declares the target version. Non-reserved Markdown concepts placed there must have valid YAML frontmatter and a non-empty `type`.
- `ADMISSION_GATE.md`: documented decision rule; **HOLD by default**; only a real human review may decide `ADMIT_TO_WIKI`.
- `REVIEW_MATRIX.md`: distinct structural, source, admission, authority and independent-validity checks; none implies the next.
- `DECISIONS/`: storage for *actual* scoped human decision records; starts empty.
- `index.md`: catalog of the pilot workflow and any subsequently reviewed concept links.
- `log.md`: dated maintenance log, not admission evidence.
- `AGENTS.md`: scoped `INGEST`, `QUERY`, `LINT` instructions.

The repository-wide working folders are **not** declared OKF bundles. Governance metadata such as `review_status` or `research_status` may coexist with OKF lifecycle status, but these fields are **not synonyms**.

## Conditions for admission

A well-formed concept with traceable sources is **necessary, not sufficient**. The human review must inspect sources, conflicting evidence, scope, freeze/version boundaries and the consequences of allowing the note. Merely adding a note to an index does not upgrade it.

The supplied `ADMISSION_CASE_001.md` is a synthetic *negative path* only, with no source and the default HOLD. It is not an executed or approved research case.

## External standards

This blank starter references the [Open Knowledge Format project](https://github.com/GoogleCloudPlatform/open-knowledge-format) for the v0.2 interchange conventions; it does not copy upstream specs. No claim of HSDL mapping, HSRT Core conformance or external scientific validation is made.
