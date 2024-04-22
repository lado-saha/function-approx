from math import sqrt
from utils import integral_simpson


def epsilon(
    x_coords: list[float], y_coords_f: list[float], y_coords_approx_f: list[float]
):
    """
    Calculates the error
    let ~f be the approximation of f over [x0, x1, ..., xn]
    error(~f) = sqrt(integral((~f(x) - f(x))^2))
    NB: y_coords_f[i] = f(x_coords[i])
        y_coords_approx_f[i] = ~f(x_coords[i])
        All have n elements
        x_coords is partition of a certain [a, b]
    """
    n = len(x_coords)

    # let y_coords_diff = (~f(x) - f(x))^2
    y_coords_diff = [(y_coords_f[i] - y_coords_approx_f[i]) ** 2 for i in range(n)]

    eps = integral_simpson(x_coords, y_coords_diff)

    return sqrt(eps)
