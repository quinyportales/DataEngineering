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

-- Step 1: Create a PostgreSQL Table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    department_id INTEGER,
    salary NUMERIC
);

-- Step 2: Insert Data into the Table
INSERT INTO employees (name, email, department_id, salary) VALUES
('John Doe', 'john@example.com', 1, 50000),
('Jane Smith', 'jane@example.com', 2, 60000),
('Alice Johnson', 'alice@example.com', 1, 55000),
('Bob Brown', 'bob@example.com', 3, 45000),
('Carol White', 'carol@example.com', 2, 62000);

-- Step 3: Create Functions
--3.1 Basic Custom Function
CREATE OR REPLACE FUNCTION calculate_bonus(salary NUMERIC) RETURNS NUMERIC AS $$
BEGIN
    RETURN salary * 0.15;
END;
$$ LANGUAGE PLPGSQL;
-- Test calculate_bonus
SELECT name, salary, calculate_bonus(salary) AS bonus
FROM employees;

--3.2 Function Using Conditional Logic
CREATE OR REPLACE FUNCTION department_status(department_id_var INTEGER) RETURNS TEXT AS $$
DECLARE
    employee_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO employee_count FROM employees WHERE department_id = department_id_var;
    IF employee_count > 10 THEN
        RETURN 'Large';
    ELSE
        RETURN 'Small';
    END IF;
END;
$$ LANGUAGE PLPGSQL;

-- Test department_status
SELECT department_id, department_status(department_id)
FROM employees GROUP BY department_id;

--3.3 Aggregate Function
CREATE OR REPLACE FUNCTION sum_salary(state NUMERIC, salary NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    RETURN state + salary;
END;
$$ LANGUAGE PLPGSQL;

CREATE OR REPLACE AGGREGATE total_salaries(NUMERIC) (
    SFUNC = sum_salary,
    STYPE = NUMERIC,
    INITCOND = '0'
);

-- Test total_salaries
SELECT total_salaries(salary)
FROM employees;

--  3.4 Error Handling in Function
CREATE OR REPLACE FUNCTION safe_divide(numerator NUMERIC, denominator NUMERIC) RETURNS NUMERIC AS $$
BEGIN
    IF denominator = 0 THEN
        RAISE EXCEPTION 'Division by zero';
    END IF;
    RETURN round(numerator / denominator);
EXCEPTION
    WHEN others THEN
        RETURN NULL;
END;
$$ LANGUAGE PLPGSQL;


-- Test safe_divide
SELECT safe_divide(10, 0); -- Should handle division by zero
SELECT safe_divide(10, 2); -- Should return 5

--3.5 Using Built-in String Function
SELECT name, LENGTH(name) AS name_length FROM employees;

--3.6 String Manipulation Function
CREATE OR REPLACE FUNCTION email_domain(email TEXT) RETURNS TEXT AS $$
BEGIN
    RETURN split_part(email, '@', 2);
END;
$$ LANGUAGE PLPGSQL;

SELECT name, email, email_domain(email) AS domain
FROM employees;

-- 3.7 Complex Calculation Function
CREATE OR REPLACE FUNCTION net_salary(salary NUMERIC, tax_rate NUMERIC) RETURNS NUMERIC AS $$
BEGIN
    RETURN salary - (salary * tax_rate);
END;
$$ LANGUAGE PLPGSQL;

-- Test net_salary
SELECT name, salary, net_salary(salary, 0.2) AS net_salary
FROM employees;

-- 3.8 Table Function
CREATE OR REPLACE FUNCTION department_employees(dept_id INTEGER) RETURNS SETOF employees AS $$
BEGIN
    RETURN QUERY SELECT * FROM employees WHERE department_id = dept_id;
END;
$$ LANGUAGE PLPGSQL;


-- Test department_employees
SELECT * FROM department_employees(1);

--3.9 Step 4: Cleanup
DROP FUNCTION calculate_bonus;
DROP FUNCTION department_status;
DROP AGGREGATE IF EXISTS total_salaries(NUMERIC);
DROP FUNCTION safe_divide;
DROP FUNCTION department_employees;
DROP FUNCTION net_salary;
DROP FUNCTION email_domain;
DROP TABLE employees;
