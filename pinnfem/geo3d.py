from typing import Union

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


from .points_manipulation import random_points_on_face


class Cuboid:
    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        z: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        depth: Union[int, float],
        BC: dict = None,
    ):
        """
        __init__

        Parameters
        ----------
        x : Union[int,float]
            x-position of the edge
        y : Union[int,float]
            y-position of the edge
        z : Union[int,float]
            z-position of the edge
        width : Union[int,float]
            x-direction width
        height : Union[int,float]
            y-direction width
        depth : Union[int,float]
            z-direction width
        BC : dict, optional
            class object properties for ngsolve, by default None
        """
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
        """
        print properties
        """
        print(self.__dict__)

    def gen_vertices(self):
        """
        generate vertices

        Returns
        -------
        _type_
            _description_
        """
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
        # TBD -> check if more elegant programming is feasable
        return vertices

    def gen_faces(self):
        """
        generate faces

        Returns
        -------
        _type_
            _description_
        """
        faces = [
            tuple([self.vertices[i] for i in [0, 1, 2, 3]]),  # xy|z=min
            tuple([self.vertices[i] for i in [4, 5, 6, 7]]),  # xy|z=max
            tuple([self.vertices[i] for i in [0, 1, 5, 4]]),  # xz|y=min
            tuple([self.vertices[i] for i in [2, 3, 7, 6]]),  # xz|y=max
            tuple([self.vertices[i] for i in [1, 2, 6, 5]]),  # zy|x=max
            tuple([self.vertices[i] for i in [0, 3, 7, 4]]),  # zy|x=min
        ]
        # TBD -> check if more elegant programming is feasable
        return faces

    def generate_surfaces_points(self, n_pts_per_face: int, return_pts: bool = True):
        """
        generate surfaces points

        Parameters
        ----------
        n_pts_per_face : int
            number of points per face (total number of points = 6*n_pts_per_face)
        return_pts : bool, optional
            return the created points, by default True

        Returns
        -------
        np.ndarray
            surface points
        """
        pts = list()
        for f, face in enumerate(self.faces):
            pts.append(random_points_on_face(face, n_pts_per_face))
        pts = np.array(pts).reshape(-1, 3)

        self.surface_points = pts
        print(f"Generated {pts.shape} surface points.")
        if return_pts:
            return pts

    def generate_volume_points(self, n_pts: int, return_pts: bool = True):
        """
        generate volume points

        Parameters
        ----------
        n_pts : int
            number of points
        return_pts : bool, optional
            return the created points, by default True

        Returns
        -------
        np.ndarray
            surface points
        """
        pts = np.random.rand(n_pts, 3)
        pts[:, 0] = self.x_min + (self.x_max - self.x_min) * pts[:, 0]
        pts[:, 1] = self.y_min + (self.y_max - self.y_min) * pts[:, 1]
        pts[:, 2] = self.z_min + (self.z_max - self.z_min) * pts[:, 2]

        self.volume_points = pts
        print(f"Generated {pts.shape} volume points.")
        if return_pts:
            return pts

    def plot(
        self,
        elev: Union[int, float] = 40,
        azim: Union[int, float] = 30,
        facecolors: str = "gray",
        linewidths: Union[int, float] = 1,
        edgecolors: str = "C0",
        alpha: Union[int, float] = 0.1,
    ):
        """
        plot geometry

        Parameters
        ----------
        elev : Union[int,float], optional
            elevation angle, by default 40
        azim : Union[int,float], optional
            azimut angle, by default 30
        facecolors : str, optional
            _description_, by default "gray"
        linewidths : Union[int,float], optional
            _description_, by default 1
        edgecolors : str, optional
            _description_, by default "C0"
        alpha : Union[int,float], optional
            _description_, by default 0.1
        """
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
        print(f"Generated {pts.shape} surface points.")
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
        print(f"Generated {pts.shape} volume points.")
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


class Cylinder:
    def __init__(self, x, y, z, r, h, BC=None):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.h = h
        self.x_min = self.x - self.r
        self.x_max = self.x + self.r
        self.y_min = self.y - self.r
        self.y_max = self.y + self.r
        self.z_min = self.z - self.h / 2
        self.z_max = self.z + self.h / 2
        self.geo_type = "Cylinder"
        self.n_dim = 3
        self.BC = BC

    def properties(self):
        print(self.__dict__)

    def generate_surfaces_points(self, n_pts_circ, n_pts_lat, return_pts=True):
        """
        n_pts_circ : total number of points on top and bottom surface
        n_pts_lat : total number of points at the lateral surface
        """

        # top
        rand_r = self.r * np.sqrt(np.random.uniform(0, 1, n_pts_circ))
        theta = np.random.uniform(0, 2 * np.pi, n_pts_circ)
        x = self.x + rand_r * np.cos(theta)
        y = self.y + rand_r * np.sin(theta)
        z = np.ones(n_pts_circ) * self.z_max

        pts_top = np.vstack((x, y, z)).T

        # bottom
        rand_r = self.r * np.sqrt(np.random.uniform(0, 1, n_pts_circ))
        theta = np.random.uniform(0, 2 * np.pi, n_pts_circ)
        x = self.x + rand_r * np.cos(theta)
        y = self.y + rand_r * np.sin(theta)
        z = np.ones(n_pts_circ) * self.z_min

        pts_bot = np.vstack((x, y, z)).T

        # lateral surface
        theta = np.random.uniform(0, 2 * np.pi, n_pts_lat)
        x = self.x + self.r * np.cos(theta)
        y = self.y + self.r * np.sin(theta)
        z = np.random.uniform(self.z_min, self.z_max, n_pts_lat)

        pts_lat = np.vstack((x, y, z)).T

        pts = np.vstack((pts_top, pts_lat, pts_bot))
        self.surface_points = pts
        print(f"Generated {pts.shape} surface points.")
        if return_pts:
            return pts

    def generate_volume_points(self, n_pts, return_pts=True):
        radial = self.r * np.sqrt(np.random.uniform(0, 1, n_pts))
        theta = np.random.uniform(0, 2 * np.pi, n_pts)
        x = self.x + radial * np.cos(theta)
        y = self.y + radial * np.sin(theta)
        z = np.random.uniform(self.z_min, self.z_max, n_pts)

        pts = np.vstack((x, y, z)).T

        self.volume_points = pts
        print(f"Generated {pts.shape} volume points.")
        if return_pts:
            return pts

    def plot(self, elev=40, azim=30, facecolors="C0", alpha=0.3):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        z = np.linspace(self.z_min, self.z_max, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        theta_grid, z = np.meshgrid(theta, z)
        x = self.r * np.cos(theta_grid) + self.x
        y = self.r * np.sin(theta_grid) + self.y
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

    def plot_volume_points(self, elev=40, azim=30, facecolors="C0", alpha=0.1):
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
