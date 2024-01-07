'''Module containing methods of representing color, if enabled.

:author: Willow Ciesialka
'''

from abc import abstractmethod
from img2txt.characters.coloredtext import ColoredText

class ColoredTextVisitor:

    @staticmethod
    @abstractmethod
    def _visit(colored_text: ColoredText):
        pass

    @classmethod
    def print(cls, colored_text: ColoredText):
        if not isinstance(colored_text, ColoredText):
            raise TypeError(f"colored_text should be of type ColoredText, not type {colored_text.__class__.__name__}")
        cls._visit(colored_text)

class FourBitAnsiVisitor(ColoredTextVisitor):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.four_bit_ansi()

class EightBitAnsiVisitor(ColoredTextVisitor):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.eight_bit_ansi()

class TrueColorAnsiVisitor(ColoredTextVisitor):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.true_color_ansi()

class HTMLVisitor(ColoredTextVisitor):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.html()

class PlaintextVisitor(ColoredTextVisitor):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.text