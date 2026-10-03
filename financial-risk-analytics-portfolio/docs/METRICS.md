# Metric contract
Snapshot: 2026-10-01. Claims opened Apr–Sep 2026. Dates are day-grain; hours are precomputed synthetic values. This portfolio is not a financial reporting or regulatory model.

| Metric | Numerator or measure | Denominator / eligibility | Interpretation |
|---|---|---|---|
| Backlog | Open claims at snapshot | One row per claim | Stock, not monthly inflow |
| Overdue open | Open and age_days > sla_days | Open claims; count shown | Demonstration SLA by type |
| Closed cycle median/P90 | Closure date minus opening date | Closed claims only | Open cases excluded; selection/censoring limits comparisons |
| Closed SLA attainment | Closed within type SLA | All closed claims | Different type mix can change rate |
| Missing-document rate | missing_documents = 1 | All selected claims | Workflow flag, not causal proof |
| Confirmation rate | confirmed_issue = 1 | Reviewed alerts only | Not population fraud prevalence or recall |
| Aged pending | Unreviewed and queue age > 7 | Pending alerts; count shown | Demo queue threshold |
| Filing completion | Completed within 7 days | All assigned unique users | Intention-to-treat, includes noncompleters |
| Absolute lift | Guided rate minus control rate | Assigned users by variant | Percentage points, distinct from relative percent lift |
| Rework / assigned | User has completed filing requiring rework | All assigned users | Includes conversion effect |
| Rework / completion | Completed filing requiring rework | Completed users only | Post-treatment selection; exploratory |
| Support contact | Any contact within 7 days | All assigned users | Binary per user, not contact volume |
| 30-day cohort closure | Closed within 30 days | Claims with age >= 30 | Consistent observation horizon |

Zero denominators produce NULL in SQL and N/A for primary dashboard rates. SQL AVG ignores NULL. Do not average already aggregated percentages; divide summed numerator by summed denominator.
