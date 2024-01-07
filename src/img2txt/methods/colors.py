'''Module containing methods of representing color, if enabled.

:author: Willow Ciesialka
'''

from abc import abstractmethod
from img2txt.characters.coloredtext import ColoredText

class ColoredTextFormatter:

    @staticmethod
    @abstractmethod
    def _visit(colored_text: ColoredText):
        pass

    @classmethod
    def format(cls, colored_text: ColoredText) -> str:
        if not isinstance(colored_text, ColoredText):
            raise TypeError(f"colored_text should be of type ColoredText, not type {colored_text.__class__.__name__}")
        cls._visit(colored_text)

class FourBitAnsiFormatter(ColoredTextFormatter):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.four_bit_ansi()

class EightBitAnsiFormatter(ColoredTextFormatter):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.eight_bit_ansi()

class TrueColorAnsiFormatter(ColoredTextFormatter):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.true_color_ansi()

class HTMLFormatter(ColoredTextFormatter):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.html()

class PlaintextFormatter(ColoredTextFormatter):

    @staticmethod
    def _visit(colored_text: ColoredText):
        return colored_text.text