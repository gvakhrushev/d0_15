#!/usr/bin/env python3
"""Replay the saved exact quartic vector by direct full-Euler substitution."""
import hashlib
import json
import sys
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_cubic_finite_cartan_range as c
import check_quartic_finite_cartan_range as restricted

SECTORS = ((4, 0), (3, 1), (2, 2), (1, 3), (0, 4))
MIXED = (2, 2)
OLD_SOLUTION = HERE / "quartic_all_sectors_shared_cubic_branch_solution.json"
NEW_SOLUTION = HERE / "quartic_full_spatial_jet_solution.json"
NEW_RESULT = HERE / "quartic_full_spatial_jet_result.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def freeze_cache(cache, substitutions):
    def get(site):
        return [[[c.Jet({amp: s.expand(value.xreplace(substitutions))
                         for amp, value in entry.c.items()})
                  for entry in row] for row in matrix] for matrix in cache(site)]
    return get


def freeze_modes(modes, substitutions):
    def get(site):
        return {key: s.expand(value.xreplace(substitutions))
                for key, value in modes(site).items()}
    return get


def main():
    old_record = json.loads(OLD_SOLUTION.read_text())
    result_record = json.loads(NEW_RESULT.read_text())
    new_record = json.loads(NEW_SOLUTION.read_text())
    require(sha256(HERE / old_record["source_checker"]) ==
            old_record["source_checker_sha256"],
            "prior checker SHA-256 mismatch")
    require(sha256(HERE / old_record["source_output"]) ==
            old_record["source_output_sha256"],
            "prior solver output SHA-256 mismatch")
    require(result_record["status"] ==
            "PASS_LOCAL_FULL_SPATIAL_DEGREE4_40_EULER_JET",
            "full-spatial solve result is not a PASS receipt")
    require(result_record["solution_sha256"] == sha256(NEW_SOLUTION),
            "full-spatial solution SHA-256 mismatch")
    require(result_record["prior_four_sector_solution_sha256"] ==
            sha256(OLD_SOLUTION),
            "prior four-sector solution SHA-256 mismatch")

    old_matrix = s.Matrix([[s.Rational(value) for value in row]
                           for row in old_record["matrix"]])
    old_link_monomials = c.monomials(5)
    old_coframe_monomials = c.monomials(4)
    old_n_link = 24 * len(old_link_monomials)
    old_n_coframe = 16 * len(old_coframe_monomials)
    require(old_matrix.shape == (old_n_link + old_n_coframe, len(SECTORS)),
            "prior exact solution has an unexpected shape")

    link_monomials = c.monomials(6)
    coframe_monomials = c.monomials(5)
    n_link = 24 * len(link_monomials)
    n_coframe = 16 * len(coframe_monomials)
    require(new_record["amplitude"] == list(MIXED),
            "saved mixed solution has the wrong amplitude sector")
    require(new_record["link_spatial_degree_at_most"] == 6 and
            new_record["coframe_spatial_degree_at_most"] == 5,
            "saved mixed solution has the wrong spatial support")
    new_solution = s.Matrix([s.Rational(value)
                             for value in new_record["solution"]])
    require(new_solution.shape == (n_link + n_coframe, 1),
            "saved mixed solution has an unexpected length")
    require(all(value.is_Rational for value in new_solution),
            "saved mixed solution contains non-rational entries")

    A, B = (1, 0), (0, 1)
    point, cubic_cache, cubic_modes, kernel_parameters = \
        restricted.source_profile(A, B)
    zero_kernel = {parameter: s.Integer(0) for parameter in kernel_parameters}
    cubic_cache = freeze_cache(cubic_cache, zero_kernel)
    cubic_modes = freeze_modes(cubic_modes, zero_kernel)

    old_gamma_fields = []
    old_coframe_solutions = {}
    for column, amplitude in enumerate(SECTORS):
        if amplitude == MIXED:
            continue
        old_gamma_fields.append(c.gamma_field(
            {amplitude: old_matrix[:old_n_link, column]}, old_link_monomials))
        old_coframe_solutions[amplitude] = old_matrix[old_n_link:, column]
    old_gamma = c.merge_gamma_fields(*old_gamma_fields)
    mixed_gamma = c.gamma_field(
        {MIXED: new_solution[:n_link]}, link_monomials)
    final_gamma = c.merge_gamma_fields(old_gamma, mixed_gamma)
    final_cache = restricted.add_quartic_links(cubic_cache, final_gamma)
    old_coframe = c.coframe_field(old_coframe_solutions,
                                  old_coframe_monomials)
    mixed_coframe = c.coframe_field(
        {MIXED: new_solution[n_link:]}, coframe_monomials)

    def modes(site):
        result = cubic_modes(site)
        for field in (old_coframe, mixed_coframe):
            for key, value in field(site).items():
                result[key] = s.expand(result.get(key, 0) + value)
        return result

    link_rows = c.link_rows(point, final_cache, A, B, cubic=True,
                            coframe_modes=modes)
    coframe_rows = c.solder_rows(point, final_cache, A, B, cubic=True,
                                 coframe_modes=modes)
    checks = {}
    for amplitude in c.monomials(4):
        failures = []
        for row_index, row in enumerate(link_rows + coframe_rows):
            polynomial = s.Poly(s.expand(row.coeff(amplitude)), c.X, c.Y)
            if not polynomial.is_zero:
                failures.append({
                    "row": row_index,
                    "spatial_degree": polynomial.total_degree(),
                    "terms": [
                        {"monomial": list(monomial), "coefficient": str(coefficient)}
                        for monomial, coefficient in polynomial.terms()
                    ],
                })
        checks[f"{amplitude[0]},{amplitude[1]}"] = {
            "exactly_zero_all_spatial_degrees": not failures,
            "failure_row_count": len(failures),
            "failures": failures,
        }
    all_zero = all(result["exactly_zero_all_spatial_degrees"]
                   for result in checks.values())
    c.check_lorentz_links(final_cache(point))
    report = {
        "schema": "d0-exact-replay-result/v1",
        "status": "PASS_DIRECT_FULL_SPATIAL_EULER_REPLAY" if all_zero else
                  "FAIL_DIRECT_FULL_SPATIAL_EULER_REPLAY",
        "input_solution_sha256": sha256(NEW_SOLUTION),
        "prior_four_sector_solution_sha256": sha256(OLD_SOLUTION),
        "all_15_amplitude_monomials_checked": len(checks),
        "all_40_euler_rows_all_spatial_coefficients_zero": all_zero,
        "proper_lorentz_links_through_amplitude_degree_four": True,
        "checks": checks,
        "GR_closed": False,
    }
    print(json.dumps(report, indent=2))
    require(all_zero, "saved quartic vector leaves a full-polynomial Euler residual")


if __name__ == "__main__":
    main()
