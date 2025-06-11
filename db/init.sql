
CREATE DATABASE IF NOT EXISTS analytics;
USE analytics;

-- Tabellen f�r Checkouts
CREATE TABLE IF NOT EXISTS checkout (
    checkout_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    total_amount DECIMAL(10,2),
    currency VARCHAR(3),
    payment_method VARCHAR(50),
    status VARCHAR(20),
    created_at DATETIME
);

CREATE TABLE IF NOT EXISTS shipping_address (
    checkout_id VARCHAR(36),
    name VARCHAR(100),
    street VARCHAR(100),
    zip VARCHAR(10),
    city VARCHAR(50),
    country VARCHAR(5),
    PRIMARY KEY (checkout_id),
    FOREIGN KEY (checkout_id) REFERENCES checkout(checkout_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cart_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    checkout_id VARCHAR(36),
    product_id VARCHAR(50),
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (checkout_id) REFERENCES checkout(checkout_id) ON DELETE CASCADE
);

-- Neue Tabellen f�r Orders

CREATE TABLE IF NOT EXISTS `order` (
    order_id VARCHAR(36) PRIMARY KEY,
    checkout_id VARCHAR(36) UNIQUE,
    user_id VARCHAR(36),
    total_amount DECIMAL(10,2),
    currency VARCHAR(3),
    payment_method VARCHAR(50),
    status VARCHAR(20),
    created_at DATETIME,
    FOREIGN KEY (checkout_id) REFERENCES checkout(checkout_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_shipping_address (
    order_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    street VARCHAR(100),
    zip VARCHAR(10),
    city VARCHAR(50),
    country VARCHAR(5),
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_cart_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(36),
    product_id VARCHAR(50),
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fulfillment (
    fulfillment_id VARCHAR(36),
    order_id VARCHAR(36),
    status VARCHAR(20),
    created_at DATETIME,
    PRIMARY KEY (fulfillment_id),
);

