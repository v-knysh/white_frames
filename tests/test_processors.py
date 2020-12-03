import unittest

from expand_canvas import ExpandCanvasParamsFactory
from test_image import TestImage
from processors import ImageProcessorFactory
from image_processing import fotovramke_default_height, fotovramke_default_width, fotovramke_result_width


class FotovramkeTestCase(unittest.TestCase):
    def test_landscape_success(self):
        image_processor_factory = ImageProcessorFactory(ExpandCanvasParamsFactory())
        processor = image_processor_factory.processor(TestImage(height=fotovramke_default_height, width=fotovramke_default_width))
        image_with_frame = processor.image_with_frame()
        print(self.id(), image_with_frame)
        self.assertEqual(image_with_frame.width(), fotovramke_result_width)
        self.assertEqual(image_with_frame.height(), fotovramke_result_width)

    def test_portrait_success(self):
        image_processor_factory = ImageProcessorFactory(ExpandCanvasParamsFactory())
        processor = image_processor_factory.processor(TestImage(width=fotovramke_default_height, height=fotovramke_default_width))
        image_with_frame = processor.image_with_frame()
        print(self.id(), image_with_frame)
        self.assertEqual(image_with_frame.width(), fotovramke_result_width)
        self.assertEqual(image_with_frame.height(), fotovramke_result_width)

    def test_square_success(self):
        image_processor_factory = ImageProcessorFactory(ExpandCanvasParamsFactory())
        processor = image_processor_factory.processor(TestImage(width=fotovramke_default_width, height=fotovramke_default_width))
        image_with_frame = processor.image_with_frame()
        print(self.id(), image_with_frame)
        self.assertEqual(image_with_frame.width(), fotovramke_result_width)
        self.assertEqual(image_with_frame.height(), fotovramke_result_width)

    def test_almost_square_success(self):
        image_processor_factory = ImageProcessorFactory(ExpandCanvasParamsFactory())

        test_image = TestImage(width=fotovramke_default_width, height=int(fotovramke_default_width * 0.99))

        processor = image_processor_factory.processor(test_image)
        image_with_frame = processor.image_with_frame()
        print(self.id(), image_with_frame)
        self.assertEqual(image_with_frame.width(), fotovramke_result_width)
        self.assertEqual(image_with_frame.height(), fotovramke_result_width)


class ColdenRatioTestCase(unittest.TestCase):
    def test_golden_ratio_landscape(self):
        image_processor_factory = ImageProcessorFactory(ExpandCanvasParamsFactory())
        image = TestImage(height=fotovramke_default_height, width=fotovramke_default_width)
        processor = image_processor_factory.processor(image)
        image_with_frame = processor.image_with_frame()
        self.assertAlmostEqual(image_with_frame._coord_h / 446, 1, places=2)

