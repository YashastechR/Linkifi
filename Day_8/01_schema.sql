-- ============================================================
-- E-COMMERCE DATABASE SCHEMA
-- PostgreSQL DDL Operations
-- ============================================================

-- Drop existing tables (for clean re-runs)
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS product_reviews CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS addresses CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;

-- ============================================================
-- TABLE 1: customers
-- ============================================================
CREATE TABLE customers (
    customer_id   SERIAL PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    phone         VARCHAR(20),
    date_of_birth DATE,
    loyalty_tier  VARCHAR(10)  NOT NULL DEFAULT 'bronze'
                  CHECK (loyalty_tier IN ('bronze', 'silver', 'gold', 'platinum')),
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE customers IS 'Stores registered customer information';

-- ============================================================
-- TABLE 2: addresses
-- ============================================================
CREATE TABLE addresses (
    address_id    SERIAL PRIMARY KEY,
    customer_id   INT          NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    address_type  VARCHAR(10)  NOT NULL DEFAULT 'shipping'
                  CHECK (address_type IN ('billing', 'shipping')),
    street_line1  VARCHAR(150) NOT NULL,
    street_line2  VARCHAR(150),
    city          VARCHAR(80)  NOT NULL,
    state         VARCHAR(80),
    postal_code   VARCHAR(20)  NOT NULL,
    country       VARCHAR(60)  NOT NULL DEFAULT 'India',
    is_default    BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABLE 3: suppliers
-- ============================================================
CREATE TABLE suppliers (
    supplier_id   SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    country       VARCHAR(60)  NOT NULL DEFAULT 'India',
    rating        NUMERIC(3,2) CHECK (rating BETWEEN 0 AND 5),
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABLE 4: categories
-- ============================================================
CREATE TABLE categories (
    category_id   SERIAL PRIMARY KEY,
    name          VARCHAR(80)  NOT NULL UNIQUE,
    slug          VARCHAR(80)  NOT NULL UNIQUE,
    parent_id     INT          REFERENCES categories(category_id) ON DELETE SET NULL,
    description   TEXT,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ============================================================
-- TABLE 5: products
-- ============================================================
CREATE TABLE products (
    product_id    SERIAL PRIMARY KEY,
    category_id   INT          NOT NULL REFERENCES categories(category_id),
    supplier_id   INT          REFERENCES suppliers(supplier_id) ON DELETE SET NULL,
    name          VARCHAR(200) NOT NULL,
    slug          VARCHAR(200) NOT NULL UNIQUE,
    description   TEXT,
    price         NUMERIC(12,2) NOT NULL CHECK (price >= 0),
    cost_price    NUMERIC(12,2) CHECK (cost_price >= 0),
    stock_qty     INT          NOT NULL DEFAULT 0 CHECK (stock_qty >= 0),
    sku           VARCHAR(50)  UNIQUE,
    weight_kg     NUMERIC(8,3),
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABLE 6: product_reviews
-- ============================================================
CREATE TABLE product_reviews (
    review_id     SERIAL PRIMARY KEY,
    product_id    INT          NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    customer_id   INT          NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    rating        SMALLINT     NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title         VARCHAR(150),
    body          TEXT,
    is_verified   BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    UNIQUE (product_id, customer_id)   -- one review per customer per product
);

-- ============================================================
-- TABLE 7: orders
-- ============================================================
CREATE TABLE orders (
    order_id      SERIAL PRIMARY KEY,
    customer_id   INT          NOT NULL REFERENCES customers(customer_id),
    address_id    INT          REFERENCES addresses(address_id) ON DELETE SET NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending','confirmed','processing','shipped','delivered','cancelled','refunded')),
    subtotal      NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (subtotal >= 0),
    discount      NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (discount >= 0),
    tax           NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (tax >= 0),
    shipping_fee  NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (shipping_fee >= 0),
    total         NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    notes         TEXT,
    ordered_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABLE 8: order_items
-- ============================================================
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id      INT          NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id    INT          NOT NULL REFERENCES products(product_id),
    quantity      INT          NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    discount      NUMERIC(12,2) NOT NULL DEFAULT 0,
    line_total    NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price - discount) STORED
);

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================
CREATE INDEX idx_customers_email        ON customers(email);
CREATE INDEX idx_customers_loyalty      ON customers(loyalty_tier);
CREATE INDEX idx_products_category      ON products(category_id);
CREATE INDEX idx_products_supplier      ON products(supplier_id);
CREATE INDEX idx_products_price         ON products(price);
CREATE INDEX idx_products_active        ON products(is_active);
CREATE INDEX idx_orders_customer        ON orders(customer_id);
CREATE INDEX idx_orders_status          ON orders(status);
CREATE INDEX idx_orders_ordered_at      ON orders(ordered_at);
CREATE INDEX idx_order_items_order      ON order_items(order_id);
CREATE INDEX idx_order_items_product    ON order_items(product_id);
CREATE INDEX idx_reviews_product        ON product_reviews(product_id);

-- ============================================================
-- ALTER TABLE EXAMPLES
-- ============================================================
ALTER TABLE customers ADD COLUMN IF NOT EXISTS referral_code VARCHAR(20);
ALTER TABLE products  ADD COLUMN IF NOT EXISTS tags TEXT[];
ALTER TABLE orders    ADD COLUMN IF NOT EXISTS coupon_code VARCHAR(30);

-- Rename a column example (commented out to avoid breaking later scripts)
-- ALTER TABLE customers RENAME COLUMN phone TO phone_number;

-- Change data type example (commented out)
-- ALTER TABLE suppliers ALTER COLUMN rating TYPE NUMERIC(4,2);

SELECT 'Schema created successfully!' AS status;