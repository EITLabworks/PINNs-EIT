import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from .points_manipulation import random_points_on_face


class Cuboid:
    def __init__(self, x, y, z, width, height, depth, BC: dict = None):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.x_min = self.x
        self.x_max = self.x + self.width
        self.y_min = self.y
        self.y_max = self.y + self.height
        self.z_min = self.z
        self.z_max = self.z + self.depth
        self.geo_type = "Cuboid"
        self.vertices = self.gen_vertices()
        self.faces = self.gen_faces()
        self.n_dim = 3
        self.BC = BC

    def properties(self):
        print(self.__dict__)

    def gen_vertices(self):
        x, y, z = self.x, self.y, self.z
        dx, dy, dz = self.width, self.height, self.depth
        vertices = np.array(
            [
                [x, y, z],
                [x + dx, y, z],
                [x + dx, y + dy, z],
                [x, y + dy, z],
                [x, y, z + dz],
                [x + dx, y, z + dz],
                [x + dx, y + dy, z + dz],
                [x, y + dy, z + dz],
            ]
        )
        return vertices

    def gen_faces(self):
        faces = [
            tuple([self.vertices[i] for i in [0, 1, 2, 3]]),  # xy|z=min
            tuple([self.vertices[i] for i in [4, 5, 6, 7]]),  # xy|z=max
            tuple([self.vertices[i] for i in [0, 1, 5, 4]]),  # xz|y=min
            tuple([self.vertices[i] for i in [2, 3, 7, 6]]),  # xz|y=max
            tuple([self.vertices[i] for i in [1, 2, 6, 5]]),  # zy|x=max
            tuple([self.vertices[i] for i in [0, 3, 7, 4]]),  # zy|x=min
        ]
        return faces

    def generate_surfaces_points(self, n_pts_per_face, return_pts=True):
        pts = list()
        for f, face in enumerate(self.faces):
            pts.append(random_points_on_face(face, n_pts_per_face))
        pts = np.array(pts).reshape(-1, 3)

        self.surface_points = pts
        print(f"Generated {pts.shape} surface points. ")
        if return_pts:
            return pts

    def generate_volume_points(self, n_pts, return_pts=True):
        pts = np.random.rand(n_pts, 3)
        pts[:, 0] = self.x_min + (self.x_max - self.x_min) * pts[:, 0]
        pts[:, 1] = self.y_min + (self.y_max - self.y_min) * pts[:, 1]
        pts[:, 2] = self.z_min + (self.z_max - self.z_min) * pts[:, 2]

        self.volume_points = pts
        print(f"Generated {pts.shape} volume points. ")
        if return_pts:
            return pts

    def plot(
        self,
        elev=40,
        azim=30,
        facecolors="gray",
        linewidths=1,
        edgecolors="C0",
        alpha=0.1,
    ):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.add_collection3d(
            Poly3DCollection(
                self.faces,
                facecolors=facecolors,
                linewidths=linewidths,
                edgecolors=edgecolors,
                alpha=alpha,
            )
        )
        ax.set_xlim([self.x_min - 0.2, self.x_max + 0.2])
        ax.set_ylim([self.y_min - 0.2, self.y_max + 0.2])
        ax.set_zlim([self.z_min - 0.2, self.z_max + 0.2])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_aspect("equal")
        ax.view_init(elev=elev, azim=azim)
        plt.show()

    def plot_surface_points(
        self,
        elev=40,
        azim=30,
        facecolors="gray",
        linewidths=1,
        edgecolors="C0",
        alpha=0.1,
    ):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.scatter(
            self.surface_points[:, 0],
            self.surface_points[:, 1],
            self.surface_points[:, 2],
            c=np.repeat(
                np.array([0, 1, 2, 3, 4, 5]), self.surface_points.shape[0] // 6
            ),
        )
        ax.add_collection3d(
            Poly3DCollection(
                self.faces, facecolors="gray", linewidths=1, edgecolors="C0", alpha=0.1
            )
        )

        ax.set_xlim([self.x_min - 0.2, self.x_max + 0.2])
        ax.set_ylim([self.y_min - 0.2, self.y_max + 0.2])
        ax.set_zlim([self.z_min - 0.2, self.z_max + 0.2])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_aspect("equal")
        ax.view_init(elev=elev, azim=azim)
        plt.show()

    def plot_volume_points(
        self,
        elev=40,
        azim=30,
        facecolors="gray",
        linewidths=1,
        edgecolors="C0",
        alpha=0.1,
    ):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.scatter(
            self.volume_points[:, 0],
            self.volume_points[:, 1],
            self.volume_points[:, 2],
        )
        ax.add_collection3d(
            Poly3DCollection(
                self.faces, facecolors="gray", linewidths=1, edgecolors="C0", alpha=0.1
            )
        )

        ax.set_xlim([self.x_min - 0.2, self.x_max + 0.2])
        ax.set_ylim([self.y_min - 0.2, self.y_max + 0.2])
        ax.set_zlim([self.z_min - 0.2, self.z_max + 0.2])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_aspect("equal")
        ax.view_init(elev=elev, azim=azim)
        plt.show()


class Sphere:
    def __init__(self, x, y, z, r, BC=None):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.x_min = self.x - self.r
        self.x_max = self.x + self.r
        self.y_min = self.y - self.r
        self.y_max = self.y + self.r
        self.z_min = self.z - self.r
        self.z_max = self.z + self.r
        self.geo_type = "Sphere"
        self.n_dim = 3
        self.BC = BC

    def properties(self):
        print(self.__dict__)

    def generate_surfaces_points(self, n_pts, return_pts=True):
        phi = np.random.uniform(0, 2 * np.pi, n_pts)
        theta = np.arccos(np.random.uniform(-1, 1, n_pts))

        x = self.r * np.sin(theta) * np.cos(phi)
        y = self.r * np.sin(theta) * np.sin(phi)
        z = self.r * np.cos(theta)

        pts = np.vstack((x, y, z)).T

        self.surface_points = pts
        print(f"Generated {pts.shape} surface points. ")
        if return_pts:
            return pts

    def generate_volume_points(self, n_pts, return_pts=True):
        phi = np.random.uniform(0, 2 * np.pi, n_pts)
        theta = np.arccos(np.random.uniform(-1, 1, n_pts))
        r = self.r * np.cbrt(np.random.uniform(0, 1, n_pts))
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        pts = np.vstack((x, y, z)).T

        self.volume_points = pts
        print(f"Generated {pts.shape} volume points. ")
        if return_pts:
            return pts

    def plot(self, elev=40, azim=30, facecolors="C0", alpha=0.3):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = self.x + self.r * np.outer(np.cos(u), np.sin(v))
        y = self.y + self.r * np.outer(np.sin(u), np.sin(v))
        z = self.z + self.r * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color=facecolors, alpha=alpha)
        ax.set_xlim([self.x_min - 0.2, self.x_max + 0.2])
        ax.set_ylim([self.y_min - 0.2, self.y_max + 0.2])
        ax.set_zlim([self.z_min - 0.2, self.z_max + 0.2])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_aspect("equal")
        ax.view_init(elev=elev, azim=azim)
        ax.set_aspect("equal")
        plt.show()

    def plot_surface_points(self, elev=40, azim=30, facecolors="C0", alpha=0.3):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(
            self.surface_points[:, 0],
            self.surface_points[:, 1],
            self.surface_points[:, 2],
            color=facecolors,
            alpha=alpha,
        )
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_aspect("equal")
        ax.view_init(elev=elev, azim=azim)
        ax.set_aspect("equal")
        plt.show()

    def plot_volume_points(self, elev=40, azim=30, facecolors="C1", alpha=0.3):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(
            self.volume_points[:, 0],
            self.volume_points[:, 1],
            self.volume_points[:, 2],
            color=facecolors,
            alpha=alpha,
        )
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_aspect("equal")
        ax.view_init(elev=elev, azim=azim)
        ax.set_aspect("equal")
        plt.show()
