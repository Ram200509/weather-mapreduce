import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[1]
df = pd.read_csv(root / "data" / "weather_data.csv", parse_dates=["Date"])
out = root / "output"
out.mkdir(exist_ok=True)

df["Month"] = df["Date"].dt.month

rainfall = df.groupby(["City", "Month"], as_index=False)["Rainfall_mm"].sum()
rainfall.to_csv(out / "rainfall_city_month.csv", index=False)

summer = (
    df[df["Season"] == "Summer"]
    .groupby("City", as_index=False)["Temp_Avg"]
    .mean()
    .sort_values("Temp_Avg", ascending=False)
)
summer.to_csv(out / "summer_temp_city.csv", index=False)

heat = (
    df[df["Temp_Max"] > 38]
    .groupby("City", as_index=False)
    .size()
    .rename(columns={"size": "Extreme_Heat_Days"})
    .sort_values("Extreme_Heat_Days", ascending=False)
)
heat.to_csv(out / "extreme_heat_days.csv", index=False)

print("Saved extra analytics in output/")
print("\nSummer avg temp:")
print(summer.to_string(index=False))
print("\nExtreme heat days:")
print(heat.to_string(index=False))