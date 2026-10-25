
import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

DB_FILE = "skincare_data.db"

st.set_page_config(
    page_title="Skincare IoT Dashboard",
    layout="wide"
)

st.title("Skincare IoT Environmental Dashboard")
st.caption("ESP32-S3 + SHT31-D + Open-Meteo")

@st.cache_data(ttl=5)
def load_data():
    with sqlite3.connect(DB_FILE) as conn:
        sensor = pd.read_sql_query("""
            SELECT timestamp, temperature, humidity
            FROM readings
            ORDER BY timestamp
        """, conn)

        weather = pd.read_sql_query("""
            SELECT timestamp_utc, weather_time_utc,
                   temperature_c, humidity_percent
            FROM weather_readings
            ORDER BY timestamp_utc
        """, conn)

    if not sensor.empty:
        sensor["time"] = pd.to_datetime(
            sensor["timestamp"], utc=True
        )

    if not weather.empty:
        weather["time"] = pd.to_datetime(
            weather["weather_time_utc"], utc=True
        )

    return sensor, weather

sensor, weather = load_data()

col1, col2, col3 = st.columns(3)

col1.metric("Sensor readings", len(sensor))
col2.metric("Weather readings", len(weather))

if not sensor.empty:
    col3.metric(
        "Latest sensor temperature",
        f"{sensor['temperature'].iloc[-1]:.2f} °C"
    )

st.divider()

if sensor.empty or weather.empty:
    st.warning("Waiting for both data sources.")
else:
    fig_temp = go.Figure()

    fig_temp.add_trace(go.Scatter(
        x=sensor["time"],
        y=sensor["temperature"],
        name="SHT31 temperature",
        mode="lines"
    ))

    fig_temp.add_trace(go.Scatter(
        x=weather["time"],
        y=weather["temperature_c"],
        name="Outdoor temperature",
        mode="lines+markers"
    ))

    fig_temp.update_layout(
        title="Temperature comparison",
        xaxis_title="Time (UTC)",
        yaxis_title="Temperature (°C)"
    )

    st.plotly_chart(fig_temp, use_container_width=True)

    fig_humidity = go.Figure()

    fig_humidity.add_trace(go.Scatter(
        x=sensor["time"],
        y=sensor["humidity"],
        name="SHT31 humidity",
        mode="lines"
    ))

    fig_humidity.add_trace(go.Scatter(
        x=weather["time"],
        y=weather["humidity_percent"],
        name="Outdoor humidity",
        mode="lines+markers"
    ))

    fig_humidity.update_layout(
        title="Relative humidity comparison",
        xaxis_title="Time (UTC)",
        yaxis_title="Relative humidity (%)"
    )

    st.plotly_chart(fig_humidity, use_container_width=True)

st.divider()

st.subheader("Raw sensor data")
st.dataframe(sensor, use_container_width=True)

st.subheader("Raw weather data")
st.dataframe(weather, use_container_width=True)
