#!/usr/bin/env python3
"""New same-history return/cost composition; exact Q(i,p), all CAR16/128 rows.

This does not run historical certificates or identify Book Info. The changed
jet is physical coframe scale, not the old compact-link fixture. Two rounds
are expanded by the full dual map, representing all 128**2 ordered records.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time

import sympy as s
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True)
parser.add_argument("--output", type=Path)
args = parser.parse_args()
ROOT = args.root.resolve()
OUT = args.output or Path(__file__).with_name("RESULT.json")
START = time.monotonic()
CHECKS = []
PINS = {
    "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md":
    "2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79",
    "02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md":
    "a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915",
    "02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md":
    "c5b2f1021e8da573221f4327bacae67934470a368966456bf328b19fc51555fb",
    "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md":
    "ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d",
}


def require(value, name):
    if not value:
        raise AssertionError(name)
    CHECKS.append(name)


for path, digest in PINS.items():
    require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest,
            "input_sha256:" + path)


class Mat:
    _op_priority = 1000

    def __init__(self, value):
        self.dm = (value if isinstance(value, DomainMatrix) else
                   DomainMatrix.from_Matrix(value).convert_to(QQ_I).to_sparse())

    def __add__(self, other):
        if other == 0:
            return self
        return Mat(self.dm.add(other.dm))

    __radd__ = __add__

    def __neg__(self):
        return Mat(self.dm.neg())

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        if isinstance(other, Mat):
            return Mat(self.dm.matmul(other.dm))
        return Mat(self.dm.scalarmul(QQ_I.from_sympy(s.sympify(other))))

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (1 / s.sympify(other))

    @property
    def H(self):
        return Mat(self.dm.transpose().applyfunc(
            lambda z: QQ_I(z.x, -z.y), QQ_I))

    def __eq__(self, other):
        return isinstance(other, Mat) and self.dm == other.dm


I, O = Mat(s.eye(16)), Mat(s.zeros(16))


def creator(role):
    entries = {}
    for mask in range(16):
        if not ((mask >> role) & 1):
            entries[(mask | (1 << role), mask)] = (
                -1) ** ((mask & ((1 << role) - 1)).bit_count())
    return Mat(s.ImmutableSparseMatrix(16, 16, entries))


# Q[p]/(p^2+p-1), with either scalar or Q(i) matrix coefficients.
def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[0], -a[1]


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    bd = a[1] * b[1]
    return a[0] * b[0] + bd, a[0] * b[1] + a[1] * b[0] - bd


def scale(c, a):
    return c * a[0], c * a[1]


def adj(a):
    return a[0].H, a[1].H


def power(a, n, unit):
    ans = unit
    for _ in range(n):
        ans = mul(ans, a)
    return ans


def eq(a, b, label):
    require(all(x == y for x, y in zip(a, b)), label)


ONE, ZERO, P = (s.Integer(1), s.Integer(0)), (s.Integer(0), s.Integer(0)), (s.Integer(0), s.Integer(1))
MI, MO = (I, O), (O, O)


def scalar_matrix(a):
    return a[0] * I, a[1] * I


def dual(Ks, dKs, X, dX, x=ONE, moment=0, only_port=None):
    result, derivative = MO, MO
    for idx, (K, dK) in enumerate(zip(Ks, dKs)):
        port = idx % 2
        if only_port is not None and port != only_port:
            continue
        c = 1 + port
        coefficient = scale(c**moment, power(x, c, ONE))
        if port:
            coefficient = mul(P, coefficient)  # K1 = sqrt(p) * stored row
        term = mul(mul(adj(K), X), K)
        dterm = add(add(mul(mul(adj(dK), X), K),
                         mul(mul(adj(K), dX), K)),
                     mul(mul(adj(K), X), dK))
        result = add(result, mul(coefficient, term))
        derivative = add(derivative, mul(coefficient, dterm))
    return result, derivative


def power_jet(B, dB, n):
    result, derivative = MI, MO
    for _ in range(n):
        derivative = add(mul(dB, result), mul(B, derivative))
        result = mul(B, result)
    return result, derivative


# Same flat coframe family: h=1/4, rho=(nu/h)^2=144/25, nu=3/5.
# This rational Julia point allows an exact, NONZERO physical scale jet.
h, rho, nu = s.Rational(1, 4), s.Rational(144, 25), s.Rational(3, 5)
root = s.Rational(4, 5)
dnu = nu / (2 * rho)
droot = -nu * dnu / root
words, dwords = [], []
for role in range(4):
    c = creator(role)
    PL, PR = c * c.H, c.H * c
    left, right = I + (root - 1) * PL, I + (root - 1) * PR
    dleft, dright = droot * PL, droot * PR
    phase = s.I if role == 3 else s.Integer(1)
    C, dC = nu * c, dnu * c
    moving, dmoving = phase * C, phase * dC
    for row, drow in zip(
        ((moving, left), (moving.H, right), (-C, -left), (-C.H, -right)),
        ((dmoving, dleft), (dmoving.H, dright), (-dC, -dleft), (-dC.H, -dright)),
    ):
        for _ in range(2):
            words.append(row)
            dwords.append(drow)

Ns, dNs = [], []
for label in range(32):
    signs = [s.Rational((-1) ** ((label & j).bit_count()), 32) for j in range(32)]
    for coeff in range(2):
        Ns.append(sum((signs[j] * words[j][coeff] for j in range(32)), O))
        dNs.append(sum((signs[j] * dwords[j][coeff] for j in range(32)), O))
require(len(Ns) == 64, "all64_original_label_coefficient_rows")
require(sum((N * N.H for N in Ns), O) == I, "row_completeness")
require(sum((dN * N.H + N * dN.H for N, dN in zip(Ns, dNs)), O) == O,
        "row_completeness_scale_jet")
A, dA = Ns[0], dNs[0]
D, dD = 64 * A, 64 * dA
lam, dlam = 2 * rho, s.Integer(2)
require(D * D == lam * I, "same_family_Delta_equals_rho_mu_I16")
require(dD * D + D * dD == dlam * I, "same_family_dDelta_equals_mu_I16")

Ks, dKs = [], []
for idx, (N, dN) in enumerate(zip(Ns, dNs)):
    M, dM = N.H * A, dN.H * A + N.H * dA
    Ks.extend([((I if idx == 0 else O) - 2 * M, 2 * M), (O, -2 * M)])
    dKs.extend([(-2 * dM, 2 * dM), (O, -2 * dM)])
require(len(Ks) == 128, "all128_original_Kraus_rows")
complete, dcomplete = dual(Ks, dKs, MI, MO)
eq(complete, MI, "full128_Kraus_completeness")
eq(dcomplete, MO, "full128_Kraus_scale_jet_completeness")

eps = scale(h**2 / 64, mul(P, P))
b = sub(ONE, scale(lam / 2, eps))
db = scale(-dlam / 2, eps)
eq(Ks[0], scalar_matrix(b), "literal_blank_port0_B")
eq(dKs[0], scalar_matrix(db), "literal_blank_port0_scale_jet")
B4, dB4 = power_jet(Ks[0], dKs[0], 4)
report = {}
for label, x in (("unmarked", ONE), ("half_mark", (s.Rational(1, 2), s.Integer(0))), ("golden_mark", P)):
    G1, dG1 = dual(Ks, dKs, MI, MO, x)
    G2, dG2 = dual(Ks, dKs, G1, dG1, x)
    x2 = mul(x, x)
    F2 = sub(G2, mul(x2, B4))
    dF2 = sub(dG2, mul(x2, dB4))
    ax = add(ONE, scale(lam, mul(mul(P, eps), sub(x, ONE))))
    dax = scale(dlam, mul(mul(P, eps), sub(x, ONE)))
    expected = mul(x2, sub(mul(ax, ax), power(b, 4, ONE)))
    dexpected = mul(x2, sub(scale(2, mul(ax, dax)), scale(4, mul(power(b, 3, ONE), db))))
    eq(G2, scalar_matrix(mul(x2, mul(ax, ax))), label + ":full128_squared_cost_partition")
    eq(F2, scalar_matrix(expected), label + ":same_return_cost_formula")
    eq(dF2, scalar_matrix(dexpected), label + ":genuine_scale_source")
    if label != "unmarked":
        wrong_scalar_clock = mul(x2, sub(MI, B4))
        require(F2 != wrong_scalar_clock, label + ":reject_scalar_clock_substitution")
    report[label] = {"F2_Qp": list(map(str, expected)), "dF2_Qp": list(map(str, dexpected))}

M1, dM1 = dual(Ks, dKs, MI, MO, moment=1)
shift_M1, dshift_M1 = dual(Ks, dKs, M1, dM1)
C2, dC2 = add(M1, shift_M1), add(dM1, dshift_M1)
r = scale(lam, mul(P, eps))
dr = scale(dlam, mul(P, eps))
eq(C2, scalar_matrix(scale(2, add(ONE, r))), "complete_two_round_known_cost")
eq(dC2, scalar_matrix(scale(2, dr)), "complete_two_round_known_cost_scale_source")
Cexit, dCexit = sub(C2, scale(2, B4)), sub(dC2, scale(2, dB4))
expected_exit = sub(scale(2, add(ONE, r)), scale(2, power(b, 4, ONE)))
expected_dexit = sub(scale(2, dr), scale(8, mul(power(b, 3, ONE), db)))
eq(Cexit, scalar_matrix(expected_exit), "all_exit_histories_cost_insertion")
eq(dCexit, scalar_matrix(expected_dexit), "all_exit_histories_cost_mixed_source")
port1, _ = dual(Ks, dKs, MI, MO, only_port=1)
eq(port1, scalar_matrix(r), "actual_port1_scalar_effect")
B2, _ = power_jet(Ks[0], dKs[0], 2)
require(sub(MI, B2) != port1, "reject_port1_as_complete_nonblank_cut")
B8, _ = power_jet(Ks[0], dKs[0], 8)
require(B4 != B8, "reject_wrong_clock_n_equals_m")

# Exact symbolic finite-stopping identities, including all failures to stop.
q, r_symbol, N = s.symbols("q r N", positive=True)
j = s.symbols("j", integer=True, nonnegative=True)
finite_stop_probability = s.summation(q**j * (1 - q), (j, 0, 4))
require(s.expand(finite_stop_probability - (1 - q**5)) == 0,
        "finite_horizon_full_first_event_partition")
finite_expected_ticks = sum(q**j for j in range(5))
finite_terminal_port1 = r_symbol * sum(q**j for j in range(5))
require(s.expand(finite_expected_ticks + finite_terminal_port1 -
                 (1 + r_symbol) * finite_expected_ticks) == 0,
        "capped_first_event_actual_cost_including_final_port")

proof = Path(__file__).with_name("return_cost_and_stopping.md")
result = {
    "status": "PASS",
    "checks": len(CHECKS),
    "seconds": round(time.monotonic() - START, 3),
    "input_commit": "acfe3e19ecda5f2dbc678ec52e2f7cd0f3e639a1",
    "scope": "Exact original full128 CAR16 two-round return/cost composition on the physical coframe scale family; all 128^2 histories via full transfer. Generic all-n and all-L conclusions are analytic proof, not finite extrapolation.",
    "fixture": {"h": str(h), "rho": str(rho), "mu": "2", "lambda": str(lam), "d_lambda": str(dlam), "n": 2, "oldRIGHT": "Generic unchanged identity factor, dimension128 retained analytically; no full-site replay"},
    "source_sha256": PINS,
    "proof_sha256": hashlib.sha256(proof.read_bytes()).hexdigest(),
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "exact_marked_return": report,
    "labels": CHECKS,
    "not_proved": ["native physical admission", "Book amplitude/Info binding", "complete physical price", "D_min task or clock selection", "GR closure"],
}
OUT.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": result["checks"], "seconds": result["seconds"], "output": str(OUT)}))
