import requests
import json

from fake_user_agent import user_agent
from entities.Item import Item
from parcers.IParser import IParser


class LootFarmParser(IParser):
    PRICE_RATIO = 1.03 / 100
    URL = "https://loot.farm/botsInventory_730.json"

    def request_market(self) -> str:
        ua = user_agent()
        response = requests.get(url=self.URL, headers={"user-agent": f"{ua}"})

        return response.text

    def parse_response(self, response: str, weapon: str) -> list[Item]:
        return self._parse_blocks_to_items(self._parce_to_blocks(response, weapon))

    @classmethod
    def _parse_blocks_to_items(cls, item_blocks: list[dict]) -> list[Item]:
        items = []

        for item in item_blocks:
            if "|" in item["n"]:
                weapon, skin = item["n"].split(" | ")
            else:
                weapon = item["n"]
                skin = "Vanilla"

            exterior = item["e"]

            price = item["pst"] if "pst" in item else item["p"]
            price = round(price * cls.PRICE_RATIO, 2)

            item_values = sum(item["u"].values(), [])
            for unit in item_values:
                float_value, pattern_seed = unit["f"].split(":")
                float_value = round(float(float_value) / 10 ** 5, 3)

                item_data = Item(price, exterior, float_value, pattern_seed, weapon, skin)
                items.append(item_data)

            return items

    @staticmethod
    def _parce_to_blocks(response: str, weapon: str) -> list[dict]:
        data = json.loads(response)
        item_blocks = []
        for item_block in data["result"].values():
            if weapon not in item_block["n"]:
                continue

            item_blocks.append(item_block)

        return item_blocks
