import argparse
import os

import logging

from expand_canvas import ExpandCanvasParamsFactory
from image import PilImage
from image_processing import FV_MULTIPLIER, NotAnImageException
from processors import ImageProcessorFactory

logger = logging.getLogger('')

parser = argparse.ArgumentParser(description="Adds white frame to image to make it suitable for _metavlad's instagram")

parser.add_argument(
    '-p', '--path',
    type=str,
    help='image file path',
    default='../',
    dest='path',
)

parser.add_argument(
    '-m', '--multiplier',
    type=float,
    help='percent size for porder',
    default=FV_MULTIPLIER,
    dest='multiplier',
)


def process_file(content_path, multiplier, destination=None):
    logger.info(f"processing file '{content_path}'")
    try:
        image = PilImage.open(content_path)
    except NotAnImageException:
        logger.warning(f"cannot process file {content_path}. it is not an image")
        return
    processor = ImageProcessorFactory(ExpandCanvasParamsFactory()).processor(image)
    image_with_frame = processor.image_with_frame(multiplier=multiplier)
    if destination is None:
        file_name, file_extension = os.path.splitext(content_path)
        destination = f'{file_name}-square.{file_extension}'
    image_with_frame.save(destination)


def process_dir(content_path, multiplier):
    logger.info(f"processing dir '{content_path}'")
    result_dir_name = os.path.join(content_path, 'square_images')
    logger.info(f'putting results to {result_dir_name}')
    if not os.path.isdir(result_dir_name):
        os.mkdir(result_dir_name)
    for file in os.listdir(content_path):
        root_file = os.path.join(content_path, file)
        if os.path.isfile(root_file):
            process_file(root_file, multiplier, destination=os.path.join(result_dir_name, file))



if __name__ == "__main__":
    args = parser.parse_args()
    content_path = args.path
    multiplier = args.multiplier

    if os.path.isfile(content_path):
        process_file(content_path, multiplier)

    elif os.path.isdir(content_path):
        process_dir(content_path, multiplier)
