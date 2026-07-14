# Metric Governance Agent

**A Git-native workflow for turning conflicting metric evidence into reviewable, governed definitions.**

Metric Governance Agent helps analytics and data teams move from “this dashboard says revenue” to an auditable definition with an owner, source of truth, usage boundaries, and decision history.

It scans lightweight evidence, exposes ambiguity, prepares stakeholder alignment materials, records Metric Decision Records (MDRs), publishes a catalog, identifies affected dashboard and SQL labels, and checks governance completeness. It does not decide business truth: only a confirmed metric owner can approve a definition.

## What it produces

Metric Governance Agent turns messy metric evidence into a governed decision trail:

```text
messy evidence → ambiguity register → owner-confirmed decisions
               → MDRs → business metric catalog → dashboard change plan
```

| Stage | Artifact | Purpose |
|---|---|---|
| Discover ambiguity | Ambiguity Register | Shows where labels, sources, owners, or meanings do not align. |
| Prepare alignment | Workshop Pack | Gives analysts stakeholder questions and decision points. |
| Record decisions | Metric Decision Records | Captures confirmed definitions, naming decisions, caveats, and usage boundaries. |
| Publish definitions | Business Metric Catalog | Creates a cleaner metric dictionary from structured decisions. |
| Drive execution | Dashboard Change Plan | Identifies where old labels should be renamed or reviewed. |

From the worked revenue example:

- [Ambiguity Register](examples/revenue/artifacts/03_ambiguity_register.md)
- [Pipeline Value MDR](examples/revenue/decisions/MDR-004-pipeline-value.md)
- [Business Metric Dictionary](examples/revenue/catalog/business_metric_dictionary.md)
- [Dashboard Change Plan](examples/revenue/artifacts/07_dashboard_change_plan.md)

The agent does not automatically certify business truth. It exposes ambiguity, prepares decisions, and only fills governed catalog fields when owners confirm them.

## Why this exists

The same label—revenue, churn, active customer—often hides different formulas, grains, time bases, and intended uses. This project turns those disagreements into explicit, reviewable decisions without letting software invent business truth.

Use it when you want a lightweight, repository-based process before adopting—or alongside—a semantic layer or enterprise catalog. It is not a dashboard, a general-purpose data catalog, or an automatic certification engine.

```text
evidence → family map → ambiguity register → workshop pack
         → human decisions → MDRs → metric catalog
         → dashboard change plan → governance check
```

## Sample output

The worked revenue example produces draft governance artifacts from supplied evidence and workshop notes. The excerpts below reflect the generated files; unresolved fields remain `TBD` until owners confirm them.

### Ambiguity Register (excerpt)

| Type | Evidence | Risk / next step |
|---|---|---|
| `generic_label_without_certification` | Generic label 'Revenue' appears in 4 evidence rows. | The same label may hide multiple business meanings. Ask owners whether it should be split. |
| `same_label_multiple_sources` | 'Revenue' appears in `board_pack.md`, `finance_export.csv`, `marketing_pipeline.sql`, and `sales_dashboard.sql`. | Confirm source of truth, owner, and approved use. |
| `metric_family_has_multiple_variants` | Detected `booked_revenue`, `gross_revenue`, `net_revenue`, `pipeline_value`, and `recognised_revenue`. | Create distinct MDRs for legitimate variants. |
| `owner_gap` | Recognised revenue in `finance_export.csv` has no owner mentioned. | Identify the business owner before certification. |

The register identifies ambiguity and questions; it does not decide which definition is true.

### Metric Decision Record (excerpt)

```markdown
# MDR: Pipeline Value

## Status
Proposed

## Owner
Marketing

## Owner Confirmed
true

## Definition
Weighted value of open, qualified marketing-sourced opportunities.

## Source of Truth
mart.marketing_sourced_pipeline

## Approved Use
Pipeline planning and forecast discussion

## Naming Decision
Rename "Pipeline Revenue" to "Pipeline Value"
```

The structured fields are populated because this example decision explicitly records `owner_confirmed: true`; its status remains Proposed.

### Business Metric Catalog (excerpt)

| Metric | Status | Owner | Definition | Source of truth |
|---|---|---|---|---|
| Booked Revenue | Proposed | Sales Ops | TBD — requires owner confirmation. | `crm.opportunities` |
| Pipeline Value | Proposed | Marketing | Weighted value of open, qualified marketing-sourced opportunities. | `mart.marketing_sourced_pipeline` |
| Recognised Revenue | Proposed | Finance | TBD — requires owner confirmation. | Recognised Revenue |

The generated catalog is draft-first: it publishes proposed records and preserves missing confirmation instead of presenting them as certified definitions.

### Dashboard Change Plan (excerpt)

| Current Label | Recommended Label | Affected Evidence | Owner | Status |
|---|---|---|---|---|
| Pipeline Revenue | Pipeline Value | `marketing_pipeline.sql` | Marketing | Ready to rename |

The catalog defines the governed metric; the change plan identifies evidence, reports, dashboard labels, or SQL that should be renamed or reviewed. It never modifies those assets automatically.

Run it from the example project directory:

```console
$ cd examples/revenue
$ metricgov prepare
$ metricgov finalize --from feedback/workshop_decisions.yaml
$ metricgov change-plan
$ metricgov check
```

The check reports four expected failures: Pipeline Value is complete, while the other MDRs remain incomplete until owners confirm definitions, grains, usage boundaries, and review cadences. See the [complete worked example](examples/revenue/README.md).

## What v0.3 supports

Built-in metric families: `revenue`, `churn`, and `active_customer`.

Evidence formats: SQL, CSV, Markdown, text, and Excel (`.xlsx`/`.xlsm`) when the optional `openpyxl` dependency is installed.

v0.3 adds the Dashboard Change Plan: an actionable Markdown report that maps confirmed naming decisions to affected evidence. It is a review aid, not an automatic dashboard or SQL migration tool.

## Quick start

Requires Python 3.10 or later.

```bash
git clone <your-repo-url>
cd metric-governance-agent
python -m pip install -e .
```

`prepare` and `finalize` must be run inside a metric project directory—the directory containing `metric_context.json`. They are not repository-root commands.

The included worked example is in `examples/revenue`. From the repository root, try it with:

```bash
cd examples/revenue
metricgov prepare
metricgov finalize --from feedback/workshop_notes.md
```

Alternatively, create and enter a new directory, then initialize a revenue project:

```bash
mkdir my-revenue-governance
cd my-revenue-governance
metricgov init revenue
metricgov prepare
```

See [the revenue example](examples/revenue/README.md) for its artifacts and expected governance status.

## CLI reference

| Command | Purpose |
|---|---|
| `metricgov init revenue` | Initialize a project from a built-in metric family |
| `metricgov scan` | Scan files in `evidence/` and create an evidence log |
| `metricgov classify` | Create the metric family map and ambiguity register |
| `metricgov workshop` | Generate a stakeholder alignment workshop pack |
| `metricgov record --from feedback/workshop_notes.md` | Preserve free-text notes in draft MDRs |
| `metricgov record --from feedback/workshop_decisions.yaml` | Populate MDR fields from structured decisions |
| `metricgov publish` | Generate CSV and Markdown catalogs from MDRs |
| `metricgov change-plan` | Map naming decisions to affected evidence and labels |
| `metricgov check` | Write a governance completeness report |
| `metricgov check --fail-on-error` | Also exit non-zero when definitions are incomplete |
| `metricgov prepare` | Run `scan → classify → workshop` |
| `metricgov finalize --from feedback/workshop_notes.md` | Run `record → publish → change-plan → check` |

Run workflow commands from the metric project directory (the directory containing `metric_context.json`). The equivalent module form is `python -m metricgov.cli`.

## Governance workflow

Initialize a project, add SQL, notes, or sample exports under `evidence/`, and prepare the alignment artifacts:

```bash
mkdir my-churn-governance
cd my-churn-governance
metricgov init churn
metricgov prepare
```

This creates the evidence log, metric family map, ambiguity register, and workshop pack under `artifacts/`. Review them with the relevant owners and preserve decisions and unresolved questions in `feedback/workshop_notes.md`, then run:

```bash
metricgov finalize --from feedback/workshop_notes.md
```

This produces draft MDRs under `decisions/`, catalogs under `catalog/`, and decision, dashboard-change, and completeness reports under `artifacts/`. Generated does not mean certified: review each MDR and only approve it after owner confirmation.

### Free-text notes and structured decisions

Markdown workshop notes remain supported and are preserved as a feedback snapshot. They do not populate governed fields automatically:

```bash
metricgov record --from feedback/workshop_notes.md
```

Use YAML when stakeholders have made explicit, structured decisions:

```yaml
decisions:
  - metric: Pipeline Value
    status: Proposed
    owner: Marketing
    owner_confirmed: true
    source_of_truth: mart.marketing_sourced_pipeline
    definition: Weighted value of open, qualified opportunities.
    approved_use: Pipeline planning
    not_approved_use: Financial reporting as actual revenue
    naming_decision: Rename "Pipeline Revenue" to "Pipeline Value"
    related_metrics: [Booked Revenue, Recognised Revenue]
    caveats: [Pipeline value is not realised revenue.]
```

Run `metricgov record --from feedback/workshop_decisions.yaml`, or use the same path with `finalize`. Plain YAML field values are trusted only when `owner_confirmed: true`. For an unconfirmed decision, explicitly proposed fields use this form:

```yaml
definition:
  value: Candidate definition for stakeholder review.
  proposed: true
```

Certification is rejected unless the owner is confirmed and every required governance field is complete. Structured YAML also accepts `logic_formula`, `grain`, `time_basis`, and `review_cadence`, which are required for a complete definition. See the [revenue decision example](examples/revenue/feedback/workshop_decisions.yaml).

## Governance contract

Every certified definition must include an owner, definition, source of truth, formula, grain, time basis, approved and prohibited uses, caveats, related metrics, and review cadence. Similar names are never sufficient evidence that variants should be merged. Incomplete evidence and open questions remain explicit.

`metricgov check --fail-on-error` enforces field completeness and is suitable for CI when the checked project is expected to be complete. This repository's CI runs `metricgov check` without that flag because the worked example intentionally preserves unconfirmed fields. Neither form verifies that an owner truly approved a record; that remains a human review responsibility.

## Repository layout

```text
metricgov/             Python CLI
metric_packs/          Built-in discovery vocabulary
skills/                Seven-step agent workflow instructions
templates/             MDR and catalog templates
examples/revenue/      Worked example
tests/                 CLI smoke tests
.github/workflows/     CI configuration
```

See [ROADMAP.md](ROADMAP.md) for planned work. Licensed under the [MIT License](LICENSE).
