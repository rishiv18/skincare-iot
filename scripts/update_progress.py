"""Add today's progress entry to README.md, built from the database and git.

Run from anywhere; paths are relative to the repo root. Re-running on the
same day replaces that day's entry rather than adding a duplicate.
"""
import re
import sqlite3
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
README = REPO / "README.md"
DB = REPO / "skincare_data.db"
START, END = "<!-- PROGRESS:START -->", "<!-- PROGRESS:END -->"

HEADER = f"""# Skincare IoT

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

{START}
{END}
"""


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()


def table_stats(conn, table, ts_col, temp_col, hum_col, since):
    total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    new, avg_t, avg_h = conn.execute(
        f"SELECT COUNT(*), AVG({temp_col}), AVG({hum_col}) FROM {table} "
        f"WHERE {ts_col} >= ?", (since,)).fetchone()
    return total, new, avg_t, avg_h


def fmt_stats(label, stats):
    total, new, avg_t, avg_h = stats
    line = f"- **{label}:** {new} new readings ({total} total)"
    if new:
        line += f", avg {avg_t:.1f} °C / {avg_h:.1f} % RH"
    return line


def build_entry(today):
    since = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    lines = [f"### {today}"]

    if DB.exists():
        with sqlite3.connect(DB) as conn:
            lines.append(fmt_stats("Indoor sensor (ESP32)", table_stats(
                conn, "readings", "timestamp", "temperature", "humidity", since)))
            lines.append(fmt_stats("Outdoor weather", table_stats(
                conn, "weather_readings", "timestamp_utc", "temperature_c",
                "humidity_percent", since)))
    else:
        lines.append("- Database not found.")

    commits = git("log", "--since=24 hours ago", "--no-merges",
                  "--format=%s", "--", ".", ":!README.md")
    commits = [c for c in commits.splitlines() if not c.startswith("Daily update")]
    pending = [f for f in git("diff", "--name-only", "HEAD").splitlines()
               if f != "README.md"]
    if commits:
        lines.append("- **Commits:** " + "; ".join(commits))
    if pending:
        lines.append("- **Files changed today:** " + ", ".join(f"`{f}`" for f in pending))
    if not commits and not pending:
        lines.append("- No code changes.")
    return "\n".join(lines)


def main():
    text = README.read_text(encoding="utf-8") if README.exists() else HEADER
    if START not in text:
        text = text.rstrip() + f"\n\n## Progress log\n\n{START}\n{END}\n"

    today = datetime.now().strftime("%Y-%m-%d")
    head, rest = text.split(START, 1)
    log, tail = rest.split(END, 1)
    # Drop any existing entry for today, then put the new one on top.
    log = re.sub(rf"### {today}\n.*?(?=\n### |\Z)", "", log, flags=re.S).strip()
    log = build_entry(today) + ("\n\n" + log if log else "")
    README.write_text(f"{head}{START}\n{log}\n{END}{tail}", encoding="utf-8")


if __name__ == "__main__":
    main()
