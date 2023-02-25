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
from frames.expand_canvas import ExpandCanvasParamsFactory
from frames.image import PilImage
from frames.image_processing import FV_BORDER_THICKNESS_MULTIPLIER
from frames.processors import ShashlikManProcessorFactory, WhiteFrameProcessorFactory


file_id_action_callback_data = CallbackData("i", "file_id", "action")

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

actions = {
    'wf': "White Frame",
    'sm': "Shashlik Man",
}


def _get_keyboard(file_id):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(text=actions['wf'], callback_data=file_id_action_callback_data.new(file_id, "wf")),
        InlineKeyboardButton(text=actions['sm'], callback_data=file_id_action_callback_data.new(file_id, "sm"))
    )

@dp.message_handler(content_types=['photo', 'document'], state="*")
async def image_action_handler(message: types.Message):
    logging.warning(f'Recieved a image from {message.from_user}')
    if message.photo:
        file_id = message.photo[-1].file_id
    if message.document:
        file_id = message.document.file_id
    short_file_id = storage.save(file_id)
    
    
    print(file_id)
    await message.reply("Received image. Which action to perform?", reply_markup=_get_keyboard(short_file_id))
    # await ImageActionForm.file_id.set()
    # async with state.proxy() as data:
    #     data['name'] = message.text
    return

@dp.callback_query_handler(file_id_action_callback_data.filter())
async def perform_action(callback: types.CallbackQuery, callback_data):
    
    file_id = storage.pop(callback_data['file_id'])
    action = actions[callback_data['action']]
    
    file = await bot.get_file(file_id)
    origin_image = await bot.download_file(file.file_path)
    origin_image.seek(0)

    image = PilImage.open(origin_image)
    if action == "White Frame":
        processor = WhiteFrameProcessorFactory(ExpandCanvasParamsFactory()).processor(image)
    elif action == "Shashlik Man":
        processor = ShashlikManProcessorFactory().processor(image)
    else:
        raise NotImplementedError
    image_with_frame = processor.modified_image(border_thickness_multiplier=FV_BORDER_THICKNESS_MULTIPLIER)
    response = BytesIO()
    response.name = "result.jpg"
    image_with_frame.save(response)
    response.seek(0)

    await bot.edit_message_text(
        f'Received image. Performing {action}', 
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
