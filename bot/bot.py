import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from settings import TG_BOT_API_TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TG_BOT_API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start", "help"))
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        "Hi! Send me a photo and I'll let you pick what to do with it — "
        "add a white frame or drop it into one of the meme templates."
    )
