import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np


def plot_geo(geo_s):
    if isinstance(geo_s, list):
        n_geos = len(geo_s)
        print(f"Got a list of {n_geos} geometries.")
    else:
        n_geos = 1
        geo_s = [geo_s]

    # 2D : [circ, rect, poly, ?] or 3D : [rect, sphere, cylinder]
    obj_counts = [1, 1, 1]

    # 2d geometries
    if geo_s[0].n_dim == 2:
        fig, ax = plt.subplots()
        for i, geo in enumerate(geo_s):
            if geo.geo_type == "Circ":
                patch = patches.Circle(
                    (geo.x, geo.y),
                    geo.r,
                    label=f"{geo.geo_type} {obj_counts[0]}",
                    edgecolor=f"C{i}",
                    facecolor="none",
                )
                obj_counts[0] += 1
            elif geo.geo_type == "Rect":
                patch = patches.Rectangle(
                    (geo.x, geo.y),
                    geo.width,
                    geo.height,
                    label=f"{geo.geo_type} {obj_counts[1]}",
                    edgecolor=f"C{i}",
                    facecolor="none",
                )
                obj_counts[1] += 1

            elif geo.geo_type == "Poly":
                patch = patches.Polygon(
                    geo.vertices,
                    closed=True,
                    label=f"{geo.geo_type} {obj_counts[1]}",
                    edgecolor=f"C{i}",
                    facecolor="none",
                )
                obj_counts[1] += 1

            ax.add_patch(patch)

        if n_geos != 1:
            plt.legend()
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.axis("equal")

    # 3d geometries
    if geo_s[0].n_dim == 3:
        xlims = list()
        ylims = list()
        zlims = list()
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        for i, geo in enumerate(geo_s):
            if geo.geo_type == "Cuboid":
                label = f"{geo.geo_type} {obj_counts[1]}"
                ax.add_collection3d(
                    Poly3DCollection(
                        geo.faces,
                        label=label,
                        facecolors="gray",
                        linewidths=1,
                        edgecolors=f"C{i}",
                        alpha=0.2,
                    )
                )
                obj_counts[0] += 1
            if geo.geo_type == "Sphere":
                u = np.linspace(0, 2 * np.pi, 100)
                v = np.linspace(0, np.pi, 100)
                x = geo.x + geo.r * np.outer(np.cos(u), np.sin(v))
                y = geo.y + geo.r * np.outer(np.sin(u), np.sin(v))
                z = geo.z + geo.r * np.outer(np.ones(np.size(u)), np.cos(v))
                ax.plot_surface(x, y, z, color=f"C{i}", alpha=0.2)
                obj_counts[1] += 1
            if geo.geo_type == "Cylinder":
                z = np.linspace(geo.z_min, geo.z_max, 100)
                theta = np.linspace(0, 2 * np.pi, 100)
                theta_grid, z = np.meshgrid(theta, z)
                x = geo.r * np.cos(theta_grid) + geo.x
                y = geo.r * np.sin(theta_grid) + geo.y
                ax.plot_surface(x, y, z, color=f"C{i}", alpha=0.2)
                obj_counts[2] += 1
        # if n_geos != 1:
        #     ax.legend()
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.autoscale()
        # ax.set_aspect("equal")

    # plt.tight_layout()
    plt.show()


def plot_prediction(X, Y, u_pred):
    u_pred = u_pred.reshape(X.shape)
    plt.figure(figsize=(8, 6))
    plt.contourf(X, Y, u_pred, 100, cmap="coolwarm", vmin=0, vmax=1)
    plt.colorbar(label="Potential $ϕ(x, y)$")
    plt.title("Predicted Potential Distribution")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()


def plot_test_points(xs, ys, vals):
    plt.scatter(xs, ys, c=vals)
    plt.colorbar(label="Potential ϕ(x, y)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.show()
