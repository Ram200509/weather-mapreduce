#!/usr/bin/env python3
import sys

current_key = None
temp_sum = 0.0
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        key, temp = line.split("\t")
        temp = float(temp)
        if current_key == key:
            temp_sum += temp
            count += 1
        else:
            if current_key is not None:
                print(f"{current_key}\t{round(temp_sum / count, 2)}")
            current_key = key
            temp_sum = temp
            count = 1
    except Exception:
        continue

if current_key is not None:
    print(f"{current_key}\t{round(temp_sum / count, 2)}")