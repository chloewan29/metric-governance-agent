# Revenue governance example

This worked example shows how a generic “revenue” label can resolve into several related metric definitions without merging them merely because their names are similar.

## Run it

Install the package from the repository root, then:

```bash
cd examples/revenue
metricgov prepare
metricgov finalize --from feedback/workshop_notes.md
metricgov check
```

`prepare` scans `evidence/`, maps the revenue family, classifies ambiguity, and creates a workshop pack. `finalize` uses workshop notes to draft MDRs, publish the catalog, and write the governance report.

## Review the outputs

- `artifacts/01_evidence_log.csv` records what was found and where.
- `artifacts/02_metric_family_map.md` keeps revenue variants distinct.
- `artifacts/03_ambiguity_register.md` preserves risks and open alignment work.
- `artifacts/04_workshop_pack.md` turns ambiguity into stakeholder questions.
- `decisions/MDR-*.md` contains the metric decision records.
- `catalog/` contains the generated business-facing catalog.
- `artifacts/06_governance_check.md` reports completeness.

These records illustrate the workflow; they are not certifications for another organization. Owners, definitions, sources, uses, caveats, and review cadence must be confirmed locally.

The command ends with `Governance check complete. Failures: 5`. This is expected: all five sample MDRs are intentionally draft and incomplete until their owners confirm the missing definitions, grains, usage boundaries, and review cadences. The example preserves those gaps instead of inventing business truth.

## Structured decision example

`feedback/workshop_decisions.yaml` contains one owner-confirmed decision for Pipeline Value. To populate its structured MDR and catalog fields, run:

```bash
metricgov finalize --from feedback/workshop_decisions.yaml
```

The structured decision makes Pipeline Value complete and reduces the governance report to `Failures: 4`. The other four revenue MDRs remain incomplete. YAML values only populate fields when `owner_confirmed: true` or when an individual value is explicitly marked `proposed: true`.
