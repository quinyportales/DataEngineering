-- 1. Find the sum of sales for the month by each product, sold in Jan-2013.
WITH RankedProducts AS (
    SELECT ssod.productid,
        pp.name,
        SUM(ssod.unitprice * ssod.orderqty) AS total_sales,
        PERCENT_RANK() OVER (ORDER BY SUM(ssod.unitprice * ssod.orderqty)) AS percent_rank
    FROM production.product AS pp
    JOIN sales.salesorderdetail AS ssod 
        ON pp.productid = ssod.productid
    JOIN sales.salesorderheader AS ssoh 
        ON ssod.salesorderid = ssoh.salesorderid
    WHERE ssoh.orderdate BETWEEN '2013-01-01' AND '2013-01-31'
    GROUP BY ssod.productid, pp.name
)
SELECT productid,
    name,
    total_sales
FROM RankedProducts
WHERE percent_rank > 0.1 AND percent_rank < 0.9 --Including only the sales range between 10% al 90% 
ORDER BY productid ASC;

--2. Get the cheapest products in each subcategory using the Production.Product table.
WITH CheapestProducts AS (
    SELECT 
        pp.productsubcategoryid,
        pps.name AS subcategory_name,
        pp.productid,
        pp.name AS product_name,
        MIN(ssod.unitprice) AS cheapest_price,
        ROW_NUMBER() OVER (PARTITION BY pp.productsubcategoryid ORDER BY MIN(ssod.unitprice) ASC) AS rnk
    FROM production.productsubcategory AS pps
    JOIN production.product AS pp 
        ON pps.productsubcategoryid = pp.productsubcategoryid
    JOIN sales.salesorderdetail AS ssod 
        ON pp.productid = ssod.productid
    GROUP BY 
        pp.productsubcategoryid, pps.name, pp.productid, pp.name
)
SELECT 
    productsubcategoryid,
    subcategory_name,
    productid,
    product_name,
    cheapest_price
FROM CheapestProducts
WHERE rnk = 1
ORDER BY productsubcategoryid ASC;


--3. Find the second by-value price for mountain bikes using Production.Product table.
WITH MountainValues AS (
    SELECT pp.productid,
        pp.name,
        pp.listprice,
        pp.productsubcategoryid,
        ROW_NUMBER() OVER (ORDER BY pp.listprice DESC) AS row_num
    FROM production.product AS pp
    WHERE pp.name LIKE '%Mountain%' AND pp.listprice <> 0
)
SELECT productid,
    name,
    listprice,
    productsubcategoryid
FROM MountainValues
WHERE row_num = 2;

--4. Count sales for 2013 year in slices of categories (“YoY metric”: (Sales - PrevSales) / PrevSales)
WITH TotalSales AS (
  SELECT 
    ppc.Name AS category, -- Nombre de la categoría
    SUM(ssod.OrderQty * ssod.UnitPrice * (1 - ssod.UnitPriceDiscount)) AS TotalSales, 
    LAG(SUM(ssod.OrderQty * ssod.UnitPrice * (1 - ssod.UnitPriceDiscount)), 1, 0) OVER (ORDER BY ppc.Name) AS PreviousQuota 
  FROM Production.ProductCategory AS ppc
  JOIN Production.ProductSubcategory AS pps 
    ON ppc.ProductCategoryID = pps.ProductCategoryID
  JOIN Production.Product AS pp 
    ON pps.ProductSubcategoryID = pp.ProductSubcategoryID
  JOIN Sales.SalesOrderDetail AS ssod 
    ON pp.ProductID = ssod.ProductID
  JOIN Sales.SalesOrderHeader AS ssoh 
    ON ssod.SalesOrderID = ssoh.SalesOrderID
  WHERE ssoh.OrderDate BETWEEN '2013-01-01' AND '2013-12-31'
  GROUP BY ppc.Name
)
SELECT 
  category, 
  TotalSales, 
  PreviousQuota,
  CASE 
    WHEN PreviousQuota = 0 THEN NULL
    ELSE (TotalSales - PreviousQuota) / PreviousQuota 
  END AS YoYMetric
FROM TotalSales;

--5 Find the max sum of order for each day of Jan-2013 
SELECT ssoh.orderdate,
  MAX(ssoh.totaldue) AS max_order
FROM sales.salesorderheader AS ssoh
WHERE ssoh.orderdate BETWEEN '2013-01-01' AND '2013-01-31'
GROUP BY ssoh.orderdate
ORDER BY ssoh.orderdate ASC

--6. Find the most salable product for each subcategory in Jan-2013 
WITH SalesPerProduct AS (
  SELECT 
    pps.productsubcategoryid,
    pps.name AS subcategory,
    pp.name AS item,
    SUM(ssod.unitprice * ssod.orderqty) AS item_sale,
    ROW_NUMBER() OVER (PARTITION BY pps.productsubcategoryid ORDER BY SUM(ssod.unitprice * ssod.orderqty) DESC) AS rnk
  FROM production.productsubcategory AS pps
  JOIN production.product AS pp 
    ON pps.productsubcategoryid = pp.productsubcategoryid
  JOIN sales.salesorderdetail AS ssod
    ON ssod.productid = pp.productid
  JOIN sales.salesorderheader AS ssoh
    ON ssod.salesorderid = ssoh.salesorderid
  WHERE ssoh.orderdate BETWEEN '2013-01-01' AND '2013-01-31'
  GROUP BY pps.productsubcategoryid, pps.name, pp.name
)
SELECT 
  subcategory,
  item,
  item_sale AS mostfreq
FROM SalesPerProduct
WHERE rnk = 1
ORDER BY productsubcategoryid;
