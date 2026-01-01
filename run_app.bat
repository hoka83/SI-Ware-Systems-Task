@echo off
echo Starting Sensor Simulator...
start cmd /k "cd "D:\Real-Time Production Line Sensor Dashboard with Remote\sensor simulator" && python simulator.py"

timeout /t 2 >nul

echo Starting Application...
start cmd /k "cd "D:\Real-Time Production Line Sensor Dashboard with Remote\app" && python main.py"
