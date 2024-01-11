import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    telegram_id: str
    telegram_bot_token: str
    wb_dest: int


def get_config() -> Config:
    load_dotenv()

    return Config(
        telegram_id=os.getenv("TELEGRAM_ID"),
        telegram_bot_token=os.getenv("TELEGRAM_TOKEN"),
        wb_dest=os.getenv("WB_DEST"),
    )
