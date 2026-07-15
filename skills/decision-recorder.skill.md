---
name: decision-recorder
description: Convert stakeholder workshop notes into safe structured feedback/workshop_decisions.yaml entries while distinguishing owner-confirmed facts from proposed fields and preserving unresolved questions.
---

# Decision recorder

## Record safely

1. Read the workshop notes, evidence, ambiguity register, and relevant owner statements.
2. Create one YAML decision per distinct metric; do not merge by label similarity.
3. Set `owner_confirmed: true` only when the accountable owner explicitly confirmed the decision.
4. For an unconfirmed candidate, mark each allowed value explicitly:

   ```yaml
   definition:
     value: Candidate definition for owner review.
     proposed: true
   ```

5. Never convert silence, attendance, inferred ownership, or ambiguous wording into confirmation.
6. Preserve missing fields and open questions rather than filling them from general knowledge.

## Supported fields

Record `metric`, `status`, `owner`, `owner_confirmed`, `source_of_truth`, `definition`, `logic_formula`, `grain`, `time_basis`, `approved_use`, `not_approved_use`, `naming_decision`, `related_metrics`, `caveats`, and `review_cadence` when supported by the decision.

Do not set `status: Certified` unless owner confirmation is explicit and every required governance field is complete.
