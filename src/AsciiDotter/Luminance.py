from enum import Enum
from typing import Callable


# Due to the way that Python handles Enums, we have to wrap our functions in a class to
# be able to put them in an Enum. __EnumerableFunction is the wrapper class, and it's __call__ is set to
# mimic it's inner function. The __enumerable_function decorator will make any function
# enumerable by returning the function wrapped in our class.

class __EnumerableFunction:
    '''A simple wrapper class for any function.'''
    def __init__(self,func):
        self.__func = func
    
    def __call__(self,*args,**kwargs):
        return self.__func(*args,**kwargs)

def __enumerable_function(func):
    return __EnumerableFunction(func)


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

@__enumerable_function
def calculate_average(r:int, g:int, b:int) -> float:
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

@__enumerable_function
def calculate_luminance(r:int, g:int, b:int) -> float:
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

@__enumerable_function
def calculate_value(r:int, g:int, b:int):
    '''Get the luminance of a color in RGB space by calculating it's value.
    
    :param r: red value.
    :type r: int
    :param g: green value.
    :type g: int
    :param b: blue value.
    :type b: int
    
    :returns Luminance of the color in [0.0, 1.0]
    :rtype: float'''

    return max(r/255,g/255,b/255)

@__enumerable_function
def calculate_weighted(r:int, g:int, b:int):
    '''Get the luminance of a color in RGB space by calculating it's weighted luminance. Similar to relative luminance.
    
    :param r: red value.
    :type r: int
    :param g: green value.
    :type g: int
    :param b: blue value.
    :type b: int
    
    :returns Luminance of the color in [0.0, 1.0]
    :rtype: float'''

    gs = (0.299*r) + (0.587*g) + (0.114*b)

    return __map(gs,0,255)

class LuminanceMethod(Enum):
    '''Valid methods for calculating Luminance. Each Enum's value is a Callable(int,int,int) -> float'''

    AVERAGE:Callable[[int,int,int],float] = calculate_average
    VALUE:Callable[[int,int,int],float] = calculate_value
    WEIGHTED:Callable[[int,int,int],float] = calculate_weighted
    RELATIVE:Callable[[int,int,int],float] = calculate_luminance