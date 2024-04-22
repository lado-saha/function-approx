from operator import lshift
import matplotlib.pyplot as plt
import multiprocessing

PLOT_POINTS_COUNT = 1000


def plot_f(
    nom: str,
    x_interpol: list[float],
    y_interpol: list[float],
    x_coords: list[float],
    y_coords: list[float],
    y_coords_approx: list[float],
):
    plt.figure(figsize=(10, 6))  # Définir la taille de la figure

    # Tracer les points d'interpolation
    plt.scatter(x_interpol, y_interpol, color="black", label="Interpolating Points")

    # Tracer la courbe de la fonction réelle
    plt.plot(x_coords, y_coords, label="Real Function", marker="", linestyle="-")

    # Tracer la courbe de la fonction approchée
    plt.plot(
        x_coords,
        y_coords_approx,
        label="Approximated Function",
        marker="",
        linestyle="--",
    )

    # Ajouter des légendes
    plt.legend()

    # Définir les limites des axes
    plt.xlim(min(x_coords), max(x_coords))
    plt.ylim(
        min(min(y_coords), min(y_coords_approx)),
        max(max(y_coords), max(y_coords_approx)),
    )

    # Ajouter des titres et des étiquettes aux axes
    plt.title(nom)
    plt.xlabel("X")
    plt.ylabel("Y")

    # Afficher le graphique
    plt.grid(True)
    plt.show()


def find_sub_interval(intervals: list[float], x: float):
    n = len(intervals)
    if x == intervals[-1]:
        return n - 2
    elif x < intervals[0] or x > intervals[-1]:
        return -1

    start = 0
    end = n - 1
    mid = 0

    # binary search to find position
    while start <= end:
        mid = (start + end) // 2
        if intervals[mid] == x:
            break
        elif intervals[mid] < x:
            start = mid + 1
        else:
            end = mid - 1

    if start > end:
        return end
    else:
        return mid


def split_interval(a: float, b: float, n: int) -> list[float]:
    if n < 1:
        return []
    intervals = [0.0] * (n + 1)
    intervals[0] = a
    h = (b - a) / n

    for i in range(1, n + 1):
        intervals[i] = intervals[i - 1] + h

    return intervals


def integral_simpson(x_coords: list[float], y_coords: list[float]) -> float:
    """
    x_coords: List of xi must be a subdivsion
    y_coords: List of yi, yi = f(xi)
    """
    if len(x_coords) != len(y_coords):
        raise ValueError("x_coords and y_coords must have the same length")

    n = len(x_coords)
    h = (x_coords[-1] - x_coords[0]) / (n - 1)
    integral = y_coords[0] + y_coords[-1]

    for i in range(1, n - 1):
        coeff = 2 if i % 2 == 0 else 4
        integral += coeff * y_coords[i]

    return integral * h / 3


def call_functions_parallel(functions):
    """
    Execute a list of functions in parallel using multiprocessing.

    Args:
        functions (list): A list of functions to be executed.

    Returns:
        None
    """
    processes = []

    # Define a helper function to execute each function
    def execute_function(func):
        func()

    # Create and start a process for each function
    for func in functions:
        process = multiprocessing.Process(target=execute_function, args=(func,))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    # for process in processes:
    # process.join()
