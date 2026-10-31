---
type: Attested Computation
title: "REPLACE — computation title"
description: "REPLACE — what this sanctioned computation returns"
status: draft
runtime: REPLACE_WITH_RUNTIME
parameters: []
executor:
  resource: references/REPLACE_WITH_RUN_INSTRUCTIONS.md
  receipt: [result]
attester:
  resource: references/REPLACE_WITH_DETERMINISTIC_ATTESTER
sources: []
authority: none
review_status: AWAITING_HUMAN_REVIEW
---

# REPLACE — computation title

> [!warning] Candidate contract only. It is neither admitted nor scientifically validated.

# Computation

~~~text
REPLACE_WITH_SANCTIONED_COMPUTATION
~~~

## Contract notes

- Declare only typed parameter holes the agent may fill.
- Keep exactly one computation: either this fenced block or a `computation` path, never both.
- The executor must return the declared receipt fields.
- The attester must be deterministic and must not use an LLM.
- Add real `generated`, `verified`, freshness and provenance fields only when supported by observed evidence.
