from PIL import Image

from make_frame import ImageABC, ExpandCanvasParams


class PilImage(ImageABC):
    def __init__(self, image: Image.Image):
        self._image = image

    @classmethod
    def open(cls, filename):
        return cls(Image.open(filename))

    def width(self) -> int:
        return self._image.width

    def height(self) -> int:
        return self._image.height

    def expand_canvas(self, new_height: int, new_width: int, params: ExpandCanvasParams) -> 'ImageABC':
        new_image = Image.new(self._image.mode, (new_width, new_height), (255,255,255))
        coord_h = params.coord_h(new_height)
        coord_w = params.coord_w(new_height)
        new_image.paste(self._image, (coord_w, coord_h))
        return PilImage(new_image)

    def save(self, filename):
        self._image.save(filename)