from typing import Callable
from loguru import logger
from app.config.config import settings
from telebot import TeleBot
import os


def _loop_for_ids(func: Callable) -> Callable:
    def inner_function(*args, **kwargs):
        bot = TeleBot(settings.telegram.token)
        for id in settings.telegram.ids:
            func(bot, id, *args, **kwargs)
    return inner_function


class ConfigLogging:
    @classmethod
    def setup(cls):
        logger.level("ALERT", no=39, color="<green>")
        logger.level("SEND_LOG_FILE", no=100, color="<green>")

        if not os.path.exists('logs'):
            os.makedirs('logs')
        if settings.MODE == "prod":
            cls._add_loggers()

    @classmethod
    def _add_loggers(cls):
        logger.add(
            sink=settings.logs.path,
            rotation=settings.logs.rotation,
            level=settings.logs.level)

        if settings.logs.telegram:
            logger.add(
                cls._send_alert_log,
                level='ALERT',
                format='{message}')

        if settings.logs.telegram:
            logger.add(
                cls._send_file_log,
                level="SEND_LOG_FILE",
                format="{message}"
            )

    @staticmethod
    @_loop_for_ids
    def _send_alert_log(bot: TeleBot, id: int, message: str):
        bot.send_message(id, message)

    @staticmethod
    @_loop_for_ids
    def _send_file_log(bot: TeleBot, id: int, msg: str):
        with open(settings.logs.path, "rb") as file:
            bot.send_document(chat_id=id, document=file, caption=msg)
