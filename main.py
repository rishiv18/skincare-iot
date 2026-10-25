
import sqlite3

# Connect to the database
conn = sqlite3.connect("skincare_data.db")
cursor = conn.cursor()

# Retrieve the 10 most recent readings
cursor.execute("""
    SELECT timestamp, temperature, humidity
    FROM readings
    ORDER BY id DESC
    LIMIT 10
""")

rows = cursor.fetchall()

print("Latest sensor readings:")
print("-" * 55)

for timestamp, temperature, humidity in rows:
    print(
        f"{timestamp} | "
        f"{temperature} °C | "
        f"{humidity} %"
    )

print("-" * 55)
print(f"Total readings displayed: {len(rows)}")

conn.close()

