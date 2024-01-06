'''Package containing logic for selecting user-customizable various functions.

:author: Willow Ciesialka
'''

import img2txt.methods.threshold as threshold
import img2txt.methods.colors as colors

THRESHOLD_METHODS = {}
THRESHOLD_METHODS["luminance_filter"] = threshold.luminance_filter

COLOR_METHODS = {"none": None}