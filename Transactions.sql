USE stupify;
SELECT o.order_id, o.customer_id, o.order_status,  oi.product_id, p.stocks, pay.payment_status
FROM `order` o
JOIN order_item oi ON o.order_id = oi.order_id
JOIN product p ON oi.product_id = p.product_id  /*a general overview of the product and their details*/
JOIN payment pay ON o.order_id = pay.order_id
WHERE o.order_status = 'Delivered'
LIMIT 10;

SELECT o.order_id, o.customer_id, o.order_status, oi.product_id, p.stocks, pay.payment_status
FROM `order` o
JOIN order_item oi ON o.order_id = oi.order_id
JOIN product p ON oi.product_id = p.product_id   /* The SELECT statement before the cancellation*/
JOIN payment pay ON o.order_id = pay.order_id
WHERE o.order_id = 5;

/*CANCELLATION*/
START TRANSACTION;
UPDATE `order`
SET order_status='Cancelled'
WHERE order_id=5;
UPDATE payment
SET payment_status = 'Refunded' /*cancellation of product*/
WHERE order_id=5;
UPDATE product
SET stocks=stocks+1
WHERE product_id IN (SELECT product_id
FROM order_item
WHERE order_id=5);
COMMIT;

SELECT o.order_id, o.order_status, pay.payment_status, p.product_id, p.stocks
FROM `order` o
JOIN payment pay ON o.order_id = pay.order_id
JOIN order_item oi ON o.order_id = oi.order_id   /*shows the updated status of the cancelled product*/
JOIN product p ON oi.product_id = p.product_id
WHERE o.order_id = 5;
 
/*ROLLBACK*/

SELECT o.order_id, o.customer_id, o.order_status, oi.product_id, p.stocks, pay.payment_status
FROM `order` o
JOIN order_item oi ON o.order_id = oi.order_id    /*before ROLLBACK*/
JOIN product p ON oi.product_id = p.product_id
JOIN payment pay ON o.order_id = pay.order_id
WHERE o.order_id = 4;

START TRANSACTION;
UPDATE `order`
SET order_status='Cancelled'
WHERE order_id=4;
UPDATE payment
SET payment_status = 'Refunded'
WHERE order_id=4;
UPDATE product
SET stocks=stocks+1
WHERE product_id IN (SELECT product_id
FROM order_item
WHERE order_id=4);
ROLLBACK;
SELECT o.order_id, o.customer_id, o.order_status, oi.product_id, p.stocks, pay.payment_status
FROM `order` o
JOIN order_item oi ON o.order_id = oi.order_id
JOIN product p ON oi.product_id = p.product_id  /*our output stays the same proving ROLLBACK*/
JOIN payment pay ON o.order_id = pay.order_id
WHERE o.order_id = 4;


/*
UPDATE `order`
 SET order_status = 'Delivered'
 WHERE order_id=4;

UPDATE payment
SET payment_status = 'Completed' 
WHERE order_id = 4;
UPDATE payment 
SET payment_status = 'Completed'
WHERE order_id = 5; 

UPDATE `order`
 SET order_status = 'Delivered'
 WHERE order_id=5;*/