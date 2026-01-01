from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QTabWidget
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

import pyqtgraph as pg
from collections import deque
from datetime import datetime
from plyer import notification


class Dashboard(QWidget):
    def __init__(self, data_queue, sensor_limits):
        super().__init__()

        self.queue = data_queue
        self.sensor_limits = sensor_limits
        self.worker = None
        self.sensors = {}         
        self.alarms = []          
        self.plots = {}           
        self.data_buffers = {}    
        self.max_points = 40      

        self.setWindowTitle("Production Line Monitoring System")
        self.resize(900, 600)

        # ================= Main Layout =================
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        
        # TAB 1 — LIVE DASHBOARD
        
        self.live_tab = QWidget()
        live_layout = QVBoxLayout()

        self.status_label = QLabel("System Status: OK")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        live_layout.addWidget(self.status_label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Sensor", "Value", "Timestamp", "Status"]
        )
        live_layout.addWidget(self.table)

        # --------- Real-Time Plots ----------
        self.plot_widget = pg.GraphicsLayoutWidget()
        live_layout.addWidget(self.plot_widget)

        self.live_tab.setLayout(live_layout)
        self.tabs.addTab(self.live_tab, "Live Dashboard")

        
        # TAB 2 — ALARM LOG
        
        self.alarm_tab = QWidget()
        alarm_layout = QVBoxLayout()

        self.alarm_table = QTableWidget(0, 4)
        self.alarm_table.setHorizontalHeaderLabels(
            ["Time", "Sensor", "Value", "Type"]
        )
        alarm_layout.addWidget(self.alarm_table)

        self.alarm_tab.setLayout(alarm_layout)
        self.tabs.addTab(self.alarm_tab, "Alarm Log")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        #  Updated Timer 
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(500)  # 2 updates per second

        # Update Dashboard (Called by Timer)
    
    def update_dashboard(self):
        system_alarm = False

        # -------- Consume Queue --------
        while not self.queue.empty():
            reading = self.queue.get()
            print("DASHBOARD RECEIVED:", reading.name, reading.value)
            self.sensors[reading.name] = reading
            self.update_plot(reading.name, reading.value)

        self.table.setRowCount(len(self.sensors))

        # -------- Update Table --------
        for row, (sensor, reading) in enumerate(self.sensors.items()):
            limits = self.sensor_limits.get(sensor)

            status = "OK"
            color = QColor("lightgreen")

            if limits:
                if reading.value < limits["low"]:
                    status = "LOW"
                    color = QColor("red")
                elif reading.value > limits["high"]:
                    status = "HIGH"
                    color = QColor("red")

            if status != "OK":
                system_alarm = True
                self.add_alarm(sensor, reading.value, status)

            self.table.setItem(row, 0, QTableWidgetItem(sensor))
            self.table.setItem(row, 1, QTableWidgetItem(str(reading.value)))
            self.table.setItem(row, 2, QTableWidgetItem(str(reading.timestamp)))
            self.table.setItem(row, 3, QTableWidgetItem(status))

            for col in range(4):
                self.table.item(row, col).setBackground(color)

        # -------- Global Status --------
        if system_alarm:
            self.status_label.setText("System Status: ALARM")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.status_label.setText("System Status: OK")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")

    
    # Update Real-Time Plot

    def update_plot(self, sensor, value):
        if sensor not in self.data_buffers:
            self.data_buffers[sensor] = deque(maxlen=self.max_points)

            plot = self.plot_widget.addPlot(title=sensor)
            plot.showGrid(x=True, y=True)
            curve = plot.plot(pen="y")

            self.plots[sensor] = curve
            self.plot_widget.nextRow()

        self.data_buffers[sensor].append(value)
        self.plots[sensor].setData(list(self.data_buffers[sensor]))

    # =================================================
    # Add Alarm (Log + Notification)
    # =================================================
    def add_alarm(self, sensor, value, alarm_type):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # منع التكرار المستمر لنفس Alarm
        if self.alarms and self.alarms[-1][:3] == (timestamp, sensor, value):
            return

        self.alarms.append((timestamp, sensor, value, alarm_type))

        row = self.alarm_table.rowCount()
        self.alarm_table.insertRow(row)

        self.alarm_table.setItem(row, 0, QTableWidgetItem(timestamp))
        self.alarm_table.setItem(row, 1, QTableWidgetItem(sensor))
        self.alarm_table.setItem(row, 2, QTableWidgetItem(str(value)))
        self.alarm_table.setItem(row, 3, QTableWidgetItem(alarm_type))

        # -------- Desktop Notification --------
        notification.notify(
            title="⚠ Alarm Triggered",
            message=f"{sensor} value {value} ({alarm_type})",
            timeout=5
        )
    def set_worker(self, worker):
        self.worker = worker
    
    
    def closeEvent(self, event):
        print("Closing application...")

        if self.worker:
            self.worker.stop()

        event.accept()

