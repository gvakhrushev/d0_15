#!/usr/bin/env python3
"""Cross-owner test: does the exact AF price minimizer enter engine support?"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
PREPARATION_PATH = "02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16/preparation.py"
PRICE_PATH = "02_REGISTRY/research/sources/d0_jacobian_controlled_record_2026-10-16/controlled_record.py"
ROLE_CHECKER_PATH = "02_REGISTRY/research/certificates/a4d_native_af_role_orbit_metric_check.py"
ROLE_RESULT_PATH = "02_REGISTRY/research/certificates/a4d_native_af_role_orbit_metric_results.json"
RESULT_PATH = Path(__file__).with_name("a4d_native_preparation_engine_admission_results.json")
ROLE_NOTE_PATH = "02_REGISTRY/research/A4D_NATIVE_AF_ROLE_ORBIT_CAR_GEOMETRY_2026-10-16.md"
PINS = {
    PREPARATION_PATH: "1e3c00dc0e28503e8c9103daf6ce3583f0500d65b64ee7bc4baf8e1bf4726ffd",
    PRICE_PATH: "dd3b7aa6f661dbef4117b2913e62136447a14e2d08a16b08b325cb688874f4ff",
    ROLE_CHECKER_PATH: "b718a3ea3e3f47087b664cc9bb194e0e09c5ae818836efdba3e63b9c11e4f2d5",
    ROLE_RESULT_PATH: "ad3630ea297bb6ec6d8e5481fa5e3ffd6ee8fd2c9a81108da679d5f0e016f53c",
    ROLE_NOTE_PATH: "7a14491f4c14a24f7e44aa0ffefddad2a5b21c9ccd33a8f20f90a829289369b1",
}


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_preparation(repo: Path):
    spec = importlib.util.spec_from_file_location(
        "preparation_engine_admission_owned_definition", repo/PREPARATION_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("preparation_owner_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def f0_interval(e, p, a, ell, iv):
    """Outward interval evaluation of the exact owner conditional price."""
    w, v2, r2 = a*p, p**4, iv.sqrt(2)
    fine0 = ((w*iv.sqrt(1-e)+iv.sqrt(e)/r2)**2,
             (w*iv.sqrt(1-e)-iv.sqrt(e)/r2)**2,
             w*w*(1-e))
    fine1 = (v2*(1-e), v2*(1-e))
    fine = fine0+fine1
    reference = (p**3, p**3, p**3, p**4, p**4)
    require(all(value > 0 for value in fine), "all_optimizer_fixture_probabilities_positive")
    return sum(value*iv.log(value/ref)
               for value, ref in zip(fine, reference))/ell


def run_checks(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def check(condition: object, name: str) -> None:
        require(condition, name)
        checks.append(name)

    for relative, digest in PINS.items():
        check(sha256(repo/relative) == digest, "pinned_owner:"+relative)

    preparation = load_preparation(repo)
    AF, price = preparation.owners(repo)
    role = json.loads((repo/ROLE_RESULT_PATH).read_text())
    check(role["exact_controls"] == 1887, "fresh_role_orbit_exact_control_count")
    for relative, digest in role["owner_sha256"].items():
        check(sha256(repo/relative) == digest, "role_orbit_receipt_owner:"+relative)
    check(sha256(repo/ROLE_NOTE_PATH) == role["note_sha256"],
          "role_orbit_receipt_note_fresh")
    check(sha256(repo/ROLE_CHECKER_PATH) == role["checker_sha256"],
          "role_orbit_receipt_checker_fresh")

    interface = role["AF_engine_cross_owner_joint_sector"]["complete_A1_activation_interface"]
    check(interface["activation_to_CAR_map_rank"] == 4 and
          interface["engine_support_constraint_rank"] == 3,
          "owned_AF_CAR_engine_support_ranks")
    kernel = interface["engine_support_kernel_basis"]
    check(kernel == [["1", "0", "0", "1", "0"],
                     ["0", "0", "0", "0", "1"]],
          "owned_support_preimage_is_M2_trace_plus_M1_scalar")

    ell = s.Symbol("log_phi", positive=True)
    for label, e in (("9_25", s.Rational(9, 25)),
                     ("16_25", s.Rational(16, 25))):
        fine = price.conditional_probabilities(AF, 0, e)
        w, v2 = AF.a*AF.p, AF.p**4
        expected0 = ((w*s.sqrt(1-e)+s.sqrt(e)/s.sqrt(2))**2,
                     (w*s.sqrt(1-e)-s.sqrt(e)/s.sqrt(2))**2,
                     w**2*(1-e))
        expected1 = (v2*(1-e), v2*(1-e))
        check(all(AF.zero(x-y) for x, y in zip(fine[0], expected0)) and
              all(AF.zero(x-y) for x, y in zip(fine[1], expected1)),
              "literal_owner_probabilities_"+label)
        check(AF.zero(sum(fine[0]+fine[1])-1),
              "literal_owner_probability_normalization_"+label)
        kl = (sum(x*s.log(x) for x in fine[0]+fine[1])/ell
              +3*sum(fine[0])+4*sum(fine[1]))
        check(AF.zero(price.conditional_old_price(AF, 0, e, ell)-kl),
              "conditional_price_is_actual_PF_KL_"+label)

    # Reuse the actual optimizer construction on the same coherent effect
    # fixture as preparation.py: the M2 eigenvalues are 9/25 and 16/25.
    U = s.Matrix([[3, 4*s.I], [4*s.I, 3]])/5
    resolutions = ((U, (s.Rational(9, 25), s.Rational(16, 25))),
                   (s.eye(1), (s.Rational(9, 25),)))
    optimum = preparation.faithful_preparation(AF, price, 1, resolutions, ell)
    rho_eigenbasis = s.simplify(U.H*optimum["density"][0]*U)
    f9 = s.simplify((U.H*optimum["conditional_cost"][0]*U)[0, 0])
    f16 = s.simplify((U.H*optimum["conditional_cost"][0]*U)[1, 1])
    symbolic_ratio = s.simplify(rho_eigenbasis[0, 0]/rho_eigenbasis[1, 1])
    expected_ratio = s.exp(-ell*(f9-f16))
    check(s.simplify(symbolic_ratio-expected_ratio) == 0,
          "optimizer_density_ratio_is_exact_price_exponential")

    from mpmath import iv
    old_dps = iv.dps
    iv.dps = 60
    try:
        p = (iv.sqrt(5)-1)/2
        a, ell_iv = iv.sqrt(p), -iv.log(p)
        f9_iv = f0_interval(iv.mpf(9)/25, p, a, ell_iv, iv)
        f16_iv = f0_interval(iv.mpf(16)/25, p, a, ell_iv, iv)
        check(f9_iv > iv.mpf("1.08684529796154") and
              f9_iv < iv.mpf("1.08684529796155"),
              "conditional_price_9_over_25_strict_interval")
        check(f16_iv > iv.mpf("1.15165203585467") and
              f16_iv < iv.mpf("1.15165203585469"),
              "conditional_price_16_over_25_strict_interval")
        delta = f9_iv-f16_iv
        density_ratio = iv.exp(-ell_iv*delta)
        singular_ratio = iv.sqrt(density_ratio)
        check(delta > iv.mpf("-0.0648068") and
              delta < iv.mpf("-0.0648067"),
              "conditional_costs_are_strictly_unequal_interval")
        check(density_ratio > iv.mpf("1.0316771") and
              density_ratio < iv.mpf("1.0316772"),
              "optimizer_density_eigenvalues_are_unequal_interval")
        check(singular_ratio > iv.mpf("1.0157150") and
              singular_ratio < iv.mpf("1.0157152"),
              "all_optimizer_amplitude_lifts_have_unequal_singular_values")
    finally:
        iv.dps = old_dps

    check(interface["physical_admission_of_full_A1_family_derived"] is False and
          role["physical_scope"]["native_q_D_b_m_binding"] is False,
          "scope_stays_inside_named_engine_interface")
    return {
        "status": "PASS",
        "exact_checks": len(checks),
        "effect_spectrum_M2": ["9/25", "16/25"],
        "f0_9_over_25_interval": str(f9_iv),
        "f0_16_over_25_interval": str(f16_iv),
        "difference_interval": str(delta),
        "optimizer_density_eigenvalue_ratio": str(density_ratio),
        "optimizer_GNS_amplitude_singular_value_ratio": str(singular_ratio),
        "engine_support_input_kernel": kernel,
        "optimizer_right_unitary_orbit_intersects_named_engine_support": False,
        "scope": "one coherent effect fixture and the named AF-to-CAR engine support; no global native or GR no-go",
        "checks": checks,
    }


if __name__ == "__main__":
    result = run_checks()
    expected = json.loads(RESULT_PATH.read_text())
    if result != expected:
        raise ArithmeticError("cross-owner certificate result mismatch")
    print(json.dumps(result, sort_keys=True))
