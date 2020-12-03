from make_frame import ExpandCanvasParams, ImageABC, ExpandCanvasParamsFactoryABC, ExpandCanvasParamsType


class CenterExpandParams(ExpandCanvasParams):
    def __init__(self, source_image: ImageABC):
        self._image = source_image

    def coord_h(self, new_height) -> int:
        return int((new_height - self._image.height()) / 2)

    def coord_w(self, new_width) -> int:
        return int((new_width - self._image.width()) / 2)


class GoldenRatioParams(ExpandCanvasParams):
    GOLDEN_RATIO = (5**0.5 + 1) / 2

    def __init__(self, source_image: ImageABC):
        self._image = source_image

    def coord_h(self, new_height) -> int:
        return int((new_height - self._image.height()) * (self.GOLDEN_RATIO ** -2))

    def coord_w(self, new_width) -> int:
        return int((new_width - self._image.width()) / 2)


class ExpandCanvasParamsFactory(ExpandCanvasParamsFactoryABC):
    def params(self, image: ImageABC, param_type: ExpandCanvasParamsType) -> ExpandCanvasParams:
        if param_type == ExpandCanvasParamsType.GOLDEN_RATIO:
            return GoldenRatioParams(image)
        elif param_type == ExpandCanvasParamsType.CENTER:
            return CenterExpandParams(image)
        else:
            raise NotImplementedError
