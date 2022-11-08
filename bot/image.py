from io import BytesIO
from aiogram import types
from bot.bot import dp, bot
from frames.expand_canvas import ExpandCanvasParamsFactory
from frames.image import PilImage
from frames.image_processing import FV_BORDER_THICKNESS_MULTIPLIER
from frames.processors import ImageProcessorFactory

@dp.message_handler(content_types=['photo'])
async def image_handler(message: types.Message):
    await message.answer("received_image")
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    result = await bot.download_file(file.file_path)
    result.seek(0)

    image = PilImage.open(result)
    processor = ImageProcessorFactory(ExpandCanvasParamsFactory()).processor(image)
    image_with_frame = processor.image_with_frame(border_thickness_multiplier=FV_BORDER_THICKNESS_MULTIPLIER)
    image_with_frame.save('result.jpg')
    
    await message.answer_photo(types.InputFile("result.jpg"))   

