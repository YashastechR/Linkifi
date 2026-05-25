# SQL Learning — PostgreSQL Complete Reference

## Project Structure

```
sql-learning/
├── scripts/
│   ├── 01_schema.sql      — DDL: tables, constraints, indexes
│   ├── 02_seed_data.sql   — DML: INSERT seed records
│   └── 03_queries.sql     — 55+ practice queries
└── README.md              — this file
```

---

## Phase 1 — Installation

### Install PostgreSQL (Ubuntu / Debian / WSL)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Install PostgreSQL (macOS with Homebrew)

```bash
brew install postgresql@16
brew services start postgresql@16
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Install PostgreSQL (Windows)

Download the installer from https://www.postgresql.org/download/windows  
Choose version 16 → run installer → keep default port 5432 → set a password for `postgres`.

### Verify Installation

```bash
psql --version         # should print: psql (PostgreSQL) 16.x
sudo -u postgres psql  # opens the psql shell
```

---

## Phase 2 — pgAdmin / DBeaver Setup

### Option A: pgAdmin (GUI, beginner-friendly)

1. Download from https://www.pgadmin.org/download/
2. Open pgAdmin → right-click **Servers** → **Register → Server**
3. Name: `Local`, Host: `localhost`, Port: `5432`, User: `postgres`, Password: your password
4. Click **Save**

### Option B: DBeaver (Universal DB tool — recommended)

1. Download from https://dbeaver.io/download/
2. New Connection → PostgreSQL → host `localhost`, port `5432`, database `postgres`, user `postgres`
3. Test Connection → Finish

---

## Phase 3 — Create the Practice Database

```sql
-- In psql or pgAdmin query tool:
CREATE DATABASE ecommerce_db;
\c ecommerce_db          -- connect to it (psql only)
```

Or from the terminal:

```bash
createdb -U postgres ecommerce_db
psql -U postgres -d ecommerce_db -f scripts/01_schema.sql
psql -U postgres -d ecommerce_db -f scripts/02_seed_data.sql
psql -U postgres -d ecommerce_db -f scripts/03_queries.sql
```

---

## Phase 4 — SQL Reference

### DDL — Data Definition Language

```sql
-- CREATE TABLE with common constraints
CREATE TABLE products (
    product_id  SERIAL PRIMARY KEY,          -- auto-increment PK
    name        VARCHAR(200) NOT NULL,        -- required field
    price       NUMERIC(12,2) CHECK (price >= 0), -- validation
    category_id INT REFERENCES categories(category_id), -- FK
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- ALTER TABLE
ALTER TABLE products ADD COLUMN tags TEXT[];
ALTER TABLE products DROP COLUMN tags;
ALTER TABLE products RENAME COLUMN name TO product_name;
ALTER TABLE products ALTER COLUMN price TYPE NUMERIC(14,2);
ALTER TABLE products ADD CONSTRAINT uq_sku UNIQUE (sku);

-- DROP TABLE
DROP TABLE IF EXISTS products;           -- safe, no error if missing
DROP TABLE products CASCADE;             -- drops dependent objects too

-- INDEXES
CREATE INDEX idx_products_price ON products(price);       -- single col
CREATE INDEX idx_orders_cust_status ON orders(customer_id, status); -- composite
CREATE UNIQUE INDEX uix_email ON customers(email);
DROP INDEX idx_products_price;
```

### DML — Data Manipulation Language

```sql
-- INSERT single row
INSERT INTO customers (first_name, last_name, email)
VALUES ('Arun', 'Das', 'arun.das@gmail.com');

-- INSERT multiple rows
INSERT INTO products (name, price, category_id)
VALUES
  ('Product A', 999,  1),
  ('Product B', 1999, 2),
  ('Product C', 499,  1);

-- RETURNING — get inserted/updated values back
INSERT INTO customers (first_name, email)
VALUES ('Test', 'test@test.com')
RETURNING customer_id, created_at;

-- UPDATE
UPDATE products SET price = 899 WHERE product_id = 17;

-- UPDATE multiple cols
UPDATE customers
SET loyalty_tier = 'gold', updated_at = NOW()
WHERE customer_id = 4;

-- DELETE
DELETE FROM product_reviews WHERE review_id = 5;

-- UPSERT (INSERT … ON CONFLICT)
INSERT INTO customers (email, first_name, last_name)
VALUES ('test@test.com', 'Test', 'User')
ON CONFLICT (email)
DO UPDATE SET first_name = EXCLUDED.first_name;
```

### SELECT Fundamentals

```sql
-- Basic SELECT
SELECT *              FROM products;
SELECT name, price    FROM products;
SELECT name AS product_name, price * 1.18 AS price_with_gst FROM products;

-- WHERE operators
WHERE price > 1000
WHERE price BETWEEN 500 AND 5000
WHERE name LIKE 'Sony%'          -- starts with Sony
WHERE name ILIKE '%phone%'       -- case-insensitive contains
WHERE category_id IN (1, 3, 7)
WHERE category_id NOT IN (2, 4)
WHERE phone IS NULL
WHERE phone IS NOT NULL

-- ORDER BY
ORDER BY price ASC
ORDER BY price DESC
ORDER BY category_id ASC, price DESC   -- multi-column

-- LIMIT & OFFSET (pagination)
LIMIT 10 OFFSET 0     -- page 1
LIMIT 10 OFFSET 10    -- page 2
LIMIT 10 OFFSET 20    -- page 3

-- DISTINCT
SELECT DISTINCT loyalty_tier FROM customers;
SELECT DISTINCT ON (category_id) category_id, name, price
FROM products ORDER BY category_id, price DESC;
```

### Aggregate Functions

```sql
SELECT
    COUNT(*)                AS total_rows,
    COUNT(phone)            AS has_phone,     -- NULLs excluded
    SUM(price)              AS total_value,
    AVG(price)              AS avg_price,
    ROUND(AVG(price), 2)    AS avg_price_2dp,
    MIN(price)              AS cheapest,
    MAX(price)              AS most_expensive
FROM products;

-- GROUP BY + HAVING
SELECT category_id, COUNT(*), AVG(price)
FROM   products
GROUP  BY category_id
HAVING COUNT(*) > 2;          -- filter after grouping
```

### JOINs

```sql
-- INNER JOIN — only matching rows
SELECT p.name, c.name AS category
FROM products p
INNER JOIN categories c ON c.category_id = p.category_id;

-- LEFT JOIN — all left + matching right (NULLs for no match)
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;

-- RIGHT JOIN — all right + matching left
SELECT o.order_id, c.name
FROM orders o
RIGHT JOIN customers c ON c.customer_id = o.customer_id;

-- FULL OUTER JOIN — all rows from both sides
SELECT p.name, oi.order_id
FROM products p
FULL OUTER JOIN order_items oi ON oi.product_id = p.product_id;

-- SELF JOIN — same table twice (e.g. category hierarchy)
SELECT child.name, parent.name AS parent
FROM categories child
JOIN categories parent ON parent.category_id = child.parent_id;
```

### Subqueries

```sql
-- In WHERE
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- In FROM (derived table)
SELECT category_id, avg_price
FROM (
    SELECT category_id, AVG(price) AS avg_price
    FROM products GROUP BY category_id
) averages;

-- Correlated subquery
SELECT name FROM products p
WHERE price = (
    SELECT MAX(price) FROM products WHERE category_id = p.category_id
);

-- EXISTS
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders WHERE customer_id = c.customer_id
);
```

### CTEs (Common Table Expressions)

```sql
-- Basic CTE
WITH top_customers AS (
    SELECT customer_id, SUM(total) AS spend
    FROM orders
    WHERE status = 'delivered'
    GROUP BY customer_id
    HAVING SUM(total) > 50000
)
SELECT c.first_name, c.last_name, t.spend
FROM customers c
JOIN top_customers t ON t.customer_id = c.customer_id;

-- Multiple CTEs
WITH revenue AS (...),
     costs   AS (...)
SELECT * FROM revenue JOIN costs USING (product_id);
```

### Window Functions

```sql
-- RANK, ROW_NUMBER, DENSE_RANK
SELECT name, price,
    RANK()       OVER (PARTITION BY category_id ORDER BY price DESC) AS rank,
    ROW_NUMBER() OVER (ORDER BY price DESC)                          AS row_num,
    DENSE_RANK() OVER (ORDER BY price DESC)                          AS dense_rank
FROM products;

-- SUM / AVG / COUNT as windows
SELECT order_id, total,
    SUM(total) OVER ()                            AS grand_total,
    SUM(total) OVER (ORDER BY ordered_at)         AS running_total,
    AVG(total) OVER (PARTITION BY customer_id)    AS customer_avg
FROM orders;

-- LAG / LEAD — access adjacent rows
SELECT ordered_at, total,
    LAG(total)  OVER (ORDER BY ordered_at) AS prev_order,
    LEAD(total) OVER (ORDER BY ordered_at) AS next_order
FROM orders;

-- NTILE — split rows into N buckets
SELECT customer_id, total,
    NTILE(4) OVER (ORDER BY total) AS quartile
FROM orders;
```

### Useful String & Date Functions

```sql
-- String
UPPER(name)           -- ALL CAPS
LOWER(email)          -- lowercase
INITCAP(first_name)   -- Title Case
LENGTH(name)          -- character count
TRIM(name)            -- remove whitespace
LTRIM / RTRIM
SUBSTRING(email, 1, 5)
SPLIT_PART(email, '@', 2)   -- domain part
CONCAT(first_name, ' ', last_name)
first_name || ' ' || last_name   -- same with ||

-- Date / Time
NOW()                         -- current timestamp
CURRENT_DATE                  -- today's date only
EXTRACT(YEAR FROM ordered_at)
DATE_TRUNC('month', ordered_at)
ordered_at + INTERVAL '30 days'
AGE(date_of_birth)            -- interval from DOB to now
TO_CHAR(ordered_at, 'DD Mon YYYY')

-- Casting
price::TEXT           -- numeric to text
'42'::INT             -- text to integer
CAST(price AS TEXT)   -- same, more explicit
```

### CASE Expressions

```sql
SELECT name, price,
    CASE
        WHEN price < 1000         THEN 'Budget'
        WHEN price BETWEEN 1000 AND 9999 THEN 'Mid-range'
        ELSE 'Premium'
    END AS tier
FROM products;
```

---

## Phase 5 — psql Cheat Sheet

```bash
\l              -- list databases
\c ecommerce_db -- connect to database
\dt             -- list tables
\d products     -- describe table structure
\di             -- list indexes
\df             -- list functions
\timing         -- toggle query timing
\e              -- open query in editor
\q              -- quit psql
\i scripts/01_schema.sql  -- run a file
```

---

## Key Concepts

| Concept | What It Does |
|---|---|
| PRIMARY KEY | Uniquely identifies each row; always NOT NULL |
| FOREIGN KEY | Links to another table's primary key |
| NOT NULL | Field must have a value |
| UNIQUE | No duplicate values allowed |
| CHECK | Validates a condition on insert/update |
| DEFAULT | Value used if none provided |
| INDEX | Speeds up reads; slows writes slightly |
| CASCADE | Delete/update propagates to child rows |
| SERIAL | Auto-incrementing integer (shorthand for SEQUENCE) |
| GENERATED ALWAYS AS | Computed column stored on disk |

---

## Recommended YouTube Videos

| Topic | Search Term | Channel |
|---|---|---|
| SQL Full Course | "SQL complete course for beginners" | freeCodeCamp |
| PostgreSQL Setup | "PostgreSQL tutorial for beginners" | Programming with Mosh |
| Database Design | "Database design basics for beginners" | Traversy Media |
| SQL for Data Eng | "SQL for data engineering" | freeCodeCamp |
| Window Functions | "SQL window functions explained" | Alex The Analyst |