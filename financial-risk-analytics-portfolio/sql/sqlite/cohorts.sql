-- Opening cohorts have different maturity; compare rates only after a common observation window.
SELECT cohort_month, COUNT(*) AS claims,
 SUM(CASE WHEN status='Closed' AND cycle_days<=30 THEN 1 ELSE 0 END)*1.0/COUNT(*) AS closed_within_30d_rate
FROM claims WHERE age_days>=30 GROUP BY cohort_month;
-- Compare document groups within type; descriptive association, not causal attribution.
SELECT claim_type,missing_documents,COUNT(*) AS claims,AVG(cycle_days) AS avg_closed_days
FROM claims GROUP BY claim_type,missing_documents;
