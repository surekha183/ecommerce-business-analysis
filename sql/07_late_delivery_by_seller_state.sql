
-- Compare late-delivery rates by seller state.
-- Count each order once within each seller state.

WITH order_seller_states AS (
    SELECT DISTINCT
        oi.order_id,
        s.seller_state
    FROM public.orders AS o
    JOIN public.olist_order_items_dataset AS oi
        ON o.order_id = oi.order_id
    JOIN public.olist_sellers_dataset AS s
        ON oi.seller_id = s.seller_id
    WHERE o.eligible_delivery = TRUE
)

SELECT
    oss.seller_state,
    COUNT(DISTINCT o.order_id) AS eligible_orders,
    COUNT(DISTINCT CASE
        WHEN o.is_late = TRUE THEN o.order_id
    END) AS late_orders,
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN o.is_late = TRUE THEN o.order_id
        END) / COUNT(DISTINCT o.order_id),
        2
    ) AS late_delivery_rate_pct
FROM public.orders AS o
JOIN order_seller_states AS oss
    ON o.order_id = oss.order_id
GROUP BY oss.seller_state
HAVING COUNT(DISTINCT o.order_id) >= 100
ORDER BY late_delivery_rate_pct DESC;
