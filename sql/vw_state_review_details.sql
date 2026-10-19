
CREATE OR REPLACE VIEW public.vw_state_review_details AS
WITH order_states AS (
    SELECT DISTINCT
        oi.order_id,
        s.seller_state
    FROM public.olist_order_items_dataset AS oi
    JOIN public.olist_sellers_dataset AS s
        ON oi.seller_id = s.seller_id
)
SELECT
    os.order_id,
    os.seller_state,
    r.review_id,
    r.review_score,
    o.is_late,
    o.eligible_delivery
FROM order_states AS os
JOIN public.orders AS o
    ON os.order_id = o.order_id
JOIN public.olist_order_reviews_dataset AS r
    ON os.order_id = r.order_id
WHERE o.eligible_delivery = TRUE;


--execute after executing above code

SELECT *
FROM public.vw_state_review_details
LIMIT 10;