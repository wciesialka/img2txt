

def __map(value:float,lower_bound:float,upper_bound:float) -> float:
    '''Map a value that is in the range of [lower bound, upper bound] to [0.0, 1.0].\n
    A value between [0.0, 1.0] is not guaranteed (for example, if value is less than lower bound or greater than upper bound.)
    
    :param value: Value to map.
    :type value: float
    :param lower_bound: Lower bound of value, inclusive.
    :type lower_bound: float
    :param upper_bound: Upper bound of value, inclusive.
    :type upper_bound: float
    
    :returns: The mapped value between [0.0, 1.0].
    :rtype: float'''
    
    return (value - lower_bound) * 1.0 / (upper_bound - lower_bound)

def average(r:int, g:int, b:int) -> float:
    '''Get the luminance of a color in RGB space using the average of the three colors.
    
    :param r: red value.
    :type r: int
    :param g: green value.
    :type g: int
    :param b: blue value.
    :type b: int
    
    :returns: Luminance of the color in [0.0, 1.0]
    :rtype: float'''
    avg = (r+g+b)/3

    return __map(avg,0,255)

def relative_luminance(r:int, g:int, b:int) -> float:
    '''Get the luminance of a color in RGB space using the relative luminance formula.
    
    :param r: red value.
    :type r: int
    :param g: green value.
    :type g: int
    :param b: blue value.
    :type b: int
    
    :returns: Luminance of the color in [0.0, 1.0]
    :rtype: float'''

    r_lin = r**2.2
    g_lin = g**2.2
    b_lin = b**2.2

    y = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

    return __map(y,0,196964.69911399897)