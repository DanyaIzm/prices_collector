import requests

from abc import ABC, abstractmethod
from typing import List, Dict


WB_URL_FORMAT = (
    "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest={}&spp=29&nm={}"
)
WB_PRODUCT_URL_FORMAT = "https://www.wildberries.ru/catalog/{}/detail.aspx"


class Collector(ABC):
    @abstractmethod
    def collect(self) -> str:
        ...


class WildberriesCollector(Collector):
    def __init__(self, items: Dict[str, List[int]], wb_dest: int) -> None:
        self.items = items
        self.wb_dest = wb_dest

    def collect(self) -> str:
        min_price_item_key = list(self.items.keys())[0]
        min_price = -1
        min_price_item_id = self.items[min_price_item_key][0]

        for position_name, items_list in self.items.items():
            for item_id in items_list:
                price = self._get_wildberries_price(item_id)

                if price <= min_price or min_price == -1:
                    min_price = price
                    min_price_item_id = item_id
                    min_price_item_key = position_name

        formatted_link = WB_PRODUCT_URL_FORMAT.format(min_price_item_id)
        result = (
            f"Минимальная цена на {min_price_item_key}: {min_price}\n{formatted_link}"
        )

        return result

    def _get_wildberries_price(self, item_id: int) -> int:
        result = requests.get(WB_URL_FORMAT.format(self.wb_dest, item_id))
        data = result.json()

        return data["data"]["products"][0]["salePriceU"] // 100
