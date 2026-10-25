
import sqlite3

with sqlite3.connect("skincare_data.db") as conn:
    sensor_count = conn.execute(
        "SELECT COUNT(*) FROM readings"
    ).fetchone()[0]

    weather_count = conn.execute(
        "SELECT COUNT(*) FROM weather_readings"
    ).fetchone()[0]

    latest_weather = conn.execute("""
        SELECT timestamp_utc, temperature_c, humidity_percent
        FROM weather_readings
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

print("Sensor readings:", sensor_count)
print("Weather readings:", weather_count)
print("Latest weather:", latest_weather)
