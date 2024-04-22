from utils import split_interval, PLOT_POINTS_COUNT, find_sub_interval, plot_f
from interpol_error import epsilon


import math as m


def cds_matrix_A(n: int, h: float) -> list[list[float]]:
    """
    n: Nombre de point d'interpolation
    h: L'amplitude de chaque sous intervalle de [a, b]
    """
    A = [
        [h] * n,  # Diagonale Inferieur
        [4 * h] * n,  # Diagonale Principale
        [h] * n,  # Diagonale Superieur
    ]

    A[0][0] = 0
    A[-1][-1] = 0
    return A


def tri_diagonal_solver(A: list[list[float]], B: list[float]) -> list[float]:
    """
    Resoudre l'equation AX = B,
    A version CDS d'une matrice tri-diagonal
    B un vecteur
    """
    n = len(B)

    # Elimination en avant
    for i in range(0, n):
        m = A[2][i - 1] / A[1][i - 1]
        A[1][i] -= m * A[2][i - 1]
        B[i] -= m * B[i - 1]

    # Substitution en arriere
    X = [0.0] * n
    for i in range(n - 2, -1, -1):
        X[i] = (B[i] - A[2][i] * X[i - 1]) / A[1][i]

    return X


def cubic_spline_polynomial(C: list[list[float]], X: list[float], x: float):
    i = find_sub_interval(X, x)
    d = x - X[i]
    return C[i][0] + (C[i][1] * d) + (C[i][2] * d * d / 2) + (C[i][3] * d * d * d / 6)


def cubic_spline_f(f, a: float, b: int, N: int):
    h = (b - a) / N  # calcul de h
    X = split_interval(a, b, N)  # recueillir les ai dans A sous forme de liste
    Y = [f(x) for x in X]  # ou Y=[f(x[i]) for i in range (n+1)] ou for i in range

    # Matrix tri-diagonal CDS
    A = cds_matrix_A(N, h)

    beta = [(Y[i + 1] - Y[i]) / h for i in range(N)]
    V = [beta[i] - beta[i - 1] for i in range(1, N)]

    # D[i] = f''(ai) et f``(a) = f``(b) = 0
    D = [0] + tri_diagonal_solver(A, V) + [0]

    C = [
        [
            Y[i],  # c0
            (Y[i + 1] - Y[i]) / h - (2 * D[i] + D[i + 1]) * (h / 6),  # c1
            D[i],  # c2,
            (D[i + 1] - D[i]) / h,  # c3
        ]
        for i in range(N)
    ]

    x_coords = split_interval(a, b, PLOT_POINTS_COUNT)
    y_coords_f = [f(x) for x in x_coords]
    y_coord_approx_f = [cubic_spline_polynomial(C, X, x) for x in x_coords]

    error = epsilon(x_coords, y_coords_f, y_coord_approx_f)

    plot_f(
        nom=f"Cubic Spline: Error={error}",
        x_interpol=X,
        y_interpol=Y,
        x_coords=x_coords,
        y_coords=y_coords_f,
        y_coords_approx=y_coord_approx_f,
    )
