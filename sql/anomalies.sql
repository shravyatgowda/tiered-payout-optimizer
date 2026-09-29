-- Edge cases: paid more than the rule allows, or paid for zero distance
SELECT
    CASE WHEN distance_km = 0 THEN 'zero_distance_paid'
         ELSE 'payout_above_rule' END AS issue,
    COUNT(*)                          AS trips,
    ROUND(SUM(paid_payout - base_payout), 2) AS excess_payout
FROM trips
WHERE paid_payout > base_payout + 0.01 OR distance_km = 0
GROUP BY issue;
