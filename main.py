from expand_canvas import ExpandCanvasParamsFactory
from image import PilImage
from image_processors import ImageProcessorFactory

from PIL import Image


if __name__ == "__main__":
    filename = 'asdasdqwd.jpeg'
    image = PilImage(Image.open(filename))
    processor = ImageProcessorFactory(ExpandCanvasParamsFactory()).processor(image)
    image_with_frame = processor.image_with_frame()
    image_with_frame.save('test.jpg')