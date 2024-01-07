'''Module useful for determining differences between colors.

:author: Willow Ciesialka
'''

from typing import Tuple, Dict, List, Any
from math import atan2, radians, cos, sin, exp, inf, degrees

def rgb_to_xyz(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    '''Convert a color in RGB space to XYZ space

    :param rgb: Color in RGB space with each band in [0, 255]
    :type rgb: Tuple[int, int, int]
    :return: _description_
    :rtype: Tuple[float, float, float]
    '''
    # Normalize to [0.0, 1.0]
    r = float(rgb[0]) / 255.0
    g = float(rgb[1]) / 255.0
    b = float(rgb[2]) / 255.0

    # Apply gamma correction if needed
    r = (r / 12.92) if (r <= 0.04045) else ((r + 0.055) / 1.055) ** 2.4
    g = (g / 12.92) if (g <= 0.04045) else ((g + 0.055) / 1.055) ** 2.4
    b = (b / 12.92) if (b <= 0.04045) else ((b + 0.055) / 1.055) ** 2.4

    # Apply the RGB to XYZ conversion matrix
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    return (x * 100.0, y * 100.0, z * 100.0)

    return (x, y, z)

def xyz_to_lab(xyz: Tuple[float, float, float]) -> Tuple[float, float, float]:
    '''Convert a color in XYZ colorspace to L*ab colorspace.

    :param xyz: Color in XYZ colorspace
    :type xyz: Tuple[float, float, float]
    :return: Color in L*ab colorspace
    :rtype: Tuple[float, float, float]
    '''
    x = xyz[0] / 95.047
    y = xyz[1] / 100.000
    z = xyz[2] / 108.883

    # Apply the XYZ to LAB conversion
    x = x if x > 0.008856 else (903.3 * x + 16.0) / 116.0
    y = y if y > 0.008856 else (903.3 * y + 16.0) / 116.0
    z = z if z > 0.008856 else (903.3 * z + 16.0) / 116.0

    l = max(0.0, 116.0 * y - 16.0)
    a = (x - y) * 500.0
    b = (y - z) * 200.0

    return (l, a, b)

def rgb_to_lab(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    '''Convert a color in RGB space to L*ab space.

    :param rgb: Color in RGB colorspace.
    :type rgb: Tuple[int, int, int]
    :return: Color in L*ab colorspace.
    :rtype: Tuple[float, float, float]
    '''
    xyz = rgb_to_xyz(rgb)
    lab = xyz_to_lab(xyz)
    return lab

def ciede2000(lab_1: Tuple[float, float, float], lab_2: Tuple[float, float, float]) -> float:
    '''Get the distance between two colors utilizing the CIEDE2000 method.

    :param lab_1: First color in L*ab space.
    :type lab_1: Tuple[float, float, float]
    :param lab_2: Second color in L*ab space.
    :type lab_2: Tuple[float, float, float]
    :return: Distance between the colors.
    :rtype: float
    '''
    # Constants
    K_H = 1.0
    K_C = 1.0
    K_L = 1.0

    # Arithmetic!
    L_Hat_Prime = (lab_1[0] + lab_2[0])/2.0
    C_1 = (lab_1[1]**2 + lab_1[2]**2)**0.5
    C_2 = (lab_2[1]**2 + lab_2[2]**2)**0.5
    C_Hat = (C_1 + C_2)/2.0
    G = 0.5*(1 - ((C_Hat ** 7)/((C_Hat**7) + (25**7)))**0.5)
    a_1_Prime = lab_1[1] * (1+G)
    a_2_Prime = lab_2[1] * (1+G)
    C_1_Prime = (a_1_Prime**2 + lab_1[2]**2)**0.5
    C_2_Prime = (a_2_Prime**2 + lab_2[2]**2)**0.5
    C_Hat_Prime = (C_1_Prime + C_2_Prime)/2.0
    h_1_Prime = degrees(atan2(lab_1[2], a_1_Prime))
    if h_1_Prime >= 0:
        h_1_Prime += 360.0
    h_2_Prime = degrees(atan2(lab_2[2], a_2_Prime))
    if h_2_Prime >= 0:
        h_2_Prime += 360.0
    H_Hat_Prime = (h_1_Prime + h_2_Prime)/2.0
    if abs(h_1_Prime - h_2_Prime) > 180.0:
        H_Hat_Prime = (h_1_Prime + h_2_Prime + 360)/2.0
    T = 1.0 - 0.17*cos(radians(H_Hat_Prime - 30)) + 0.24*cos(radians(2*H_Hat_Prime)) + 0.32*cos(radians(3*H_Hat_Prime + 6)) - 0.20*cos(radians(4*H_Hat_Prime - 63))

    condition = abs(h_2_Prime - h_1_Prime)
    delta_h_Prime = None
    if condition <= 180:
        delta_h_Prime = h_2_Prime - h_1_Prime
    elif condition > 180 and h_2_Prime <= h_1_Prime:
        delta_h_Prime = h_2_Prime - h_1_Prime + 360
    else:
        delta_h_Prime = h_2_Prime - h_1_Prime - 360
    
    delta_L_Prime = lab_2[0] - lab_1[0]
    delta_C_Prime = C_2_Prime - C_1_Prime
    delta_H_Prime = 2 * (C_1_Prime*C_2_Prime)**0.5 * sin(radians(delta_h_Prime/2))
    S_L = 1.0 + (0.015 * (L_Hat_Prime - 50)**2)/((20+(L_Hat_Prime - 50)**2)**0.5)
    S_C = 1.0 + 0.045 * C_Hat_Prime
    S_H = 1.0 + 0.015*C_Hat_Prime*T
    delta_theta = 30*exp(radians(-((H_Hat_Prime-275)/25)**2))
    R_C = 2.0 * ((C_Hat_Prime**7)/(C_Hat_Prime**7 + 25**7))
    R_T = (0.0-R_C)*sin(radians(2*delta_theta))
    
    # Put it all together!
    delta_E_a = (delta_L_Prime / (K_L*S_L))**2
    delta_E_b = (delta_C_Prime / (K_C*S_C))**2
    delta_E_c = (delta_H_Prime / (K_H*S_H))**2
    delta_E_d = R_T * (delta_C_Prime / (K_C * S_C)) * (delta_H_Prime / (K_H * S_H))
    delta_E = (delta_E_a + delta_E_b + delta_E_c + delta_E_d)**0.5
    return min(100.0, max(0.0, delta_E))

def redmean(rgb_1: Tuple[int, int, int], rgb_2: Tuple[int, int, int]) -> float:
    '''Return the euclidean difference between two colors in RGB colorspace using the redmean method.

    :param rgb_1: First color in RGB colorspace.
    :type rgb_1: Tuple[int, int, int]
    :param rgb_2: Second color in RGB colorspace.
    :type rgb_2: Tuple[int, int, int]
    :return: Color difference.
    :rtype: float
    '''
    r_bar = (rgb_1[0] + rgb_2[0])/2
    delta_r = (rgb_2[0] - rgb_1[0])**2
    delta_g = (rgb_2[1] - rgb_2[1])**2
    delta_b = (rgb_2[2] - rgb_2[2])**2

    return ( (2+r_bar/256)*delta_r + 4*delta_g + (2 + (255-r_bar)/256) * delta_b ) ** 0.5


difference_lookup = {}

def color_difference(rgb_1: Tuple[int, int, int], rgb_2: Tuple[int, int, int]) -> float:
    '''Return the difference between two colors in RGB colorspace.

    :param rgb_1: First color in RGB colorspace.
    :type rgb_1: Tuple[int, int, int]
    :param rgb_2: Second color in RGB colorspace.
    :type rgb_2: Tuple[int, int, int]
    :return: Color difference.
    :rtype: float
    '''
    # Check in lookup table first.
    hash_1 = rgb_1[0] << 16 | rgb_1[1] << 8 | rgb_1[2]
    hash_2 = rgb_2[0] << 16 | rgb_2[1] << 8 | rgb_2[2]
    if hash_1 == hash_2:
        # Exact match!
        return 0
    lookup_a = min(hash_1, hash_2)
    lookup_b = max(hash_1, hash_2)
    if lookup_a in difference_lookup:
        if lookup_b in difference_lookup[lookup_a]:
            return difference_lookup[lookup_a][lookup_b]
    else:
        difference_lookup[lookup_a] = {}

    lab_1 = rgb_to_lab(rgb_1)
    lab_2 = rgb_to_lab(rgb_2)
    c_diff = ciede2000(lab_1, lab_2)
    # c_diff = redmean(rgb_1, rgb_2)
    difference_lookup[lookup_a][lookup_b] = c_diff
    return c_diff

def find_nearest_color_neighbor(color: Tuple[int, int, int], population: Tuple | List | Dict) -> Tuple[Any, Tuple[int, int, int]]:
    '''Find the nearest color in a population of colors in RGB colorspace.

    :param color: Color to find neighbor of.
    :type color: Tuple[int, int, int]
    :param population: Population of colors. If dict, keys used as indices.
    :type population: Tuple | List | Dict
    :return: Tuple containing indice found and nearest color.
    :rtype: Tuple[Any, Tuple[int, int, int]]
    '''
    enumerable = None
    if isinstance(population, dict):
        enumerable = population.items()
    elif isinstance(population, list | tuple):
        enumerable = enumerate(population)
    else:
        raise TypeError(f"population must be type tuple, list, or dict, not type {population.__class__.__name__}")
    
    min_difference = inf
    key_value = None
    for index, compare_color in enumerable:
        difference = color_difference(color, compare_color)
        if difference < min_difference:
            min_difference = difference
            key_value = index
    
    return (key_value, population[key_value])