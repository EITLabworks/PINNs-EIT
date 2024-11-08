from typing import Union

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Rect:
    def __init__(self, x, y, width, height, BC: dict = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_min = self.x
        self.x_max = self.x + self.width
        self.y_min = self.y
        self.y_max = self.y + self.height
        self.geo_type = "Rect"
        self.n_dim = 2
        self.BC = BC

    def properties(self):
        print(
            f"x0 = {self.x}, y0 = {self.y}, width = {self.width}, height = {self.height}"
        )
        print(
            f"x_min = {self.x_min:.2f}, x_max = {self.x_max:.2f}, y_min = {self.y_min:.2f}, y_max = {self.y_max:.2f}"
        )

    def generate_edge_points(self, n_pts):
        ydir_pts = np.random.uniform(low=self.y_min, high=self.y_max, size=n_pts // 2)
        xdir_pts = np.random.uniform(low=self.x_min, high=self.x_max, size=n_pts // 2)

        x_lower_pts = np.vstack((xdir_pts[::2], np.ones(n_pts // 4) * self.y_min))
        x_upper_pts = np.vstack((xdir_pts[::2], np.ones(n_pts // 4) * self.y_max))
        y_left_pts = np.vstack((np.ones(n_pts // 4) * self.x_min, ydir_pts[::2]))
        y_right_pts = np.vstack((np.ones(n_pts // 4) * self.x_max, ydir_pts[::2]))

        pts = np.hstack((x_lower_pts, x_upper_pts, y_left_pts, y_right_pts)).T
        self.edge_points = pts
        return pts

    def generate_surface_points(self, n_pts, return_pts = True):
        pts = np.random.rand(n_pts, 2)
        pts[:, 0] = self.x_min + (self.x_max - self.x_min) * pts[:, 0]
        pts[:, 1] = self.y_min + (self.y_max - self.y_min) * pts[:, 1]
        
        self.surface_points = pts
        if return_pts:
            return pts

    def plot(self, edgecolor="C0", facecolor="none", hatch="/"):
        fig, ax = plt.subplots()
        patch = patches.Rectangle(
            (self.x, self.y),
            self.width,
            self.height,
            edgecolor=edgecolor,
            facecolor=facecolor,
            hatch=hatch,
        )
        ax.add_patch(patch)
        plt.xlim(self.x - 0.2, self.x + self.width + 0.2)
        plt.ylim(self.y - 0.2, self.y + self.height + 0.2)
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

    def generate_grid(self, n_pts_x=100, n_pts_y=100):
        """
        Create uniform distributed mesh points on the geometry.
        """
        x = np.linspace(self.x_min, self.x_max, n_pts_x)
        y = np.linspace(self.y_min, self.y_max, n_pts_y)
        X, Y = np.meshgrid(x, y)
        grid_points = np.stack([X.flatten(), Y.flatten()], axis=-1)
        return X, Y, grid_points

    def domain_points_exclude_Rect(self, exclude, n_pts, tol=0.02):
        ### old
        gen_points = 0
        Pts = list()
        while gen_points < n_pts:
            n_dim = 2  # 2d
            pts = np.random.rand(n_pts, n_dim)
            pts[:, 0] = (
                self.x_min + tol + (self.x_max - self.x_min - 2 * tol) * pts[:, 0]
            )
            pts[:, 1] = (
                self.y_min + tol + (self.y_max - self.y_min - 2 * tol) * pts[:, 1]
            )
            mask = (
                (pts[:, 0] >= exclude.x_min - tol)
                & (pts[:, 0] <= exclude.x_max + tol)
                & (pts[:, 1] >= exclude.y_min - tol)
                & (pts[:, 1] <= exclude.y_max + tol)
            )
            pts = pts[~mask]
            Pts.append(pts)
            gen_points += pts.shape[0]

        return np.vstack(Pts)[:n_pts]


class Circ:
    def __init__(self, x, y, r, BC: dict = None):
        self.x = x
        self.y = y
        self.r = r
        self.x_min = self.x - self.r
        self.x_max = self.x + self.r
        self.y_min = self.y - self.r
        self.y_max = self.y + self.r
        self.geo_type = "Circ"
        self.n_dim = 2
        self.BC = BC

    def properties(self):
        print(f"x0 = {self.x}, y0 = {self.y}, r = {self.r}")
        print(
            f"x_min = {self.x_min:.2f}, x_max = {self.x_max:.2f}, y_min = {self.y_min:.2f}, y_max = {self.y_max:.2f}"
        )

    def generate_edge_points(self, n_pts, return_pts = True):
        pts = np.zeros((n_pts, 2))
        angles = np.random.uniform(0, 2 * np.pi, n_pts)

        pts[:, 0] = self.x + self.r * np.cos(angles)
        pts[:, 1] = self.y + self.r * np.sin(angles)
        self.edge_points = pts 
        if return_pts:
            return pts

    def generate_surface_points(self, n_pts, return_pts = True):
        pts = np.zeros((n_pts, n_pts))
        rand_r = self.r * np.sqrt(np.random.uniform(0, 1, n_pts))
        rand_angle = np.random.uniform(0, 2 * np.pi, n_pts)

        pts[:, 0] = self.x + rand_r * np.cos(rand_angle)
        pts[:, 1] = self.y + rand_r * np.sin(rand_angle)
        self.surface_points = pts
        if return_pts:
            return pts

    def plot(self, edgecolor="C0", facecolor="none", hatch="/"):
        fig, ax = plt.subplots()
        patch = patches.Circle(
            (self.x, self.y),
            self.r,
            edgecolor=edgecolor,
            facecolor=facecolor,
            hatch=hatch,
        )
        ax.add_patch(patch)
        plt.xlim(self.x - self.r - 0.2, self.x + self.r + 0.2)
        plt.ylim(self.y - self.r - 0.2, self.y + self.r + 0.2)
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()


from typing import Union
import matplotlib.pyplot as plt
import matplotlib.patches as patches


###
class Poly:
    def __init__(self, P_xy_s: Union[list, np.ndarray], BC: dict = None):
        """
        P_xy_s ... [[-0.5,-0.5],[0.5,-0.5],[0,0.5]] for drawing a triangle.
        """
        assert len(P_xy_s) > 2, print("Need a list of at least two points.")

        if isinstance(P_xy_s, list):
            P_xy_s = np.array(P_xy_s)

        self.P_xy_s = P_xy_s
        self.vertices = [(x, y) for x, y in P_xy_s]
        self.P_xs = P_xy_s[:, 0]
        self.P_ys = P_xy_s[:, 1]
        self.x_min = np.min(P_xy_s[:, 0])
        self.x_max = np.max(P_xy_s[:, 0])
        self.y_min = np.min(P_xy_s[:, 1])
        self.y_max = np.max(P_xy_s[:, 1])
        self.geo_type = "Poly"
        self.n_dim = 2
        self.BC = BC

    def properties(self):
        for i, ps in enumerate(self.P_xy_s):
            print(f"P{i}(x,y) = {ps}")

    def generate_edge_points(self, n_pts, return_pts = True):
        # TBD
        if return_pts:
            return pts

    def generate_surface_points(self, n_pts, return_pts=False):
        # TBD
        if return_pts:
            return pts
        

    def plot(self, edgecolor="C0", facecolor="none", hatch="/"):
        fig, ax = plt.subplots()
        polygon = patches.Polygon(
            self.vertices,
            closed=True,
            edgecolor=edgecolor,
            facecolor=facecolor,
            hatch=hatch,
        )
        ax.add_patch(polygon)
        plt.xlim(self.x_min - 0.2, self.x_max + 0.2)
        plt.ylim(self.y_min - 0.2, self.y_max + 0.2)
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()