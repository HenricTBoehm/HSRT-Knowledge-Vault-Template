# HSRT Knowledge Vault Template

**A source-linked, governed knowledge-vault starter with an HSRT-inspired admission discipline.**

This is a **blank public template**, not a research repository, data corpus, certified HSRT implementation, HSDL conformance package, or validated scientific framework. It contains **no original HSRT research artifacts, case results, private Drive links, or project-specific identifiers**.

## Boundary first

| Layer | Meaning | Permission |
| --- | --- | --- |
| External RAW | Original documents, governed versions and source evidence in **your** chosen source system | Read-only from the vault; never copied automatically |
| Inbox / draft knowledge | Unreviewed notes, hypotheses and proposed changes | Candidate; no authority |
| Admission Gate | Explicit human review of source provenance, conflicts, scope and effect | Default `HOLD` |
| Wiki / OKF | Linked, maintained knowledge representations | Only limited knowledge-layer standing after human admission |
| Canonical research / operational release | Governed by separate external authorities | Never granted by this vault |

**Core invariant:** source readability ≠ source validity ≠ wiki admission ≠ scientific validity ≠ authorization to act.

## Layout

| Path | Purpose |
| --- | --- |
| `00-Inbox/` | Incoming candidate notes; not admitted knowledge |
| `10-Concepts/` | Topic and concept notes once reviewed under your policy |
| `20-Studies/` | Study-navigation placeholders, not studies or results |
| `30-Artifacts/` | Artifact pointers and metadata, no copied evidence |
| `40-Decisions/` | Reviewable decisions and their bounded effects |
| `50-Publications/` | Publication reference index, empty by default |
| `60-Knowledge-Pilot/` | Controlled RAW-pointer / OKF / admission pilot |
| `templates/` | Generic blank note and decision templates (not active knowledge) |
| `scripts/` and `tests/` | Structural checks and public-disclosure guard |
| `.github/` | CI and PR review checklist |

Only `60-Knowledge-Pilot/OKF/` targets **Open Knowledge Format (OKF) v0.2**. The full Obsidian vault is not declared OKF-conformant. [OKF upstream specification](https://github.com/GoogleCloudPlatform/open-knowledge-format). This template intentionally **links to** external specifications rather than redistributing their full contents.

## Initial use

Start with [START_HERE.md](START_HERE.md) for ready-to-use INGEST, QUERY and LINT prompts.


1. Keep original sources in a separate, permission-controlled system. Enter **pointers only**, never raw documents or credentials, into `60-Knowledge-Pilot/RAW/source-register.md`.
2. Prepare a note from `templates/research-note.md` or `templates/okf-concept.md` on a review branch. Resolve actual source IDs and freeze boundaries; write `UNKNOWN / NOT YET LINKED` where unresolved.
3. Open an admission record from `templates/admission-record.md`. Review with `60-Knowledge-Pilot/ADMISSION_GATE.md`. The **default is `HOLD`**.
4. Use the [review matrix](60-Knowledge-Pilot/REVIEW_MATRIX.md) to distinguish structural success from source, governance and independent-evaluation claims. A blank [independent-validation contract](templates/independent-validation-contract.md) is provided for prospective studies; no evaluation is performed.
5. Only a real, documented human `ADMIT_TO_WIKI` decision permits limited incorporation into the working Wiki, without declaring research truth or authority.
6. Update `60-Knowledge-Pilot/index.md` and `log.md` as reviewable changes. Run `python scripts/validate_vault.py .` and `python scripts/audit_public.py .` before publishing.

This repository starts with **zero admitted concepts, zero source records and zero research findings**. An example negative `HOLD` dry-run illustrates missing-evidence handling without recording a real research case.

## Review and safety

- `AGENTS.md` states the repository-wide agent restrictions; `60-Knowledge-Pilot/AGENTS.md` specifies pilot workflow (`INGEST`, `QUERY`, `LINT`).
- Structural validation and the public-disclosure scan are CI checks, **not** scientific validation or executable admission enforcement. The disclosure scan blocks non-allowlisted file types and configured sensitive patterns, but deliberate human review is still required.
- `verified` and `status: stable` in OKF do not imply `ADMIT_TO_WIKI`, external canonical authority or scientific verification.
- Do not upload private documents, real account identifiers, source texts without rights, personal data or access-controlled URLs to a public instance.
- A Git merge does not substitute for admission or domain-level approval.

## Publish as an actual GitHub template

See [PUBLISHING.md](PUBLISHING.md). After creating the public repository, enable GitHub's **Template repository** setting. The included publish script can do both when the GitHub CLI is installed and authenticated.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch, pull-request, manifest and review requirements.

## License and provenance

The generic starter materials in this repository are MIT-licensed (see `LICENSE`). The external OKF specification and LLM Wiki conceptual reference are not copied or relicensed here. The admission terminology and layered safeguards are **HSRT-inspired design choices**, not assertions of formal HSRT implementation or conformance. This template grants no rights to any private source material.
