import argparse
from math import ceil, floor
from os import linesep
import PIL.Image as Image
from img2txt.methods import THRESHOLD_METHODS, COLOR_METHODS
from img2txt.characters.brailleimage import BrailleImage


def hsv_to_rgb(h, s, v):
    """
    Convert HSV (Hue, Saturation, Value) to RGB (Red, Green, Blue).

    :param h: Hue (0-360)
    :type h: float
    :param s: Saturation (0-1)
    :type s: float
    :param v: Value (0-1)
    :type v: float
    :return: RGB tuple (Red, Green, Blue) in the range [0, 255]
    :rtype: Tuple[int, int, int]
    """
    h /= 360.0  # Normalize hue to the range [0, 1]
    hi = int(h * 6)  # Get the corresponding sector (0 to 5)

    f = h * 6 - hi  # Fractional part of h
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if hi == 0:
        return int(v * 255), int(t * 255), int(p * 255)
    elif hi == 1:
        return int(q * 255), int(v * 255), int(p * 255)
    elif hi == 2:
        return int(p * 255), int(v * 255), int(t * 255)
    elif hi == 3:
        return int(p * 255), int(q * 255), int(v * 255)
    elif hi == 4:
        return int(t * 255), int(p * 255), int(v * 255)
    else:  # hi == 5
        return int(v * 255), int(p * 255), int(q * 255)

def main():
    argparser = argparse.ArgumentParser(description="Convert image to text.")
    argparser.add_argument("--method", '-m', action="store", choices=THRESHOLD_METHODS.keys(), default="luminance", help="Select method to use to determine if a pixel should be included in the image.")
    argparser.add_argument("--tolerance", '-t', action="store", type=float, default=0.5, help="Tolerance limit for determinance method.")
    argparser.add_argument("--invert", '-i', action='store_true', help="Include this flag to invert the determinance method.")
    argparser.add_argument("--color", '-c', action="store", choices=COLOR_METHODS.keys(), default="none", help="Select color display method.")
    argparser.add_argument("--limit", '-l', action="store", type=int, default=None, help="Enforce character limit.")
    argparser.add_argument("--output", '-o', action="store", type=argparse.FileType("w", encoding="utf-8"), default="-", help="Output file.")
    argparser.add_argument("image", action="store", type=argparse.FileType("rb"))
    
    args = argparser.parse_args()

    if not args.limit is None:
        if args.limit <= 0:
            raise ValueError(f"Character limit must be > 0, not {args.limit}")
    tolerance_method = THRESHOLD_METHODS[args.method]
    printing_visitor = COLOR_METHODS[args.color]

    # Get image, and resize if necessary
    image = Image.open(args.image)
    width, height = image.size
    image_area = width * height
    original_character_count = ceil(image_area / 8)
    if args.limit and original_character_count > args.limit:
        scaling_ratio = ((args.limit * 8) / image_area)**0.5
        width = floor(width * scaling_ratio)
        height = floor(height * scaling_ratio)
        image = image.resize((width, height))
    image = image.convert('RGBA')

    # Create BrailleImage and write output.
    braille = BrailleImage.from_image(image, tolerance_method, tolerance = args.tolerance, invert = args.invert)
    result = braille.get_colored_text(printing_visitor)
    if args.color == "html":
        result = result.replace(linesep, '<br>')
    args.output.write(result)
    args.output.write(linesep)
    args.image.close()
    args.output.close()


if __name__ == "__main__":
    main()