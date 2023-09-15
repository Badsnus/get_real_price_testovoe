from dataclasses import dataclass
from datetime import date


@dataclass
class NeedSubCategories:
    name: str
    category_name: str


@dataclass
class SubCategory(NeedSubCategories):
    id: int


@dataclass
class Categories:
    man: list[SubCategory]
    woman: list[SubCategory]
    kid: list[SubCategory]

    def add_item(self, category_name: str, value: SubCategory) -> None:
        if value in ['JOIN LIFE', '+ Info']:
            return
        insert_to: list = {
            'ЖЕНЩИНЫ': self.woman,
            'МУЖЧИНЫ': self.man,
            'ДЕТИ': self.kid,
        }[category_name]
        insert_to.append(value)


@dataclass
class Image:
    path: str
    name: str
    timestamp: str

    def get_url(self):
        ...


@dataclass
class Property:
    name: str
    description: str


@dataclass
class Product:
    id: int
    vendor_code: str
    name: str
    price: float
    old_price: float | None
    is_active: bool
    description: str
    categories: list[SubCategory]
    images: list[Image]
    properties: list[Property]
    url: str
    added: date
