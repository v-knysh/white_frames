import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError, ExifTags, ImageDraw

from frames.image_processing import (
    ImageABC,
    ExpandCanvasParams,
    NotAnImageException
)


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

        orientation = exif.get(orientation_tag)

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
    
    def distort(self) -> 'ImageABC':
        background = Image.open("16400267487971.jpg")
        background = background.convert("RGBA")
        self._image = self._image.convert("RGBA")
        print(self._image)
        roi = ((0, 0), (self._image.width, self._image.height))
        output = Image.new('RGBA', (background.width, background.height), (255, 255, 255, 255))
        # output.paste(self._image, (0, 0))
        # output = Image.open("16400267487971.jpg")

        draw = ImageDraw.Draw(output)
        
        tl_dst = (550, 433)
        tr_dst = (864, 404)
        br_dst = (877, 644)
        bl_dst = (555, 622)

        draw.polygon([tl_dst, tr_dst, br_dst, bl_dst], outline=(0,0,0))
        # draw.polygon([tl_dst, tr_dst, br_dst, bl_dst])



        image_cv2 = np.array(self._image)
        output_cv2 = np.array(output)

        tl = (0, 0,)
        tr = (self._image.width, 0)
        br = (self._image.width, self._image.height)
        bl = (0, self._image.height)
        pts = np.array([bl, br, tr, tl])


        dst_pts = np.array([bl_dst, br_dst, tr_dst, tl_dst])

        pts = np.float32(pts.tolist())
        dst_pts = np.float32(dst_pts.tolist())
        print(pts, dst_pts)
        M = cv2.getPerspectiveTransform(pts, dst_pts)
        image_size = (output_cv2.shape[1], output_cv2.shape[0])
        warped = cv2.warpPerspective(image_cv2, M, dsize=image_size)

        # Get mask from quad in output image, and copy content from warped image
        gray = cv2.cvtColor(output_cv2, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)[1]
        cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        mask = np.zeros_like(output_cv2)
        mask = cv2.drawContours(mask, cnts, 0, (255, 255, 25, 255), cv2.FILLED)
        mask = mask.all(axis=2)
        import pprint
        pprint.pprint(image_cv2)
        
        output_cv2[mask, :] = warped[mask, :]
        pprint.pprint(output_cv2)

        output_cv2[:, :, 3] = (255 * (output_cv2[:, :, :3] != 255).any(axis=2)).astype(np.uint8)

        # Transform back to PIL images
        output_new = Image.fromarray(output_cv2)
        output2 = Image.new('RGBA', (background.width, background.height), (255, 255, 255, 0))
        output2.paste(background, (0, 0))
        output2.paste(output_new, (0, 0), output_new)

        output2 = output2.convert("RGBA")
        output2.save('final_output.png')
        output2 = output2.convert("RGB")

        return PilImage(output2)




    def save(self, filename):
        self._image.save(filename)