
CREATE OR REPLACE VIEW public.vw_state_delivery_stage_details AS
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
    o.is_late,
    o.purchase_to_approval_hours,
    o.approval_to_carrier_hours,
    o.carrier_to_delivery_hours
FROM order_states AS os
JOIN public.orders AS o
    ON os.order_id = o.order_id
WHERE o.eligible_delivery = TRUE;
