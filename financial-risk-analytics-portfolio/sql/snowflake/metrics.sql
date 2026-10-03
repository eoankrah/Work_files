-- Platform adaptation: load typed curated inputs first. Not executed on a live snowflake account.
-- Canonical inputs: curated data, not the deliberately dirty raw feed.
-- Each view has one documented grain. Aggregate alerts before joining to claims.
CREATE OR REPLACE VIEW claims_metrics AS
SELECT carrier, claim_type, channel, cohort_month,
 COUNT(*) AS claim_count,
 SUM(CASE WHEN status='Closed' THEN 1 ELSE 0 END) AS closed_count,
 SUM(CASE WHEN status='Open' THEN 1 ELSE 0 END) AS backlog,
 SUM(CASE WHEN status='Open' AND age_days > sla_days THEN 1 ELSE 0 END) AS overdue_open,
 AVG(first_response_hours) AS avg_first_response_hours,
 AVG(cycle_days) AS avg_closed_cycle_days,
 SUM(missing_documents)*1.0/NULLIF(COUNT(*),0) AS missing_document_rate,
 SUM(CASE WHEN status='Closed' AND cycle_days <= sla_days THEN 1 ELSE 0 END)*1.0/
 NULLIF(SUM(CASE WHEN status='Closed' THEN 1 ELSE 0 END),0) AS closed_sla_rate,
 SUM(paid_amount) AS paid_amount
FROM claims GROUP BY carrier,claim_type,channel,cohort_month;
CREATE OR REPLACE VIEW risk_metrics AS
SELECT rule,COUNT(*) AS alert_count,SUM(reviewed) AS reviewed_count,
 SUM(CASE WHEN reviewed=0 THEN 1 ELSE 0 END) AS pending_count,
 SUM(CASE WHEN reviewed=1 THEN confirmed_issue ELSE 0 END) AS confirmed_count,
 SUM(CASE WHEN reviewed=1 THEN confirmed_issue ELSE 0 END)*1.0/NULLIF(SUM(reviewed),0) AS reviewed_confirmation_rate,
 AVG(review_hours) AS avg_review_hours,
 SUM(CASE WHEN reviewed=0 AND days_in_queue>7 THEN 1 ELSE 0 END) AS aged_pending
FROM alerts GROUP BY rule;
CREATE OR REPLACE VIEW experiment_metrics AS
SELECT variant,channel,COUNT(*) AS assigned_users,SUM(completed_7d) AS completions,
 AVG(completed_7d*1.0) AS completion_rate,
 AVG(rework_7d*1.0) AS rework_per_assigned_user,
 SUM(rework_7d)*1.0/NULLIF(SUM(completed_7d),0) AS rework_per_completion,
 AVG(support_contact_7d*1.0) AS support_contact_rate
FROM filing_experiment GROUP BY variant,channel;
CREATE OR REPLACE VIEW claim_alert_summary AS
SELECT claim_id,COUNT(*) AS alerts_per_claim,MAX(risk_score) AS max_risk_score
FROM alerts GROUP BY claim_id;
CREATE OR REPLACE VIEW claim_risk_join AS
SELECT c.*,COALESCE(a.alerts_per_claim,0) AS alerts_per_claim,a.max_risk_score
FROM claims c LEFT JOIN claim_alert_summary a ON c.claim_id=a.claim_id;
