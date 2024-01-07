'''
Module containing BrailleFlag and BrailleSegment classes.

:author: Willow Ciesialka
'''

from __future__ import annotations
from enum import Enum
from typing import Tuple
from img2txt.characters.coloredtext import ColoredText

class BrailleFlag(Enum):
    '''Enum containing bit flags used in constructing Braille Unicode characters.'''

    A: int = 0x1
    B: int = 0x8
    C: int = 0x2
    D: int = 0x10
    E: int = 0x4
    F: int = 0x20
    G: int = 0x40
    H: int = 0x80

    @staticmethod
    def get(segment_x: int, segment_y: int) -> BrailleFlag:
        '''Get the flag corresponding to the segment x and y.
        :param segment_x: '''
        if segment_x == 0:
            if segment_y == 0:
                return BrailleFlag.A
            elif segment_y == 1:
                return BrailleFlag.C
            elif segment_y == 2:
                return BrailleFlag.E
            return BrailleFlag.G
        if segment_y == 0:
            return BrailleFlag.B
        elif segment_y == 1:
            return BrailleFlag.D
        elif segment_y == 2:
            return BrailleFlag.F
        return BrailleFlag.H


class BrailleSegment:
    '''Class representing a 2x4 segment of a BrailleImage.
    Contains methods for setting and unsetting flags.'''

    __slots__ = ('__flags', '__colors')

    def __init__(self):
        self.__flags: int = 0
        self.__colors = {enumeration.value: None for enumeration in BrailleFlag}

    def as_char(self) -> str:
        '''Return the character representation of the Braille pattern in UTF-16/UTF-32 Encoding.
        :returns: A string containing the Braille Pattern.
        :rtype: str'''
        # In UTF-16 and UTF-32 Encoding, the base Braille pattern is 0x2800.
        return chr(0x2800 + self.__flags)

    def get_color(self) -> Tuple[int, int, int]:
        '''Get the average color of the components.

        :return: Average color of every bit in the segment.
        :rtype: Tuple[int, int, int]
        '''
        total_red = 0
        total_green = 0 
        total_blue = 0
        total_segments = 0
        for bit, color in self.__colors.items():
            if color is None:
                continue
            total_red += color[0]
            total_green += color[1]
            total_blue += color[2]
            total_segments += 1
        return (total_red // total_segments, total_green // total_segments, total_blue // total_segments)

    def as_colored_text(self) -> ColoredText:
        '''Return the ColoredText representation of this character.

        :return: Text with the character representation and average color of the segment.
        :rtype: ColoredText
        '''
        return ColoredText(self.as_char(), self.get_color())

    def __str__(self):
        return self.as_char()

    def __repr__(self):
        return f"BrailleSegment({hex(self.__flags)})"

    def copy(self) -> BrailleSegment:
        '''Return a copy of the BrailleSegment.'''
        new_copy = BrailleSegment()
        new_copy.__flags = self.__flags
        return new_copy

    def fill(self, color: Tuple[int, int, int]):
        '''Completely fill the BrailleSegment.
        :param color: Color to fill.
        :type color: Tuple[int, int, int]'''
        self.__flags = 0xFF
        for bit in self.__colors:
            self.__colors[bit] = color

    def set_flag(self, flag: BrailleFlag, color: Tuple[int, int, int]):
        '''Set the BrailleSegment flag.
        :param flag: Flag to set.
        :type flag: BrailleFlag
        '''
        self.__flags = self.__flags | flag.value
        self.__colors[flag.value] = color

    def unset_flag(self, flag: BrailleFlag):
        '''Unset the BrailleSegment flag.
        :param flag: Flag to unset.
        :type flag: BrailleFlag
        '''
        self.__flags = self.__flags & (~flag.value)
        self.__colors[flag.value] = None

    def flag_is_set(self, flag: BrailleFlag) -> bool:
        '''Return if the BrailleSegment flag is set.
        :param flag: Flag to check.
        :type flag: BrailleFlag
        :returns: True if flag is set, False otherwise.
        :rtype: bool'''
        return self.__flags & flag.value == flag.value
