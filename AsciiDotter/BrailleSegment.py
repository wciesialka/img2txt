from enum import Enum

class BrailleFlag(Enum):
    '''Enum containing bit flags used in constructing Braille Unicode characters.'''

    A:int = 0x1
    B:int = 0x8
    C:int = 0x2
    D:int = 0x10
    E:int = 0x4
    F:int = 0x20
    G:int = 0x40
    H:int = 0x80

    @staticmethod
    def get(x:int, y:int):
        if x == 0:
            if y == 0:
                return BrailleFlag.A
            elif y == 1:
                return BrailleFlag.C
            elif y == 2:
                return BrailleFlag.E
            else:
                return BrailleFlag.G
        else:
            if y == 0:
                return BrailleFlag.B
            elif y == 1:
                return BrailleFlag.D
            elif y == 2:
                return BrailleFlag.F
            else:
                return BrailleFlag.H


class BrailleSegment:
    '''Class representing a 2x4 segment of a BrailleImage. Contains methods for setting and unsetting flags.'''

    def __init__(self):
        self.__flags:int = 0

    def as_char(self) -> str:
        '''Return the character representation of the Braille pattern in UTF-16/UTF-32 Encoding.
        
        :returns: A string containing the single character of the Braille Pattern in UTF-16/UTF-32 Encoding.
        :rtype: str'''
        # In UTF-16 and UTF-32 Encoding, the base Braille pattern is 0x2800.
        return chr(0x2800 + self.__flags)
    
    def __str__(self):
        
        return self.as_char()

    def __repr__(self):

        return f"BrailleSegment({hex(self.__flags)})"

    def set_flag(self,flag:BrailleFlag):
        '''Set the BrailleSegment flag.
        :param flag: Flag to set.
        :type flag: BrailleFlag
        '''
        self.__flags = self.__flags | flag.value

    def unset_flag(self,flag:BrailleFlag):
        '''Unset the BrailleSegment flag.
        :param flag: Flag to unset.
        :type flag: BrailleFlag
        '''
        self.__flags = self.__flags & (~flag.value)