
-- Create a reusable monthly delivery-performance view

CREATE OR REPLACE VIEW public.vw_monthly_delivery_performance AS
SELECT
    purchase_month,
    COUNT(*) AS eligible_orders,
    COUNT(*) FILTER (
        WHERE is_late = TRUE
    ) AS late_orders,
    COUNT(*) FILTER (
        WHERE is_late = FALSE
    ) AS on_time_or_early_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE is_late = TRUE
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_rate_pct
FROM public.orders
WHERE eligible_delivery = TRUE
GROUP BY purchase_month;



--execute after executing above code

SELECT *
FROM public.vw_monthly_delivery_performance
ORDER BY purchase_month;
