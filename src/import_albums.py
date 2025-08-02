import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import timedelta
from dotenv import load_dotenv
import os

# === Load environment variables from .env ===
load_dotenv()

CSV_FILE = "albums_test.csv"
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432))
}

def validate_row(row):
    errors = []
    if not row["title"]:
        errors.append("Missing title")
    if not row["release_date"]:
        errors.append("Missing release_date")
    try:
        pd.to_datetime(row["release_date"])
    except Exception:
        errors.append("Invalid date format")
    if not isinstance(row["genre"], str) or not row["genre"].startswith("{"):
        errors.append("genre should be in {Concerto,Symphony} format")
    if row["total_duration"]:
        try:
            pd.to_timedelta("00:" + row["total_duration"]) if len(row["total_duration"].split(":")) == 2 else pd.to_timedelta(row["total_duration"])
        except Exception:
            errors.append("Invalid total_duration format")
    return errors

df = pd.read_csv(CSV_FILE)
error_rows = []

for idx, row in df.iterrows():
    errs = validate_row(row)
    if errs:
        error_rows.append((idx+2, errs))

if error_rows:
    print("❌ Validation errors found:")
    for row_num, errors in error_rows:
        print(f"  Row {row_num}: {errors}")
    exit(1)
else:
    print("✅ Validation passed. Inserting into DB...")

cols = df.columns.tolist()
values = [tuple(row) for row in df.to_numpy()]

insert_query = f"""
INSERT INTO albums ({', '.join(cols)})
VALUES %s;
"""

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
execute_values(cur, insert_query, values)
conn.commit()
cur.close()
conn.close()

print("✅ Insert complete.")
