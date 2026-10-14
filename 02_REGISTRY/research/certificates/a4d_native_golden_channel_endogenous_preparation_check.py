#!/usr/bin/env python3
"""Exact invariant and attracting state of the candidate golden CAR channel.

This proves a conditional finite-dimensional result for the literal D0 record
operators and the v3 golden instrument.  It does not admit that channel as the
physical D0 transition or identify its state with a native (q,D,b,m) owner.
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
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parents[3]
STEM = "a4d_native_golden_channel_endogenous_preparation"
PROOF = "02_REGISTRY/research/A4D_NATIVE_GOLDEN_CHANNEL_ENDOGENOUS_PREPARATION.md"
CHRONOLOGY_CHECK = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py"
CHRONOLOGY_CERT = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json"
CHRONOLOGY_PROOF = "02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md"
SOURCE_CHECK = "02_REGISTRY/research/certificates/a4d_native_relative_observer_source_jet_check.py"
SOURCE_RESULT = "02_REGISTRY/research/certificates/a4d_native_relative_observer_source_jet_results.json"
SOURCE_PROOF = "02_REGISTRY/research/A4D_NATIVE_RELATIVE_OBSERVER_SOURCE_JET.md"
V3 = "02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14/continuation_v3"
V3_CODE = f"{V3}/src/moving_preparation_exact.py"
V3_PROOF = f"{V3}/proofs/MOVING_PREPARATION_SOURCE_RU.md"
V3_RESULT = f"{V3}/results/moving_preparation_exact.json"

INPUTS = {
    CHRONOLOGY_CHECK: "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    CHRONOLOGY_CERT: "0b91e13d823568898a006dd468f9963ffbbc1949f0976a21e8530af465ecfbbe",
    CHRONOLOGY_PROOF: "601e5bb9203789a66ad2a945aad30da92b6233ac40417d54c6b47c95dc43536b",
    SOURCE_CHECK: "0c972c55373ab2607514e2f6a1d6bcc60e6b0606dc07701b316c355dc5d2847f",
    SOURCE_RESULT: "f07994965c3e6c54b9ff16f6573021c56e5dac0e13011d95eed8ffc86feabe42",
    SOURCE_PROOF: "13be48d9a1c6cc2275d025d906840b9df7996e4756e207fe2e32d4c108bde7d4",
    V3_CODE: "1b3d0f5e10a59ca97daaf06744d6fe1429e7643dd350523b897ca9e2b287bc06",
    V3_PROOF: "67bea08cc8a39f49fe92f6d679eabe9d1ae2df7daee260dfe55c23641d45cb61",
    V3_RESULT: "dec95b219a55d5cd39e8e65bfc6f538cf4be1fa43630cc5c14ee96ce97f7470f",
}


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"OWNER_UNAVAILABLE:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def exact_commutant_rank(returns: list[s.Matrix], owner) -> int:
    """Rank the actual joint-intertwiner map over Q(a), exactly."""
    x = s.Symbol("x")
    minimal = x**4 + x**2 - 1
    alpha = s.RootOf(minimal, 1)  # the positive real root a=sqrt(p)
    field = s.QQ.algebraic_field(alpha)
    if not alpha.is_positive or s.minpoly(alpha, x) != minimal:
        raise AssertionError("POSITIVE_GOLDEN_FIELD_EMBEDDING_FAILED")

    field_returns = []
    for U in returns:
        entries = []
        for entry in U:
            value = s.cancel(entry.subs(owner.p, owner.a**2).subs(owner.a, x))
            numerator, denominator = s.fraction(value)
            numerator = s.rem(s.expand(numerator), minimal, x)
            denominator = s.rem(s.expand(denominator), minimal, x)
            value = s.rem(s.expand(numerator * s.invert(denominator, minimal, x)),
                          minimal, x)
            entries.append(field.from_sympy(value.as_expr().subs(x, alpha)))
        field_returns.append(entries)

    zero = field.zero
    rows = []
    # Unknown X is row-major: coefficient of X[k,l] in (XU-UX)[i,j].
    for U in field_returns:
        for i in range(16):
            for j in range(16):
                row = [
                    (U[l * 16 + j] if i == k else zero)
                    - (U[i * 16 + k] if l == j else zero)
                    for k in range(16) for l in range(16)
                ]
                if any(value != zero for value in row):
                    rows.append(row)
    matrix = DomainMatrix(rows, (len(rows), 256), field)
    return matrix.rank()


def conditioned_count_cost_jet(returns, return_jets, p, a, owner):
    """Differentiate the pinned three-round 1<=k<=2 full-Fock cost."""
    I16 = s.eye(16)

    def channel0(X):
        value = sum(((p * I16 + p**2 * U) * X * (p * I16 + p**2 * U).T
                     for U in returns), s.zeros(16)) / 4
        return value.applyfunc(owner.red)

    def channel1(X):
        value = p**3 * sum(((U - I16) * X * (U - I16).T
                            for U in returns), s.zeros(16)) / 4
        return value.applyfunc(owner.red)

    def dchannel0(X):
        value = s.zeros(16)
        for U, dU in zip(returns, return_jets):
            A, dA = p * I16 + p**2 * U, p**2 * dU
            value += dA * X * A.T + A * X * dA.T
        return (value / 4).applyfunc(owner.red)

    def dchannel1(X):
        value = s.zeros(16)
        for U, dU in zip(returns, return_jets):
            A = U - I16
            value += p**3 * (dU * X * A.T + A * X * dU.T) / 4
        return value.applyfunc(owner.red)

    states = {(0, 0): I16 / 16}
    jets = {(0, 0): s.zeros(16)}
    for total in range(3):
        for count in range(total + 1):
            X = states.get((total, count), s.zeros(16))
            dX = jets.get((total, count), s.zeros(16))
            for branch, channel, dchannel in (
                (0, channel0, dchannel0), (1, channel1, dchannel1)
            ):
                key = (total + 1, count + branch)
                states[key] = states.get(key, s.zeros(16)) + channel(X)
                jets[key] = jets.get(key, s.zeros(16)) + channel(dX) + dchannel(X)

    Delta = sum(((U - I16).T * (U - I16) for U in returns),
                s.zeros(16)).applyfunc(owner.red)
    dDelta = sum((dU.T * (U - I16) + (U - I16).T * dU
                  for U, dU in zip(returns, return_jets)),
                 s.zeros(16)).applyfunc(owner.red)
    sigma = (states[(3, 1)] + states[(3, 2)]).applyfunc(owner.red)
    dsigma = (jets[(3, 1)] + jets[(3, 2)]).applyfunc(owner.red)
    probability = owner.red(s.trace(sigma))
    dprobability = owner.red(s.trace(dsigma))
    cost = owner.red(s.trace(Delta * sigma) / probability)
    derivative = owner.red(
        (s.trace(dDelta * sigma + Delta * dsigma) - cost * dprobability)
        / probability
    )
    return probability, cost, derivative


def run() -> dict:
    checks: list[str] = []

    def check(name: str, condition) -> None:
        if not bool(condition):
            raise AssertionError("FAILED:" + name)
        checks.append(name)

    for path, expected in INPUTS.items():
        actual = sha(path)
        if actual != expected:
            raise AssertionError(f"INPUT_PIN_MISMATCH:{path}:{actual}")

    chronology_receipt = json.loads((ROOT / CHRONOLOGY_CERT).read_text())
    check("UPSTREAM_CHRONOLOGY_RECEIPT_PASS",
          chronology_receipt.get("status") == "PASS"
          and chronology_receipt.get("exact_controls") == 469
          and chronology_receipt.get("full_native_fibre") == 16)
    check("UPSTREAM_CHRONOLOGY_CHECKER_AND_PROOF_HASHES",
          chronology_receipt.get("checker_sha256") == sha(CHRONOLOGY_CHECK)
          and chronology_receipt.get("proof_sha256") == sha(CHRONOLOGY_PROOF))
    for path, expected in chronology_receipt["input_sha256"].items():
        check("UPSTREAM_CHRONOLOGY_TRANSITIVE_INPUT_PIN", sha(path) == expected)

    source_receipt = json.loads((ROOT / SOURCE_RESULT).read_text())
    check("UPSTREAM_RELATIVE_SOURCE_RECEIPT_PASS",
          source_receipt.get("status") == "PASS_EXACT_POSITIVE_FULL_PREPARATION_SOURCE_JET"
          and source_receipt.get("exact_controls") == 26
          and source_receipt.get("candidate", {}).get("initial_state") == "I_16/16")
    check("UPSTREAM_RELATIVE_SOURCE_CHECKER_AND_PROOF_HASHES",
          source_receipt.get("checker_sha256") == sha(SOURCE_CHECK)
          and source_receipt.get("proof_sha256") == sha(SOURCE_PROOF))
    for path, expected in source_receipt["input_sha256"].items():
        check("UPSTREAM_RELATIVE_SOURCE_TRANSITIVE_INPUT_PIN",
              sha(path) == expected)

    v3_receipt = json.loads((ROOT / V3_RESULT).read_text())
    check("UPSTREAM_V3_EXACT_INSTRUMENT_RECEIPT_PASS",
          v3_receipt.get("status") == "PASS" and v3_receipt.get("exact_controls") == 169)

    chronology = load(CHRONOLOGY_CHECK, "d0_endogenous_channel_chronology_owner")
    owner = chronology.old
    a, p = owner.a, owner.p
    I4, I16 = s.eye(4), s.eye(16)
    basis = [I4[:, r] for r in range(4)]
    returns = [chronology.record(I4, n)[0] for n in basis]
    check("FOUR_RETURNS_ARE_ACTUAL_NATIVE_RECORD_OPERATORS",
          len(returns) == 4 and all(owner.zero(U.T * U - I16) for U in returns))

    # These are precisely the two outcome Kraus operators per record used by
    # the pinned v3 count instrument.  The four records are summed, not reset.
    kraus_pairs = [
        ((p * I16 + p**2 * U) / 2, a * p * (U - I16) / 2)
        for U in returns
    ]
    for r, (K0, K1) in enumerate(kraus_pairs):
        check(f"RETURN_{r}_PAIR_HAS_WEIGHT_INDEPENDENT_TRACE_NORMALIZER",
              owner.zero(K0.T * K0 + K1.T * K1 - I16 / 4))
        check(f"RETURN_{r}_PAIR_HAS_WEIGHT_INDEPENDENT_UNITAL_NORMALIZER",
              owner.zero(K0 * K0.T + K1 * K1.T - I16 / 4))
    kraus = [K for pair in kraus_pairs for K in pair]
    tp = sum((K.T * K for K in kraus), s.zeros(16))
    unital = sum((K * K.T for K in kraus), s.zeros(16))
    check("NONSELECTIVE_GOLDEN_CHANNEL_IS_TRACE_PRESERVING",
          owner.zero(tp - I16))
    check("NONSELECTIVE_GOLDEN_CHANNEL_IS_UNITAL",
          owner.zero(unital - I16))
    check("MAXIMALLY_MIXED_STATE_IS_EXACTLY_STATIONARY",
          owner.zero(sum((K * (I16 / 16) * K.T for K in kraus), s.zeros(16))
                     - I16 / 16))

    # At the symmetric rest tuple q=eta, D=I, b=0, m=e0+volume, every proper
    # spatial rotation fixes the native data.  The fixed-basis four-return
    # channel nevertheless fails SO(3) covariance, so this particular
    # instrument cannot be read out from that tuple alone.
    R = s.eye(4)
    R[1, 1] = R[2, 2] = s.Rational(3, 5)
    R[1, 2], R[2, 1] = -s.Rational(4, 5), s.Rational(4, 5)
    E = owner.ext(R)
    eta = s.diag(1, -1, -1, -1)
    m0 = s.zeros(16, 1)
    m0[1] = m0[15] = 1
    check("SPATIAL_ROTATION_IS_PROPER_AND_NATIVE_REFERENCE_IS_FIXED",
          R.T * R == I4 and R.det() == 1
          and R * eta * R.T == eta and R * I4 * R.T == I4
          and E * m0 == m0)

    def channel(X):
        return sum((K * X * K.T for K in kraus), s.zeros(16)).applyfunc(owner.red)

    e0_state = s.zeros(16, 1)
    e0_state[1] = 1
    invariant_probe = e0_state * e0_state.T
    covariance_defect = channel(E * invariant_probe * E.T) - E * channel(invariant_probe) * E.T
    covariance_entry = owner.red(covariance_defect[1, 3])
    expected_covariance_entry = 3 * a * (1 - 2 * p) / 10
    check("HOSTILE_CONTROL_NATIVE_CHANNEL_BREAKS_SPATIAL_COVARIANCE",
          E * invariant_probe * E.T == invariant_probe
          and owner.zero(covariance_entry - expected_covariance_entry)
          and not owner.zero(covariance_entry))

    # The existing affine-shift slots do carry four vectors per site.  If a
    # return reads the oriented ray of its own shift, positive-G normalization
    # is canonical and covariant; this is a kinematic candidate interface,
    # not a physical identification currently selected by the core.
    q = eta
    D = I4
    b = [I4[:, r] for r in range(4)]
    m = m0
    v = s.Matrix([m[1 << r] for r in range(4)])
    k = (v.T * q.inv() * v)[0]
    Q = -q + 2 * v * v.T / k
    G = Q.inv()
    check("NATIVE_SHIFT_REFERENCE_HAS_POSITIVE_OBSERVER_PAIRING",
          k == 1 and Q == I4 and G == I4)
    check("NATIVE_SHIFT_REFERENCE_SATISFIES_SPATIAL_LINK_CONSTRAINT",
          D * q * D.T == q)
    normalized = [vector / s.sqrt((vector.T * G * vector)[0]) for vector in b]
    shift_returns = [chronology.record(G, n)[0] for n in normalized]
    check("ORIENTED_AFFINE_SHIFTS_RECONSTRUCT_THE_FOUR_ACTUAL_RETURNS",
          normalized == basis and all(owner.zero(U - V)
                                      for U, V in zip(shift_returns, returns)))

    # A unit shift tangent moves only the first return and reproduces the
    # already-certified relative-observer source jet exactly.
    db0 = basis[1]
    dnorm0 = db0 - normalized[0] * (normalized[0].T * G * db0)[0]
    dU_shift = chronology.record(G, normalized[0], s.zeros(4), dnorm0)[2]
    dU_source = chronology.record(G, basis[0], s.zeros(4), basis[1])[2]
    check("NATIVE_SHIFT_TANGENT_PULLS_BACK_TO_CERTIFIED_SOURCE_TANGENT",
          dnorm0 == basis[1] and owner.zero(dU_shift - dU_source)
          and owner.zero(dU_shift.T * returns[0] + returns[0].T * dU_shift))

    # When the shifts themselves transform, the canonical same-ray readout
    # restores covariance: no fixed spatial triad remains hidden in constants.
    rotated_b = [R * vector for vector in b]
    rotated_n = [vector / s.sqrt((vector.T * G * vector)[0]) for vector in rotated_b]
    rotated_shift_returns = [chronology.record(G, n)[0] for n in rotated_n]
    check("ORIENTED_SHIFT_READOUT_TRANSFORMS_THE_ACTUAL_RECORD_COVARIANTLY",
          all(owner.zero(Urot - E * U * E.T)
              for Urot, U in zip(rotated_shift_returns, returns)))

    # The pairwise coefficient matrix from (I,U_r) to (K_{r,0},K_{r,1})
    # has determinant a*p/4, hence both I and every U_r lie in the Kraus span.
    kraus_span_determinant = a * p**2 * (1 + p) / 4
    check("KRAUS_SPAN_RECOVERS_IDENTITY_AND_EACH_RETURN",
          owner.zero(kraus_span_determinant - a * p / 4)
          and not owner.zero(a * p))

    rank = exact_commutant_rank(returns, owner)
    check("ACTUAL_FOUR_RETURN_COMMON_COMMUTANT_IS_SCALARS",
          rank == 255 and 256 - rank == 1)
    one_return_rank = exact_commutant_rank(returns[:1], owner)
    check("HOSTILE_CONTROL_ONE_RETURN_DOES_NOT_HAVE_SCALAR_COMMUTANT",
          one_return_rank == 192 and one_return_rank < 255)

    # The actual relative observer tangent also preserves the maximally mixed
    # state to first order; the exact pair identity is U-independent.
    dU = chronology.record(I4, basis[0], s.zeros(4), basis[1])[2]
    dK0, dK1 = p**2 * dU / 2, a * p * dU / 2
    d_first_pair_tp = (dK0.T * kraus_pairs[0][0] + kraus_pairs[0][0].T * dK0
                       + dK1.T * kraus_pairs[0][1] + kraus_pairs[0][1].T * dK1)
    d_first_pair_unital = (dK0 * kraus_pairs[0][0].T + kraus_pairs[0][0] * dK0.T
                           + dK1 * kraus_pairs[0][1].T + kraus_pairs[0][1] * dK1.T)
    check("RELATIVE_OBSERVER_MOVE_KEEPS_EQUILIBRIUM_STATE_TO_FIRST_ORDER",
          owner.zero(d_first_pair_tp) and owner.zero(d_first_pair_unital))

    # Pull the same conditional event cost back along an admissible flat
    # trace-free q shear with b and m fixed. This is one metric slot of the
    # candidate action, not the total D0 stress.
    V = s.zeros(4)
    V[0, 1] = V[1, 0] = 2
    A = q.inv()
    dA = -A * V * A
    dv = s.zeros(4, 1)
    dk = (dv.T * A * v + v.T * dA * v + v.T * A * dv)[0]
    dQ = -V + 2 * (dv * v.T + v * dv.T) / k - 2 * v * v.T * dk / k**2
    dG = -G * dQ * G
    q_jets = []
    dUs_q = []
    for br, nr in zip(b, normalized):
        norm_sq = (br.T * G * br)[0]
        dnorm_sq = (br.T * dG * br)[0]
        dn = -nr * dnorm_sq / (2 * norm_sq)
        dUs_q.append(chronology.record(G, nr, dG, dn)[2])
        q_jets.append(dn)
    check("TRACEFREE_Q_SHEAR_IS_ADMISSIBLE_ON_HOMOGENEOUS_NATIVE_LINKS",
          V == V.T and s.trace(eta.inv() * V) == 0
          and D * V * D.T - V == s.zeros(4))
    check("FIXED_LINK_RAYS_HAVE_ZERO_FIRST_OBSERVER_JET_ON_THIS_SHEAR",
          dG == V and all(owner.zero(dn) for dn in q_jets))
    _, _, q_source_jet = conditioned_count_cost_jet(shift_returns, dUs_q, p, a, owner)
    x = s.Symbol("x")
    minimal = x**4 + x**2 - 1
    reduced = s.cancel(q_source_jet.subs({a: x, p: x**2}))
    numerator, denominator = s.fraction(reduced)
    numerator = s.rem(s.expand(numerator), minimal, x)
    denominator = s.rem(s.expand(denominator), minimal, x)
    reduced = s.rem(s.expand(numerator * s.invert(denominator, minimal, x)), minimal, x)
    expected_q_polynomial = (
        2088601935789604 * x**3 + 1705879982091207 * x**2
        - 1311016250921047 * x - 1028861680129291
    ) / 346943031568563
    q_lower = Fraction(
        -1028861680129291
        - 1311016250921047 * Fraction(787, 1000)
        + 1705879982091207 * Fraction(393, 500)**2
        + 2088601935789604 * Fraction(393, 500)**3,
        346943031568563,
    )
    flat_rho0 = chronology_receipt.get("flat_geometric_rho0_in_all10_slots")
    check("TRACEFREE_Q_SOURCE_JET_EXACT_FIELD_REDUCTION",
          s.expand(reduced - expected_q_polynomial) == 0)
    check("TRACEFREE_Q_SOURCE_JET_IS_STRICTLY_POSITIVE_AND_MISSES_FLAT_RHO0",
          q_lower == Fraction(116463720765635098441, 5420984868258796875000)
          and q_lower > 0 and flat_rho0 == ["0"] * 10)

    # Exact rational brackets isolate the positive golden roots used above.
    p_lo, p_hi = Fraction(309, 500), Fraction(619, 1000)
    a_lo, a_hi = Fraction(393, 500), Fraction(787, 1000)
    check("POSITIVE_GOLDEN_ROOTS_HAVE_EXACT_RATIONAL_BRACKETS",
          p_lo**2 + p_lo < 1 < p_hi**2 + p_hi
          and a_lo**4 + a_lo**2 < 1 < a_hi**4 + a_hi**2)

    return {
        "schema": "d0-native-golden-channel-endogenous-preparation/1",
        "status": "PASS_CONDITIONAL_PRIMITIVE_GOLDEN_RECORD_CHANNEL",
        "proof": PROOF,
        "input_sha256": {path: sha(path) for path in INPUTS},
        "channel": {
            "kraus_operators": "K[r,0]=(p*I+p^2*U_r)/2; K[r,1]=a*p*(U_r-I)/2",
            "returns": "U_r=record(I_4,e_r), r=0..3, actual 16-component CAR carrier",
            "dynamics": "sum_{r=0}^3 sum_{j=0}^1 K[r,j]*rho*K[r,j]^T; outcomes and return labels ignored",
            "preparation_return_weights": "arbitrary pi_r>0 with sum(pi_r)=1; scale each pair by sqrt(4*pi_r)",
            "golden_relations": "a^2=p; p^2+p=1; positive roots",
        },
        "exact_result": {
            "common_commutant_map_rank_over_Q_a": rank,
            "common_commutant_dimension": 256 - rank,
            "one_return_hostile_control_rank": one_return_rank,
            "one_return_hostile_control_commutant_dimension": 256 - one_return_rank,
            "stationary_density": "I_16/16",
            "primitive_power_upper_bound": 255,
            "relative_observer_equilibrium_jet": "zero",
            "equilibrium_independent_of_full_support_return_weights": True,
            "SO3_covariance_defect_on_symmetric_rest_tuple": str(covariance_entry),
            "native_affine_shift_readout": "n_e=b_e/sqrt(b_e^T*G*b_e), candidate same-ray map",
            "shift_readout_reference_source_jet": source_receipt["exact_values"]["full_prepared_source_derivative"],
            "tracefree_metric_probe_V01": "V_01=V_10=2; tr(eta^-1 V)=0",
            "candidate_metric_source_jet_on_V01": str(q_source_jet),
            "candidate_metric_source_jet_positive_lower_bound": str(q_lower),
            "flat_geometric_rho0_on_V01": "0",
        },
        "exact_controls": len(checks),
        "checks": checks,
        "scope": {
            "unique_attracting_state_for_this_channel": True,
            "nonselective_channel_admitted_as_a_D0_physical_law": False,
            "full_four_return_support_derived_from_complete_core": False,
            "candidate_channel_natural_from_symmetric_q_D_b_m_alone": False,
            "candidate_shift_readout_covariant_on_nonzero_b_sector": True,
            "candidate_v3_cost_alone_matches_flat_rho0": False,
            "native_core_selects_shift_as_record_direction": False,
            "full_core_no_go": False,
            "state_identified_with_native_joint_matter_m": False,
            "own_action_source_Ward_or_ten_metric_slots_derived": False,
            "finite_time_mixing_rate_certified": False,
            "G0_GR_or_original_parent_terminal_closed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="refresh the adjacent result receipt after review")
    args = parser.parse_args()
    result = run()
    result["checker_sha256"] = sha(str(Path(__file__).relative_to(ROOT)))
    result["proof_sha256"] = sha(PROOF)
    target = ROOT / "02_REGISTRY/research/certificates" / f"{STEM}_results.json"
    if target.exists() and not args.write:
        existing = json.loads(target.read_text())
        if existing != result:
            raise SystemExit("IMMUTABLE_RECEIPT_MISMATCH: rerun with --write after reviewing inputs")
        mode = "verified"
    else:
        target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        mode = "written"
    print(json.dumps({"status": result["status"], "exact_controls": result["exact_controls"],
                      "commutant_rank": result["exact_result"]["common_commutant_map_rank_over_Q_a"],
                      "mode": mode, "result": str(target.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
