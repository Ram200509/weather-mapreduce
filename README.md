# 🌦️ Weather Data Analytics and Prediction Dashboard using MapReduce

A Big Data Analytics mini-project that processes multi-city historical weather records using a **MapReduce-style Python pipeline**, performs climate analytics, predicts the **2027 average temperature**, and presents the results through an interactive **Streamlit dashboard**.

---

## 📌 Project Overview

| Item          | Details                                               |
| ------------- | ----------------------------------------------------- |
| 📅 Timeline   | 1 Jan 2018 → 31 Dec 2026                              |
| 🔮 Prediction | 2027                                                  |
| 🏙️ Cities    | Hyderabad, Delhi, Mumbai, Bangalore, Chennai, Kolkata |
| 🐍 Language   | Python 3                                              |
| ⚙️ Processing | MapReduce                                             |
| 📊 Analytics  | Pandas                                                |
| 🤖 Prediction | Scikit-learn Linear Regression                        |
| 🖥️ Dashboard | Streamlit                                             |
| 📁 Dataset    | Synthetic, climate-realistic                          |

---

# 1. 🎯 Project Goal

The project demonstrates how a large weather CSV can be processed using the **Map → Shuffle/Sort → Reduce** model.

```text
                 weather_data.csv
                        │
                        ▼
                 ┌─────────────┐
                 │   MAPPER    │
                 │  mapper.py  │
                 └──────┬──────┘
                        │
                        │ City_Year → Temp_Avg
                        ▼
                 ┌─────────────┐
                 │ SHUFFLE /   │
                 │    SORT     │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  REDUCER    │
                 │ reducer.py  │
                 └──────┬──────┘
                        │
                        ▼
              avg_temp_city_year.csv
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
      Extra Analytics        2027 Prediction
             │                     │
             └──────────┬──────────┘
                        ▼
               Streamlit Dashboard
```

### 💡 Viva Point

> **"MapReduce is the programming model. Hadoop is one engine that runs it. This project implements the Map → Shuffle/Sort → Reduce logic locally in Python."**

---

# 2. Project Structure

```text
weather-mapreduce/
│
├── README.md
│
├── data/
│   ├── generate_weather_data.py
│   └── weather_data.csv
│
├── mapreduce/
│   ├── mapper.py
│   ├── reducer.py
│   ├── run_jobs.py
│   ├── extra_jobs.py
│   └── spark_jobs.py          # optional / unused
│
├── output/
│   ├── avg_temp_city_year.csv
│   ├── rainfall_city_month.csv
│   ├── summer_temp_city.csv
│   └── extreme_heat_days.csv
│
└── dashboard/
    └── app.py
```

---

# 3. 🌡️ Dataset Generation

`generate_weather_data.py` creates daily weather records for all six cities from **2018–2026**.

```text
2018 ─┐
2019  │
2020  │
2021  │
2022  ├──→ Daily Records
2023  │       ×
2024  │    6 Cities
2025  │       ↓
2026 ─┘   weather_data.csv
```

Approximately:

```text
9 years × ~365 days × 6 cities
             ≈
        19,700 rows
```

### Dataset Fields

```text
Date
City
Temp_Max
Temp_Min
Temp_Avg
Humidity
Rainfall_mm
Wind_Speed_kmh
Weather_Condition
Season
```

### Seasonal Model

```text
        ┌───────────────┐
        │     WINTER    │
        │   Dec – Feb   │
        │   Cooler      │
        └───────┬───────┘
                ↓
┌───────────────┐       ┌───────────────┐
│    SUMMER     │       │    MONSOON    │
│   Mar – May   │──────▶│   Jun – Sep   │
│     Hot       │       │ Rain + Humid  │
└───────────────┘       └───────┬───────┘
                                ↓
                       ┌─────────────────┐
                       │ POST-MONSOON    │
                       │    Oct – Nov    │
                       │   Lighter Rain  │
                       └─────────────────┘
```

Generate the dataset:

```bash
cd data
py generate_weather_data.py
```

---

# 4. ⚙️ MapReduce

## Mapper — `mapper.py`

The Mapper reads each weather record and emits:

```text
City_Year    Temp_Avg
```

Example:

```text
Hyderabad_2023    28.4
Delhi_2023        25.1
Mumbai_2023       28.7
```

Conceptually:

```text
CSV Row
  │
  ├── Date → Year
  ├── City
  └── Temp_Avg
        │
        ▼
Hyderabad_2023 → 28.4
```

---

## Shuffle / Sort

The operating system's `sort` command groups identical keys:

```text
Bangalore_2023    23.4
Bangalore_2023    24.1
Bangalore_2023    23.8
        ↓
Bangalore_2023    [23.4, 24.1, 23.8]
```

---

## Reducer — `reducer.py`

The Reducer calculates:

```text
Average Temperature
=
Sum of Temp_Avg
─────────────────
 Number of rows
```

Example:

```text
Delhi_2023
   │
   ├── 24.5
   ├── 25.2
   └── 26.1
        │
        ▼
     Average
        │
        ▼
   Delhi_2023    25.27
```

---

# 5. 🔄 Complete MapReduce Command

```bash
py mapper.py < weather_data.csv | sort | py reducer.py
```

Or simply:

```bash
cd mapreduce
py run_jobs.py
```

Output:

```text
output/avg_temp_city_year.csv
```

```text
City_Year,Avg_Temp
Bangalore_2018,23.79
Bangalore_2019,23.84
Chennai_2024,29.98
Delhi_2026,24.71
...
```

---

# 6. 📊 Extra Analytics

`extra_jobs.py` generates three additional datasets:

```text
                 weather_data.csv
                        │
                        ▼
                 ┌─────────────┐
                 │ extra_jobs  │
                 └──────┬──────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     Rainfall       Summer Temp    Heat Days
          │             │             │
          ▼             ▼             ▼
 rainfall_        summer_temp_    extreme_heat_
 city_month.csv   city.csv        days.csv
```

| Output                    | Analysis                     |
| ------------------------- | ---------------------------- |
| `rainfall_city_month.csv` | Total rainfall by city/month |
| `summer_temp_city.csv`    | Average summer temperature   |
| `extreme_heat_days.csv`   | Days where `Temp_Max > 38°C` |

Run:

```bash
py extra_jobs.py
```

---

# 7. 🔮 2027 Prediction

The MapReduce output provides yearly temperatures for **2018–2026**.

These values are used to train a simple Linear Regression model.

```text
Average
Temp.
  │
  │                       ● 2026
  │                   ●
  │               ●
  │           ●
  │       ●
  │   ●
  └──────────────────────────────▶ Year
      2018                 2027
                              │
                              ▼
                       🔮 Prediction
```

### Prediction Flow

```text
2018–2026 Yearly Averages
           │
           ▼
    Linear Regression
           │
           ▼
        Year = 2027
           │
           ▼
   Predicted Avg Temperature
```

> ⚠️ This is a **trend forecast**, not an official meteorological prediction.

---

# 8. 🖥️ Streamlit Dashboard

The dashboard provides interactive weather analytics for the selected city.

```text
┌──────────────────────────────────────────────┐
│       🌦️ WEATHER ANALYTICS DASHBOARD        │
├──────────────────────────────────────────────┤
│ City: [ Hyderabad ▼ ]                        │
├──────────────┬──────────────┬────────────────┤
│ 🌡️ Avg Temp  │ 🌧️ Rainfall  │ 🔥 Heat Days  │
├──────────────┴──────────────┴────────────────┤
│                                              │
│       📈 Yearly Average Temperature         │
│                                              │
├──────────────────────────────────────────────┤
│       🌧️ Monthly Rainfall                   │
│                                              │
├──────────────────────────────────────────────┤
│       ☀️ Summer Temperature Comparison       │
│                                              │
├──────────────────────────────────────────────┤
│       🔥 Extreme Heat Days                  │
│                                              │
├──────────────────────────────────────────────┤
│       🔮 2027 Predicted Temperature         │
└──────────────────────────────────────────────┘
```

Run:

```bash
cd D:\weather-mapreduce
py -m streamlit run dashboard/app.py
```

Dashboard:

```text
http://localhost:8501
```

---

# 9. 🚀 Complete Execution

```text
┌─────────────────────────┐
│ generate_weather_data   │
└────────────┬────────────┘
             ▼
      weather_data.csv
             │
             ▼
┌─────────────────────────┐
│      run_jobs.py        │
│ Mapper → Sort → Reducer │
└────────────┬────────────┘
             ▼
 avg_temp_city_year.csv
             │
             ├───────────────┐
             ▼               ▼
      extra_jobs.py     Linear Regression
             │               │
             ▼               ▼
     Analytics CSVs      2027 Forecast
             │               │
             └───────┬───────┘
                     ▼
              Streamlit App
```

### Commands

```bash
cd D:\weather-mapreduce

# 1. Generate dataset
cd data
py generate_weather_data.py

# 2. MapReduce
cd ..\mapreduce
py run_jobs.py

# 3. Extra analytics
py extra_jobs.py

# 4. Dashboard
cd ..
py -m streamlit run dashboard/app.py
```

---

# 10. 📈 Expected Insights

The synthetic dataset is designed to demonstrate patterns such as:

* 🔥 **Delhi / Chennai:** hotter summers
* 🌡️ **Bangalore:** milder temperatures
* 🌧️ **Mumbai / Kolkata:** strong monsoon rainfall
* 🌧️ **Chennai:** significant late-year rainfall
* 🔥 **Bangalore:** fewer extreme-heat days
* 🌧️ **Most cities:** rainfall concentrated around June–September

> Final results should be taken from the newly generated output CSVs because values may change when the dataset is regenerated.

---

# 11. ⚠️ Limitations

* Dataset is **synthetic**, not official IMD data.
* MapReduce runs **locally**, not on a Hadoop cluster.
* 2027 prediction uses **simple Linear Regression**.
* Prediction does not model real atmospheric or monsoon conditions.
* `Temp_Max > 38°C` is a **project-defined** extreme-heat threshold.
* `spark_jobs.py` is optional and not part of the working pipeline.

---

# 12. 🔮 Future Scope

```text
Current Project
      │
      ├──→ Real IMD / NOAA Data
      ├──→ Hadoop Streaming
      ├──→ Apache Spark
      ├──→ Advanced Forecasting
      ├──→ Rainfall / Humidity Prediction
      ├──→ Heatwave Detection
      └──→ Cloud Deployment
```

---

# 13. 🎓 Key Viva Points

### Why MapReduce?

> It demonstrates how large datasets can be processed through Map, Shuffle/Sort, and Reduce stages.

### Why Python instead of Hadoop?

> Hadoop was attempted, but the local environment had compatibility issues. Python provides the same MapReduce logic without requiring a cluster.

### Why Pandas?

> Pandas is used for additional analytics after the core MapReduce aggregation.

### Why Linear Regression?

> It is simple, interpretable, and suitable for demonstrating a basic trend-based prediction.

### Is the prediction accurate?

> It is a trend estimate, not a real meteorological forecast.

---

# 14. 👨‍💻 Author

**Pranav Prayaga** | B.Tech CSE | Geethanjali College of Engineering and Technology

### Project

**Weather Data Analytics and Prediction Dashboard using MapReduce**
