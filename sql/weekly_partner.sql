-- Weekly trips and base payout per partner (input to tier back-test)
SELECT
    partner_id,
    strftime('%Y-%W', trip_date) AS week,
    COUNT(*)                     AS trips,
    ROUND(SUM(base_payout), 2)   AS base_payout
FROM trips
WHERE distance_km > 0
GROUP BY partner_id, week;
