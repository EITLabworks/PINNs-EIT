from typing import Union

import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from .geo2d import Circ, Rect  # , Poly


class EitEnvironment:
    def __init__(
        self,
        n_el: int,
        x: Union[float, int] = 0,
        y: Union[float, int] = 0,
        r_out: Union[float, int] = 1,
        el_r: Union[float, int] = 0.05,
    ):
        self.n_el = n_el
        self.x = x
        self.y = y
        self.r_out = r_out
        self.el_r = el_r
        self.domain = self.create_domain()
        self.el_xs_ys = self.create_electrodes()

    def create_domain(self, el_r_spacer: float = 0.0005, BC: dict = None):
        if BC is None:
            BC = {
                "bc": "default",
                "mat": "air",
                "mat_perm": 1,
                "pot_val": 0,
            }
        self.el_r_spacer = el_r_spacer
        return Circ(self.x, self.y, self.r_out + el_r_spacer, BC)

    def create_electrodes(self, BC: dict = None):
        if BC is None:
            BC = {
                "bc": "default",
                "mat": "el_mat",
                "mat_perm": 5,
                "pot_val": 0,
            }
        angles = np.linspace(2 * np.pi, 0, self.n_el, endpoint=False)
        xs = (self.r_out - self.el_r) * np.cos(angles)
        ys = (self.r_out - self.el_r) * np.sin(angles)
        pts = np.column_stack((xs, ys))

        el_list = list()
        for n, (x, y) in enumerate(zip(xs, ys)):
            el_BC = BC.copy()
            el_BC["bc"] = f"el_mat{n}"
            el_list.append(Circ(x, y, self.el_r, el_BC))
        self.electrodes = el_list
        return pts

    def add_anomalie(self, anomalie: Union[Rect, Circ]):
        self.anomalie = anomalie
        self.electrodes.append(anomalie)

    def set_inj_stage(
        self,
        el_plus: int,
        el_minus: int,
        pot_plus: Union[float, int] = 1,
        pot_minus: Union[float, int] = -1,
    ):
        assert el_plus < self.n_el and el_minus < self.n_el
        self.create_electrodes()
        self.el_plus = el_plus
        self.el_minus = el_minus
        self.pot_plus = pot_plus
        self.pot_minus = pot_minus

        self.electrodes[self.el_plus].BC["pot_val"] = pot_plus
        self.electrodes[self.el_minus].BC["pot_val"] = pot_minus

    def set_el_BC(self, el_num: int, BC: dict):
        # Set or update BC of a single electrode
        # {'bc': 'default', 'mat': 'el_mat', 'mat_perm': 5, 'pot_val': 1}
        self.electrodes[el_num].BC = BC

    def create_protocol(
        self,
    ):
        pass

    # plotting | printing

    def print_BCs(self):
        print("Domain BC:\n\t", self.domain.BC)

        print("Components BC:")
        for i, ele in enumerate(self.electrodes):
            print(f"\t{i}", ele.BC)

    def plot_domain(self):
        fig, ax = plt.subplots()
        patch = patches.Circle(
            (self.x, self.y),
            self.r_out,
            label="Domain",
            edgecolor="C0",
            facecolor="none",
        )
        ax.add_patch(patch)
        for i, el in enumerate(self.electrodes):
            patch = patches.Circle(
                (el.x, el.y),
                el.r,
                edgecolor="C1",
                facecolor="C1",
            )
            ax.text(el.x, el.y, str(i), size=12)
            ax.add_patch(patch)
        plt.legend(["Domain", "Electrodes"])
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.axis("equal")
        plt.show()

    def plot_inj_stage(self):
        assert hasattr(self, "el_plus"), print(
            "Please use '.set_inj_stage()' to create the injection stage."
        )

        fig, ax = plt.subplots()
        patch = patches.Circle(
            (self.x, self.y),
            self.r_out,
            label="Domain",
            edgecolor="C0",
            facecolor="none",
        )
        ax.add_patch(patch)
        colors = [f"C1" for _ in range(self.n_el)]
        colors[self.el_plus] = "red"
        colors[self.el_minus] = "black"
        legend_elements = list()

        for i, el in enumerate(self.electrodes):
            patch = patches.Circle(
                (el.x, el.y),
                el.r,
                edgecolor=colors[i],
                facecolor=colors[i],
            )
            ax.text(el.x + 0.03, el.y + 0.03, str(i), size=12)
            ax.add_patch(patch)
            if i == self.el_plus:
                legend_elements.append(patches.Patch(color="red", label="inj. +"))
            elif i == self.el_minus:
                legend_elements.append(patches.Patch(color="black", label="inj. -"))
        if self.n_el > 2:
            legend_elements.append(patches.Patch(color="C1", label="Electrodes"))
        legend_elements.append(
            patches.Patch(edgecolor="C0", facecolor="none", label="Domain")
        )
        plt.legend(handles=legend_elements)
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.axis("equal")
        plt.show()
