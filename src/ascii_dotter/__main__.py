#!/usr/bin/env python3
'''Command-line interface of the package.'''''

import argparse
from typing import TextIO, BinaryIO
import sys
from math import ceil, floor, sqrt
from PIL import Image
import ascii_dotter.braille_image as braille_image
import ascii_dotter.luminance as luminance


def main(input_stream: BinaryIO, output_stream: TextIO, tolerance: float, \
    method: luminance.LuminanceMethod, inverted: bool, character_limit: int):
    '''Perform the main duties of the program. Namely, convert an image\
         into it's braille art equivalent.
    :param input_stream: Binary Stream representing input image.
    :type input_stream: BinaryIO
    :param output_stream: Text stream to write to.
    :type output_stream: TextIO
    :param tolerance: Tolerance of luminance in range [0.0, 1.0].
    :type tolerance: float
    :param method: Method to calculate luminance.
    :type method: LuminanceMethod
    :param inverted: If true, output image will be inverted.
    :type inverted: bool
    :param character_limit: Maximum character limit.
    :type character_limit: int'''

    image = Image.open(input_stream).convert('RGBA')

    width, height = image.size
    char_width = ceil(width/2)
    char_height = ceil(height/4)
    c_size = (char_width*char_height) + (char_height-1)
    # add character height to account for newlines

    if c_size > character_limit:
        percentage = character_limit/c_size
        ratio = sqrt(percentage)
        width = floor(width * ratio)
        height = floor(height * ratio)
        image = image.resize((width, height))
    braille = braille_image.BrailleImage.from_image(image, tolerance, method)
    if inverted:
        braille.invert()
    output_stream.write(braille.as_str())
    output_stream.flush()


def cli_entry_point():
    '''Read and parse arguments, then pass them into main()'''
    methods = luminance.LuminanceMethod._member_map_.copy()
    # Gets the name-value pairs of the Enum and copies it into a new dict.

    # this will let us add "shortcut" key-value pairs,
    # i.e. copy the value of each key to a key that is the first letter of the key.
    # we have to use list comprehension here because the .keys() function will throw an
    # error due to it being manipulated in the for loop.
    # we pass these keys in as choices for the --method flag.
    for k in list(methods.keys()):
        methods[k[0]] = methods[k]

    parser = argparse.ArgumentParser(prog="asciidotter", \
        description="Turn an image into a similar rendition using Unicode Braille characters!")
    parser.add_argument("--output", "-o", type=argparse.FileType("w"), \
        default=sys.stdout, help="Output stream.")
    parser.add_argument("--tolerance", "-t", type=float, default=0.5, \
        help="Luminance tolerance level in range [0.0, 1.0].")
    parser.add_argument("--method", "-m", type=str.upper, choices=methods.keys(), \
        default="AVERAGE", help="Which method to use for calculating luminance.")
    parser.add_argument("--invert", "-i", action="store_true", help="Invert output image.")
    parser.add_argument("--limit", "-l", type=int, default=1048576, help="Character limit.")
    parser.add_argument("input", type=argparse.FileType("rb"), help="Input image.")
    args = parser.parse_args()

    stream = args.output
    tolerance = args.tolerance
    character_limit = args.limit

    if tolerance < 0 or tolerance > 1:
        raise ValueError(f"Tolerance of \"{tolerance}\" outside of range [0.0, 1.0]")
    if character_limit <= 0:
        raise ValueError("Character Limit cannot be less than or equal to 0.")

    method = methods[args.method]
    image_stream = args.input
    inverted = args.invert

    try:
        main(image_stream, stream, tolerance, method, inverted, character_limit)
    finally:
        stream.close()
        image_stream.close()

if __name__ == "__main__":
    cli_entry_point()
