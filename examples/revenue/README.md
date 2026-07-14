# Revenue governance example

This worked example shows how a generic “revenue” label can resolve into several related metric definitions without merging them merely because their names are similar.

## Run it

Install the package from the repository root, then:

```bash
cd examples/revenue
metricgov prepare
metricgov finalize --from feedback/workshop_decisions.yaml
metricgov change-plan
metricgov check
```

`prepare` scans `evidence/`, maps the revenue family, classifies ambiguity, and creates a workshop pack. `finalize` uses the structured decision to draft MDRs, publish the catalog, generate a dashboard change plan, and write the governance report. The explicit `change-plan` command above demonstrates that the plan can also be regenerated independently.

## Review the outputs

- `artifacts/01_evidence_log.csv` records what was found and where.
- `artifacts/02_metric_family_map.md` keeps revenue variants distinct.
- `artifacts/03_ambiguity_register.md` preserves risks and open alignment work.
- `artifacts/04_workshop_pack.md` turns ambiguity into stakeholder questions.
- `decisions/MDR-*.md` contains the metric decision records.
- `catalog/` contains the generated business-facing catalog.
- `artifacts/06_governance_check.md` reports completeness.
- `artifacts/07_dashboard_change_plan.md` identifies labels and evidence to rename or review.

These records illustrate the workflow; they are not certifications for another organization. Owners, definitions, sources, uses, caveats, and review cadence must be confirmed locally.

The command ends with `Governance check complete. Failures: 4`. This is expected: Pipeline Value is complete, while the other four sample MDRs remain incomplete until their owners confirm the missing definitions, grains, usage boundaries, and review cadences.

## Structured decision example

`feedback/workshop_decisions.yaml` contains one owner-confirmed decision for Pipeline Value. It populates the structured MDR and catalog fields and creates this change-plan row:

| Current Label | Recommended Label | Affected Evidence | Reason | Owner | Status |
|---|---|---|---|---|---|
| Pipeline Revenue | Pipeline Value | `marketing_pipeline.sql` | Owner-confirmed naming decision | Marketing | Ready to rename |

The plan does not change `marketing_pipeline.sql`; it gives an analyst an explicit implementation task. YAML values only populate fields when `owner_confirmed: true` or when an individual value is explicitly marked `proposed: true`.

To exercise the original free-text path instead, use `metricgov finalize --from feedback/workshop_notes.md`. Free-text notes remain snapshots and do not populate governed fields automatically.
