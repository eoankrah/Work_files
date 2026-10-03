-- Load data/raw/claims_ingest.csv into a separate claims_ingest table.
SELECT claim_id,COUNT(*) AS occurrences FROM claims_ingest GROUP BY claim_id HAVING COUNT(*)>1;
SELECT * FROM claims_ingest WHERE carrier IS NULL OR carrier='';
SELECT * FROM claims_ingest WHERE paid_amount<0;
-- Do not deduplicate without defining a trusted version timestamp or source priority.
