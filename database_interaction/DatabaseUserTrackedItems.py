import sqlite3
import os

from entities.Item import Item


class DatabaseUserTrackedItems:
    def __init__(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        db_path = os.path.join(project_root, 'database_interaction', 'databases', 'user_tracked_items.db')
        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_tracked_items"
            "(user_id text,"
            "item_hash text)"
        )

    def add_items(self, user_id: str, items: list[Item]) -> None:
        for item in items:
            item_hash = item.get_sha256_value()
            self._cursor.execute("INSERT INTO user_tracked_items VALUES (?, ?)", (user_id, item_hash))

        self._connection.commit()

    def get_all_by_user_id(self, user_id: str) -> list:
        self._cursor.execute("SELECT * FROM user_tracked_items WHERE user_id=?", (user_id,))
        return self._cursor.fetchall()

    def get_by_user_id_and_item(self, user_id: str, item: Item) -> tuple:
        item_hash = item.get_sha256_value()

        self._cursor.execute("SELECT * FROM user_tracked_items WHERE user_id=? AND item_hash=?", (user_id, item_hash))
        return self._cursor.fetchone()

    def remove_by_user_id(self, user_id: str):
        self._cursor.execute("DELETE FROM user_tracked_items WHERE user_id=?", (user_id,))
        self._connection.commit()

    def __del__(self):
        self._connection.close()
