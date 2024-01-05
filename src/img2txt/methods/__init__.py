from typing import List, Tuple


def luminance_filter(pixels: List[Tuple[float, float, float]], *, tolerance: float = 0.5, invert: bool = False) -> List[Tuple[float, float, float]]:
    '''Filter a list of pixels

    :param pixels: _description_
    :type pixels: List[Tuple[float, float, float]]
    :param tolerance: _description_, defaults to 0.5
    :type tolerance: float, optional
    :param invert: _description_, defaults to False
    :type invert: bool, optional
    :raises ValueError: _description_
    :raises TypeError: _description_
    :return: _description_
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
