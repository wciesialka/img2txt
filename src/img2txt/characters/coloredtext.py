import img2txt.characters.colors as colors

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