import sqlite3

from entities.Item import Item


def add_item(item: Item):
    item_hash = item.get_sha256_value()
    with sqlite3.connect("../databases/items.db") as con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?)",
            (item_hash,
             item.price,
             item.exterior,
             item.float_value,
             item.pattern_seed,
             item.weapon,
             item.skin))


def find_item(item: Item) -> Item:
    item_hash = item.get_sha256_value()
    with sqlite3.connect("../databases/items.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM items WHERE hash=?", (item_hash,))
        return cursor.fetchone()


def delete_item(item: Item):
    item_hash = item.get_sha256_value()
    with sqlite3.connect("../databases/items.db") as con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM items WHERE hash=?", (item_hash,))


def main():
    with sqlite3.connect("../databases/items.db") as con:
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS items"
            "(hash text primary key,"
            "price real,"
            "exterior text,"
            "float_value real,"
            "pattern_seed integer,"
            "weapon text,"
            "skin text)"
        )


if __name__ == "__main__":
    main()
