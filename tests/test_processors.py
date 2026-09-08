import unittest

from tests.test_image import TestImage
from frames.actions import WhiteFrameAction
from frames.image_processing import fotovramke_default_height, fotovramke_default_width, fotovramke_result_width


class FotovramkeTestCase(unittest.TestCase):
    def test_landscape_success(self):
        processor = WhiteFrameAction().processor(TestImage(height=fotovramke_default_height, width=fotovramke_default_width))
        image_with_frame = processor.modified_image()
        print(self.id(), image_with_frame)
        self.assertEqual(image_with_frame.width(), fotovramke_result_width)
        self.assertEqual(image_with_frame.height(), fotovramke_result_width)

    def test_portrait_success(self):
        processor = WhiteFrameAction().processor(TestImage(width=fotovramke_default_height, height=fotovramke_default_width))
        image_with_frame = processor.modified_image()
        print(self.id(), image_with_frame)
        self.assertEqual(image_with_frame.width(), fotovramke_result_width)
        self.assertEqual(image_with_frame.height(), fotovramke_result_width)

    def test_square_success(self):
        processor = WhiteFrameAction().processor(TestImage(width=fotovramke_default_width, height=fotovramke_default_width))
        image_with_frame = processor.modified_image()
        print(self.id(), image_with_frame)
        self.assertEqual(image_with_frame.width(), fotovramke_result_width)
        self.assertEqual(image_with_frame.height(), fotovramke_result_width)

    def test_almost_square_success(self):
        test_image = TestImage(width=fotovramke_default_width, height=int(fotovramke_default_width * 0.99))

        processor = WhiteFrameAction().processor(test_image)
        image_with_frame = processor.modified_image()
        print(self.id(), image_with_frame)
        self.assertEqual(image_with_frame.width(), fotovramke_result_width)
        self.assertEqual(image_with_frame.height(), fotovramke_result_width)


class GoldenRatioTestCase(unittest.TestCase):
    def test_golden_ratio_landscape(self):
        image = TestImage(height=fotovramke_default_height, width=fotovramke_default_width)
        processor = WhiteFrameAction().processor(image)
        image_with_frame = processor.modified_image()
        self.assertAlmostEqual(image_with_frame._coord_h / 446, 1, places=2)

