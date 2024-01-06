'''Module containing functions for filtering lists of pixels to turn into text.

:author: Willow Ciesialka
'''

from typing import List, Tuple

def luminance_filter(pixels: List[Tuple[float, float, float]], *, tolerance: float = 0.5, invert: bool = False) -> List[Tuple[float, float, float]]:
    '''Filter a list of pixels by luminance.

    :param pixels: Pixels to filter.
    :type pixels: List[Tuple[float, float, float]]
    :param tolerance: Tolerance limit, defaults to 0.5
    :type tolerance: float, optional
    :param invert: Invert flag, defaults to False
    :type invert: bool, optional
    :raises ValueError: Tolerance filter is not [0.0, 1.0]
    :raises TypeError: Pixels are not a list.
    :return: Filtered pixels to look at.
    :rtype: List[Tuple[float, float, float]]
    '''
    if tolerance > 1 or tolerance < 0:
        raise ValueError("Tolerance filter must be between [0.0, 1.0].")
    if not isinstance(pixels, list):
        raise TypeError("Data to filter must be list.")

    # Pixel to look at will be on top.
    pixel = pixels[0]

    # If luminance is less (more if invert) than threshold, add to list.
    # Otherwise, add None. 
    luminance = ( .299 * (pixel[0]**2) + .587 * (pixel[1]**2) + .114 * (pixel[2]**2) )
    result = None
    if (luminance < tolerance) ^ invert:
        result = pixel

    if len(pixels) > 1:
        return [result] + luminance_filter(pixels[1:], tolerance=tolerance, invert=invert)
    return [result]