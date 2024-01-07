'''Package containing logic for selecting user-customizable various functions.

:author: Willow Ciesialka
'''

import img2txt.methods.threshold as __threshold
import img2txt.methods.colors as __colors

THRESHOLD_METHODS = {}
THRESHOLD_METHODS["luminance"] = __threshold.luminance_method
THRESHOLD_METHODS["lightness"] = __threshold.lightness_method

COLOR_METHODS = {}
COLOR_METHODS["none"] = __colors.PlaintextFormatter
COLOR_METHODS["4bitansi"] = __colors.FourBitAnsiFormatter
COLOR_METHODS["8bitansi"] = __colors.EightBitAnsiFormatter
COLOR_METHODS["truecoloransi"] = __colors.TrueColorAnsiFormatter
COLOR_METHODS["html"] = __colors.HTMLFormatter
