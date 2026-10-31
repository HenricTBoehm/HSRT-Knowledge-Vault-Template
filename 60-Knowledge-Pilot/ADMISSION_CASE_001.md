# Synthetic negative case 001 — missing original evidence

This is a **test fixture**, not a real research object, verification or human decision.

| Field | Simulated state |
| --- | --- |
| Candidate | Unspecified placeholder concept |
| Original source | NONE SUPPLIED |
| Source version | UNKNOWN / NOT YET LINKED |
| Human review | NONE RECORDED |
| Independent validation | NONE CLAIMED |
| Expected disposition | **HOLD** |
| Permitted knowledge effect | **NONE** |

A conformant YAML shape cannot supply missing original evidence or human authorization. This case tests that a missing source remains on the negative path and no admission is created.

## Expected agent trace

1. Read the repository and pilot `AGENTS.md` files.
2. Observe that no exact source object, immutable version or human review is available.
3. Leave source identity and version unresolved; do not invent a pointer.
4. Record or report `HOLD` with `authorized_effect: none`.
5. Do not create an OKF concept, update the admitted index, or claim verification.
6. Report which evidence and human decision would be required before reconsideration.

Expected result: the source register and OKF bundle remain empty. This fixture demonstrates control flow only and must never be converted into an admission record.
