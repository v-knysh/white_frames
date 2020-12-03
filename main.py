from expand_canvas import ExpandCanvasParamsFactory
from image_processors import ImageProcessorFactory

if __name__ == "__main__":
    processor = ImageProcessorFactory(ExpandCanvasParamsFactory()).processor()
    image_with_frame = processor.image_with_frame()
    image_with_frame.save()