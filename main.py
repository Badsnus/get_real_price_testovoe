import asyncio

import aiohttp
from fake_useragent import UserAgent

from dto import Categories, Product, Property, SubCategory

ua = UserAgent()


class Parser:
    __CATEGORIES_URL = '/categories'

    def __init__(self, main_url: str, need_categories: Categories) -> None:
        self.__main_url = main_url
        self.__need_categories = need_categories

    @staticmethod
    async def __get_json_response(url: str) -> dict:
        headers = {'User-agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                try:
                    return await response.json()
                except:  # TODO
                    ...

    async def get_categories(self):
        categories = Categories([], [], [])

        data = await self.__get_json_response(
            url=self.__main_url + self.__CATEGORIES_URL,
        )
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

    async def get_items(self):
        ...

    async def get_item_extra_info(self):
        ...


async def main():
    parser = Parser(
        'https://www.zara.com/kz/ru',
        Categories([], [], []),
    )  # префикс че?
    # print(await parser.get_categories())
    shit = await parser.get_categories()
    print(shit)


asyncio.run(main())
