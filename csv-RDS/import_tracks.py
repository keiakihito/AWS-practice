import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

# === Load environment variables from .env ===
load_dotenv()

CSV_FILE = "tracks_test.csv"
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432))
}

def is_valid_time_format(s):
    parts = s.strip().split(":")
    return len(parts) == 2 or len(parts) == 3

def validate_row(row):
    errors = []
    if pd.isna(row["album_id"]):
        errors.append("Missing album_id")
    if pd.isna(row["track_no"]):
        errors.append("Missing track_no")
    if pd.isna(row["title"]):
        errors.append("Missing title")
    if row["duration"]:
        if not is_valid_time_format(row["duration"]):
            errors.append("Invalid duration format (expected MM:SS or HH:MM:SS)")
    if not isinstance(row["tags"], str) or not row["tags"].startswith("{"):
        errors.append("tags should be in {Tag1,Tag2} format")
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

# Remove 'id' and 'created_at' columns if they exist (they are auto-generated)
cols = [col for col in df.columns if col not in ["id", "created_at"]]
values = [tuple(row[col] for col in cols) for _, row in df.iterrows()]

insert_query = f"""
INSERT INTO tracks ({', '.join(cols)})
VALUES %s;
"""

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
execute_values(cur, insert_query, values)
conn.commit()
cur.close()
conn.close()

print("✅ Insert complete.")
