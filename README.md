Production Line Monitoring System
=================================

Overview
--------
This project is a desktop application that simulates and monitors an industrial
production line in real time. Sensor data is streamed over TCP, processed in a
background worker thread, and visualized through a graphical dashboard.

The system demonstrates real-world concepts such as TCP communication,
multithreading, real-time monitoring, alarm handling, and clean software
architecture.

---

System Architecture
-------------------
The system consists of two main components:

1) Sensor Simulator
   - Acts as a TCP server
   - Simulates multiple industrial sensors
   - Sends real-time sensor data in JSON format

2) Monitoring Application
   - TCP client connects to the simulator
   - Background worker thread processes incoming data
   - GUI dashboard visualizes live values, trends, and alarms

Data Flow:
Sensor Simulator
    → TCP Client
        → SensorWorker (Thread)
            → Queue
                → Dashboard (GUI)

---

Key Features
------------
- Real-time sensor monitoring
- Multithreaded TCP communication
- Thread-safe data exchange using Queue
- Live dashboard with tables and graphs
- Alarm detection (HIGH / LOW thresholds)
- Alarm history log
- Desktop notifications
- Graceful shutdown of threads and connections

---

Project Structure
-----------------
production_monitoring_system/
│
├── sensor_simulator/
│   └── simulator.py
│
├── app/
│   ├── main.py
│   ├── config/
│   │   └── config.yaml
│   ├── comm/
│   │   └── client.py
│   ├── core/
│   │   ├── sensor_worker.py
│   │   └── models.py
│   └── gui/
│       └── dashboard.py
│
├── SI-Ware_app.bat
└── README.txt

---

Requirements
------------
- Python 3.10+
- PyQt5
- pyqtgraph
- pyyaml
- plyer

Install dependencies:
pip install PyQt5 pyqtgraph pyyaml plyer

---

How to Run
----------
Method 1: One-click startup (Windows)
- Double-click SI-Ware_pp.bat

Method 2: Manual startup
1) Start the sensor simulator:
   python sensor_simulator/simulator.py

2) Start the application:
   cd app
   python main.py

---

Configuration
-------------
Sensor definitions and alarm limits can be modified in:
app/config/config.yaml

No code changes are required to update sensor thresholds.

---

Notes
-----
- The simulator console output is for monitoring/debugging purposes.
- The dashboard displays processed data visually (tables, graphs, alarms).
- The application uses a clean separation between communication, logic, and UI.

---

Author
------
This project was developed as a practical demonstration of Python-based
industrial monitoring systems, focusing on clean architecture, reliability,
and real-time visualization.
