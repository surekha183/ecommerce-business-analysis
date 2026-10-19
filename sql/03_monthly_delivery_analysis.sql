
-- Analyze late deliveries by purchase month
SELECT
    purchase_month,
    COUNT(*) AS eligible_orders,
    SUM(CASE WHEN is_late = TRUE THEN 1 ELSE 0 END)
        AS late_orders,
    ROUND(
        100.0 * SUM(CASE WHEN is_late = TRUE THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS late_delivery_rate_pct
FROM public.orders
WHERE eligible_delivery = TRUE
GROUP BY purchase_month
ORDER BY purchase_month;
