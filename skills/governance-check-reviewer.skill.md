---
name: governance-check-reviewer
description: Interpret artifacts/06_governance_check.md, trace incomplete MDR fields, and turn governance failures into owner-specific next actions without treating completeness as proof of approval.
---

# Governance check reviewer

## Review failures

1. Read `artifacts/06_governance_check.md` and each referenced MDR.
2. For every missing field, identify:
   - the metric and accountable owner, if evidenced
   - the missing or incomplete value
   - the evidence already available
   - the exact confirmation or decision still needed
3. Group related questions for the same owner to reduce follow-up work.
4. Recommend updating `feedback/workshop_decisions.yaml` when decisions are confirmed, then rerunning `metricgov finalize --from feedback/workshop_decisions.yaml`.

## Interpretation

- A failure means required governance information is incomplete; it does not prove the metric is wrong.
- A pass means fields are complete according to current rules; it does not independently prove owner approval or business correctness.
- Do not fill missing values from assumptions or generic industry definitions.
- Preserve unresolved questions and provide an actionable owner-by-owner checklist.
