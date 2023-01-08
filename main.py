import time

from database_interaction.DatabaseController import DatabaseController
from parcers.LootFarmParser import LootFarmParser
from notification_providers.TelegramNotificationProvider import TelegramNotificationProvider
from notification_providers.NotificationTextFormatter import NotificationTextFormatter


def main():
    lootfarm_parser = LootFarmParser()
    database_controller = DatabaseController()
    telegram_notification_provider = TelegramNotificationProvider()
    item = "Glock-18"
    user_id = "123456789"

    while True:
        result = lootfarm_parser.parse_response(lootfarm_parser.request_market(), item)
        new_items, sold_items = database_controller.get_item_difference(user_id, result)
        database_controller.update_user(user_id, result)
        text = NotificationTextFormatter.format_sold_new_message(new_items, sold_items)
        telegram_notification_provider.send_notification(text)
        time.sleep(20)


if __name__ == "__main__":
    main()
