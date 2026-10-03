CREATE TABLE claims (
  claim_id STRING,
  carrier STRING,
  claim_type STRING,
  channel STRING,
  opened_date STRING,
  cohort_month STRING,
  closed_date STRING,
  status STRING,
  missing_documents INTEGER,
  first_response_hours DECIMAL(12,2),
  cycle_days INTEGER,
  age_days INTEGER,
  paid_amount DECIMAL(14,2),
  sla_days INTEGER
) USING DELTA;

CREATE TABLE alerts (
  alert_id STRING,
  claim_id STRING,
  rule STRING,
  risk_score DECIMAL(6,4),
  reviewed INTEGER,
  confirmed_issue INTEGER,
  review_hours DECIMAL(12,2),
  days_in_queue INTEGER
) USING DELTA;

CREATE TABLE filing_experiment (
  user_id STRING,
  assigned_date STRING,
  variant STRING,
  channel STRING,
  completed_7d INTEGER,
  rework_7d INTEGER,
  support_contact_7d INTEGER
) USING DELTA;
