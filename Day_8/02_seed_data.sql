-- ============================================================
-- SEED DATA — E-COMMERCE DATABASE
-- DML: INSERT operations (single and bulk)
-- ============================================================

-- ── SUPPLIERS ───────────────────────────────────────────────
INSERT INTO suppliers (name, contact_email, contact_phone, country, rating) VALUES
  ('TechWorld Imports',  'contact@techworld.in',  '+91-9810001111', 'India',  4.8),
  ('FashionHub Ltd',     'info@fashionhub.in',    '+91-9820002222', 'India',  4.5),
  ('GadgetZone Corp',    'sales@gadgetzone.in',   '+91-9830003333', 'India',  4.2),
  ('HomeEssentials Co',  'hello@homeessentials.in','+91-9840004444','India',  4.6),
  ('SportsGear Pro',     'orders@sportsgear.in',  '+91-9850005555', 'India',  4.3),
  ('GlobalSource Inc',   'global@source.com',     '+1-4151001001',  'USA',    4.7),
  ('EcoProducts Ltd',    'eco@products.uk',       '+44-2071001001', 'UK',     4.9);

-- ── CATEGORIES ──────────────────────────────────────────────
INSERT INTO categories (name, slug, description) VALUES
  ('Electronics',     'electronics',     'Gadgets, devices, and tech accessories'),
  ('Clothing',        'clothing',        'Apparel, footwear and fashion'),
  ('Home & Kitchen',  'home-kitchen',    'Furniture, cookware, and home décor'),
  ('Sports',          'sports',          'Sporting goods and fitness equipment'),
  ('Books',           'books',           'Fiction, non-fiction, and educational titles'),
  ('Beauty',          'beauty',          'Skincare, makeup, and personal care');

-- Sub-categories
INSERT INTO categories (name, slug, parent_id, description) VALUES
  ('Smartphones',  'smartphones',  1, 'Android and iOS devices'),
  ('Laptops',      'laptops',      1, 'Work and gaming laptops'),
  ('Headphones',   'headphones',   1, 'Wired and wireless audio'),
  ('Men''s Wear',  'mens-wear',    2, 'Shirts, trousers, and accessories'),
  ('Women''s Wear','womens-wear',  2, 'Dresses, tops, and accessories');

-- ── CUSTOMERS ───────────────────────────────────────────────
INSERT INTO customers (first_name, last_name, email, phone, date_of_birth, loyalty_tier) VALUES
  ('Aarav',    'Sharma',    'aarav.sharma@gmail.com',     '+91-9000000001', '1990-03-15', 'gold'),
  ('Priya',    'Patel',     'priya.patel@yahoo.com',      '+91-9000000002', '1993-07-22', 'silver'),
  ('Rohan',    'Mehta',     'rohan.mehta@hotmail.com',    '+91-9000000003', '1988-11-05', 'platinum'),
  ('Sneha',    'Reddy',     'sneha.reddy@gmail.com',      '+91-9000000004', '1995-01-30', 'bronze'),
  ('Vikram',   'Nair',      'vikram.nair@outlook.com',    '+91-9000000005', '1985-09-18', 'gold'),
  ('Anjali',   'Singh',     'anjali.singh@gmail.com',     '+91-9000000006', '1998-04-12', 'silver'),
  ('Karthik',  'Rao',       'karthik.rao@gmail.com',      '+91-9000000007', '1992-06-25', 'bronze'),
  ('Divya',    'Kumar',     'divya.kumar@yahoo.com',      '+91-9000000008', '1991-12-03', 'gold'),
  ('Arjun',    'Gupta',     'arjun.gupta@gmail.com',      '+91-9000000009', '1987-08-17', 'platinum'),
  ('Kavya',    'Joshi',     'kavya.joshi@gmail.com',      '+91-9000000010', '1996-02-28', 'silver'),
  ('Rahul',    'Verma',     'rahul.verma@gmail.com',      '+91-9000000011', '1994-05-10', 'bronze'),
  ('Meera',    'Pillai',    'meera.pillai@outlook.com',   '+91-9000000012', '1989-10-22', 'gold'),
  ('Suresh',   'Iyer',      'suresh.iyer@gmail.com',      '+91-9000000013', '1983-03-07', 'platinum'),
  ('Lakshmi',  'Bhat',      'lakshmi.bhat@gmail.com',     '+91-9000000014', '1997-07-14', 'bronze'),
  ('Aditya',   'Chopra',    'aditya.chopra@yahoo.com',    '+91-9000000015', '1990-11-29', 'silver');

-- ── ADDRESSES ───────────────────────────────────────────────
INSERT INTO addresses (customer_id, address_type, street_line1, city, state, postal_code, country, is_default) VALUES
  (1,  'shipping', '12 MG Road',         'Bengaluru', 'Karnataka',   '560001', 'India', TRUE),
  (1,  'billing',  '12 MG Road',         'Bengaluru', 'Karnataka',   '560001', 'India', FALSE),
  (2,  'shipping', '45 Linking Road',    'Mumbai',    'Maharashtra', '400050', 'India', TRUE),
  (3,  'shipping', '7 Connaught Place',  'New Delhi', 'Delhi',       '110001', 'India', TRUE),
  (4,  'shipping', '88 Park Street',     'Kolkata',   'West Bengal', '700016', 'India', TRUE),
  (5,  'shipping', '23 Anna Salai',      'Chennai',   'Tamil Nadu',  '600002', 'India', TRUE),
  (6,  'shipping', '15 Banjara Hills',   'Hyderabad', 'Telangana',   '500034', 'India', TRUE),
  (7,  'shipping', '9 FC Road',          'Pune',      'Maharashtra', '411004', 'India', TRUE),
  (8,  'shipping', '67 Navrangpura',     'Ahmedabad', 'Gujarat',     '380009', 'India', TRUE),
  (9,  'shipping', '3 Sector 17',        'Chandigarh','Chandigarh',  '160017', 'India', TRUE),
  (10, 'shipping', '54 Hazratganj',      'Lucknow',   'Uttar Pradesh','226001','India', TRUE);

-- ── PRODUCTS ────────────────────────────────────────────────
INSERT INTO products (category_id, supplier_id, name, slug, description, price, cost_price, stock_qty, sku, weight_kg) VALUES
  -- Smartphones (cat 7)
  (7, 1, 'Samsung Galaxy S24',     'samsung-galaxy-s24',   'Flagship Android phone with 50MP camera',     74999, 62000, 45, 'SAM-S24-001',  0.167),
  (7, 1, 'OnePlus 12',             'oneplus-12',           '5G smartphone with Snapdragon 8 Gen 3',       64999, 53000, 60, 'OP12-001',     0.220),
  (7, 3, 'Redmi Note 13 Pro',      'redmi-note-13-pro',    'Mid-range with 200MP camera',                 27999, 22000, 120,'RN13P-001',    0.187),
  (7, 1, 'iPhone 15',              'iphone-15',            'Apple A16 Bionic, titanium design',           79999, 68000, 30, 'APP-IP15-001', 0.171),
  -- Laptops (cat 8)
  (8, 6, 'Dell XPS 15',            'dell-xps-15',          'Core i7, 16GB RAM, 512GB SSD',               129999,108000, 20, 'DELL-XPS15',  1.860),
  (8, 2, 'MacBook Air M3',         'macbook-air-m3',       'Apple M3 chip, 8GB unified memory',          114999, 95000, 15, 'APP-MBA-M3',  1.240),
  (8, 3, 'HP Pavilion 15',         'hp-pavilion-15',       'AMD Ryzen 5, 8GB RAM, 512GB SSD',            54999, 46000, 35, 'HP-PAV15',    1.750),
  -- Headphones (cat 9)
  (9, 1, 'Sony WH-1000XM5',        'sony-wh1000xm5',       'Industry-leading noise cancellation',        29999, 23000, 50, 'SONY-XM5',    0.250),
  (9, 3, 'boAt Rockerz 450',       'boat-rockerz-450',     'Wireless with 15h battery, bass-heavy',       1999,  1400,200, 'BOAT-R450',   0.220),
  (9, 1, 'Sennheiser HD 560S',     'sennheiser-hd-560s',   'Audiophile open-back headphones',             9999,  8100, 30, 'SENN-HD560S', 0.240),
  -- Clothing (cat 10 & 11)
  (10,2, 'Allen Solly Slim Shirt', 'allen-solly-slim-shirt','Formal slim fit, 100% cotton',               1999,  1200, 80, 'AS-SLIM-S-M', 0.200),
  (11,2, 'Zara Floral Dress',      'zara-floral-dress',    'Summer floral print, midi length',            3499,  2200, 60, 'ZAR-FLRL-S',  0.350),
  -- Home & Kitchen (cat 3)
  (3, 4, 'Prestige Induction Cooktop','prestige-induction','2000W with push button control',              2999,  2100,100, 'PRE-INDUC-01',3.500),
  (3, 4, 'Milton Thermosteel Flask','milton-thermosteel',  '1L, keeps hot/cold for 24h',                   799,   550,150, 'MIL-THERM-1L',0.400),
  -- Sports (cat 4)
  (4, 5, 'Cosco Football',         'cosco-football',       'FIFA approved, size 5',                       1299,   900,200, 'COS-FB-S5',   0.420),
  (4, 5, 'Nivia Yoga Mat',         'nivia-yoga-mat',       '6mm thick, anti-slip, carry strap',            999,   650,175, 'NIV-YM-6MM',  0.700),
  -- Books (cat 5)
  (5, 7, 'Atomic Habits',          'atomic-habits',        'James Clear — proven framework for habits',    599,   250, 300,'ATH-CLEAR',   0.300),
  (5, 7, 'The Pragmatic Programmer','pragmatic-programmer','Hunt & Thomas — timeless dev wisdom',          899,   380, 150,'PRAGPROG-20', 0.460),
  -- Beauty (cat 6)
  (6, 4, 'Minimalist Vitamin C Serum','minimalist-vit-c', '10% Vitamin C + Hyaluronic Acid, 30ml',        599,   320,250, 'MIN-VITC-30',  0.050),
  (6, 4, 'Mamaearth Onion Shampoo','mamaearth-onion-shampoo','Reduces hairfall, 250ml',                   349,   200,300, 'MAM-ONI-250', 0.260);

-- ── ORDERS ──────────────────────────────────────────────────
INSERT INTO orders (customer_id, address_id, status, subtotal, discount, tax, shipping_fee, total, ordered_at) VALUES
  (1,  1,  'delivered',  74999, 5000, 12599, 0,    82598, '2024-11-10 10:23:00'),
  (2,  3,  'delivered',  29999, 0,    5399,  99,   35497, '2024-11-15 14:05:00'),
  (3,  4,  'shipped',    179998,10000,30599, 0,    200597,'2024-12-01 09:00:00'),
  (4,  5,  'delivered',   2798, 0,     503,  49,    3350, '2024-12-05 17:30:00'),
  (5,  6,  'cancelled',  64999, 0,    0,     0,     0,    '2024-12-10 11:45:00'),
  (6,  7,  'delivered',   3498, 200,  593,   49,    3940, '2024-12-12 08:20:00'),
  (1,  1,  'delivered',   9999, 0,    1799,  0,    11798, '2024-12-18 20:15:00'),
  (8,  9,  'processing',114999, 5000,19799,  0,   129798, '2025-01-03 13:10:00'),
  (9,  10, 'delivered',   1798, 0,     323,  49,    2170, '2025-01-08 16:40:00'),
  (10, 11, 'delivered',  74999, 0,    13499,  0,   88498, '2025-01-12 11:00:00'),
  (3,  4,  'delivered',   1598, 0,     287,  49,    1934, '2025-01-20 09:30:00'),
  (12, 1,  'confirmed',  27999, 2000, 4679,  0,    30678, '2025-02-01 14:22:00'),
  (13, 1,  'delivered', 129999, 10000,21599, 0,   141598, '2025-02-10 10:05:00'),
  (2,  3,  'delivered',    948, 0,     170,  49,    1167, '2025-02-14 19:00:00'),
  (5,  6,  'shipped',    54999, 3000, 9359,  0,    61358, '2025-03-01 08:45:00');

-- ── ORDER ITEMS ─────────────────────────────────────────────
INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount) VALUES
  (1,  1,  1, 74999, 5000),   -- Galaxy S24
  (2,  8,  1, 29999,    0),   -- Sony XM5
  (3,  6,  1,114999, 5000),   -- MacBook Air M3
  (3,  5,  1, 65000, 5000),   -- Dell XPS (negotiated)
  (4,  15, 1,  1299,    0),   -- Cosco Football
  (4,  16, 1,   999,    0),   -- Yoga Mat
  (5,  2,  1, 64999,    0),   -- OnePlus (cancelled)
  (6,  11, 1,  1999,  200),   -- Shirt
  (6,  12, 1,  1499,    0),
  (7,  10, 1,  9999,    0),   -- Sennheiser
  (8,  6,  1,114999, 5000),   -- MacBook
  (9,  17, 2,   599,    0),   -- Atomic Habits ×2
  (10, 4,  1, 79999,    0),   -- iPhone 15
  (11, 17, 1,   599,    0),
  (11, 18, 1,   899,    0),
  (12, 3,  1, 27999, 2000),   -- Redmi Note
  (13, 5,  1,129999,10000),   -- Dell XPS
  (14, 19, 2,   599,    0),   -- Minimalist serum ×2
  (14, 20, 1,   349,    0),   -- Shampoo
  (15, 7,  1, 54999, 3000);   -- HP Pavilion

-- ── PRODUCT REVIEWS ─────────────────────────────────────────
INSERT INTO product_reviews (product_id, customer_id, rating, title, body, is_verified) VALUES
  (1,  1,  5, 'Excellent phone!',        'Amazing camera and battery life.',           TRUE),
  (8,  2,  5, 'Best headphones ever',    'Noise cancellation is phenomenal.',          TRUE),
  (6,  3,  4, 'Great laptop',            'Fast, slim, and the display is gorgeous.',   TRUE),
  (15, 4,  4, 'Good quality ball',       'Decent for casual play.',                    TRUE),
  (11, 6,  3, 'Average fit',             'Material is nice but sizing runs large.',    TRUE),
  (10, 9,  5, 'Audiophile quality',      'Clear and detailed sound, worth every rupee.',TRUE),
  (4,  10, 5, 'iPhone is life',          'Smooth, fast, and the camera is insane.',    TRUE),
  (17, 3,  5, 'Life-changing book',      'Changed how I approach habits.',             TRUE),
  (17, 11, 4, 'Good read',               'Practical advice, easy to apply.',           FALSE),
  (6,  13, 5, 'M3 is blazing fast',      'Best laptop I have ever owned.',             TRUE),
  (3,  12, 4, 'Great mid-range phone',   'Camera is impressive for the price.',        TRUE),
  (19, 2,  5, 'Skin glowing!',           'Visible results in 2 weeks.',                TRUE),
  (9,  9,  2, 'Expected better',         'Bass is too heavy, lacks clarity.',          TRUE),
  (13, 4,  5, 'Cooks perfectly',         'Heats evenly, controls are easy.',           FALSE),
  (7,  5,  4, 'Solid budget laptop',     'Good performance for the price.',            TRUE);

SELECT 'Seed data inserted successfully!' AS status;