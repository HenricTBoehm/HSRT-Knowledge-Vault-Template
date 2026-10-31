# HSRT-inspired review matrix — methodological scaffold

This matrix is a **proposal for checking representations**, not a report of executed HSRT research, empirical validity or technical access enforcement. Each check needs an actual reviewer and scoped evidence to support a verdict.

| ID | Check | Evidence demanded | Default when absent | Allowed inference |
| --- | --- | --- | --- | --- |
| S-1 | Original source identity | Exact artifact, source system, version/revision | HOLD / UNKNOWN | Source pointer only |
| S-2 | Source governance | Access/classification, freeze and supersession status | HOLD | Classification scope only |
| R-1 | Representation structure | Valid Markdown/YAML, references, type and format constraints | HOLD for adoption; technical structural pass may be recorded | Syntax only |
| R-2 | Claim attribution | Claim ↔ stable source IDs, contradictory/negative sources | HOLD / SUPPLEMENT | Traceable working hypothesis, not proof |
| G-1 | Human admission | Actual human, date, candidate diff, bounded scope, decision rationale | HOLD | ADMIT_TO_WIKI only for limited representation |
| G-2 | Authority non-creation | Evidence that format/merge/trust signals have not been treated as research or action authorization | ESCALATE if disputed | No external authority conveyed |
| V-1 | Independent generality | Independent comparator, reference standard, negative outcome criterion | NOT_EVALUATED | No science-validity verdict without external test |
| X-1 | Rollback | Reviewable history and explicit correction/withdrawal process | HOLD | Reversible knowledge edit only |

## Decision spaces are separate

- **Technical format:** `PASS / FAIL / NOT_EVALUATED` for specified structural checks.
- **Knowledge admission:** `HOLD / SUPPLEMENT / ESCALATE / REJECT / ADMIT_TO_WIKI` by a real, authorized human.
- **Scientific validity:** not assessed by this repository. Use an independently specified research protocol if applicable.
- **Operational authority:** never assigned by the knowledge layer.

A positive result in one decision space does **not** create a positive result in any other. In particular, S-1 + R-1 + R-2 does not entail G-1 or V-1.

## Negative and null results

Unresolved provenance, a contradiction, an adverse comparator result or a null effect must remain visible. Do not silently rewrite a candidate or change success criteria after seeing results. An independent claim evaluation belongs in a separately versioned, prior-approved contract, not in an agent-generated note.
