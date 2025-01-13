--1. Identify Department Groupings
SELECT COUNT(DISTINCT department.name) AS number_of_departments, 
        department.groupname
FROM humanresources.department AS department
GROUP BY department.groupname
ORDER BY number_of_departments DESC;

--2. Determine Maximum Salary for Each Employee
SELECT employee.businessentityid, 
    employee.loginid, 
    employee.jobtitle,
    MAX(employee_pay_history.rate) AS maximum_salary
FROM humanresources.employee AS employee
JOIN humanresources.employeepayhistory AS employee_pay_history
    ON employee.businessentityid = employee_pay_history.businessentityid
GROUP BY employee.businessentityid, 
    employee.loginid, 
    employee.jobtitle
ORDER BY maximum_salary DESC, 
    employee.businessentityid;

--3. Minimum Product Price by Subcategory
SELECT product_subcategory.productsubcategoryid,
    product_subcategory.name,
    MIN(sales_order.unitprice) AS min_unit_price
FROM production.productsubcategory AS product_subcategory
JOIN production.product AS product
    ON product_subcategory.productsubcategoryid = product.productsubcategoryid
JOIN sales.salesorderdetail AS sales_order
    ON product.productid = sales_order.productid
GROUP BY product_subcategory.productsubcategoryid, 
    product_subcategory.name
ORDER BY product_subcategory.productsubcategoryid ASC;

--4. Count of Subcategories within Each Product Category
SELECT product_subcategory.productcategoryid,
    productcategory.name,
    COUNT(product_subcategory.productsubcategoryid) AS total_subcategories
FROM production.productcategory AS productcategory
JOIN production.productsubcategory AS product_subcategory
    ON product_subcategory.productcategoryid = productcategory.productcategoryid
GROUP BY product_subcategory.productcategoryid, 
    productcategory.name
ORDER BY product_subcategory.productcategoryid ASC;

--5. Average Order Total by Product Subcategory
SELECT product_subcategory.productsubcategoryid,
    product_subcategory.name,
    AVG(sales_order.unitprice * sales_order.orderqty * (1 - sales_order.unitpricediscount)) AS avg_order_total
FROM sales.salesorderdetail AS sales_order
JOIN production.product AS product
    ON sales_order.productid = product.productid
JOIN production.productsubcategory AS product_subcategory
    ON product_subcategory.productsubcategoryid = product.productsubcategoryid
GROUP BY product_subcategory.productsubcategoryid, 
    product_subcategory.name
ORDER BY product_subcategory.productsubcategoryid ASC;

--6. Employee with Highest Salary and Their Rate Appointment Date
SELECT employee_pay_history.businessentityid, 
    employee_pay_history.rate AS maximum_salary,
    employee_pay_history.ratechangedate
FROM humanresources.employeepayhistory AS employee_pay_history
JOIN ( SELECT employee_pay_history.businessentityid,
            MAX(employee_pay_history.rate) AS maximum_salary
        FROM humanresources.employeepayhistory AS employee_pay_history
        GROUP BY employee_pay_history.businessentityid
) AS max_salary 
ON employee_pay_history.businessentityid = max_salary.businessentityid
   AND employee_pay_history.rate = max_salary.maximum_salary
ORDER BY employee_pay_history.ratechangedate ASC
LIMIT 1;
