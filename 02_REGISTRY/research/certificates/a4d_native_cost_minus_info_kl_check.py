#!/usr/bin/env python3
"""Conditional KL/source test for Shannon Info on the actual QND record.

This checks the exact fixed-T code/KL identity and an outward interval on the
inherited v10 root box. It does not select Shannon entropy as native Info.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
PROOF = "02_REGISTRY/research/A4D_NATIVE_COST_MINUS_INFO_KL_TEST.md"
STEM = "a4d_native_cost_minus_info_kl"
INPUTS = {
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md":
        "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d",
    "02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/RESULT.md":
        "92fecc34d44a6bb22a63d09073d861ef0f5accdb866b33d658c80eaa0944832b",
    "02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/verify.py":
        "d5660e27d0fe2a6f46472084de30ef197fb7a187ff27c269574032a1dd189491",
    "02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/receipt.json":
        "ca896fa704ebd8c44d81bc7be072a969b55d6c7835d74921c4259060ca7f31db",
    "02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14/RESULT.md":
        "df090d17a6c0fbaaccac6af9ce55ce4ae969826550cd094200c1dcdf4ae57a0a",
    "02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14/receipt.json":
        "2ad637c39bf69f69aa30d374585e9f708b1d03fab673629dda59a326f4ea8f44",
    "03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean":
        "692f2b5929b001361a2f22d7dc224fba46a80738036f26a1ff7bdd5175fc80c4",
    "02_REGISTRY/research/certificates/a4d_native_cost_minus_info_kl.lean":
        "ae2f4698d921c7b9788e8718abae62ac98c83e2439ea69109a10eb3675c3d9d5",
}
LEAN_OUTPUT = "02_REGISTRY/research/certificates/a4d_native_cost_minus_info_kl_output.txt"
LEAN_OUTPUT_SHA256 = "32babf7bb64b713180d481c87b4a2889087999749237da2fa03aa216ca74a9cc"
CHECKS: list[str] = []


def check(name: str, condition: bool) -> None:
    if not bool(condition):
        raise AssertionError(name)
    CHECKS.append(name)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symbolic() -> dict[str, str]:
    p, r, eps, gamma, kappa, T = sp.symbols(
        "p r eps gamma kappa T", positive=True
    )
    # p=phi^-1, so ln(phi)=-ln(p); p also obeys p^2+p=1.
    logphi = -sp.log(p)
    golden_poly = sp.Poly(p**2 + p - 1, p)
    bits = list(itertools.product((0, 1), repeat=3))
    check("EXACTLY_EIGHT_THREE_ROUND_WORDS", len(bits) == 8)
    ref_mass = sum(p ** (3 + sum(w)) for w in bits)
    ref_remainder = sp.rem(sp.Poly(sp.expand(ref_mass - 1), p), golden_poly).as_expr()
    check("GOLDEN_REFERENCE_NORMALIZES", sp.simplify(ref_remainder) == 0)

    q_mass = sum(r ** sum(w) * (1 - r) ** (3 - sum(w)) for w in bits)
    check("ACTUAL_IID_TAPE_NORMALIZES", sp.simplify(q_mass - 1) == 0)
    expected_length = sum(
        r ** sum(w) * (1 - r) ** (3 - sum(w)) * (3 + sum(w))
        for w in bits
    )
    check("ACTUAL_EXPECTED_CODE_LENGTH_IS_T_PLUS_TR",
          sp.simplify(expected_length - 3 * (1 + r)) == 0)

    # The actual tape entropy is the sum of the three iid conditional
    # increments. The net expected code length minus entropy is KL(q || mu).
    entropy_nats = -3 * ((1 - r) * sp.log(1 - r) + r * sp.log(r))
    net_nats = 3 * (1 + r) * logphi - entropy_nats
    kl_nats = 3 * (
        (1 - r) * sp.log((1 - r) / p) + r * sp.log(r / p**2)
    )
    check("COST_MINUS_SHANNON_IS_GOLDEN_KL",
          sp.simplify(sp.expand_log(net_nats - kl_nats, force=True)) == 0)

    dkl_dt = sp.diff(kl_nats / logphi, r) * (-2 * r)
    normalized = sp.simplify(dkl_dt.subs(r, gamma * kappa * eps) /
                              (3 * gamma * kappa))
    target = 2 * eps * sp.log(
        p * (1 - gamma * kappa * eps) / (gamma * kappa * eps)
    ) / logphi
    check("RADIAL_KL_DERIVATIVE_NORMALIZES_EXACTLY",
          sp.simplify(normalized - target) == 0)

    cost_source = -2 * eps
    info_action_source = 2 * eps * sp.log(
        (1 - gamma * kappa * eps) / (gamma * kappa * eps)
    ) / logphi
    combined = sp.simplify(cost_source + info_action_source)
    combined_target = target
    check("COST_AND_NEGATIVE_ENTROPY_SOURCE_MATCH_KL",
          sp.simplify(sp.expand_log(combined - combined_target, force=True)) == 0)

    matched_r = p**2
    matched_ratio = sp.cancel(matched_r / (p * (1 - matched_r)))
    matched_remainder = sp.rem(
        sp.Poly(sp.together(matched_ratio - 1).as_numer_denom()[0], p), golden_poly
    ).as_expr()
    check("REFERENCE_FIXED_POINT_IS_R_EQUALS_P_SQUARED",
          sp.simplify(matched_remainder) == 0)

    # A mixture of eigenmodes is not the iid Bernoulli law at its mean rate.
    q_mix_word = sp.Rational(1, 2) * (sp.Rational(1, 2) ** 2) * (1 - sp.Rational(1, 2))
    q_mean_word = (sp.Rational(1, 4) ** 2) * (1 - sp.Rational(1, 4))
    check("MIXTURE_IS_NOT_IID_AT_MEAN_RATE", q_mix_word != q_mean_word)

    owner_text = (ROOT / "03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean").read_text()
    owner_block = owner_text.split(
        "structure ActionProtocol (P : VerificationProtocol) where", 1
    )[1].split("/-- The canonical endogenous action quantum", 1)[0]
    owner_fields = re.findall(
        r"^\s{2}([A-Za-z][A-Za-z0-9_]*)\s*:", owner_block, re.MULTILINE
    )
    check("LEAN_ACTION_PROTOCOL_DOES_NOT_SELECT_INFO",
          owner_fields == ["action", "action_refl", "action_nontrivial"])

    return {
        "words": str(len(bits)),
        "code_cost_minus_info": "D_phi(q_r || mu)",
        "normalized_radial_derivative":
            "-2*epsilon*log_phi(r/(p*(1-r)))",
        "matched_reference_rate": "r=p^2",
        "mixture_scope_control": f"{q_mix_word} != {q_mean_word}",
    }


def intervals() -> dict[str, str]:
    iv = mp.iv
    iv.dps = 70
    p = (iv.sqrt(5) - 1) / 2
    phi = 1 / p
    gamma = 4 * p**3
    ell = iv.mpf(1) / 8
    kappa = ell**2 / 256

    v10_path = ROOT / "02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14/receipt.json"
    v10 = json.loads(v10_path.read_text())
    check("INHERITED_V10_RECEIPT_IS_PASS", v10["status"] == "PASS")
    check("INHERITED_V10_ROOT_IS_L8", v10["interval"]["parameters"]["L"] == 8)
    check("INHERITED_V10_ROOT_RADIUS_IS_PINNED",
          v10["interval"]["root_radius"] == "1e-12")

    center = v10["interval"]["root_center"][0]
    radius = mp.mpf(v10["interval"]["root_radius"])
    d0 = iv.mpf(center) + iv.mpf([str(-radius), str(radius)])
    epsilon = d0 * (128 - 64 * iv.sqrt(2))
    r = gamma * kappa * epsilon
    logphi = lambda x: iv.ln(x) / iv.ln(phi)

    cost_source = -2 * epsilon
    info_action_source = 2 * epsilon * logphi((1 - r) / r)
    net_source = cost_source + info_action_source
    kl_source = -2 * epsilon * logphi(r / (p * (1 - r)))

    check("V10_EPSILON8_INSIDE_CERTIFIED_ENCLOSURE",
          bool(epsilon > iv.mpf("2.3857044602")) and
          bool(epsilon < iv.mpf("2.3857044604")))
    check("ACTUAL_QND_ERROR_RATE_IS_INTERIOR",
          bool(r > 0) and bool(r < p**2))
    check("SHANNON_INFO_SOURCE_SHIFT_IS_STRICTLY_POSITIVE",
          bool(info_action_source > iv.mpf("88.16547511")) and
          bool(info_action_source < iv.mpf("88.16547512")))
    check("COST_MINUS_INFO_SOURCE_IS_NONZERO",
          bool(net_source > iv.mpf("83.39406619")) and
          bool(net_source < iv.mpf("83.39406620")))
    identity_residual = net_source - kl_source
    check("INTERVAL_KL_IDENTITY_CONTAINS_ZERO",
          bool(identity_residual.a <= 0) and bool(identity_residual.b >= 0))
    check("COST_ONLY_SOURCE_HAS_REGISTERED_SIGN", bool(cost_source < 0))

    fmt = lambda x: iv.nstr(x, 32)
    return {
        "d0_box_center": center,
        "d0_box_radius": v10["interval"]["root_radius"],
        "epsilon8": fmt(epsilon),
        "kappa": fmt(kappa),
        "gamma": fmt(gamma),
        "error_rate_r": fmt(r),
        "cost_only_radial_source": fmt(cost_source),
        "negative_entropy_source_shift": fmt(info_action_source),
        "conditional_cost_minus_info_source": fmt(net_source),
        "direct_kl_derivative": fmt(kl_source),
        "identity_residual": fmt(identity_residual),
    }


def run() -> dict:
    for rel, expected in INPUTS.items():
        actual = sha(ROOT / rel)
        check("PIN_" + rel, actual == expected)
    direct_receipt = json.loads(
        (ROOT / "02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/receipt.json").read_text()
    )
    check("DIRECT_ATTACK_RECEIPT_BINDS_PROOF",
          direct_receipt["proof_sha256"] == INPUTS[
              "02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/RESULT.md"
          ])
    lean_output = ROOT / LEAN_OUTPUT
    output_text = lean_output.read_text()
    check("LEAN_COMPILE_OUTPUT_HASH_PINNED", sha(lean_output) == LEAN_OUTPUT_SHA256)
    check("LEAN_COMPILE_OUTPUT_HAS_BOTH_PROPOSITIONS",
          "code_minus_info_eq_golden_kl" in output_text and
          "three_round_code_minus_info_eq_golden_kl" in output_text)
    check("LEAN_COMPILE_OUTPUT_HAS_NO_ERRORS_OR_SORRY",
          "error:" not in output_text and "sorryAx" not in output_text)
    check("LEAN_COMPILE_OUTPUT_AXIOMS_ARE_STANDARD",
          "depends on axioms: [propext, Classical.choice, Quot.sound]" in output_text and
          output_text.count("depends on axioms:") == 2)
    return {
        "schema": "d0-cost-minus-info-kl/1",
        "status": "PASS",
        "proof_sha256": sha(ROOT / PROOF),
        "checker_sha256": sha(Path(__file__)),
        "input_sha256": INPUTS,
        "lean_replay": {
            "status": "PASS",
            "command": "lake env lean ../02_REGISTRY/research/certificates/a4d_native_cost_minus_info_kl.lean",
            "command_cwd": "03_FORMALIZATION",
            "compiler_exit_code": 0,
            "output_sha256": LEAN_OUTPUT_SHA256,
            "sorryAx": False,
        },
        "symbolic": symbolic(),
        "interval": intervals(),
        "conditions": len(CHECKS),
        "scope": {
            "shannon_info_selected_by_native_owner": False,
            "actual_three_round_qnd_tape_used": True,
            "conditional_on_qnd_eigenstate": True,
            "native_joint_tangent_or_full_source_closed": False,
            "physical_ward_or_gr_closed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run()
    dest = ROOT / f"02_REGISTRY/research/certificates/{STEM}_results.json"
    if args.write:
        dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    else:
        expected = json.loads(dest.read_text())
        if report != expected:
            raise AssertionError("RESULT_RECEIPT_MISMATCH")
    print("PASS_COST_MINUS_INFO_KL", report["conditions"], "conditions")
    print("COST_ONLY_SOURCE", report["interval"]["cost_only_radial_source"])
    print("NEGATIVE_ENTROPY_SHIFT", report["interval"]["negative_entropy_source_shift"])
    print("COST_MINUS_INFO_SOURCE", report["interval"]["conditional_cost_minus_info_source"])


if __name__ == "__main__":
    main()
