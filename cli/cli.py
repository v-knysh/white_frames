import argparse
import os

import logging
from frames.actions import ActionABC, get_action, actions

from frames.expand_canvas import ExpandCanvasParamsFactory
from frames.image import PilImage
from frames.image_processing import FV_BORDER_THICKNESS_MULTIPLIER, NotAnImageException

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
    default=FV_BORDER_THICKNESS_MULTIPLIER,
    dest='multiplier',
)

parser.add_argument(
    '-a', '--action_code',
    type=str,
    help='Choose target action_code',
    default='white_frame',
    choices=[action.code for action in actions],
)


def process_file(content_path, multiplier, action_code, destination=None):
    logger.info(f"processing file '{content_path}'")
    try:
        image = PilImage.open(content_path)
    except NotAnImageException:
        logger.warning(f"cannot process file {content_path}. it is not an image")
        return
    
    action: ActionABC = get_action(action_code)

    processor = action.processor(image)
    modified_image = processor.modified_image()
    if destination is None:
        file_name, file_extension = os.path.splitext(content_path)
        destination = f'{file_name}-square.{file_extension.replace(".", "")}'
    modified_image.save(destination)


def process_dir(content_path, multiplier, action_code):
    logger.info(f"processing dir '{content_path}'")
    result_dir_name = os.path.join(content_path, 'square_images')
    logger.info(f'putting results to {result_dir_name}')
    if not os.path.isdir(result_dir_name):
        os.mkdir(result_dir_name)
    for file in os.listdir(content_path):
        root_file = os.path.join(content_path, file)
        if os.path.isfile(root_file):
            process_file(root_file, multiplier, action_code, destination=os.path.join(result_dir_name, file))


def run_cli():
    args = parser.parse_args()
    content_path = args.path
    multiplier = args.multiplier
    action_code = args.action_code

    if os.path.isfile(content_path):
        process_file(content_path, multiplier, action_code)

    elif os.path.isdir(content_path):
        process_dir(content_path, multiplier, action_code)
