# HSRT-inspired knowledge admission gate (template v0.1)

> **Documented decision discipline, not executable security enforcement.** This template does not implement or certify HSRT, PADC, HSDL, scientific validation, or an institutional approval process.

## Admissible object and bounded effect

- **Candidate:** one specific Wiki note, sourced claim, relationship, summary or status annotation with an exact proposed diff.
- **Potential effect:** admission of that representation to the experimental/working Wiki only. It does not amend source artifacts, frozen studies, research canon, external authority or permitted system actions.
- **Agent powers:** read within authorized access, compare, cite, flag gaps and propose drafts; no autonomous admission, execution or release.
- **Decision authority:** an actual named human reviewer with a documented, scoped verdict. **Absent such a decision: HOLD.**

## Evidence checklist

1. Exact candidate ID, path, change/diff and intended effect.
2. One or more exact accessible original source objects, source roles, relevant versions/IDs and hashes when available (else explicitly `UNKNOWN / NOT YET LINKED`).
3. Clear separation of source evidence, earlier interpretation and newly generated synthesis.
4. Source status, applicability, supersession and immutable/frozen boundary checks.
5. Contradictory or negative evidence, countercriteria, uncertainties and the potential downstream impact of admission.
6. Genuine human reviewer, review instant and rationale, **only if actually provided**.

## Possible dispositions

| Disposition | Meaning | Permitted effect |
| --- | --- | --- |
| `HOLD` | Missing, unresolved or unreviewed prerequisites (**default**) | No admission |
| `SUPPLEMENT` | Precisely identified missing material | No admission |
| `ESCALATE` | Authority, privacy, conflicts or effects outside this gate | No admission; separate decision required |
| `REJECT` | Inconsistent or inadmissible candidate | No admission; retain audit trace |
| `ADMIT_TO_WIKI` | Explicit human-reviewed admission of a specific bounded representation | Working Wiki note only; **never canon** |

## Guard conditions

`well_formed ∧ sources_traceable ∧ in_scope` is **necessary but not sufficient** for admission. An agent-created note, code check, `verified` signal, `status: stable` or Git merge is **not** the human decision.

An `ADMIT_TO_WIKI` record must identify the exact candidate, authorizing human reviewer, date/time, cited sources, scope/effect, limitations and review rationale. If any item is missing, stay in HOLD (or SUPPLEMENT/ESCALATE/REJECT as separately and genuinely determined). No record may be fabricated to satisfy a validator.

## Rollback and audit

Use an isolated branch / reviewable PR. Preserve superseded notes and decision traces; do not silently change the decision history. A follow-up withdrawal/rejection requires a new explicit record. Closing an unmerged PR leaves the accepted source state unchanged; a merged edit needs a separately reviewed revert.
