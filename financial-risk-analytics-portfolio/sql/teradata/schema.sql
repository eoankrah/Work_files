CREATE MULTISET TABLE claims (
  claim_id VARCHAR(16),
  carrier VARCHAR(30),
  claim_type VARCHAR(20),
  channel VARCHAR(20),
  opened_date VARCHAR(10),
  cohort_month VARCHAR(7),
  closed_date VARCHAR(10),
  status VARCHAR(10),
  missing_documents INTEGER,
  first_response_hours DECIMAL(12,2),
  cycle_days INTEGER,
  age_days INTEGER,
  paid_amount DECIMAL(14,2),
  sla_days INTEGER
) PRIMARY INDEX (claim_id);

CREATE MULTISET TABLE alerts (
  alert_id VARCHAR(16),
  claim_id VARCHAR(16),
  rule VARCHAR(30),
  risk_score DECIMAL(6,4),
  reviewed INTEGER,
  confirmed_issue INTEGER,
  review_hours DECIMAL(12,2),
  days_in_queue INTEGER
) PRIMARY INDEX (alert_id);

CREATE MULTISET TABLE filing_experiment (
  user_id VARCHAR(16),
  assigned_date VARCHAR(10),
  variant VARCHAR(12),
  channel VARCHAR(20),
  completed_7d INTEGER,
  rework_7d INTEGER,
  support_contact_7d INTEGER
) PRIMARY INDEX (user_id);
