from dataclasses import dataclass
from datetime import date


@dataclass
class Category:
    name: str


@dataclass
class Image:
    path: str
    name: str

    def get_url(self):
        ...


@dataclass
class Property:
    name: str
    description: str


@dataclass
class Product:
    vendor_code: str
    name: str
    price: float
    old_price: float
    is_active: bool
    description: str
    categories: list[Category]
    images: list[Image]
    properties: list[Property]
    url: str
    added: date
