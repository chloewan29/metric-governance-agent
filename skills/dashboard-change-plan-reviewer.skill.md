---
name: dashboard-change-plan-reviewer
description: Review artifacts/07_dashboard_change_plan.md for safe rename readiness, evidence-match quality, owner confirmation, broad-label risk, and actionable follow-up without modifying source assets.
---

# Dashboard change plan reviewer

## Review every row

1. Trace the naming decision to its MDR and `Owner Confirmed` section.
2. Verify current and recommended labels are parsed clearly.
3. Verify the affected evidence match is exact or high-confidence.
4. Verify the owner is explicitly known.
5. Explain why the row is **Ready to rename** or **Review required**.

Use **Ready to rename** only when all four checks pass: owner confirmation, clear labels, exact or high-confidence evidence match, and known owner.

Use **Review required** when any check fails. Treat broad labels such as `sale`, `sales`, `revenue`, `customer`, `user`, `active`, or `pipeline` as Review required unless explicit owner-confirmed context makes the intended reference unambiguous.

## Boundaries

- Never invent an owner or infer confirmation from a likely team.
- Never rewrite SQL, dashboards, reports, exports, or evidence automatically.
- Identify the asset, reason, responsible owner, verification step, and recommended human action.
