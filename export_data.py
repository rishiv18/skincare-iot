
import sqlite3
import csv
from datetime import datetime

DB_FILE = "skincare_data.db"
CSV_FILE = "skincare_dataset.csv"

with sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            device_id,
            temperature,
            humidity
        FROM readings
        ORDER BY timestamp ASC
    """)

    rows = cursor.fetchall()

with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "id",
        "timestamp_utc",
        "device_id",
        "temperature_c",
        "relative_humidity_percent"
    ])

    writer.writerows(rows)

print(f"Exported {len(rows)} readings to {CSV_FILE}")
