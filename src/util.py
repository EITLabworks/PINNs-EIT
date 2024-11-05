import numpy as np


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_min = self.x
        self.x_max = self.x + self.width
        self.y_min = self.y
        self.y_max = self.y + self.height

    def properties(self):
        print(
            f"x0 = {self.x}, y0 = {self.y}, width = {self.width}, height = {self.height}"
        )
        print(
            f"x_min = {self.x_min:.2f}, x_max = {self.x_max:.2f}, y_min = {self.y_min:.2f}, y_max = {self.y_max:.2f}"
        )

    def edge_points(self):
        # return online the x/y min max values.
        return self.x_min, self.x_max, self.y_min, self.y_max

    def generate_surface_points(self, n_pts):
        # attention: no tolerance
        pts = np.random.rand(n_pts, 2)
        pts[:, 0] = self.x_min + (self.x_max - self.x_min) * pts[:, 0]
        pts[:, 1] = self.y_min + (self.y_max - self.y_min) * pts[:, 1]
        return pts

    def generate_edge_points(self, n_pts):
        ydir_pts = np.random.uniform(low=self.y_min, high=self.y_max, size=n_pts // 2)
        xdir_pts = np.random.uniform(low=self.x_min, high=self.x_max, size=n_pts // 2)

        x_lower_pts = np.vstack((xdir_pts[::2], np.ones(n_pts // 4) * self.y_min))
        x_upper_pts = np.vstack((xdir_pts[::2], np.ones(n_pts // 4) * self.y_max))
        y_left_pts = np.vstack((np.ones(n_pts // 4) * self.x_min, ydir_pts[::2]))
        y_right_pts = np.vstack((np.ones(n_pts // 4) * self.x_max, ydir_pts[::2]))

        Bpts = np.hstack((x_lower_pts, x_upper_pts, y_left_pts, y_right_pts)).T
        return Bpts

    def domain_points_exclude_Rect(self, exclude, n_pts, tol=0.02):
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


def generate_domain_points(n_points, Ω: Rect, exclΩ: Rect, tol=0.02):
    def scale_points_2d(pts, x_min, x_max, y_min, y_max):
        scaled_pts = np.empty_like(pts)
        scaled_pts[:, 0] = x_min + (x_max - x_min) * pts[:, 0]
        scaled_pts[:, 1] = y_min + (y_max - y_min) * pts[:, 1]
        return np.array(scaled_pts)

    def exclude_2d_Rect(pts, bound, tol):
        x_min, x_max, y_min, y_max = bound.edge_points()
        mask = (
            (pts[:, 0] >= x_min - tol)
            & (pts[:, 0] <= x_max + tol)
            & (pts[:, 1] >= y_min - tol)
            & (pts[:, 1] <= y_max + tol)
        )
        pts = pts[~mask]
        return np.array(pts)

    x_min, x_max, y_min, y_max = Ω.edge_points()

    gen_points = 0
    Pts = list()
    while gen_points < n_points:
        n_dim = 2  # 2d
        pts = np.random.rand(n_points, n_dim)
        pts = scale_points_2d(pts, x_min + tol, x_max - tol, y_min + tol, y_max - tol)
        pts = exclude_2d_Rect(pts, exclΩ, tol)
        Pts.append(pts)
        gen_points += pts.shape[0]

    return np.vstack(Pts)[:n_points]


def generate_edge_points(n_points, Ω, tol=0.02):
    x_min, x_max, y_min, y_max = Ω.edge_points()
    # y direction points
    ydir_pts = np.random.uniform(low=y_min, high=y_max, size=n_points // 2)
    # x direction points
    xdir_pts = np.random.uniform(low=x_min, high=x_max, size=n_points // 2)

    x_lower_pts = np.vstack((xdir_pts[::2], np.ones(n_points // 4) * y_min))
    x_upper_pts = np.vstack((xdir_pts[::2], np.ones(n_points // 4) * y_max))
    y_left_pts = np.vstack((np.ones(n_points // 4) * x_min, ydir_pts[::2]))
    y_right_pts = np.vstack((np.ones(n_points // 4) * x_max, ydir_pts[::2]))

    Bpts = np.hstack((x_lower_pts, x_upper_pts, y_left_pts, y_right_pts)).T
    return Bpts