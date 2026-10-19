
-- Prepare review impact metrics for Power BI

CREATE OR REPLACE VIEW public.vw_delivery_review_impact AS

WITH review_per_order AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score
    FROM public.olist_order_reviews_dataset
    GROUP BY order_id
)

SELECT
    CASE
        WHEN o.is_late = TRUE THEN 'Late'
        WHEN o.is_late = FALSE THEN 'On-time or early'
    END AS delivery_result,

    COUNT(*) AS eligible_orders,

    COUNT(r.review_score) AS orders_with_reviews,

    ROUND(AVG(r.review_score)::numeric, 2)
        AS average_review_score,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE r.review_score <= 2
        ) / NULLIF(COUNT(r.review_score), 0),
        2
    ) AS low_review_rate_pct

FROM public.orders AS o

LEFT JOIN review_per_order AS r
    ON o.order_id = r.order_id

WHERE o.eligible_delivery = TRUE

GROUP BY o.is_late;

--execute after executing above code

SELECT *
FROM public.vw_delivery_review_impact
ORDER BY delivery_result;
