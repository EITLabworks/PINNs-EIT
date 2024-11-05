import matplotlib.pyplot as plt
import matplotlib.patches as patches
from .util import Rect


def plot_domain(Ω: Rect, exclΩ: Rect, mode="square"):
    fig, ax = plt.subplots()
    if mode == "square":
        domainΩ = patches.Rectangle(
            (Ω.x, Ω.y),
            Ω.width,
            Ω.height,
            edgecolor="C0",
            facecolor="none",
            hatch="/",
            label="$\Omega$",
        )
        exclude = patches.Rectangle(
            (exclΩ.x, exclΩ.y),
            exclΩ.width,
            exclΩ.height,
            edgecolor="C1",
            facecolor="none",
            hatch="\ ",
            label="$\Gamma$",
        )

        ax.add_patch(domainΩ)
        ax.add_patch(exclude)
    plt.xlim(Ω.x - 0.2, Ω.x + Ω.width + 0.2)
    plt.ylim(Ω.y - 0.2, Ω.y + Ω.height + 0.2)
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.axis("equal")
    plt.tight_layout()
    plt.legend()
    plt.show()


def plot_domain_wpoints(
    Ω: Rect, exclΩ: Rect, Pts, pts_visual: dict = None, mode="square"
):
    """
    pts_vis if not none [size, color, marker, label]
    """
    fig, ax = plt.subplots()
    if mode == "square":
        domainΩ = patches.Rectangle(
            (Ω.x, Ω.y),
            Ω.width,
            Ω.height,
            edgecolor="C0",
            facecolor="none",
            hatch="/",
            label="$\Omega$",
        )
        exclude = patches.Rectangle(
            (exclΩ.x, exclΩ.y),
            exclΩ.width,
            exclΩ.height,
            edgecolor="C1",
            facecolor="none",
            hatch="\ ",
            label="$\Gamma$",
        )

        ax.add_patch(domainΩ)
        ax.add_patch(exclude)
    if pts_visual == None:
        plt.scatter(Pts[:, 0], Pts[:, 1], s=1, label="$\Omega - \Gamma$ Points")
    else:
        plt.scatter(Pts[:, 0], Pts[:, 1], **pts_visual)
    plt.xlim(Ω.x - 0.2, Ω.x + Ω.width + 0.2)
    plt.ylim(Ω.y - 0.2, Ω.y + Ω.height + 0.2)
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.legend()
    plt.axis("equal")
    plt.tight_layout()
    plt.show()
