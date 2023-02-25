from frames.image_processing import (
    ImageProcessorABC,
    ImageABC,
    ExpandCanvasParamsFactoryABC,
    ExpandCanvasParamsType,
    FV_BORDER_THICKNESS_MULTIPLIER
)


class BaseImageProcessor:
    def __init__(self, source_image: ImageABC, params_factory: ExpandCanvasParamsFactoryABC):
        self._image = source_image
        self._params_factory = params_factory


class PortraitImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def modified_image(self, border_thickness_multiplier: float = FV_BORDER_THICKNESS_MULTIPLIER) -> ImageABC:
        height = self._image.height()
        new_height = new_width = int(height * border_thickness_multiplier)

        return self._image.expand_canvas(new_height, new_width,
                                         self._params_factory.params(self._image, ExpandCanvasParamsType.CENTER))


class SquareImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def modified_image(self, border_thickness_multiplier: float = FV_BORDER_THICKNESS_MULTIPLIER) -> ImageABC:
        biggest_side = max(self._image.height(), self._image.width())
        new_height = new_width = int(biggest_side * border_thickness_multiplier)

        return self._image.expand_canvas(new_height, new_width,
                                         self._params_factory.params(self._image, ExpandCanvasParamsType.CENTER))


class LandscapeImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def modified_image(self, border_thickness_multiplier: float = FV_BORDER_THICKNESS_MULTIPLIER) -> ImageABC:
        new_height = new_width = int(self._image.width() * border_thickness_multiplier)
        return self._image.expand_canvas(new_height, new_width,
                                         self._params_factory.params(self._image, ExpandCanvasParamsType.GOLDEN_RATIO))


class DistortImageProcessor(ImageProcessorABC):
    def __init__(self, source_image: ImageABC):
        self._image = source_image

    def modified_image(self, border_thickness_multiplier: float = FV_BORDER_THICKNESS_MULTIPLIER) -> ImageABC:
        return self._image.distort()


class WhiteFrameProcessorFactory:
    def __init__(self, params_factory: ExpandCanvasParamsFactoryABC):
        self._params_factory = params_factory

    def processor(self, image: ImageABC) -> ImageProcessorABC:
        rate = image.height() / image.width()
        if rate > 1.1:
            return PortraitImageProcessor(image, self._params_factory)
        elif rate < 0.9:
            return LandscapeImageProcessor(image, self._params_factory)
        else:
            return SquareImageProcessor(image, self._params_factory)


class ShashlikManProcessorFactory:
    def processor(self, image: ImageABC) -> ImageProcessorABC:
        return DistortImageProcessor(image)
