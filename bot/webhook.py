import logging

from aiogram import Bot, types, filters
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from settings import (
    TG_BOT_API_TOKEN,
    HEROKU_APP_NAME,
    WEBHOOK_URL,
    WEBHOOK_PATH,
    WEBAPP_HOST,
    WEBAPP_PORT
)

from bot.bot import bot, dp

dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
