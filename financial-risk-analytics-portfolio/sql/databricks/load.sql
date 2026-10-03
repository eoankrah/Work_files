-- Runtime 13.3 LTS+; replace the volume path with an accessible Unity Catalog volume.
-- Run schema.sql first. Explicit schemas prevent numeric fields being inferred as strings.
INSERT INTO claims SELECT * FROM read_files('/Volumes/catalog/schema/portfolio/claims.csv',format=>'csv',header=>true,schema=>'claim_id STRING, carrier STRING, claim_type STRING, channel STRING, opened_date STRING, cohort_month STRING, closed_date STRING, status STRING, missing_documents INT, first_response_hours DECIMAL(12,2), cycle_days INT, age_days INT, paid_amount DECIMAL(14,2), sla_days INT');
INSERT INTO alerts SELECT * FROM read_files('/Volumes/catalog/schema/portfolio/alerts.csv',format=>'csv',header=>true,schema=>'alert_id STRING, claim_id STRING, rule STRING, risk_score DECIMAL(6,4), reviewed INT, confirmed_issue INT, review_hours DECIMAL(12,2), days_in_queue INT');
INSERT INTO filing_experiment SELECT * FROM read_files('/Volumes/catalog/schema/portfolio/filing_experiment.csv',format=>'csv',header=>true,schema=>'user_id STRING, assigned_date STRING, variant STRING, channel STRING, completed_7d INT, rework_7d INT, support_contact_7d INT');
-- Empty numeric CSV fields must map to NULL. Confirm imported counts before running metrics.sql.
SELECT carrier,median(cycle_days) AS median_closed_days FROM claims WHERE status='Closed' GROUP BY carrier;
