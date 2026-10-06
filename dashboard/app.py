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
st.caption("MapReduce analytics on weather data for 6 Indian cities, 1 Jan 2018 – 30 Sep 2026. Forecast year: 2027.")

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

st.subheader("Prediction: 2027 Average Temperature")
st.caption("Linear regression on yearly MapReduce averages. Training window ends 30 September 2026. 2026 is a partial year (Jan–Sep).")

train = city_year[city_year["Year"] <= 2026].sort_values("Year")
if len(train) >= 2:
    model = LinearRegression()
    model.fit(train[["Year"]].values, train["Avg_Temp"].values)
    pred = float(model.predict(np.array([[2027]]))[0])
    st.write(f"Predicted average temperature for **{city} in 2027**: **{pred:.2f} °C**")
    chart = pd.concat([
        train.assign(Series="Observed")[["Year", "Avg_Temp", "Series"]],
        pd.DataFrame({"Year": [2027], "Avg_Temp": [round(pred, 2)], "Series": ["Predicted"]}),
    ])
    st.line_chart(chart.pivot_table(index="Year", columns="Series", values="Avg_Temp"))
else:
    st.warning("Not enough yearly points to fit 2027.")