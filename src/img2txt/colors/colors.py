'''Module containing common color constants.

:author: Willow Ciesialka'''

class FourBitAnsiColor:

    __slots__ = ("__fg_code", "__bg_code", "__rgb")

    def __init__(self, fg_code: int, bg_code:int, rgb: tuple):
        self.__fg_code = fg_code
        self.__bg_code = bg_code
        self.__rgb = rgb

    @property
    def bg_code(self):
        return self.__bg_code

    @property
    def fg_code(self):
        return self.__fg_code

    @property
    def rgb(self):
        return self.__rgb

    def fg(self):
        return f"\033[{self.fg_code}m"

    def bg(self):
        return f"\033[{self.bg_code}m"

ANSI_RESET = "\033[0m"

__FOUR_BIT_ANSI = [None] * 16
__FOUR_BIT_ANSI[0] = FourBitAnsiColor(30, 40, (0,0,0))
__FOUR_BIT_ANSI[1] = FourBitAnsiColor(31, 41, (170, 0, 0))
__FOUR_BIT_ANSI[2] = FourBitAnsiColor(32, 42, (0, 170, 0))
__FOUR_BIT_ANSI[3] = FourBitAnsiColor(33, 43, (128, 128, 0))
__FOUR_BIT_ANSI[4] = FourBitAnsiColor(34, 44, (0, 0, 170))
__FOUR_BIT_ANSI[5] = FourBitAnsiColor(35, 45, (170, 0, 170))
__FOUR_BIT_ANSI[6] = FourBitAnsiColor(36, 46, (0, 170, 170))
__FOUR_BIT_ANSI[7] = FourBitAnsiColor(37, 47, (170, 170, 170))
__FOUR_BIT_ANSI[8] = FourBitAnsiColor(90, 100, (85, 85, 85))
__FOUR_BIT_ANSI[9] = FourBitAnsiColor(91, 101, (255, 85, 85))
__FOUR_BIT_ANSI[10] = FourBitAnsiColor(92, 102, (85, 255, 85))
__FOUR_BIT_ANSI[11] = FourBitAnsiColor(93, 103, (255, 255, 85))
__FOUR_BIT_ANSI[12] = FourBitAnsiColor(94, 104, (85, 85, 255))
__FOUR_BIT_ANSI[13] = FourBitAnsiColor(95, 105, (255, 85, 255))
__FOUR_BIT_ANSI[14] = FourBitAnsiColor(96, 106, (85, 255, 255))
__FOUR_BIT_ANSI[15] = FourBitAnsiColor(97, 107, (255, 255, 255))
FOUR_BIT_ANSI = tuple(__FOUR_BIT_ANSI)

class EightBitAnsiColor:

    __slots__ = ("__code", "__rgb")

    def __init__(self, code, rgb):
        self.__code = code
        self.__rgb = rgb
    
    @property
    def code(self):
        return self.__code
    
    @property
    def rgb(self):
        return self.__rgb
    
    def fg(self):
        return f"\033[38;5;{self.code}m"
    
    def bg(self):
        return f"\033[48;5;{self.code}m"

__EIGHT_BIT_ANSI = [None] * 256
for i, value in enumerate(FOUR_BIT_ANSI):
    __EIGHT_BIT_ANSI[i] = value.rgb
for value in range(216):
    __red = (value & 0xE0) >> 5
    __green = (value & 0x1C) >> 2
    __blue = (value & 0x03)
    # scale
    __red = (__red * 255) // 7
    __green = (__green * 255) // 7
    __blue = (__blue * 255) // 3
    __EIGHT_BIT_ANSI[value + 16] = (__red, __green, __blue)
for value in range(24):
    __offset = 0xA * value
    __grayscale = (8 + __offset, 8 + __offset, 8 + __offset)
    __EIGHT_BIT_ANSI[value + 16 + 216] = __offset

EIGHT_BIT_ANSI = tuple(__EIGHT_BIT_ANSI)

class TrueColorAnsi:

    __slots__ = ("__rgb")

    def __init__(self, rgb):
        self.__rgb = rgb
    
    @property
    def rgb(self):
        return self.__rgb
    
    def fg(self):
        return f"\033[38;2;{self.rgb[0]};{self.rgb[1]};{self.rgb[2]}m"

    def bg(self):
        return f"\033[48;2;{self.rgb[0]};{self.rgb[1]};{self.rgb[2]}m"

# HTML named colors

NAMED_COLORS = {}
NAMED_COLORS["aliceblue"] = (0xf0, 0xf8, 0xff)
NAMED_COLORS["antiquewhite"] = (0xfa, 0xeb, 0xd7)
NAMED_COLORS["aqua"] = (0x00, 0xff, 0xff)
NAMED_COLORS["aquamarine"] = (0x7f, 0xff, 0xd4)
NAMED_COLORS["azure"] = (0xf0, 0xff, 0xff)
NAMED_COLORS["beige"] = (0xf5, 0xf5, 0xdc)
NAMED_COLORS["bisque"] = (0xff, 0xe4, 0xc4)
NAMED_COLORS["black"] = (0x00, 0x00, 0x00)
NAMED_COLORS["blanchedalmond"] = (0xff, 0xeb, 0xcd)
NAMED_COLORS["blue"] = (0x00, 0x00, 0xff)
NAMED_COLORS["blueviolet"] = (0x8a, 0x2b, 0xe2)
NAMED_COLORS["brown"] = (0xa5, 0x2a, 0x2a)
NAMED_COLORS["burlywood"] = (0xde, 0xb8, 0x87)
NAMED_COLORS["cadetblue"] = (0x5f, 0x9e, 0xa0)
NAMED_COLORS["chartreuse"] = (0x7f, 0xff, 0x00)
NAMED_COLORS["chocolate"] = (0xd2, 0x69, 0x1e)
NAMED_COLORS["coral"] = (0xff, 0x7f, 0x50)
NAMED_COLORS["cornflowerblue"] = (0x64, 0x95, 0xed)
NAMED_COLORS["cornsilk"] = (0xff, 0xf8, 0xdc)
NAMED_COLORS["crimson"] = (0xdc, 0x14, 0x3c)
NAMED_COLORS["cyan"] = (0x00, 0xff, 0xff)
NAMED_COLORS["darkblue"] = (0x00, 0x00, 0x8b)
NAMED_COLORS["darkcyan"] = (0x00, 0x8b, 0x8b)
NAMED_COLORS["darkgoldenrod"] = (0xb8, 0x86, 0x0b)
NAMED_COLORS["darkgray"] = (0xa9, 0xa9, 0xa9)
NAMED_COLORS["darkgreen"] = (0x00, 0x64, 0x00)
NAMED_COLORS["darkgrey"] = (0xa9, 0xa9, 0xa9)
NAMED_COLORS["darkkhaki"] = (0xbd, 0xb7, 0x6b)
NAMED_COLORS["darkmagenta"] = (0x8b, 0x00, 0x8b)
NAMED_COLORS["darkolivegreen"] = (0x55, 0x6b, 0x2f)
NAMED_COLORS["darkorange"] = (0xff, 0x8c, 0x00)
NAMED_COLORS["darkorchid"] = (0x99, 0x32, 0xcc)
NAMED_COLORS["darkred"] = (0x8b, 0x00, 0x00)
NAMED_COLORS["darksalmon"] = (0xe9, 0x96, 0x7a)
NAMED_COLORS["darkseagreen"] = (0x8f, 0xbc, 0x8f)
NAMED_COLORS["darkslateblue"] = (0x48, 0x3d, 0x8b)
NAMED_COLORS["darkslategray"] = (0x2f, 0x4f, 0x4f)
NAMED_COLORS["darkslategrey"] = (0x2f, 0x4f, 0x4f)
NAMED_COLORS["darkturquoise"] = (0x00, 0xce, 0xd1)
NAMED_COLORS["darkviolet"] = (0x94, 0x00, 0xd3)
NAMED_COLORS["deeppink"] = (0xff, 0x14, 0x93)
NAMED_COLORS["deepskyblue"] = (0x00, 0xbf, 0xff)
NAMED_COLORS["dimgray"] = (0x69, 0x69, 0x69)
NAMED_COLORS["dimgrey"] = (0x69, 0x69, 0x69)
NAMED_COLORS["dodgerblue"] = (0x1e, 0x90, 0xff)
NAMED_COLORS["firebrick"] = (0xb2, 0x22, 0x22)
NAMED_COLORS["floralwhite"] = (0xff, 0xfa, 0xf0)
NAMED_COLORS["forestgreen"] = (0x22, 0x8b, 0x22)
NAMED_COLORS["fuchsia"] = (0xff, 0x00, 0xff)
NAMED_COLORS["gainsboro"] = (0xdc, 0xdc, 0xdc)
NAMED_COLORS["ghostwhite"] = (0xf8, 0xf8, 0xff)
NAMED_COLORS["gold"] = (0xff, 0xd7, 0x00)
NAMED_COLORS["goldenrod"] = (0xda, 0xa5, 0x20)
NAMED_COLORS["gray"] = (0x80, 0x80, 0x80)
NAMED_COLORS["green"] = (0x00, 0x80, 0x00)
NAMED_COLORS["greenyellow"] = (0xad, 0xff, 0x2f)
NAMED_COLORS["grey"] = (0x80, 0x80, 0x80)
NAMED_COLORS["honeydew"] = (0xf0, 0xff, 0xf0)
NAMED_COLORS["hotpink"] = (0xff, 0x69, 0xb4)
NAMED_COLORS["indianred"] = (0xcd, 0x5c, 0x5c)
NAMED_COLORS["indigo"] = (0x4b, 0x00, 0x82)
NAMED_COLORS["ivory"] = (0xff, 0xff, 0xf0)
NAMED_COLORS["khaki"] = (0xf0, 0xe6, 0x8c)
NAMED_COLORS["lavender"] = (0xe6, 0xe6, 0xfa)
NAMED_COLORS["lavenderblush"] = (0xff, 0xf0, 0xf5)
NAMED_COLORS["lawngreen"] = (0x7c, 0xfc, 0x00)
NAMED_COLORS["lemonchiffon"] = (0xff, 0xfa, 0xcd)
NAMED_COLORS["lightblue"] = (0xad, 0xd8, 0xe6)
NAMED_COLORS["lightcoral"] = (0xf0, 0x80, 0x80)
NAMED_COLORS["lightcyan"] = (0xe0, 0xff, 0xff)
NAMED_COLORS["lightgoldenrodyellow"] = (0xfa, 0xfa, 0xd2)
NAMED_COLORS["lightgray"] = (0xd3, 0xd3, 0xd3)
NAMED_COLORS["lightgreen"] = (0x90, 0xee, 0x90)
NAMED_COLORS["lightgrey"] = (0xd3, 0xd3, 0xd3)
NAMED_COLORS["lightpink"] = (0xff, 0xb6, 0xc1)
NAMED_COLORS["lightsalmon"] = (0xff, 0xa0, 0x7a)
NAMED_COLORS["lightseagreen"] = (0x20, 0xb2, 0xaa)
NAMED_COLORS["lightskyblue"] = (0x87, 0xce, 0xfa)
NAMED_COLORS["lightslategray"] = (0x77, 0x88, 0x99)
NAMED_COLORS["lightslategrey"] = (0x77, 0x88, 0x99)
NAMED_COLORS["lightsteelblue"] = (0xb0, 0xc4, 0xde)
NAMED_COLORS["lightyellow"] = (0xff, 0xff, 0xe0)
NAMED_COLORS["lime"] = (0x00, 0xff, 0x00)
NAMED_COLORS["limegreen"] = (0x32, 0xcd, 0x32)
NAMED_COLORS["linen"] = (0xfa, 0xf0, 0xe6)
NAMED_COLORS["magenta"] = (0xff, 0x00, 0xff)
NAMED_COLORS["maroon"] = (0x80, 0x00, 0x00)
NAMED_COLORS["mediumaquamarine"] = (0x66, 0xcd, 0xaa)
NAMED_COLORS["mediumblue"] = (0x00, 0x00, 0xcd)
NAMED_COLORS["mediumorchid"] = (0xba, 0x55, 0xd3)
NAMED_COLORS["mediumpurple"] = (0x93, 0x70, 0xdb)
NAMED_COLORS["mediumseagreen"] = (0x3c, 0xb3, 0x71)
NAMED_COLORS["mediumslateblue"] = (0x7b, 0x68, 0xee)
NAMED_COLORS["mediumspringgreen"] = (0x00, 0xfa, 0x9a)
NAMED_COLORS["mediumturquoise"] = (0x48, 0xd1, 0xcc)
NAMED_COLORS["mediumvioletred"] = (0xc7, 0x15, 0x85)
NAMED_COLORS["midnightblue"] = (0x19, 0x19, 0x70)
NAMED_COLORS["mintcream"] = (0xf5, 0xff, 0xfa)
NAMED_COLORS["mistyrose"] = (0xff, 0xe4, 0xe1)
NAMED_COLORS["moccasin"] = (0xff, 0xe4, 0xb5)
NAMED_COLORS["navajowhite"] = (0xff, 0xde, 0xad)
NAMED_COLORS["navy"] = (0x00, 0x00, 0x80)
NAMED_COLORS["oldlace"] = (0xfd, 0xf5, 0xe6)
NAMED_COLORS["olive"] = (0x80, 0x80, 0x00)
NAMED_COLORS["olivedrab"] = (0x6b, 0x8e, 0x23)
NAMED_COLORS["orange"] = (0xff, 0xa5, 0x00)
NAMED_COLORS["orangered"] = (0xff, 0x45, 0x00)
NAMED_COLORS["orchid"] = (0xda, 0x70, 0xd6)
NAMED_COLORS["palegoldenrod"] = (0xee, 0xe8, 0xaa)
NAMED_COLORS["palegreen"] = (0x98, 0xfb, 0x98)
NAMED_COLORS["paleturquoise"] = (0xaf, 0xee, 0xee)
NAMED_COLORS["palevioletred"] = (0xdb, 0x70, 0x93)
NAMED_COLORS["papayawhip"] = (0xff, 0xef, 0xd5)
NAMED_COLORS["peachpuff"] = (0xff, 0xda, 0xb9)
NAMED_COLORS["peru"] = (0xcd, 0x85, 0x3f)
NAMED_COLORS["pink"] = (0xff, 0xc0, 0xcb)
NAMED_COLORS["plum"] = (0xdd, 0xa0, 0xdd)
NAMED_COLORS["powderblue"] = (0xb0, 0xe0, 0xe6)
NAMED_COLORS["purple"] = (0x80, 0x00, 0x80)
NAMED_COLORS["rebeccapurple"] = (0x66, 0x33, 0x99)
NAMED_COLORS["red"] = (0xff, 0x00, 0x00)
NAMED_COLORS["rosybrown"] = (0xbc, 0x8f, 0x8f)
NAMED_COLORS["royalblue"] = (0x41, 0x69, 0xe1)
NAMED_COLORS["saddlebrown"] = (0x8b, 0x45, 0x13)
NAMED_COLORS["salmon"] = (0xfa, 0x80, 0x72)
NAMED_COLORS["sandybrown"] = (0xf4, 0xa4, 0x60)
NAMED_COLORS["seagreen"] = (0x2e, 0x8b, 0x57)
NAMED_COLORS["seashell"] = (0xff, 0xf5, 0xee)
NAMED_COLORS["sienna"] = (0xa0, 0x52, 0x2d)
NAMED_COLORS["silver"] = (0xc0, 0xc0, 0xc0)
NAMED_COLORS["skyblue"] = (0x87, 0xce, 0xeb)
NAMED_COLORS["slateblue"] = (0x6a, 0x5a, 0xcd)
NAMED_COLORS["slategray"] = (0x70, 0x80, 0x90)
NAMED_COLORS["slategrey"] = (0x70, 0x80, 0x90)
NAMED_COLORS["snow"] = (0xff, 0xfa, 0xfa)
NAMED_COLORS["springgreen"] = (0x00, 0xff, 0x7f)
NAMED_COLORS["steelblue"] = (0x46, 0x82, 0xb4)
NAMED_COLORS["tan"] = (0xd2, 0xb4, 0x8c)
NAMED_COLORS["teal"] = (0x00, 0x80, 0x80)
NAMED_COLORS["thistle"] = (0xd8, 0xbf, 0xd8)
NAMED_COLORS["tomato"] = (0xff, 0x63, 0x47)
NAMED_COLORS["turquoise"] = (0x40, 0xe0, 0xd0)
NAMED_COLORS["violet"] = (0xee, 0x82, 0xee)
NAMED_COLORS["wheat"] = (0xf5, 0xde, 0xb3)
NAMED_COLORS["white"] = (0xff, 0xff, 0xff)
NAMED_COLORS["whitesmoke"] = (0xf5, 0xf5, 0xf5)
NAMED_COLORS["yellow"] = (0xff, 0xff, 0x00)
NAMED_COLORS["yellowgreen"] = (0x9a, 0xcd, 0x32)
NAMED_COLORS["black"] = (0x00, 0x00, 0x00)
NAMED_COLORS["silver"] = (0xc0, 0xc0, 0xc0)
NAMED_COLORS["gray"] = (0x80, 0x80, 0x80)
NAMED_COLORS["white"] = (0xff, 0xff, 0xff)
NAMED_COLORS["maroon"] = (0x80, 0x00, 0x00)
NAMED_COLORS["red"] = (0xff, 0x00, 0x00)
NAMED_COLORS["purple"] = (0x80, 0x00, 0x80)
NAMED_COLORS["fuchsia"] = (0xff, 0x00, 0xff)
NAMED_COLORS["green"] = (0x00, 0x80, 0x00)
NAMED_COLORS["lime"] = (0x00, 0xff, 0x00)
NAMED_COLORS["olive"] = (0x80, 0x80, 0x00)
NAMED_COLORS["yellow"] = (0xff, 0xff, 0x00)
NAMED_COLORS["navy"] = (0x00, 0x00, 0x80)
NAMED_COLORS["blue"] = (0x00, 0x00, 0xff)
NAMED_COLORS["teal"] = (0x00, 0x80, 0x80)
NAMED_COLORS["aqua"] = (0x00, 0xff, 0xff)
