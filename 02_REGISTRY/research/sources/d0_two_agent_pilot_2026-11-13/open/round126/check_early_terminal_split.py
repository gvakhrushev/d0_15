"""Exact split of the A68 feedback and spatial heat on the same layout."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round125"))
from check_no_field_anchor import verify_native_flag, ne


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def verify_virtual_feedback():
    p, u, z, t = sp.symbols("p u z t", positive=True)
    a = 1-z
    active_h = p**2*u
    C0 = sp.sqrt(p)
    C1 = sp.Matrix([[p*sp.sqrt(u), 0]])
    C = sp.Matrix([[C0, *C1]])
    F = sp.eye(3)-C.T*C
    effective_z = z*p**2
    early_a = a+z*p
    require(sp.rem(early_a-1+effective_z, p*p+p-1, p) == 0, "Golden virtual fugacity")
    full = sp.eye(3)-z*F
    active = early_a*sp.eye(2)+effective_z*sp.diag(u, 0)
    ratio = a**2 / early_a
    require(sp.cancel(full.det()-ratio*active.det()) == 0, "A68 determinant renormalization")

    mark = sp.diag(t, 1, 1)
    D = a+z*(p+active_h)
    nu = z/a*(1-p/D)
    pgf = full.det()/(sp.eye(3)-z*F*mark).det()
    require(sp.cancel(pgf-1/(1+(1-t)*nu)) == 0, "Early occupation law")
    require(sp.cancel(sp.diff(nu, u) - z**2*p**3/(a*D**2)) == 0,
            "Late geometry derivative of the virtual early mark")

    z_literal = sp.Rational(1, 2**20)
    p_literal = ne.P
    vacuum_lower = (1-z_literal)**12
    require(vacuum_lower > sp.Rational(3, 4) and sp.Rational(1, 2) < p_literal < sp.Rational(3, 4),
            "Vacuum and physical flag must be separated")
    require(1-vacuum_lower < sp.Rational(1, 2), "No nonempty-only event has the native probability")
    return {
        "early_reached_rank": 4,
        "full_reached_rank_bound": 12,
        "effective_active_fugacity": "z*p^2",
        "virtual_reference_only_factor": "[1-z*(1-p)]^(-4)-1",
        "virtual_early_PGF": "[1+(1-t)*nu]^(-4)",
        "nu": "z/(1-z)*[1-p/(1-z+z*h)]",
        "earliest_virtual_event_cannot_have_native_p": True,
        "joint_normalized_virtual_early_distribution_can_see_late_h": True,
    }


def verify_spatial_harmonics():
    groups = (range(9), range(9, 20), range(20, 33))
    edges = [(v, w) for i, grp in enumerate(groups)
             for later in groups[i+1:] for v in grp for w in later]
    incidence = sp.zeros(len(edges), 33)
    for row, (v, w) in enumerate(edges):
        incidence[row, v] = -1
        incidence[row, w] = 1
    rank = incidence.rank()
    require(len(edges) == 359 and rank == 32, "Unexpected scene incidence")
    cycle = sp.zeros(len(edges), 1)
    for edge, sign in (((0, 9), 1), ((9, 20), 1), ((0, 20), -1)):
        cycle[edges.index(edge)] = sign
    require(incidence.T*cycle == sp.zeros(33, 1), "Triangle is not a spatial cycle")
    return {"actual_scene_vertices": 33, "actual_scene_edges": 359,
            "incidence_rank": rank, "field_independent_spatial_harmonics_per_stage": len(edges)-rank}


def main():
    book = HERE.parents[5] / "01_BOOKS" / "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md"
    print(json.dumps({
        "book03_sha256": sha256(book.read_bytes()).hexdigest(),
        "native_stopped_flag": verify_native_flag(),
        "virtual_feedback": verify_virtual_feedback(),
        "spatial_harmonics": verify_spatial_harmonics(),
        "Book03_declares_virtual_mass_is_physical_early_leaf": False,
        "same_absolute_paid_stop_certified_on_full_late_chart": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
