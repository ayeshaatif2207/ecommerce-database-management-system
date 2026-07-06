USE stupify;

--QUERY#1
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(oi.quantity)        AS total_qty_sold,
        COUNT(oi.orderitem_id)  AS times_ordered
    FROM product p
    JOIN order_item oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT
    product_name,
    total_qty_sold,
    times_ordered
FROM product_sales
ORDER BY total_qty_sold ASC
LIMIT 5;

--QUERY#2
WITH category_revenue AS (
    SELECT
        c.category_name,
        COUNT(DISTINCT o.order_id)       AS total_orders,
        SUM(oi.quantity * oi.price)       AS total_revenue
    FROM category c
    JOIN product p      ON c.category_id = p.category_id
    JOIN order_item oi  ON p.product_id  = oi.product_id
    JOIN `order` o      ON oi.order_id   = o.order_id
    WHERE  o.order_status = 'Delivered'
    AND    oi.price > 0
    GROUP BY c.category_name
)
SELECT
    category_name,
    total_orders,
    total_revenue
FROM category_revenue
ORDER BY total_revenue ASC;

USE stupify;


--QUERY#3
WITH completed_payers AS (
    SELECT DISTINCT order_id
    FROM payment
    WHERE payment_status = 'Completed'
),
all_orders AS (
    SELECT DISTINCT customer_id, order_id
    FROM `order`
    WHERE order_status != 'Cancelled'
)
SELECT
    c.customer_id,
    c.customer_name,
    c.email
FROM customer c
JOIN all_orders ao ON c.customer_id = ao.customer_id
WHERE ao.order_id NOT IN (
    SELECT order_id FROM completed_payers
)
AND c.email IS NOT NULL
ORDER BY c.customer_name ASC;


--QUERY#4
SELECT
    p.product_name,
    COUNT(r.review_id)        AS total_reviews,
    AVG(r.rating)             AS avg_rating,
    MAX(r.rating)             AS highest_rating,
    MIN(r.rating)             AS lowest_rating
FROM product p
JOIN review r ON p.product_id = r.product_id
WHERE  r.rating IS NOT NULL
AND    r.rating BETWEEN 1 AND 5
GROUP BY p.product_id, p.product_name
HAVING COUNT(r.review_id) >= 2
ORDER BY avg_rating ASC;


--QUERY#5
UPDATE `order`
SET    order_status = 'Processing'
WHERE  order_status = 'Pending'
AND    order_date  < '2024-06-01';
SELECT *
FROM `order`;


--QUERY#6
DELETE FROM review
WHERE (comments IS NULL OR comments = '')
AND rating < 3;

