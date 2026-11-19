#!/usr/bin/env python3
"""Bounded independent controls for the coupled cut-heat application.

No native PF/full128 census or existing all42 root is replayed. The full
finite-matrix fixture tests the operator identity and moving-cut pullback;
the actual Golden n20/refinement inputs are consumed through their proved
counts and reporter formulas. Absolute heat is retained; a separately named
constant-free evaluation is used only to avoid cancellation in differences.
"""

import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction

import numpy as np


getcontext().prec = 100
checks = []


def require(name, condition):
    if not bool(condition):
        raise RuntimeError(name)
    checks.append(name)


def dec(x):
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


P = (Decimal(5).sqrt() - 1) / 2
ZETA_Q = Fraction(1, 2**20)
ZETA = dec(ZETA_Q)
BETA = 2 * P**2
S = 128
M20 = fib(20) + 6 * fib(21)
W20_LOWER = fib(20) + 4 * fib(21)
DIM20_LOWER = M20 * W20_LOWER
ZMIN20 = M20 * (W20_LOWER - 2)
ETA_UPPER = Fraction(13, 5) / (64 * ZETA_Q * (1 - 2 * ZETA_Q) * ZMIN20)
require("original_n20_counts", (fib(20), fib(21), M20, W20_LOWER) == (6765, 10946, 72441, 50549))
require("conservative_harmonic_count", ZMIN20 == 3661675227)
require("exact_eta_less_than_one_over_80000", ETA_UPPER < Fraction(1, 80000))
require("coupled_uniform_value_bound", (1 - Fraction(1, 80000)) * Fraction(1681727, 25000000000) > Fraction(6726823, 10**11))
require("coupled_three_status_gain_bound", (1 - Fraction(1, 80000)) * Fraction(5665, 10000) > Fraction(56649, 100000))
p_lo = Fraction(6180339887498948482, 10**19)
p_hi = Fraction(6180339887498948483, 10**19)
require("rational_golden_bracket", p_lo*p_lo+p_lo < 1 < p_hi*p_hi+p_hi)
require("beta0_exact_upper", 2*p_hi*p_hi < Fraction(4, 5))


def f(q):
    return 4*q*(1-q)


def j(q):
    return -(1-ZETA*f(q)).ln()


def jp(q):
    return 4*ZETA*(1-2*q)/(1-ZETA*f(q))


def jpp(q):
    return -8*ZETA*(1-2*ZETA+ZETA*f(q))/(1-ZETA*f(q))**2


def energy(q, beta=BETA):
    return (-beta*f(q)).exp()


def full_trace(groups, dimension, beta=BETA):
    """groups contain (multiplicity, probability), including dormant zeros."""
    m = sum(n for n, _ in groups)
    return dec(dimension - 2*m) + 2*sum((n*energy(q, beta) for n, q in groups), Decimal(0))


def feedback(groups):
    return S*sum((n*j(q) for n, q in groups), Decimal(0))


def coeff(q, trace, beta=BETA):
    return S*jp(q) - 8*energy(q, beta)*(1-2*q)/trace


# True original n20 probabilities; all late labels and overshoots are present.
N = fib(21)
PI = P**23
READY = 2*N*PI
L_NATIVE = 4*P**3
Q_E = 1-ZETA*L_NATIVE
R_E = 1-ZETA*L_NATIVE*(1+P**6)
R0 = 1-Q_E*R_E
R_F = 4*ZETA*Q_E*P**11
R_Q = 8*ZETA*P**6*(R_E+Q_E*P**6)
fine_groups = [(fib(20), P**21), (N, P**22), (N, P**24),
               (2*N, PI*(1-R0)), (2*N, PI*R0)]
three_groups = [(1, 1-READY), (1, READY*(1-R0)), (1, READY*R0), (M20-3, Decimal(0))]
require("all_fine_probabilities_normalized", abs(sum(n*q for n, q in fine_groups)-1) < Decimal("1e-90"))
require("three_status_full_padding_normalized", abs(sum(n*q for n, q in three_groups)-1) < Decimal("1e-90"))
require("positive_original_report", 0 < R0 < Decimal("0.000002"))
require("unchanged_matter_ratio", Decimal("-23.417") < -R_Q/R_F < Decimal("-23.416"))
zf = full_trace(fine_groups, DIM20_LOWER)
z3 = full_trace(three_groups, DIM20_LOWER)
jf, j3 = feedback(fine_groups), feedback(three_groups)
heat_increase = (z3/zf).ln()/BETA
feedback_gap = jf-j3
coupled_gap = feedback_gap-heat_increase
eta_actual = (1+2*BETA)/(64*ZETA*(1-2*ZETA)*dec(ZMIN20))
require("actual_n20_heat_increases_on_coarsening", heat_increase > 0)
require("actual_n20_feedback_gap_positive", feedback_gap > Decimal("0.00026"))
require("actual_n20_full_order", (1-eta_actual)*feedback_gap <= coupled_gap < feedback_gap)
require("absolute_heat_retained", (S*zf).ln()/BETA > 30)
gain_ratios = {}
for name, a, tr in [("fine", PI, zf), ("three_status", READY, z3)]:
    u, v = a*R0, a*(1-R0)
    gj = S*(jp(u)-jp(v))
    gc = coeff(u, tr)-coeff(v, tr)
    require(name+"_strict_nonzero_all42_gain", gj > 0 and (1-eta_actual)*gj <= gc < gj)
    gain_ratios[name] = str(gc/gj)

# Exact algebraic feedback merge identity (not a floating determinant test).
for i, (a, b) in enumerate([(Fraction(1, 7), Fraction(2, 9)),
                            (Fraction(1, 10**12), Fraction(1, 10**12)),
                            (Fraction(1, 3), Fraction(2, 3)),
                            (Fraction(0), Fraction(1, 2))]):
    d = lambda q: 1-ZETA_Q*4*q*(1-q)
    lhs = d(a+b)-d(a)*d(b)
    rhs = 8*ZETA_Q*a*b*(1-2*ZETA_Q*(1-a)*(1-b))
    require("exact_feedback_merge_identity_"+str(i), lhs == rhs)

# Direct finite changes across masses, including a true tiny-cell merge.
merge_diagnostics = []
for i, (a, b) in enumerate([(Decimal(1)/7, Decimal(2)/9),
                            (PI*R0, PI*R0),
                            (Decimal("0.37"), Decimal("0.63")),
                            (Decimal("0.000001"), Decimal("0.4"))]):
    rest = 1-a-b
    before = [(1, a), (1, b), (1, rest)]
    after = [(1, a+b), (1, Decimal(0)), (1, rest)]
    zb = full_trace(before, DIM20_LOWER)
    za = full_trace(after, DIM20_LOWER)
    gh = (za/zb).ln()/BETA
    gj = feedback(before)-feedback(after)
    heat_bound = 16*(1+2*BETA)*a*b/dec(ZMIN20)
    j_lower = 1024*ZETA*(1-2*ZETA)*a*b
    require("merge_"+str(i)+"_heat_bound", 0 < gh <= heat_bound)
    require("merge_"+str(i)+"_feedback_bound", gj >= j_lower)
    require("merge_"+str(i)+"_coupled_bound", 0 < gj-gh and gh <= eta_actual*gj)
    merge_diagnostics.append({"a": str(a), "b": str(b), "heat_over_feedback": str(gh/gj)})

# Independent finite-matrix route. Every column is retained. This is a
# structural fixture, not a new claim that its variable rotation is a D0 primitive.
def rotation(d, i, k, angle):
    u = np.eye(d, dtype=complex)
    c, sn = math.cos(angle), math.sin(angle)
    u[i, i] = u[k, k] = c
    u[i, k] = -sn
    u[k, i] = sn
    return u


pf = float(P)
golden = np.array([[math.sqrt(pf), -pf], [pf, math.sqrt(pf)]], dtype=complex)
golden_word = np.kron(np.kron(golden, golden), golden)
cnot = np.zeros((8, 8), dtype=complex)
for column in range(8):
    row = column ^ (1 if column & 4 else 0)
    cnot[row, column] = 1


def fixture(theta, cells, frozen_prepared=None):
    prep = rotation(8, 0, 6, 0.27+0.2*theta) @ rotation(8, 1, 6, 0.19-0.3*theta)
    base = cnot @ rotation(8, 0, 3, theta) @ golden_word
    v = base @ prep.conj().T
    omega = prep[:, 0]
    if frozen_prepared is not None:
        omega = frozen_prepared
    p = np.outer(omega, omega.conj())
    prob = np.abs(v @ omega)**2
    blocks = []
    masses = []
    for cell in cells:
        pi = np.zeros((8, 8), dtype=complex)
        for k in cell:
            pi[k, k] = 1
        blocks.append(v.conj().T @ (np.eye(8)-2*pi) @ v)
        masses.append(float(sum(prob[k] for k in cell)))
    for _ in range(8-len(cells)):
        blocks.append(np.eye(8))
        masses.append(0.0)
    u = np.zeros((64, 64), dtype=complex)
    for i, block in enumerate(blocks):
        u[8*i:8*i+8, 8*i:8*i+8] = block
    pp = np.kron(np.eye(8), p)
    cc = (np.eye(64)-pp) @ u @ pp
    ff = cc.conj().T @ cc
    lap = ff+cc@cc.conj().T
    return {"U": u, "P": pp, "C": cc, "F": ff, "L": lap,
            "q": np.array(masses), "omega": omega}


theta0 = 0.23
fine_cells = [[k] for k in range(8)]
coarse_cells = [[0, 1, 2], [3, 4], [5, 6, 7]]
matrix_checks = {}
for label, cells in [("fine", fine_cells), ("coarse", coarse_cells)]:
    fi = fixture(theta0, cells)
    fv = 4*fi["q"]*(1-fi["q"])
    expected_f = np.sort(np.concatenate([fv, np.zeros(56)]))
    expected_l = np.sort(np.concatenate([fv, fv, np.zeros(48)]))
    ferr = float(np.max(np.abs(np.linalg.eigvalsh(fi["F"])-expected_f)))
    lerr = float(np.max(np.abs(np.linalg.eigvalsh(fi["L"])-expected_l)))
    require(label+"_all_column_unitarity", np.linalg.norm(fi["U"].conj().T@fi["U"]-np.eye(64), ord=2) < 2e-14)
    require(label+"_actual_nilpotent_cut", np.linalg.norm(fi["C"]@fi["C"], ord=2) < 2e-14)
    require(label+"_actual_complement_spectrum", ferr < 2e-14)
    require(label+"_full_paired_hodge_spectrum", lerr < 2e-14)
    full_z = np.exp(-float(BETA)*np.linalg.eigvalsh(fi["L"])).sum()
    expected_z = 64-16+2*np.exp(-float(BETA)*fv).sum()
    require(label+"_full_harmonic_trace", abs(full_z-expected_z) < 3e-13)
    dropped_z = 2*np.exp(-float(BETA)*fv[fv > 1e-12]).sum()
    require(label+"_dropped_harmonics_negative_control", full_z-dropped_z > 40)
    matrix_checks[label] = {"F_spectrum_error": ferr, "Hodge_spectrum_error": lerr,
                            "full_unpadded_trace": float(full_z)}


def matrix_value(theta, cells, beta=float(BETA), dimension=DIM20_LOWER, frozen=None, absolute=False):
    fi = fixture(theta, cells, frozen)
    eval_l = np.linalg.eigvalsh(fi["L"])
    eval_f = np.linalg.eigvalsh(fi["F"])
    # Exact harmonic padding of the literal 64-dimensional matrix.
    delta_z = float(np.expm1(-beta*eval_l).sum())
    relative_heat = math.log1p(delta_z/dimension)/beta
    feedback_value = float(-S*np.log1p(-float(ZETA)*eval_f).sum())
    value = relative_heat+feedback_value
    if absolute:
        value += math.log(S*dimension)/beta
    return value


def five_point(fun, x, step=1e-4):
    return (fun(x-2*step)-8*fun(x-step)+8*fun(x+step)-fun(x+2*step))/(12*step)


def probability_coeff(q, dimension, beta):
    ff = 4*q*(1-q)
    fp = 4*(1-2*q)
    ee = np.exp(-beta*ff)
    zz = dimension-2*len(q)+2*ee.sum()
    zp = float(ZETA)
    kk = zp*fp/(1-zp*ff)
    return S*kk-2*ee*fp/zz


source_diagnostics = {}
for label, cells in [("fine", fine_cells), ("coarse", coarse_cells)]:
    fi = fixture(theta0, cells)
    dq = five_point(lambda t: fixture(t, cells)["q"], theta0)
    expected_source = float(probability_coeff(fi["q"], DIM20_LOWER, float(BETA)) @ dq)
    direct_source = five_point(lambda t: matrix_value(t, cells), theta0)
    frozen_source = five_point(lambda t: matrix_value(t, cells, frozen=fi["omega"]), theta0)
    require(label+"_moving_cut_full_source", abs(direct_source-expected_source) < 2e-11)
    require(label+"_frozen_input_is_different", abs(frozen_source-direct_source) > 1e-7)
    source_diagnostics[label] = {"direct_matrix_source": direct_source,
                                 "pulled_probability_source": expected_source,
                                 "incorrect_frozen_source": frozen_source}

# Entire Hessian; use a small full carrier so normalizer cross terms cannot
# hide below numerical accuracy, then check the large-carrier concavity bound.
qvec = fixture(theta0, fine_cells)["q"]


def analytic_hessian(q, dimension, beta):
    ff, fp = 4*q*(1-q), 4*(1-2*q)
    ee = np.exp(-beta*ff)
    zz = dimension-2*len(q)+2*ee.sum()
    zzeta = float(ZETA)
    jjpp = -8*zzeta*(1-2*zzeta+zzeta*ff)/(1-zzeta*ff)**2
    diagonal = S*jjpp+2*ee*(beta*fp**2+8)/zz
    vv = ee*fp
    cross = -4*beta*np.outer(vv, vv)/zz**2
    return np.diag(diagonal)+cross, cross


hh, cross = analytic_hessian(qvec, 64, float(BETA))
numeric_hh = np.zeros((8, 8))
for k in range(8):
    basis = np.eye(8)[k]
    numeric_hh[:, k] = five_point(lambda t: probability_coeff(qvec+t*basis, 64, float(BETA)), 0, 1e-5)
require("full_hessian_including_normalizer", np.max(np.abs(hh-numeric_hh)) < 2e-9)
require("normalizer_term_material_negative_control", np.max(np.abs(cross)) > 1e-3)
large_hh, _ = analytic_hessian(qvec, DIM20_LOWER, float(BETA))
curvature_bound = -(1-float(ETA_UPPER))*1024*float(ZETA)*(1-2*float(ZETA))
require("padded_full_hessian_strict_concavity", np.linalg.eigvalsh(large_hh).max() <= curvature_bound+1e-14)

# Temperature variation retains the large absolute pressure, unlike a
# fixed-temperature difference where that constant is numerically removable.
fi = fixture(theta0, coarse_cells)
ff = 4*fi["q"]*(1-fi["q"])
beta_float = float(BETA)
ee = np.exp(-beta_float*ff)
zz = DIM20_LOWER-16+2*ee.sum()
dbeta = -math.log(S*zz)/beta_float**2-2*float((ff*ee).sum())/(beta_float*zz)
direct_dbeta = five_point(lambda b: matrix_value(theta0, coarse_cells, beta=b, absolute=True), beta_float)
require("moving_beta_full_absolute_source", abs(dbeta-direct_dbeta) < 2e-8)
require("normalizing_away_dimension_changes_beta_source", abs(dbeta) > 40)

# Actual depth arithmetic, not a new address census.
refinement = []
for size in [4, 8, 16, 64, 1024]:
    scale_steps = 0
    while (1/P)**scale_steps < size:
        scale_steps += 1
    n = 64*scale_steps+128
    fn, fn1 = fib(n), fib(n+1)
    m, w = fn+6*fn1, fn+4*fn1
    zmin = m*(w-2)
    require("L"+str(size)+"_integer_dimension_bound", zmin >= 18*fn1**2)
    eta_n = (1+2*BETA)/(64*ZETA*(1-2*ZETA)*dec(zmin))
    c0 = (1+2*BETA)/(1152*ZETA*(1-2*ZETA)*P**2)
    envelope = c0*P**256/dec(size)**128
    require("L"+str(size)+"_actual_refinement_envelope", eta_n <= envelope)
    require("L"+str(size)+"_ready_nonvanishing", Decimal("0.28") < 2*dec(fn1)*P**(n+3) < Decimal("0.37"))
    refinement.append({"L": size, "n": n, "eta": str(eta_n), "bound_C0_p256_Lminus128": str(envelope)})

# Rigorous high-beta scope countercontrol; this is a finite mathematical
# carrier choice, not an asserted upper bound on the unspecified native WORK.
HIGH_D = M20*M20
a_q = Fraction(1, 2**60)
threshold = 7*(1-ZETA_Q)**2/(4096*ZETA_Q*HIGH_D)
require("high_beta_exact_small_mass_condition", 0 < a_q < min(Fraction(1, 4), threshold))
require("exp3_greater_than_16_by_exact_series", sum(Fraction(3**k, math.factorial(k)) for k in range(5)) > 16)
a = dec(a_q)
beta_high = 1/a
# All three probabilities lie in [0,1], with one genuine unused selector slot.
high_before = [(1, a), (1, a), (1, 1-2*a)]
high_after = [(1, 2*a), (1, Decimal(0)), (1, 1-2*a)]
zhb = full_trace(high_before, HIGH_D, beta_high)
zha = full_trace(high_after, HIGH_D, beta_high)
high_heat = (zha/zhb).ln()/beta_high
high_j = feedback(high_before)-feedback(high_after)
require("high_beta_full_trace_delta_bound", zha-zhb > Decimal(7)/4)
require("high_beta_exact_heat_lower", high_heat > 7*a/(4*HIGH_D))
require("high_beta_feedback_upper", high_j < 1024*ZETA*a*a/(1-ZETA)**2)
require("high_beta_reverses_full_partition_order", high_heat > high_j > 0)

result = {
    "status": "PASS",
    "checks": len(checks),
    "check_names": checks,
    "scope": "Full cut Hodge+feedback on one padded READY partition carrier; no physical Book selection or new all42 root certificate.",
    "original_n20": {
        "selector_dimension": M20,
        "work_dimension_lower_bound_only": W20_LOWER,
        "non_right_dimension_lower_bound_only": DIM20_LOWER,
        "harmonic_lower_bound": ZMIN20,
        "beta0": str(BETA),
        "eta_rational_upper": str(ETA_UPPER),
        "eta_rational_upper_decimal": str(dec(ETA_UPPER)),
        "r0": str(R0),
        "ready_probability": str(READY),
        "lambda_minus": str(-R_Q/R_F),
        "evaluation_at_conservative_dimension_bound": {
            "feedback_gap": str(feedback_gap),
            "heat_increase": str(heat_increase),
            "coupled_gap": str(coupled_gap),
            "coupled_over_feedback_source": gain_ratios,
        },
    },
    "merge_diagnostics": merge_diagnostics,
    "full_matrix_fixture": matrix_checks,
    "moving_input_source": source_diagnostics,
    "hessian_error": float(np.max(np.abs(hh-numeric_hh))),
    "moving_beta_source": {"analytic": dbeta, "direct_matrix_difference": direct_dbeta},
    "actual_refinement": refinement,
    "high_beta_mathematical_scope_control": {
        "non_right_dimension": HIGH_D,
        "mass": str(a), "beta": str(beta_high),
        "heat_increase": str(high_heat), "feedback_decrease": str(high_j),
        "heat_over_feedback": str(high_heat/high_j),
        "not_a_claim_about_the_unknown_native_work_dimension": True,
    },
    "GR_closed": False,
}
print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
