import matplotlib.pyplot as plt
import numpy as np


def plot_binet2d(x_start, x_end, step) -> None:
    PHI = (1 + np.sqrt(5)) / 2 + 0j
    PSI = 1 - PHI

    x = np.arange(x_start, x_end, step)
    x = np.meshgrid(x)

    f: complex = (PHI**x - PSI**x) / np.sqrt(5)

    fig, ax = plt.subplots()
    ax.plot(f.real[0], f.imag[0])
    ax.set(xlabel="$f_{real}$", ylabel="$f_{imag}$")
    ax.grid()

    plt.show()


if __name__ == "__main__":
    plot_binet2d(0, 5, 0.01)
