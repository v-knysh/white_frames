import logging

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from settings import (
    WEBHOOK_URL,
    WEBHOOK_PATH,
    WEBAPP_HOST,
    WEBAPP_PORT,
)

import bot  # noqa: F401  -- registers message/callback handlers
from bot.bot import bot as tg_bot, dp


async def on_startup(bot):
    logging.warning('Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(bot):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=tg_bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=tg_bot)

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
