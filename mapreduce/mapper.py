#!/usr/bin/env python3
import sys

header = sys.stdin.readline()
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        parts = line.split(",")
        date = parts[0]
        city = parts[1]
        temp_avg = float(parts[4])
        year = date.split("-")[0]
        print(f"{city}_{year}\t{temp_avg}")
    except Exception:
        continue