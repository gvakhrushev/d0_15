#!/usr/bin/env python3
"""Bounded composition check for the paid moment-writer echo.

Consumes the pinned Golden factory theorem. It does not reconstruct every
factory hardware branch, the original measured 72,441-history programme, or
the all42 source. Default execution is read-only; explicit author mode
--write-result writes only RESULT.json inside this packet.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
TOL = 2e-12
checks: list[dict] = []
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--write-result", action="store_true",
    help="Author mode only: regenerate this packet's RESULT.json.",
)
args = parser.parse_args()


def check(name: str, condition: bool, **details) -> None:
    if not bool(condition):
        raise AssertionError(f"{name}: {details}")
    checks.append({"name": name, "pass": True, **details})


def close(name: str, actual, expected, tol: float = TOL) -> None:
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    check(name, error <= tol, max_abs_error=error, tolerance=tol)


def dagger(a):
    return np.asarray(a).conj().T


def density(v):
    return np.outer(v, np.asarray(v).conj())


def probability(effect, rho):
    value = np.trace(effect @ rho)
    if abs(value.imag) > TOL:
        raise AssertionError(f"Nonreal probability: {value}")
    return float(value.real)


def tensor(*arrays):
    result = np.array([1.0])
    for a in arrays:
        result = np.kron(result, a)
    return result


def bit(index, n, position):
    return (index >> (n - 1 - position)) & 1


def permutation(n, rule):
    out = np.zeros((2**n, 2**n))
    for j in range(2**n):
        out[rule(j), j] = 1.0
    return out


def cnot(n, control, target):
    return permutation(
        n, lambda j: j ^ (bit(j, n, control) << (n - 1 - target))
    )


def toffoli(n, c1, c2, target):
    return permutation(
        n,
        lambda j: j
        ^ ((bit(j, n, c1) & bit(j, n, c2)) << (n - 1 - target)),
    )


def cz(n, c1, c2):
    return np.diag(
        [(-1.0) ** (bit(j, n, c1) & bit(j, n, c2)) for j in range(2**n)]
    )


def partial_trace(rho, dims, keep):
    dims = list(dims)
    value = rho.reshape(dims + dims)
    for j in reversed(range(len(dims))):
        if j not in keep:
            value = np.trace(value, axis1=j, axis2=j + len(dims))
            dims.pop(j)
    d = math.prod(dims)
    return value.reshape(d, d)


def h_phi(x):
    if x == 0.0 or x == 1.0:
        return 0.0
    return -(x * math.log(x) + (1 - x) * math.log1p(-x)) / math.log(phi)


def hp_phi(x):
    return math.log((1 - x) / x) / math.log(phi)


def entropy(probabilities):
    return -sum(
        v * math.log(v) / math.log(phi) for v in probabilities if v > 0
    )


def code_dephase(rho, code_dimension, rest_dimension):
    value = np.zeros_like(rho)
    for k in range(code_dimension):
        idx = slice(k * rest_dimension, (k + 1) * rest_dimension)
        value[idx, idx] = rho[idx, idx]
    return value


# Read historical immutable blobs even if another agent advances the checkout.
pins = json.loads((HERE / "SOURCE_PINS.json").read_text())
verified_pins = []
for source in pins["sources"]:
    raw = subprocess.run(
        ["git", "cat-file", "blob", source["git_blob"]],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    actual_blob = hashlib.sha1(
        f"blob {len(raw)}\0".encode() + raw
    ).hexdigest()
    if actual_blob != source["git_blob"]:
        raise AssertionError(f"Pin mismatch for {source['path']}")
    verified_pins.append({"path": source["path"], "git_blob": actual_blob})
check("all consumed historical source blobs available and exact", True)


phi = (1 + math.sqrt(5)) / 2
p = 1 / phi
a = math.sqrt(p)
I2 = np.eye(2)
X = np.array([[0.0, 1.0], [1.0, 0.0]])
Z = np.diag([1.0, -1.0])
H = np.array([[1.0, 1.0], [1.0, -1.0]]) / math.sqrt(2)
G = np.array([[a, -p], [p, a]])
zero = np.array([1.0, 0.0])
plus = np.array([1.0, 1.0]) / math.sqrt(2)
minus = np.array([1.0, -1.0]) / math.sqrt(2)
Pplus = density(plus)
Pminus = density(minus)
qG = 4 * p**3
s3 = 16 * p**9
close("Golden defining relation and full-column paid inverse",
      np.block([[G.T @ G, X @ G @ X], [np.zeros((2, 2)), G.T]]),
      np.block([[I2, G.T], [np.zeros((2, 2)), G.T]]))
close("native X and CCZ success identities",
      [qG + p**6, s3],
      [1.0, math.sin(4 * math.atan2(p, a)) ** 2])


# Build each weak test from actual G/CNOT matrices, not from its desired effect.
CX2 = cnot(2, 0, 1)
weak_A = tensor(G, I2) @ CX2 @ tensor(G, I2)
weak_B = tensor(X @ G @ X, I2) @ CX2 @ tensor(G, I2)
A0, A1 = weak_A[0:2, 0:2], weak_A[2:4, 0:2]
B0, B1 = weak_B[0:2, 0:2], weak_B[2:4, 0:2]
close("literal Golden weak-test Kraus on all data columns",
      np.stack([A0, A1, B0, B1]),
      np.stack([p * I2 - p**2 * X, a * p * (I2 + X),
                p * I2 + p**2 * X, -a * p * (I2 - X)]))
Kplus, Kminus, Kfail, Kimpossible = B0 @ A1, B1 @ A0, B0 @ A0, B1 @ A1
close("complete two-read cycle including impossible branch",
      np.stack([Kplus, Kminus, Kfail, Kimpossible]),
      np.stack([2 * a * p * Pplus, -2 * a * p * Pminus,
                p**3 * I2, np.zeros((2, 2))]))
close("complete X-cycle trace preservation",
      sum(dagger(k) @ k for k in [Kplus, Kminus, Kfail, Kimpossible]), I2)

for cap in [1, 2, 5]:
    pos = sum(dagger(Kplus @ np.linalg.matrix_power(Kfail, j))
              @ (Kplus @ np.linalg.matrix_power(Kfail, j))
              for j in range(cap))
    neg = sum(dagger(Kminus @ np.linalg.matrix_power(Kfail, j))
              @ (Kminus @ np.linalg.matrix_power(Kfail, j))
              for j in range(cap))
    unresolved = np.linalg.matrix_power(Kfail, cap)
    close(f"retained finite X cap {cap}",
          np.stack([pos, neg, dagger(unresolved) @ unresolved]),
          np.stack([(1 - p**(6 * cap)) * Pplus,
                    (1 - p**(6 * cap)) * Pminus,
                    p**(6 * cap) * I2]))


# Native logical row multiplexer on C,A,B. The only CAR masks are 0 and 1.
CXab = cnot(3, 1, 2)
CC = toffoli(3, 0, 2, 1)
U = CXab @ CC @ CXab

def cswap_index(j):
    if bit(j, 3, 0) and bit(j, 3, 1) != bit(j, 3, 2):
        return j ^ 3
    return j

Udirect = permutation(3, cswap_index)
close("literal two-CNOT one-Toffoli CSWAP on all eight columns", U, Udirect)
close("same logical word is full inverse", U @ U, np.eye(8))
W0, W1 = tensor(plus, minus), tensor(minus, plus)
close("conditional two-row work is orthogonal", np.vdot(W0, W1), 0)
initial = tensor(plus, plus, minus)
written = U @ initial
rho_written = density(written)
rho_dephased = code_dephase(rho_written, 2, 4)
close("code marginal before echo is maximally mixed",
      partial_trace(rho_written, [2, 4], [0]), I2 / 2)
close("every code-only observable has identical density input",
      partial_trace(rho_written, [2, 4], [0]),
      partial_trace(rho_dephased, [2, 4], [0]))

# Explicit 0/1-mask embedding into two CAR16 rows, retaining all other bits.
embed = np.zeros((2 * 16 * 16, 8))
for c in range(2):
    for aa in range(2):
        for bb in range(2):
            embed[c * 256 + aa * 16 + bb, c * 4 + aa * 2 + bb] = 1
car_swap = np.zeros((512, 512))
for c in range(2):
    for aa in range(16):
        for bb in range(16):
            out_a, out_b = aa, bb
            if c:
                out_a = (aa & ~1) | (bb & 1)
                out_b = (bb & ~1) | (aa & 1)
            car_swap[c * 256 + out_a * 16 + out_b,
                     c * 256 + aa * 16 + bb] = 1
close("actual CAR16 masks 0/1 intertwine active-bit CSWAP",
      car_swap @ embed, embed @ U)
close("active-bit CAR16 extension is unitary on all columns",
      car_swap.T @ car_swap, np.eye(512))
output_index = np.argmax(car_swap, axis=0)
spectator_changes = [
    sum(bit(int(output_index[j]), 9, position) != bit(j, 9, position)
        for j in range(512))
    for position in [1, 2, 3, 5, 6, 7]
]
close("all six spectator-Z eigenvalues preserved on all 512 columns",
      spectator_changes, [0] * 6)

# Owned exact macro readiness. No invented abort output state is substituted.
K, L, LX = 3, 2, 2
plus_ready = 1 - (1 - 2 * p**3)**K
b2, b3, bX = 1 - p**(6 * L), 1 - (1 - s3)**L, 1 - p**(6 * LX)
toffoli_ready = b2**4 * b3
gamma_reverse = plus_ready**2 * toffoli_ready
gamma_extra = gamma_reverse * bX
# Explicit coherent fixture prefix: C+, A+, B+ and two H resources;
# Z converts B+ to B-, then the forward CSWAP. Known-one is a retained
# product byproduct of the first successful plus bank.
gamma_prefix = plus_ready**5 * b2 * toffoli_ready
Gamma = gamma_prefix * gamma_extra
check("true native finite-cap readiness is strictly positive and below one",
      0 < Gamma < gamma_extra < 1,
      full_fixture_readiness=Gamma, conditional_extra_readiness=gamma_extra)
Eplus = gamma_extra * U @ tensor(Pplus, np.eye(4)) @ dagger(U)
Eminus = gamma_extra * U @ tensor(Pminus, np.eye(4)) @ dagger(U)
Eabort = (1 - gamma_extra) * np.eye(8)
close("paid echo instrument effects include the entire abort mass",
      Eplus + Eminus + Eabort, np.eye(8))
coherent_law = np.array([probability(e, rho_written)
                         for e in [Eplus, Eminus, Eabort]])
dephased_law = np.array([probability(e, rho_dephased)
                         for e in [Eplus, Eminus, Eabort]])
close("already-ready coherence and dephasing give actual paid laws",
      np.stack([coherent_law, dephased_law]),
      [[gamma_extra, 0, 1 - gamma_extra],
       [gamma_extra / 2, gamma_extra / 2, 1 - gamma_extra]])
full_coherent = gamma_prefix * coherent_law + np.array([0, 0, 1 - gamma_prefix])
full_dephased = gamma_prefix * dephased_law + np.array([0, 0, 1 - gamma_prefix])
close("end-to-end contrast retains preparation and forward readiness",
      np.stack([full_coherent, full_dephased]),
      [[Gamma, 0, 1 - Gamma], [Gamma / 2, Gamma / 2, 1 - Gamma]])
check("old-ready-only normalization would overclaim full contrast",
      abs(gamma_extra / 2 - Gamma / 2) > 1e-4)

# Arbitrarily entangled retained RIGHT is untouched; old H-sign tape is
# classical and independent of data. Spent pure factory work factors too.
bank_right = np.array([1, 1j, -2, 0.3j, 0.7, -0.2, 1.1j, -0.4], dtype=complex)
bank_right /= np.linalg.norm(bank_right)
initial_right = tensor(plus, bank_right)
U_right = tensor(U, I2)
written_right = U_right @ initial_right
returned_right = dagger(U_right) @ written_right
close("logical inverse works with arbitrary entangled oldRIGHT",
      returned_right, initial_right)
right_before = partial_trace(density(written_right), [2, 2, 2, 2], [3])
right_after = partial_trace(density(returned_right), [2, 2, 2, 2], [3])
close("oldRIGHT entire marginal is preserved", right_before, right_after)
old_tape = np.diag([0.5, 0.5])  # actual two corrected H signs
rho_with_old = tensor(old_tape, density(written_right))
inverse_with_old = tensor(I2, dagger(U_right))
rho_after_old = inverse_with_old @ rho_with_old @ dagger(inverse_with_old)
close("old measured factory tape remains an independent retained block",
      partial_trace(rho_after_old, [2, 16], [0]), old_tape)
close("tensor spectator identity: representative old-tape X and RIGHT Z commute",
      inverse_with_old @ tensor(X, np.eye(8), Z),
      tensor(X, np.eye(8), Z) @ inverse_with_old)

# Hostile control: an inaccessible additional which-code copy cannot vanish.
copy_external = cnot(4, 0, 3)
tagged = copy_external @ tensor(written, zero)
still_tagged = tensor(dagger(U), I2) @ tagged
tagged_code = partial_trace(density(still_tagged), [2, 2, 2, 2], [0])
close("inaccessible extra code tag defeats a merely logical echo",
      tagged_code, I2 / 2)
check("tagging isometry is not product factory factorization",
      np.linalg.norm(tagged_code - Pplus) > 0.5)


# Source word on a Schmidt/isometric compression of a purified moment row.
# The orthogonal retained eta+/- states (raw labels, suffix and work) are
# represented by |0>,|1>; no clean-qubit physical row factory is claimed.
# Fixed A=I_purifier tensor H on the active CAR bit respects this compression.
# All field dependence is in the generated moment, not in a moving gate.
A = tensor(I2, H)  # purifier, active 0/1-mask CAR bit
Pi = tensor(I2, np.diag([0.0, 1.0]))
R = dagger(A) @ (np.eye(4) - 2 * Pi) @ A
V = tensor(I2, dagger(A)) @ cz(3, 0, 2) @ tensor(I2, A)
block_expected = np.block([[np.eye(4), np.zeros((4, 4))],
                           [np.zeros((4, 4)), R]])
close("A-CZ-fresh-inverse equals controlled reflection on all columns",
      V, block_expected)
close("reflection is genuinely selfadjoint and unitary",
      np.stack([R, dagger(R) @ R]), np.stack([dagger(R), np.eye(4)]))
close("minus branch is the true full-column report projector",
      (np.eye(4) - R) / 2, dagger(A) @ Pi @ A)

row_parameters = [-0.8, -0.2, 0.3, 0.75]
report_laws = []
gamma_report_extra = plus_ready**3 * b2**5 * bX
# Three fair resources: new probe plus one for each H pass. Both H use
# b2^2; middle CZ uses b2; final X uses bX. This is conditional on the
# paid catalogue itself being ready, never declared to be full readiness.
for t in row_parameters:
    row = (math.sqrt((1 + t) / 2) * tensor(zero, plus)
           + math.sqrt((1 - t) / 2) * tensor(np.array([0.0, 1.0]), minus))
    output = V @ tensor(plus, row)
    rho_out = density(output)
    r = probability(Pi, density(A @ row))
    measured = [
        gamma_report_extra * probability(tensor(Pplus, np.eye(4)), rho_out),
        gamma_report_extra * probability(tensor(Pminus, np.eye(4)), rho_out),
        1 - gamma_report_extra,
    ]
    close(f"purified exact moment t={t}: paid phase report and all aborts",
          measured,
          [gamma_report_extra * (1 - (1 - t) / 2),
           gamma_report_extra * (1 - t) / 2,
           1 - gamma_report_extra])
    close(f"purified exact moment t={t}: original report probability",
          r, (1 - t) / 2)
    report_laws.append({"t": t, "r": r, "conditional_paid_law": measured})

# Every final fine sign branch of a pure complete input remains pure.
t = 0.3
row = (math.sqrt((1 + t) / 2) * tensor(zero, plus)
       + math.sqrt((1 - t) / 2) * tensor(np.array([0.0, 1.0]), minus))
output = V @ tensor(plus, row)
purities = []
for gate in [Kplus, Kminus]:
    branch = tensor(gate, np.eye(4)) @ output
    branch /= np.linalg.norm(branch)
    rho_branch = density(branch)
    purities.append(np.trace(rho_branch @ rho_branch).real)
close("full retained quantum work is pure conditional on terminal sign",
      purities, [1, 1])

# Complete entropy identity for actual X-cycle outcome laws, with a
# classical data-independent ready/abort factory macro. The abort quantum
# state is not replaced; purity comes from the consumed complete-work theorem.
r = (1 - t) / 2
before_X_ready = gamma_report_extra / bX
factory_probs = [1 - before_X_ready]
full_probs = [1 - before_X_ready]
for j in range(LX):
    success_time = before_X_ready * p**(6 * j) * qG
    factory_probs.append(success_time)
    full_probs.extend([success_time * (1 - r), success_time * r])
unresolved = before_X_ready * p**(6 * LX)
factory_probs.append(unresolved)
full_probs.append(unresolved)
close("coarse macro display retains every success time and abort probability",
      [sum(factory_probs), sum(full_probs)], [1, 1])
close("complete sign entropy is H(T) plus true readiness times h(r)",
      entropy(full_probs), entropy(factory_probs) + gamma_report_extra * h_phi(r))

# No invented raw instruction equivalence: different deterministic code
# labels are entropy-preserving relabellings of the same stochastic index.
pi_T0 = [qG, p**6]
T_code0 = {("BA", j): w for j, w in enumerate(pi_T0)}
T_code1 = {("AB", j): w for j, w in enumerate(pi_T0)}
check("raw prewritten instruction records remain distinct",
      set(T_code0).isdisjoint(T_code1))
close("only stochastic law after relabelling, entropy and counted total agree",
      [entropy(T_code0.values()), entropy(T_code1.values()),
       sum(pi_T0) * (1 + 1)],
      [entropy(pi_T0), entropy(pi_T0), 2])

# Analytical price/source controls. These are algebraic fixtures, not
# numerical assignments of the physical Book or factory baseline.
def smooth_B(x):
    return 3 + 0.2 * x*x


def smooth_gamma(x):
    return 0.4 + 0.1 * x


def smooth_r(x):
    return (1 - x) / 2


def price_fixture(x):
    return smooth_B(x) - smooth_gamma(x) * h_phi(smooth_r(x))


step = 1e-5
x = 0.3
numeric_derivative = (price_fixture(x + step) - price_fixture(x - step)) / (2 * step)
full_derivative = (
    0.4 * x - 0.1 * h_phi(smooth_r(x))
    + 0.5 * smooth_gamma(x) * hp_phi(smooth_r(x))
)
naive_derivative = 0.5 * smooth_gamma(x) * hp_phi(smooth_r(x))
close("full dB - h dGamma - Gamma h' dr source",
      numeric_derivative, full_derivative, tol=2e-9)
check("field-dependent prefix/readiness cannot be dropped",
      -0.015 < full_derivative - naive_derivative < -0.014,
      missing_source=full_derivative - naive_derivative)
old_gain, new_gain = 0.71, 0.43
r_values = [smooth_r(x - 0.07), smooth_r(x), smooth_r(x + 0.07)]
old_prices = np.array([9 - old_gain * h_phi(v) for v in r_values])
new_prices = np.array([25 - new_gain * h_phi(v) for v in r_values])
close("finite fixed-catalogue first and second secants use actual gain ratio",
      [new_prices[2] - new_prices[0],
       new_prices[2] - 2 * new_prices[1] + new_prices[0]],
      (new_gain / old_gain) * np.array([
          old_prices[2] - old_prices[0],
          old_prices[2] - 2 * old_prices[1] + old_prices[0]]))

# Uniform-code schedule: read code only on completed report episodes.
rr = [0.2, 0.7]
M = len(rr)
gamma_u = 0.63
uniform_joint = [1 - gamma_u] + [
    gamma_u * v / M for r in rr for v in [1 - r, r]
]
uniform_probe = [1 - gamma_u, gamma_u * (1 - sum(rr) / M),
                 gamma_u * sum(rr) / M]
close("uniform code read only on completion: honest full entropy",
      entropy(uniform_joint),
      h_phi(gamma_u) + gamma_u * (
          math.log(M) / math.log(phi) + sum(h_phi(r) for r in rr) / M))
close("uniform code never read: coherent-work report entropy",
      entropy(uniform_probe),
      h_phi(gamma_u) + gamma_u * h_phi(sum(rr) / M))
check("fixed-code, code-read uniform, and code-unread uniform gains differ",
      abs(h_phi(rr[0]) - h_phi(sum(rr) / M)) > 0.05
      and abs(math.log(M) / math.log(phi) + sum(h_phi(r) for r in rr) / M
              - h_phi(sum(rr) / M)) > 0.05)
all_branches_code_read = [
    (1 - gamma_u) / M for _ in rr
] + [gamma_u * v / M for r in rr for v in [1 - r, r]]
close("reading uniform code on every abort adds its actual entropy",
      entropy(all_branches_code_read) - entropy(uniform_joint),
      (1 - gamma_u) * math.log(M) / math.log(phi))

result = {
    "status": "PASS",
    "checks_passed": len(checks),
    "checks": checks,
    "source_pins_verified": verified_pins,
    "native_parameters": {
        "p": p, "q_G": qG, "s_CCZ": s3, "K": K, "L": L, "L_X": LX,
        "reverse_readiness_after_old_ready": gamma_reverse,
        "extra_readiness_including_final_X": gamma_extra,
        "explicit_small_fixture_prefix_readiness": gamma_prefix,
        "explicit_small_fixture_full_readiness": Gamma,
        "small_fixture_end_to_end_plus_contrast": Gamma / 2,
        "additional_gate_call_upper_bound_excluding_reading_controller_storage":
            10 * K + 98 * L + 10 + 8 * LX,
    },
    "report_fixture": {
        "scope": "Conditional on actual paid catalogue ready; its readiness must multiply the displayed extra factor.",
        "purifier_representation": "Schmidt/isometric compression of the actual orthogonal retained eta+/- records; physical row factory not replayed.",
        "additional_ready_factor": gamma_report_extra,
        "laws": report_laws,
    },
    "validation_scope": {
        "checker_default_read_only": True,
        "literal_G_CNOT_X_cycle_checked": True,
        "CSWAP_all_eight_active_columns_checked": True,
        "CAR16_masks_0_1_embedding_checked": True,
        "factory_success_law_consumed_from_pinned_owner": True,
        "all_factory_hardware_branches_replayed": False,
        "physical_B_new_numerically_computed": False,
        "all42_source_replayed": False,
        "original_72441_recovered": False,
        "original_Q8_suites_rerun": False,
        "Book_cut_or_Info_selected": False,
        "uniform_refinement_claim": False,
        "GR_closed": False,
    },
}
if args.write_result:
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "mode": "explicit-author-write-result",
        "status": result["status"],
        "checks_passed": len(checks),
        "full_small_fixture_readiness": Gamma,
        "full_small_fixture_plus_contrast": Gamma / 2,
        "max_recorded_numeric_error": max(
            (c.get("max_abs_error", 0) for c in checks), default=0
        ),
        "scope": "bounded new composition; old suites not replayed; GR_closed=false",
    }, indent=2))
else:
    print(json.dumps(result, indent=2))
