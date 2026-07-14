# Stakeholder Alignment Workshop Pack: Revenue

## Purpose

Align business stakeholders on what each metric variant means, who owns it, where it should be used, and what should be certified or deprecated.

## Pre-read summary

The scan identified metric evidence that requires human confirmation. The goal of the workshop is not to force one definition, but to decide which variants are legitimate, how they should be named, and which uses are approved.

## Current ambiguity register

# Ambiguity Register: Revenue

| Issue ID | Type | Evidence | Risk | Suggested next step |
|---|---|---|---|---|
| I001 | generic_label_without_certification | Generic label 'Revenue' appears in 4 evidence rows. | The same label may hide multiple business meanings. | Ask owners whether this should be split into more specific certified metrics. |
| I002 | same_label_multiple_sources | 'recognised revenue' appears in multiple files: board_pack.md, finance_export.csv. | Different reports may use the same label with different logic or ownership. | Confirm source of truth, owner, and approved use for this label. |
| I003 | same_label_multiple_sources | 'gross revenue' appears in multiple files: board_pack.md, finance_export.csv. | Different reports may use the same label with different logic or ownership. | Confirm source of truth, owner, and approved use for this label. |
| I004 | same_label_multiple_sources | 'net revenue' appears in multiple files: board_pack.md, finance_export.csv. | Different reports may use the same label with different logic or ownership. | Confirm source of truth, owner, and approved use for this label. |
| I005 | same_label_multiple_sources | 'Revenue' appears in multiple files: board_pack.md, finance_export.csv, marketing_pipeline.sql, sales_dashboard.sql. | Different reports may use the same label with different logic or ownership. | Confirm source of truth, owner, and approved use for this label. |
| I006 | metric_family_has_multiple_variants | Detected variants: booked_revenue, gross_revenue, net_revenue, pipeline_value, recognised_revenue. | Related metrics may be incorrectly merged or compared without caveats. | Create distinct Metric Decision Records for legitimate variants. |
| I007 | owner_gap | recognised revenue in finance_export.csv has no owner mentioned. | Metric cannot be certified without an accountable owner. | Identify the business owner before publishing as certified. |


## Stakeholder questions

### Finance

- Is official revenue booked, billed, recognised, collected, gross, or net?
- Are refunds, credits, tax, and FX adjustments included?
- Which date determines the reporting period?
- Is this the source of truth for Board or ELT reporting?

### Sales Ops

- Is sales revenue based on closed-won opportunity amount or signed contract value?
- How are cancellations, downgrades, and amendments handled?
- Should this metric be renamed Booked Revenue rather than Revenue?

### Marketing

- Is pipeline revenue open pipeline, weighted pipeline, or closed-won influenced value?
- Should it be labelled Pipeline Value rather than Revenue?

## Recommended agenda

1. Confirm the decision context for this metric family.
2. Review discovered metric variants and evidence.
3. Classify each variant: certify, rename, split, deprecate, or investigate.
4. Assign business owner and source of truth for each certified metric.
5. Confirm approved use and not-approved use.
6. Agree open questions, deadlines, and next review cadence.

## Decision options

- **Certify:** the metric has owner-confirmed definition, source, logic, grain, time basis, usage, and caveats.
- **Rename:** the current label is ambiguous and should be changed in reports.
- **Split:** one generic label should become multiple legitimate certified metrics.
- **Deprecate:** a label or report should no longer be used for decision-making.
- **Investigate:** evidence is insufficient for a decision.
