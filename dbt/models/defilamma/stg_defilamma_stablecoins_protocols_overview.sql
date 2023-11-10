WITH raw AS (
SELECT * 
FROM `zeta-sol-396504.raw.defilamma_protocols` dp
WHERE dp.stablecoins IS NOT NULL)


SELECT 
    *
FROM raw