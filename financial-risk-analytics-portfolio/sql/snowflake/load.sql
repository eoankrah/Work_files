-- Set a current database/schema and upload curated CSVs to this named stage.
CREATE OR REPLACE FILE FORMAT portfolio_csv TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' EMPTY_FIELD_AS_NULL=TRUE NULL_IF=('');
CREATE OR REPLACE STAGE portfolio_stage FILE_FORMAT=portfolio_csv;
-- Upload with Snowsight or your approved client; stage paths below must match uploaded names.
COPY INTO claims FROM @portfolio_stage/claims.csv;
COPY INTO alerts FROM @portfolio_stage/alerts.csv;
COPY INTO filing_experiment FROM @portfolio_stage/filing_experiment.csv;
-- Run metrics.sql, then:
SELECT carrier,MEDIAN(cycle_days) AS median_closed_days,
 PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY cycle_days) AS p90_closed_days
FROM claims WHERE status='Closed' GROUP BY carrier;
