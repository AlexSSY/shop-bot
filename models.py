from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    image_id: str
    price: float
