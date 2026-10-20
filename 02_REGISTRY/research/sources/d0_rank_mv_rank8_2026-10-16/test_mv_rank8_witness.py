#!/usr/bin/env python3
"""Checks for the rank-8 witness. No assert: python -O must keep every check."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parent
CHECKER = ROOT / "check_mv_rank8_witness.py"
BANNED = (
    "d0_memory_rank_continuation_2026-10-16",
    "d0_native_memory_source_2026-10-16",
    "WRK-A4D-MV-FULL-RANK-SPAN",
    "mv_full_rank",
    "importlib",
)
CHECKS = []


def require(name, condition):
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def load_checker():
    spec = importlib.util.spec_from_file_location("mv_rank8_witness", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_rank_one(module):
    chi = module.pure_chi()
    witness = chi * chi.T - s.eye(16) / 16
    require("independent_chi_norm", (chi.T * chi)[0] == 1)
    require("independent_action", witness * chi == s.Rational(15, 16) * chi)
    require("independent_pairing", s.trace(witness * witness) == s.Rational(15, 16))
    require("independent_trace", s.trace(witness) == 0)


def main():
    source = CHECKER.read_text(encoding="utf-8")
    for token in BANNED:
        require("checker_does_not_mention_" + token, token not in source)
    module = load_checker()
    independent_rank_one(module)
    result = module.certify()
    require("candidate", result["status"] == "candidate")
    require("strictly_weaker", result["strictly_weaker"] is True)
    require("equation_28_holds", result["equation_28"]["holds"] is True)
    require("lambda_15_over_16", result["equation_28"]["lambda"] == "15/16")
    require("beta_zero", result["equation_28"]["beta"] == [0, 0, 0])
    require("beta_real", result["equation_28"]["coefficients_real"] is True)
    require("equation_26_fails", result["equation_26"]["holds_for_operator"] is False)
    require("pairing_15_over_16", result["equation_26"]["neutral_pairing"] == "15/16")
    require("span_implies_pure", result["equation_26_implies_equation_28"] is True)
    require("not_native_field_velocity", result["native_field_velocity"] is False)
    require("field_kernel_open", result["field_kernel_solved"] is False)
    require("no_nonlinear_branch", result["nonlinear_branch_constructed"] is False)
    require("gr_not_derived", result["gr_derived"] is False)
    require("r01_not_imported", result["r01_package_imported"] is False)
    require("pr_334_not_merged", result["pull_request_334_merged"] is False)
    require("thirty_two_exact_checks", result["exact_checks"] == 32)
    require("memo_chi", result["chi"] == "(e_mask1-e_mask15)/sqrt(2)")
    require("J_r_are_B_r", result["J_r_means"] == "memo B_r")
    print("PASS mv_rank8_witness %s" % len(CHECKS))


if __name__ == "__main__":
    main()
