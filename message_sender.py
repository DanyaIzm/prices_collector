import requests
from abc import ABC, abstractmethod


TELEGRAM_BOT_URL_FORMAT = (
    "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
)


class MessageSender(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        ...


class TelegramMessageSender(MessageSender):
    def __init__(self, bot_token: str, consumer_id: int) -> None:
        self.bot_token = bot_token
        self.consumer_id = consumer_id

    def send(self, message: str) -> None:
        requests.get(
            TELEGRAM_BOT_URL_FORMAT.format(self.bot_token, self.consumer_id, message)
        )
