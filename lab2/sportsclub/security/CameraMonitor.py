from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class CameraMonitor:
    camera_id: str
    status: str
    alerts: list[str] = field(default_factory=list)

    def record_alert(self, message: str) -> None:
        self.alerts.append(message)
        self.status = "alert"

    def clear_alerts(self) -> None:
        self.alerts.clear()
        self.status = "online"
