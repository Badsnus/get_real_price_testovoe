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
        # ну это бы тоже не вшивать так-то
        return (
            f'https://static.zara.net/photos//{self.path}/{self.name}'
            f'?ts={self.timestamp}'
        )


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
    category: str
    subcategories: list[SubCategory]
    images: list[Image]
    properties: list[Property]
    url: str
    added: date

    @property
    def category_text(self):
        res_text = self.category + ';'
        res_text += ';'.join(map(lambda x: x.name, self.subcategories))
        return res_text

    @property
    def images_text(self):
        return ';'.join(image.get_url() for image in self.images)

    @property
    def properties_text(self):
        return ';'.join(
            f'{prop.name}:{prop.description}' for prop in self.properties
        )
