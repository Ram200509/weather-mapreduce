# 🌦️ Weather Data Analytics and Prediction Dashboard using MapReduce

A Big Data Analytics mini-project that processes multi-city historical weather records using a **MapReduce-style Python pipeline**, performs climate analytics, predicts the **2027 average temperature**, and presents the results through an interactive **Streamlit dashboard**.

---

## 📌 Project Overview

| Item                   | Details                                               |
| ---------------------- | ----------------------------------------------------- |
| 📅 **Timeline**        | 1 January 2018 → 30 September 2026                    |
| 🔮 **Prediction Year** | 2027                                                  |
| 🏙️ **Cities**         | Hyderabad, Delhi, Mumbai, Bangalore, Chennai, Kolkata |
| 🐍 **Language**        | Python 3                                              |
| ⚙️ **Processing**      | MapReduce                                             |
| 📊 **Analytics**       | Pandas                                                |
| 🤖 **Prediction**      | Scikit-learn Linear Regression                        |
| 🖥️ **Dashboard**      | Streamlit                                             |
| 📁 **Dataset**         | Synthetic, climate-realistic                          |

> **Important:** 2026 is a **partial year** containing data only from January through September. October–December 2026 are not included in the dataset, so the model does not train on those excluded months.

---

# 1. 🎯 Project Goal

The project demonstrates how a large weather CSV dataset can be processed using the **Map → Shuffle/Sort → Reduce** programming model.

```text
weather_data.csv
        │
        ▼
┌─────────────┐
│   MAPPER    │
│  mapper.py  │
└──────┬──────┘
       │
       │  City_Year → Temp_Avg
       ▼
┌─────────────┐
│ SHUFFLE /   │
│    SORT     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   REDUCER   │
│ reducer.py  │
└──────┬──────┘
       │
       ▼
avg_temp_city_year.csv
       │
   ┌───┴──────────┐
   ▼              ▼
Extra Analytics   2027 Prediction
   │              │
   └──────┬───────┘
          ▼
  Streamlit Dashboard
```

### 💡 Viva Point

> **"MapReduce is the programming model. Hadoop is one engine that runs it. This project implements the Map → Shuffle/Sort → Reduce logic locally in Python."**

---

# 2. 📁 Project Structure

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
│   └── spark_jobs.py          # Optional / unused
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

`generate_weather_data.py` creates daily weather records for all six cities from **1 January 2018 to 30 September 2026**.

```text
2018 ─┐
2019  │
2020  │
2021  │
2022  ├──→ Daily Records
2023  │         ×
2024  │      6 Cities
2025  │         ↓
2026 ─┘   weather_data.csv
(Jan–Sep only)
```

### 📊 Approximate Dataset Size

```text
2018–2025: 8 full years × ~365 days × 6 cities
2026:      273 days (1 Jan – 30 Sep) × 6 cities

≈ 19,176 rows
```

## Dataset Fields

| Field               | Description                     |
| ------------------- | ------------------------------- |
| `Date`              | Date of the weather observation |
| `City`              | City name                       |
| `Temp_Max`          | Maximum temperature             |
| `Temp_Min`          | Minimum temperature             |
| `Temp_Avg`          | Average temperature             |
| `Humidity`          | Relative humidity               |
| `Rainfall_mm`       | Rainfall in millimeters         |
| `Wind_Speed_kmh`    | Wind speed in km/h              |
| `Weather_Condition` | Weather condition               |
| `Season`            | Season classification           |

## 🌤️ Seasonal Model

```text
┌───────────────┐
│    WINTER     │
│   Dec – Feb   │
│    Cooler     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    SUMMER     │
│   Mar – May   │
│      Hot      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    MONSOON    │
│   Jun – Sep   │
│ Rain + Humid  │
└───────┬───────┘
        │
        ▼
┌─────────────────┐
│  POST-MONSOON   │
│    Oct – Nov    │
│  Lighter Rain   │
└─────────────────┘
```

For **2026**, winter, summer, and monsoon are present.

> **Note:** Post-monsoon (October–November) and December are **not generated for 2026**.

### Generate the Dataset

```bash
cd data
py generate_weather_data.py
```

The generator must use the following end date:

```python
end_date = datetime(2026, 9, 30)
```

---

# 4. ⚙️ MapReduce Processing

## 🗺️ Mapper — `mapper.py`

The Mapper reads each weather record and emits a key-value pair:

```text
City_Year    Temp_Avg
```

### Example

```text
Hyderabad_2023    28.4
Delhi_2023        25.1
Mumbai_2023       28.7
```

For 2026, the keys are generated only from the available **January–September** records.

---

## 🔀 Shuffle / Sort

The operating system's `sort` command groups identical keys together.

### Example

```text
Bangalore_2023    23.4
Bangalore_2023    24.1
Bangalore_2023    23.8
        ↓
Bangalore_2023    [23.4, 24.1, 23.8]
```

This represents the **Shuffle/Sort** stage of MapReduce.

---

## 📉 Reducer — `reducer.py`

The Reducer calculates the average temperature for each city-year group.

### Formula

```text
Average Temperature
=
Sum of Temp_Avg
─────────────────
 Number of rows
```

The **2026 average is a partial-year average**, because the dataset contains only January–September 2026.

---

# 5. 🔄 Complete MapReduce Command

The complete pipeline can be executed manually using:

```bash
py mapper.py < weather_data.csv | sort | py reducer.py
```

Or by using the job runner:

```bash
cd mapreduce
py run_jobs.py
```

### Output

```text
output/avg_temp_city_year.csv
```

---

# 6. 📊 Extra Analytics

`extra_jobs.py` performs additional analytics using the same dataset cutoff of **30 September 2026**.

| Output File               | Analysis                               |
| ------------------------- | -------------------------------------- |
| `rainfall_city_month.csv` | Total rainfall by city and month       |
| `summer_temp_city.csv`    | Average summer temperature by city     |
| `extreme_heat_days.csv`   | Number of days where `Temp_Max > 38°C` |

Run the extra analytics using:

```bash
py extra_jobs.py
```

---

# 7. 🔮 2027 Temperature Prediction

The yearly MapReduce averages from **2018–2026** are used to train a **Linear Regression** model.

The model then predicts the average temperature for **2027**.

```text
2018 ─┐
2019  │
2020  │
2021  │
2022  ├──→ Linear Regression ──→ 2027 Prediction
2023  │
2024  │
2025  │
2026* ┘
```

> ***2026 contains January–September data only.**

### ⚠️ Important

This is a **trend forecast**, not an official meteorological prediction.

The dashboard always predicts **2027** rather than dynamically predicting `max(year) + 1`.

---

# 8. 🖥️ Streamlit Dashboard

The Streamlit dashboard presents the processed results and prediction interactively.

The dashboard displays:

* Historical yearly temperature trends
* City-wise comparisons
* Rainfall analytics
* Summer temperature analysis
* Extreme heat statistics
* 2027 temperature prediction

The dashboard caption clearly states:

```text
Data Window: 1 January 2018 – 30 September 2026
Forecast Year: 2027
```

### Run the Dashboard

From the project root:

```bash
cd D:\weather-mapreduce
py -m streamlit run dashboard/app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

---

# 9. 🚀 Complete Execution Pipeline

Run the complete project using the following commands:

```bash
cd D:\weather-mapreduce

# Generate weather dataset
cd data
py generate_weather_data.py

# Run MapReduce and extra analytics
cd ..\mapreduce
py run_jobs.py
py extra_jobs.py

# Launch Streamlit dashboard
cd ..
py -m streamlit run dashboard/app.py
```

### Complete Workflow

```text
┌──────────────────────┐
│ Generate Weather Data│
│ generate_weather_data│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     Mapper           │
│     mapper.py        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Shuffle / Sort     │
│      OS sort         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Reducer         │
│     reducer.py       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ avg_temp_city_year   │
│        .csv          │
└──────────┬───────────┘
           │
      ┌────┴────┐
      ▼         ▼
┌───────────┐ ┌──────────────┐
│  Extra    │ │   Linear     │
│ Analytics │ │  Regression  │
└─────┬─────┘ └──────┬───────┘
      │              │
      └──────┬───────┘
             ▼
    ┌─────────────────┐
    │    Streamlit    │
    │    Dashboard    │
    └─────────────────┘
```

---

# 10. 📈 Expected Insights

The analysis is expected to reveal patterns such as:

* **Delhi and Chennai** generally experience hotter summer temperatures.
* **Bangalore** generally has milder temperatures and fewer extreme-heat days.
* **Mumbai and Kolkata** experience strong monsoon rainfall.
* **Chennai** can experience significant late-year rainfall during complete years.
* Rainfall in most cities is concentrated around the **June–September monsoon period**.

> **Note:** Final numerical results depend on the generated dataset and should be obtained from the output CSV files after regeneration through **30 September 2026**.

---

# 11. ⚠️ Limitations

1. The dataset is **synthetic** and is not sourced from official IMD weather observations.
2. Weather records stop at **30 September 2026**.
3. The 2026 MapReduce average represents a **partial-year average**.
4. MapReduce is implemented locally in Python and does **not run on a Hadoop cluster**.
5. The 2027 prediction uses **simple Linear Regression**, not a specialized meteorological forecasting model.
6. `Temp_Max > 38°C` is a **project-defined threshold** for identifying extreme heat days.
7. `spark_jobs.py` is optional and is **not part of the working pipeline**.
8. Synthetic data may not fully represent real-world weather variability, extreme events, or long-term climate behavior.

---

# 12. 🔮 Future Scope

The project can be extended in several ways:

* Use real **IMD / NOAA** weather datasets.
* Implement the pipeline using **Hadoop Streaming**.
* Migrate large-scale processing to **Apache Spark**.
* Predict rainfall and humidity.
* Develop dedicated heatwave detection algorithms.
* Incorporate additional meteorological variables.
* Deploy the dashboard to a cloud platform.
* Use advanced time-series forecasting models.
* Process significantly larger datasets using distributed computing.

---

# 13. 🎓 Key Viva Points

### ❓ Why MapReduce?

> MapReduce provides a structured way to process large datasets through three major stages: **Map, Shuffle/Sort, and Reduce**.

### ❓ Why Python instead of Hadoop?

> Hadoop was attempted, but the environment was incompatible. Python was therefore used to implement the same MapReduce programming model locally.

### ❓ Is this Hadoop?

> No. This project implements the **MapReduce programming model locally in Python**. Hadoop is a distributed framework that can execute MapReduce jobs across a cluster.

### ❓ Why stop the dataset in September 2026?

> The project intentionally excludes October–December 2026. The pipeline therefore trains using data available through **30 September 2026** and forecasts the average temperature for **2027**.

### ❓ Why use Pandas?

> Pandas is used for additional analytics after the core MapReduce processing, including rainfall analysis, summer temperature analysis, and extreme-heat analysis.

### ❓ Why Linear Regression?

> Linear Regression provides a simple, interpretable method for identifying the overall yearly temperature trend and generating a basic 2027 forecast.

### ❓ Is the 2027 prediction accurate?

> It should not be considered an official weather prediction. It is a **trend-based estimate** generated using Linear Regression. The limitation is especially important because the 2026 training point contains only January–September data.

### ❓ What happens to 2026?

> 2026 is treated as a partial year. Only records from **1 January through 30 September 2026** are included in the dataset and MapReduce calculations.

### ❓ What does the Reducer calculate?

> The Reducer groups records by `City_Year` and calculates the average of `Temp_Avg` for each group.

---

# 14. 👨‍💻 Authors

**Pranav Prayaga** | **Sreenidhi** | **Dhanunjaya**

**B.Tech CSE**
**Geethanjali College of Engineering and Technology**

### 🌦️ Weather Data Analytics and Prediction Dashboard using MapReduce
