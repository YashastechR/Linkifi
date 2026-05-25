-- ============================================================
-- 50+ SQL PRACTICE QUERIES
-- Covers: SELECT, WHERE, LIKE/ILIKE, IN, BETWEEN,
--         ORDER BY, LIMIT, DISTINCT, Aggregates,
--         JOINs, Subqueries, CTEs, Window Functions,
--         UPDATE, DELETE, RETURNING
-- ============================================================


-- ═══════════════════════════════════════════════════════════
-- SECTION 1: BASIC SELECT & WHERE (Q1–Q10)
-- ═══════════════════════════════════════════════════════════

-- Q1: All active customers
SELECT * FROM customers WHERE is_active = TRUE;

-- Q2: Customers in gold or platinum tier
SELECT customer_id, first_name, last_name, loyalty_tier
FROM   customers
WHERE  loyalty_tier IN ('gold', 'platinum')
ORDER  BY loyalty_tier, last_name;

-- Q3: Products priced between ₹1000 and ₹10000
SELECT name, price, stock_qty
FROM   products
WHERE  price BETWEEN 1000 AND 10000
  AND  is_active = TRUE
ORDER  BY price ASC;

-- Q4: Search products by name (case-insensitive)
SELECT product_id, name, price
FROM   products
WHERE  name ILIKE '%headphone%';

-- Q5: Orders placed in January 2025
SELECT order_id, customer_id, total, status, ordered_at
FROM   orders
WHERE  ordered_at BETWEEN '2025-01-01' AND '2025-01-31 23:59:59'
ORDER  BY ordered_at;

-- Q6: Products with low stock (fewer than 30 units)
SELECT name, stock_qty, sku
FROM   products
WHERE  stock_qty < 30
  AND  is_active = TRUE
ORDER  BY stock_qty ASC;

-- Q7: Delivered orders only
SELECT order_id, customer_id, total, ordered_at
FROM   orders
WHERE  status = 'delivered'
ORDER  BY ordered_at DESC;

-- Q8: Customers born in the 1990s
SELECT first_name, last_name, date_of_birth
FROM   customers
WHERE  date_of_birth BETWEEN '1990-01-01' AND '1999-12-31'
ORDER  BY date_of_birth;

-- Q9: Products whose SKU starts with 'APP'
SELECT name, sku, price
FROM   products
WHERE  sku LIKE 'APP%';

-- Q10: DISTINCT order statuses in the system
SELECT DISTINCT status FROM orders ORDER BY status;


-- ═══════════════════════════════════════════════════════════
-- SECTION 2: ORDER BY, LIMIT & OFFSET (Q11–Q15)
-- ═══════════════════════════════════════════════════════════

-- Q11: Top 5 most expensive products
SELECT name, price
FROM   products
WHERE  is_active = TRUE
ORDER  BY price DESC
LIMIT  5;

-- Q12: Cheapest 5 products with stock
SELECT name, price, stock_qty
FROM   products
WHERE  is_active = TRUE AND stock_qty > 0
ORDER  BY price ASC
LIMIT  5;

-- Q13: Pagination — page 2 of customers (5 per page)
SELECT customer_id, first_name, last_name, email
FROM   customers
ORDER  BY customer_id
LIMIT  5 OFFSET 5;

-- Q14: 3 most recent orders
SELECT order_id, customer_id, total, status, ordered_at
FROM   orders
ORDER  BY ordered_at DESC
LIMIT  3;

-- Q15: Highest-rated products (from reviews)
SELECT product_id, AVG(rating) AS avg_rating, COUNT(*) AS review_count
FROM   product_reviews
GROUP  BY product_id
ORDER  BY avg_rating DESC, review_count DESC
LIMIT  5;


-- ═══════════════════════════════════════════════════════════
-- SECTION 3: AGGREGATE FUNCTIONS (Q16–Q22)
-- ═══════════════════════════════════════════════════════════

-- Q16: Total revenue from delivered orders
SELECT SUM(total) AS total_revenue
FROM   orders
WHERE  status = 'delivered';

-- Q17: Revenue, order count, and average order value by status
SELECT status,
       COUNT(*)           AS order_count,
       SUM(total)         AS total_revenue,
       ROUND(AVG(total),2) AS avg_order_value,
       MAX(total)         AS largest_order
FROM   orders
GROUP  BY status
ORDER  BY total_revenue DESC;

-- Q18: Number of products per category
SELECT c.name AS category, COUNT(p.product_id) AS product_count
FROM   categories c
LEFT   JOIN products p ON p.category_id = c.category_id
WHERE  c.parent_id IS NOT NULL    -- sub-categories only
GROUP  BY c.name
ORDER  BY product_count DESC;

-- Q19: Average product rating per product
SELECT p.name, ROUND(AVG(r.rating),2) AS avg_rating, COUNT(r.*) AS reviews
FROM   products p
JOIN   product_reviews r ON r.product_id = p.product_id
GROUP  BY p.name
HAVING COUNT(r.*) >= 2
ORDER  BY avg_rating DESC;

-- Q20: Customer spend summary
SELECT c.customer_id,
       c.first_name || ' ' || c.last_name AS full_name,
       COUNT(o.order_id)   AS total_orders,
       SUM(o.total)        AS lifetime_value
FROM   customers c
JOIN   orders o ON o.customer_id = c.customer_id
WHERE  o.status NOT IN ('cancelled', 'refunded')
GROUP  BY c.customer_id, full_name
ORDER  BY lifetime_value DESC;

-- Q21: Total products and average price per supplier
SELECT s.name AS supplier,
       COUNT(p.product_id)    AS products_supplied,
       ROUND(AVG(p.price),2)  AS avg_price
FROM   suppliers s
JOIN   products  p ON p.supplier_id = s.supplier_id
GROUP  BY s.name
ORDER  BY products_supplied DESC;

-- Q22: Min, max, and avg product price
SELECT MIN(price) AS cheapest, MAX(price) AS most_expensive, ROUND(AVG(price),2) AS avg_price
FROM   products WHERE is_active = TRUE;


-- ═══════════════════════════════════════════════════════════
-- SECTION 4: JOINs (Q23–Q30)
-- ═══════════════════════════════════════════════════════════

-- Q23: Full order details — customer, order, and status
SELECT o.order_id,
       c.first_name || ' ' || c.last_name AS customer,
       c.email,
       o.status,
       o.total,
       o.ordered_at
FROM   orders o
JOIN   customers c ON c.customer_id = o.customer_id
ORDER  BY o.ordered_at DESC;

-- Q24: Order line items with product names
SELECT o.order_id,
       p.name            AS product,
       oi.quantity,
       oi.unit_price,
       oi.line_total
FROM   order_items oi
JOIN   orders    o ON o.order_id   = oi.order_id
JOIN   products  p ON p.product_id = oi.product_id
ORDER  BY o.order_id, oi.order_item_id;

-- Q25: Products with their category and supplier
SELECT p.name        AS product,
       cat.name      AS category,
       s.name        AS supplier,
       p.price,
       p.stock_qty
FROM   products  p
JOIN   categories cat ON cat.category_id = p.category_id
LEFT   JOIN suppliers s ON s.supplier_id = p.supplier_id
ORDER  BY cat.name, p.price;

-- Q26: Customers with their default shipping addresses
SELECT c.first_name || ' ' || c.last_name AS customer,
       a.street_line1, a.city, a.state, a.postal_code
FROM   customers c
LEFT   JOIN addresses a ON a.customer_id = c.customer_id
                       AND a.address_type = 'shipping'
                       AND a.is_default   = TRUE
ORDER  BY c.customer_id;

-- Q27: Reviews with customer and product info
SELECT r.review_id,
       p.name                              AS product,
       c.first_name || ' ' || c.last_name AS reviewer,
       r.rating,
       r.title,
       r.created_at
FROM   product_reviews r
JOIN   products  p ON p.product_id  = r.product_id
JOIN   customers c ON c.customer_id = r.customer_id
ORDER  BY r.created_at DESC;

-- Q28: Sub-categories with parent category name
SELECT child.name  AS sub_category,
       parent.name AS parent_category
FROM   categories child
JOIN   categories parent ON parent.category_id = child.parent_id
ORDER  BY parent.name, child.name;

-- Q29: All categories including those with no products (LEFT JOIN)
SELECT c.name AS category, COUNT(p.product_id) AS products
FROM   categories c
LEFT   JOIN products p ON p.category_id = c.category_id AND p.is_active = TRUE
GROUP  BY c.name
ORDER  BY products DESC;

-- Q30: Complete order receipt for order #1
SELECT o.order_id,
       c.first_name || ' ' || c.last_name  AS customer,
       a.city,
       oi.quantity,
       p.name                              AS product,
       oi.unit_price,
       oi.line_total,
       o.subtotal, o.discount, o.tax, o.shipping_fee, o.total,
       o.status
FROM   orders o
JOIN   customers   c  ON c.customer_id  = o.customer_id
LEFT   JOIN addresses   a  ON a.address_id   = o.address_id
JOIN   order_items oi ON oi.order_id    = o.order_id
JOIN   products    p  ON p.product_id   = oi.product_id
WHERE  o.order_id = 1;


-- ═══════════════════════════════════════════════════════════
-- SECTION 5: SUBQUERIES (Q31–Q35)
-- ═══════════════════════════════════════════════════════════

-- Q31: Products that have never been ordered
SELECT product_id, name, stock_qty
FROM   products
WHERE  product_id NOT IN (
    SELECT DISTINCT product_id FROM order_items
)
AND is_active = TRUE;

-- Q32: Customers who placed more than 1 order
SELECT customer_id, first_name, last_name
FROM   customers
WHERE  customer_id IN (
    SELECT customer_id
    FROM   orders
    GROUP  BY customer_id
    HAVING COUNT(*) > 1
);

-- Q33: Products priced above the category average
SELECT p.name, cat.name AS category, p.price,
       ROUND(avg_prices.avg_price, 2) AS category_avg
FROM   products p
JOIN   categories cat ON cat.category_id = p.category_id
JOIN   (
    SELECT category_id, AVG(price) AS avg_price
    FROM   products
    WHERE  is_active = TRUE
    GROUP  BY category_id
) avg_prices ON avg_prices.category_id = p.category_id
WHERE  p.price > avg_prices.avg_price
ORDER  BY category, p.price DESC;

-- Q34: The customer who spent the most
SELECT c.first_name || ' ' || c.last_name AS top_customer, t.total_spend
FROM   customers c
JOIN   (
    SELECT customer_id, SUM(total) AS total_spend
    FROM   orders
    WHERE  status NOT IN ('cancelled','refunded')
    GROUP  BY customer_id
    ORDER  BY total_spend DESC
    LIMIT  1
) t ON t.customer_id = c.customer_id;

-- Q35: Orders above the average order total
SELECT order_id, customer_id, total, status
FROM   orders
WHERE  total > (SELECT AVG(total) FROM orders WHERE status = 'delivered')
  AND  status = 'delivered'
ORDER  BY total DESC;


-- ═══════════════════════════════════════════════════════════
-- SECTION 6: CTEs & WINDOW FUNCTIONS (Q36–Q42)
-- ═══════════════════════════════════════════════════════════

-- Q36: CTE — monthly revenue report
WITH monthly_revenue AS (
    SELECT DATE_TRUNC('month', ordered_at) AS month,
           SUM(total)    AS revenue,
           COUNT(*)      AS orders
    FROM   orders
    WHERE  status NOT IN ('cancelled','refunded')
    GROUP  BY 1
)
SELECT TO_CHAR(month, 'Mon YYYY') AS period,
       orders,
       revenue
FROM   monthly_revenue
ORDER  BY month;

-- Q37: CTE — top product per category by revenue
WITH product_revenue AS (
    SELECT oi.product_id,
           p.name                AS product_name,
           p.category_id,
           SUM(oi.line_total)   AS revenue
    FROM   order_items oi
    JOIN   products p ON p.product_id = oi.product_id
    GROUP  BY oi.product_id, p.name, p.category_id
),
ranked AS (
    SELECT pr.*, c.name AS category,
           RANK() OVER (PARTITION BY pr.category_id ORDER BY pr.revenue DESC) AS rnk
    FROM   product_revenue pr
    JOIN   categories c ON c.category_id = pr.category_id
)
SELECT category, product_name, revenue
FROM   ranked
WHERE  rnk = 1
ORDER  BY revenue DESC;

-- Q38: Running total of revenue over time
SELECT ordered_at::DATE AS order_date,
       total,
       SUM(total) OVER (ORDER BY ordered_at) AS running_total
FROM   orders
WHERE  status NOT IN ('cancelled','refunded')
ORDER  BY ordered_at;

-- Q39: Rank customers by lifetime value
SELECT c.first_name || ' ' || c.last_name AS customer,
       c.loyalty_tier,
       SUM(o.total) AS lifetime_value,
       RANK() OVER (ORDER BY SUM(o.total) DESC) AS spend_rank
FROM   customers c
JOIN   orders o ON o.customer_id = c.customer_id
WHERE  o.status NOT IN ('cancelled','refunded')
GROUP  BY c.customer_id, c.first_name, c.last_name, c.loyalty_tier
ORDER  BY spend_rank;

-- Q40: LAG — month-over-month revenue change
WITH monthly AS (
    SELECT DATE_TRUNC('month', ordered_at)   AS month,
           SUM(total) AS revenue
    FROM   orders WHERE status NOT IN ('cancelled','refunded')
    GROUP  BY 1
)
SELECT TO_CHAR(month, 'Mon YYYY')               AS period,
       revenue,
       LAG(revenue) OVER (ORDER BY month)       AS prev_month,
       revenue - LAG(revenue) OVER (ORDER BY month) AS change
FROM   monthly
ORDER  BY month;

-- Q41: NTILE — segment customers into 4 spend quartiles
SELECT c.first_name || ' ' || c.last_name AS customer,
       SUM(o.total) AS total_spend,
       NTILE(4) OVER (ORDER BY SUM(o.total)) AS spend_quartile
FROM   customers c
JOIN   orders o ON o.customer_id = c.customer_id
WHERE  o.status NOT IN ('cancelled','refunded')
GROUP  BY c.customer_id, c.first_name, c.last_name
ORDER  BY total_spend DESC;

-- Q42: Product sales ranked within each category
SELECT cat.name   AS category,
       p.name     AS product,
       SUM(oi.line_total)                                                   AS revenue,
       RANK() OVER (PARTITION BY cat.category_id ORDER BY SUM(oi.line_total) DESC) AS rank_in_category
FROM   order_items oi
JOIN   products    p   ON p.product_id   = oi.product_id
JOIN   categories  cat ON cat.category_id = p.category_id
GROUP  BY cat.category_id, cat.name, p.product_id, p.name
ORDER  BY cat.name, rank_in_category;


-- ═══════════════════════════════════════════════════════════
-- SECTION 7: DML — UPDATE & DELETE (Q43–Q50)
-- ═══════════════════════════════════════════════════════════

-- Q43: Upgrade customers to gold if they spent over ₹50,000
UPDATE customers
SET    loyalty_tier = 'gold',
       updated_at   = NOW()
WHERE  customer_id IN (
    SELECT customer_id
    FROM   orders
    WHERE  status NOT IN ('cancelled','refunded')
    GROUP  BY customer_id
    HAVING SUM(total) > 50000
)
AND loyalty_tier = 'silver'
RETURNING customer_id, first_name, last_name, loyalty_tier;

-- Q44: Apply a 10% price cut to all books
UPDATE products
SET    price      = ROUND(price * 0.90, 2),
       updated_at = NOW()
WHERE  category_id = (SELECT category_id FROM categories WHERE slug = 'books')
RETURNING product_id, name, price AS new_price;

-- Q45: Increase stock by 50 for products below 30 units
UPDATE products
SET    stock_qty  = stock_qty + 50,
       updated_at = NOW()
WHERE  stock_qty < 30
  AND  is_active = TRUE
RETURNING product_id, name, stock_qty;

-- Q46: Mark all confirmed orders older than 30 days as processing
UPDATE orders
SET    status     = 'processing',
       updated_at = NOW()
WHERE  status     = 'confirmed'
  AND  ordered_at < NOW() - INTERVAL '30 days'
RETURNING order_id, status, ordered_at;

-- Q47: Deactivate products with zero stock
UPDATE products
SET    is_active  = FALSE,
       updated_at = NOW()
WHERE  stock_qty  = 0
RETURNING product_id, name, stock_qty;

-- Q48: DELETE — remove unverified reviews older than 6 months
DELETE FROM product_reviews
WHERE  is_verified = FALSE
  AND  created_at  < NOW() - INTERVAL '6 months'
RETURNING review_id, product_id, customer_id;

-- Q49: Soft-delete an inactive customer (UPDATE, not DELETE)
UPDATE customers
SET    is_active  = FALSE,
       updated_at = NOW()
WHERE  customer_id = 14
RETURNING customer_id, first_name, is_active;

-- Q50: Bulk INSERT new products with RETURNING
INSERT INTO products (category_id, supplier_id, name, slug, price, cost_price, stock_qty, sku)
VALUES
  (5, 7, 'Clean Code',          'clean-code-martin',         699, 290, 200, 'CLEAN-CODE-1'),
  (5, 7, 'Designing Data Apps', 'designing-data-apps',       999, 420, 100, 'DES-DATA-APP'),
  (9, 3, 'JBL Tune 520BT',      'jbl-tune-520bt',           3999,3100,  60, 'JBL-T520BT')
RETURNING product_id, name, price;

-- Q51: UPSERT — insert or update supplier rating
INSERT INTO suppliers (name, contact_email, country, rating)
VALUES ('NextGen Supplies', 'info@nextgen.in', 'India', 4.5)
ON CONFLICT (name)
DO UPDATE SET rating = EXCLUDED.rating, is_active = TRUE
RETURNING supplier_id, name, rating;

-- Q52: Complex filter — high-value unshipped orders from gold/platinum customers
SELECT o.order_id,
       c.first_name || ' ' || c.last_name AS customer,
       c.loyalty_tier,
       o.total,
       o.status,
       o.ordered_at
FROM   orders    o
JOIN   customers c ON c.customer_id = o.customer_id
WHERE  o.status  IN ('confirmed','processing','shipped')
  AND  o.total   > 50000
  AND  c.loyalty_tier IN ('gold','platinum')
ORDER  BY o.total DESC;

-- Q53: Date/time — orders grouped by day of the week
SELECT TO_CHAR(ordered_at, 'Day') AS day_of_week,
       COUNT(*)                   AS order_count,
       SUM(total)                 AS revenue
FROM   orders
WHERE  status NOT IN ('cancelled','refunded')
GROUP  BY EXTRACT(DOW FROM ordered_at), TO_CHAR(ordered_at, 'Day')
ORDER  BY EXTRACT(DOW FROM ordered_at);

-- Q54: String functions — format customer display name
SELECT customer_id,
       UPPER(last_name)  || ', ' || INITCAP(first_name) AS display_name,
       SUBSTRING(email, POSITION('@' IN email) + 1)     AS email_domain,
       LENGTH(phone)                                     AS phone_length
FROM   customers
ORDER  BY last_name;

-- Q55: CASE — classify products by price tier
SELECT name, price,
       CASE
           WHEN price < 1000             THEN 'Budget'
           WHEN price BETWEEN 1000 AND 9999 THEN 'Mid-range'
           WHEN price BETWEEN 10000 AND 49999 THEN 'Premium'
           ELSE 'Luxury'
       END AS price_tier
FROM   products
WHERE  is_active = TRUE
ORDER  BY price;

SELECT 'All 55 queries executed successfully!' AS status;