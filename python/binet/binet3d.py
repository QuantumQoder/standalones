import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


def plot_binet3d(
    x_start: float, x_end: float, y_start: float, y_end: float, step: float
) -> None:
    PHI: float = (1 + np.sqrt(5)) / 2 + 0j
    PSI: float = 1 - PHI

    x = np.arange(x_start, x_end, step)
    y = np.arange(y_start, y_end, step)
    x, y = np.meshgrid(x, y)

    f = ((PHI**x) * (PHI ** (y * 1j)) - (PSI**x) * (PSI ** (y * 1j))) / (PHI - PSI)
    f_r = f.real
    f_i = f.imag

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(
        f_r, y, f_i, cmap=cm.viridis_r, linewidth=0, antialiased=True
    )
    ax.set(xlabel="$f_{real}$", ylabel="y", zlabel="$f_{imag}$")
    ax.grid()
    plt.show()


if __name__ == "__main__":
    plot_binet3d(0, 5, -0.5, 0, 0.001)
