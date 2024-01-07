'''Module containing the BrailleImage class.

:author: Willow Ciesialka'''

from __future__ import annotations
from math import ceil, floor
from typing import List, Tuple
from os import linesep
from PIL.Image import Image
from img2txt.characters.braillesegment import BrailleSegment, BrailleFlag
from img2txt.methods.colors import ColoredTextFormatter

ALPHA_TOLERANCE: int = 255//2

class BrailleImage:
    '''Representation of a Braille Image.'''
    def __init__(self, width: int, height: int):

        self.__width: int = width
        self.__height: int = height

        self.__segments: List[BrailleSegment] = \
            [BrailleSegment() for _ in range(self.char_width * self.char_height)]

    @classmethod
    def from_image(cls, img: Image, tolerance: float = 0.5, invert: bool = False, \
         method) -> BrailleImage:
        '''Return a BrailleImage constructed from an Image.
        :param img: Source image.
        :type img: Image
        :param tolerance: Luminance tolerance.
        :type tolerance: float
        :param method: Method used to calculate luminance.
        :returns: Constructed BrailleImage.
        :rtype: BrailleImage'''
        width, height = img.size
        braille = cls(width, height)

        for y in range(height):
            for x in range(width):
                red, green, blue, alpha = img.getpixel((x, y))
                if alpha >= ALPHA_TOLERANCE:
                    if method((red, green, blue), tolerance=tolerance, invert=invert):
                        braille.plot(x, y, (red, green, blue))

        return braille

    @property
    def width(self) -> int:
        '''Width of image.'''
        return self.__width

    @property
    def height(self) -> int:
        '''Height of image.'''
        return self.__height

    @property
    def char_width(self) -> int:
        '''Character width of image.'''
        return ceil(self.width / 2)

    @property
    def char_height(self) -> int:
        '''Character height of image.'''
        return ceil(self.__height / 4)

    def __get_segment(self, x: int, y: int) -> BrailleSegment:
        '''Get the segment specified by the x and y position.
        :param x: x position.
        :type x: int
        :param y: y position.
        :type y: int
        :returns: Braille Segment that occupies the position (x,y)
        :rtype: BrailleSegment
        :raises ValueError: ValueError raised if x < 0 or y < 0 or x > width or y > height
        '''
        if x < 0 or x > self.width:
            raise ValueError(f"x value \"{x}\" outside of bounds [0, {self.width}].")
        elif y < 0 or y > self.height:
            raise ValueError(f"y value \"{y}\" outside of bounds [0, {self.height}].")
        else:
            char_x = floor(x / 2)
            char_y = floor(y / 4)
            i = char_x + (char_y * self.char_width)
            return self.__segments[i]

    def plot(self, x: int, y: int, color: Tuple[int, int, int] = None, *, unplot: bool = False):
        '''Plots the "pixel" residing at (x, y).
        :param x: x-coordinate to plot at.
        :type x: int
        :param y: y-coordinate to plot at.
        :type y: int
        :param unplot: If True, the method will instead unplot the point residing at (x, y).\
             Default is False.
        :type unplot: bool'''
        segment = self.__get_segment(x, y)

        sub_x = x % 2
        sub_y = y % 4

        flag = BrailleFlag.get(sub_x, sub_y)

        if unplot:
            segment.unset_flag(flag)
        else:
            if color is None:
                raise ValueError("Cannot plot without setting color!")
            segment.set_flag(flag, color)
    
    def get_colored_text(self, formatter: ColoredTextFormatter) -> str:
        '''Return string representation of colored text.

        :param formatter: Appropriate formatter for display method.
        :type formatter: ColoredTextFormatter
        :return: String containing the formatted colored text.
        :rtype: str
        '''
        return_string = ""
        for i, segment in enumerate(self.__segments):
            if i > 0 and i % self.char_width == 0:
                return_string += linesep
            segment_text = segment.as_colored_text()
            return_string += formatter.format(segment_text)
        return return_string


    def __repr__(self):
        return f"BrailleImage({self.width}, {self.height}, list[BrailleSegment])"