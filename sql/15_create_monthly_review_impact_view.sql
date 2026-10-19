
CREATE OR REPLACE VIEW public.vw_delivery_review_impact_monthly AS
WITH review_per_order AS (
    SELECT
        order_id,
        AVG(review_score::numeric) AS average_review_score
    FROM public.olist_order_reviews_dataset
    GROUP BY order_id
),
order_reviews AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp)::date AS purchase_month,
        CASE
            WHEN o.is_late THEN 'Late'
            ELSE 'On-time or early'
        END AS delivery_result,
        o.order_id,
        r.average_review_score
    FROM public.orders o
    LEFT JOIN review_per_order r
        ON o.order_id = r.order_id
    WHERE o.eligible_delivery = TRUE
)
SELECT
    purchase_month,
    delivery_result,
    COUNT(*) AS eligible_orders,
    COUNT(average_review_score) AS orders_with_reviews,
    ROUND(AVG(average_review_score), 2) AS average_review_score,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE average_review_score <= 2
        ) / NULLIF(COUNT(average_review_score), 0),
        2
    ) AS low_review_rate_pct
FROM order_reviews
GROUP BY purchase_month, delivery_result
ORDER BY purchase_month, delivery_result;



--execute after executing above code

SELECT *
FROM public.vw_delivery_review_impact_monthly
ORDER BY purchase_month, delivery_result
LIMIT 10;
