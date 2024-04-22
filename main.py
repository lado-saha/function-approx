from cubic_spline import cubic_spline_f
from linear_spline import linear_spline_f
from utils import call_functions_parallel
import math as m


def f1(x):
    return 1 / (1 + m.exp(x**2)) + m.cosh(x)


a = -20
b = 20
n = 100

call_functions_parallel([linear_spline_f(f1, a, b, n), cubic_spline_f(f1, a, b, n)])
