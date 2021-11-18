import AsciiDotter.BrailleSegment as BrailleSegment
from math import ceil, floor
from typing import List
from PIL import Image
from AsciiDotter.Luminance import LuminanceMethod

class BrailleImage:

    def __init__(self,width:int,height:int):

        self.__width:int = width
        self.__height:int = height

        self.__segments:List[BrailleSegment.BrailleSegment] = [BrailleSegment.BrailleSegment() for _ in range(self.char_width * self.char_height)]

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def char_width(self) -> int:
        return ceil(self.width / 2)

    @property
    def char_height(self) -> int:
        return ceil(self.__height / 4)

    def __get_segment(self, x:int, y:int) -> BrailleSegment.BrailleSegment:
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
            cx = floor(x / 2)
            cy = floor(y / 4)
            i = cx + (cy * self.char_width)
            return self.__segments[i]

    def fill(self):
        '''Fill the canvas.'''
        for segment in self.__segments:
            segment.fill()

    def invert(self):
        '''Invert the canvas.'''
        for segment in self.__segments:
            segment.invert()

    def plot(self, x:int, y:int, *, unplot:bool = False):
        '''Plots the "pixel" residing at (x,y).
        
        :param x: x-coordinate to plot at.
        :type x: int
        :param y: y-coordinate to plot at.
        :type y: int
        :param unplot: If True, the method will instead unplot the point residing at (x,y). Default is False.
        :type unplot: bool'''
 
        segment = self.__get_segment(x,y)

        subx = x % 2
        suby = y % 4

        flag = BrailleSegment.BrailleFlag.get(subx,suby)   

        if unplot:
            segment.unset_flag(flag)
        else:
            segment.set_flag(flag)

    def __repr__(self):
        return f"BrailleImage({self.width},{self.height},list[BrailleSegment])"

    def as_str(self) -> str:
        '''Depict image as string.
        
        :returns: The complete image.
        :rtype: str'''
        s = ""
        for i,segment in enumerate(self.__segments):
            if(i > 0 and i % self.char_width == 0):
                s += "\n"
            s += segment.as_char()
        return s


    def __str__(self):
        return self.as_str()