CREATE DATABASE stupify;
use stupify;
CREATE TABLE category(
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100)
);
CREATE TABLE customer(
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR (50),
    phone VARCHAR(11),
    email VARCHAR(320) /*standard email address can contain a maximum of 254 to 320 characters total is wajah say yeh number*/ 
);
CREATE TABLE product(
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    price DECIMAL(15,2),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    stocks INT
);
CREATE TABLE shipping_method(
    shipping_id INT PRIMARY KEY AUTO_INCREMENT,
    method_name ENUM('Standard', 'Express', 'Overnight', 'Free Shipping') NOT NULL,
    shipping_cost DECIMAL(15,2)
);
CREATE TABLE postal_code(
    postal_code VARCHAR(20) PRIMARY KEY,
    city VARCHAR(50),
    country VARCHAR(50)
);
CREATE TABLE address(
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
    address_line1 VARCHAR(100),
    address_line2 VARCHAR(100),
    postal_code VARCHAR(20),
    FOREIGN KEY (postal_code)  REFERENCES postal_code(postal_code)
);
CREATE TABLE cart(
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE cart_item(
    cartitem_id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
CREATE TABLE `order` (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(15,2),
    order_status ENUM ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'),
    shipping_id INT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (shipping_id) REFERENCES shipping_method(shipping_id)
);
CREATE TABLE order_item(
    orderitem_id INT PRIMARY KEY AUTO_INCREMENT, 
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(15,2),
    FOREIGN KEY (order_id)   REFERENCES `order`(order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
CREATE TABLE payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    amount DECIMAL(15,2),
    payment_date DATE,
    payment_status ENUM('Pending', 'Completed', 'Failed', 'Refunded'),
    payment_method ENUM('Credit Card', 'Debit Card', 'PayPal', 'Cash on Delivery'),
    FOREIGN KEY (order_id) REFERENCES `order`(order_id)
);
CREATE TABLE review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (product_id)  REFERENCES product(product_id)
);