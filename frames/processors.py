from frames.image_processing import (
    ExpandCanvasParams,
    ImageProcessorABC,
    ImageABC,
    FV_BORDER_THICKNESS_MULTIPLIER
)


class BaseImageProcessor:
    def __init__(self, source_image: ImageABC, params: ExpandCanvasParams):
        self._image = source_image
        self._params = params


class PortraitImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def modified_image(self, border_thickness_multiplier: float = FV_BORDER_THICKNESS_MULTIPLIER) -> ImageABC:
        height = self._image.height()
        new_height = new_width = int(height * border_thickness_multiplier)

        return self._image.expand_canvas(new_height, new_width, self._params)


class SquareImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def modified_image(self, border_thickness_multiplier: float = FV_BORDER_THICKNESS_MULTIPLIER) -> ImageABC:
        biggest_side = max(self._image.height(), self._image.width())
        new_height = new_width = int(biggest_side * border_thickness_multiplier)

        return self._image.expand_canvas(new_height, new_width, self._params)


class LandscapeImageProcessor(BaseImageProcessor, ImageProcessorABC):
    def modified_image(self, border_thickness_multiplier: float = FV_BORDER_THICKNESS_MULTIPLIER) -> ImageABC:
        new_height = new_width = int(self._image.width() * border_thickness_multiplier)
        return self._image.expand_canvas(new_height, new_width, self._params)


class DistortImageProcessor(BaseImageProcessor):
    def __init__(self, source_image: ImageABC, background_path, corners):
        self._image = source_image
        self._background_path = background_path
        self._corners = corners

    def modified_image(self) -> ImageABC:
        return self._image.distort(self._background_path, self._corners)
