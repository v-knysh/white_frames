from PIL import Image, UnidentifiedImageError, ExifTags

from image_processing import ImageABC, ExpandCanvasParams, NotAnImageException


class PilImage(ImageABC):
    def __init__(self, image: Image.Image):
        self._image = image

    @classmethod
    def open(cls, filename):
        try:
            image = Image.open(filename)
        except UnidentifiedImageError:
            raise NotAnImageException()

        image = cls.apply_tagged_rotation(image)

        return cls(image)

    @classmethod
    def apply_tagged_rotation(cls, image):
        if not hasattr(image, '_getexif'):  # only present in JPEGs
            return image

        orientation_tag = cls._exif_orientation_tag()

        exif = image._getexif()  # returns None if no EXIF data
        if exif is None:
            return image

        orientation = exif[orientation_tag]

        if orientation == 3:
            image = image.transpose(Image.ROTATE_180)
        elif orientation == 6:
            image = image.transpose(Image.ROTATE_270)
        elif orientation == 8:
            image = image.transpose(Image.ROTATE_90)
        return image

    @classmethod
    def _exif_orientation_tag(cls):
        orientation = None
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        return orientation

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