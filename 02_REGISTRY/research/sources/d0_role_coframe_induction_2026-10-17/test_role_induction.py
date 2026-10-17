#!/usr/bin/env python3
"""Exact checks for the Role coframe induction. Raises ArithmeticError.

python3 and python3 -O must print the same JSON. Assertions are not used.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import sympy as S

import role_induction as induction

CHECKS = []
ROOT = Path(__file__).resolve().parents[4]


def require(name, ok):
    if not ok:
        raise ArithmeticError(name)
    CHECKS.append(name)


def load(relative):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def christoffel_ricci(height):
    """Independent coordinate Ricci. MTW sign, R_sigma nu = R^rho_sigma rho nu."""
    coords = S.symbols("t x y z", real=True)
    eta = S.diag(1, -1, -1, -1)
    wave = S.Matrix([1, 0, 0, 1])
    metric = S.simplify(eta + height * (wave * wave.T))
    inverse = S.simplify(metric.inv())
    derivative = [
        [[S.diff(metric[down, across], coords[direction]) for across in range(4)] for down in range(4)]
        for direction in range(4)
    ]
    gamma = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for upper in range(4):
        for left in range(4):
            for right in range(left, 4):
                total = 0
                for slot in range(4):
                    total += inverse[upper, slot] * (
                        derivative[left][right][slot]
                        + derivative[right][left][slot]
                        - derivative[slot][left][right]
                    )
                gamma[upper][left][right] = S.together(total / 2)
                gamma[upper][right][left] = gamma[upper][left][right]
    ricci = S.zeros(4)
    for down in range(4):
        for across in range(4):
            total = 0
            for upper in range(4):
                total += S.diff(gamma[upper][across][down], coords[upper])
                total -= S.diff(gamma[upper][upper][down], coords[across])
                for slot in range(4):
                    total += gamma[upper][upper][slot] * gamma[slot][across][down]
                    total -= gamma[upper][across][slot] * gamma[slot][upper][down]
            ricci[down, across] = S.factor(total)
    return S.simplify(ricci)


def main():
    CHECKS.clear()
    symbols = S.symbols("H Hx Hy Hxx Hxy Hyy", real=True)
    height, hx, hy, hxx, hxy, hyy = symbols
    family = induction.wave_family(height, hx, hy, hxx, hxy, hyy)
    source = induction.curvature_source(family["e"], family["de"], family["dde"])
    wave = family["k"]
    published = (hxx + hyy) * (wave * wave.T) / 2
    require("coframe_ricci_equals_curvature_formula", source["Ric"] == published)
    require("scalar_density_zero_off_shell", source["scalar_density"] == 0)

    coefficient, transverse, mixed = S.symbols("p q r", real=True)
    x, y = S.symbols("x y", real=True)
    quadratic = coefficient * x**2 / 2 + transverse * y**2 / 2 + mixed * x * y
    metric_ricci = christoffel_ricci(quadratic)
    metric_target = (coefficient + transverse) * (wave * wave.T) / 2
    require("christoffel_ricci_equals_same_coefficient", metric_ricci == metric_target)
    cubic = christoffel_ricci(x**3)
    require("christoffel_cubic_is_3x_kk", cubic == (3 * x) * (wave * wave.T))
    shifted = christoffel_ricci(x**2 + S.Rational(1, 4))
    require("christoffel_shifted_square_is_kk", shifted == wave * wave.T)

    nonvacuum = {
        height: S.Rational(1, 4),
        hx: 0,
        hy: 0,
        hxx: 2,
        hxy: 0,
        hyy: 0,
    }
    ricci_point = S.simplify(source["Ric"].subs(nonvacuum))
    require("nonvacuum_ricci_is_kk", ricci_point == wave * wave.T)
    probe_direction = S.zeros(4)
    probe_direction[0, 0] = 1
    probe = induction.metric_probe(source["Gup"], probe_direction)
    require("nonvacuum_probe_is_one", S.simplify(probe.subs(nonvacuum)) == 1)
    require("profile_tangent_probe_is_zero", induction.metric_probe(source["Gup"], wave * wave.T) == 0)

    profile = wave * wave.T
    lifted_profile = S.simplify(induction.induce_coframe(family["e"], profile))
    require("profile_lifts_to_nilpotent", lifted_profile == family["N"])
    require("profile_lift_support_is_rows_0_and_3", induction.row_support(family["N"]) == (0, 3))
    require(
        "transverse_frame_rows_do_not_depend_on_H",
        family["F"][1, :].diff(height) == S.zeros(1, 4)
        and family["F"][2, :].diff(height) == S.zeros(1, 4),
    )
    lifted_probe = S.simplify(induction.induce_coframe(family["e"], probe_direction).subs(nonvacuum))
    expected_lift = S.zeros(4)
    expected_lift[0, 0] = S.Rational(7, 16)
    expected_lift[3, 0] = S.Rational(1, 16)
    require("nonvacuum_probe_lift", lifted_probe == expected_lift)
    require(
        "probe_lift_support_is_rows_0_and_3",
        induction.row_support(lifted_probe) == (0, 3),
    )
    require(
        "probe_lift_reproduces_metric_variation",
        induction.recovered_metric_variation(family["e"].subs(nonvacuum), lifted_probe) == probe_direction,
    )

    origin = dict(nonvacuum)
    origin[height] = 0
    require("origin_probe_still_one", S.simplify(probe.subs(origin)) == 1)
    heat_gap = 2 * (hx**2 + hy**2)
    require("origin_heat_gap_is_zero", S.simplify(heat_gap.subs(origin)) == 0)
    require("heat_gap_is_not_the_probe_symbol", S.simplify(heat_gap - (hxx + hyy) / 2) != 0)

    require("determinant_is_one", S.simplify(family["e"].det()) == 1)
    require("weight_derivative_is_zero", S.diff(family["e"].det(), height) == 0)

    lorentz = S.eye(4)
    lorentz[0, 0] = lorentz[3, 3] = S.Rational(5, 4)
    lorentz[0, 3] = lorentz[3, 0] = S.Rational(3, 4)
    require("sample_P_is_lorentz", S.simplify(lorentz.T * induction.ETA * lorentz) == induction.ETA)
    moved = S.simplify(lorentz * family["e"])
    require(
        "left_lorentz_preserves_metric",
        S.simplify(moved.T * induction.ETA * moved) == family["g"],
    )
    require("left_lorentz_changes_coframe", S.simplify(moved - family["e"]) != S.zeros(4))
    right = S.simplify(family["e"] * lorentz.inv())
    require(
        "right_action_changes_metric",
        S.simplify(right.T * induction.ETA * right - family["g"]) != S.zeros(4),
    )

    leg = induction.native_leg(family["F"], 0)
    coframe_row = family["e"][0, :].T
    require(
        "native_leg_is_not_coframe_row",
        S.simplify((leg - coframe_row).subs(height, 1)) != S.zeros(4, 1),
    )

    matter = load("02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/matter_response.py")
    weights = load("02_REGISTRY/research/sources/d0_w2_weighted_source_2026-10-16/weighted_source.py")
    row = matter.row_wave_family(S.Rational(1, 4), S.Rational(1, 125))
    gamma = S.simplify(row["gamma"])
    owned_gamma = (
        S.Integer(40443990906472) / S.Integer(5471020515625)
        - S.Integer(19682707537316) * S.sqrt(2) / S.Integer(5471020515625)
    )
    require("row_wave_gamma_matches_owned_chart", gamma == owned_gamma)
    require("row_wave_gamma_nonzero", gamma != 0)
    require("row_wave_second_source_is_not_probe", S.simplify(row["matter_second_contribution"] - 1) != 0)
    frame = (S.Rational(1, 4) - S.Rational(1, 125)) * S.eye(4) + S.Rational(1, 125) * S.ones(4)
    gram = S.simplify(frame * frame.T)
    require("row_wave_gram_has_no_coordinate", all(entry.free_symbols == set() for entry in gram))
    flat = christoffel_ricci(0)
    require("constant_metric_ricci_is_zero", flat == S.zeros(4))
    factor = weights.endpoint_factor(4.0, 1.0)
    require("endpoint_factor_is_two", math.isclose(factor, 2.0))
    require("endpoint_factor_is_not_probe", not math.isclose(factor, 1.0))
    require("geometric_source_is_not_zero_matrix", ricci_point != S.zeros(4))

    vacuum = dict(origin)
    vacuum[hyy] = -2
    vacuum_source = induction.curvature_source(
        family["e"].subs(vacuum),
        [block.subs(vacuum) for block in family["de"]],
        [[block.subs(vacuum) for block in row_blocks] for row_blocks in family["dde"]],
    )
    require("harmonic_vacuum_ricci_zero", vacuum_source["Ric"] == S.zeros(4))
    require("harmonic_vacuum_scalar_zero", vacuum_source["scalar_density"] == 0)
    vacuum_forms = S.Matrix.vstack(*[S.simplify(block) for block in vacuum_source["forms"].values()])
    require("harmonic_vacuum_curvature_nonzero", vacuum_forms != S.zeros(*vacuum_forms.shape))

    payload = {
        "schema": "d0-role-coframe-induction/1",
        "status": "PASS",
        "candidate": True,
        "native_price_equals_geometric_action": False,
        "gr_derived": False,
        "pin": induction.PIN,
        "checker_blob": induction.CHECKER_BLOB,
        "nonvacuum_jet": "H=1/4, Hx=Hy=Hxy=Hyy=0, Hxx=2",
        "probe_E00": "1",
        "probe_lift": "[[7/16,0,0,0],[0,0,0,0],[0,0,0,0],[1/16,0,0,0]]",
        "scalar_density": "0",
        "checks": CHECKS,
        "exact_check_count": len(CHECKS),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
