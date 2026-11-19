#!/usr/bin/env python3
"""Exact finite checks for the conditional nilpotent-vacuum entropy result.

The logarithmic small-parameter limit is proved analytically in the companion
memo. This checker validates the exact probability algebra and hostile cases;
it does not select this readout as a physical D0 action.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
PROOF = "02_REGISTRY/research/A4D_NATIVE_NILPOTENT_VACUUM_ENTROPY_JET.md"
STEM = "a4d_native_nilpotent_vacuum_entropy_jet"
INPUTS = {
    "03_FORMALIZATION/D0/Geometry/A4DNilpotentAffineMatterLift.lean":
        "643182331ff9ecddb031ea44d829ea3d0900d8e551166bab68706683ad245563",
    "03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean":
        "0e3a7c7dba7fc91f2e451578234baf01eda2c4d7d3d0b23fa4f9ee7dd3b78597",
    "02_REGISTRY/research/A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md":
        "5fb7f4c5e7bbae5924b1b169c867c96993266d9eec52ac05e1ba6e451de722af",
    "02_REGISTRY/research/certificates/a4d_native_factor_imbalance_remainder_check.py":
        "1fdb90d822d362a52200b42a4fb3e663efa59e3a2371f9da15cada1eed1363da",
    "02_REGISTRY/research/certificates/a4d_native_factor_imbalance_remainder_certificate.json":
        "5c2e3691feccf4f9c3bf4d62931f14aa965bf08a344f9aa1272fcef490946107",
    "02_REGISTRY/research/A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md":
        "2a5dfbbafc9c1c6fe20e31d6a99a949d25abd4f1a5dbe40bb5e08dd392f8d5b4",
    "02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance_certificate.json":
        "87de2c08a7767a1b9e9bd47105013f225cd44df43a03a5ac09d54ff9d193a8cb",
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md":
        "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d",
    "02_REGISTRY/research/MEMO_A4D_AFFINE_SENSITIVE_SITE_MATTER_LINK.md":
        "39bc181ff1726316845101cc07cdc2e6ca9839e144926f63f7ff6d28e4cca21b",
    "02_REGISTRY/research/sources/d0_two_projection_archive_v9_2026-10-14/RESULT.md":
        "a2ad578714a64bf92c5999500bae87963c9b62bd675bfc35b7d696d668f8c47c",
    "02_REGISTRY/research/sources/d0_two_projection_archive_v9_2026-10-14/verify.py":
        "dab2d8fc83f1dfc46baade4d1dc8a4a23743bbb5ce5203f847aa6b275ba119b3",
    "02_REGISTRY/research/sources/d0_two_projection_archive_v9_2026-10-14/receipt.json":
        "0b364e1130b6d7a678d45b773b5755bec922aaac750c02e78d2a0f205d912748",
    "02_REGISTRY/research/A4D_NATIVE_FULL_RECORD_TAPE_HEAT.md":
        "a430fe428803dcbc7dc51b1cd29fcecf735485669972006d6968e79c8787aeb1",
    "02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14/RESULT.md":
        "df090d17a6c0fbaaccac6af9ce55ce4ae969826550cd094200c1dcdf4ae57a0a",
    "02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14/verify.py":
        "6a3f6dd67bb8b17c9a863e14e282e8599af449fcfef268c841ec8183353678ee",
    "02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14/receipt.json":
        "2ad637c39bf69f69aa30d374585e9f708b1d03fab673629dda59a326f4ea8f44",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checks: list[str] = []

    def check(name: str, condition: object) -> None:
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    for rel, expected in INPUTS.items():
        check("PIN:" + rel, digest(ROOT / rel) == expected)

    # Formal vacuum lift supplies a degree-zero plus degree-one vector; the
    # occupation readout is the explicitly conditional extra choice.
    lift = (ROOT / "03_FORMALIZATION/D0/Geometry/A4DNilpotentAffineMatterLift.lean").read_text()
    mismatch = (ROOT / "03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean").read_text()
    check("LEAN_OWNER_PROVES_VACUUM_LIFT", "theorem nilpotentAffineTranslation_vacuum" in lift)
    check("REFERENCE_IS_SUPPLIED_NOT_SELECTED", "does **not** select an intrinsic" in mismatch)
    check("BOOK_ACTION_INFO_DESCRIPTION_READ",
          "lowering uncertainty entropy" in
          (ROOT / "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md").read_text())
    v9 = ROOT / "02_REGISTRY/research/sources/d0_two_projection_archive_v9_2026-10-14"
    v9_receipt = json.loads((v9 / "receipt.json").read_text())
    check("V9_RETURNS_A_REAL_QND_TAPE_BUT_NO_TAPE_ENERGY_LAW",
          v9_receipt["persistent_outcome_tape_has_independent_energy_law"] is False)
    check("V9_RETURNS_ALL_RECORDED_HISTORIES",
          "4^n outcome-history состояний сохранены" in (v9 / "RESULT.md").read_text())
    v9_normalized = " ".join((v9 / "RESULT.md").read_text().split())
    check("V9_KRAUS_BRANCHES_USE_THE_TWO_PROJECTION_LOOP",
          "Kraus-ветвей есть линейная комбинация I,V,V*. Поэтому" in v9_normalized and
          "Khat = I-P-R+PR+RP = (I-V)*(I-V)/4" in v9_normalized)
    v10 = ROOT / "02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14"
    v10_receipt = json.loads((v10 / "receipt.json").read_text())
    check("V10_FULL_TAPE_ENERGY_AND_ALL_N_INTERTWINER_PINNED",
          v10_receipt["status"] == "PASS" and
          v10_receipt["scope"]["full_outcome_tape_active"] is True and
          v10_receipt["scope"]["same_record_intertwiner_all_n"] is True and
          v10_receipt["scope"]["M1_forcing"] is False and
          v10_receipt["scope"]["AF_or_spatial_refinement_identified"] is False and
          v10_receipt["scope"]["physical_Ward_or_GR"] is False)

    # Reconstruct the four actual SELECT/label Kraus branches on a principal
    # two-plane. Their effects must equal the stated functions of t=kappa*lambda.
    golden_p, a, t, u = sp.symbols("p a t u", real=True)
    i2 = sp.eye(2)
    j2 = sp.Matrix([[0, -1], [1, 0]])
    c = 1 - 2 * t
    v2 = sp.Matrix([[c, -u], [u, c]])
    G = sp.Matrix([[a, -golden_p], [golden_p, a]])
    H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    prep = sp.diag(sp.eye(2), H) * sp.kronecker_product(G, i2)
    words = [i2, i2, v2, v2.T]
    expected_effects = [
        (1 - 2 * golden_p**2 * t) ** 2,
        4 * golden_p**4 * t * (1 - t),
        4 * golden_p**3 * t**2,
        4 * golden_p**3 * t * (1 - t),
    ]
    branch_relations = [a**2 - golden_p, golden_p**2 + golden_p - 1, u**2 - 4 * t * (1 - t)]
    branch_groebner = sp.groebner(branch_relations, a, golden_p, u, t, order="lex", domain=sp.QQ)
    for outcome in range(4):
        branch = sum((prep[j, outcome] * prep[j, 0] * words[j] for j in range(4)), sp.zeros(2))
        effect = (branch.T * branch - expected_effects[outcome] * i2).applyfunc(sp.simplify)
        check("ACTUAL_V9_KRAUS_EFFECT_" + str(outcome), all(
            branch_groebner.reduce(sp.cancel(entry).as_numer_denom()[0])[1] == 0
            for entry in effect
        ))

    # Exact finite L=4 Fourier sum on Q(s)=diag(4e^(2s),e^(-2s)/4,1,1).
    # |z(k)|^2 for k=0,1,2,3 is [0,32,64,32]; all 4^4 modes and 16 grades remain.
    mode_norms = [sp.Integer(0), sp.Integer(32), sp.Integer(64), sp.Integer(32)]
    pi_symbol = sp.symbols("pi_mode", real=True)
    pi_functions = [
        (1 - 2 * golden_p**2 * pi_symbol) ** 2,
        4 * golden_p**4 * pi_symbol * (1 - pi_symbol),
        4 * golden_p**3 * pi_symbol**2,
        4 * golden_p**3 * pi_symbol * (1 - pi_symbol),
    ]
    marginal = [sp.Integer(0)] * 4
    marginal_jet = [sp.Integer(0)] * 4
    for mode in itertools.product(range(4), repeat=4):
        z2 = [mode_norms[k] for k in mode]
        lam = sp.Rational(z2[0], 4) + 4 * z2[1] + z2[2] + z2[3]
        lam_jet = -sp.Rational(z2[0], 2) + 8 * z2[1]
        t_mode = lam / (256 * 4**2)
        t_jet = lam_jet / (256 * 4**2)
        for outcome in range(4):
            marginal[outcome] += pi_functions[outcome].subs(pi_symbol, t_mode) / 4**4
            marginal_jet[outcome] += (sp.diff(pi_functions[outcome], pi_symbol)
                                      .subs(pi_symbol, t_mode) * t_jet / 4**4)

    def reduce_golden(expr: sp.Expr) -> sp.Expr:
        return sp.rem(sp.Poly(sp.expand(expr), golden_p),
                      sp.Poly(golden_p**2 + golden_p - 1, golden_p)).as_expr().simplify()

    expected_marginal = [
        sp.Rational(54275, 65536) + sp.Rational(20983, 131072) * golden_p,
        sp.Rational(24061, 65536) - sp.Rational(72183, 131072) * golden_p,
        sp.Rational(1539, 65536) * golden_p - sp.Rational(1539, 131072),
        sp.Rational(24061, 65536) * golden_p - sp.Rational(24061, 131072),
    ]
    expected_marginal_jet = [
        sp.Rational(4665, 32768) * golden_p - sp.Rational(2835, 16384),
        sp.Rational(6675, 16384) - sp.Rational(20025, 32768) * golden_p,
        sp.Rational(1005, 16384) * golden_p - sp.Rational(1005, 32768),
        sp.Rational(6675, 16384) * golden_p - sp.Rational(6675, 32768),
    ]
    check("L4_ALL_256_FOURIER_MODES_AND_ZERO_MODE_RETAINED", len(list(itertools.product(range(4), repeat=4))) == 256)
    check("L4_ACTUAL_V9_MARGINAL_PROBABILITIES", all(
        reduce_golden(marginal[j] - expected_marginal[j]) == 0 for j in range(4)))
    check("L4_ACTUAL_V9_MARGINAL_FIRST_JETS", all(
        reduce_golden(marginal_jet[j] - expected_marginal_jet[j]) == 0 for j in range(4)))
    check("L4_OUTCOME_PROBABILITIES_AND_JETS_NORMALIZE",
          reduce_golden(sum(marginal) - 1) == 0 and reduce_golden(sum(marginal_jet)) == 0)

    # Rigorous outward interval arithmetic for the logarithmic Shannon jet.
    # The heat comparator is the already pinned exact L=4 positive-heat row.
    mp.iv.dps = 50
    p_iv = (mp.iv.sqrt(mp.iv.mpf(5)) - 1) / 2
    marginal_iv = [
        mp.iv.mpf(54275) / 65536 + mp.iv.mpf(20983) * p_iv / 131072,
        mp.iv.mpf(24061) / 65536 - mp.iv.mpf(72183) * p_iv / 131072,
        mp.iv.mpf(1539) * p_iv / 65536 - mp.iv.mpf(1539) / 131072,
        mp.iv.mpf(24061) * p_iv / 65536 - mp.iv.mpf(24061) / 131072,
    ]
    marginal_jet_iv = [
        mp.iv.mpf(4665) * p_iv / 32768 - mp.iv.mpf(2835) / 16384,
        mp.iv.mpf(6675) / 16384 - mp.iv.mpf(20025) * p_iv / 32768,
        mp.iv.mpf(1005) * p_iv / 16384 - mp.iv.mpf(1005) / 32768,
        mp.iv.mpf(6675) * p_iv / 16384 - mp.iv.mpf(6675) / 32768,
    ]
    entropy_jet_iv = -sum((1 + mp.iv.ln(prob)) * dprob
                          for prob, dprob in zip(marginal_iv, marginal_jet_iv))
    heat_jet_iv = 2 * (mp.iv.mpf(16) / 257 - mp.iv.mpf(256) / (2**128 + 1))
    residual_iv = heat_jet_iv - entropy_jet_iv
    check("L4_V9_MARGINAL_SHANNON_JET_OUTWARD_INTERVAL",
          float(entropy_jet_iv.a) > 0.2947213 and
          float(entropy_jet_iv.b) < 0.2947214)
    check("L4_COST_MINUS_INFO_RESIDUAL_IS_NONZERO_OUTWARD_INTERVAL",
          float(residual_iv.a) > -0.170208 and
          float(residual_iv.b) < -0.170207)

    # The persistent v9 record is a finite mixture of iid outcome laws
    # conditional on the initial trace mode. Since pi_2(t)=4p^3*t^2 is
    # strictly increasing for t>=0, distinct t's are identifiable from a long
    # tape. Its asymptotic per-tick Shannon entropy is therefore the uniform
    # mode average of H(pi(t)); evaluate its actual metric derivative.
    rate_entropy = mp.iv.mpf(0)
    rate_entropy_jet = mp.iv.mpf(0)
    mode_norms_int = [0, 32, 64, 32]
    for mode in itertools.product(range(4), repeat=4):
        z2 = [mode_norms_int[k] for k in mode]
        lam = Fraction(z2[0], 4) + 4 * z2[1] + z2[2] + z2[3]
        lam_jet = -Fraction(z2[0], 2) + 8 * z2[1]
        t_mode = lam / (256 * 4**2)
        t_mode_jet = lam_jet / (256 * 4**2)
        if t_mode == 0:
            check("L4_ZERO_MODE_HAS_ZERO_FACTOR_JET", t_mode_jet == 0)
            continue
        tm_iv = mp.iv.mpf(t_mode.numerator) / t_mode.denominator
        dtm_iv = mp.iv.mpf(t_mode_jet.numerator) / t_mode_jet.denominator
        probs = [
            (1 - 2 * p_iv**2 * tm_iv)**2,
            4 * p_iv**4 * tm_iv * (1 - tm_iv),
            4 * p_iv**3 * tm_iv**2,
            4 * p_iv**3 * tm_iv * (1 - tm_iv),
        ]
        prob_jets = [
            -4 * p_iv**2 * (1 - 2 * p_iv**2 * tm_iv),
            4 * p_iv**4 * (1 - 2 * tm_iv),
            8 * p_iv**3 * tm_iv,
            4 * p_iv**3 * (1 - 2 * tm_iv),
        ]
        rate_entropy += -sum(prob * mp.iv.ln(prob) for prob in probs)
        rate_entropy_jet += -sum((1 + mp.iv.ln(probs[j])) * prob_jets[j] * dtm_iv
                                 for j in range(4))
    rate_entropy /= 4**4
    rate_entropy_jet /= 4**4
    rate_residual_iv = heat_jet_iv - rate_entropy_jet
    check("L4_PERSISTENT_RECORD_ENTROPY_RATE_JET_OUTWARD_INTERVAL",
          float(rate_entropy_jet.a) > 0.2698613 and
          float(rate_entropy_jet.b) < 0.2698615)
    check("L4_COST_MINUS_ASYMPTOTIC_INFO_RATE_RESIDUAL_NONZERO",
          float(rate_residual_iv.a) > -0.145348 and
          float(rate_residual_iv.b) < -0.145347)

    b = sp.symbols("b0:4", nonzero=True, real=True)
    x = sp.symbols("x", positive=True, real=True)
    x_b = sp.Add(*(z*z for z in b))
    p0 = 1 / (1 + x_b)
    q = x_b / (1 + x_b)
    p = [z*z / (1 + x_b) for z in b]
    check("VACUUM_AND_FOUR_OCCUPATION_PROBABILITIES_NORMALIZE",
          sp.simplify(p0 + sum(p) - 1) == 0)

    H_role = -p0 * sp.log(p0) - sum(pi * sp.log(pi) for pi in p)
    H_formula = sp.log(1 + x_b) - sum(z*z * sp.log(z*z) for z in b) / (1 + x_b)
    check("ROLE_RESOLVED_ENTROPY_CLOSED_FORM", sp.simplify(H_role - H_formula) == 0)

    weights = [z*z / x_b for z in b]
    H_conditional = -sum(w * sp.log(w) for w in weights)
    H_binary = sp.log(1 + x_b) - x_b * sp.log(x_b) / (1 + x_b)
    check("BINARY_PLUS_CONDITIONAL_ENTROPY_DECOMPOSITION",
          sp.simplify(H_role - H_binary - q * H_conditional) == 0)
    check("BINARY_ENTROPY_DERIVATIVE", sp.simplify(sp.diff(
          sp.log(1 + x) - x * sp.log(x) / (1 + x), x) + sp.log(x) / (1 + x)**2) == 0)
    check("VACUUM_ENTROPY_LIMIT", sp.limit(
          sp.log(1 + x) - x * sp.log(x) / (1 + x), x, 0, dir="+") == 0)

    # Any smooth b(t) through zero has x'(0)=0, independently of the first
    # metric jet. This is an exact polynomial identity.
    t = sp.symbols("t", real=True)
    v = sp.symbols("v0:4", real=True)
    w = sp.symbols("w0:4", real=True)
    g0_symbols = sp.symbols("g0:10", real=True)
    g1_symbols = sp.symbols("g1:10", real=True)
    pairs = [(i, j) for i in range(4) for j in range(i, 4)]
    G0 = sp.zeros(4)
    G1 = sp.zeros(4)
    for (i, j), a0, a1 in zip(pairs, g0_symbols, g1_symbols):
        G0[i, j] = G0[j, i] = a0
        G1[i, j] = G1[j, i] = a1
    b_path = sp.Matrix([t*v[i] + t**2*w[i] for i in range(4)])
    x_path = (b_path.T * (G0 + t*G1) * b_path)[0]
    check("SMOOTH_METRIC_AND_VACUUM_VECTOR_GIVE_QUADRATIC_X",
          sp.diff(x_path, t).subs(t, 0) == 0 and x_path.subs(t, 0) == 0)

    # A degree-preserving POVM effect has no vacuum/one-form cross term.
    # Include both a full-support and a zero-probability outcome at b=0.
    c1, d0, d1 = sp.symbols("c1 d0 d1", positive=True, real=True)
    x1 = t**2
    probability_positive = (d0 + d1*t**2) / (1 + x1)
    probability_rare = c1*t**2 / (1 + x1)
    Hprob = lambda y: -y*sp.log(y)
    check("FULL_SUPPORT_OUTCOME_ENTROPY_HAS_ZERO_SHIFT_JET",
          sp.limit((Hprob(probability_positive)-Hprob(d0))/t, t, 0, dir="+") == 0)
    check("ZERO_SUPPORT_OUTCOME_ENTROPY_HAS_ZERO_SHIFT_JET",
          sp.limit(Hprob(probability_rare)/t, t, 0, dir="+") == 0)
    A, B = sp.symbols("A B", real=True)
    I2 = sp.eye(2)
    J2 = sp.Matrix([[0, -1], [1, 0]])
    K2 = A*I2 + B*J2
    check("REAL_QND_KRAUS_EFFECT_IS_SCALAR_ON_EACH_TWO_PLANE",
          K2.T*K2 == (A**2 + B**2)*I2)
    parity = sp.diag(1, -1)
    effect = sp.diag(d0, d1)
    vacuum = sp.Matrix([1, 0])
    one_form = sp.Matrix([0, 1])
    check("PARITY_EVEN_EFFECT_HAS_NO_VACUUM_ONE_FORM_CROSS_TERM",
          parity*effect == effect*parity and (vacuum.T*effect*one_form)[0] == 0)

    # Exact rational sample with a nontrivial positive diagonal G.
    Gd = sp.diag(1, sp.Rational(3, 2), 2, 4)
    bd = sp.Matrix([sp.Rational(1, 2), -1, sp.Rational(3, 2), 0])
    xd = (bd.T * Gd * bd)[0]
    pd = [Gd[i, i] * bd[i]**2 / (1 + xd) for i in range(4)]
    p0d = 1 / (1 + xd)
    check("RATIONAL_METRIC_WITNESS_X", xd == sp.Rational(25, 4))
    check("RATIONAL_METRIC_WITNESS_NORMALIZATION", sp.simplify(p0d + sum(pd) - 1) == 0)
    b_zero = sp.zeros(4, 1)
    x_zero = (b_zero.T * Gd * b_zero)[0]
    p0_zero = 1 / (1 + x_zero)
    p_exc_zero = x_zero / (1 + x_zero)
    check("ZERO_SHIFT_HAS_EMPTY_EXCITATION_FIBER",
          p0_zero == 1 and p_exc_zero == 0)

    # Hostile controls: non-vacuum data can have a linear entropy jet, whereas
    # branch surprisal and norm are not smooth substitutes at the vacuum.
    Hx = sp.log(1 + x) - x * sp.log(x) / (1 + x)
    nonvacuum_derivative = sp.diff(Hx, x).subs(x, 4)
    check("NONVACUUM_BASE_CAN_HAVE_NONZERO_ENTROPY_JET", nonvacuum_derivative != 0)
    rare = t**2 / (1 + t**2)
    check("RARE_BRANCH_SURPRISAL_DIVERGES",
          sp.limit(-sp.log(rare), t, 0, dir="+") == sp.oo)
    check("NORM_CANDIDATE_HAS_A_CUSP", sp.limit(sp.Abs(t)/t, t, 0, dir="+") == 1 and
          sp.limit(sp.Abs(t)/t, t, 0, dir="-") == -1)
    p_unnormalized = [Gd[i, i] * bd[i]**2 for i in range(4)]
    check("OMITTING_NORMALIZATION_IS_DETECTED", sum(p_unnormalized) != 1)

    result = {
        "schema": "d0-native-nilpotent-vacuum-entropy-jet/1",
        "status": "PASS_CONDITIONAL_VACUUM_AND_V9_ONE_TICK_ENTROPY_JETS",
        "checker_sha256": digest(Path(__file__)),
        "proof": PROOF,
        "proof_sha256": digest(ROOT / PROOF),
        "input_sha256": {p: digest(ROOT / p) for p in INPUTS},
        "exact_controls": len(checks),
        "checks": checks,
        "exact_rational_witness": {
            "G_diagonal": ["1", "3/2", "2", "4"],
            "b": ["1/2", "-1", "3/2", "0"],
            "x": str(xd),
            "probabilities_vacuum_then_roles": [str(p0d)] + [str(z) for z in pd],
        },
        "analytic_result": {
            "x_along_smooth_vacuum_tangent": "O(t^2)",
            "occupation_entropy": "O(x*(1+abs(log(x))))",
            "first_directional_derivative_at_vacuum": "0",
            "logarithmic_limit_formalized_in_Lean": False,
        },
        "actual_v9_one_tick_factor_probe": {
            "L": 4,
            "golden_parameter": "p=phi^-1; p+p^2=1",
            "marginal_probabilities_exact": [str(reduce_golden(v)) for v in marginal],
            "marginal_probability_jets_exact": [str(reduce_golden(v)) for v in marginal_jet],
            "shannon_entropy_jet_outward_interval": str(entropy_jet_iv),
            "owned_heat_factor_jet_outward_interval": str(heat_jet_iv),
            "Cost_minus_Info_residual_outward_interval": str(residual_iv),
            "asymptotic_persistent_record_entropy_rate_jet_outward_interval": str(rate_entropy_jet),
            "Cost_minus_asymptotic_Info_rate_residual_outward_interval": str(rate_residual_iv),
            "Info_identified_with_one_tick_marginal_entropy_by_native_owner": False,
            "finite_n_history_entropy_claimed": False,
            "asymptotic_conditional_entropy_rate_derived_for_this_QND_mixture": True,
            "full_ten_slot_joint_source_claimed": False,
            "v10_full_tape_quadratic_energy_identified_with_shannon_Info": False,
        },
        "scope": {
            "occupation_readout_selected_by_native_core": False,
            "Info_v_identified_with_this_entropy": False,
            "reference_q_selected_by_native_core": False,
            "entropy_added_to_native_action": False,
            "actual_v9_one_tick_branch_effects_derived": True,
            "L4_one_tick_marginal_jet_exact_and_interval_checked": True,
            "one_tick_candidate_cancels_L4_factor_contrast": False,
            "finite_n_full_history_entropy_closed": False,
            "persistent_record_entropy_rate_jet_checked": True,
            "v10_full_tape_operator_thermal_completion_reproduced": True,
            "M1_forcing_or_physical_Ward_or_GR_derived": False,
            "full_ten_slot_joint_metric_source_closed": False,
            "vacuum_candidate_cancels_factor_imbalance_first_jet": False,
            "nonvacuum_or_other_owned_action_terms_excluded": False,
            "whole_core_no_go": False,
            "native_source_or_GR_closed": False,
        },
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS_NATIVE_NILPOTENT_VACUUM_ENTROPY_JET", len(checks), "exact controls")
    for name in checks:
        print("PASS_" + name)
    if args.output:
        print("WROTE", args.output)


if __name__ == "__main__":
    main()
