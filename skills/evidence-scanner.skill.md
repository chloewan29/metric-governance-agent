---
name: evidence-scanner
description: Review metric evidence and artifacts/01_evidence_log.csv for missing context, weak extraction, unsupported claims, and evidence gaps before metric ambiguity or decisions are assessed.
---

# Evidence scanner

## Review

1. Read `metric_context.json`, `artifacts/01_evidence_log.csv`, and the referenced evidence files.
2. Confirm that labels and captured logic are traceable to their source files.
3. Check for missing context:
   - formula, filters, exclusions, and joins
   - source table or field
   - grain and aggregation
   - time basis and timezone
   - currency, units, and population
   - owner or accountable team
   - report purpose and decision context
4. Flag unreadable, stale, sampled, or low-confidence evidence.
5. Keep conflicting evidence as separate rows; do not reconcile it by assumption.

## Output

- Separate observed facts from interpretations.
- List missing evidence and precise follow-up requests.
- Preserve file paths and evidence identifiers.
- Recommend the next scan or stakeholder action; do not certify a metric.
