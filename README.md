# Metric Governance Agent

**Stop arguing about which business metric is right.**

Metric Governance Agent helps analysts turn messy metric evidence—SQL, notes, exports, and report labels—into structured metric decisions, catalog entries, and dashboard change plans.

## The problem

One company can use “revenue” to mean several different things:

| Team / source | Label used | What it might mean |
|---|---|---|
| Finance export | Revenue | Recognised revenue |
| Sales SQL | Revenue | Closed-won bookings |
| Marketing report | Pipeline Revenue | Future opportunity value |
| Board pack | Revenue | Undefined executive metric |
| Excel export | Net Revenue | Revenue after deductions |

The issue is not that every version is wrong. The issue is that the labels, owners, approved uses, and definitions are not aligned.

Metric Governance Agent finds those gaps and prepares them for people to resolve. It does not automatically certify business truth.

## What it produces

| Output | Purpose |
|---|---|
| Ambiguity Register | Shows where metric labels, sources, owners, or meanings do not align. |
| Workshop Pack | Gives analysts stakeholder questions and decision points. |
| Metric Decision Records | Capture owner-confirmed definitions, naming decisions, caveats, and usage boundaries. |
| Business Metric Catalog | Publishes cleaner metric definitions from structured decisions. |
| Dashboard Change Plan | Identifies where old report labels should be renamed or reviewed. |

A **Metric Decision Record (MDR)** is an auditable record of what a metric means, who owns it, where it comes from, and where it should—or should not—be used.

The agent exposes ambiguity, prepares decisions, records owner-confirmed inputs, and generates governance artifacts. Only a confirmed metric owner can approve a definition.

## Install

Requires Python 3.10 or later.

```bash
git clone https://github.com/chloewan29/metric-governance-agent.git
cd metric-governance-agent
python -m pip install -e .
```

## How do I actually use this?

There are two different paths: run the demo to inspect the outputs, or create a separate project for a metric your organization needs to govern.

### Path 1: Try the worked example

Use this path only to see the generated artifacts quickly. From the repository root:

```bash
cd examples/revenue
metricgov prepare
metricgov finalize --from feedback/workshop_decisions.yaml
metricgov check
```

If you only want to see what the tool creates, browse [`examples/revenue`](examples/revenue/README.md):

- [Ambiguity Register](examples/revenue/artifacts/03_ambiguity_register.md)
- [Pipeline Value MDR](examples/revenue/decisions/MDR-004-pipeline-value.md)
- [Business Metric Dictionary](examples/revenue/catalog/business_metric_dictionary.md)
- [Dashboard Change Plan](examples/revenue/artifacts/07_dashboard_change_plan.md)

The example has one complete, owner-confirmed Pipeline Value decision. Its other four MDRs intentionally remain incomplete, so `Governance check complete. Failures: 4` is expected.

### Path 2: Use it on your own metric

1. Create and enter a new project directory, then initialize a supported metric family:

   ```bash
   mkdir my-metric-governance
   cd my-metric-governance

   metricgov init revenue
   # Or: metricgov init churn
   # Or: metricgov init active_customer
   ```

2. Add messy evidence files to `evidence/`. Useful inputs include:

   - a SQL query
   - a CSV or Excel export
   - a dashboard label list
   - meeting notes
   - Markdown notes

3. Scan and classify the evidence, then generate the workshop material:

   ```bash
   metricgov prepare
   ```

4. Review the discovery outputs:

   - `artifacts/03_ambiguity_register.md`
   - `artifacts/04_workshop_pack.md`

5. Meet with the relevant business owners—such as Finance, Sales, Product, Marketing, or Customer Success—to resolve definitions, ownership, naming, and approved uses.

6. Record the owner-confirmed outcomes in `feedback/workshop_decisions.yaml`.

7. Generate the MDRs, catalog, change plan, and governance report:

   ```bash
   metricgov finalize --from feedback/workshop_decisions.yaml
   metricgov check
   ```

8. Review the final outputs:

   - `decisions/*.md`
   - `catalog/business_metric_dictionary.md`
   - `artifacts/07_dashboard_change_plan.md`
   - `artifacts/06_governance_check.md`

The agent does not replace the business meeting. It prepares the evidence, structures decisions, and records confirmed outcomes.

## How it works

```text
messy evidence
→ ambiguity register
→ stakeholder workshop
→ owner-confirmed decisions
→ Metric Decision Records
→ business metric catalog
→ dashboard change plan
→ governance check
```

The catalog defines governed metrics. The Dashboard Change Plan identifies evidence, SQL, and report labels that should be renamed or reviewed; it never modifies those assets automatically.

## Using with coding agents

The CLI generates the evidence, decision, catalog, and change-plan artifacts. The guides in [`skills/`](skills/README.md) help Codex, Claude Code, and other coding agents review, refine, or extend those artifacts consistently.

Run the CLI first, then ask the agent to apply a specific skill—for example, use [`dashboard-change-plan-reviewer.skill.md`](skills/dashboard-change-plan-reviewer.skill.md) to review rename readiness. Humans still confirm business truth and approve governed definitions.

## Free-text notes or structured decisions

Use Markdown for unstructured workshop notes. The text is preserved in draft MDRs but does not automatically populate governed fields:

```bash
metricgov record --from feedback/workshop_notes.md
```

Use YAML when stakeholders have made explicit decisions:

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

Plain YAML values populate MDR fields only when `owner_confirmed: true`. An unconfirmed value must be explicitly proposed:

```yaml
definition:
  value: Candidate definition for stakeholder review.
  proposed: true
```

Certification is rejected unless the owner is confirmed and all required governance fields are complete. See the [structured revenue decision](examples/revenue/feedback/workshop_decisions.yaml).

## What this is—and is not

This is a lightweight, Git-friendly workflow for analysts, BI managers, and analytics leads. It creates reviewable Markdown and CSV artifacts that teams can diff, discuss, and approve.

It is not:

- an automatic source of business truth
- a dashboard or enterprise data catalog
- a replacement for Finance or metric-owner approval
- an automatic SQL, dashboard, Power BI, Salesforce, or Tableau migration tool
- a reason to upload sensitive row-level customer data

Prefer metadata, SQL, sample headers, and notes over raw sensitive data.

## Supported metric packs and evidence

Built-in metric families:

- `revenue`
- `churn`
- `active_customer`

Evidence formats:

- SQL, CSV, Markdown, and text
- Excel (`.xlsx` and `.xlsm`) with the optional `openpyxl` dependency

## Governance rules

- Never certify a metric without owner confirmation.
- Never merge variants only because their names are similar.
- Keep metric families separate from certified definitions.
- Preserve incomplete evidence and open questions.
- Every certified definition needs an owner, definition, source of truth, formula, grain, time basis, approved and prohibited uses, caveats, related metrics, and review cadence.

`metricgov check --fail-on-error` returns a non-zero exit code when required fields are incomplete. It checks completeness; it cannot prove that a human owner genuinely approved a record.

## CLI reference

| Command | Purpose |
|---|---|
| `metricgov init revenue` | Initialize a project from a built-in metric family. |
| `metricgov scan` | Scan `evidence/` and create the evidence log. |
| `metricgov classify` | Create the metric family map and ambiguity register. |
| `metricgov workshop` | Generate a stakeholder workshop pack. |
| `metricgov record --from feedback/workshop_notes.md` | Preserve free-text notes in draft MDRs. |
| `metricgov record --from feedback/workshop_decisions.yaml` | Populate MDR fields from structured decisions. |
| `metricgov publish` | Generate CSV and Markdown catalogs from MDRs. |
| `metricgov change-plan` | Map naming decisions to affected evidence and labels. |
| `metricgov check` | Write a governance completeness report. |
| `metricgov check --fail-on-error` | Also fail the command when definitions are incomplete. |
| `metricgov prepare` | Run `scan → classify → workshop`. |
| `metricgov finalize --from <file>` | Run `record → publish → change-plan → check`. |

The equivalent module form is `python -m metricgov.cli`.

## Project structure

```text
metricgov/             Python CLI
metric_packs/          Built-in discovery vocabulary
skills/                Seven-step governance workflow
templates/             MDR and catalog templates
examples/revenue/      Worked revenue example
tests/                 CLI tests
.github/workflows/     CI configuration
```

## Roadmap and limitations

See [ROADMAP.md](ROADMAP.md) for planned work. Current matching and naming-decision parsing are intentionally simple and conservative: unclear or unmatched changes are marked for review instead of guessed.

Licensed under the [MIT License](LICENSE).
