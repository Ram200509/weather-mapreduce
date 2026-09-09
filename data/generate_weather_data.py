import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

cities = {
    "Hyderabad": {"base_temp": 28, "rain_factor": 0.7, "humidity_base": 55},
    "Delhi": {"base_temp": 25, "rain_factor": 0.5, "humidity_base": 45},
    "Mumbai": {"base_temp": 29, "rain_factor": 1.4, "humidity_base": 75},
    "Bangalore": {"base_temp": 24, "rain_factor": 0.9, "humidity_base": 60},
    "Chennai": {"base_temp": 30, "rain_factor": 1.1, "humidity_base": 70},
    "Kolkata": {"base_temp": 28, "rain_factor": 1.3, "humidity_base": 72},
}

start_date = datetime(2018, 1, 1)
end_date = datetime(2026, 12, 31)

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    if month in [3, 4, 5]:
        return "Summer"
    if month in [6, 7, 8, 9]:
        return "Monsoon"
    return "Post-Monsoon"

def generate_weather(city, date, city_info):
    month = date.month
    season = get_season(month)

    if season == "Summer":
        temp_avg = city_info["base_temp"] + random.uniform(4, 9)
    elif season == "Winter":
        temp_avg = city_info["base_temp"] - random.uniform(6, 12)
    elif season == "Monsoon":
        temp_avg = city_info["base_temp"] + random.uniform(-1, 3)
    else:
        temp_avg = city_info["base_temp"] + random.uniform(-2, 4)

    if city == "Delhi" and season == "Summer":
        temp_avg += random.uniform(3, 7)
    if city == "Delhi" and season == "Winter":
        temp_avg -= random.uniform(3, 8)
    if city == "Mumbai":
        temp_avg = max(temp_avg, 24)

    temp_max = temp_avg + random.uniform(3, 7)
    temp_min = temp_avg - random.uniform(3, 6)

    humidity = city_info["humidity_base"] + random.uniform(-15, 15)
    if season == "Monsoon":
        humidity += random.uniform(10, 20)
    humidity = max(20, min(98, humidity))

    if season == "Monsoon":
        rainfall = np.random.exponential(scale=12 * city_info["rain_factor"])
        if random.random() < 0.3:
            rainfall += random.uniform(20, 80)
    elif season == "Post-Monsoon":
        rainfall = np.random.exponential(scale=3)
    else:
        rainfall = np.random.exponential(scale=1.5)
        if random.random() < 0.85:
            rainfall = 0

    rainfall = round(max(0, rainfall), 1)
    wind_speed = random.uniform(5, 18)
    if season == "Monsoon":
        wind_speed += random.uniform(3, 10)

    if rainfall > 30:
        condition = "Heavy Rain"
    elif rainfall > 5:
        condition = "Rainy"
    elif humidity > 80:
        condition = "Cloudy"
    elif temp_max > 38:
        condition = "Hot"
    elif temp_min < 12:
        condition = "Cold"
    else:
        condition = random.choice(["Sunny", "Clear", "Partly Cloudy"])

    return {
        "Date": date.strftime("%Y-%m-%d"),
        "City": city,
        "Temp_Max": round(temp_max, 1),
        "Temp_Min": round(temp_min, 1),
        "Temp_Avg": round(temp_avg, 1),
        "Humidity": round(humidity, 1),
        "Rainfall_mm": rainfall,
        "Wind_Speed_kmh": round(wind_speed, 1),
        "Weather_Condition": condition,
        "Season": season,
    }

print("Generating weather data... Please wait.")
data = []
current_date = start_date
while current_date <= end_date:
    for city, info in cities.items():
        data.append(generate_weather(city, current_date, info))
    current_date += timedelta(days=1)

df = pd.DataFrame(data)
df.to_csv("weather_data.csv", index=False)
print(f"Dataset created successfully! Total rows: {len(df)}")
print("Saved as: weather_data.csv")
print(df.head())