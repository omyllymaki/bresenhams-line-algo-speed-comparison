import time

import numpy as np
from matplotlib import pyplot as plt

from bresenham_line.cython.line_rasterization import rasterize_lines as rasterize_lines_cython
from bresenham_line.numba.line_rasterization import rasterize_lines as rasterize_lines_numba
from bresenham_line.python.line_rasterization import rasterize_lines as rasterize_lines_py
from bresenham_line.scikit_image.line_rasterization import rasterize_lines as rasterize_lines_skimage

import sys

sys.path.append("bresenham_line/c++/build")
from line_rasterization_module import rasterize_lines as rasterize_lines_cplusplus


def comparison():
    start_points_int = np.loadtxt("data/start_points_int.txt").astype(int)
    end_points_int = np.loadtxt("data/end_points_int.txt").astype(int)

    max_start_points_int = np.max(start_points_int, axis=0)
    max_end_points_int = np.max(end_points_int, axis=0)

    x_max = max(max_start_points_int[0], max_end_points_int[0]) + 1
    y_max = max(max_start_points_int[1], max_end_points_int[1]) + 1
    grid_dim = (x_max, y_max)

    print(f"grid size: {grid_dim}")

    methods = {
        "C++ python binding": rasterize_lines_cplusplus,
        "numba": rasterize_lines_numba,
        "cython": rasterize_lines_cython,
        "skimage": rasterize_lines_skimage,
        "python": rasterize_lines_py,
    }

    # Run numba version once before analysis to compile
    rasterize_lines_numba(start_points_int[:2], end_points_int[:2], grid_dim)

    for method_name, method in methods.items():

        t1 = time.time()
        method(start_points_int, end_points_int, grid_dim)
        t2 = time.time()
        n_lines_per_second = int(start_points_int.shape[0] / (t2 - t1))
        print(f"Version {method_name}: {n_lines_per_second} lines per second")

        grid = method(start_points_int[:10], end_points_int[:10], grid_dim)

        plt.figure()
        plt.imshow(grid.T > 0, cmap="gray", aspect="auto")
        plt.gca().invert_yaxis()
        sps = start_points_int[:10]
        eps = end_points_int[:10]
        for (sp, ep) in zip(sps, eps):
            xs = [sp[0], ep[0]]
            ys = [sp[1], ep[1]]
            plt.plot(xs, ys, "r-")

        plt.title(method_name)

    plt.show()


if __name__ == "__main__":
    comparison()
