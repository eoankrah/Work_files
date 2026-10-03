# Tableau dashboard build guide
The working offline dashboard is `dashboard/index.html`. This guide builds a native Tableau counterpart; no native workbook is claimed to have been executed.

## Sources and grain
Connect directly to `data/curated/claims.csv`, `alerts.csv`, and `filing_experiment.csv` as separate data sources. Alternatively use `outputs/claims_metrics.csv`, `risk_metrics.csv`, and `experiment_metrics.csv`; those are aggregated, so use weighted ratios rather than averaging rates. Keep claims and alerts separate, or use `outputs/claim_risk_join.csv`, already reduced to one row per claim. A physical join of raw alerts to claims inflates claim measures.

## Calculations for the claim-level CSV
- Backlog: `SUM(IF [status] = "Open" THEN 1 ELSE 0 END)`
- Closed count: `SUM(IF [status] = "Closed" THEN 1 ELSE 0 END)`
- Missing document rate: `SUM([missing_documents]) / COUNT([claim_id])`
- Median closed cycle: `MEDIAN(IF [status] = "Closed" THEN [cycle_days] END)`
- P90 closed cycle: `PERCENTILE(IF [status] = "Closed" THEN [cycle_days] END, 0.9)`
- SLA rate: `SUM(IF [status] = "Closed" AND [cycle_days] <= [sla_days] THEN 1 ELSE 0 END) / SUM(IF [status] = "Closed" THEN 1 ELSE 0 END)`
- Overdue backlog: `SUM(IF [status] = "Open" AND [age_days] > [sla_days] THEN 1 ELSE 0 END)`
- Alert confirmation: `SUM(IF [reviewed] = 1 THEN [confirmed_issue] ELSE 0 END) / SUM([reviewed])`
- ITT completion: `SUM([completed_7d]) / COUNT([user_id])`

Set numeric types explicitly; blank cycle_days is NULL, not zero. Format rates as percentages. Use COUNTD to verify key uniqueness, not to hide duplicate ingestion.

## Layout
1. Claims: top KPI strip, missing-documents by channel, cohort trend, claim-type cycle distribution, backlog table. Carrier/type/channel filters apply to all claim sheets.
2. Risk: alert counts by rule, confirmation among reviewed, review effort, pending over seven days. Do not apply claim filters without explicit relationships and denominators.
3. Experiment: completion by variant and channel, assigned counts, CI and lift from `outputs/summary.json`, rework and support guardrails. Label all data synthetic.

Use a 1,200 × 800 dashboard, white background, navy text and blue bars. Publish only after confirming public extracts contain synthetic data. Validate Tableau totals against summary.json and the Python exports.
