from cubic_spline import cubic_spline_f
from linear_spline import linear_spline_f
import math as m


def func(x):
    return 2 + 4 * m.sin(x)


a = -20
b = 20
n = 55

linear_spline_f(func, a, b, n)
cubic_spline_f(func, a, b, n)
