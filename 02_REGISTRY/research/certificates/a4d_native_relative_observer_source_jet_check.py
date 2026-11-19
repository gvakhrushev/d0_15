#!/usr/bin/env python3
"""Exact v3 count-source jet for a relative native CAR observer rotation.

This certifies one candidate composition, not its physical admission by D0.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
STEM = "a4d_native_relative_observer_source_jet"
PROOF = "02_REGISTRY/research/A4D_NATIVE_RELATIVE_OBSERVER_SOURCE_JET.md"
CHRONOLOGY = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py"
CHRONOLOGY_CERT = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json"
PURE_FRAME_RESULT = "02_REGISTRY/research/certificates/a4d_native_coframe_record_frame_jet_results.json"
V3 = "02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14/continuation_v3"
INPUTS = {
    "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py": "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json": "0b91e13d823568898a006dd468f9963ffbbc1949f0976a21e8530af465ecfbbe",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py": "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_certificate.json": "8cba34862bf6af48c8c49d75c5e3a5a2a80948f9f0bf2e1818c42f43b370a238",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_results.json": "4c28dd449b844e5a8332d56d457c2bbcd83853069563542dc12f0238439510a8",
    "02_REGISTRY/research/A4D_NATIVE_COFRAME_RECORD_FRAME_JET_BOUNDARY.md": "91b036e6c8b793bce1597b64041b50185acf3a9877507b756a8e9bcddec1699f",
    "02_REGISTRY/research/certificates/a4d_native_coframe_record_frame_jet_check.py": "c21d75f46bc456dfbf23f7874bda3d8cd89a876f56f73f486c995d35ae029edf",
    "02_REGISTRY/research/certificates/a4d_native_coframe_record_frame_jet_results.json": "9f2ffde6f17a9cd1b6c46817450b86d7b77c6130155d501e15ee773c1d71fa02",
    f"{V3}/src/moving_preparation_exact.py": "1b3d0f5e10a59ca97daaf06744d6fe1429e7643dd350523b897ca9e2b287bc06",
    f"{V3}/proofs/MOVING_PREPARATION_SOURCE_RU.md": "67bea08cc8a39f49fe92f6d679eabe9d1ae2df7daee260dfe55c23641d45cb61",
    f"{V3}/results/moving_preparation_exact.json": "dec95b219a55d5cd39e8e65bfc6f538cf4be1fa43630cc5c14ee96ce97f7470f",
}

P_EXACT = "-102*a*p + 63*a + 255*p/8 - 309/16"
DP_EXACT = "221/16 - 179*p/8"
S_EXACT = "(9856*a*p - 6084*a + 8044*p - 4990)/(544*a*p - 336*a - 170*p + 103)"
DS_EXACT = "(-17097116*a*p + 10566598*a + 9221682*p - 5699312)/(1233792*a*p - 762528*a + 3019248*p - 1865985)"
DS_REDUCED = (
    "2*(418298977134234*A**3 + 47136853411765*A**2 "
    "- 266996949536729*A - 17948253838120)/346943031568563"
)


def sha(path: str | Path) -> str:
    target = Path(path)
    if not target.is_absolute():
        target = ROOT / target
    return hashlib.sha256(target.read_bytes()).hexdigest()


def load_chronology():
    path = ROOT / CHRONOLOGY
    spec = importlib.util.spec_from_file_location("d0_native_record_chronology_source", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("NATIVE_RECORD_CHRONOLOGY_OWNER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_v3_reducer():
    path = ROOT / V3 / "src/moving_preparation_exact.py"
    spec = importlib.util.spec_from_file_location("d0_v3_moving_preparation_source", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("V3_MOVING_PREPARATION_SOURCE_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.red


def reduce_to_a(expression, p, a, symbol):
    polynomial = symbol**4 + symbol**2 - 1
    expression = s.cancel(expression.subs({p: symbol**2, a: symbol}))
    numerator, denominator = s.fraction(expression)
    numerator = s.rem(numerator, polynomial, symbol)
    denominator = s.rem(denominator, polynomial, symbol)
    inverse = s.invert(denominator, polynomial, symbol)
    return s.rem(s.expand(numerator * inverse), polynomial, symbol)


def run() -> dict:
    for path, expected in INPUTS.items():
        actual = sha(path)
        if actual != expected:
            raise AssertionError(f"INPUT_PIN_MISMATCH:{path}:{actual}")

    chronology_cert = json.loads((ROOT / CHRONOLOGY_CERT).read_text())
    if chronology_cert.get("status") != "PASS" or chronology_cert.get("full_native_fibre") != 16:
        raise AssertionError("NATIVE_RECORD_CHRONOLOGY_RECEIPT_NOT_PASS")
    for path, expected in chronology_cert["input_sha256"].items():
        if sha(path) != expected:
            raise AssertionError(f"CHRONOLOGY_TRANSITIVE_PIN_MISMATCH:{path}")
    v3_receipt = json.loads((ROOT / V3 / "results/moving_preparation_exact.json").read_text())
    if v3_receipt.get("status") != "PASS" or v3_receipt.get("exact_controls") != 169:
        raise AssertionError("V3_SOURCE_RECEIPT_NOT_PASS")
    pure_frame_receipt = json.loads((ROOT / PURE_FRAME_RESULT).read_text())
    if (pure_frame_receipt.get("status") != "PASS_PURE_FRAME_METRIC_JETS_NULL_RELATIVE_OBSERVER_OPEN"
            or pure_frame_receipt.get("exact_controls") != 108):
        raise AssertionError("PURE_FRAME_NULL_RECEIPT_NOT_PASS")

    owner = load_chronology()
    red = owner.red
    zero = owner.old.zero
    p, a = owner.old.p, owner.old.a
    reduce = load_v3_reducer()
    I4, I16 = s.eye(4), s.eye(16)
    G = I4
    observers = [I4[:, r] for r in range(4)]
    returns = [owner.record(G, n)[0] for n in observers]
    dUs = [owner.record(G, observers[0], s.zeros(4), observers[1])[2]] + [
        s.zeros(16) for _ in range(3)
    ]

    checks: list[str] = []
    negatives: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not bool(condition):
            raise AssertionError("FAILED:" + name)
        checks.append(name)

    def reject(name: str, false_claim: bool) -> None:
        check("REJECT_" + name, false_claim)
        negatives.append(name)

    check("PURE_FRAME_NULL_RESULT_CONSUMED", pure_frame_receipt["status"]
          == "PASS_PURE_FRAME_METRIC_JETS_NULL_RELATIVE_OBSERVER_OPEN")
    for path, expected in pure_frame_receipt["input_sha256"].items():
        check("PURE_FRAME_TRANSITIVE_INPUT_PIN", sha(path) == expected)

    check("FOUR_ACTUAL_NATIVE_FULL_FOCK_RETURNS_ORTHOGONAL",
          all(zero(U.T * U - I16) for U in returns))
    noncommuting_pairs = [
        [i, j] for i in range(4) for j in range(i)
        if not zero(returns[i] * returns[j] - returns[j] * returns[i])
    ]
    check("REFERENCE_HAS_NONCOMMUTING_RETURNS", bool(noncommuting_pairs))
    check("RELATIVE_OBSERVER_PATH_IS_TANGENT_TO_UNIT_SPHERE",
          (observers[0].T * G * observers[1])[0] == 0)
    check("NATIVE_RELATIVE_RETURN_JET_IS_UNITARY",
          zero(dUs[0].T * returns[0] + returns[0].T * dUs[0]))

    kraus0 = [(p * I16 + p**2 * U) / 2 for U in returns]
    kraus1 = [a * p * (U - I16) / 2 for U in returns]
    completeness = sum((A0.T * A0 + A1.T * A1 for A0, A1 in zip(kraus0, kraus1)), s.zeros(16))
    check("FOUR_GOLDEN_KRAUS_PAIRS_ARE_TRACE_PRESERVING", zero(completeness - I16))

    def channel0(X):
        value = sum(((p * I16 + p**2 * U) * X * (p * I16 + p**2 * U).T
                     for U in returns), s.zeros(16)) / 4
        return value.applyfunc(red)

    def channel1(X):
        value = p**3 * sum(((U - I16) * X * (U - I16).T for U in returns), s.zeros(16)) / 4
        return value.applyfunc(red)

    def dchannel0(X):
        value = s.zeros(16)
        for U, dU in zip(returns, dUs):
            A, dA = p * I16 + p**2 * U, p**2 * dU
            value += dA * X * A.T + A * X * dA.T
        return (value / 4).applyfunc(red)

    def dchannel1(X):
        value = s.zeros(16)
        for U, dU in zip(returns, dUs):
            A = U - I16
            value += p**3 * (dU * X * A.T + A * X * dU.T) / 4
        return value.applyfunc(red)

    states = {(0, 0): I16 / 16}
    jets = {(0, 0): s.zeros(16)}
    for total in range(3):
        for count in range(total + 1):
            X = states.get((total, count), s.zeros(16))
            dX = jets.get((total, count), s.zeros(16))
            for branch, channel, dchannel in ((0, channel0, dchannel0), (1, channel1, dchannel1)):
                key = (total + 1, count + branch)
                states[key] = states.get(key, s.zeros(16)) + channel(X)
                jets[key] = jets.get(key, s.zeros(16)) + channel(dX) + dchannel(X)

    Delta = sum(((U - I16).T * (U - I16) for U in returns), s.zeros(16)).applyfunc(red)
    dDelta = sum((dU.T * (U - I16) + (U - I16).T * dU
                  for U, dU in zip(returns, dUs)), s.zeros(16)).applyfunc(red)
    sigma = (states[(3, 1)] + states[(3, 2)]).applyfunc(red)
    dsigma = (jets[(3, 1)] + jets[(3, 2)]).applyfunc(red)
    probability = red(s.trace(sigma))
    dprobability = red(s.trace(dsigma))
    prepared = red(s.trace(Delta * sigma) / probability)
    source = red((s.trace(dDelta * sigma + Delta * dsigma)
                  - prepared * dprobability) / probability)
    rho = sigma / probability
    frozen_state_source = red(s.trace(dDelta * rho))
    omitted_normalizer_source = red(s.trace(dDelta * sigma + Delta * dsigma) / probability)

    expected_probability = -102 * a * p + 63 * a + s.Rational(255, 8) * p - s.Rational(309, 16)
    expected_dprobability = s.Rational(221, 16) - s.Rational(179, 8) * p
    expected_prepared = (9856 * a * p - 6084 * a + 8044 * p - 4990) / (
        544 * a * p - 336 * a - 170 * p + 103
    )
    expected_source = (-17097116 * a * p + 10566598 * a + 9221682 * p - 5699312) / (
        1233792 * a * p - 762528 * a + 3019248 * p - 1865985
    )
    check("EXACT_EVENT_PROBABILITY", zero(probability - expected_probability))
    check("EXACT_EVENT_PROBABILITY_DERIVATIVE", zero(dprobability - expected_dprobability))
    check("EXACT_NORMALIZED_REFERENCE_COST", zero(prepared - expected_prepared))
    check("EXACT_FULL_PREPARED_SOURCE_JET", zero(source - expected_source))
    reject("SOURCE_JET_VANISHES", not zero(source))
    reject("FREEZE_PREPARED_STATE", not zero(source - frozen_state_source))
    reject("DROP_EVENT_NORMALIZATION_DERIVATIVE", not zero(source - omitted_normalizer_source))
    check("TOTAL_COUNT_STATE_TRACE_IS_ONE", zero(sum(s.trace(states[(3, k)]) for k in range(4)) - 1))
    check("TOTAL_COUNT_STATE_JET_TRACE_IS_ZERO", zero(sum(s.trace(jets[(3, k)]) for k in range(4))))

    # Exact rational intervals certify Z_A>0 and the sign of the reduced jet.
    p_lo, p_hi = Fraction(309, 500), Fraction(619, 1000)
    a_lo, a_hi = Fraction(393, 500), Fraction(787, 1000)
    check("GOLDEN_ROOT_INTERVALS_EXACT",
          p_lo**2 + p_lo < 1 < p_hi**2 + p_hi
          and a_lo**2 < p_lo and a_hi**2 > p_hi)
    prob_lower = -102 * a_hi * p_hi + 63 * a_lo + Fraction(255, 8) * p_lo - Fraction(309, 16)
    prob_upper = -102 * a_lo * p_lo + 63 * a_hi + Fraction(255, 8) * p_hi - Fraction(309, 16)
    check("EVENT_PROBABILITY_STRICTLY_POSITIVE_BY_RATIONAL_INTERVAL",
          prob_lower == Fraction(53661, 250000) and prob_lower > 0 and prob_upper < 1)

    A = s.Symbol("A")
    reduced_source = reduce_to_a(source, p, a, A)
    q_poly = (418298977134234 * A**3 + 47136853411765 * A**2
              - 266996949536729 * A - 17948253838120)
    expected_reduced = s.expand(2 * q_poly / 346943031568563)
    check("EXACT_DEGREE_FOUR_FIELD_REDUCTION", reduced_source == expected_reduced)
    q_lower = (418298977134234 * a_lo**3 + 47136853411765 * a_lo**2
               - 266996949536729 * a_hi - 17948253838120)
    check("SOURCE_JET_STRICTLY_POSITIVE_BY_RATIONAL_INTERVAL",
          q_lower == Fraction(260432886291208272219, 62500000) and q_lower > 0)

    return {
        "schema": "d0-native-relative-observer-source-jet/1",
        "status": "PASS_EXACT_POSITIVE_FULL_PREPARATION_SOURCE_JET",
        "input_sha256": {path: sha(path) for path in INPUTS},
        "proof_sha256": sha(PROOF),
        "checker_sha256": sha(Path(__file__)),
        "candidate": {
            "returns": "record(I_4,e_r), r=0..3, on the actual 16D full-Fock carrier",
            "relative_variation": "n_0(t)=cos(t)e_0+sin(t)e_1; other returns fixed",
            "initial_state": "I_16/16",
            "rounds": 3,
            "fixed_event": "1<=error_count<=2",
            "v3_commuting_reference_theorem_used": False,
        },
        "exact_values": {
            "event_probability": P_EXACT,
            "event_probability_derivative": DP_EXACT,
            "reference_prepared_cost": S_EXACT,
            "full_prepared_source_derivative": DS_EXACT,
            "reduced_source_derivative": DS_REDUCED,
            "event_probability_rational_lower_bound": "53661/250000",
            "source_polynomial_rational_lower_bound_numerator": "260432886291208272219/62500000",
        },
        "checks": checks,
        "exact_controls": len(checks),
        "negative_controls": negatives,
        "scope": {
            "native_record_operator_used": True,
            "four_native_observer_records_physically_admitted_as_v3_returns": False,
            "nonzero_relative_observer_prepared_cost_jet": True,
            "pure_common_frame_metric_source": "ZERO_BY_SEPARATE_EXACT_CERTIFICATE",
            "source_subtracted_metric_cotangent_or_rho0_projection": False,
            "D0_native_action_or_joint_Ward_derived": False,
            "curved_native_root_or_GR_derived": False,
            "new_Lean_declarations": 0,
            "G0_closed": False,
            "original_parent_terminals_changed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    destination = ROOT / "02_REGISTRY/research/certificates" / f"{STEM}_results.json"
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        destination.write_text(encoded)
    elif not destination.exists() or destination.read_text() != encoded:
        raise AssertionError("IMMUTABLE_RECEIPT_MISMATCH; use --write only after reviewing the exact result")
    print(f"PASS_NATIVE_RELATIVE_OBSERVER_SOURCE_JET controls={result['exact_controls']}")
    print("the actual full-Fock count recursion gives a positive exact source jet; physical admission remains open")


if __name__ == "__main__":
    main()
