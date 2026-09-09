import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = root / "data" / "weather_data.csv"
out_dir = root / "output"
out_dir.mkdir(exist_ok=True)
out_file = out_dir / "avg_temp_city_year.csv"

cmd = f'py mapper.py < "{data}" | sort | py reducer.py'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

with open(out_file, "w", encoding="utf-8") as f:
    f.write("City_Year,Avg_Temp\n")
    for line in result.stdout.strip().splitlines():
        if "\t" in line:
            key, val = line.split("\t")
            f.write(f"{key},{val}\n")

print(f"\nSaved: {out_file}")