import argparse
import os

import logging

from frames.image import PilImage
from frames.image_processing import NotAnImageException


parser = argparse.ArgumentParser(description="splits page into two by column delimiter coords")

parser.add_argument(
    '-p', '--path',
    type=str,
    help='image file path',
    default='../',
    dest='path',
)

logger = logging.getLogger('')


parser.add_argument(
    "-c1", "--column_1",
    type=int,
    help="left column coord",
                    default=0,
                    dest="c1"
                    )

parser.add_argument(
    "-c2", "--column_2",
                    type=int,
                    help="left column coord",
                    default=0,
                    dest="c2"
                    )


def process_file(content_path, c1, c2):
    logger.info(f"processing file '{content_path}'")
    try:
        image = PilImage.open(content_path)
    except NotAnImageException:
        logger.warning(f"cannot process file {content_path}. it is not an image")
        return
    
    file_name, file_extension = os.path.splitext(content_path)
    
    destination1 = f'{file_name}-1.{file_extension.replace(".", "")}'
    modified_image_1 = image.crop(0, 0, c1, image.height())
    modified_image_1.save(destination1)
    
    destination2 = f'{file_name}-2.{file_extension.replace(".", "")}'
    modified_image_2 = image.crop(c2, 0, image.width(), image.height())
    modified_image_2.save(destination2)
        

def process_dir(content_path, c1, c2):
    logger.info(f"processing dir '{content_path}'")
    result_dir_name = os.path.join(content_path, 'split_halves')
    logger.info(f'putting results to {result_dir_name}')
    if not os.path.isdir(result_dir_name):
        os.mkdir(result_dir_name)
    for file in os.listdir(content_path):
        root_file = os.path.join(content_path, file)
        if os.path.isfile(root_file):
            process_file(root_file, c1, c2)


def run_cli():
    args = parser.parse_args()
    content_path = args.path
    c1 = int(args.c1)
    c2 = int(args.c2)

    print(type(c1), c1)
    
    if os.path.isfile(content_path):
        process_file(content_path, c1, c2)

    elif os.path.isdir(content_path):
        process_dir(content_path, c1, c2)

if __name__ == "__main__":
    run_cli()