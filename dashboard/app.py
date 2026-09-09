import pandas as pd
import streamlit as st
from pathlib import Path
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="Weather Analytics Dashboard", layout="wide")
root = Path(__file__).resolve().parents[1]

raw = pd.read_csv(root / "data" / "weather_data.csv", parse_dates=["Date"])
avg_temp = pd.read_csv(root / "output" / "avg_temp_city_year.csv")
if "City_Year" in avg_temp.columns:
    avg_temp[["City", "Year"]] = avg_temp["City_Year"].str.rsplit("_", n=1, expand=True)
    avg_temp["Year"] = avg_temp["Year"].astype(int)

summer = pd.read_csv(root / "output" / "summer_temp_city.csv")
heat = pd.read_csv(root / "output" / "extreme_heat_days.csv")
rain = pd.read_csv(root / "output" / "rainfall_city_month.csv")

st.title("Weather Data Analytics and Prediction Dashboard")
st.caption("MapReduce analytics on 2018–2024 weather data for 6 Indian cities")

city = st.sidebar.selectbox("Select city", sorted(raw["City"].unique()))

c1, c2, c3 = st.columns(3)
city_raw = raw[raw["City"] == city]
c1.metric("Avg Temperature", f"{city_raw['Temp_Avg'].mean():.1f} °C")
c2.metric("Total Rainfall", f"{city_raw['Rainfall_mm'].sum():.0f} mm")
c3.metric("Extreme Heat Days", int(heat.loc[heat["City"] == city, "Extreme_Heat_Days"].sum()))

st.subheader("Average Temperature by Year (MapReduce output)")
city_year = avg_temp[avg_temp["City"] == city].sort_values("Year")
st.line_chart(city_year.set_index("Year")["Avg_Temp"])

st.subheader("Monthly Rainfall")
city_rain = rain[rain["City"] == city].sort_values("Month")
st.bar_chart(city_rain.set_index("Month")["Rainfall_mm"])

st.subheader("Summer Average Temperature by City")
st.bar_chart(summer.set_index("City")["Temp_Avg"])

st.subheader("Extreme Heat Days by City")
st.bar_chart(heat.set_index("City")["Extreme_Heat_Days"])

st.subheader("Prediction: Next Year Average Temperature")
X = city_year[["Year"]].values
y = city_year["Avg_Temp"].values
model = LinearRegression()
model.fit(X, y)
next_year = int(city_year["Year"].max()) + 1
pred = model.predict(np.array([[next_year]]))[0]
st.write(f"Predicted average temperature for **{city} in {next_year}**: **{pred:.2f} °C**")