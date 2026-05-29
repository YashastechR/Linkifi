"""
ETL Data Pipeline
=================
Extract from public API → Transform with pandas → Load to PostgreSQL
API used: https://jsonplaceholder.typicode.com (free, no key needed)

Install: pip install requests pandas sqlalchemy psycopg2-binary
"""

import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import logging
import time

# ── SETUP ─────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

DB_URL  = "postgresql+psycopg2://postgres:Yashas%40123@localhost:5433/mydb"
API_URL = "https://jsonplaceholder.typicode.com"

engine = create_engine(DB_URL)


# ── EXTRACT ───────────────────────────────────────────────────────────────────
def extract_users() -> list[dict]:
    """Pull users from API."""
    log.info("🔄 Extracting users from API...")
    resp = requests.get(f"{API_URL}/users", timeout=10)
    resp.raise_for_status()
    data = resp.json()
    log.info(f"  ✅ Extracted {len(data)} users")
    return data


def extract_posts() -> list[dict]:
    """Pull posts from API."""
    log.info("🔄 Extracting posts from API...")
    resp = requests.get(f"{API_URL}/posts", timeout=10)
    resp.raise_for_status()
    data = resp.json()
    log.info(f"  ✅ Extracted {len(data)} posts")
    return data


# ── TRANSFORM ─────────────────────────────────────────────────────────────────
def transform_users(raw: list[dict]) -> pd.DataFrame:
    """Flatten nested JSON and clean user data."""
    log.info("🔧 Transforming users...")

    df = pd.json_normalize(raw)  # flattens nested dicts

    # Select and rename useful columns
    df = df[[
        "id", "name", "username", "email",
        "address.city", "address.zipcode",
        "company.name", "phone", "website"
    ]].rename(columns={
        "address.city":    "city",
        "address.zipcode": "zipcode",
        "company.name":    "company"
    })

    # Clean up
    df["email"]   = df["email"].str.lower().str.strip()
    df["website"] = df["website"].str.replace(r"^(?!https?://)", "https://", regex=True)

    # Add pipeline metadata
    df["loaded_at"] = datetime.utcnow()

    log.info(f"  ✅ Transformed {len(df)} users | columns: {list(df.columns)}")
    return df


def transform_posts(raw: list[dict]) -> pd.DataFrame:
    """Transform posts — word count, truncated title, etc."""
    log.info("🔧 Transforming posts...")

    df = pd.DataFrame(raw)

    # Add derived columns
    df["word_count"]      = df["body"].str.split().str.len()
    df["title_short"]     = df["title"].str[:50]
    df["has_long_body"]   = df["word_count"] > 30
    df["loaded_at"]       = datetime.utcnow()

    # Rename for clarity
    df = df.rename(columns={"userId": "user_id"})

    log.info(f"  ✅ Transformed {len(df)} posts")
    return df


# ── LOAD ──────────────────────────────────────────────────────────────────────
def load_to_db(df: pd.DataFrame, table: str, if_exists: str = "replace"):
    """Write DataFrame to PostgreSQL."""
    log.info(f"💾 Loading {len(df)} rows → table '{table}' (if_exists='{if_exists}')...")

    df.to_sql(
        name=table,
        con=engine,
        if_exists=if_exists,
        index=False,
        chunksize=500,   # write in chunks for large DataFrames
        method="multi"   # faster bulk insert
    )
    log.info(f"  ✅ Loaded successfully.")


# ── INCREMENTAL LOAD ──────────────────────────────────────────────────────────
def get_last_loaded_id(table: str, id_col: str = "id") -> int:
    """Return the max ID already in the table (0 if table is empty/missing)."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COALESCE(MAX({id_col}), 0) FROM {table};"))
            max_id = result.scalar()
            log.info(f"  Last loaded {id_col} in '{table}': {max_id}")
            return max_id
    except Exception:
        return 0   # table doesn't exist yet


def incremental_load_posts():
    """Only load posts with id > last loaded id."""
    log.info("🔄 Incremental load — posts...")

    last_id = get_last_loaded_id("api_posts")
    raw     = extract_posts()
    df      = transform_posts(raw)

    new_rows = df[df["id"] > last_id]
    if new_rows.empty:
        log.info("  ℹ️  No new posts to load.")
    else:
        load_to_db(new_rows, "api_posts", if_exists="append")
        log.info(f"  ✅ Incremental: loaded {len(new_rows)} new posts.")


# ── ERROR HANDLING ────────────────────────────────────────────────────────────
def safe_extract(url: str, retries: int = 3) -> list[dict]:
    """Extract with retry logic and error handling."""
    for attempt in range(1, retries + 1):
        try:
            log.info(f"  Attempt {attempt}/{retries}: GET {url}")
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            log.warning(f"  ⏱ Timeout on attempt {attempt}")
        except requests.exceptions.HTTPError as e:
            log.error(f"  ❌ HTTP error: {e}")
            break
        except requests.exceptions.ConnectionError:
            log.warning(f"  🔌 Connection error on attempt {attempt}")

        if attempt < retries:
            time.sleep(2 ** attempt)   # exponential backoff: 2s, 4s, 8s

    raise RuntimeError(f"Failed to extract from {url} after {retries} attempts")


# ── FULL PIPELINE ─────────────────────────────────────────────────────────────
def run_full_pipeline():
    """Run the complete ETL pipeline."""
    start = datetime.utcnow()
    log.info("=" * 50)
    log.info("🚀 Starting ETL Pipeline")
    log.info("=" * 50)

    try:
        # Users pipeline
        raw_users = extract_users()
        users_df  = transform_users(raw_users)
        load_to_db(users_df, "api_users", if_exists="replace")

        # Posts pipeline (full)
        raw_posts = extract_posts()
        posts_df  = transform_posts(raw_posts)
        load_to_db(posts_df, "api_posts", if_exists="replace")

        # Quick validation
        with engine.connect() as conn:
            u_count = conn.execute(text("SELECT COUNT(*) FROM api_users;")).scalar()
            p_count = conn.execute(text("SELECT COUNT(*) FROM api_posts;")).scalar()
            log.info(f"✅ Validation — users: {u_count}, posts: {p_count}")

        elapsed = (datetime.utcnow() - start).total_seconds()
        log.info(f"🏁 Pipeline complete in {elapsed:.2f}s")

    except Exception as e:
        log.error(f"💥 Pipeline failed: {e}")
        raise


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_full_pipeline()

    # Demo incremental load (simulates a second run)
    log.info("\n── Simulating incremental run ────────────────")
    incremental_load_posts()
