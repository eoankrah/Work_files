/* SAS 9.4 adaptation; set repo to your extracted directory. Not run in a licensed SAS environment. */
%let repo=/your/path/financial-risk-analytics-portfolio;
data claims;
 length claim_id $16 carrier $30 claim_type $20 channel $20 opened_date $10 cohort_month $7 closed_date $10 status $10;
 infile "&repo./data/curated/claims.csv" dsd dlm="," firstobs=2 truncover;
 input claim_id :$16. carrier :$30. claim_type :$20. channel :$20. opened_date :$10. cohort_month :$7. closed_date :$10. status :$10. missing_documents :best32. first_response_hours :best32. cycle_days :best32. age_days :best32. paid_amount :best32. sla_days :best32.;
run;
data alerts;
 length alert_id $16 claim_id $16 rule $30;
 infile "&repo./data/curated/alerts.csv" dsd dlm="," firstobs=2 truncover;
 input alert_id :$16. claim_id :$16. rule :$30. risk_score :best32. reviewed :best32. confirmed_issue :best32. review_hours :best32. days_in_queue :best32.;
run;
data filing_experiment;
 length user_id $16 assigned_date $10 variant $12 channel $20;
 infile "&repo./data/curated/filing_experiment.csv" dsd dlm="," firstobs=2 truncover;
 input user_id :$16. assigned_date :$10. variant :$12. channel :$20. completed_7d :best32. rework_7d :best32. support_contact_7d :best32.;
run;
proc sql;
 create table claims_metrics as
 select carrier,claim_type,channel,cohort_month,count(*) as claim_count,
 sum(status='Closed') as closed_count,sum(status='Open') as backlog,
 mean(cycle_days) as avg_closed_cycle_days,mean(missing_documents) as missing_document_rate,
 sum(status='Closed' and cycle_days <= sla_days and not missing(cycle_days)) /
 sum(status='Closed') as closed_sla_rate
 from claims group by carrier,claim_type,channel,cohort_month;
 create table risk_metrics as
 select rule,count(*) as alert_count,sum(reviewed) as reviewed_count,
 sum(confirmed_issue)/sum(reviewed) as reviewed_confirmation_rate
 from alerts group by rule;
 create table experiment_metrics as
 select variant,count(*) as assigned_users,mean(completed_7d) as completion_rate
 from filing_experiment group by variant;
quit;
proc means data=claims median p90; where status='Closed'; var cycle_days; run;
proc export data=claims_metrics outfile="&repo./outputs/sas_claims_metrics.csv" dbms=csv replace; run;
