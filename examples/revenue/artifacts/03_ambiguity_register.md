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
