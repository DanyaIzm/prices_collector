import time

import schedule

from collector import Collector, WildberriesCollector
from config import get_config
from message_sender import MessageSender, TelegramMessageSender


class Manager:
    def __init__(self, collector: Collector, message_sender: MessageSender) -> None:
        self.collector = collector
        self.message_sender = message_sender

    def make_action(self) -> None:
        try:
            try:
                message = self.collector.collect()
            except Exception as e:
                message = f"Произошла непредвиденная ошибка:\n{e}"

            self.message_sender.send(message)
        except Exception as e:
            print(e)


def main():
    config = get_config()

    collector = WildberriesCollector(
        {"Clean Architecture": [179890195, 150735551]}, config.wb_dest
    )
    message_sender = TelegramMessageSender(
        config.telegram_bot_token, config.telegram_id
    )

    manager = Manager(collector, message_sender)

    schedule.every(30).minutes.do(manager.make_action)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
