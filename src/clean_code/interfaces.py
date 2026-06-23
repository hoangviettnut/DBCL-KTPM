from abc import ABC, abstractmethod
from src.models import Customer

class ICustomerRepository(ABC):
    """
    Interface/Port bẻ gãy sự phụ thuộc vào Database thực tế.
    Kỹ thuật "Creating Seams" theo sách Software Testing Strategies của Matthew Heusser.
    """
    @abstractmethod
    def fetch_customer_by_id(self, customer_id: str) -> Customer:
        pass
