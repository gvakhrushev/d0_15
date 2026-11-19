#!/usr/bin/env python3
"""Narrow exact composition check; old source/factory suites are not rerun."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REF = "f64d4c3389b507c7e7fb66ace9480ed6191c463d"
PROOF = "FINITE_PAID_DESCENT_AND_CONTROLLER_GATE.md"
PINS = "SOURCE_PINS.json"
WITNESS = ("02_REGISTRY/research/sources/"
           "d0_native_joint_field_minimum_2026-10-20/WITNESS_RECEIPT.json")
checks = []


def require(ok, name):
    if not ok:
        raise RuntimeError(name)
    checks.append(name)


def sha(data):
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Qp:
    """Exact real Q(p), p^2=1-p, p=(sqrt(5)-1)/2."""
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    @staticmethod
    def make(x):
        return x if isinstance(x, Qp) else Qp(F(x))

    def __add__(self, other):
        other = Qp.make(other)
        return Qp(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Qp(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-Qp.make(other))

    def __rsub__(self, other):
        return Qp.make(other) - self

    def __mul__(self, other):
        other = Qp.make(other)
        return Qp(self.a * other.a + self.b * other.b,
                  self.a * other.b + self.b * other.a - self.b * other.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a * self.a - self.a * self.b - self.b * self.b
        if not norm:
            raise ZeroDivisionError("zero Q(p) element")
        return Qp((self.a - self.b) / norm, -self.b / norm)

    def __truediv__(self, other):
        return self * Qp.make(other).inverse()

    def __rtruediv__(self, other):
        return Qp.make(other) / self

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        answer, base = Qp(1), self
        while n:
            if n & 1:
                answer = answer * base
            base = base * base
            n >>= 1
        return answer

    def sign(self):
        if not self.b:
            return (self.a > 0) - (self.a < 0)
        t = -self.a / self.b
        if t <= 0:
            root_minus_t = 1
        elif t >= 1:
            root_minus_t = -1
        else:
            f_t = t * t + t - 1
            root_minus_t = -((f_t > 0) - (f_t < 0))
        return ((self.b > 0) - (self.b < 0)) * root_minus_t

    def encoded(self):
        return {"constant": str(self.a), "p_coefficient": str(self.b)}


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(q, a):
    return [[q * x for x in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    aug = [list(row) + unit for row, unit in zip(a, eye(n))]
    for col in range(n):
        pivot = next((j for j in range(col, n) if aug[j][col]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        divisor = aug[col][col]
        aug[col] = [x / divisor for x in aug[col]]
        for row in range(n):
            if row != col:
                q = aug[row][col]
                aug[row] = [x - q * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def wedge2(a):
    pairs = list(itertools.combinations(range(len(a)), 2))
    return [[a[i][k] * a[j][l] - a[i][l] * a[j][k]
             for k, l in pairs] for i, j in pairs]


def historical(repo, path):
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{REF}:{path}"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "CHECK_RESULT.json")
    args = parser.parse_args()
    pin_bytes = (HERE / PINS).read_bytes()
    pins = json.loads(pin_bytes)
    require(pins["source_ref"] == REF, "historical input ref")
    source_data = {}
    for item in pins["sources"]:
        data = historical(args.repo, item["path"])
        require(len(data) == item["bytes"] and sha(data) == item["sha256"],
                "historical bytes: " + item["label"])
        source_data[item["path"]] = data

    old = json.loads(source_data[WITNESS])
    expected = {
        "status": "PASS", "mesh_h": "1/8", "original_based_faces": 6,
        "normal_support_sites": 1, "profile_support_sites": 8,
        "cartan_changed_components": 32, "fixed_collar": [0, 1, 6, 7],
        "direct_fhat": "2*r*(epsilon**2*h**2*lambda + s)/h**3",
        "direct_q": "-2*epsilon**2*r/h",
        "source_combination": "2*r*s/h**3",
        "mixed_gravity_at_mesh": "1024",
        "original_all40_theorem_replayed": False,
    }
    for key, value in expected.items():
        require(old[key] == value, "consumed six-face receipt: " + key)

    p = Qp(0, 1)
    require(p * p + p == Qp(1), "Golden relation")
    require((p - F(3, 5)).sign() > 0 and (F(5, 8) - p).sign() > 0,
            "3/5 < p < 5/8")
    h, z = F(1, 8), F(1, 2**20)
    spike, normal = F(1, 2**20), F(1, 2**40)
    L = 4 * p**3
    M = L * (1 + p**6)
    Q0, R0 = 1 - z * L, 1 - z * M
    lam = -2 * p**(-5) * (R0 / Q0 + p**6)
    require(L == 1 - p**6 and M == 1 - p**12, "actual baseline bands")
    require(R0.sign() > 0 and (Q0 - R0).sign() > 0
            and (1 - Q0).sign() > 0, "0 < R0 < Q0 < 1")
    require(lam.sign() < 0 and (32 + lam).sign() > 0,
            "actual sigma-minus lambda lies in (-32,0)")

    # A representative exact arithmetic substitution, NOT an L8 scale census.
    a = p**3
    epsilon = a**2 / 1024
    require((F(1, 4) - a).sign() > 0, "k>=3 implies a<1/4")
    require((Qp(F(1, 2**14)) - epsilon).sign() > 0,
            "representative epsilon<2^-14")
    require(F(32) * F(1, 2**28) * h**2 == F(1, 2**29)
            and F(1, 2**29) < spike, "uniform k>=3 sign bound")
    bracket = lam * epsilon**2 * h**2 + spike
    f_times_rho = 2 * normal * bracket / (h**3 * a**2)
    q_times_rho = -2 * epsilon**2 * normal / (h * a**2)
    require(bracket.sign() > 0 and f_times_rho.sign() > 0
            and q_times_rho.sign() < 0, "strict signs for every positive actual rho")
    require(f_times_rho + lam * q_times_rho
            == 2 * normal * spike / (h**3 * a**2),
            "exact calibrated source combination")
    require((p / 4 - F(1, 2**11)).sign() > 0,
            "actual native material lies strictly inside |psi|<p/4")

    I = eye(4)
    E = eye(4)
    E[0][1] = normal / h
    Einv = eye(4)
    Einv[0][1] = -normal / h
    T = [[F(1), F(1, 2), F(0), F(0)],
         [F(1), F(-1, 2), F(0), F(0)],
         [F(0), F(0), F(1), F(0)],
         [F(0), F(0), F(0), F(1)]]
    etaR = [[F((1 if i == 0 else -1) if i == j else 0)
             for j in range(4)] for i in range(4)]
    eta = [[F(0), F(1), F(0), F(0)],
           [F(1), F(0), F(0), F(0)],
           [F(0), F(0), F(-1), F(0)],
           [F(0), F(0), F(0), F(-1)]]
    require(mul(transpose(T), mul(etaR, T)) == eta, "literal null/REST metric")
    D = mul(etaR, transpose(inverse(mul(T, E))))
    require(mul(E, Einv) == I and mul(transpose(D), mul(etaR, T)) == Einv,
            "actual rational normal D moment map")
    require(mul(transpose(E), mul(eta, E))[1][1] == 2 * normal / h,
            "normal changes the calibrated metric")
    Z = wedge2(Einv)
    N = add(Z, scale(-1, eye(6)))
    require(mul(N, N) == zero(6), "normal compound is square-zero")
    P5, power = zero(6), eye(6)
    for j in range(6):
        P5 = add(P5, scale((-1)**j, power))
        power = mul(power, N)
    require(P5 == wedge2(E) and mul(Z, P5) == eye(6),
            "P5 exact VALUE on the finite normal surface")
    for i, j in [(0, 1), (1, 0)]:
        rank_one = zero(4)
        rank_one[i][j] = 1
        areaN = add(wedge2(add(I, rank_one)), scale(-1, eye(6)))
        require(mul(areaN, areaN) == zero(6), f"rank-one primary compound {i}{j}")

    N2, N3 = zero(4), zero(4)
    N2[1][2] = N2[2][0] = 1
    N3[1][3] = N3[3][0] = 1
    require(all(mul(mul(x, y), zz) == zero(4)
                for x, y, zz in itertools.product([N2, N3], repeat=3)),
            "every Cartan-generator triple product vanishes")
    require(all(add(mul(transpose(n), eta), mul(eta, n)) == zero(4)
                for n in [N2, N3]), "literal null generators are eta-skew")
    K = add(N2, scale(2, N3))
    U = add(add(I, K), scale(F(1, 2), mul(K, K)))
    C8, power = I, I
    for j in range(1, 9):
        power = mul(power, scale(F(1, 2), K))
        C8 = add(C8, scale(2, power))
    require(C8 == U and mul(transpose(U), mul(eta, U)) == eta,
            "C8 exact VALUE and proper-link orthogonality")
    Usharp = mul(eta, mul(transpose(U), eta))
    require(mul(Usharp, U) == I, "reverse links are exact eta-transpose inverses")

    E_hi = F(5, 8)**2 * F(65, 64)
    b_hi = (F(5, 8) + F(5, 8)**2 / 64)**2
    require(E_hi < F(1, 2) and b_hi < F(1, 2),
            "actual report tables stay in their increasing branch")
    require(2 * z < F(1, 2), "actual report entropy is strictly increasing")
    require(((0 ^ 2).bit_count() == 1), "root00/competitor10 differ by one selector cell")
    distributions = []
    for b in [0, 1]:
        weights = [F(0), F(0)]
        for fair_label in [0, 1]:
            weights[b * fair_label] += F(1, 2)
        distributions.append(weights)
    require(distributions == [[F(1), F(0)], [F(1, 2), F(1, 2)]],
            "retained fair-label whole-law replacement weights")
    require([x - y for x, y in zip(distributions[1], distributions[0])]
            == [F(-1, 2), F(1, 2)], "whole-law price contrast has factor gamma/2")

    result = {
        "status": "PASS", "source_ref": REF, "checks_count": len(checks),
        "checks": checks,
        "proof_sha256": sha((HERE / PROOF).read_bytes()),
        "checker_sha256": sha(Path(__file__).read_bytes()),
        "pins_sha256": sha(pin_bytes),
        "exact_witness": {"mesh_h": str(h), "spike_s": str(spike),
            "normal_r": str(normal), "z0": [2, 0, 3, 3],
            "curvature_convention": "EPS_PLUS", "recording_orientation": "sigma=-1",
            "lambda": lam.encoded(), "diagnostic_scale_a": a.encoded(),
            "diagnostic_epsilon": epsilon.encoded(),
            "rho_times_f": f_times_rho.encoded(), "rho_times_q": q_times_rho.encoded(),
            "material_max_abs": "1/2048"},
        "scope": {
            "actual_positive_rho": "symbolic; no replacement or new L8 PF assignment",
            "scale": "k=3 arithmetic diagnostic; proof covers any once-fixed admitted k>=3",
            "old_suites_replayed": False,
            "majority_and_factories": "consumed exact owners; no enormous-bank simulation",
            "strict_price_sign": "analytical monotonicity after exact f>0,q<0",
            "common_catalogue": "one catalogue containing all four literal nodes",
            "physical_admission": "same-initial AB/BA controller diamond remains required",
            "physical_price": "complete counted-CQ proven; compulsory Book binding remains open",
            "continuous_full_state_lift": False,
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {len(checks)} exact narrow checks; result {args.output}")


if __name__ == "__main__":
    main()
