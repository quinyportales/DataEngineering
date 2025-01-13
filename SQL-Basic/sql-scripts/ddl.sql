--Deleting previous tables if the exist
DO
$$
DECLARE
    table_name TEXT;
BEGIN
    FOR table_name IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP TABLE IF EXISTS public.%I CASCADE;', table_name);
    END LOOP;
END;
$$;

-- Create table test
CREATE TABLE test ( 
    test_col_1 INT,
    test_col_2 VARCHAR (250)
);

-- Rename column and drop table in test
ALTER TABLE test RENAME COLUMN test_col_1 TO new_column_name;
ALTER TABLE test RENAME TO test_name_updated;
DROP TABLE test_name_updated;

-- Create author table
CREATE TABLE author( 
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR (250),
    birthdate INT NOT NULL,
    CONSTRAINT chk_birthdate CHECK (birthdate >= 1500 AND birthdate <= EXTRACT(YEAR FROM CURRENT_DATE))
);

-- Create bookstore table
CREATE TABLE bookstore( 
    bookstore_id SERIAL PRIMARY KEY,
    store_name VARCHAR (250),
    store_address VARCHAR (250)
);

-- Alter bookstore table
ALTER TABLE bookstore DROP COLUMN store_address;
ALTER TABLE bookstore RENAME COLUMN store_name TO bookstore_name;

-- Create book table
CREATE TABLE book  ( 
    book_id SERIAL PRIMARY KEY,
    title VARCHAR (500),
    year_published INT NOT NULL,
    price FLOAT NOT NULL,
    republished_year INT DEFAULT NULL
);

-- Intermediate book_authors table
CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    CONSTRAINT fk_book_id FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_author_id FOREIGN KEY (author_id) REFERENCES author(author_id) ON DELETE CASCADE
);

-- Create book_exemplar table to represent multiple copies of the same book
CREATE TABLE book_exemplar (
    exemplar_id SERIAL PRIMARY KEY,
    book_id INT NOT NULL, 
    bookstore_id INT NOT NULL,
    CONSTRAINT fk_book FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_bookstore FOREIGN KEY (bookstore_id) REFERENCES bookstore(bookstore_id) ON DELETE CASCADE
);
-- Create roles table
CREATE TABLE roles  ( 
    role_id SERIAL PRIMARY KEY,
    job_role VARCHAR (250) NOT NULL
    CONSTRAINT chk_roles CHECK (job_role IN ('administrator', 'customer'))
);

-- Create users table
CREATE TABLE users  ( 
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR (250) NOT NULL,
    role_id INT, 
    CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES roles(role_id),
    CONSTRAINT chk_role CHECK (role_id IN (1, 2)) -- Only Administrator (1) or Customer (2) roles allowed
);

--Unique users
ALTER TABLE users ADD CONSTRAINT unique_user_role UNIQUE (user_name);

-- Create orders table
CREATE TABLE orders  ( 
    order_id SERIAL PRIMARY KEY,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    total_cost FLOAT,
    bookstore_id INT NOT NULL, 
    CONSTRAINT fk_userid FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_bsid FOREIGN KEY (bookstore_id) REFERENCES bookstore(bookstore_id)
);

-- Create ordered_books table to manage many-to-many relationship between orders and books
CREATE TABLE ordered_books (
    order_id INT,
    book_id INT,
    exemplar_id INT NOT NULL,
    CONSTRAINT fk_orderid FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_exemplar FOREIGN KEY (exemplar_id) REFERENCES book_exemplar(exemplar_id) ON DELETE CASCADE
);




