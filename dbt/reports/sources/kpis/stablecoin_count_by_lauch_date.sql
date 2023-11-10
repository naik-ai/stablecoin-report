with raw AS (
    SELECT
        DATE(launch_date) AS launch_date
        , peg_mechanism
        , stablecoins
        , sum(stablecoins) OVER ()  AS total_stablecoins
        , MAX(DATE(launch_date)) OVER (PARTITION BY peg_mechanism) AS last_launch_date
    FROM `zeta-sol-396504.stablecoins.defilamma_stablecoins_launch_count`
    ORDER BY 1 DESC
    )

SELECT 
    r.peg_mechanism,
    r.total_stablecoins,
    DATE_DIFF(CURRENT_DATE(), r.last_launch_date, DAY) AS days_since_last_lauch,
    SUM(r.stablecoins) AS stablecoins
FROM raw r
GROUP BY 1,2,3