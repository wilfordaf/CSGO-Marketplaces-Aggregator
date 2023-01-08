import telebot

from os import path, environ
from dotenv import load_dotenv
from notification_providers.INotificationProvider import INotificationProvider


class TelegramNotificationProvider(INotificationProvider):
    MAX_MESSAGE_LENGTH = 4096
    LINE_LENGTH = 50

    def __init__(self):
        load_dotenv()
        self._bot = telebot.TeleBot(token=environ.get("TOKEN"))
        self._bot.send_message(chat_id=environ.get("CHAT_ID"), text="Started working!")

    def send_notification(self, text: list[str]) -> None:
        for message in text:
            self._bot.send_message(chat_id=environ.get("CHAT_ID"), text=message)
