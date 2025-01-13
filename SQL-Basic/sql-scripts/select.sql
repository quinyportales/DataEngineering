--Selecting using conditional
SELECT *  FROM book WHERE year_published > 2000;

--Selecting conditional
SELECT * FROM book WHERE republished_year IS NOT NULL;

-- Checking the users table
SELECT * FROM users ORDER BY user_id ASC;

-- Selecting the customers roles users 
SELECT DISTINCT role_id FROM users;

-- Selecting the customers roles users 
SELECT * FROM users WHERE role_id = '2';

-- Inner join queries
SELECT b.book_id, 
  b.title, 
  b.price, 
  bs.bookstore_name, 
  be.exemplar_id
FROM book AS b
JOIN book_exemplar AS be 
  ON b.book_id = be.book_id
JOIN bookstore AS bs
  ON bs.bookstore_id = be.bookstore_id
ORDER BY bookstore_name ASC;

-- Checking the books and their authors
SELECT b.title,
  a.author_name
FROM book AS b
JOIN book_authors AS ba
  ON b.book_id = ba.book_id
JOIN author AS a 
  ON a.author_id = ba.author_id
  ORDER BY author_name ASC;


--left join: querying the orders for all the users
SELECT u.user_id, 
  u.user_name,  
  r.job_role,
  o.order_id
FROM users AS u
LEFT JOIN orders AS o 
  ON o.user_id = u.user_id
JOIN roles AS r 
  ON u.role_id = r.role_id
ORDER BY user_id ASC;

--Checking the exemplars available for each book, including the stores with no books/exemplars
SELECT b.book_id,
  b.title,
  bs.bookstore_name,
  be.exemplar_id
FROM bookstore AS bs
LEFT JOIN book_exemplar AS be
  ON bs.bookstore_id = be.bookstore_id
LEFT JOIN book AS b
  ON b.book_id = be.book_id;

     
-- Right join: querying the stores with orders associated
SELECT bs.bookstore_name,
	COUNT (o.order_id) AS total_orders,
  SUM (o.total_cost) AS total_sales
FROM orders as o
RIGHT JOIN bookstore AS bs 
  ON o.bookstore_id= bs.bookstore_id
GROUP BY bs.bookstore_name
ORDER BY total_sales DESC;    
    
--Selecting customer that have placed more than one order
SELECT *
FROM orders
WHERE user_id IN (
	SELECT user_id
 	FROM orders
  GROUP BY user_id
  HAVING COUNT (order_id) > 1);



-- Selecting the best seller book and UNION with the worst seller (bu all with orders placed)
(SELECT ob.book_id,
        b.title,
        COUNT(ob.exemplar_id) AS total_books_sold
    FROM ordered_books AS ob
    JOIN book AS b 
      ON b.book_id = ob.book_id
    GROUP BY ob.book_id, b.title
    ORDER BY total_books_sold DESC
    LIMIT 1 )
UNION
(SELECT ob.book_id,
        b.title,
        COUNT(ob.exemplar_id) AS total_books_sold
    FROM ordered_books AS ob
    JOIN book AS b 
      ON b.book_id = ob.book_id
    GROUP BY ob.book_id, b.title
    ORDER BY total_books_sold ASC
    LIMIT 1 )
ORDER BY total_books_sold DESC;


-- Transforming Timestamp to string format
SELECT order_id, 
    user_id, 
    TO_CHAR(order_date, 'Day, DD Mon YYYY') AS order_date_string, 
    total_cost 
FROM orders;