from typing import Union
from .geo import Rect, Circ


def exclude_points_in_region(pts, geo_s: Union[Rect, Circ]):
    if isinstance(geo_s, list):
        n_geos = len(geo_s)
        print(f"Got a list of {n_geos} geometries to exclude.")
    else:
        n_geos = 1
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
            pts = pts[~mask]
    return pts
