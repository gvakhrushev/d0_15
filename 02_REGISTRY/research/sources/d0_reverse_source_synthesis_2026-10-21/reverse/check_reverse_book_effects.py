#!/usr/bin/env python3
"""Exact finite real-Golden inverse and Book first-source controls only."""
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
REF = "2961dc6ee4abcda0a0fb2aa36dc6ecd7e62a6535"
PROOF = "REVERSE_BOOK_EFFECT_RECONSTRUCTION.md"
PINS = "REVERSE_SOURCE_PINS.json"
checks = []


def require(ok, name):
    if not ok:
        raise RuntimeError(name)
    checks.append(name)


def sha(data):
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Qa:
    """Q(a), a^4+a^2-1=0, with its positive Golden embedding."""
    c: tuple = (F(0), F(0), F(0), F(0))

    def __post_init__(self):
        object.__setattr__(self, "c", tuple(F(x) for x in self.c))

    @staticmethod
    def of(x):
        return x if isinstance(x, Qa) else Qa((F(x), 0, 0, 0))

    def __add__(self, other):
        other = Qa.of(other)
        return Qa(tuple(x + y for x, y in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return Qa(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self + (-Qa.of(other))

    def __rsub__(self, other):
        return Qa.of(other) - self

    def __mul__(self, other):
        other = Qa.of(other)
        coeff = [F(0)] * 7
        for i in range(4):
            for j in range(4):
                coeff[i+j] += self.c[i] * other.c[j]
        for j in range(6, 3, -1):
            coeff[j-4] += coeff[j]
            coeff[j-2] -= coeff[j]
        return Qa(tuple(coeff[:4]))

    __rmul__ = __mul__

    def __truediv__(self, other):
        return Qa(tuple(x / F(other) for x in self.c))

    def __pow__(self, n):
        result = Qa.of(1)
        for _ in range(n):
            result = result * self
        return result


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zeros(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(s, a):
    return [[s*x for x in row] for row in a]


def trans(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def trace(a):
    return sum(a[j][j] for j in range(len(a)))


def inv(a):
    n = len(a)
    aug = [list(row)+unit for row, unit in zip(a, eye(n))]
    for j in range(n):
        k = next((k for k in range(j, n) if aug[k][j]), None)
        if k is None:
            raise ValueError("singular matrix")
        aug[j], aug[k] = aug[k], aug[j]
        pivot = aug[j][j]
        aug[j] = [x/pivot for x in aug[j]]
        for k in range(n):
            if k != j:
                c = aug[k][j]
                aug[k] = [x-c*y for x, y in zip(aug[k], aug[j])]
    return [row[n:] for row in aug]


def determinant_jet(a, da):
    """Permutation expansion and its first coefficient, without log/eigenvalues."""
    n = len(a)
    value, derivative = F(0), F(0)
    for perm in itertools.permutations(range(n)):
        sign = (-1)**sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term = F(sign)
        for i in range(n):
            term *= a[i][perm[i]]
        value += term
        for changed in range(n):
            term = F(sign)
            for i in range(n):
                term *= da[i][perm[i]] if i == changed else a[i][perm[i]]
            derivative += term
    return value, derivative


def expectation(e, v):
    return sum(v[i] * e[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))


def reconstruct(e, a, p):
    n = len(e)
    diagonal = []
    for j in range(n):
        v = [Qa.of(int(i == j)) for i in range(n)]
        diagonal.append(expectation(e, v))
    result = [[Qa.of(0) for _ in range(n)] for _ in range(n)]
    reciprocal = a + a**3 / 2  # exactly 1/(2*a*p)
    for j in range(n):
        result[j][j] = diagonal[j]
        for k in range(j+1, n):
            v = [Qa.of(0) for _ in range(n)]
            v[j], v[k] = a, p
            q = expectation(e, v)
            answer = (q-p*diagonal[j]-p**2*diagonal[k])*reciprocal
            result[j][k] = result[k][j] = answer
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "REVERSE_RESULT.json")
    args = parser.parse_args()
    pin_bytes = (HERE/PINS).read_bytes()
    pins = json.loads(pin_bytes)
    require(pins["source_ref"] == REF, "fixed historical input")
    for pin in pins["sources"]:
        data = subprocess.check_output(["git", "-C", str(args.repo), "show", f"{REF}:{pin['path']}"])
        require(sha(data) == pin["sha256"] and len(data) == pin["bytes"],
                "historical pin: " + pin["label"])

    a = Qa((0, 1, 0, 0))
    p = a*a
    require(p+p*p == Qa.of(1), "normalized unequal Golden pair")
    require((2*a*p)*(a+a**3/2) == Qa.of(1), "exact native tomography denominator")
    A = [[F(1,2), F(1,4), F(0)], [F(0), F(1,3), F(1,5)],
         [F(1,7), F(0), F(1,2)]]
    C = [[F(1,3), F(0), F(0)], [F(0), F(1,4), F(0)],
         [F(0), F(0), F(1,5)]]
    W = A+C
    P = zeros(6)
    for j in range(3):
        P[j][j] = 1
    DP = zeros(6)
    DP[0][3] = DP[3][0] = 1
    DW = [[F(1,11), F(0), F(0)], [F(0), F(1,13), F(0)],
          [F(0), F(0), F(1,17)], [F(1,19), F(0), F(0)],
          [F(0), F(1,23), F(0)], [F(0), F(0), F(1,29)]]
    N = mul(trans(W), W)
    B = mul(trans(W), mul(P, W))
    DN = add(mul(trans(DW), W), mul(trans(W), DW))
    DB_frozen = add(mul(trans(DW), mul(P, W)), mul(trans(W), mul(P, DW)))
    DB = add(DB_frozen, mul(trans(W), mul(DP, W)))
    require(add(mul(P, DP), mul(DP, P)) == DP, "moving-cut tangent equation")
    require(add(N, scale(-1, B)) == mul(trans(C), C), "actual two-effect order B<=N")
    require(all(sum(abs(x) for x in row) < 1 for row in N), "diagnostic N is a strict effect")
    require(mul(N, B) != mul(B, N), "genuine noncommuting normalizer/return pair")
    for name, effect in [("N", N), ("B", B), ("DN", DN), ("DB", DB)]:
        require(reconstruct(effect, a, p) == [[Qa.of(x) for x in row] for row in effect],
                "Golden full real inverse: " + name)
    z, r_R = F(1, 2**20), 128
    M = add(scale(1-z, N), scale(z, B))
    DM = add(scale(1-z, DN), scale(z, DB))
    source = r_R * (trace(mul(inv(N), DN))-trace(mul(inv(M), DM)))
    detN, detDN = determinant_jet(N, DN)
    detM, detDM = determinant_jet(M, DM)
    require(detN > 0 and detM > 0, "strict logarithm domain")
    require(source == r_R*(detDN/detN-detDM/detM), "Book full first source matches determinant jet")
    frozen_source = r_R*(trace(mul(inv(N), DN))-
                         trace(mul(inv(M), add(scale(1-z, DN), scale(z, DB_frozen)))))
    require(source != frozen_source, "omitting moving-cut source is detected")
    moving_cut_scalar_source = r_R*z/(1-z/2)
    require(moving_cut_scalar_source > 0, "one-column moving-cut source is strictly nonzero")

    W0 = [[a, Qa.of(0)], [Qa.of(0), a], [p, Qa.of(0)], [Qa.of(0), p]]
    W1 = [[a, Qa.of(0)], [Qa.of(0), p], [p, Qa.of(0)], [Qa.of(0), a]]
    P2 = [[F(i == j and i < 2) for j in range(4)] for i in range(4)]
    I2 = [[Qa.of(x) for x in row] for row in eye(2)]
    require(mul(trans(W0), W0) == I2 and mul(trans(W1), W1) == I2,
            "both literal Golden/CNOT maps are complete isometries")
    require([row[0] for row in W0] == [row[0] for row in W1],
            "same ENTIRE prepared e0 output")
    B0, B1 = mul(trans(W0), mul(P2, W0)), mul(trans(W1), mul(P2, W1))
    require(B0 == [[p, Qa.of(0)], [Qa.of(0), p]]
            and B1 == [[p, Qa.of(0)], [Qa.of(0), p*p]],
            "unused input column changes the actual return effect")
    require(p-p*p == 2*p-1, "exact Golden gap p-p^2=2p-1")
    # x^2+x-1 is strictly increasing for x>=0 and changes sign on (1/2,1).
    require(F(1,2)**2+F(1,2)-1 < 0 < F(1)**2+F(1)-1,
            "positive Golden embedding p>1/2, hence strict return gap")
    CNOT = eye(4)
    CNOT[1], CNOT[3] = CNOT[3], CNOT[1]
    require(mul(CNOT, W0) == W1, "countermodel difference is the literal CNOT")

    # Consume the published AABB=I / ABAB=CX(c,b) words; do not rerun
    # their gate algebra. Only check the new single-prepared-input application.
    oldW0, oldW1 = zeros(8, 2), zeros(8, 2)
    oldW0[0][0] = oldW1[0][0] = 1
    oldW0[4][1] = oldW1[5][1] = 1
    oldP = zeros(8)
    oldP[0][0] = oldP[4][4] = 1
    require(mul(trans(oldW0), oldW0) == eye(2)
            and mul(trans(oldW1), oldW1) == eye(2),
            "consumed equal-inventory maps have the same complete norm")
    require([row[0] for row in oldW0] == [row[0] for row in oldW1],
            "consumed equal-inventory control agrees on the full c=0 output")
    oldB0 = mul(trans(oldW0), mul(oldP, oldW0))
    oldB1 = mul(trans(oldW1), mul(oldP, oldW1))
    require(oldB0 == eye(2) and oldB1 == [[F(1), F(0)], [F(0), F(0)]],
            "published auxiliary-blank cut detects the unseen c=1 column")
    oldM0 = add(scale(1-z, eye(2)), scale(z, oldB0))
    oldM1 = add(scale(1-z, eye(2)), scale(z, oldB1))
    require(determinant_jet(oldM0, zeros(2))[0] == 1
            and determinant_jet(oldM1, zeros(2))[0] == 1-z and 0 < z < 1,
            "consumed Book gap is strictly -r_R log(1-z)")

    # Original two-code cost C=(1,2), analytical t=log(4); P=|+><+|.
    marked = [a/2, p/4]
    norm_marked = sum(x*x for x in marked)
    coherent_return = (marked[0]+marked[1])**2/2
    classically_reweighted = norm_marked/2
    require(coherent_return-classically_reweighted == a*p/8,
            "noncommuting cost dephasing loses exact coherent cut term")

    result = {
        "status": "PASS", "source_ref": REF, "checks_count": len(checks), "checks": checks,
        "proof_sha256": sha((HERE/PROOF).read_bytes()),
        "checker_sha256": sha(Path(__file__).read_bytes()), "pins_sha256": sha(pin_bytes),
        "diagnostic": {"dimension": 3, "real_Golden_probes": 6,
            "z": str(z), "oldRIGHT_spectator_factor": r_R,
            "full_first_source": str(source), "frozen_cut_wrong_source": str(frozen_source),
            "moving_cut_scalar_source": str(moving_cut_scalar_source)},
        "scope": {"old_suites_replayed": False,
            "actual_fields_or_factory_bank_simulated": False,
            "matrices": "small exact inverse/source control; not a new full128 execution",
            "countermodel": "Golden/CNOT control plus prepared-input application of owned AABB/ABAB; not equal full controller/price",
            "physical_input_cut_coverage": "hypothesis, not supplied by reconstruction",
            "primitive_selector_or_Info_derived": False, "GR_closed": False},
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(f"PASS: {len(checks)} exact reverse-interface checks; result {args.output}")


if __name__ == "__main__":
    main()
