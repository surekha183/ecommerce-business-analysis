
CREATE OR REPLACE VIEW public.vw_delivery_kpi_summary AS
SELECT
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (
        WHERE eligible_delivery = TRUE
    ) AS eligible_delivered_orders,
    COUNT(*) FILTER (
        WHERE is_late = TRUE
    ) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE is_late = TRUE
        ) / NULLIF(
            COUNT(*) FILTER (
                WHERE eligible_delivery = TRUE
            ), 0
        ),
        2
    ) AS late_delivery_rate_pct
FROM public.orders;



--execute after executing above code

SELECT *
FROM public.vw_delivery_kpi_summary;
