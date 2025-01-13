--Trigger Practice
--1.1 Creating the Table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2),
    creation_date DATE,
    last_update DATE
);

-- 1.2. Sample Data Insertion
INSERT INTO employees (name, salary, creation_date, last_update)
VALUES ('John Doe', 50000, '2023-01-01', '2023-01-01');

INSERT INTO employees (name, salary, creation_date, last_update)
VALUES ('Jane Smith', 60000, '2023-01-02', '2023-01-02');

INSERT INTO employees (name, salary, creation_date, last_update)
VALUES ('Emily Johnson', 55000, '2023-01-03', '2023-01-03');


--1.3. Writing a Trigger Function
CREATE OR REPLACE FUNCTION update_last_update_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_update = CURRENT_DATE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 1.4. Attaching the Trigger Function to a Table
CREATE TRIGGER update_last_update
BEFORE UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION update_last_update_column();

--Testing the trigger
SELECT * FROM employees;

UPDATE employees SET name ='John Snow' WHERE id=1;
SELECT * FROM employees;

--2. Advanced Trigger Examples
--2.1.Creating the Audit Log Table
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    employee_id INT,
    old_salary DECIMAL(10, 2),
    new_salary DECIMAL(10, 2),
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--2.2. Writing the Trigger Function for Auditing
CREATE OR REPLACE FUNCTION log_salary_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.salary IS DISTINCT FROM NEW.salary THEN
        INSERT INTO audit_log (employee_id, old_salary, new_salary)
        VALUES (NEW.id, OLD.salary, NEW.salary);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--2.3. Attaching the Trigger to the Employees Table
CREATE TRIGGER trigger_audit_salary_change
AFTER UPDATE OF salary ON employees
FOR EACH ROW
EXECUTE FUNCTION log_salary_change();

--Testing 
SELECT * FROM audit_log;
UPDATE employees SET salary= 70000 WHERE name ='Jane Smith';
SELECT * FROM audit_log;

--3. Examples of Different Types of Triggers
--3.1 BEFORE Triggers
CREATE OR REPLACE FUNCTION check_salary_before_insert()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.salary < 30000 THEN
        RAISE EXCEPTION 'Salary must be at least 30000';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_salary_before_insert_trigger
BEFORE INSERT ON employees
FOR EACH ROW
EXECUTE FUNCTION check_salary_before_insert();

-- This should raise an exception
INSERT INTO employees (name, salary, creation_date, last_update)
VALUES ('Test Employee', 25000, CURRENT_DATE, CURRENT_DATE);

--3.2 AFTER Triggers
CREATE OR REPLACE FUNCTION log_salary_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.salary IS DISTINCT FROM NEW.salary THEN
        INSERT INTO audit_log (employee_id, old_salary, new_salary)
        VALUES (NEW.id, OLD.salary, NEW.salary);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_salary_changes_trigger
AFTER UPDATE OF salary ON employees
FOR EACH ROW
EXECUTE FUNCTION log_salary_changes();

-- This should log the salary change
UPDATE employees SET salary = 55000 WHERE id = 1;

--3.3 INSTEAD OF Triggers (For Views)
CREATE VIEW employee_salary_view AS SELECT id, salary FROM employees;

CREATE OR REPLACE FUNCTION update_salary_through_view()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE employees SET salary = NEW.salary WHERE id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_salary_view_trigger
INSTEAD OF UPDATE ON employee_salary_view
FOR EACH ROW
EXECUTE FUNCTION update_salary_through_view();

-- This should update the salary through the view
UPDATE employee_salary_view SET salary = 60000 WHERE id = 1;

-- 3.4 Row-Level Triggers
CREATE OR REPLACE FUNCTION prevent_high_salary_deletion()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.salary > 60000 THEN
        RAISE EXCEPTION 'Cannot delete employees with a salary above 70000';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_high_salary_deletion_trigger
BEFORE DELETE ON employees
FOR EACH ROW
EXECUTE FUNCTION prevent_high_salary_deletion();

SELECT * FROM employees;
-- employee with id 2 has a salary above 60000, this should raise an exception
SELECT * FROM employees;
DELETE FROM employees WHERE id = 2;


--3.5 Statement-Level Triggers
CREATE TABLE bulk_update_log (
    log_id SERIAL PRIMARY KEY,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by TEXT
);

CREATE OR REPLACE FUNCTION log_bulk_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO bulk_update_log (updated_by)
    VALUES (CURRENT_USER);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_bulk_update_trigger
AFTER UPDATE ON employees
FOR EACH STATEMENT
EXECUTE FUNCTION log_bulk_update();

-- This should log the bulk update operation
UPDATE employees SET salary = salary * 1.05;

SELECT * FROM bulk_update_log;
