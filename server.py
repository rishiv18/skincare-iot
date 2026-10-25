
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import sqlite3
import os

app = FastAPI()

DB = "skincare_data.db"
API_KEY = os.environ.get("SKINCARE_API_KEY")

class Reading(BaseModel):
    device_id: str
    temperature: float = Field(ge=-45, le=130)
    humidity: float = Field(ge=0, le=100)

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                device_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL
            )
        """)

init_db()

@app.get("/")
def home():
    return {"status": "Skincare IoT server running"}

@app.post("/readings")
def add_reading(reading: Reading, key: str = ""):
    if not API_KEY or key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    timestamp = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB) as conn:
        conn.execute(
            """INSERT INTO readings
               (timestamp, device_id, temperature, humidity)
               VALUES (?, ?, ?, ?)""",
            (
                timestamp,
                reading.device_id,
                reading.temperature,
                reading.humidity
            )
        )

    print(
        f"{timestamp} | {reading.device_id} | "
        f"{reading.temperature} C | {reading.humidity}%"
    )

    return {"saved": True, "timestamp": timestamp}
