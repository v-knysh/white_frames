from ast import Bytes
from io import BytesIO
from aiogram import types
from bot.bot import dp, bot
from frames.expand_canvas import ExpandCanvasParamsFactory
from frames.image import PilImage
from frames.image_processing import FV_BORDER_THICKNESS_MULTIPLIER
from frames.processors import ImageProcessorFactory

@dp.message_handler(content_types=['photo', 'document'])
async def image_handler(message: types.Message):
    if message.photo:
        file_id = message.photo[-1].file_id
    if message.document:
        file_id = message.document.file_id
    file = await bot.get_file(file_id)
    origin_image = await bot.download_file(file.file_path)
    origin_image.seek(0)

    image = PilImage.open(origin_image)
    processor = ImageProcessorFactory(ExpandCanvasParamsFactory()).processor(image)
    image_with_frame = processor.image_with_frame(border_thickness_multiplier=FV_BORDER_THICKNESS_MULTIPLIER)
    response = BytesIO()
    response.name = "result.jpg"
    image_with_frame.save(response)
    response.seek(0)
    
    await message.answer_document(types.InputFile(response))   

