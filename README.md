# Metric Governance Agent

**A Git-native workflow for turning conflicting metric evidence into reviewable, governed definitions.**

Metric Governance Agent helps analytics and data teams move from “this dashboard says revenue” to an auditable definition with an owner, source of truth, usage boundaries, and decision history.

It scans lightweight evidence, exposes ambiguity, prepares stakeholder alignment materials, records Metric Decision Records (MDRs), publishes a catalog, and checks governance completeness. It does not decide business truth: only a confirmed metric owner can approve a definition.

## Why this exists

The same label—revenue, churn, active customer—often hides different formulas, grains, time bases, and intended uses. This project turns those disagreements into explicit, reviewable decisions without letting software invent business truth.

Use it when you want a lightweight, repository-based process before adopting—or alongside—a semantic layer or enterprise catalog. It is not a dashboard, a general-purpose data catalog, or an automatic certification engine.

```text
evidence → family map → ambiguity register → workshop pack
         → human decisions → MDRs → metric catalog → governance check
```

## Sample output

The worked revenue example turns scattered evidence into artifacts that stakeholders can review and approve.

### Ambiguity Register

> **Generic label: Revenue**  
> **Evidence:** “Revenue” appears across Finance exports, Sales SQL,
> Marketing pipeline reports, and the board pack.  
> **Risk:** One label may be hiding several different business meanings.  
> **Interpretation:** Sales usage appears closer to **booked revenue**.
> Marketing's “pipeline revenue” is not revenue and should likely be renamed
> **pipeline value**. Board and Finance usage still needs an accountable owner
> to confirm the intended definition before certification.  
> **Next step:** Review each variant with Finance, Sales, and Marketing; assign
> owners and keep legitimate variants separate.

### Metric Decision Record

> **Metric:** Pipeline Value  
> **Status:** Proposed  
> **Owner:** Marketing — confirmation required  
> **Definition:** Expected value of open sales opportunities represented in
> the marketing pipeline evidence. Exact stage, probability, and exclusion
> rules remain open.  
> **Naming decision:** Rename “pipeline revenue” to “pipeline value” to avoid
> presenting unbooked opportunities as revenue.  
> **Approved use:** Pipeline planning, subject to owner confirmation.  
> **Not approved use:** Financial reporting, recognised revenue, or board
> reporting as actual revenue.

### Business Metric Catalog

> **Booked Revenue** — Sales evidence appears to represent closed-won bookings;
> definition and owner confirmation remain required.  
> **Pipeline Value** — Proposed replacement for Marketing's “pipeline revenue”;
> never use as actual revenue.  
> **Board / Finance Revenue** — Not certified. The evidence does not yet prove
> whether this means gross, net, booked, or recognised revenue; an owner must
> confirm the definition and source of truth.

Run the workflow from the example project directory:

```console
$ cd examples/revenue
$ metricgov prepare
$ metricgov check
```

The example governance check reports failures because its MDRs are deliberately
left as drafts until owners confirm the missing definitions, grains, usage
boundaries, and review cadences. A generated draft is not a certified metric.
See the [complete worked example](examples/revenue/README.md).

## What v0.1 supports

Built-in metric families: `revenue`, `churn`, and `active_customer`.

Evidence formats: SQL, CSV, Markdown, text, and Excel (`.xlsx`/`.xlsm`) when the optional `openpyxl` dependency is installed.

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
| `metricgov record --from feedback/workshop_notes.md` | Draft MDRs from evidence and human feedback |
| `metricgov publish` | Generate CSV and Markdown catalogs from MDRs |
| `metricgov check` | Write a governance completeness report |
| `metricgov check --fail-on-error` | Also exit non-zero when definitions are incomplete |
| `metricgov prepare` | Run `scan → classify → workshop` |
| `metricgov finalize --from feedback/workshop_notes.md` | Run `record → publish → check` |

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

This produces draft MDRs under `decisions/`, catalogs under `catalog/`, and decision and completeness reports under `artifacts/`. Generated does not mean certified: review each MDR and only approve it after owner confirmation.

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
