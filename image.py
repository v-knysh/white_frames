from make_frame import ImageABC, ExpandCanvasParams


class TestImage(ImageABC):
    def __init__(self, height, width):
        self._height = height
        self._width = width

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def expand_canvas(self, new_height: int, new_width: int, params: ExpandCanvasParams) -> ImageABC:
        return TestImage(new_height, new_width)

    def save(self):
        pass