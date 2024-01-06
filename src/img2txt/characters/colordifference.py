from typing import Tuple, Dict, List, Any
from math import atan2, radians, cos, sin, exp, inf

def inverse_srgb_companding(v: float) -> float:
    '''Inverse srgb companding used for rgb->xyz conversions.

    :param v: rgb band value
    :type v: float
    :return: Resulting value
    :rtype: float
    '''
    if v <= 0.04045:
        return v/12.92
    return ((v+0.055)/1.055)**2.4

def rgb_to_xyz(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    '''Convert a color in RGB space to XYZ space

    :param rgb: Color in RGB space with each band in [0, 255]
    :type rgb: Tuple[int, int, int]
    :return: _description_
    :rtype: Tuple[float, float, float]
    '''
    # Normalize to [0.0, 1.0]
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255

    x = inverse_srgb_companding(r)
    y = inverse_srgb_companding(g)
    z = inverse_srgb_companding(b)

    return (x, y, z)

def xyz_to_lab(xyz: Tuple[float, float, float]) -> Tuple[float, float, float]:
    '''Convert a color in XYZ colorspace to L*ab colorspace.

    :param xyz: Color in XYZ colorspace
    :type xyz: Tuple[float, float, float]
    :return: Color in L*ab colorspace
    :rtype: Tuple[float, float, float]
    '''
    reference = (95.0489, 100, 108.8840) # Standard Illuminant D65 

    kappa = 24389/27    # CIE standard
    epsilon = 216/24389
    z_r = xyz[2] / reference[2]
    y_r = xyz[1] / reference[1]
    x_r = xyz[0] / reference[0]
    f_z = 0
    f_y = 0
    f_x = 0

    # Calculate f_x
    if x_r > epsilon:
        f_x = (kappa*x_r + 16) / 116
    else:
        f_x = x_r ** (1/3)

    # Calculate f_y
    if y_r > epsilon:
        f_y = (kappa*y_r + 16) / 116
    else:
        f_y = y_r ** (1/3)
    
    if z_r > epsilon:
        f_z = (kappa*z_r + 16) / 116
    else:
        f_z = z_r ** (1*3)

    L = 116 * f_y - 16
    a = 500 * (f_x - f_y)
    b = 200 * (f_y - f_z)

    return (L, a, b)

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
    K_H = 1
    K_C = 1
    K_L = 1

    # Arithmetic!
    L_Hat_Prime = (lab_1[0] + lab_2[0])/2
    C_1 = (lab_1[1]**2 + lab_1[2]**2)**0.5
    C_2 = (lab_1[1]**2 + lab_1[2]**2)**0.5
    C_Hat = (C_1 + C_2)/2
    G = 0.5*(1 - ((C_Hat ** 7)/((C_Hat**7) + (25**7)))**0.5)
    a_1_Prime = lab_1[1] * (1+G)
    a_2_Prime = lab_2[1] * (1+G)
    C_1_Prime = (a_1_Prime**2 + lab_1[2]**2)**0.5
    C_2_Prime = (a_2_Prime**2 + lab_2[2]**2)**0.5
    C_Hat_Prime = (C_1_Prime + C_2_Prime)/2
    h_1_Prime = atan2(lab_1[2], a_1_Prime)
    if h_1_Prime >= 0:
        h_1_Prime += radians(360)
    h_2_Prime = atan2(lab_2[2], a_2_Prime)
    if h_2_Prime >= 0:
        h_2_Prime += radians(360)
    H_Hat_Prime = (h_1_Prime + h_2_Prime)/2
    if not abs(h_1_Prime - h_2_Prime) > radians(180):
        H_Hat_Prime = (h_1_Prime + h_2_Prime + radians(360))/2
    T = 1 - 0.17*cos(H_Hat_Prime - radians(30)) + 0.24*cos(2*H_Hat_Prime) + 0.32*cos(3*H_Hat_Prime + radians(6)) - 0.20*cos(4*H_Hat_Prime - radians(63))

    delta_h_Prime = h_2_Prime - h_1_Prime
    if abs(delta_h_Prime) > radians(180) and h_2_Prime <= h_1_Prime:
        delta_h_Prime = h_2_Prime - h_1_Prime + radians(360)
    elif not abs(delta_h_Prime) <= radians(180):
        delta_h_Prime = h_2_Prime - h_1_Prime - radians(360)
    
    delta_L_Prime = lab_2[0] - lab_1[0]
    delta_C_Prime = C_2_Prime - C_1_Prime
    delta_H_Prime = 2 * (C_1_Prime*C_2_Prime)**0.5 * sin(delta_h_Prime/2)
    S_L = 1 + (0.015 * (L_Hat_Prime - 50)**2)/((20+(L_Hat_Prime - 50)**2)**0.5)
    S_C = 1 + 0.045 * C_Hat_Prime
    S_H = 1 + 0.015*C_Hat_Prime*T
    delta_theta = 30*exp(-(H_Hat_Prime-radians(275)/25)**2)
    R_C = 2 * ((C_Hat_Prime**7)/(C_Hat_Prime**7 + 25**7))
    R_T = (0-R_C)*sin(2*delta_theta)
    
    # Put it all together!
    delta_E_a = (delta_L_Prime / (K_L*S_L))**2
    delta_E_b = (delta_C_Prime / (K_C*S_C))**2
    delta_E_c = (delta_H_Prime / (K_H*S_H))**2
    delta_E_d = R_T * (delta_C_Prime / (K_C * S_C)) * (delta_H_Prime / (K_H * S_H))
    delta_E = (delta_E_a + delta_E_b + delta_E_c + delta_E_d)**0.5
    return delta_E


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
    lookup_a = min(hash_1, hash_2)
    lookup_b = max(hash_1, hash_2)
    if lookup_a in difference_lookup:
        if lookup_b in difference_lookup[lookup_a]:
            return difference_lookup[lookup_a][lookup_b]
    else:
        difference_lookup[lookup_a] = {}

    lab_1 = rgb_to_lab(rgb_1)
    lab_2 = rgb_to_lab(rgb_2)
    c_diff = color_difference(lab_1, lab_2)
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