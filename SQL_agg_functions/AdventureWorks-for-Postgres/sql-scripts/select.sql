--1. Identify Department Groupings
SELECT COUNT(DISTINCT humanresources.department.name) AS number_of_departments, 
        humanresources.department.groupname
FROM humanresources.department
GROUP BY humanresources.department.groupname
ORDER BY number_of_departments DESC;

--2. Determine Maximum Salary for Each Employee
SELECT humanresources.employee.businessentityid, 
    humanresources.employee.loginid, 
    humanresources.employee.jobtitle,
    MAX(humanresources.employeepayhistory.rate) AS maximum_salary
FROM humanresources.employee
JOIN humanresources.employeepayhistory 
    ON humanresources.employee.businessentityid = humanresources.employeepayhistory.businessentityid
GROUP BY humanresources.employee.businessentityid, 
    humanresources.employee.loginid, 
    humanresources.employee.jobtitle
ORDER BY maximum_salary DESC, 
    humanresources.employee.businessentityid;

--3. Minimum Product Price by Subcategory
SELECT production.productsubcategory.productsubcategoryid,
    production.productsubcategory.name,
    MIN(sales.salesorderdetail.unitprice) AS min_unit_price
FROM production.productsubcategory
JOIN production.product 
    ON production.productsubcategory.productsubcategoryid = production.product.productsubcategoryid
JOIN sales.salesorderdetail 
    ON production.product.productid = sales.salesorderdetail.productid
GROUP BY production.productsubcategory.productsubcategoryid, 
    production.productsubcategory.name
ORDER BY production.productsubcategory.productsubcategoryid ASC;

--4. Count of Subcategories within Each Product Category
SELECT production.productcategory.productcategoryid,
    production.productcategory.name,
    COUNT(production.productsubcategory.productsubcategoryid) AS total_subcategories
FROM production.productcategory
JOIN production.productsubcategory 
    ON production.productsubcategory.productcategoryid = production.productcategory.productcategoryid
GROUP BY production.productcategory.productcategoryid, 
    production.productcategory.name
ORDER BY production.productcategory.productcategoryid ASC;

--5. Average Order Total by Product Subcategory
SELECT production.productsubcategory.productsubcategoryid,
    production.productsubcategory.name,
    AVG(sales.salesorderdetail.unitprice * sales.salesorderdetail.orderqty * (1 - sales.salesorderdetail.unitpricediscount)) AS avg_order_total
FROM sales.salesorderdetail
JOIN production.product 
    ON sales.salesorderdetail.productid = production.product.productid
JOIN production.productsubcategory 
    ON production.productsubcategory.productsubcategoryid = production.product.productsubcategoryid
GROUP BY production.productsubcategory.productsubcategoryid, 
    production.productsubcategory.name
ORDER BY production.productsubcategory.productsubcategoryid ASC;

--6. Employee with Highest Salary and Their Rate Appointment Date
SELECT humanresources.employeepayhistory.businessentityid, 
    humanresources.employeepayhistory.rate AS maximum_salary,
    humanresources.employeepayhistory.ratechangedate
FROM humanresources.employeepayhistory
JOIN ( SELECT humanresources.employeepayhistory.businessentityid,
            MAX(humanresources.employeepayhistory.rate) AS maximum_salary
        FROM humanresources.employeepayhistory
        GROUP BY humanresources.employeepayhistory.businessentityid
) AS max_salary 
ON humanresources.employeepayhistory.businessentityid = max_salary.businessentityid
   AND humanresources.employeepayhistory.rate = max_salary.maximum_salary
ORDER BY humanresources.employeepayhistory.ratechangedate ASC
LIMIT 1;
