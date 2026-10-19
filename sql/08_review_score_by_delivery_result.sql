
-- Compare average customer review scores by delivery result.

SELECT
    CASE
        WHEN o.is_late = TRUE THEN 'Late'
        WHEN o.is_late = FALSE THEN 'On-time or early'
    END AS delivery_result,

    COUNT(DISTINCT o.order_id) AS eligible_orders,

    COUNT(DISTINCT r.order_id) AS orders_with_reviews,

    ROUND(AVG(r.review_score)::numeric, 2)
        AS average_review_score,

    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN r.review_score <= 2 THEN r.order_id
        END)
        / NULLIF(COUNT(DISTINCT r.order_id), 0),
        2
    ) AS low_review_rate_pct

FROM public.orders AS o

LEFT JOIN public.olist_order_reviews_dataset AS r
    ON o.order_id = r.order_id

WHERE o.eligible_delivery = TRUE

GROUP BY o.is_late

ORDER BY o.is_late DESC;
