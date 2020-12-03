from make_frame import ImageProcessorABC, ImageABC, ExpandCanvasParamsFactoryABC, ExpandCanvasParamsType

fotovramke_default_height = 2075
fotovramke_default_width = 3130
thin_border_multiplier = 3246 / fotovramke_default_width


class BaseImageProcessor:
    def __init__(self, source_image: ImageABC, params_factory: ExpandCanvasParamsFactoryABC):
        self._image = source_image
        self._params_factory = params_factory


class PortraitImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def image_with_frame(self) -> ImageABC:
        height = self._image.height()
        new_height = new_width = int(height * thin_border_multiplier)

        return self._image.expand_canvas(new_height, new_width,
                                         self._params_factory.params(self._image, ExpandCanvasParamsType.CENTER))


class SquareImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def image_with_frame(self) -> ImageABC:
        return self._image


class LandscaipImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def image_with_frame(self) -> ImageABC:
        new_height = new_width = int(self._image.height() * thin_border_multiplier)
        return self._image.expand_canvas(new_height, new_width,
                                         self._params_factory.params(self._image, ExpandCanvasParamsType.CENTER))


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
