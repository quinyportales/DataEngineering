-- Inserting data into author
INSERT INTO author (author_name, birthdate) VALUES 
('J. R. R. Tolkien', 1892), 
('J. K. Rowling', 1965), 
('Andrzej Sapkowski', 1948),
('Ray Bradbury', 1920),
('Jill MacKenzie', 1990),
('Lane Diamond', 1950),
('Amanda Papenfus', 1950), 
('Ariyana Spencer', 1950);

-- Inserting data into book
INSERT INTO book (title, year_published, price) VALUES 
('The Lord of the Rings', 1954, 10000),
('The Hobbit', 1937, 10000),
('Harry Potter', 1997, 9000), 
('Geralt of Rivia - The Witcher', 1993, 8000),
('Farenheit 451', 1953, 15000),
('Spin the Sky', 2016, 5000),
('Evolution: Vol. 1', 2011, 5000);

-- Updating records in book table
UPDATE book SET republished_year = 1968 WHERE book_id = 1;
UPDATE book SET republished_year = 2019 WHERE book_id = 6;
UPDATE book SET republished_year = 2013 WHERE book_id = 5;
UPDATE book SET republished_year = 2012 WHERE book_id = 7;

-- Inserting data into book_authors
INSERT INTO book_authors (book_id, author_id)
SELECT b.book_id, a.author_id
FROM book b
JOIN author a 
ON (b.title = 'The Lord of the Rings' AND a.author_name = 'J. R. R. Tolkien')
   OR (b.title = 'The Hobbit' AND a.author_name = 'J. R. R. Tolkien')
   OR (b.title = 'Harry Potter' AND a.author_name = 'J. K. Rowling')
   OR (b.title = 'Geralt of Rivia - The Witcher' AND a.author_name = 'Andrzej Sapkowski')
   OR (b.title = 'Farenheit 451' AND a.author_name = 'Ray Bradbury')
   OR (b.title = 'Spin the Sky' AND a.author_name = 'Jill MacKenzie')
   OR (b.title = 'Evolution: Vol. 1' AND a.author_name = 'Lane Diamond')
   OR (b.title = 'Evolution: Vol. 1' AND a.author_name = 'Amanda Papenfus')
   OR (b.title = 'Evolution: Vol. 1' AND a.author_name = 'Ariyana Spencer');

-- Inserting data into roles
INSERT INTO roles (job_role) VALUES 
('administrator'),
('customer');

-- Inserting data into users
INSERT INTO users (user_name, role_id) VALUES 
('super admin 1', 1),
('super admin 2', 1),
('customer 1', 2), 
('customer 2', 2),
('customer 3', 2);

-- Inserting data into bookstore
INSERT INTO bookstore (bookstore_name) VALUES
('Great Bookstore North'),
('Great Bookstore South'),
('Great Bookstore East'),
('Great Bookstore West');

-- Inserting data into book_exemplar
INSERT INTO book_exemplar (book_id, bookstore_id) VALUES
  (1, 1),
  (1, 1),
  (1, 1),
  (2, 1),
  (3, 1),
  (4, 1),
  (5, 1),
  (5, 1),
  (5, 1),
  (5, 1),
  (6, 2),
  (7, 2);

-- Inserting values into orders
INSERT INTO orders (user_id, bookstore_id, total_cost) VALUES 
  (3, 1, 30000), -- ordered two Fahrenheit 451
  (4, 1, 10000), -- ordered one The Hobbit
  (5, 1, 10000), -- ordered one The Lord of the Rings
  (3, 2, 5000);  -- ordered one Evolution: Vol. 1

-- Inserting into ordered_books
-- Order 1
INSERT INTO ordered_books (order_id, book_id, exemplar_id)
SELECT 1, be.book_id, be.exemplar_id 
FROM book_exemplar be
JOIN book b ON b.book_id = be.book_id
WHERE b.title = 'Farenheit 451'
LIMIT 2; -- two books ordered

-- Order 2
INSERT INTO ordered_books (order_id, book_id, exemplar_id)
SELECT 2, be.book_id, be.exemplar_id 
FROM book_exemplar be
JOIN book b ON b.book_id = be.book_id
WHERE b.title = 'The Hobbit'
LIMIT 1; -- one book ordered

-- Order 3
INSERT INTO ordered_books (order_id, book_id, exemplar_id)
SELECT 3, be.book_id, be.exemplar_id 
FROM book_exemplar be
JOIN book b ON b.book_id = be.book_id
WHERE b.title = 'The Lord of the Rings'
LIMIT 1; -- one book ordered

-- Order 4
INSERT INTO ordered_books (order_id, book_id, exemplar_id)
SELECT 4, be.book_id, be.exemplar_id 
FROM book_exemplar be
JOIN book b ON b.book_id = be.book_id
WHERE b.title = 'Evolution: Vol. 1'
LIMIT 1; -- one book ordered

-- Deleting stores with no sales
DELETE FROM bookstore
WHERE bookstore_id IN (
  SELECT bs.bookstore_id
  FROM bookstore AS bs
  LEFT JOIN orders AS o ON o.bookstore_id = bs.bookstore_id
  GROUP BY bs.bookstore_id, bs.bookstore_name
  HAVING SUM(o.total_cost) = 0 OR SUM(o.total_cost) IS NULL
);

--Inserting new stores
INSERT INTO bookstore (bookstore_name) VALUES
('Great New Bookstore 1'),
('Great New Bookstore 2');
