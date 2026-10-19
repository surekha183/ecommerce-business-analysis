
-- Executive summary of delivery performance and customer reviews

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
        )
        / NULLIF(
            COUNT(*) FILTER (
                WHERE eligible_delivery = TRUE
            ),
            0
        ),
        2
    ) AS late_delivery_rate_pct,

    ROUND(
        AVG(review_score) FILTER (
            WHERE is_late = TRUE
        )::numeric,
        2
    ) AS avg_review_score_late,

    ROUND(
        AVG(review_score) FILTER (
            WHERE is_late = FALSE
        )::numeric,
        2
    ) AS avg_review_score_on_time

FROM (
    SELECT
        o.order_id,
        o.eligible_delivery,
        o.is_late,
        r.review_score
    FROM public.orders AS o
    LEFT JOIN public.olist_order_reviews_dataset AS r
        ON o.order_id = r.order_id
) AS order_summary;
