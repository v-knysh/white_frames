import logging
from io import BytesIO
from typing import List

from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

import settings

from bot.bot import dp, bot
from frames.actions import ActionABC, get_action, actions
from frames.image import PilImage


class FileActionCallback(CallbackData, prefix="i"):
    file_id: str
    action_code: str


class NotInStorageException(Exception):
    pass

class InMemoryStorage():
    def __init__(self):
        self._storage = {}

    def save(self, data):
        key = data[-32:]
        self._storage[key] = data
        return key

    def get(self, key):
        if key in self._storage:
            return self._storage.get(key)
        else:
            raise Exception(f"{key} not in storage")



storage = InMemoryStorage()


def _get_keyboard(file_id, actions: List[ActionABC]):
    buttons = [
        InlineKeyboardButton(
            text=a.name,
            callback_data=FileActionCallback(file_id=file_id, action_code=a.code).pack(),
        )
        for a in actions
    ]
    mid = int(len(buttons) / 2)
    return InlineKeyboardMarkup(inline_keyboard=[buttons[:mid], buttons[mid:]])



@dp.message(F.photo | F.document)
async def image_action_handler(message: types.Message):
    logging.warning(f'Recieved a image from {message.from_user}')
    if message.photo:
        file_id = message.photo[-1].file_id
    if message.document:
        file_id = message.document.file_id
    short_file_id = storage.save(file_id)

    await message.reply("Received image. Which action to perform?", reply_markup=_get_keyboard(short_file_id, actions))
    return

@dp.callback_query(FileActionCallback.filter())
async def perform_action(callback: types.CallbackQuery, callback_data: FileActionCallback):

    file_id = storage.get(callback_data.file_id)
    action_code = callback_data.action_code
    action: ActionABC = get_action(action_code)

    try:
        await bot.edit_message_text(
            text=f'Received image. Performing {action.name}',
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None,
        )
    except TelegramBadRequest:
        # message already answered / not modified
        return

    file = await bot.get_file(file_id)
    origin_image = await bot.download_file(file.file_path)
    origin_image.seek(0)

    image = PilImage.open(origin_image)
    processor = action.processor(image)
    modified_image = processor.modified_image()
    response = BytesIO()
    response.name = "result.jpg"
    modified_image.save(response)
    response.seek(0)

    result_file = BufferedInputFile(response.read(), filename="result.jpg")
    if action.answer_type == "document":
        await callback.message.answer_document(result_file)
    else:
        await callback.message.answer_photo(result_file)

    for supervisor in settings.TG_SUPERVISORS_LIST:
        response = BytesIO()
        response.name = "result.jpg"
        modified_image.save(response)
        response.seek(0)
        await bot.send_photo(
            chat_id=supervisor,
            caption=f"User @{callback.from_user.username} created image.",
            photo=BufferedInputFile(response.read(), filename="result.jpg"),
        )

    await callback.answer()
    return



@dp.message(Command("cancel"))
@dp.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """

    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it

    await state.clear()
    # And remove keyboard (just in case)

    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
