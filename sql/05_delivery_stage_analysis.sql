
-- Compare average duration across delivery stages.
-- Negative and missing durations are excluded from averages.

SELECT
    'Purchase to approval' AS delivery_stage,
    COUNT(purchase_to_approval_hours) AS valid_orders,
    ROUND(AVG(purchase_to_approval_hours)::numeric, 2)
        AS average_hours
FROM public.orders
WHERE purchase_to_approval_hours >= 0

UNION ALL

SELECT
    'Approval to carrier handoff' AS delivery_stage,
    COUNT(approval_to_carrier_hours) AS valid_orders,
    ROUND(AVG(approval_to_carrier_hours)::numeric, 2)
        AS average_hours
FROM public.orders
WHERE approval_to_carrier_hours >= 0

UNION ALL

SELECT
    'Carrier to customer delivery' AS delivery_stage,
    COUNT(carrier_to_delivery_hours) AS valid_orders,
    ROUND(AVG(carrier_to_delivery_hours)::numeric, 2)
        AS average_hours
FROM public.orders
WHERE carrier_to_delivery_hours >= 0;
