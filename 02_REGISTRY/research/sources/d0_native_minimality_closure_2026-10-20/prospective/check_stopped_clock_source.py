#!/usr/bin/env python3
"""Exact bounded composition check; standard library only, read-only by default."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from math import comb, sqrt
from pathlib import Path
import time


@dataclass(frozen=True)
class Golden:
    """Q[p]/(p^2+p-1), on the positive real Golden embedding."""
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    @staticmethod
    def of(x):
        return x if isinstance(x, Golden) else Golden(Fraction(x))

    def __add__(self, other):
        if isinstance(other, Jet):
            return NotImplemented
        other = Golden.of(other)
        return Golden(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Golden(-self.a, -self.b)

    def __sub__(self, other):
        if isinstance(other, Jet):
            return NotImplemented
        return self + (-Golden.of(other))

    def __rsub__(self, other):
        return Golden.of(other) - self

    def __mul__(self, other):
        if isinstance(other, Jet):
            return NotImplemented
        other = Golden.of(other)
        return Golden(
            self.a * other.a + self.b * other.b,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    __rmul__ = __mul__

    def inverse(self):
        denominator = self.a * self.a - self.a * self.b - self.b * self.b
        if denominator == 0:
            raise ZeroDivisionError("zero Golden element")
        return Golden((self.a - self.b) / denominator, -self.b / denominator)

    def __truediv__(self, other):
        if isinstance(other, Jet):
            return NotImplemented
        return self * Golden.of(other).inverse()

    def __rtruediv__(self, other):
        return Golden.of(other) / self

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        out = Golden.of(1)
        factor = self
        while n:
            if n & 1:
                out *= factor
            factor *= factor
            n //= 2
        return out

    def is_zero(self):
        return self.a == 0 and self.b == 0

    def real(self):
        return float(self.a) + float(self.b) * (sqrt(5) - 1) / 2

    def exact(self):
        return {"rational": str(self.a), "p_coefficient": str(self.b)}


@dataclass(frozen=True)
class Jet:
    """Exact first jet; arithmetic differentiates products and inverses."""
    v: Golden = Golden()
    d: Golden = Golden()

    @staticmethod
    def of(x):
        return x if isinstance(x, Jet) else Jet(Golden.of(x))

    def __add__(self, other):
        other = Jet.of(other)
        return Jet(self.v + other.v, self.d + other.d)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, -self.d)

    def __sub__(self, other):
        return self + (-Jet.of(other))

    def __rsub__(self, other):
        return Jet.of(other) - self

    def __mul__(self, other):
        other = Jet.of(other)
        return Jet(self.v * other.v, self.d * other.v + self.v * other.d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Jet.of(other)
        return Jet(self.v / other.v,
                   self.d / other.v - self.v * other.d / (other.v ** 2))

    def __rtruediv__(self, other):
        return Jet.of(other) / self

    def __pow__(self, n):
        if n < 0:
            return (Jet.of(1) / self) ** (-n)
        out = Jet.of(1)
        for _ in range(n):
            out *= self
        return out


def zeros(n=3):
    return [[Jet.of(0) for _ in range(n)] for _ in range(n)]


def diagonal(values):
    out = zeros(len(values))
    for i, x in enumerate(values):
        out[i][i] = Jet.of(x)
    return out


def identity(n=3):
    return diagonal([1] * n)


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(s, a):
    return [[Jet.of(s) * x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n)), Jet.of(0))
             for j in range(n)] for i in range(n)]


def power(a, n):
    out = identity(len(a))
    for _ in range(n):
        out = mul(out, a)
    return out


def inverse(a):
    n = len(a)
    right = identity(n)
    aug = [list(row) + right[i] for i, row in enumerate(a)]
    for c in range(n):
        r = next(r for r in range(c, n) if not aug[r][c].v.is_zero())
        aug[c], aug[r] = aug[r], aug[c]
        pivot = aug[c][c]
        aug[c] = [x / pivot for x in aug[c]]
        for r in range(n):
            if r != c:
                factor = aug[r][c]
                aug[r] = [x - factor * y for x, y in zip(aug[r], aug[c])]
    return [row[n:] for row in aug]


def primal(a):
    return [[Jet(x.v) for x in row] for row in a]


def tangent(a):
    return [[Jet(x.d) for x in row] for row in a]


def combine_jet(value, derivative):
    return [[Jet(x.v, y.v) for x, y in zip(vr, dr)]
            for vr, dr in zip(value, derivative)]


def commutator(a, b):
    return sub(mul(a, b), mul(b, a))


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Jet.of(0))


def det3(a):
    return sum((a[0][j] * (
        a[1][(j + 1) % 3] * a[2][(j + 2) % 3]
        - a[1][(j + 2) % 3] * a[2][(j + 1) % 3]
    ) for j in range(3)), Jet.of(0))


def nonzero(a):
    return any(not x.v.is_zero() or not x.d.is_zero() for row in a for x in row)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    here = Path(__file__).resolve().parent
    start = time.monotonic()
    names = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        names.append(name)

    manifest = json.loads((here / "INPUTS.json").read_text())
    for entry in manifest["inputs"]:
        check("pin:" + entry["path"],
              sha(root / entry["path"]) == entry["sha256"])
    check("pin:proof", sha(here / "STOPPED_CLOCK_SOURCE.md") == manifest["proof_sha256"])

    p = Golden(Fraction(0), Fraction(1))
    check("exact Golden relation", p + p ** 2 == Golden.of(1))
    one = identity()
    b0 = diagonal([1, Fraction(3, 4), Fraction(1, 2)])
    rotation = [[Jet.of(x) for x in row] for row in [
        [0, Fraction(1, 3), Fraction(-1, 5)],
        [Fraction(-1, 3), 0, Fraction(1, 7)],
        [Fraction(1, 5), Fraction(-1, 7), 0],
    ]]
    db = add(commutator(rotation, b0),
             diagonal([0, Fraction(1, 7), Fraction(-1, 11)]))
    b = combine_jet(b0, db)
    q = mul(b, b)
    e = sub(one, q)
    epsilon = Jet(p ** 2 / 64, p ** 2 / 320)
    delta = scale(2 / epsilon, sub(one, b))
    e1 = scale(p * epsilon, delta)
    c = add(one, e1)
    x = Jet(Golden.of(Fraction(2, 3)), Golden.of(Fraction(1, 17)))
    s = Jet(Golden.of(Fraction(3, 5)), Golden.of(Fraction(1, 13)))
    g = add(scale(x, sub(e, e1)), scale(x ** 2, e1))
    check("owned cost substitution including epsilon jet",
          g == scale(x, add(e, scale(p * epsilon * (x - 1), delta))))
    check("noncommuting physical-source fixture", nonzero(commutator(primal(q), tangent(q))))
    check("positive nonblank port0 effects in generic fixture",
          all((e[i][i].v - e1[i][i].v).real() >= -1e-14 for i in range(3)))

    rx = inverse(sub(one, scale(x, q)))
    f = mul(g, rx)
    expected_df = add(
        mul(tangent(g), primal(rx)),
        mul(mul(mul(primal(g), primal(rx)),
                add(scale(x.d, primal(q)), scale(x.v, tangent(q)))), primal(rx)),
    )
    check("full noncommuting cost first jet", tangent(f) == expected_df)
    check("terminal port1 price cannot be replaced by clock alone",
          f != mul(scale(x, e), rx))

    n = 4
    exit_leaves = zeros()
    complete_moment = zeros()
    for j in range(n):
        bj = power(b, j)
        exit_leaves = add(exit_leaves, scale(x ** j, mul(mul(bj, g), bj)))
        local_leaf_moment = add(scale(j + 1, e), e1)
        complete_moment = add(complete_moment, mul(mul(bj, local_leaf_moment), bj))
    xnqn = power(scale(x, q), n)
    check("finite complete-exit transform and all jets",
          exit_leaves == mul(f, sub(one, xnqn)))
    complete = add(exit_leaves, xnqn)
    check("finite capped cost transform keeps unresolved branch",
          complete == add(f, mul(sub(one, f), xnqn)))
    check("exact exit-tail residual and source",
          sub(f, exit_leaves) == mul(f, xnqn))
    complete_moment = add(complete_moment, scale(n, power(q, n)))
    occupation = zeros()
    for j in range(n):
        occupation = add(occupation, mul(mul(power(b, j), c), power(b, j)))
    check("leaf prices equal occupation cost including all field jets",
          complete_moment == occupation)
    xmoment = Jet(Golden.of(1), Golden.of(1))
    moment_from_marker = zeros()
    for j in range(n):
        local = add(scale(xmoment ** (j + 1), primal(sub(e, e1))),
                    scale(xmoment ** (j + 2), primal(e1)))
        moment_from_marker = add(moment_from_marker,
                                mul(mul(primal(power(b, j)), local),
                                    primal(power(b, j))))
    moment_from_marker = add(moment_from_marker,
                             scale(xmoment ** n, primal(power(q, n))))
    check("complete finite cap has normalization I", primal(moment_from_marker) == one)
    check("complete finite-cap mark derivative is actual cost",
          tangent(moment_from_marker) == primal(occupation))

    rs = inverse(sub(one, scale(s, q)))
    fs = mul(scale(s, e), rs)
    check("clock resolvent alternate form",
          fs == sub(one, scale(1 - s, rs)))
    reconstructed_q = scale(1 / s, mul(sub(scale(s, one), fs),
                                      inverse(sub(one, fs))))
    check("clock reconstructs whole Q including kernel and noncommuting jet",
          reconstructed_q == q)
    expected_ds = sub(
        scale(s.d, mul(primal(e), power(primal(rs), 2))),
        scale(s.v * (1 - s.v), mul(mul(primal(rs), tangent(q)), primal(rs))),
    )
    check("clock source with moving analysis parameter", tangent(fs) == expected_ds)
    fixed_s_jet = sub(tangent(fs),
                     scale(s.d, mul(primal(e), power(primal(rs), 2))))
    recovered_dq = scale(
        -1 / (s.v * (1 - s.v)),
        mul(mul(primal(sub(one, scale(s, q))), fixed_s_jet),
            primal(sub(one, scale(s, q)))),
    )
    check("universal ordered clock-source inverse", recovered_dq == tangent(q))
    wrongly_commuted = scale(
        -s.v * (1 - s.v), mul(power(primal(rs), 2), tangent(q)))
    check("scalar derivative shortcut rejected", fixed_s_jet != wrongly_commuted)

    p00 = diagonal([1, 0, 0])
    dp0 = commutator(rotation, p00)
    p0 = combine_jet(p00, dp0)
    support = sub(one, p0)
    check("moving support is a projector through first order",
          mul(support, support) == support)
    check("eventual projector itself has nonzero source", nonzero(tangent(support)))
    z = Golden.of(Fraction(2, 5))
    determinant = det3(sub(one, scale(z, support)))
    check("unmarked fixed-rank determinant including moving kernel",
          determinant == Jet((1 - z) ** 2))
    check("full oldRIGHT determinant multiplicity",
          (determinant ** 128) == Jet((1 - z) ** 256))
    rho = [[Jet.of(x) for x in row] for row in [
        [Fraction(1, 2), Fraction(1, 2), 0],
        [Fraction(1, 2), Fraction(1, 2), 0],
        [0, 0, 0],
    ]]
    check("prepared eventual-exit source need not vanish",
          not trace(mul(rho, support)).d.is_zero())
    b_alt = diagonal([1, Fraction(2, 3), Fraction(4, 5)])
    q_alt = mul(b_alt, b_alt)
    fs_alt = mul(scale(s.v, sub(one, q_alt)),
                 inverse(sub(one, scale(s.v, q_alt))))
    check("same support different spectrum has different retained-clock effect",
          primal(fs) != fs_alt)

    e_dagger0 = diagonal([0, Fraction(16, 7), Fraction(4, 3)])
    active_diagonal_derivative = diagonal([
        0, -(e[1][1].d) / (e[1][1].v ** 2),
        -(e[2][2].d) / (e[2][2].v ** 2),
    ])
    e_dagger = combine_jet(
        e_dagger0,
        add(commutator(rotation, e_dagger0), active_diagonal_derivative),
    )
    check("moving-kernel Moore-Penrose relation", mul(e, e_dagger) == support)
    pseudoinverse_source = add(
        scale(-1, mul(mul(e_dagger0, tangent(e)), e_dagger0)),
        add(mul(mul(power(e_dagger0, 2), tangent(e)), p00),
            mul(mul(p00, tangent(e)), power(e_dagger0, 2))),
    )
    check("all moving-kernel pseudoinverse source terms",
          tangent(e_dagger) == pseudoinverse_source)
    cplus = mul(c, e_dagger)
    check("whole-operator cap cost retains dark NP0 and source",
          occupation == add(scale(n, p0), mul(cplus, sub(one, power(q, n)))))
    check("dropping nonhalting clock charge rejected",
          occupation != mul(cplus, sub(one, power(q, n))))
    check("support-restricted paid source not erased by constant determinant",
          not trace(cplus).d.is_zero())
    check("fixed finite cap return/source differs from projector",
          sub(one, power(q, n)) != support)

    # Literal flat original four-dimensional periodic L=4 spectrum:
    # each direction has mu=0,2,2,4. All CAR16 grades are retained.
    level_multiplicities = [comb(8, k) for k in range(9)]
    check("flat grid contains all 4^4 Fourier modes", sum(level_multiplicities) == 4 ** 4)
    data_dimension = 16 * sum(level_multiplicities)
    rank = 16 * sum(level_multiplicities[1:])
    check("full CAR16 and oldRIGHT dimension", data_dimension * 128 == 524288)
    epsilon_flat = p ** 2 / (64 * 4 ** 2)
    rho_scale = Jet(Golden.of(1), Golden.of(1))
    mark = Golden.of(Fraction(3, 4))
    marked_trace = Jet.of(0)
    marked_cost_trace = Jet.of(0)
    paid_trace = Jet.of(0)
    for k, multiplicity in enumerate(level_multiplicities):
        lam = rho_scale * (2 * k)
        blank = 1 - epsilon_flat * lam / 2
        blank_probability = blank ** 2
        exit_effect = 1 - blank_probability
        port1 = p * epsilon_flat * lam
        clock_effect = mark * exit_effect / (1 - mark * blank_probability)
        cost_effect = mark * (exit_effect + (mark - 1) * port1) / (1 - mark * blank_probability)
        check(f"native flat mode {k} clock inverse",
              (mark - clock_effect) / (mark * (1 - clock_effect)) == blank_probability)
        check(f"native flat mode {k} positive window",
              0 < blank.v.real() <= 1 and
              (exit_effect.v - port1.v).real() >= -1e-13)
        marked_trace += (16 * 128 * multiplicity) * clock_effect
        marked_cost_trace += (16 * 128 * multiplicity) * cost_effect
        if k:
            price = (1 + port1) / exit_effect
            x1 = Jet(Golden.of(1), Golden.of(1))
            cost_effect_x = (
                x1 * (exit_effect.v + (x1 - 1) * port1.v)
                / (1 - x1 * blank_probability.v)
            )
            check(f"native flat mode {k} exact exit-cost moment",
                  cost_effect_x.d == price.v)
            paid_trace += (16 * 128 * multiplicity) * price
        else:
            check("native dark mode has zero finite-exit effect",
                  clock_effect == Jet.of(0) and cost_effect == Jet.of(0))
    check("native full-trace retained clock source is nonzero",
          not marked_trace.d.is_zero())
    check("native full-trace actual cost mark source is nonzero",
          not marked_cost_trace.d.is_zero())
    check("native full-support paid source is nonzero",
          not paid_trace.d.is_zero())
    check("native unlimited determinant has exact fixed-rank coefficient",
          rank * 128 == 522240)

    result = {
        "status": "PASS",
        "input_commit": manifest["input_commit"],
        "checks": len(names),
        "check_names": names,
        "proof_sha256": sha(here / "STOPPED_CLOCK_SOURCE.md"),
        "checker_sha256": sha(Path(__file__)),
        "inputs_sha256": sha(here / "INPUTS.json"),
        "scope": {
            "arithmetic": "exact Q[p]/(p^2+p-1), exact first jets",
            "native_input": "owned all128 one-step identities; no Kraus-suite replay",
            "noncommuting_fixture": "generic 3x3 algebra/source check, not a native-admission witness",
            "native_fixture": "original flat L=4, all 256 Fourier modes, all CAR16, oldRIGHT factor128",
            "attainment": "analytic earliest-stop lower bound for known port Cost only",
            "book_Info_or_compulsory_task_derived": False,
            "controlled_halt_admission_derived": False,
            "GR_closed": False,
        },
        "native_diagnostics": {
            "data_dimension": data_dimension,
            "oldRIGHT_dimension": 128,
            "positive_data_rank": rank,
            "full_unmarked_logdet_coefficient": rank * 128,
            "full_clock_mark_source": marked_trace.d.exact(),
            "full_port_cost_mark_source": marked_cost_trace.d.exact(),
            "full_stopped_paid_source": paid_trace.d.exact(),
        },
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "checks", "proof_sha256", "checker_sha256", "elapsed_seconds"
    )}, indent=2))


if __name__ == "__main__":
    main()
