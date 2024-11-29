from typing import Union
from .geo2d import Rect, Circ, Poly
import numpy as np


def exclude_points_in_region(pts, geo_s: Union[Rect, Circ, Poly], return_mask=False):
    """
    At the moment only tested on 2d -> TBD 3d expansion?
    """
    if isinstance(geo_s, list):
        print(f"Got a list of {len(geo_s)} geometries to exclude.")
    else:
        geo_s = [geo_s]

    for geo in geo_s:
        if geo.geo_type == "Rect":
            mask = (
                (geo.x_min <= pts[:, 0])
                & (pts[:, 0] <= geo.x_max)
                & (geo.y_min <= pts[:, 1])
                & (pts[:, 1] <= geo.y_max)
            )
        elif geo.geo_type == "Circ":
            mask = (pts[:, 0] - geo.x) ** 2 + (pts[:, 1] - geo.y) ** 2 <= geo.r**2
        elif geo.geo_type == "Poly":
            print("TBD: Not implemented")
            break

        pts = pts[~mask]

    if not return_mask:
        return pts
    else:
        return pts, mask


def random_points_on_face(face, n_pts):
    assert len(face) == 4, print(
        "Hand in a face, described by four coordinates (.shape=(4,3))."
    )
    arr = np.array(face)
    konst_ax = np.where(np.all(arr == arr[0, :], axis=0))[0][0]
    remain_ax = [0, 1, 2]
    del remain_ax[konst_ax]
    pts = np.random.rand(n_pts, 3)
    pts[:, konst_ax] = arr[0, konst_ax]

    for rem_ax in remain_ax:
        ax_min, ax_max = np.min(arr[:, rem_ax]), np.max(arr[:, rem_ax])
        pts[:, rem_ax] = ax_min + (ax_max - ax_min) * pts[:, rem_ax]
    return pts
