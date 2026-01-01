@echo off
echo Starting Sensor Simulator...
start cmd /k "cd "sensor simulator" && python simulator.py"

timeout /t 2 >nul

echo Starting Application...
start cmd /k "cd "app" && python main.py"
