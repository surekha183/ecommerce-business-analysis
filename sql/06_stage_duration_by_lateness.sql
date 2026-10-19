
-- Compare average stage durations for late and on-time orders.

SELECT
    CASE
        WHEN is_late = TRUE THEN 'Late'
        WHEN is_late = FALSE THEN 'On-time or early'
    END AS delivery_result,

    COUNT(*) AS eligible_orders,

    ROUND(AVG(purchase_to_approval_hours)::numeric, 2)
        AS avg_purchase_to_approval_hours,

    ROUND(AVG(approval_to_carrier_hours)::numeric, 2)
        AS avg_approval_to_carrier_hours,

    ROUND(AVG(carrier_to_delivery_hours)::numeric, 2)
        AS avg_carrier_to_delivery_hours

FROM public.orders
WHERE eligible_delivery = TRUE
GROUP BY is_late
ORDER BY is_late DESC;
