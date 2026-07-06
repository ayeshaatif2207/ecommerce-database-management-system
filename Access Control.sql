use stupify;

-- 1. ADMIN ROLE - Full access to everything
CREATE USER 'admin_2'@'localhost' IDENTIFIED BY 'admin_pass123';
GRANT ALL PRIVILEGES ON stupify.* TO 'admin_2'@'localhost';

-- 2. manager ROLE - Can view and add products, but not delete
CREATE USER 'database_manager'@'localhost' IDENTIFIED BY 'manager_pass_123';
GRANT SELECT, INSERT, UPDATE ON stupify.product TO 'database_manager'@'localhost';
GRANT SELECT ON stupify.category TO 'database_manager'@'localhost';
GRANT SELECT ON stupify.customer TO 'database_manager'@'localhost';
GRANT SELECT ON stupify.`order` TO 'database_manager'@'localhost';
SHOW GRANTS FOR 'database_manager'@'localhost';

-- 3. ANALYST ROLE - Read-only access
CREATE USER 'analyst'@'localhost' IDENTIFIED BY 'analyst_pass_123';
GRANT SELECT ON stupify.* TO 'analyst'@'localhost';
-- Apply changes
FLUSH PRIVILEGES;



-----mysql -u root -p

mysql -u analyst -p

----------QUERIES TO RUN TO SHOW RESTRICTIONS:
ADMIN:
EVERYTHING WORKS:
CREATE TABLE testing (
    id INT
);
SHOW tables;
DROP TABLE testing;
SHOW tables;
MANAGER::
WORKING:
SELECT * FROM product;

INSERT INTO product (product_name, category_id, price, stock)
VALUES ('Manager Product', 1, 300, 5);

UPDATE product
SET stock = 20
WHERE product_id = 1;

NOT WORKING:
ALTER TABLE product ADD test INT;
DELETE FROM product WHERE product_id = 1;
ANALYST:
WORKING:
SELECT product_name, price FROM product;
NOT WORKING:
INSERT INTO product (product_id, product_name, category_id, price, stock)
VALUES (1, 'Laptop', 2, 1200.00, 10);
















