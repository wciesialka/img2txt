'''Module containing functionality for colored text.

:author: Willow Ciesialka'''

import img2txt.colors.colors as colors
from img2txt.colors.colordifference import find_nearest_color_neighbor

class ColoredText:

    __slots__ = ("__text", "__color")

    def __init__(self, text, color):
        self.text = text
        self.color = color
    
    @property
    def text(self):
        return self.__text
    
    @property
    def color(self):
        return self.__color
    
    @text.setter
    def text(self, new_text):
        if not isinstance(new_text, str):
            raise TypeError(f"Text should of type str, not type {new_text.__class__.__name__}.")
        self.__text = new_text
    
    @color.setter
    def color(self, new_color):
        if not isinstance(new_color, tuple):
            raise TypeError(f"color should of type tuple, not type {new_color.__class__.__name__}.")
        if len(new_color) != 3 or not isinstance(new_color[0], int) or not isinstance(new_color[1], int) or not isinstance(new_color[2], int):
            raise TypeError("color should be of type tuple[int, int, int].")
        if (new_color[0] < 0 or new_color[0] > 255) or (new_color[1] < 0 or new_color[1] > 255) or (new_color[2] < 0 or new_color[2] > 255):
            raise ValueError("color bands should be between 0-255.")
        self.__color = new_color
    
    def html(self) -> str:
        '''Get text representation in HTML

        :return: Text representation in HTML.
        :rtype: str
        '''
        # Find nearest named color
        name, _ = find_nearest_color_neighbor(self.color, colors.NAMED_COLORS)
        return f"<span style=\"color: {name};\">{self.text}</span>"
    
    def four_bit_ansi(self) -> str:
        '''Get text representation using four-bit ANSI.

        :return: Text representation in four-bit ANSI.
        :rtype: str
        '''
        # Find nearest four-bit ANSI color.
        index, _ = find_nearest_color_neighbor(self.color, [ansi.rgb for ansi in colors.FOUR_BIT_ANSI])
        return colors.FOUR_BIT_ANSI[index].fg() + self.text + colors.ANSI_RESET

    def eight_bit_ansi(self) -> str:
        '''Get text representation using eight-bit ANSI.

        :return: Text representation in eight-bit ANSI.
        :rtype: str
        '''
        index, _ = find_nearest_color_neighbor(self.color, [ansi.rgb for ansi in colors.EIGHT_BIT_ANSI])
        return colors.EIGHT_BIT_ANSI[index].fg() + self.text + colors.ANSI_RESET
    
    def true_color_ansi(self) -> str:
        '''Get text representation using "true-color" (24-bit) ANSI.

        :return: Text representaiton using true-color ANSI.
        :rtype: str
        '''
        ansi = colors.TrueColorAnsi(self.color)
        return ansi.fg() + self.text + colors.ANSI_RESET

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__text}, {self.__color})"

    def __str__(self) -> str:
        return self.text