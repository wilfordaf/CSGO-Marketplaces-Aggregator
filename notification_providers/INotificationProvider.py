from abc import ABC, abstractmethod


class INotificationProvider(ABC):
    """Interface for notification providers"""

    @abstractmethod
    def send_notification(self, text: str) -> None:
        """Send notification"""
