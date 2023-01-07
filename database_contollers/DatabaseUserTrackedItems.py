import sqlite3

from entities.Item import Item


def add_items(user_id: str, *items: Item):
    with sqlite3.connect("../databases/user_tracked_items.db") as con:
        cursor = con.cursor()
        for item in items:
            item_hash = item.get_sha256_value()
            cursor.execute("INSERT INTO user_tracked_items VALUES (?, ?)", (user_id, item_hash))


def get_all_by_user_id(user_id: str) -> list:
    with sqlite3.connect("../databases/user_tracked_items.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM user_tracked_items WHERE user_id=?", (user_id,))
        return cursor.fetchall()


def remove_by_user_id(user_id: str):
    with sqlite3.connect("../databases/user_tracked_items.db") as con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM user_tracked_items WHERE user_id=?", (user_id,))


def main():
    with sqlite3.connect("../databases/user_tracked_items.db") as con:
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_tracked_items"
            "(user_id text,"
            "item_hash text)"
        )


if __name__ == "__main__":
    main()

