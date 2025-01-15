--1. Creating the table customer
CREATE TABLE customer(
  customer_id int,
  first_name varchar(50),
  last_name varchar(50),
  email varchar(100),
  modified_date date,
  age int,
  active boolean,
  CONSTRAINT pk_customer PRIMARY KEY (customer_id)
  );


--Checking the indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'customer';

--Inserting data 
INSERT INTO public.customer
SELECT
    gs AS customer_id,
    concat('firstname', gs) AS first_name,
    concat('lastname', gs) AS last_name,
    concat('firstname', 'lastname', gs, '@email.com') AS email,
    modifieddate + INTERVAL '1 day' * (gs % 365) AS modified_date,
    gs % 90 AS age,
    gs % 7 = 0 AS active
FROM
    GENERATE_SERIES(1, 1000000) as gs
CROSS JOIN
    (SELECT * FROM humanresources.employee LIMIT 1) as emp;

SELECT COUNT(customer_id) FROM customer;
SELECT * FROM customer LIMIT 20;

-- 3. Create a B-tree multi-column index on the customer table on the first_name and last_name columns.
CREATE INDEX idx_customer_name ON customer (first_name, last_name);

-- 4. Create an index on the customer table so that the output of the query below is the specified output... where age between 18 and 60;
CREATE INDEX idx_customer_age ON customer (age);

-- Checking the execution plan
explain (analyze)
select *
from customer
where age between 18 and 60;

--5. Create a covering index customer_modified_date_idx for fast query execution
CREATE INDEX customer_modified_date_idx
ON customer(modified_date, first_name, last_name);

EXPLAIN (ANALYZE)
SELECT
  first_name, last_name
FROM customer
WHERE modified_date = '2014-12-21';

--6. Delete the index/constraint that you created on the customer_id column in first step
ALTER TABLE customer
DROP CONSTRAINT pk_customer;

--Checking the indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'customer';

--7. Rename previously created covering index customer_modified_date_idx to customer_modified_date_idx_covering
ALTER INDEX customer_modified_date_idx RENAME TO customer_modified_date_idx_covering;

--8. Create a Hash index called customer_modified_date_idx on the customer table on the modified_date column
CREATE INDEX customer_modified_date_idx
ON customer USING hash (modified_date);

-- 9. Create a partial index on the email column only for those records that have active = true. Also, write a query to the table in which this index will be used.
CREATE INDEX customer_email_active_idx
ON customer(email)
WHERE active = true;


SELECT email
FROM customer
WHERE active = true;

-- 10. Create an index on expression on the customer table to quickly find records using this rule. Expression must implement the following logic: if first_name = 'firstname1' and last_name = 'lastname1', then we are looking for 'f, lastname1', if the first name 'my_name' last name 'apple' → result should be 'm, apple', etc.
ALTER TABLE customer
ADD COLUMN name_concat text GENERATED ALWAYS AS (substring(first_name from 1 for 1) || ', ' || last_name) STORED;

CREATE INDEX customer_name_concat_idx
ON customer (name_concat);

-- 11. Check the query plan that this index is being used.
EXPLAIN (ANALYZE)
SELECT * FROM customer
WHERE name_concat = 'f, lastname1';




