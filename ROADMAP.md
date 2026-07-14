# Roadmap

Metric Governance Agent will stay focused on evidence, alignment, human decisions, and auditable publication. The roadmap does not include automatic certification of business truth.

## Shipped in v0.2 — Structured decisions

- Accept owner-confirmed workshop decisions in YAML.
- Populate MDR and catalog fields only from confirmed or explicitly proposed values.
- Prevent certification without owner confirmation and complete required fields.

## Shipped in v0.3 — Dashboard Change Plan

- Translate recorded naming decisions into an actionable Markdown change plan.
- Match old labels to captured evidence conservatively.
- Mark confirmed matches ready to rename and uncertain matches for review.
- Never rewrite dashboards, reports, SQL, or evidence automatically.

## Next — Safer authoring

- Validate MDR structure and status with a machine-readable schema.
- Distinguish owner-confirmed approval from field completeness in checks.
- Add dry-run and output-directory options.
- Improve diagnostics for unreadable or unsupported evidence.
- Package metric packs so installed wheels work outside a source checkout.

## Later — Extensibility

- Support user-defined metric packs and organization-specific governance rules.
- Add structured YAML decision records alongside Markdown.
- Provide import/export adapters for common semantic-layer and catalog formats.
- Expand tests across supported Python versions and operating systems.

## Longer term

- Track definition changes and review due dates.
- Produce migration plans for renamed, split, or deprecated metrics.
- Add optional integrations only where decisions remain reviewable and human-owned.

## Not planned

- Inferring and certifying a “correct” definition without owner confirmation.
- Merging variants based only on similar names.
- Requiring sensitive row-level business data.

Suggestions and pull requests should preserve the governance rules in `AGENTS.md`.
