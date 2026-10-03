# Platform execution and validation status

| Platform | Delivered | Validation |
|---|---|---|
| Python | Seeded generation, SQLite runner, statistical analysis, exports, HTML builder | Executed locally |
| SQLite | Metric views, cohort and quality queries | Metric views executed; fixture tests included |
| SAS | Explicit CSV DATA steps, PROC SQL aggregates, PROC MEANS, CSV export | Adaptation; licensed runtime unavailable |
| Teradata | Typed DDL, metric views, import instructions | Adaptation; live account unavailable |
| Snowflake | Typed DDL, stage/load SQL, views, percentile examples | Adaptation; live account unavailable |
| Databricks | Delta DDL, read_files ingestion, metric views | Adaptation; live account unavailable |
| Tableau | CSV sources, calculations, layout and reconciliation guide | Build recipe; native workbook not executed |
| Browser dashboard | Offline embedded data and carrier/type/channel filtering | Generated; inspect locally with no server or external dependencies |

Run schemas in an empty dedicated demo namespace. Loading again appends rows, so clear/recreate demo tables deliberately before repeat ingestion. Account names, volume paths and permissions are environment-specific. Do not point scripts at production tables. Date strings are ISO; prepared cycle/age measures keep this demonstration portable. Warehouse deployment should recompute these measures from typed source timestamps under documented snapshot and timezone rules.

## Official references
- Snowflake DATEDIFF: https://docs.snowflake.com/en/sql-reference/functions/datediff
- Snowflake MEDIAN: https://docs.snowflake.com/en/sql-reference/functions/median
- Snowflake PERCENTILE_CONT: https://docs.snowflake.com/en/sql-reference/functions/percentile_cont
- Databricks read_files: https://docs.databricks.com/aws/en/sql/language-manual/functions/read_files
- Databricks median: https://docs.databricks.com/gcp/en/sql/language-manual/functions/median

Dates checked October 3, 2026. References explain syntax; they are not evidence that the adaptations have run in a live warehouse.
