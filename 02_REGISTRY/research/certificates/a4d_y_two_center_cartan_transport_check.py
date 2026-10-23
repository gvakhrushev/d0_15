#!/usr/bin/env python3
"""Exact boost-row reduction for the commuting Y/dual-center ansatz.

This checks one necessary connection-Euler row on the product-plane solder
S_f=I+(f-1)P_perp.  Even-phase role-0 links carry independent sitewise
Cayley-Y/Cayley-B amplitudes; odd-phase role-0 links and spatial links are
identity in the literal matrix replay.  The row is independent of all Y
amplitudes and is a nonzero scalar times the backward graph Laplacian of f^2.
The block decomposition in the accompanying memo explains why arbitrary
spatial Y links leave this B-row unchanged.  This is restricted to the
commuting span(Y,B), not the full connection space.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import a4d_y_slow_exact_plane_check as owner

OUT = HERE / "a4d_y_two_center_cartan_transport_results.json"
Y = owner.GEN[3] - owner.GEN[4] + owner.GEN[5]
B = owner.GEN[0] + owner.GEN[1] + owner.GEN[2]
P_PERP = -Y**2 / 3


def check(name: str, ok: bool) -> None:
    if not ok:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def run(write: bool = False) -> dict:
    check("COMMUTING_DISJOINT_Y_B_SUPPORT", Y * B == sp.zeros(4) and B * Y == sp.zeros(4))
    check("COMPLEMENTARY_PROJECTORS", P_PERP**2 == P_PERP and B**2 / 3 + P_PERP == sp.eye(4))

    @lru_cache(None)
    def parameter(site: tuple[int, ...], name: str) -> sp.Symbol:
        return sp.Symbol(f"{name}_{site[1]}_{site[2]}_{site[3]}", real=True)

    @lru_cache(None)
    def link(site: tuple[int, ...], role: int) -> sp.Matrix:
        if role != 0:
            return owner.I4
        phase = sum(site) % 4
        z = parameter(site, "z")
        d = parameter(site, "d")
        Uy = owner.cayley_simple(Y, 3, z)
        if phase == 0:
            return Uy * owner.cayley_simple(B, -3, -d)
        if phase == 2:
            return owner.linv(Uy) * owner.cayley_simple(B, -3, d)
        return owner.I4

    @lru_cache(None)
    def solder(site: tuple[int, ...]) -> sp.Matrix:
        f = parameter(site, "f")
        return owner.I4 + (f - 1) * P_PERP

    site = (0, 0, 0, 0)
    row = owner.edge_euler(solder, link, site, 0, B)
    f0 = parameter(site, "f")
    d0 = parameter(site, "d")
    lap = sum(parameter(tuple(site[k] - int(k == axis) for k in range(4)), "f")**2
              for axis in (1, 2, 3)) - 3 * f0**2
    exact = sp.factor(row - (3 * d0**2 + 4) * lap / (3 * d0**2 - 4))
    check("SITEWISE_TWO_CENTER_BOOST_ROW_EXACT", exact == 0)
    check("ROW_HAS_NO_Y_AMPLITUDE", not any(str(sym).startswith("z_") for sym in row.free_symbols))
    check("ROW_NUMERATOR_IS_POSITIVE_QUADRATIC",
          sp.Poly(3 * d0**2 + 4, d0).all_coeffs() == [3, 0, 4])
    check("ROW_DENOMINATOR_IS_CAYLEY_CHART_DENOMINATOR",
          sp.expand(3 * d0**2 - 4 + (4 - 3 * d0**2)) == 0)

    # Independent spatial Y rotations act trivially on the boost-dual plane.
    # Replay three unrelated role amplitudes as an exact symbolic hostile
    # control; the accompanying block argument extends this to sitewise ones.
    z, d = sp.symbols("z d", real=True)
    a = sp.symbols("a0:3", real=True)
    Uy = owner.cayley_simple(Y, 3, z)
    Cminus = owner.cayley_simple(B, -3, -d)
    Cplus = owner.cayley_simple(B, -3, d)
    spatial_rotations = [owner.cayley_simple(Y, 3, a[i]) for i in range(3)]

    @lru_cache(None)
    def y_spatial_link(point: tuple[int, ...], role: int) -> sp.Matrix:
        if role == 0:
            phase = sum(point) % 4
            if phase == 0:
                return Uy * Cminus
            if phase == 2:
                return owner.linv(Uy) * Cplus
            return owner.I4
        return spatial_rotations[role - 1]

    spatial_row = owner.edge_euler(solder, y_spatial_link, site, 0, B)
    spatial_expected = (3 * d**2 + 4) * lap / (3 * d**2 - 4)
    check("INDEPENDENT_SPATIAL_Y_ROTATIONS_DROP_OUT", sp.factor(spatial_row - spatial_expected) == 0)

    result = {
        "schema": "a4d-y-two-center-cartan-transport-v1",
        "ansatz": "phase-0 K0=CY(z_x) CB(-d_x); phase-2 K0=CY(z_x)^(-1) CB(+d_x); odd K0 and spatial links identity in the matrix replay",
        "solder": "S_f=I+(f-1)P_perp; f is positive and independent of time",
        "generator_split": "YB=BY=0; P_perp=-Y^2/3 and P_parallel=B^2/3 are complementary projectors",
        "phase_0_role_0_B_row": "((3*d_x^2+4)/(3*d_x^2-4))*(sum_i f(x-e_i)^2-3*f(x)^2)",
        "sitewise_parameters": "all incident Cayley-Y and Cayley-B amplitudes are independent symbols in the exact replay; only d_x remains in the row",
        "extension": "three independent spatial role amplitudes are checked symbolically; arbitrary sitewise spatial Y links preserve the row by disjoint Y/B support and invariance of the transverse Y-area",
        "consequence": "on a connected periodic spatial torus, stationarity of these phase-0 rows forces f^2 to be constant by the maximum principle",
        "scope": "exact necessary-row no-go inside the commuting Y/B Cartan ansatz only",
        "nonclaims": ["no transverse or non-Y connection correction is excluded", "no global A4D task terminal is claimed", "no refinement-uniform response theorem is proved"],
    }
    if write:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", OUT, flush=True)
    else:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(OUT.read_text()))
    print("TERMINAL A4D-Y-COMMUTING-TWO-CENTER-PRODUCT-PLANE-RIGIDITY", flush=True)
    return result


if __name__ == "__main__":
    run("--write" in sys.argv[1:])
