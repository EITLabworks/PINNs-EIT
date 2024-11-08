from netgen.geom2d import CSG2d, Circle, Rectangle
from ngsolve import (
    Mesh,
    CoefficientFunction,
    H1,
    BilinearForm,
    grad,
    dx,
    GridFunction,
    Grad,
)
from ngsolve.webgui import Draw
from collections import defaultdict
import numpy as np


def wrap_to_mesh(main, interior_s, refinement=0.2):
    def create_geo_component(geo):
        if geo.geo_type == "Rect":
            component = Rectangle(
                pmin=(geo.x_min, geo.y_min),
                pmax=(geo.x_max, geo.y_max),
                bc=geo.BC["bc"],
                mat=geo.BC["mat"],
            )
        elif geo.geo_type == "Circ":
            component = Circle(
                center=(geo.x, geo.y), radius=geo.r, bc=geo.BC["bc"], mat=geo.BC["mat"]
            )

        elif geo.geo_type == "Poly":
            print("At the moment the wrapping of polygons is not implemented.")
            pass
        return component

    if isinstance(interior_s, list):
        interior_s = interior_s
    else:
        interior_s = [interior_s]

    geometry = CSG2d()
    domain = create_geo_component(main)

    for ints in interior_s:
        fragment = create_geo_component(ints)
        geometry.Add(fragment)
        domain = domain - fragment  # "-" is subtsraction, "*" is union

    geometry.Add(domain)

    mesh = Mesh(geometry.GenerateMesh(maxh=refinement))
    # curve the mesh elements for geometry approximation of given order
    mesh.Curve(3)
    # print("Boundaries:",mesh.GetBoundaries())
    # print("Materials:",mesh.GetMaterials())

    return mesh


# solve


def solve(main, interior_s, refinement=0.2):
    if isinstance(interior_s, list):
        interior_s = interior_s
    else:
        interior_s = [interior_s]

    mesh = wrap_to_mesh(main, interior_s, refinement)

    diel_perm = defaultdict(lambda: 1)  # -1 is default
    diel_perm[main.BC["mat"]] = main.BC["mat_perm"]
    dirichlet_str_parts = list()
    potential_str_parts = list()
    potential = defaultdict(lambda: -1)
    potential[main.BC["bc"]] = main.BC["pot_val"]

    for ints in interior_s:
        diel_perm[ints.BC["mat"]] = ints.BC["mat_perm"]
        potential[ints.BC["bc"]] = ints.BC["pot_val"]

        dirichlet_str_parts.append(ints.BC["bc"])
        potential_str_parts.append(ints.BC["bc"])

    dirichlet_str = "|".join(dirichlet_str_parts)
    potential_str = "|".join(potential_str_parts)

    diel_perm_cf = CoefficientFunction([diel_perm[mat] for mat in mesh.GetMaterials()])
    potential_cf = CoefficientFunction([potential[bnd] for bnd in mesh.GetBoundaries()])

    fes = H1(mesh, order=2, dirichlet=dirichlet_str)
    ut, vt = fes.TnT()
    a = BilinearForm(fes)

    a += diel_perm_cf * grad(ut) * grad(vt) * dx
    a.Assemble()
    gfu = GridFunction(fes, name="Potential")
    gfu.Set(potential_cf, definedon=mesh.Boundaries(potential_str))
    f = gfu.vec.CreateVector()
    f.data = a.mat * gfu.vec
    gfu.vec.data -= a.mat.Inverse(fes.FreeDofs(), inverse="sparsecholesky") * f
    Draw(gfu)
    return gfu


def get_vals_of_points(mesh, gfu, Pts):
    X, Y = Pts[:, 0], Pts[:, 1]
    vals = np.array([gfu(mesh(*p)) for p in Pts])
    return X, Y, vals
