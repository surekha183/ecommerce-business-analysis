
CREATE OR REPLACE VIEW public.vw_state_monthly_delivery_performance AS
SELECT
    o.purchase_month,
    s.seller_state,
    COUNT(DISTINCT o.order_id) AS eligible_orders,
    COUNT(DISTINCT CASE
        WHEN o.is_late = TRUE THEN o.order_id
    END) AS late_orders,
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN o.is_late = TRUE THEN o.order_id
        END)
        / NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS late_delivery_rate_pct
FROM public.orders o
JOIN (
    SELECT DISTINCT order_id, seller_id
    FROM public.olist_order_items_dataset
) oi
    ON o.order_id = oi.order_id
JOIN public.olist_sellers_dataset s
    ON oi.seller_id = s.seller_id
WHERE o.eligible_delivery = TRUE
GROUP BY
    o.purchase_month,
    s.seller_state;
