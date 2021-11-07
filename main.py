#!/usr/bin/env python3

import AsciiDotter.BrailleImage as BrailleImage
import argparse
import AsciiDotter.Luminance as Luminance
from typing import TextIO, Callable, BinaryIO
import sys
from PIL import Image

def main(input_stream:BinaryIO, output_stream:TextIO, tolerance:float, method:Callable[[int,int,int],float]):
    '''Perform the main duties of the program. Namely, convert an image into it's braille art equivalent.
    
    :param input_stream: Binary Stream representing input image.
    :type input_stream: BinaryIO
    :param output_stream: Text stream to write to.
    :type output_stream: TextIO
    :param tolerance: Tolerance of luminance in range [0.0, 1.0].
    :type tolerance: float
    :param method: Method to calculate luminance. Should take in r, g, b as parameters and return a float in range [0.0, 1.0].
    :type method: Callable[[int,int,int], float]'''

    image = Image.open(input_stream).convert('RGBA')

    w,h = image.size
    braille = BrailleImage.BrailleImage(w, h)

    for y in range(h):
        for x in range(w):
            r, g, b, a = image.getpixel((x,y))
            if a > (255//2):
                lum = method(r,g,b)
                if lum >= tolerance:
                    braille.plot(x,y)
    
    output_stream.write(braille.as_str())
    
    
if __name__ == "__main__":

    methods = {"average": Luminance.calculate_average, "relative": Luminance.calculate_luminance, "value": Luminance.calculate_value, "weighted": Luminance.calculate_weighted}
    for k in [key for key in methods.keys()]: # this will let us add "shortcut" key-value pairs, i.e. copy the value of each key to a key that is the first letter of the key.
        methods[k[0]] = methods[k]            # we have to use list comprehension here because the .keys() function will throw an error due to it being manipulated in the for loop.
                                              # we pass these keys in as choices for the --method flag.

    parser = argparse.ArgumentParser(description="Turn an image into a similar rendition using Unicode Braille characters!")
    parser.add_argument("--output","-o",type=argparse.FileType("w"),default=sys.stdout,help="Output stream.")
    parser.add_argument("--tolerance","-t",type=float,default=0.5,help="Luminance tolerance level in range [0.0, 1.0].")
    parser.add_argument("--method","-m",type=str,choices=methods.keys(),default="relative",help="Which method to use for calculating luminance.")
    parser.add_argument("input", type=argparse.FileType("rb"), help="Input image.")
    args = parser.parse_args()

    stream = args.output
    tolerance = args.tolerance

    if(tolerance < 0 or tolerance > 1):
        raise ValueError(f"Tolerance of \"{tolerance}\" outside of range [0.0, 1.0]")
    
    method = methods[args.method]
    image_stream = args.input

    try:
        main(image_stream, stream, tolerance, method)
    finally:
        stream.close()
        image_stream.close()