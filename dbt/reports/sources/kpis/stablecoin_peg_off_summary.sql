DECLARE peg_limit FLOAT64 DEFAULT 0.95;
DECLARE circulating_min_limit FLOAT64 DEFAULT 20000000;

WITH current_price AS (

    SELECT 
        sp.stablecoin,
        sp.prices,
        ROW_NUMBER() OVER (PARTITION BY sp.stablecoin ORDER BY sp.date DESC) AS rn,
    FROM `raw.defilamma_stables_prices` sp
)


, days_peg_off AS (
    SELECT
        sp.stablecoin,
        SUM(1) AS days_peg_off
    FROM `raw.defilamma_stables_prices` sp
    WHERE sp.prices <= peg_limit
    GROUP BY 1
)



, ext_peg_off AS (
SELECT
    
    sp.stablecoin,
    DATE(max(sp.date)) AS last_peg_off_date,
    DATE_DIFF(CURRENT_DATE(), DATE(max(sp.date)), DAY) AS days_since_last_peg_off,
    DATE_DIFF(CURRENT_DATE(), DATE(min(sp.date)), DAY) AS days_since_first_peg_off,
    min(sp.prices) AS lowest_price,
    max(cp.rn) AS last_rnk
FROM `raw.defilamma_stables_prices` sp
LEFT JOIN current_price cp
ON sp.stablecoin = cp.stablecoin
WHERE sp.prices <= peg_limit AND cp.rn = 1
GROUP BY 1)

SELECT 
    epo.*,
    s.peg_mechanism,
    s.peg_type,
    dpo.days_peg_off,
    CASE
        WHEN s.price <= peg_limit THEN "off"
        ELSE "on"
    END AS current_peg_flag,
    s.price AS current_price,
    s.circulating AS current_circulating_supply
FROM ext_peg_off epo
LEFt JOIN `raw.defilamma_stables` s
ON epo.stablecoin = s.gecko_id

LEFT JOIN days_peg_off dpo
ON epo.stablecoin = dpo.stablecoin

WHERE s.circulating >= circulating_min_limit
AND s.peg_type= 'peggedUSD'
ORDER BY current_price DESC