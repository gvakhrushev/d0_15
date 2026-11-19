#!/usr/bin/env python3
"""Bounded exact controls; no old suites, floating point, or external packages."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess


CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def zero(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    a = zero(n, n)
    for j in range(n):
        a[j][j] = F(1)
    return a


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in tr(b)] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, q):
    return [[q * x for x in row] for row in a]


def trace(a):
    return sum((a[j][j] for j in range(len(a))), F(0))


def inverse(a):
    n = len(a)
    b = [list(row) + erow for row, erow in zip(a, eye(n))]
    for j in range(n):
        k = next(k for k in range(j, n) if b[k][j])
        b[j], b[k] = b[k], b[j]
        q = b[j][j]
        b[j] = [x / q for x in b[j]]
        for k in range(n):
            if k != j:
                q = b[k][j]
                b[k] = [x - q * y for x, y in zip(b[k], b[j])]
    return [row[n:] for row in b]


def determinant(a):
    b = [list(row) for row in a]
    ans = F(1)
    for j in range(len(b)):
        ks = [k for k in range(j, len(b)) if b[k][j]]
        if not ks:
            return F(0)
        k = ks[0]
        if k != j:
            b[k], b[j] = b[j], b[k]
            ans = -ans
        q = b[j][j]
        ans *= q
        for k in range(j + 1, len(b)):
            s = b[k][j] / q
            b[k] = [x - s * y for x, y in zip(b[k], b[j])]
    return ans


def projector(t):
    return mm(mm(t, inverse(mm(tr(t), t))), tr(t))


def dprojector(t, dt):
    ni = inverse(mm(tr(t), t))
    dn = add(mm(tr(dt), t), mm(tr(t), dt))
    first = add(mm(mm(dt, ni), tr(t)), mm(mm(t, ni), tr(dt)))
    return add(first, scale(mm(mm(mm(mm(t, ni), dn), ni), tr(t)), F(-1)))


def sparse_inner(a, b):
    return sum((v * b.get(k, F(0)) for k, v in a.items()), F(0))


def sparse_gram(a, b):
    return [[sparse_inner(x, y) for y in b] for x in a]


def bell_columns(s):
    """Apply CNOT D->P, tensor H on D, then copy Q,D,P to record M.

    Iraw / sqrt(A*d) is the initialized-input embedding.
    Vraw / (d*sqrt(A)) is the complete output isometry.
    The sparse basis is the retained physical tuple (D,Q,P,B,M).
    """
    addresses, d = len(s), len(s[0])
    icols, vcols = [], []
    for j in range(d):
        inp, out = {}, {}
        for a in range(addresses):
            for i in range(d):
                for b in range(d):
                    x = s[a][b][i]
                    if not x:
                        continue
                    inp[(j, a, i, b, 0)] = x
                    u = j ^ i
                    for v in range(d):
                        sign = F(-1 if (v & j).bit_count() % 2 else 1)
                        label = a * d * d + v * d + u
                        key = (v, a, u, b, label)
                        out[key] = out.get(key, F(0)) + sign * x
        icols.append(inp)
        vcols.append(out)
    return icols, vcols


def rotation(d):
    q = eye(d)
    q[0][0], q[0][1] = F(3, 5), F(-4, 5)
    q[1][0], q[1][1] = F(4, 5), F(3, 5)
    return q


def bell_controls():
    answer = {}
    z, r = F(1, 2 ** 20), F(128)
    for d in (2, 4):
        addresses, den = 2, 4 * d ** 3
        p0 = zero(d, d)
        p0[0][0] = F(1)
        j0, j1 = rotation(d), eye(d)
        for case in ("unitary", "nonunitary"):
            s = [j0, j1]
            if case == "nonunitary":
                d0, d1 = eye(d), eye(d)
                d0[0][0], d0[1][1] = F(7, 5), F(1, 5)
                d1[0][0], d1[1][1] = F(1, 5), F(7, 5)
                s = [mm(mm(j0, d0), rotation(d)),
                     mm(mm(j1, d1), rotation(d))]
            ic, vc = bell_columns(s)
            tag = f"bell_d{d}_{case}"
            require(tag + "_input_normalization",
                    sparse_gram(ic, ic) == scale(eye(d), F(addresses * d)))
            require(tag + "_complete_isometry",
                    sparse_gram(vc, vc) == scale(eye(d), F(addresses * d * d)))
            c = sparse_gram(ic, vc)
            g0 = mm(tr(s[0]), s[0])
            require(tag + "_physical_corner", c == mm(p0, g0))
            gram = scale(mm(tr(c), c), F(1, den))
            lam = mm(g0, g0)[0][0] / den
            q = add(scale(eye(d), 1 - z), scale(gram, z))
            require(tag + "_rank_one_determinant",
                    determinant(q) == (1 - z) ** (d - 1) * (1 - z + z * lam))
            if case != "unitary":
                continue
            ds = [scale(mm(j0, p0), F(1, 2)),
                  scale(mm(j1, p0), F(-1, 2))]
            di, dv = bell_columns(ds)
            dc = add(sparse_gram(di, vc), sparse_gram(ic, dv))
            require(tag + "_compensated_normal_input",
                    add(sparse_gram(di, ic), sparse_gram(ic, di)) == zero(d, d))
            require(tag + "_compensated_normal_corner", dc == p0)
            dg = scale(add(mm(tr(dc), c), mm(tr(c), dc)), F(1, den))
            source = -r * z * trace(mm(inverse(q), dg))
            expected = -2 * r * z / (den * (1 - z + z / den))
            require(tag + "_normal_source", source == expected and source < 0)
            skew = zero(d, d)
            skew[0][1], skew[1][0] = F(1), F(-1)
            di, dv = bell_columns([mm(j0, skew), zero(d, d)])
            cut, operation = sparse_gram(di, vc), sparse_gram(ic, dv)
            require(tag + "_moving_cut_is_essential",
                    cut != zero(d, d) and operation != zero(d, d)
                    and add(cut, operation) == zero(d, d))
            answer[f"d{d}_normal_DJ"] = str(source)
    return answer


def writer_controls():
    t = [[F(1), F(0)], [F(0), F(1)], [F(1, 2), F(1, 3)]]
    dt = [[F(0), F(1, 5)], [F(-1, 7), F(0)], [F(1, 11), F(-1, 13)]]
    v = [[F(3, 5), F(0), F(0)], [F(4, 5), F(0), F(0)],
         [F(0), F(1), F(0)], [F(0), F(0), F(1)]]
    active = [[F(1), F(0)], [F(0), F(0)], [F(0), F(1)], [F(0), F(0)]]
    z, r = F(1, 7), F(3)
    w, dw = mm(v, t), mm(v, dt)
    require("writer_complete_isometry", mm(tr(v), v) == eye(3))
    require("writer_range_pullback", projector(w) == mm(mm(v, projector(t)), tr(v)))
    dp = dprojector(t, dt)
    require("writer_range_jet_pullback", dprojector(w, dw) == mm(mm(v, dp), tr(v)))
    n, dn = mm(tr(t), t), add(mm(tr(dt), t), mm(tr(t), dt))
    a, da = mm(tr(active), w), mm(tr(active), dw)
    g, dg = mm(tr(a), a), add(mm(tr(da), a), mm(tr(a), da))
    qraw = add(scale(n, 1 - z), scale(g, z))
    dqraw = add(scale(dn, 1 - z), scale(dg, z))
    qgeo = add(scale(eye(2), 1 - z), scale(mm(mm(tr(active), projector(w)), active), z))
    source_raw = r * (trace(mm(inverse(n), dn)) - trace(mm(inverse(qraw), dqraw)))
    source_geo = -r * z * trace(mm(inverse(qgeo), mm(mm(tr(active), dprojector(w, dw)), active)))
    require("writer_actual_normalizer_determinant", determinant(qraw) / determinant(n) == determinant(qgeo))
    require("writer_actual_normalizer_source", source_raw == source_geo and source_geo != 0)
    l = [[F(2), F(1, 3)], [F(0), F(1, 2)]]
    require("writer_invertible_input_coordinates", projector(mm(t, l)) == projector(t))
    x = [[F(1, 5), F(-1, 7)], [F(1, 11), F(1, 13)]]
    require("writer_vertical_jet_vanishes", dprojector(t, mm(t, x)) == zero(3, 3))
    return {"DJ_raw_equals_DJ_range": str(source_geo)}


def cost_controls():
    x = F(1, 2)
    swap = [[F(0), F(1)], [F(1), F(0)]]
    v = scale(eye(2), F(3, 5) * x) + scale(swap, F(4, 5) * x * x)
    dv = scale(eye(2), F(3, 5)) + scale(swap, F(8, 5) * x)
    n = F(9, 25) * x * x + F(16, 25) * x ** 4
    require("cost_full_mark_scalar", mm(tr(v), v) == scale(eye(2), n))
    effects = [scale(eye(2), F(9, 25)), scale(mm(tr(swap), swap), F(16, 25))]
    for k in range(5):
        actual = add(scale(effects[0], F(2 ** k)), scale(effects[1], F(4 ** k)))
        moment = F(9, 25) * 2 ** k + F(16, 25) * 4 ** k
        require(f"cost_moment_{k}_scalar", actual == scale(eye(2), moment))
    active = eye(2) + zero(2, 2)
    overlap = mm(mm(tr(active), projector(v)), active)
    doverlap = mm(mm(tr(active), dprojector(v, dv)), active)
    p0 = F(9, 1) / (9 + 16 * x * x)
    dp0 = -288 * x / (9 + 16 * x * x) ** 2
    require("cost_marked_range_not_constant",
            overlap == scale(eye(2), p0) and doverlap == scale(eye(2), dp0) and dp0 != 0)
    return {"mark_n": str(n), "factory_zero_overlap": str(p0), "D_x_overlap": str(dp0)}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def find_repo(given):
    if given:
        return Path(given).resolve()
    here = Path(__file__).resolve()
    for p in [Path.cwd(), *here.parents]:
        for candidate in (p, p / "d0_15"):
            if (candidate / ".git").exists():
                return candidate
    raise RuntimeError("Pass --repo /path/to/d0_15")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    pins_bytes = (here / "SOURCE_PINS.json").read_bytes()
    pins = json.loads(pins_bytes)
    repo = find_repo(args.repo)
    for item in pins["sources"]:
        content = subprocess.check_output(["git", "show", pins["source_ref"] + ":" + item["path"]], cwd=repo)
        require("historical_pin:" + item["path"], digest(content) == item["sha256"])
    result = {"status": "PASS", "source_ref": pins["source_ref"],
              "scope": "Exact small algebra fixtures; not an engine or physical-writer replay",
              "bell": bell_controls(), "writer": writer_controls(), "cost": cost_controls(),
              "proof_sha256": digest((here / "FIXED_PROCESSOR_BOOK_OPERATOR.md").read_bytes()),
              "checker_sha256": digest(Path(__file__).read_bytes()),
              "pins_sha256": digest(pins_bytes), "checks": CHECKS, "check_count": len(CHECKS)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
