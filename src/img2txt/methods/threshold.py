'''Module containing functions for filtering lists of pixels to turn into text.

:author: Willow Ciesialka
'''

from typing import Tuple
from img2txt.colors.colordifference import rgb_to_lab

def threshold_method(method):
    '''Decorator for threshold methods. Gets result of luminance and compares it
    to tolerance. Then, inverts if necessary.
    '''
    def threshold_method_decorator(*args, tolerance: float = 0.5, invert: bool = False, **kwargs):
        if tolerance > 1 or tolerance < 0:
            raise ValueError("tolerance must be between [0.0, 1.0].")
        value = method(*args, **kwargs)
        return bool((value < tolerance) ^ invert)
    return threshold_method_decorator

@threshold_method
def luminance_method(pixel: Tuple[int, int, int]) -> float:
    '''Get the luminance of the pixel.

    :param pixel: RGB to get luminance value from.
    :type pixel: Tuple[int, int, int]
    :return: Luminance value
    :rtype: float
    '''
    r = pixel[0] / 255.0
    g = pixel[1] / 255.0
    b = pixel[2] / 255.0
    # If luminance is less (more if invert) than threshold, add to list.
    # Otherwise, add None. 
    luminance = ( .299 * (r**2) + .587 * (g**2) + .114 * (b**2) )
    return luminance

@threshold_method
def lightness_method(pixel: Tuple[int, int, int]) -> float:
    '''Get the perceptual lightness of the pixel.

    :param pixel: RGB values of pixel.
    :type pixel: Tuple[int, int, int]
    :return: Perceptual lightness of pixel.
    :rtype: float
    '''
    lab = rgb_to_lab(pixel)
    lightness = lab[0] / 100.0
    return lightness