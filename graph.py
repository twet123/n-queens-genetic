import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def draw(n, queens: list[tuple[float, float]]):
    dx, dy = 0.015, 0.05
    x = np.arange(-n / 2, n / 2, dx)
    y = np.arange(-n / 2, n / 2, dy)
    X, Y = np.meshgrid(x, y)
    min_max = np.min(x), np.max(x), np.min(y), np.max(y)
    res = np.add.outer(range(n), range(n)) % 2
    plt.imshow(res, cmap="binary_r")

    # fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
    for queen in queens:
        c1 = plt.Circle(queen, 0.25, color="red")
        plt.gca().add_patch(c1)

    plt.xticks([])
    plt.yticks([])
    plt.show()
