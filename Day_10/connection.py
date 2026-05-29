"""
psycopg2 Basics - PostgreSQL Connection & Operations
=====================================================
Install: pip install psycopg2-binary
"""

import psycopg2
from psycopg2 import sql, OperationalError
from psycopg2.extras import RealDictCursor
import os

# ── 1. CONNECTION CONFIG ──────────────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "mydb",       # change to your DB name
    "user": "postgres",       # change to your username
    "password": "Yashas@123",  # change to your password
}

# ── 2. CONNECT TO POSTGRESQL ─────────────────────────────────────────────────
def get_connection():
    """Create and return a PostgreSQL connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to PostgreSQL successfully!")
        return conn
    except OperationalError as e:
        print(f"❌ Connection failed: {e}")
        raise


# ── 3. EXECUTE QUERIES ───────────────────────────────────────────────────────
def create_table(conn):
    """Create a sample 'employees' table."""
    query = """
        CREATE TABLE IF NOT EXISTS employees (
            id      SERIAL PRIMARY KEY,
            name    VARCHAR(100) NOT NULL,
            dept    VARCHAR(50),
            salary  NUMERIC(10, 2),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
        print("✅ Table 'employees' created (or already exists).")


# ── 4. FETCH RESULTS ─────────────────────────────────────────────────────────
def fetch_all_employees(conn):
    """Fetch all rows as a list of dicts (using RealDictCursor)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM employees ORDER BY id;")
        rows = cur.fetchall()
        print(f"📋 Fetched {len(rows)} employees:")
        for row in rows:
            print(dict(row))
        return rows


def fetch_one(conn, emp_id):
    """Fetch a single row."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM employees WHERE id = %s;", (emp_id,))
        row = cur.fetchone()
        print(f"👤 Employee #{emp_id}: {dict(row) if row else 'Not found'}")
        return row


# ── 5. PARAMETERIZED QUERIES (prevents SQL injection) ────────────────────────
def insert_employee(conn, name, dept, salary):
    """Insert using %s placeholders — ALWAYS use this, never f-strings."""
    query = """
        INSERT INTO employees (name, dept, salary)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    with conn.cursor() as cur:
        cur.execute(query, (name, dept, salary))
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"✅ Inserted employee '{name}' with id={new_id}")
        return new_id


def bulk_insert(conn, employees: list[tuple]):
    """Insert multiple rows efficiently with executemany."""
    query = "INSERT INTO employees (name, dept, salary) VALUES (%s, %s, %s);"
    with conn.cursor() as cur:
        cur.executemany(query, employees)
        conn.commit()
        print(f"✅ Bulk inserted {len(employees)} employees.")


def search_by_dept(conn, dept):
    """Parameterized SELECT — safe from injection."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM employees WHERE dept = %s ORDER BY salary DESC;",
            (dept,)
        )
        rows = cur.fetchall()
        print(f"🔍 Found {len(rows)} employees in '{dept}':")
        for r in rows:
            print(dict(r))
        return rows


# ── 6. TRANSACTION MANAGEMENT ────────────────────────────────────────────────
def transfer_salary(conn, from_id, to_id, amount):
    """
    Demonstrate transaction: deduct from one employee, add to another.
    Rolls back if anything fails.
    """
    try:
        with conn.cursor() as cur:
            # Step 1 — deduct
            cur.execute(
                "UPDATE employees SET salary = salary - %s WHERE id = %s;",
                (amount, from_id)
            )
            # Step 2 — add
            cur.execute(
                "UPDATE employees SET salary = salary + %s WHERE id = %s;",
                (amount, to_id)
            )
            conn.commit()
            print(f"✅ Transferred ${amount} from emp#{from_id} → emp#{to_id}")
    except Exception as e:
        conn.rollback()  # ← undo everything on failure
        print(f"❌ Transaction rolled back: {e}")
        raise


# ── MAIN DEMO ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    conn = get_connection()

    create_table(conn)

    # Insert sample data
    bulk_insert(conn, [
        ("Alice Johnson", "Engineering", 95000),
        ("Bob Smith",     "Marketing",   72000),
        ("Carol White",   "Engineering", 88000),
        ("David Lee",     "HR",          65000),
    ])

    fetch_all_employees(conn)
    fetch_one(conn, 1)
    search_by_dept(conn, "Engineering")
    transfer_salary(conn, 1, 2, 5000)

    conn.close()
    print("🔒 Connection closed.")
