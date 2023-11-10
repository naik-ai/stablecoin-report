{{ config(materialized='table', sort='launch_date') }}

WITH raw AS (
  SELECT 
    sh.id,
    sh.peg_mechanism,
    min(sh.date) AS launch_date
  FROM `raw.defilamma_stables_history` sh
  GROUP BY 1,2
)

SELECT 
  TIMESTAMP_SECONDS(r.launch_date) AS launch_date, 
  r.peg_mechanism, 
  COUNT(r.id) AS stablecoins
FROM raw r
GROUP BY 1,2
ORDER BY 1