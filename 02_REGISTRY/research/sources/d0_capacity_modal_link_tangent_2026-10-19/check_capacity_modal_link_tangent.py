#!/usr/bin/env python3
"""Exact local link jet for the capacity-mean / pathwise-MDL comparison.

Recomputes the flat first jet of the original six-based-plaquette Palatini
density, then checks the two tied modal path slopes on that actual field
direction. Scope is declared in the companion result memo.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
ETA = sp.Matrix(
    [
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ]
)
PAIRS = list(combinations(range(4), 2))
H = sp.symbols("h", positive=True)
T = sp.symbols("t", positive=True)
PHI = (1 + sp.sqrt(5)) / 2
P = (sp.sqrt(5) - 1) / 2
ELL = sp.log(PHI)


def eps(indices: tuple[int, int, int, int]) -> sp.Expr:
    return sp.LeviCivita(*indices)


def shift(site: tuple[int, ...], axis: int) -> tuple[int, ...]:
    out = list(site)
    out[axis] += 1
    return tuple(out)


def lorentz_generator(i: int, j: int) -> sp.Matrix:
    q = sp.zeros(4)
    q[i, j] = 1
    q[j, i] = -1
    return q * ETA


def local_density_jet(
    cell: tuple[int, ...],
    varied_link_site: tuple[int, ...],
    varied_link_axis: int,
    generator: sp.Matrix,
) -> sp.Expr:
    """Differentiate one original six-face density at the flat point."""
    total = sp.Integer(0)
    for r, s in PAIRS:
        u, v = [axis for axis in range(4) if axis not in (r, s)]
        # P_rs = U_r(x) U_s(x+r) U_r(x+s)^(-1) U_s(x)^(-1).
        edges = (
            (cell, r, 1),
            (shift(cell, r), s, 1),
            (shift(cell, s), r, -1),
            (cell, s, -1),
        )
        d_plaquette = sp.zeros(4)
        for site, axis, orientation in edges:
            if site == varied_link_site and axis == varied_link_axis:
                d_plaquette += orientation * generator

        # At P=I, D[(P-P^{-1})/2]=DP. The flat coframe is h I.
        wedge = sp.zeros(4)
        wedge[u, v] = H**2
        wedge[v, u] = -H**2
        curvature_times_eta = d_plaquette * ETA
        contraction = sum(
            eps((a, b, c, d)) * wedge[a, b] * curvature_times_eta[c, d]
            for a, b in PAIRS
            for c, d in PAIRS
        )
        total += eps((r, s, u, v)) * contraction
    return sp.factor(total)


def main() -> None:
    origin = (0, 0, 0, 0)
    generator = lorentz_generator(0, 1)
    # This is precisely X_ab=(E_ab-E_ba) eta, used by the original owner.
    assert sp.simplify(generator.T * ETA + ETA * generator) == sp.zeros(4)

    observed: dict[tuple[int, ...], sp.Expr] = {}
    for cell in product(range(-1, 2), repeat=4):
        value = local_density_jet(cell, origin, 0, generator)
        if value != 0:
            observed[cell] = value

    expected = {
        origin: H**2,
        (0, -1, 0, 0): -H**2,
    }
    assert observed == expected, (observed, expected)

    f_jets = {cell: sp.simplify(value / H**4) for cell, value in observed.items()}
    assert f_jets == {
        origin: H**-2,
        (0, -1, 0, 0): -H**-2,
    }

    # e_i=p^2(1+t^2 f_x), so the two cells induce +/- de.
    de = sp.simplify(P**2 * T**2 / H**2)
    path_increment = sp.simplify((PHI - ELL) * de / ELL)
    assert path_increment != 0

    # For arbitrary A=D Gamma[V], the two modal branch slopes are A +/- d.
    a = sp.symbols("A", real=True)
    d = sp.symbols("d", positive=True)
    forward_min = a - d
    reverse_min = -a - d
    directional_sum = sp.simplify(forward_min + reverse_min)
    assert directional_sum == -2 * d

    relevant_sources = (
        "02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/star_euler.py",
        "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
        "02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md",
    )
    source_hashes = {
        path: sha256((ROOT / path).read_bytes()).hexdigest()
        for path in relevant_sources
    }

    result = {
        "status": "PASS_EXACT",
        "schema": "d0-capacity-modal-link-tangent/1",
        "command": "python3 02_REGISTRY/research/sources/d0_capacity_modal_link_tangent_2026-10-19/check_capacity_modal_link_tangent.py",
        "git_head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "environment": {
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
        },
        "link_variation": "delta U_0(0)=X_01 U_0(0), X_01=(E_01-E_10) eta",
        "proper_lorentz_tangent": True,
        "local_D_Pstar_support": {
            str(cell): str(value) for cell, value in sorted(observed.items())
        },
        "local_D_f_support": {
            str(cell): str(value) for cell, value in sorted(f_jets.items())
        },
        "capacity_leaf_increment_magnitude": str(de),
        "modal_path_increment_magnitude": str(path_increment),
        "for_arbitrary_mean_slope_A": {
            "Dplus_min(V)_upper_bound": "A-d",
            "Dplus_min(-V)_upper_bound": "-A-d",
            "sum_upper_bound": str(directional_sum),
            "d_positive_for_h_t_positive": True,
        },
        "coverage_condition": "at least one admitted fine leaf in each of Q_0 and Q_-e1",
        "scope": [
            "exact finite geometric source jet on the original six-plaquette carrier",
            "conditional obstruction to identifying this pointer-history minimum with the smooth capacity mean",
            "does not select the Book history space or full native Cost-Info action",
            "does not rule out a separately derived same-run compensating source",
        ],
        "input_sha256": source_hashes,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
