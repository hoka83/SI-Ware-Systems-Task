from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SensorReading:
    name: str
    value: float
    timestamp: datetime
    status: str = "OK"   


class AlarmEvent:
    sensor_name: str
    value: float
    alarm_type: str      
    timestamp: datetime
    message: Optional[str] = None
