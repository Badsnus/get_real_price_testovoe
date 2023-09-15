from datetime import datetime

import pandas as pd

from dto import Product


class ExcelWriter:
    @staticmethod
    def __get_name_for_file(filename: str) -> str:
        return f'{filename}_{datetime.now().date()}.xlsx'

    def __init__(self, filename: str, products: list[Product]) -> None:
        self.__filename = self.__get_name_for_file(filename)
        self.__products = products

    def write(self) -> None:
        df = pd.DataFrame(
            [[
                product.vendor_code,
                product.name,
                product.price,
                product.old_price or '',
                ['N', 'Y'][product.is_active],
                product.description,
                product.category_text,
                product.images_text,
                product.properties_text,
                product.url,
                product.added,
            ] for product in self.__products],
            columns=[
                'article',
                'name',
                'price',
                'price_old',
                'is_active',
                'description',
                'categories',
                'images',
                'properties',
                'url',
                'added',
            ],
        )
        df.to_excel(self.__filename, index=False)
