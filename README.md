# Skincare IoT

Environmental monitoring for skincare: an ESP32-S3 with an SHT31-D sensor
records indoor temperature and humidity, alongside outdoor weather from the
Open-Meteo API, so the two can be compared.

## Components

| File | Purpose |
|------|---------|
| `server.py` | FastAPI server that receives ESP32 readings (API-key protected) and stores them in SQLite |
| `weather_logger.py` | Logs outdoor weather from Open-Meteo every 15 minutes |
| `dashboard.py` | Streamlit + Plotly dashboard of indoor vs outdoor conditions |
| `export_data.py` | Exports readings to `skincare_dataset.csv` |
| `check_data.py`, `check_weather.py` | Quick inspection of the latest stored readings |
| `wifitest.py` | MicroPython Wi-Fi connectivity test for the ESP32 |

## Progress log

Updated automatically each day from the database and git history.

<!-- PROGRESS:START -->
### 2026-10-26
- **Indoor sensor (ESP32):** 17 new readings (17 total), avg 28.6 °C / 53.6 % RH
- **Outdoor weather:** 18 new readings (18 total), avg 9.7 °C / 70.7 % RH
- **Commits:** Add daily auto-commit script and .gitignore; Update skincare_data.db; inital_testing
- **Files changed today:** `scripts/daily_commit.ps1`
<!-- PROGRESS:END -->
