#!/usr/bin/env python3
# Support transmission of fiber optic temperature data
# Reads RS485 modbus using this bash script to print the FO1 value to stdout:
### !/bin/bash
### cint=`/home/pugsley/.local/share/virtualenvs/modbus/bin/modbus -b 9600 -S /dev/ttyUSB0 i@385`
### echo "scale=2; $cint/100" | bc
#
# This output value is formatted as metrics data and written to a node_exporter 
# file that is picked up and transmitted by the node_exporter (docker container) server

import subprocess
import time
from pathlib import Path

FILE_PATH = Path("/data/node_exporter/textfiles/RMFO1.prom")
CMD = ["/home/pugsley/Utility/readRMFO1"]          # replace with your real command

def fetch_value():
    try:
        output = subprocess.check_output(CMD, text=True).strip()
        return float(output)
    except Exception as e:
        print(f"Error running {CMD}: {e}")
        return None

while True:
    val = fetch_value()
    if val is not None:
        # Build a single metric line (you can add more lines if needed)
        metric_line = f'# TYPE rmfo_temperature_fo1_degC gauge\nrmfo_temperature_fo1_degC {val}\n'
        FILE_PATH.write_text(metric_line)   # atomic replace
    time.sleep(2)  # whatever interval you like
