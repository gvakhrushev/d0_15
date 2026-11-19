#!/usr/bin/env python3
"""Exact new Golden/CNOT cut diagnostic; no imported project test suites."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess


class Q:
    """Q[a]/(a^4+a^2-1), basis 1,a,a^2,a^3."""
    __slots__ = ("v",)

    def __init__(self, v=0):
        if isinstance(v, Q):
            self.v = v.v
        elif isinstance(v, (tuple, list)):
            self.v = tuple(F(x) for x in v)
            if len(self.v) != 4:
                raise ValueError("four coefficients required")
        else:
            self.v = (F(v), F(0), F(0), F(0))

    def __add__(self, other):
        other = Q(other)
        return Q(tuple(x+y for x, y in zip(self.v, other.v)))

    __radd__ = __add__

    def __neg__(self):
        return Q(tuple(-x for x in self.v))

    def __sub__(self, other):
        return self + (-Q(other))

    def __rsub__(self, other):
        return Q(other) + (-self)

    def __mul__(self, other):
        other = Q(other)
        cs = [F(0)] * 7
        for i, x in enumerate(self.v):
            if x:
                for j, y in enumerate(other.v):
                    if y:
                        cs[i+j] += x*y
        for k in range(6, 3, -1):
            cs[k-4] += cs[k]
            cs[k-2] -= cs[k]
        return Q(cs[:4])

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            raise ValueError("nonnegative powers only")
        out, base = Q(1), self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n //= 2
        return out

    def __eq__(self, other):
        return self.v == Q(other).v

    def __bool__(self):
        return any(self.v)

    def data(self):
        return [str(x) for x in self.v]


ZERO, ONE = Q(0), Q(1)
a, p = Q((0, 1, 0, 0)), Q((0, 0, 1, 0))
checks = []


def check(label, condition):
    # Deliberately independent of assert / Python optimization mode.
    if not condition:
        raise RuntimeError("FAIL: " + label)
    checks.append(label)


def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def tr(m):
    return [list(c) for c in zip(*m)]


def mm(x, y):
    yt = tr(y)
    return [[sum((u*v for u, v in zip(row, col) if u and v), ZERO)
             for col in yt] for row in x]


def madd(x, y):
    return [[u+v for u, v in zip(xr, yr)] for xr, yr in zip(x, y)]


def kron(x, y):
    return [[u*v for u in xr for v in yr] for xr in x for yr in y]


def gate(state, nq, spec):
    out = [ZERO] * len(state)
    if spec[0] == "G":
        mask = 1 << (nq-1-spec[1])
        for j in range(len(state)):
            if not j & mask:
                x, y = state[j], state[j | mask]
                out[j] = a*x-p*y
                out[j | mask] = p*x+a*y
    elif spec[0] == "CX":
        cm = 1 << (nq-1-spec[1])
        tm = 1 << (nq-1-spec[2])
        for j, x in enumerate(state):
            out[j ^ tm if j & cm else j] = x
    else:
        raise ValueError(spec)
    return out


def evolve(state, nq, word):
    for spec in word:
        state = gate(state, nq, spec)
    return state


def matrix(nq, word):
    n = 1 << nq
    return tr([evolve([ONE if i == j else ZERO for i in range(n)], nq, word)
               for j in range(n)])


def sub(m, rows, cols):
    return [[m[i][j] for j in cols] for i in rows]


def norm2(state):
    return sum((x*x for x in state), ZERO)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def find_repo(explicit, here):
    if explicit is not None:
        return explicit.resolve()
    for base in (Path.cwd(), *here.parents):
        for candidate in (base, base / "d0_15"):
            if (candidate / "01_BOOKS").is_dir() and (candidate / ".git").exists():
                return candidate.resolve()
    raise RuntimeError("pass --repo with the existing repository checkout")


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--output", type=Path, default=here / "RESULT.json")
    args = parser.parse_args()
    repo = find_repo(args.repo, here)
    manifest = json.loads((here / "SOURCE_PINS.json").read_text())
    for source in manifest["sources"]:
        blob = subprocess.check_output(
            ["git", "-C", str(repo), "show", manifest["commit"]+":"+source["path"]])
        check("historical source " + source["id"], sha(blob) == source["sha256"])

    check("Golden norm p+p^2=1", p+p*p == ONE)
    check("a^2=p", a*a == p)
    check("positive root bracket lower", F(8, 13)**2+F(8, 13)-1 == -F(1, 169))
    check("positive root bracket upper", F(41, 66)**2+F(41, 66)-1 == F(31, 4356))
    check("brackets imply strict entropy order",
          F(1, 2) < F(8, 13) < F(41, 66) < F(5, 8))
    r0, r1 = 41-65*p, p*p
    alpha = 2*p**3
    check("r0 direct Golden polynomial", (3*p*p-p**3)**2 == r0)
    check("r1 Golden probability", r1 == 1-p)
    check("distinct prepared reports", r0 != r1)
    check("real prefix readiness", alpha == 4*p-2)

    code = [
        [("CX", 1, 2), ("CX", 0, 1)],
        [("CX", 0, 1), ("CX", 1, 2)],
    ]
    report = [("G", 3), ("CX", 2, 3), ("G", 3), ("CX", 2, 3), ("G", 3)]
    full_code = [matrix(4, word) for word in code]
    vv = matrix(4, report)
    full = [matrix(4, word+report) for word in code]
    active = list(range(0, 16, 2))
    comp = list(range(1, 16, 2))
    id8, id16 = eye(8), eye(16)
    k0v, k1v = sub(vv, active, active), sub(vv, comp, active)
    fv = mm(tr(k1v), k1v)
    check("all 16 report columns orthogonal", mm(tr(vv), vv) == id16)
    check("full report effect spectrum",
          fv == [[(r1 if i & 1 else r0) if i == j else ZERO
                  for j in range(8)] for i in range(8)])
    prepared_input = 8  # c,u,b,R=1,0,0,0
    z = Q(F(1, 16))
    dets = []
    for k in range(2):
        check(f"code{k} full orthogonal columns", mm(tr(full_code[k]), full_code[k]) == id16)
        check(f"code{k} whole word orthogonal", mm(tr(full[k]), full[k]) == id16)
        check(f"code{k} actual chronological composition", full[k] == mm(vv, full_code[k]))
        ck = sub(full_code[k], active, active)
        check(f"code{k} preserves whole report cut", mm(tr(ck), ck) == id8)
        k0, k1 = sub(full[k], active, active), sub(full[k], comp, active)
        fk = mm(tr(k1), k1)
        check(f"code{k} all-branch completeness",
              madd(mm(tr(k0), k0), fk) == id8)
        check(f"code{k} exact right conjugacy", fk == mm(mm(tr(ck), fv), ck))
        check(f"code{k} diagonal full effect", all(not fk[i][j]
                                                  for i in range(8) for j in range(8)
                                                  if i != j))
        diag = [fk[i][i] for i in range(8)]
        check(f"code{k} both spectral multiplicities", diag.count(r0) == diag.count(r1) == 4)
        click = sum((full[k][j][prepared_input]**2 for j in comp), ZERO)
        check(f"code{k} actual prepared click", click == (r0 if k == 0 else r1))
        # Full diagonal determinant at a strict rational z, in the same exact field.
        det = ONE
        for x in diag:
            det = det * (1-z*x)
        dets.append(det)
        check(f"code{k} exact feedback factors",
              det == ((1-z*r0)*(1-z*r1))**4)
    check("same complete determinant", dets[0] == dets[1])
    check("selected-column determinants differ", 1-z*r0 != 1-z*r1)
    check("equal per-address code inventories", sorted(code[0]) == sorted(code[1]))
    check("seven gates in either ready block", all(len(c+report) == 7 for c in code))

    # Genuine common paid Golden prefix, six qubits A0,c,T,u,b,R.
    prefix = [("G", 0), ("G", 1), ("CX", 0, 2), ("CX", 1, 2), ("CX", 0, 1)]
    psi = evolve([ONE]+[ZERO]*63, 6, prefix)
    check("paid prefix norm", norm2(psi) == ONE)
    fail = [x if not j & 8 else ZERO for j, x in enumerate(psi)]
    ready = [x if j & 8 else ZERO for j, x in enumerate(psi)]
    check("all prefix failure retained", norm2(fail) == 1-alpha)
    check("actual ready probability", norm2(ready) == alpha)
    expected = [ZERO]*64
    expected[24] = a*p  # A0,c,T=0,1,1
    expected[56] = a*p  # A0,c,T=1,1,1
    check("actual known-one and pure plus byproduct", ready == expected)
    report6 = [("G", 5), ("CX", 4, 5), ("G", 5), ("CX", 4, 5), ("G", 5)]
    code6 = [
        [("CX", 3, 4), ("CX", 1, 3)],
        [("CX", 1, 3), ("CX", 3, 4)],
    ]
    qlaws = []
    for k in range(2):
        out = evolve(ready, 6, code6[k]+report6)
        probs = [norm2(fail),
                 sum((x*x for j, x in enumerate(out) if not j & 1), ZERO),
                 sum((x*x for j, x in enumerate(out) if j & 1), ZERO)]
        rk = (r0, r1)[k]
        check(f"full prefix code{k} complete law", probs == [1-alpha, alpha*(1-rk), alpha*rk])
        check(f"full prefix code{k} total probability", sum(probs, ZERO) == ONE)
        check(f"full prefix code{k} untouched u=1", all(not x for j, x in enumerate(out) if not j & 4))
        check(f"full prefix code{k} retained code", all(not x for j, x in enumerate(out)
                                                      if bool(j & 2) != bool(k)))
        qlaws.append([q.data() for q in probs])
    check("actual whole entropy contrast has nonzero readiness", alpha != ZERO)

    # Conditional spectator-cut criterion and its initialized-cut countercontrol.
    p0 = [[ONE, ZERO], [ZERO, ZERO]]
    xx = [[ZERO, ONE], [ONE, ZERO]]
    zz = [[ONE, ZERO], [ZERO, -ONE]]
    stable, initialized = kron(p0, eye(2)), kron(p0, p0)
    wx, wz = kron(eye(2), xx), kron(eye(2), zz)
    check("stable cut commutes X", mm(stable, wx) == mm(wx, stable))
    check("stable cut commutes Z", mm(stable, wz) == mm(wz, stable))
    check("stable cut blank compression", sub(stable, [0, 2], [0, 2]) == p0)
    check("initialized cut same blank compression", sub(initialized, [0, 2], [0, 2]) == p0)
    check("initialized cut fails X covariance", mm(initialized, wx) != mm(wx, initialized))

    proof = here / "RETAINED_CUT_AND_PREPARED_SOURCE.md"
    result = {
        "status": "PASS",
        "scientific_input": manifest["commit"],
        "arithmetic": "Q[a]/(a^4+a^2-1), exact Fraction coefficients",
        "proof_sha256": sha(proof.read_bytes()),
        "checker_sha256": sha(Path(__file__).read_bytes()),
        "source_pins_sha256": sha((here / "SOURCE_PINS.json").read_bytes()),
        "checks": len(checks),
        "labels": checks,
        "exact_values_basis_1_a_p_ap": {
            "r0": r0.data(), "r1": r1.data(), "alpha": alpha.data(),
            "full_q0": qlaws[0], "full_q1": qlaws[1],
            "full_det_z_1_over_16": dets[0].data(),
        },
        "scope": [
            "Actual full16 Golden/CNOT block and same report cut rank8",
            "Genuine six-qubit paid prefix, all failure and final report probabilities",
            "No claimed full-prefix Book factorization, native cut selection or heat/Info binding",
            "No imported old suite or numerical source extrapolation",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n")
    print(f"PASS {len(checks)} exact checks; {args.output}")


if __name__ == "__main__":
    main()
