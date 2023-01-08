from database_interaction.DatabaseItems import DatabaseItems
from database_interaction.DatabaseUserTrackedItems import DatabaseUserTrackedItems
from entities.Item import Item


class DatabaseController:
    def __init__(self):
        self._items = DatabaseItems()
        self._user_tracked_items = DatabaseUserTrackedItems()

    def update_user(self, user_id: str, items: list[Item]) -> None:
        self._user_tracked_items.remove_by_user_id(user_id)
        self._user_tracked_items.add_items(user_id, items)

    def get_item_difference(self, user_id: str, items: list[Item]) -> (list[Item], list[Item]):
        self._add_new_items(items)
        old_items = self._user_tracked_items.get_all_by_user_id(user_id)
        old_item_hashes = [item[0] for item in old_items]
        new_item_hashes = [item.get_sha256_value() for item in items]

        sold_items = self._get_sold_items(old_item_hashes, new_item_hashes)
        new_items = self._get_new_items(old_item_hashes, new_item_hashes)

        return sold_items, new_items

    def _get_new_items(self, old_items: list[str], new_items: list[str]) -> list[Item]:
        difference_hashes = list(set(new_items).difference(set(old_items)))
        return [self._convert_tuple_to_item(self._items.get_item_by_hash(item)) for item in difference_hashes]

    def _get_sold_items(self, old_items: list[str], new_items: list[str]) -> list[Item]:
        difference_hashes = list(set(old_items).difference(set(new_items)))
        return [self._convert_tuple_to_item(self._items.get_item_by_hash(item)) for item in difference_hashes]

    def _add_new_items(self, items: list[Item]) -> None:
        for item in items:
            if self._items.get_item(item):
                continue

            self._items.add_item(item)

    @staticmethod
    def _convert_tuple_to_item(item: tuple) -> Item:
        return Item(*item[1::])
