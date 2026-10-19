
-- 1. Count all orders
SELECT COUNT(*) AS total_orders
FROM public.orders;


-- 2. Count unique order IDs
SELECT COUNT(DISTINCT order_id) AS unique_orders
FROM public.orders;


-- 3. Check order status distribution
SELECT
    order_status,
    COUNT(*) AS number_of_orders
FROM public.orders
GROUP BY order_status
ORDER BY number_of_orders DESC;


-- 4. Check delivery eligibility and late-delivery labels
SELECT
    eligible_delivery,
    is_late,
    COUNT(*) AS number_of_orders
FROM public.orders
GROUP BY eligible_delivery, is_late
ORDER BY eligible_delivery, is_late;
