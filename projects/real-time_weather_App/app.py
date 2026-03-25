import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ----------------------------
# CONFIG
# ----------------------------
API_KEY = "5de0856be71cfdf38a73f67c85f3ad4b"

st.set_page_config(page_title="Weather App", layout="wide")

st.title("🌦️ Real-Time Weather App")

# ----------------------------
# INPUT
# ----------------------------
col1, col2 = st.columns([3, 1])

with col1:
    city = st.text_input("Enter City Name", "Bangalore")

with col2:
    unit = st.radio("Unit", ["Celsius", "Fahrenheit"])

if unit == "Celsius":
    units = "metric"
    symbol = "°C"
else:
    units = "imperial"
    symbol = "°F"

# ----------------------------
# API FUNCTIONS
# ----------------------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    return requests.get(url).json()

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
    return requests.get(url).json()

# ----------------------------
# BUTTON ACTION
# ----------------------------
if st.button("Get Weather"):

    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("❌ City not found!")
    else:
        # ----------------------------
        # CURRENT WEATHER
        # ----------------------------
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")
        weather_desc = data["weather"][0]["main"]

        st.subheader(f"📍 {city.title()} Weather")

        c1, c2, c3 = st.columns(3)
        c1.metric("🌡 Temperature", f"{temp} {symbol}")
        c2.metric("💧 Humidity", f"{humidity}%")
        c3.metric("☁ Condition", weather_desc)

        st.write(f"🌅 Sunrise: {sunrise}")
        st.write(f"🌇 Sunset: {sunset}")

        # ----------------------------
        # WEATHER ICON
        # ----------------------------
        if "Rain" in weather_desc:
            st.image("https://cdn-icons-png.flaticon.com/512/1163/1163624.png", width=100)
        elif "Cloud" in weather_desc:
            st.image("https://cdn-icons-png.flaticon.com/512/414/414825.png", width=100)
        elif "Clear" in weather_desc:
            st.image("https://cdn-icons-png.flaticon.com/512/869/869869.png", width=100)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/1779/1779940.png", width=100)

        # ----------------------------
        # FORECAST DATA
        # ----------------------------
        forecast = get_forecast(city)

        if forecast.get("cod") == "200":

            temps = []
            dates = []

            # Take one value per day (every 8th entry)
            for item in forecast["list"][::8]:
                temps.append(item["main"]["temp"])
                dates.append(item["dt_txt"])

            df = pd.DataFrame({
                "Date": pd.to_datetime(dates),
                "Temperature": temps
            })

            # ----------------------------
            # IMPROVED GRAPH
            # ----------------------------
            st.subheader("📈 5-Day Forecast")

            fig = px.line(
                df,
                x="Date",
                y="Temperature",
                markers=True,
                title="🌡️ Temperature Trend"
            )

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Date",
                yaxis_title=f"Temperature ({symbol})",
                hovermode="x unified"
            )

            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )

            # Add average line
            fig.add_hline(
                y=df["Temperature"].mean(),
                line_dash="dash",
                annotation_text="Average Temp"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Forecast data not available.")