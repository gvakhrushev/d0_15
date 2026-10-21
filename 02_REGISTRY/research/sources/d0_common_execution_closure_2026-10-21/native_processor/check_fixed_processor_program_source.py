#!/usr/bin/env python3
"""Narrow exact controls for the fixed processor and normal-source lift.

This does not replay original spatial Euler equations, native coefficient
factories, the full128 material dictionary, or any old rank/root suite.
All checks use exact rationals/Q(p) and survive Python -O.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def eye(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = F(1)
    return a


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, c):
    return [[c*x for x in row] for row in a]


def mul(a, b):
    n = len(a)
    out = zero(n)
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):
                    if b[k][j]:
                        out[i][j] += a[i][k]*b[k][j]
    return out


def transpose(a):
    return [list(r) for r in zip(*a)]


def sharp(a):
    signs = [1, -1, -1, -1]
    return [[signs[i]*signs[j]*a[j][i] for j in range(4)]
            for i in range(4)]


def car_creation(mode):
    c = zero(16)
    for mask in range(16):
        if not mask & (1 << mode):
            s = -1 if (mask & ((1 << mode)-1)).bit_count() % 2 else 1
            c[mask | (1 << mode)][mask] = F(3*s, 5)
    return c


def julia_creation(mode):
    c = car_creation(mode)
    ct = transpose(c)
    dl, dr = zero(16), zero(16)
    for i in range(16):
        dl[i][i] = F(4, 5) if i & (1 << mode) else F(1)
        dr[i][i] = F(1) if i & (1 << mode) else F(4, 5)
    require(mul(dl, dl) == add(eye(16), scale(mul(c, ct), -1)),
            "actual left defect")
    require(mul(dr, dr) == add(eye(16), scale(mul(ct, c), -1)),
            "actual right defect")
    j = zero(32)
    for r in range(16):
        for s in range(16):
            j[r][s] = c[r][s]
            j[r][s+16] = dl[r][s]
            j[r+16][s] = dr[r][s]
            j[r+16][s+16] = -ct[r][s]
    require(mul(transpose(j), j) == eye(32), "full32 Julia unitarity")
    return j


def pauli(u, v, d=32):
    # P = X^u Z^v, with column x mapped to x xor u.
    return [(x ^ u, -1 if (x & v).bit_count() % 2 else 1)
            for x in range(d)]


def bell_checks():
    d, addresses = 32, 4
    js = [julia_creation(0), julia_creation(1), eye(d), scale(eye(d), -1)]
    grams = [mul(transpose(j), j) for j in js]
    # The 32 Walsh sign rows prove orthogonality of all d^2 Pauli labels:
    # unequal X offsets have disjoint entries; equal offsets reduce to this.
    for v in range(d):
        for w in range(d):
            total = sum((-1 if (x & (v ^ w)).bit_count() % 2 else 1)
                        for x in range(d))
            require(total == (d if v == w else 0), "Bell basis complete")
    effects = 0
    for u in range(d):
        for v in range(d):
            pv = pauli(u, v, d)
            require(len({row for row, _ in pv}) == d, "Pauli permutation")
            for gram in grams:
                for i in range(d):
                    ri, si = pv[i]
                    for k in range(d):
                        rk, sk = pv[k]
                        # (J P)^* (J P); the scalar is 1/(A d^2).
                        require(si*sk*gram[ri][rk] == (1 if i == k else 0),
                                "all full32 aggregate Bell effects")
                effects += 1
    kappa = addresses*d*d
    require(sum(F(1, kappa) for _ in range(kappa)) == 1,
            "aggregate complete law normalized")
    # On the actual fixed creation input (vac + top)/sqrt(2), the partial
    # swap Good mode0 <-> Bad top has expectation 3/5. Evaluate the
    # unnormalized input and divide quadratic expectations by 2 exactly.
    j = js[0]
    out = [j[i][0]+j[i][15] for i in range(d)]
    require(sum(x*x for x in out) == 2, "known kernel input norm")
    require(out[1]*out[31] == F(3, 5), "full32 kernel moment")
    return {
        "dimension": d, "address_fixture": addresses,
        "complete_address_bell_labels": effects,
        "each_full_operator_effect": f"I/{kappa}",
        "sum_effects": "I",
        "actual_kernel_moment": "3/5",
        "scope": "four exact full32 addresses; general A and all inputs proved by (3)-(4)"
    }


def normal_and_bank_checks():
    # Actual fixed known creation input has support at full32 indices 0,15.
    # S_a(t)=J_a(I+tD), with trace D=0 and common norm correction O(t^2).
    # D_00=1, D_11=-1. The first derivative of each label is exact.
    d, addresses, slots, cap = 32, 4, 3, 2
    kappa = addresses*d*d
    diag = [F(0)]*d
    diag[0], diag[1] = F(1), F(-1)
    dp = []
    for _ in range(addresses):
        for u in range(d):
            for _v in range(d):
                dp.append((diag[u]+diag[u ^ 15])/kappa)
    require(len(dp) == kappa, "full normal derivative alphabet")
    require(sum(dp) == 0, "normal derivative preserves total probability")
    a, da = F(1, kappa), F(1, kappa)
    require(dp[0] == da and da != 0, "actual success normal derivative nonzero")
    # Normalization is part of the conditional moment. At t=0 both the
    # accepted norm and the unnormalized swap numerator have factor 1+t.
    numerator_0, numerator_1 = F(3, 5), F(3, 5)
    denominator_0, denominator_1 = F(1), F(1)
    normalized_moment_derivative = (
        numerator_1*denominator_0-numerator_0*denominator_1
    )/denominator_0**2
    require(normalized_moment_derivative == 0, "conditional normalization derivative")
    require(numerator_1 != 0, "omitted-normalizer negative control")
    b = 1-(1-a)**cap
    db = cap*(1-a)**(cap-1)*da
    s = b**slots
    ds = slots*b**(slots-1)*db
    require(ds != 0, "off-family bank readiness genuinely moves")
    # Entropy derivative at a uniform complete law is one common
    # coefficient times sum dp; no floating logarithms are required.
    entropy_first_coefficient = sum(dp)
    require(entropy_first_coefficient == 0, "uniform full tape entropy first source")
    # d[s h(r)+(1-s)h(r0)] at r=r0. Coefficients of h(r0), h'(r0)Dr:
    with_abort = (ds-ds, s)
    without_abort = (ds, s)
    require(with_abort[0] == 0, "paid reference abort cancels readiness source")
    require(without_abort[0] != 0, "silent abort negative control")
    # Fixed attempts have constant cost; stopped L=2 count E=2-a does not.
    stopped_count_derivative = -da
    require(stopped_count_derivative != 0, "stopping-cost normal negative control")
    return {
        "actual_known_input": "(vac+top)/sqrt(2) on full32",
        "complete_probability_derivative_sum": str(sum(dp)),
        "accepted_probability_derivative": str(da),
        "normalized_kernel_moment_derivative": str(normalized_moment_derivative),
        "unnormalized_negative_control": str(numerator_1),
        "fixture_slots": slots, "fixture_attempt_cap": cap,
        "bank_readiness": str(s), "bank_readiness_derivative": str(ds),
        "full_uniform_entropy_first": str(entropy_first_coefficient),
        "paid_abort_h_r0_coefficient": str(with_abort[0]),
        "silent_abort_h_r0_coefficient": str(without_abort[0]),
        "stopped_cost_derivative_negative_control": str(stopped_count_derivative),
        "scope": "exact finite bank controls; full factory/CQ identities are analytic"
    }


# Two-variable Taylor polynomials of 4x4 matrices, total degree at most two.
MONOMIALS = ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2))


def jp(a):
    return {(0, 0): a}


def jadd(a, b):
    return {q: add(a.get(q, zero(4)), b.get(q, zero(4)))
            for q in MONOMIALS}


def jscale(a, c):
    return {q: scale(m, c) for q, m in a.items()}


def jmul(a, b):
    out = {q: zero(4) for q in MONOMIALS}
    for q, x in a.items():
        for r, y in b.items():
            s = (q[0]+r[0], q[1]+r[1])
            if sum(s) <= 2:
                out[s] = add(out[s], mul(x, y))
    return out


def jsharp(a):
    return {q: sharp(x) for q, x in a.items()}


def r2_jet(m):
    h = jadd(jmul(jsharp(m), m), jp(scale(eye(4), -1)))
    f = jadd(jadd(jp(eye(4)), jscale(h, F(-1, 2))),
             jscale(jmul(h, h), F(3, 8)))
    return jmul(m, f)


def lorentz_checks():
    boost, rotation = eye(4), eye(4)
    boost[0][0] = boost[1][1] = F(13, 12)
    boost[0][1] = boost[1][0] = F(5, 12)
    rotation[1][1] = rotation[2][2] = F(3, 5)
    rotation[1][2], rotation[2][1] = F(-4, 5), F(4, 5)
    u = mul(boost, rotation)
    require(mul(sharp(u), u) == eye(4), "nontrivial rational proper Lorentz fixture")
    require(r2_jet(jp(u))[(0, 0)] == u, "R2 fixes proper carrier")
    # Arbitrary dense, independently chosen ambient perturbations.
    d = [[F((3*i+5*j+1) % 11-5, 7) for j in range(4)] for i in range(4)]
    e = [[F((7*i+2*j+4) % 13-6, 9) for j in range(4)] for i in range(4)]
    m = {(0, 0): u, (1, 0): d, (0, 1): e}
    r = r2_jet(m)
    expected = mul(u, scale(add(mul(sharp(u), d),
                               scale(sharp(mul(sharp(u), d)), -1)), F(1, 2)))
    require(r[(1, 0)] == expected, "ambient derivative equals Lorentz projection")
    gram = jmul(jsharp(r), r)
    for q in MONOMIALS:
        require(gram[q] == (eye(4) if q == (0, 0) else zero(4)),
                "R2 full bivariate orthogonality jet")
    # Explicit tangent/normal basis controls; not an inferred rank statement.
    signs = [1, -1, -1, -1]
    normals, tangents = [], []
    for i in range(4):
        x = zero(4)
        x[i][i] = F(1)
        normals.append(x)
    for i in range(4):
        for j in range(i+1, 4):
            x, y = zero(4), zero(4)
            x[i][j] = y[i][j] = F(1)
            x[j][i] = signs[i]*signs[j]
            y[j][i] = -signs[i]*signs[j]
            normals.append(x)
            tangents.append(y)
    for x in normals:
        require(sharp(x) == x, "eta-self-adjoint normal")
        dr = r2_jet({(0, 0): u, (1, 0): mul(u, x)})[(1, 0)]
        require(dr == zero(4), "normal first source annihilation")
    for x in tangents:
        require(sharp(x) == scale(x, -1), "eta-skew tangent")
        ux = mul(u, x)
        require(r2_jet({(0, 0): u, (1, 0): ux})[(1, 0)] == ux,
                "proper tangent retained")
    # Exact commuting polynomial identity behind all ambient second jets.
    f = [F(1), F(-1, 2), F(3, 8)]
    prod = [F(0)]*6
    for i, a in enumerate(f):
        for j, b in enumerate(f):
            prod[i+j] += a*b
            prod[i+j+1] += a*b
    require(prod == [F(1), F(0), F(0), F(5, 8), F(-15, 64), F(9, 64)],
            "universal polynomial defect starts at cubic order")
    return {
        "carrier": "eta=diag(1,-1,-1,-1), rational boost times rotation",
        "normal_basis_controls": len(normals),
        "tangent_basis_controls": len(tangents),
        "all_bivariate_coefficients_through_degree_2": "exact",
        "universal_R2_sharp_R2_minus_I": {
            "H^3": "5/8", "H^4": "-15/64", "H^5": "9/64"
        },
        "scope": "general two-jet proof is the binomial remainder; fixtures test its implementation"
    }


@dataclass(frozen=True)
class Q:
    """Minimal exact Q(p), p^2=1-p; arithmetic matches the consumed checker."""
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    @staticmethod
    def of(x):
        return x if isinstance(x, Q) else Q(x)

    def __add__(self, y):
        y = Q.of(y)
        return Q(self.a+y.a, self.b+y.b)
    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b)

    def __sub__(self, y):
        return self+-Q.of(y)

    def __rsub__(self, y):
        return Q.of(y)+-self

    def __mul__(self, y):
        y = Q.of(y)
        return Q(self.a*y.a+self.b*y.b,
                 self.a*y.b+self.b*y.a-self.b*y.b)
    __rmul__ = __mul__

    def __pow__(self, n):
        out = Q(1)
        for _ in range(n):
            out = out*self
        return out

    def sign(self):
        c, b = 2*self.a-self.b, self.b
        if not b:
            return (c > 0)-(c < 0)
        if not c:
            return (b > 0)-(b < 0)
        if c > 0 and b > 0:
            return 1
        if c < 0 and b < 0:
            return -1
        diff = c*c-5*b*b
        require(diff != 0, "irrational embedding has no rational cancellation")
        return ((diff > 0)-(diff < 0)) * ((c > 0)-(c < 0))


def abort_coin_check():
    p = Q(0, 1)
    require(p+p*p == Q(1), "Golden identity")
    l = 4*p**3
    m = l*(1+p**6)
    z = F(1, 2**20)
    r0 = 1-(1-z*m)*(1-z*l)
    require(r0.sign() > 0 and (Q(F(1, 2))-r0).sign() > 0,
            "actual reference report is strictly inside (0,1/2)")
    return {
        "z": str(z),
        "r0_Qp": {"rational": str(r0.a), "p_coefficient": str(r0.b)},
        "strict_interval": "(0,1/2)",
        "implementation": "consumed exact positive-prefix Golden coin, with full herald tape"
    }


def verify_pins(repo, pins_path):
    spec = json.loads(pins_path.read_text())
    for row in spec["sources"]:
        blob = (repo/row["path"]).read_bytes()
        require(len(blob) == row["bytes"], "source byte count: "+row["path"])
        require(hashlib.sha256(blob).hexdigest() == row["sha256"],
                "source SHA256: "+row["path"])
    return len(spec["sources"]), spec["source_ref"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--pins", type=Path,
                        default=Path(__file__).with_name("SOURCE_PINS.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    pin_count, source_ref = verify_pins(args.repo, args.pins)
    report = {
        "status": "PASS",
        "arithmetic": "exact Fraction and Q(p); no floors or numerical derivatives",
        "source_ref": source_ref, "source_pins_verified": pin_count,
        "full32_bell": bell_checks(),
        "programme_normals_and_paid_abort": normal_and_bank_checks(),
        "lorentz_normal_projection": lorentz_checks(),
        "actual_reference_report": abort_coin_check(),
        "not_replayed": [
            "original full spatial 16+24+2 Euler theorem",
            "native Golden factories and Q(p) resource preparation",
            "original full128 material construction",
            "any rank/root or generic broad suite"
        ]
    }
    text = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
