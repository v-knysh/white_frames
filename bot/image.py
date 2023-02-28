import logging
from ast import Bytes
from io import BytesIO
from typing import Optional

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from bot.bot import dp, bot
from frames.actions import ActionABC, get_action, actions
from frames.image import PilImage


file_id_action_callback_data = CallbackData("i", "file_id", "action_code")

class InMemoryStorage():
    def __init__(self):
        self._storage = {}
    
    def save(self, data):
        key = data[-32:]
        self._storage[key] = data
        return key
    
    def pop(self, key):
        if key in self._storage:
            return self._storage.pop(key)
        else:
            raise Exception(f"{key} not in storage")


    
storage = InMemoryStorage()


def _get_keyboard(file_id, actions):
    return InlineKeyboardMarkup().row(*(
        InlineKeyboardButton(text=a.name, callback_data=file_id_action_callback_data.new(file_id, a.code))
        for a in actions
    )
    )

@dp.message_handler(content_types=['photo', 'document'], state="*")
async def image_action_handler(message: types.Message):
    logging.warning(f'Recieved a image from {message.from_user}')
    if message.photo:
        file_id = message.photo[-1].file_id
    if message.document:
        file_id = message.document.file_id
    short_file_id = storage.save(file_id)

    await message.reply("Received image. Which action to perform?", reply_markup=_get_keyboard(short_file_id, actions))
    return

@dp.callback_query_handler(file_id_action_callback_data.filter())
async def perform_action(callback: types.CallbackQuery, callback_data):
    
    file_id = storage.pop(callback_data['file_id'])
    action_code = callback_data['action_code']
    
    file = await bot.get_file(file_id)
    origin_image = await bot.download_file(file.file_path)
    origin_image.seek(0)

    image = PilImage.open(origin_image)
    action: ActionABC = get_action(action_code)
    processor = action.processor(image)
    modified_image = processor.modified_image()
    response = BytesIO()
    response.name = "result.jpg"
    modified_image.save(response)
    response.seek(0)

    await bot.edit_message_text(
        f'Received image. Performing {action.name}', 
        callback.from_user.id,
        callback.message.message_id,
        reply_markup=None,
    )
    await callback.message.answer_document(types.InputFile(response))
    await callback.answer()
    return



@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """

    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it

    await state.finish()
    # And remove keyboard (just in case)

    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
