'''Package containing logic for selecting user-customizable various functions.

:author: Willow Ciesialka
'''

import img2txt.methods.threshold as threshold_methods
import img2txt.methods.colors as color_methods

THRESHOLD_METHODS = {}
THRESHOLD_METHODS["luminance"] = threshold_methods.luminance_method
THRESHOLD_METHODS["lightness"] = threshold_methods.lightness_method

COLOR_METHODS = {}
COLOR_METHODS["none"] = color_methods.PlaintextVisitor
COLOR_METHODS["4bitansi"] = color_methods.FourBitAnsiVisitor
COLOR_METHODS["8bitansi"] = color_methods.EightBitAnsiVisitor
COLOR_METHODS["truecoloransi"] = color_methods.TrueColorAnsiVisitor
COLOR_METHODS["html"] = color_methods.HTMLVisitor