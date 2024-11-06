import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_geo(geo_s):
    if isinstance(geo_s, list):
        n_geos = len(geo_s)
        print(f"Got a list of {n_geos} geometries.")
    else:
        n_geos = 1
        geo_s = [geo_s]
        
    fig, ax = plt.subplots()

    obj_counts = [1,1,1] # [circ, rect,line]
    for i,geo in enumerate(geo_s):
        if geo.geo_type == "Circ":
            patch = patches.Circle(
                        (geo.x, geo.y),
                        geo.r,
                        label=f"{geo.geo_type} {obj_counts[0]}",
                        edgecolor=f"C{i}",
                        facecolor="none",
    
                    )
            obj_counts[0] +=1
        elif geo.geo_type == "Rect":
            patch = patches.Rectangle(
                    (geo.x, geo.y),
                    geo.width,
                    geo.height,
                    label=f"{geo.geo_type} {obj_counts[1]}",
                    edgecolor=f"C{i}",
                    facecolor="none",
                )
            obj_counts[1] +=1
        ax.add_patch(patch)
    if n_geos != 1:
        plt.legend()
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()