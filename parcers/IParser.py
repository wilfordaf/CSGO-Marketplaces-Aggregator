from abc import ABC, abstractmethod
from entities.Item import Item


class IParser(ABC):
    """Interface for website market parcers"""

    @abstractmethod
    def request_market(self) -> str:
        """Request market data from website"""

    @abstractmethod
    def parse_response(self, response: str, weapon: str) -> list[Item]:
        """Parse response to Item objects"""
