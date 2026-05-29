# Python Database Integration — Day's Task

## Project Structure
```
python_db_project/
├── requirements.txt
├── psycopg2_basics/
│   └── connection.py          # Raw psycopg2: connect, query, transactions
├── pandas_sql/
│   └── pandas_sql.py          # read_sql_query, read_sql_table, to_sql, chunks
├── sqlalchemy_basics/
│   └── orm_demo.py            # Engine, models, CRUD, ORM queries
├── data_pipelines/
│   └── etl_pipeline.py        # Extract API → Transform pandas → Load DB
└── practice/
    └── practice_scripts.py    # CSV→PG, analysis, multi-DB queries
```

---

## How to Run in VS Code

### Step 1 — Prerequisites
- Install [VS Code](https://code.visualstudio.com/)
- Install the **Python extension** (`Ctrl+Shift+X` → search "Python" → Install)
- Install **PostgreSQL** locally or use a cloud DB (e.g. Supabase free tier)

### Step 2 — Open the project
```
File → Open Folder → select python_db_project/
```

### Step 3 — Create a virtual environment
Open the integrated terminal (`Ctrl+` ` `):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Update DB credentials
In **every** script, find this line and update it:
```python
# psycopg2 scripts
DB_CONFIG = {
    "host": "localhost",
    "database": "mydb",      # ← your DB name
    "user": "postgres",      # ← your username
    "password": "your_pass", # ← your password
}

# SQLAlchemy / pandas scripts
DB_URL = "postgresql+psycopg2://postgres:your_pass@localhost:5432/mydb"
#                               ^^^^^^^^  ^^^^^^^^^              ^^^^
#                               user      password               db name
```

### Step 6 — Create the database (one-time)
In your PostgreSQL client (psql, pgAdmin, or TablePlus):
```sql
CREATE DATABASE mydb;
```

### Step 7 — Run a script
**Option A — Run file directly:**
- Open any `.py` file
- Press `F5` or click the ▶ button top-right

**Option B — Run in terminal:**
```bash
python psycopg2_basics/connection.py
python pandas_sql/pandas_sql.py
python sqlalchemy_basics/orm_demo.py
python data_pipelines/etl_pipeline.py
python practice/practice_scripts.py
```

**Option C — Run selection:**
- Select any block of code
- Press `Shift+Enter` to run it in the terminal

### Tip — Select Python interpreter
`Ctrl+Shift+P` → "Python: Select Interpreter" → choose `venv`

---

## Integration Patterns

### Pattern 1 — Direct psycopg2 (low-level, fast)
```python
import psycopg2
conn = psycopg2.connect(host="localhost", database="mydb", user="postgres", password="pass")
with conn.cursor() as cur:
    cur.execute("SELECT * FROM employees WHERE dept = %s;", ("Engineering",))
    rows = cur.fetchall()
conn.close()
```
**Use when:** Maximum control, stored procedures, COPY commands, bulk COPY.

---

### Pattern 2 — SQLAlchemy Core (SQL + safety)
```python
from sqlalchemy import create_engine, text
engine = create_engine("postgresql+psycopg2://user:pass@localhost/mydb")
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM employees WHERE dept = :dept"), {"dept": "Engineering"})
    rows = result.fetchall()
```
**Use when:** Raw SQL but want connection pooling and cross-DB compatibility.

---

### Pattern 3 — SQLAlchemy ORM (Pythonic, no SQL needed)
```python
from sqlalchemy.orm import Session
with Session(engine) as session:
    engineers = session.query(Employee).filter_by(dept="Engineering").all()
```
**Use when:** Complex object relationships, web apps (FastAPI, Flask, Django).

---

### Pattern 4 — Pandas + SQL (analytics)
```python
import pandas as pd
df = pd.read_sql_query("SELECT dept, AVG(salary) FROM employees GROUP BY dept;", engine)
df.to_sql("salary_summary", engine, if_exists="replace", index=False)
```
**Use when:** Data analysis, reporting, ETL pipelines, Jupyter notebooks.

---

### Pattern 5 — ETL Pipeline
```
[API / CSV / File]
        ↓  Extract
[requests / pd.read_csv]
        ↓  Transform
[pandas: clean, enrich, validate]
        ↓  Load
[df.to_sql() → PostgreSQL]
```
**Use when:** Scheduled data loads, data warehousing, syncing external sources.

---

### Pattern 6 — Incremental Load
```python
# Only load new rows (avoids full reload)
last_id = conn.execute("SELECT MAX(id) FROM table").scalar() or 0
new_data = full_df[full_df["id"] > last_id]
new_data.to_sql("table", engine, if_exists="append", index=False)
```
**Use when:** Large tables, scheduled jobs, CDC (change data capture).

---

### Pattern 7 — Multi-Database Join
```python
pg_df     = pd.read_sql_query("SELECT ...", pg_engine)
sqlite_df = pd.read_sql_query("SELECT ...", sqlite_engine)
merged    = pd.merge(pg_df, sqlite_df, on="common_key")  # join in memory
```
**Use when:** Combining data across systems (e.g., production DB + local reference).

---

## Common Connection Strings
```python
# PostgreSQL
"postgresql+psycopg2://user:password@host:5432/dbname"

# SQLite (local file — no server needed, great for testing)
"sqlite:///myfile.db"
"sqlite:///:memory:"   # in-memory, wiped on exit

# MySQL
"mysql+pymysql://user:password@host:3306/dbname"

# SQL Server
"mssql+pyodbc://user:password@host/dbname?driver=ODBC+Driver+17+for+SQL+Server"
```

---

## Quick Troubleshooting

| Error | Fix |
|-------|-----|
| `OperationalError: could not connect` | Check host/port/credentials, ensure PostgreSQL is running |
| `relation does not exist` | Run `create_table()` or `Base.metadata.create_all(engine)` first |
| `permission denied` | Grant privileges: `GRANT ALL ON DATABASE mydb TO postgres;` |
| `ModuleNotFoundError: psycopg2` | Run `pip install psycopg2-binary` inside your venv |
| SSL errors on cloud DB | Add `?sslmode=require` to your connection string |
