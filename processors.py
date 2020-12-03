from image_processing import ImageProcessorABC, ImageABC, ExpandCanvasParamsFactoryABC, ExpandCanvasParamsType, \
    FV_MULTIPLIER


class BaseImageProcessor:
    def __init__(self, source_image: ImageABC, params_factory: ExpandCanvasParamsFactoryABC):
        self._image = source_image
        self._params_factory = params_factory


class PortraitImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def image_with_frame(self, multiplier: float = FV_MULTIPLIER) -> ImageABC:
        height = self._image.height()
        new_height = new_width = int(height * multiplier)

        return self._image.expand_canvas(new_height, new_width,
                                         self._params_factory.params(self._image, ExpandCanvasParamsType.CENTER))


class SquareImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def image_with_frame(self, multiplier: float = FV_MULTIPLIER) -> ImageABC:
        biggest_side = max(self._image.height(), self._image.width())
        new_height = new_width = int(biggest_side * multiplier)

        return self._image.expand_canvas(new_height, new_width,
                                         self._params_factory.params(self._image, ExpandCanvasParamsType.CENTER))


class LandscaipImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def image_with_frame(self, multiplier: float = FV_MULTIPLIER) -> ImageABC:
        new_height = new_width = int(self._image.width() * multiplier)
        return self._image.expand_canvas(new_height, new_width,
                                         self._params_factory.params(self._image, ExpandCanvasParamsType.GOLDEN_RATIO))


class ImageProcessorFactory:
    def __init__(self, params_factory: ExpandCanvasParamsFactoryABC):
        self._params_factory = params_factory

    def processor(self, image: ImageABC) -> ImageProcessorABC:
        rate = image.height() / image.width()
        if rate > 1.1:
            return PortraitImageProcessor(image, self._params_factory)
        elif rate < 0.9:
            return LandscaipImageProcessor(image, self._params_factory)
        else:
            return SquareImageProcessor(image, self._params_factory)
