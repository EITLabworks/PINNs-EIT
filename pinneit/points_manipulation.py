from typing import Union
from .classes_2d import Rect, Circ


def exclude_points_in_region(pts, geo: Union[Rect, Circ]):
    if geo.geo_type == "Rect":
        mask = (
            (geo.x_min <= pts[:, 0])
            & (pts[:, 0] <= geo.x_max)
            & (geo.y_min <= pts[:, 1])
            & (pts[:, 1] <= geo.y_max)
        )
    elif geo.geo_type == "Circ":
        mask = (pts[:, 0] - geo.x) ** 2 + (pts[:, 1] - geo.y) ** 2 <= geo.r**2

    pts = pts[~mask]
    return pts
