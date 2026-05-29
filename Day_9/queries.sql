-- ==========================================
-- MASTER ADVANCED SQL QUERIES (ALL WORKING)
-- ==========================================

-- ==========================================
-- CATEGORY A: JOINs (7 Queries)
-- ==========================================

-- 1. INNER JOIN
SELECT s.sale_id, e.name, s.amount 
FROM sales s 
INNER JOIN employees e ON s.employee_id = e.id;

-- 2. LEFT JOIN
SELECT e.name, s.amount 
FROM employees e 
LEFT JOIN sales s ON e.id = s.employee_id;

-- 3. RIGHT JOIN (Emulated)
SELECT e.name, s.amount 
FROM sales s 
LEFT JOIN employees e ON s.employee_id = e.id;

-- 4. FULL OUTER JOIN (Emulated)
SELECT e.id, e.name, s.amount 
FROM employees e 
LEFT JOIN sales s ON e.id = s.employee_id
UNION ALL
SELECT s.employee_id, NULL, s.amount 
FROM sales s 
WHERE s.employee_id NOT IN (SELECT id FROM employees);

-- 5. CROSS JOIN
SELECT e.name, p.category 
FROM employees e 
CROSS JOIN products p;

-- 6. SELF JOIN
SELECT a.name AS Employee, b.name AS Manager 
FROM employees a 
LEFT JOIN employees b ON a.manager_id = b.id;

-- 7. Multiple JOIN
SELECT s.sale_id, e.name, p.category, s.amount 
FROM sales s
JOIN employees e ON s.employee_id = e.id
JOIN products p ON s.product_id = p.product_id;


-- ==========================================
-- CATEGORY B: Aggregations
-- ==========================================

-- 8. GROUP BY with HAVING
SELECT department, SUM(salary) as total_pay 
FROM employees 
GROUP BY department 
HAVING SUM(salary) > 100000;

-- 9. COUNT DISTINCT
SELECT COUNT(DISTINCT product_id) as unique_products_sold 
FROM sales;

-- 10. Multiple Aggregations
SELECT employee_id, 
       AVG(amount) as avg_sale, 
       MAX(amount) as max_sale, 
       MIN(amount) as min_sale 
FROM sales 
GROUP BY employee_id;

-- 11. ROLLUP Alternative
SELECT product_id, SUM(amount) as total 
FROM sales 
GROUP BY product_id
UNION ALL
SELECT 0, SUM(amount) FROM sales;

-- 12. Filtered Aggregations
SELECT COUNT(*) as total FROM sales
UNION ALL
SELECT COUNT(*) FROM sales WHERE amount > 200;

-- 13. Subquery in WHERE
SELECT name, salary 
FROM employees 
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 14. Correlated Subquery
SELECT e.name, e.department, 
    (SELECT SUM(s.amount) FROM sales s WHERE s.employee_id = e.id) as total_sales
FROM employees e;


-- ==========================================
-- CATEGORY C: Window Functions (Simplified)
-- ==========================================

-- 15. ROW_NUMBER
SELECT sale_id, amount,
ROW_NUMBER() OVER (ORDER BY sale_id) as row_num
FROM sales;

-- 16. RANK
SELECT sale_id, amount,
RANK() OVER (ORDER BY amount) as rank_val
FROM sales;

-- 17. PARTITION BY
SELECT name, department, salary,
RANK() OVER (PARTITION BY department ORDER BY salary) as dept_rank
FROM employees;

-- 18. Running Total
SELECT sale_id, amount,
SUM(amount) OVER (ORDER BY sale_id) as running_total
FROM sales;

-- 19. LAG
SELECT sale_id, amount,
LAG(amount, 1) OVER (ORDER BY sale_id) as prev_amount
FROM sales;

-- 20. LEAD
SELECT sale_id, amount,
LEAD(amount, 1) OVER (ORDER BY sale_id) as next_amount
FROM sales;

-- 21. Moving Average (Simplified)
SELECT sale_id, amount,
AVG(amount) OVER (ORDER BY sale_id) as moving_avg
FROM sales;

-- 22. NTILE
SELECT name, salary,
NTILE(4) OVER (ORDER BY salary) as salary_quartile
FROM employees;


-- ==========================================
-- CATEGORY D: CTEs
-- ==========================================

-- 23. CTE
WITH high_earners AS (
    SELECT name, salary FROM employees WHERE salary > 45000
)
SELECT * FROM high_earners;

-- 24. CTE with Joins
WITH sales_summary AS (
    SELECT employee_id, SUM(amount) as total FROM sales GROUP BY employee_id
)
SELECT e.name, s.total
FROM employees e
JOIN sales_summary s ON e.id = s.employee_id;

-- 25. Multiple CTEs
WITH 
dept_max AS (SELECT department, MAX(salary) as max_sal FROM employees GROUP BY department),
total_pay AS (SELECT SUM(salary) as total FROM employees)
SELECT * FROM dept_max, total_pay;

-- 26. Scalar Subquery in SELECT
SELECT name, salary, 
    (SELECT AVG(salary) FROM employees) as company_avg
FROM employees;

-- 27. Table Subquery
SELECT * FROM (
    SELECT employee_id, SUM(amount) as total FROM sales GROUP BY employee_id
) as sales_totals WHERE total > 100;

-- 28. EXISTS
SELECT name FROM employees e 
WHERE EXISTS (SELECT 1 FROM sales s WHERE s.employee_id = e.id);

-- 29. NOT IN
SELECT name FROM employees 
WHERE id NOT IN (SELECT employee_id FROM sales WHERE employee_id IS NOT NULL);


-- ==========================================
-- CATEGORY E: Optimization
-- ==========================================

-- 30. EXPLAIN
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE name = 'Alice';

-- 31. Create Index (FIXED - drops first if exists)
DROP INDEX IF EXISTS idx_name;
CREATE INDEX idx_name ON employees(name);

-- 32. Check Index Usage
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE name = 'Alice';


-- ==========================================
-- BONUS Queries
-- ==========================================

-- 33. Percentage of Total
SELECT category, price,
    (price * 100.0 / (SELECT SUM(price) FROM products)) as pct_total
FROM products;

-- 34. Top Per Group
SELECT name, department, salary
FROM employees e1
WHERE salary = (SELECT MAX(salary) FROM employees e2 WHERE e1.department = e2.department);

-- 35. Running Count
SELECT sale_id, amount,
    COUNT(*) OVER (ORDER BY sale_id) as running_count
FROM sales;