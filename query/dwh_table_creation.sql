/* FACT TRANSACTION */
DROP TABLE IF EXISTS warehouse.fact_transaction
;

CREATE TABLE warehouse.fact_transaction AS
SELECT 
    order_id, 
    product_id, 
    customer_id, 
    order_date, 
    revenue, 
    quantity
FROM staging.transaction
;

/* DIM CUSTOMER */
DROP TABLE IF EXISTS warehouse.dim_customer
;

CREATE TABLE warehouse.dim_customer AS
SELECT 
    customer_id, 
    name AS customer_name,
    email,
    city,
    age,
    gender
FROM staging.customer;

/* DIM PRODUCT */
DROP TABLE IF EXISTS warehouse.dim_product
;

CREATE TABLE warehouse.dim_product AS
SELECT 
    product_id,
    name AS product_name,
    category,
    subcategory,
    price
FROM staging.product;

/* DIM DATE */
DROP TABLE IF EXISTS warehouse.dim_date
;

CREATE TABLE warehouse.dim_date AS
SELECT DISTINCT 
    order_date AS date_key,
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    EXTRACT(DAY FROM order_date) AS day
FROM staging.transaction;
