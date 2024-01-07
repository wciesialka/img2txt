'''Package containing logic for selecting user-customizable various functions.

:author: Willow Ciesialka
'''

import img2txt.methods.threshold
import img2txt.methods.colors

THRESHOLD_METHODS = {}
THRESHOLD_METHODS["luminance"] = img2txt.methods.threshold.luminance_method
THRESHOLD_METHODS["lightness"] = img2txt.methods.threshold.lightness_method

COLOR_METHODS = {}
COLOR_METHODS["none"] = img2txt.methods.colors.PlaintextVisitor
COLOR_METHODS["4bitansi"] = img2txt.methods.colors.FourBitAnsiVisitor
COLOR_METHODS["8bitansi"] = img2txt.methods.colors.EightBitAnsiVisitor
COLOR_METHODS["truecoloransi"] = img2txt.methods.colors.TrueColorAnsiVisitor
COLOR_METHODS["html"] = img2txt.methods.colors.HTMLVisitor
