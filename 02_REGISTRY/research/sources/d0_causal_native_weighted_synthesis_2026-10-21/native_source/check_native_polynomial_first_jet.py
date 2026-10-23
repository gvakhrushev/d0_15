#!/usr/bin/env python3
"""Narrow exact controls; the general finite-family jet claims are analytic."""
from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import math
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


@dataclass(frozen=True)
class Q:
    """Exact Q(p), p^2=1-p, with the positive real embedding."""
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
        return Q(self.a + y.a, self.b + y.b)
    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b)

    def __sub__(self, y):
        return self + -Q.of(y)

    def __rsub__(self, y):
        return Q.of(y) + -self

    def __mul__(self, y):
        y = Q.of(y)
        return Q(self.a * y.a + self.b * y.b,
                 self.a * y.b + self.b * y.a - self.b * y.b)
    __rmul__ = __mul__

    def inv(self):
        den = self.a**2 - self.a*self.b - self.b**2
        require(bool(den), "nonzero Q(p) denominator")
        return Q((self.a-self.b)/den, -self.b/den)

    def __truediv__(self, y):
        return self * Q.of(y).inv()

    def __rtruediv__(self, y):
        return Q.of(y) * self.inv()

    def __pow__(self, n):
        if n < 0:
            return self.inv() ** -n
        out, base = Q(1), self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n //= 2
        return out

    def __bool__(self):
        return bool(self.a or self.b)

    def __eq__(self, y):
        try:
            y = Q.of(y)
        except (TypeError, ValueError):
            return False
        return self.a == y.a and self.b == y.b

    def sign(self):
        aa, bb = 2*self.a-self.b, self.b
        if not bb:
            return (aa > 0) - (aa < 0)
        if not aa:
            return (bb > 0) - (bb < 0)
        if aa > 0 and bb > 0:
            return 1
        if aa < 0 and bb < 0:
            return -1
        cmp = (aa*aa > 5*bb*bb) - (aa*aa < 5*bb*bb)
        return cmp if aa > 0 else -cmp

    def text(self):
        return [str(self.a), str(self.b)]


P = Q(0, 1)
KEYS = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]


def zero(n, m=None):
    return [[Q() for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n):
    out = zero(n)
    for i in range(n):
        out[i][i] = Q(1)
    return out


def trans(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, c):
    return [[c*x for x in row] for row in a]


def mul(a, b):
    out = zero(len(a), len(b[0]))
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        out[i][j] = out[i][j] + x*y
    return out


def equal(a, b):
    return all(x == y for ar, br in zip(a, b) for x, y in zip(ar, br))


def jadd(a, b):
    n = len(next(iter(a.values())))
    return {k: add(a.get(k, zero(n)), b.get(k, zero(n))) for k in KEYS}


def jscale(a, c):
    return {k: scale(v, c) for k, v in a.items()}


def jmul(a, b):
    n = len(next(iter(a.values())))
    out = {k: zero(n) for k in KEYS}
    for ka, aa in a.items():
        for kb, bb in b.items():
            kk = (ka[0]+kb[0], ka[1]+kb[1])
            if sum(kk) <= 2:
                out[kk] = add(out[kk], mul(aa, bb))
    return out


def jtrans(a):
    return {k: trans(v) for k, v in a.items()}


def jequal(a, b, keys=KEYS):
    n = len(next(iter(a.values())))
    return all(equal(a.get(k, zero(n)), b.get(k, zero(n))) for k in keys)


def ext2(a):
    pairs = list(itertools.combinations(range(4), 2))
    out = {k: zero(6) for k in KEYS}
    for i, (r, s) in enumerate(pairs):
        for j, (u, v) in enumerate(pairs):
            for ka, aa in a.items():
                for kb, bb in a.items():
                    kk = (ka[0]+kb[0], ka[1]+kb[1])
                    if sum(kk) <= 2:
                        out[kk][i][j] += aa[r][u]*bb[s][v]-aa[r][v]*bb[s][u]
    return out


def polynomial_inverse(z, degree):
    n = len(z[(0, 0)])
    nn = jadd(z, {(0, 0): scale(eye(n), -1)})
    result = {(0, 0): eye(n)}
    power = {(0, 0): eye(n)}
    for k in range(1, degree+1):
        power = jmul(power, nn)
        result = jadd(result, jscale(power, (-1)**k))
    return result


def car_control():
    creators = []
    for role in range(4):
        c = zero(16)
        for mask in range(16):
            if not mask & (1 << role):
                c[mask | (1 << role)][mask] = Q((-1)**((mask & ((1 << role)-1)).bit_count()))
        creators.append(c)
    for a in range(4):
        for b in range(4):
            ab = add(mul(trans(creators[a]), creators[b]),
                     mul(creators[b], trans(creators[a])))
            require(equal(ab, scale(eye(16), int(a == b))), "full16 CAR identity")
        require(all(not creators[a][i][15] for i in range(16)), "common top kernel")
    v = [Q(F(1, 5)), Q(F(2, 5)), Q(F(-2, 5)), Q(0)]
    c = zero(16)
    for vv, cc in zip(v, creators):
        c = add(c, scale(cc, vv))
    k = sum(vv*vv for vv in v)
    require(k == F(9, 25), "strict creation fixture")
    factor = (Q(F(4, 5))-1)/k
    dl = add(eye(16), scale(mul(c, trans(c)), factor))
    dr = add(eye(16), scale(mul(trans(c), c), factor))
    jj = [c[i]+dl[i] for i in range(16)] + [dr[i]+scale(trans(c), -1)[i] for i in range(16)]
    require(equal(mul(trans(jj), jj), eye(32)), "complete Julia unitary including complement")
    scaled_out = [[jj[i][0]+jj[i][15]] for i in range(32)]
    require(mul(trans(scaled_out), scaled_out)[0][0] == 2, "normalized fixed input/output")
    for a in range(4):
        u, w = (1 << a), 31
        require(scaled_out[u][0]*scaled_out[w][0] == v[a], "top-reference partial-swap expectation")
        vp, vm = eye(32), scale(eye(32), -1)
        for mat in (vp, vm):
            mat[u][u] = mat[w][w] = Q(0)
            mat[u][w] = mat[w][u] = Q(1)
        require(equal(mul(vp, vp), eye(32)) and equal(mul(vm, vm), eye(32)),
                "two full signed involutions")
    return {"carrier": 32, "all_four_outputs_exact": True, "full_complement_retained": True}


def coframe_control():
    e0 = eye(4)
    e0[1][0] = Q(F(3, 14))
    e0i = eye(4)
    e0i[1][0] = Q(F(-3, 14))
    d = [[Q(F(1+3*i-2*j, 37)) for j in range(4)] for i in range(4)]
    f = [[Q(F((-1)**(i+j)*(2+2*i+j), 43)) for j in range(4)] for i in range(4)]
    ee = {(0, 0): e0, (1, 0): d, (0, 1): f}
    dx = {(1, 0): mul(e0i, d), (0, 1): mul(e0i, f)}
    ei = jmul(jadd(jadd({(0, 0): eye(4)}, jscale(dx, -1)), jmul(dx, dx)),
              {(0, 0): e0i})
    require(jequal(jmul(ee, ei), {(0, 0): eye(4)}), "actual inverse coframe second jet")
    tt = [[Q(1), Q(F(1, 2)), Q(), Q()], [Q(1), Q(F(-1, 2)), Q(), Q()],
          [Q(), Q(), Q(1), Q()], [Q(), Q(), Q(), Q(1)]]
    ti = [[Q(F(1, 2)), Q(F(1, 2)), Q(), Q()], [Q(1), Q(-1), Q(), Q()],
          [Q(), Q(), Q(1), Q()], [Q(), Q(), Q(), Q(1)]]
    eta = eye(4)
    for i in range(1, 4):
        eta[i][i] = Q(-1)
    s, rho, srho, h = P**4, Q(F(9, 4)), Q(F(3, 2)), Q(F(1, 8))
    vv = jscale(jmul({(0, 0): eta}, jtrans(jmul(ei, {(0, 0): ti}))), s*srho)
    rr = jmul(jmul(jtrans(vv), {(0, 0): eta}), {(0, 0): tt})
    zz = jscale(ext2(rr), 1/(s*s*rho))
    require(jequal(zz, ext2(ei)), "actual normalized compound dictionary, no sqrt-rho coefficient")
    n0 = add(zz[(0, 0)], scale(eye(6), -1))
    require(equal(mul(n0, n0), zero(6)), "primary compound square-zero")
    want = ext2(ee)
    p5, p3 = polynomial_inverse(zz, 5), polynomial_inverse(zz, 3)
    require(jequal(p5, want), "P5 complete mixed second jet in dense arbitrary directions")
    require(jequal(p3, want, KEYS[:3]), "P3 complete first jet fixture")
    require(not jequal(p3, want), "P3 must not be claimed a Hessian match")
    raw = jscale(jmul({(0, 0): tt}, ee), 1/(s*srho))
    actual_area_source = jscale(ext2(raw), 1/(h*h))
    compiled_area_source = jscale(jmul(ext2({(0, 0): tt}), p5), 1/(s*s*rho*h*h))
    require(jequal(actual_area_source, compiled_area_source),
            "finite edge h squared and density/calibration source prefactor")
    metric_from_v = jscale(jmul(jmul(jtrans(vv), {(0, 0): eta}), vv), 1/rho)
    metric_direct = jscale(jmul(jmul(jmul(ei, {(0, 0): ti}),
                                     {(0, 0): eta}), jtrans(jmul(ei, {(0, 0): ti}))), s*s)
    require(jequal(metric_from_v, metric_direct), "q inverse metric and PF factor")
    # This combinatorial proof certificate covers every ambient insertion,
    # not merely the preceding dense fixture.
    for r in (1, 2):
        power = 2*r+2
        for order in range(r+1):
            for inserted in itertools.combinations(range(power), order):
                longest = run = 0
                for pos in range(power):
                    run = 0 if pos in inserted else run+1
                    longest = max(longest, run)
                require(longest >= 2, "all noncommutative remainder derivative words vanish")
    return {"P5_mixed_second_jet_exact": True, "P3_second_jet_negative_control": True,
            "source_prefactor": "h^-2/(s^2*rho)", "arbitrary_ambient_proof": "remainder run certificate"}


def pa(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Q())+v
    return {k: v for k, v in out.items() if v}


def ps(a, c):
    return {k: v*c for k, v in a.items() if v*c}


def pm(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            kk = (ka[0]+kb[0], ka[1]+kb[1])
            if sum(kk) <= 2:
                out[kk] = out.get(kk, Q())+va*vb
    return {k: v for k, v in out.items() if v}


ONE = {(0, 0): Q(1)}


def expected_table(table, means):
    out = {}
    for signs, value in table.items():
        prob = ONE
        for sign, mean in zip(signs, means):
            prob = pm(prob, ps(pa(ONE, ps(mean, sign)), F(1, 2)))
        out = pa(out, ps(prob, value))
    return out


def herald_partition(weights):
    den = math.lcm(*(v.a.denominator for v in weights), *(v.b.denominator for v in weights))
    ab = [(int((v*den).a), int((v*den).b)) for v in weights]
    n = 0
    while any(a < 0 or b < 0 for a, b in ab):
        ab = [(a+b, a) for a, b in ab]
        n += 1
        require(n < 100000, "finite positive-cone fixture termination")
    count = sum(a+b for a, b in ab)
    k = (count-1).bit_length()
    for w, (a, b) in zip(weights, ab):
        require(Q(a)*P**n+Q(b)*P**(n+1) == den*w, "exact positive Golden representation")
    success = sum(Q(a)*P**n+Q(b)*P**(n+1) for a, b in ab)/2**k
    require(success == F(den, 2**k) and success.sign() > 0 and (1-success).sign() >= 0,
            "actual total herald probability")
    return {"D": den, "n": n, "k": k, "success": success.text()}


def report_control():
    tau, z = P**2/4096, Q(F(1, 2**20))
    lf, lq, gg = Q(7), Q(11), Q(F(3, 2))
    df, dq = tau*lf/gg, tau*lq/gg
    f, q = {(1, 0): Q(1)}, {(0, 1): Q(1)}
    # A3(x)=(3x-x^3)/2; the cubic has zero complete second jet at zero.
    mf, mq = ps(f, gg/lf), ps(q, gg/lq)
    elltab = {xi: 4*P**2*(1+df*xi[0])*(1-P**2*(1+df*xi[1]))
              for xi in itertools.product((-1, 1), repeat=2)}
    qtab = {xi: 4*(P-P**2*dq*xi[0])*(P-P**2*dq*xi[1]) *
            (1-(P-P**2*dq*xi[2])*(P-P**2*dq*xi[3]))
            for xi in itertools.product((-1, 1), repeat=4)}
    for val in list(elltab.values())+list(qtab.values()):
        require(val.sign() > 0 and (1-val).sign() > 0, "strict actual constant probability")
    require((1-4*P**2*F(65, 64)*(1-P**2*F(63, 64))).sign() > 0,
            "universal ell upper bound")
    lo, hi = P-P**2/64, P+P**2/64
    require(lo.sign() > 0 and (1-hi*hi).sign() > 0 and
            (1-4*hi*hi*(1-lo*lo)).sign() > 0, "universal B table bounds")
    ell, bb = expected_table(elltab, [mf, mf]), expected_table(qtab, [mq]*4)
    ee = ps(pa(ONE, ps(f, tau)), P**2)
    b0 = pm(pa({(0, 0): P}, ps(q, -P**2*tau)),
            pa({(0, 0): P}, ps(q, -P**2*tau)))
    target_ell = ps(pm(ee, pa(ONE, ps(ee, -1))), 4)
    target_b = ps(pm(b0, pa(ONE, ps(b0, -1))), 4)
    require(ell == target_ell and bb == target_b, "positive ordered tables retain the original full2jet")
    aa = pa(ell, pm(pa(ONE, ps(ell, -1)), bb))
    rr = pa(ONE, ps(pm(pa(ONE, ps(aa, -z)), pa(ONE, ps(bb, -z))), -1))
    ll, mm = 4*P**3, 4*P**3*(1+P**6)
    qq, rrr = 1-z*ll, 1-z*mm
    require(rr[(0, 0)] == 1-qq*rrr, "original report baseline")
    require(rr[(1, 0)] == z*tau*4*qq*P**11, "original geometric source coefficient")
    require(rr[(0, 1)] == -8*z*tau*P**6*(rrr+qq*P**6),
            "both original material source contributions")
    heralds = [herald_partition([v, 1-v]) for v in list(elltab.values())+list(qtab.values())]
    non_dyadic = herald_partition([Q(F(1, 3)), Q(F(2, 3))])
    # Exact low Taylor coefficients of majority; analytic proof covers all odd N.
    majority = []
    for n in (3, 9):
        m = (n-1)//2
        coefficients = [F(0)]*3
        for k in range(m+1, n+1):
            for i in range(3):
                coeff = sum(F(math.comb(k, a)*math.comb(n-k, i-a)*(-1)**(i-a))
                            for a in range(i+1) if a <= k and i-a <= n-k)
                coefficients[i] += F(2*math.comb(n, k), 2**n)*coeff
        coefficients[0] -= 1
        g = F(n*math.comb(2*m, m), 4**m)
        require(coefficients == [F(0), g, F(0)], "odd majority calibrated second jet")
        require(g*g >= m, "explicit majority growth control")
        majority.append({"N": n, "g": str(g)})
    return {"all_20_table_rows_exact_positive": True, "all_table_heralds_reconstructed": len(heralds),
            "non_dyadic_herald": non_dyadic, "report_two_jet_exact": True,
            "majority_controls": majority, "material_sign": -1}


def actual_reference_control(repo, pinned_path):
    import numpy as np
    source = (repo/pinned_path).read_text()
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "reference_characters")
    namespace = {"math": math, "itertools": itertools, "np": np, "require": require}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(repo/pinned_path), "exec"), namespace)
    size, sites = 8, 4096
    indices = np.array(list(itertools.product(range(size), repeat=4)))
    ff = namespace["reference_characters"](size, indices)
    chi = ff/math.sqrt(128)
    require(ff.shape == (4096, 128), "literal full4096 by128 original Fourier dictionary")
    leverage_error = float(np.max(np.abs(np.sum(chi*chi, axis=1)-1/sites)))
    require(leverage_error < 2e-17, "actual constant local reference norm")
    pp = (math.sqrt(5)-1)/2
    chosen = [(0, .02, -.03), (1, -.01, .025)]
    mus = []
    for idx, scalar, top in chosen:
        state = np.zeros(16)
        state[1], state[0], state[15] = math.sqrt(pp), scalar, top
        state[14] = math.sqrt(1-pp-scalar*scalar-top*top)
        complete_local = np.outer(state, chi[idx])
        observed = [float(2*np.dot(complete_local[1], complete_local[a])) for a in (0, 15)]
        target = [2*math.sqrt(pp)*v/sites for v in (scalar, top)]
        require(max(abs(a-b) for a, b in zip(observed, target)) < 2e-20,
                "actual same-site LEFT clock reference with RIGHT128 spectator")
        mus.append(observed)
    reconstructed = sites**2*mus[0][0]*mus[1][0]/(4*pp)
    require(abs(reconstructed-(.02)*(-.01)) < 2e-18, "two actual material copies, no cross-reference inverse")
    return {"reference_shape": [4096, 128], "source_function_ast_only": "reference_characters",
            "local_diagonal_error": leverage_error, "actual_first64_order_retained": True,
            "new_root_or_full42_numeric_scan": False, "scope": "exact reference owner; numerical local clock fixture"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    pins = json.loads((here/"SOURCE_PINS.json").read_text())
    for item in pins["sources"]:
        data = (args.repo/item["path"]).read_bytes()
        require(hashlib.sha256(data).hexdigest() == item["sha256"], "source pin: "+item["path"])
    result = {
        "status": "PASS",
        "input_source_ref": pins["source_ref"],
        "source_count": len(pins["sources"]),
        "source_pins_sha256": hashlib.sha256((here/"SOURCE_PINS.json").read_bytes()).hexdigest(),
        "proof_sha256": hashlib.sha256((here/"NATIVE_POLYNOMIAL_FIRST_JET.md").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "car": car_control(),
        "coframe": coframe_control(),
        "report": report_control(),
        "material": actual_reference_control(args.repo, pins["primary_dictionary"]),
        "scope": {
            "exact_primary_ambient_two_jet": "proved analytically",
            "coherent_original_moving_Julia_access": "input",
            "actual_independent_material_copies": "input",
            "native_field_writer_or_compulsory_price_selected": False,
            "source_neutral_upstream_price": "conditional, never inferred from report"
        }
    }
    destination = args.output or here/"CHECK_RESULT.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
