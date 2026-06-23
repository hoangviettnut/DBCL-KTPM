from dataclasses import dataclass

@dataclass
class Product:
    id: str
    name: str
    price: float

@dataclass
class Customer:
    id: str
    name: str
    is_vip: bool
    loyalty_points: int
