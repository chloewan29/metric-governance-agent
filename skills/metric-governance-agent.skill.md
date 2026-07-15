---
name: metric-governance-agent
description: Apply the repository's metric governance principles when reviewing evidence, decisions, MDRs, catalogs, or change plans. Use for end-to-end metric governance work and whenever another metric skill needs the governing safety boundary.
---

# Metric governance agent

## Rules

- Do not invent definitions, formulas, owners, sources, approvals, or business truth.
- Do not mark a metric Certified without explicit owner confirmation and all required governance fields.
- Keep a metric family separate from each governed metric definition.
- Do not merge variants merely because their labels are similar.
- Distinguish evidence, inference, proposed decisions, and owner-confirmed decisions.
- Preserve source references, unresolved ambiguity, open questions, and decision history.
- State when evidence is incomplete.
- Produce reviewable Markdown, CSV, or YAML changes with actionable next steps.

## Workflow

1. Read `metric_context.json` and the relevant generated artifacts.
2. Trace every recommendation to evidence or explicit stakeholder input.
3. Label uncertain judgments as proposed or Review required.
4. Keep required fields incomplete rather than guessing.
5. Tell the analyst what needs human confirmation and what command or review comes next.
