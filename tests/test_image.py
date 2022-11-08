from frames.image_processing import ImageABC, ExpandCanvasParams


class TestImage(ImageABC):
    def __init__(self, height, width, **kwargs):
        self._height = height
        self._width = width

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def expand_canvas(self, new_height: int, new_width: int, params: ExpandCanvasParams) -> ImageABC:
        coord_h = params.coord_h(new_height)
        coord_w = params.coord_w(new_height)
        return ExpandedTestImage(new_height, new_width, coord_h, coord_w)

    def save(self, filename):
        pass

    def __repr__(self):
        return f"<TestImage height={self._height} width={self._width}>"


class ExpandedTestImage(TestImage):
    def __init__(self, height, width, coord_h, coord_w):
        super().__init__(height, width)
        self._height = height
        self._width = width
        self._coord_h = coord_h
        self._coord_w = coord_w

    def __repr__(self):
        return f"<ExpandedTestImage height={self._height} width={self._width} coord_h={self._coord_h} coord_w={self._coord_w}>"
