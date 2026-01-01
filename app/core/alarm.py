from datetime import datetime
from core.models import AlarmEvent


class AlarmManager:
    def __init__(self, sensor_limits: dict):
        """
        sensor_limits example:
        {
          "Temp_1": {"low": 20, "high": 80},
          ...
        }
        """
        self.sensor_limits = sensor_limits
        self.active_alarms = []

    def check(self, sensor_name: str, value: float):
        """
        Check sensor value against limits.
        Return AlarmEvent if alarm triggered, else None.
        """
        limits = self.sensor_limits.get(sensor_name)
        if not limits:
            return None

        if value < limits["low"]:
            return self._create_alarm(sensor_name, value, "LOW")

        if value > limits["high"]:
            return self._create_alarm(sensor_name, value, "HIGH")

        return None

    def _create_alarm(self, sensor_name, value, alarm_type):
        alarm = AlarmEvent(
            sensor_name=sensor_name,
            value=value,
            alarm_type=alarm_type,
            timestamp=datetime.now(),
            message=f"{sensor_name} {alarm_type} limit exceeded"
        )
        self.active_alarms.append(alarm)
        return alarm
