import aiohttp
from fake_useragent import UserAgent

from dto import Category, Product, Property

ua = UserAgent()


class Parser:
    def __init__(self,
                 main_url: str,
                 need_categories: list[str],
                 ) -> None:
        self.__main_url = main_url
        self.__need_categories = need_categories

    async def get_categories(self):
        ...

    async def get_items(self):
        ...

    async def get_item_extra_info(self):
        ...


class ManParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = ''


man = ManParser('мужчины')
