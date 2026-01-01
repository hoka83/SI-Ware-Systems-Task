import socket
import json
import random
import time
from datetime import datetime


# Server Configuration

HOST = "127.0.0.1"
PORT = 9999


# Sensor Definitions

SENSORS = {
    "Temp_1": {"low": 20, "high": 80},
    "Temp_2": {"low": 20, "high": 80},
    "Pressure_1": {"low": 1, "high": 10},
    "Speed_1": {"low": 500, "high": 1500},
    "Vibration_1": {"low": 0.1, "high": 5.0},
}


def generate_value(low, high):
    """
    Generate sensor value.
    10% probability to exceed limits (simulate alarm).
    """
    if random.random() < 0.1:
        return round(high + random.uniform(5, 20), 2)
    return round(random.uniform(low, high), 2)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"[SIMULATOR] Server started on {HOST}:{PORT}")
    print("[SIMULATOR] Waiting for client connection...")

    conn, addr = server_socket.accept()
    print(f"[SIMULATOR] Client connected from {addr}")

    try:
        while True:
            for sensor_name, limits in SENSORS.items():
                value = generate_value(limits["low"], limits["high"])

                payload = {
                    "sensor": sensor_name,
                    "value": value,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                message = json.dumps(payload) + "\n"
                conn.sendall(message.encode("utf-8"))

                print("[SIMULATOR] Sent:", payload)

                time.sleep(0.3)

    except (BrokenPipeError, ConnectionResetError):
        print("[SIMULATOR] Client disconnected.")

    except Exception as e:
        print("[SIMULATOR] Error:", e)

    finally:
        conn.close()
        server_socket.close()
        print("[SIMULATOR] Server stopped.")


if __name__ == "__main__":
    start_server()
