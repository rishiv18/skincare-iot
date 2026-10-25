
import requests
import sqlite3
import time
from datetime import datetime, timezone

# COORDINATE OF TEST LOCATION (HARROW, LDN)
LATITUDE = 51.5806
LONGITUDE = -0.3417

DB_FILE = "skincare_data.db"
INTERVAL_SECONDS = 900  # 15 minutes

API_URL = "https://api.open-meteo.com/v1/forecast"

def initialise_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS weather_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc TEXT NOT NULL,
                weather_time_utc TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                temperature_c REAL NOT NULL,
                humidity_percent REAL NOT NULL
            )
        """)

def collect_weather():
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,relative_humidity_2m",
        "timezone": "GMT"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=15
    )
    response.raise_for_status()

    data = response.json()
    current = data["current"]

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    weather_time = current["time"] + "+00:00"
    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]

    if temperature is None or humidity is None:
        raise ValueError("Missing weather measurements")

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO weather_readings (
                timestamp_utc,
                weather_time_utc,
                latitude,
                longitude,
                temperature_c,
                humidity_percent
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            weather_time,
            LATITUDE,
            LONGITUDE,
            temperature,
            humidity
        ))

    print(
        f"{timestamp} | "
        f"Outdoor: {temperature} C, {humidity}% RH"
    )

if __name__ == "__main__":
    if LATITUDE is None or LONGITUDE is None:
        raise ValueError(
            "Set LATITUDE and LONGITUDE before running"
        )

    initialise_database()

    print("Starting Open-Meteo logger...")

    while True:
        try:
            collect_weather()
        except Exception as error:
            print("Weather collection error:", repr(error))

        time.sleep(INTERVAL_SECONDS)
