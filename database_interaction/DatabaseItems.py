import sqlite3
import os

from entities.Item import Item


class DatabaseItems:
    def __init__(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        db_path = os.path.join(project_root, 'database_interaction', 'databases', 'items.db')
        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS items"
            "(hash text primary key,"
            "price real,"
            "exterior text,"
            "float_value real,"
            "pattern_seed integer,"
            "weapon text,"
            "skin text)"
        )

    def add_item(self, item: Item):
        item_hash = item.get_sha256_value()
        self._cursor.execute(
            "INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?)",
            (item_hash,
             item.price,
             item.exterior,
             item.float_value,
             item.pattern_seed,
             item.weapon,
             item.skin))
        self._connection.commit()

    def get_item(self, item: Item) -> tuple:
        item_hash = item.get_sha256_value()
        self._cursor.execute("SELECT * FROM items WHERE hash=?", (item_hash,))
        return self._cursor.fetchone()

    def get_item_by_hash(self, item_hash: str) -> tuple:
        self._cursor.execute("SELECT * FROM items WHERE hash=?", (item_hash,))
        return self._cursor.fetchone()

    def get_all_items(self) -> list[tuple]:
        self._cursor.execute("SELECT * FROM items")
        return self._cursor.fetchall()

    def delete_item(self, item: Item):
        item_hash = item.get_sha256_value()
        self._cursor.execute("DELETE FROM items WHERE hash=?", (item_hash,))
        self._connection.commit()

    def __del__(self):
        self._connection.close()

if __name__ == "__main__":
    db = DatabaseItems()
    a = db.get_item_by_hash("7426a323b4376875d49b24c2002c73cd131f0965a94d7095fdc5c6d73d63d085")
    print(Item(*a[1::]))
