from entities.Item import Item


class NotificationTextFormatter:
    def __init__(self, max_message_length: int):
        self._max_message_length = max_message_length

    def format_sold_new_message(self, sold_items: list[Item], new_items: list[Item]) -> list[str]:
        message_content = []

        if sold_items:
            message_content.append("Sold items:")
            sold_items_text = self._format_items(sold_items)
            message_content.extend(sold_items_text)

        if new_items:
            message_content.append("\nNew items:")
            new_items_text = self._format_items(new_items)
            message_content.extend(new_items_text)

        return message_content

    def _format_items(self, items: list[Item]) -> list[str]:
        if items is None or len(items) == 0:
            return []

        message_content = []
        current_message = ""
        for item in items:
            item_text = str(item)
            if len(current_message) + len(item_text) > self._max_message_length:
                message_content.append(current_message)
                current_message = ""

            current_message += item_text + "\n"

        message_content.append(current_message)
        return message_content
