WITH raw AS (
SELECT * 
FROM `zeta-sol-396504.raw.defilamma_protocols` dp
WHERE dp.stablecoins IS NOT NULL)


SELECT
  ARRAY_LENGTH(JSON_EXTRACT_ARRAY(raw.stablecoins)) AS total_stable_coins,
  COUNT(raw.id) AS total_number_of_protocols
FROM raw
GROUP BY 1