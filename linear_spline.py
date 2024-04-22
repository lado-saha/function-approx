from utils import (
    split_interval,
    PLOT_POINTS_COUNT,
    find_sub_interval,
    plot_f,
)
from interpol_error import epsilon


def lin_spline_polynomial(X, Y, h, x) -> float:
    i = find_sub_interval(X, x)
    return Y[i] + ((Y[i + 1] - Y[i]) / h) * (x - X[i])


def linear_spline_f(f, a: float, b: int, n: int):
    h = (b - a) / n  # calcul de h
    X = split_interval(a, b, n)  # recueillir les ai dans A sous forme de liste
    Y = [f(x) for x in X]  # ou Y=[f(x[i]) for i in range (n+1)] ou for i in range

    x_coords = split_interval(a, b, PLOT_POINTS_COUNT)
    y_coords_f = [f(x) for x in x_coords]
    y_coord_approx_f = [lin_spline_polynomial(X, Y, h, x) for x in x_coords]

    error = epsilon(x_coords, y_coords_f, y_coord_approx_f)

    plot_f(
        nom=f"Linear Spline: Error={error}",
        x_interpol=X,
        y_interpol=Y,
        x_coords=x_coords,
        y_coords=y_coords_f,
        y_coords_approx=y_coord_approx_f,
    )
