import asyncio
from datetime import datetime

import aiohttp
from fake_useragent import UserAgent

from dto import (
    Categories,
    Image,
    NeedSubCategories,
    Product,
    Property,
    SubCategory,
)

ua = UserAgent()


class Parser:

    @staticmethod
    def __format_subcategory_input_data(subcategory: NeedSubCategories) -> str:
        return f'{subcategory.category_name}--{subcategory.name}'

    def __init__(self,
                 main_url: str,
                 need_categories: list[NeedSubCategories],
                 ) -> None:
        self.__main_url = main_url
        self.__categories_url = main_url + '/categories'

        self.__need_subcategories = set(
            map(self.__format_subcategory_input_data, need_categories)
        )

    def __get_products_url_by_subcategory(self,
                                          subcategory: SubCategory
                                          ) -> str:
        return f'{self.__main_url}/category/{subcategory.id}/products'

    def __get_product_extra_info_url(self, product_id: int) -> str:
        return f'{self.__main_url}/product/{product_id}/extra-detail'

    def __get_product_user_url(self, keyword: str, seo_product_id: int):
        return f'{self.__main_url}/{keyword}-p{seo_product_id}.html'

    @staticmethod
    async def __get_json_response(url: str) -> dict:
        headers = {'User-agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                try:
                    print(response.status)
                    return await response.json()
                except Exception as ex:  # TODO

                    print(ex)
                    ...

    async def get_categories(self) -> Categories:
        categories = Categories([], [], [])

        data = await self.__get_json_response(url=self.__categories_url)
        for category in data['categories']:
            for subcategory in category['subcategories']:
                categories.add_item(
                    category['name'],
                    SubCategory(
                        id=subcategory['id'],
                        name=subcategory['name'],
                        category_name=category['name'],
                    )
                )

        return categories

    # какая-то костыльная функция, потому что блять они пидарасы, хуйню какую-то а не апишку сделали
    async def set_product_properties(self, product: Product) -> None:

        data = await self.__get_json_response(
            self.__get_product_extra_info_url(product.id)
        )
        for section in data[1:]:  # cuz first is useless title
            properties = []
            for texts in section['components']:
                dt_type = texts['datatype']
                if (
                        dt_type == 'subtitle'
                        and (not properties or
                             texts['text']['value'] != properties[-1][0])
                ):
                    properties.append([texts['text']['value'], ''])
                elif dt_type == 'paragraph':
                    properties[-1][-1] = (
                            properties[-1][-1] + texts['text']['value'] + ' '
                    )

            for name, desc in properties:
                product.properties.append(Property(name, desc))

    async def get_items_by_subcategory(self,
                                       subcategory: SubCategory
                                       ) -> list[Product]:
        products = []
        tasks = []

        data = await self.__get_json_response(
            self.__get_products_url_by_subcategory(subcategory),
        )
        for productGroup in data['productGroups']:
            for elem in productGroup['elements']:
                for component in elem['commercialComponents']:
                    detail = component['detail']

                    for color in detail['colors']:
                        seo = component['seo']

                        product = Product(
                            id=component['id'],
                            vendor_code=
                            color['name'] + detail['displayReference'],
                            name=component['name'],
                            price=color['price'],
                            old_price=color.get('oldPrice'),
                            is_active=color['availability'] == 'in_stock',
                            description=component['description'],
                            categories=[subcategory],
                            images=[
                                Image(
                                    path=image['path'],
                                    name=image['name'],
                                    timestamp=image['timestamp'],
                                ) for image in color['xmedia']
                            ],
                            properties=[],
                            url=self.__get_product_user_url(
                                keyword=seo['keyword'],
                                seo_product_id=seo['seoProductId'],
                            ),
                            added=datetime.now().date(),
                        )
                        products.append(product)
                        tasks.append(asyncio.create_task(
                            self.set_product_properties(product),
                        ))
                    await asyncio.gather(*tasks)
                    tasks.clear()
        return products

    async def get_items(self):
        cats = await self.get_categories()
        for sub_category in cats.man + cats.woman + cats.kid:
            formatted_name = self.__format_subcategory_input_data(sub_category)
            if formatted_name not in self.__need_subcategories:
                continue
            items = await self.get_items_by_subcategory(sub_category)
            print(items)


async def main():
    parser = Parser(
        'https://www.zara.com/kz/ru',
        [
            NeedSubCategories('РУБАШКИ', 'МУЖЧИНЫ'),
            # NeedSubCategories('ФУТБОЛКИ', 'ЖЕНЩИНЫ'),
        ],
    )
    # print(await parser.get_categories())
    shit = await parser.get_items()
    print(shit)


asyncio.run(main())
