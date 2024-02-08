import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

PHI = (1 + np.sqrt(5)) / 2 + 0j
PSI = 1 - PHI

PLOT = "centre"


class Update:
    def __init__(self, ax, x_start, x_end, step, offset=0) -> None:
        self.ax = ax
        self.x_start = x_start
        self.x_end = x_end
        self.step = step
        self.offset = offset
        self.x = np.arange(x_start, x_end, step)
        self.f = lambda x, y: (
            PHI**x * PHI ** (y * 1j) - PSI**x * PSI ** (y * 1j)
        ) / (PHI - PSI)
        self.fri(0 + self.offset)
        (self.line,) = ax.plot(self.fr, self.fi, "k-")
        self.ax.set(xlabel="$f_{real}$", ylabel="$f_{imag}$")
        self.ax.grid(True)

    def fri(self, y) -> None:
        self.fr = self.f(self.x, y).real
        self.fi = self.f(self.x, y).imag

    def start(self):
        return (self.line,)

    def __call__(self, y):
        y += self.offset
        y *= self.step
        self.fri(y)
        if PLOT == "fix":
            self.ax.set_xlim(min(self.fr), max(self.fr))
            self.ax.set_ylim(min(self.fi), max(self.fi))
        if PLOT == "centre":
            self.ax.set_xlim(-5, 5)
            self.ax.set_ylim(-2, 2)
        self.line.set_data(self.fr, self.fi)
        return (self.line,)


def animate_binet(x_start, x_end, step, offset=0):
    fig, ax = plt.subplots()
    ud = Update(ax, x_start, x_end, step, offset)
    anim = FuncAnimation(
        fig,
        ud,
        init_func=ud.start,
        frames=100,
        interval=100,
        blit=True,
    )
    anim.save(
        ".//python//binet//binet-anim.gif",
        metadata={"artist": "Pratik Das"},
    )
    plt.show()


if __name__ == "__main__":
    animate_binet(0, 5, 0.01, -60)
