import sys
import yaml
from queue import Queue
from PyQt5.QtWidgets import QApplication

from comm.client import TCPClient
from core.sensor_worker import SensorWorker
from gui.dashboard import Dashboard

CONFIG_PATH = "config/config.yaml"


def load_sensor_limits():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    limits = {}
    for s in config["sensors"]:
        limits[s["name"]] = s["limits"]

    return limits, config["connection"]


def main():
    # Shared queue between worker thread and GUI
    data_queue = Queue()

    # Load configuration
    sensor_limits, conn = load_sensor_limits()

    # TCP client
    client = TCPClient(conn["host"], conn["port"])
    client.connect()

    # Background worker thread
    worker = SensorWorker(client, data_queue)
    worker.start()

    # Start Qt application
    app = QApplication(sys.argv)
    dashboard = Dashboard(data_queue, sensor_limits)

    # Register worker for graceful shutdown
    dashboard.set_worker(worker)

    dashboard.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
