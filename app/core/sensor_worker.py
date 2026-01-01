import threading
import json
from datetime import datetime
from core.models import SensorReading


class SensorWorker(threading.Thread):
    def __init__(self, tcp_client, data_queue):
        super().__init__(daemon=True)
        self.client = tcp_client
        self.queue = data_queue
        self.running = True
        self.buffer = ""

    def run(self):
        print("SENSOR WORKER STARTED")

        while self.running:
            try:
                raw = self.client.receive()
                if not raw:
                    continue

                self.buffer += raw

                while "\n" in self.buffer:
                    line, self.buffer = self.buffer.split("\n", 1)
                    payload = json.loads(line)

                    print("WORKER RECEIVED:", payload)

                    reading = SensorReading(
                        name=payload["sensor"],
                        value=float(payload["value"]),
                        timestamp=datetime.strptime(
                            payload["timestamp"], "%Y-%m-%d %H:%M:%S"
                        ),
                    )

                    self.queue.put(reading)

            except Exception as e:
                print("[SensorWorker ERROR]", e)

    def stop(self):
        self.running = False
        self.client.close()
