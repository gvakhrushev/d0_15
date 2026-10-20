#!/usr/bin/env python3
"""Narrow exact controls for PROSPECTIVE_FIELD_REALIZATION_BRIDGE.md.

No old geometry, compiler search, policy scan, or scientific source mutation.
Analytical quantifiers in the proof are not replaced by these finite controls.
All checks remain active under Python -O. Standard library only.
"""

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


PINS = {
    "03_FORMALIZATION/D0/Foundation/ProspectiveExecution.lean": "99db926c47864c53ecf8d43caf2518f86b96e42cdffccaaf26f6c93205155ed4",
    "03_FORMALIZATION/D0/Foundation/FutureExecution.lean": "15143b63f2bf1cc51493e3efb36c9da57c203d7e680e2f1370cf2311eb2e9ef1",
    "03_FORMALIZATION/D0/Foundation/FutureExecutionCompleteness.lean": "d202822470539f777e0f54df97d8bf9aaa983e032291195e9748036d7f00ec8c",
    "03_FORMALIZATION/D0/Foundation/VerifiabilityNecessity.lean": "e851960cf5ed7c3abdb488dc70a2ed098d9a6bfb2ca0a60d2cbecda9f93da48d",
    "02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md": "8dbca8ff9a4567a2baf216357b5d3ffa2d217281ced4e5d0e535257db2f5e83e",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md": "f6a5724e087c58b4294020a59532b7117f55247013181bcd4fd30d069a649330",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/history/NATIVE_TASK_SEARCH_4867.md": "59cbda439229c01fe38e181e68d136bc3e3006353e28a936f106de6187ed8d6e",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/records/ADAPTIVE_ALL_COST_EXTENSION.md": "34e491c6f7aa74a1f2fe7e3ba942bd784bcb6ac6e4306dd5c1c5a1e7b86a9274",
    "02_REGISTRY/research/A4D_GOLDEN_FULL_SOURCE_SELECTION_SYNTHESIS_2026_10_20.md": "99551de2dcc8ae84a165a80631090952907aa1b46873160b7a0b648e94bf85e1",
}


class Checks:
    def __init__(self):
        self.names = []

    def require(self, condition, name):
        if not condition:
            raise RuntimeError("FAILED: " + name)
        self.names.append(name)


class G:
    """Q[r]/(r^4+r^2-1), at the positive root r=sqrt(phi^-1)."""
    def __init__(self, value=0):
        if isinstance(value, G):
            self.c = value.c
        elif isinstance(value, (tuple, list)):
            if len(value) != 4:
                raise ValueError("Four reduced coefficients required")
            self.c = tuple(F(x) for x in value)
        else:
            self.c = (F(value), F(0), F(0), F(0))

    def __add__(self, other):
        other = G(other)
        return G(tuple(a + b for a, b in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return G(tuple(-a for a in self.c))

    def __sub__(self, other):
        return self + -G(other)

    def __rsub__(self, other):
        return G(other) + -self

    def __mul__(self, other):
        other = G(other)
        out = [F(0)] * 7
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                out[i + j] += a * b
        for degree in range(6, 3, -1):
            out[degree - 4] += out[degree]
            out[degree - 2] -= out[degree]
        return G(out[:4])

    __rmul__ = __mul__

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Nonnegative integer power required")
        out = G(1)
        for _ in range(n):
            out = out * self
        return out

    def __eq__(self, other):
        return self.c == G(other).c

    def interval(self, lo, hi):
        lower = upper = F(0)
        for degree, a in enumerate(self.c):
            x, y = lo ** degree, hi ** degree
            lower += a * (x if a >= 0 else y)
            upper += a * (y if a >= 0 else x)
        return lower, upper


def poly_add(a, b):
    out = [G(0)] * max(len(a), len(b))
    for i, v in enumerate(a):
        out[i] = out[i] + v
    for i, v in enumerate(b):
        out[i] = out[i] + v
    return out


def poly_scale(a, b):
    return [b * x for x in a]


def poly_mul(a, b):
    out = [G(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = out[i + j] + x * y
    return out


def poly_eval(a, t):
    value = G(0)
    for coefficient in reversed(a):
        value = value * t + coefficient
    return value


def run(repo):
    checks = Checks()
    for path, expected in sorted(PINS.items()):
        actual = hashlib.sha256((repo / path).read_bytes()).hexdigest()
        checks.require(actual == expected, "pin:" + path)
    prospective = (repo / "03_FORMALIZATION/D0/Foundation/ProspectiveExecution.lean").read_text()
    checks.require("optimal : ∀ alternative : List D.Action," in prospective,
                   "native optimal quantifies words of fixed Dynamics")
    checks.require("initial : D.State" in prospective and "goal : D.State → Prop" in prospective,
                   "initial and goal are separately supplied fields")

    # Read-only field coordinate, with complete clock and record retained.
    for field in (F(-1, 2), F(0), F(1, 3)):
        for word in ((), (0,), (1,), (0, 1, 0), (1, 1, 0, 1)):
            state = (field, 0, ())
            for action in word:
                y, clock, record = state
                state = (y, clock + 1, record + ((clock, action),))
            checks.require(state[0] == field and state[1] == len(word)
                           and len(state[2]) == len(word),
                           "read-only exact invariant:" + str(field) + ":" + str(word))

    # Same field image alone cannot replace complete prices.
    for q in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
        score, full = q, 1 + q * q
        residual = 1 + q * q - q
        checks.require(full >= 1 and residual > 0 and full == score + residual,
                       "omitted-ledger control:" + str(q))
    checks.require(F(1) + F(-1) == 0, "score source cancelled by actual ledger source")
    gradient, admitted_velocity = (F(1), F(-2)), (F(2), F(1))
    checks.require(sum(a * b for a, b in zip(gradient, admitted_velocity)) == 0
                   and gradient != (0, 0), "restricted tangent does not imply full source zero")
    for s in (F(1, 2), F(1, 4), F(1, 8)):
        r = -s * s
        score = s * r
        residual = s * s + r * r - score
        checks.require(score == -(s ** 3) and score < 0
                       and residual >= -score and score + residual >= 0,
                       "zero-first-jet ledger can stabilize a descending score:" + str(s))

    # Consume original all-40 formulas; do not reconstruct or rerun geometry.
    centre = (3, 3, 3)

    def chi(z):
        return F(int(tuple(z) == centre))

    def shift(z, axis, amount=1):
        out = list(z)
        out[axis] += amount
        return tuple(out)

    def delta_k(z, axis):
        future = shift(z, 0)
        return (chi(future) - chi(shift(future, axis, -1))) / 2

    sites = tuple(product(range(7), repeat=3))
    interior = tuple(product(range(1, 6), repeat=3))
    collar = tuple(z for z in sites if 0 in z or 6 in z)
    checks.require(all(chi(z) == 0 and delta_k(z, 1) == 0 and delta_k(z, 2) == 0
                       for z in collar), "chi and its staggered links vanish on fixed collars")
    checks.require(all(chi(z) == 0 and delta_k(z, 1) == 0 and delta_k(z, 2) == 0
                       for z in sites if z[0] == 0), "designated initial u slice unchanged")
    for axis in (1, 2):
        checks.require(all(delta_k(shift(z, 0, -1), axis)
                           == (chi(z) - chi(shift(z, axis, -1))) / 2
                           for z in interior), "original Cartan row preserved:axis" + str(axis))
    z0 = shift(centre, 0, -1)
    stencil_receipt = []
    for h in (F(1), F(1, 2), F(2, 3)):
        def full_row(z):
            return h * sum(delta_k(z, axis) - delta_k(shift(z, axis), axis)
                           for axis in (1, 2))

        def laplacian(z):
            return sum(chi(shift(z, axis)) + chi(shift(z, axis, -1)) - 2 * chi(z)
                       for axis in (1, 2)) / (h * h)

        checks.require(all(full_row(z) == -(h ** 3) * laplacian(shift(z, 0)) / 2
                           for z in interior), "original full coframe stencil:h" + str(h))
        checks.require(laplacian(centre) == -4 / (h * h), "unit spike Laplacian:h" + str(h))
        normalized = full_row(z0) / (h ** 4)
        checks.require(normalized == 2 / (h ** 3) and normalized != 0,
                       "nonzero normalized off-shell coframe source:h" + str(h))
        stencil_receipt.append({"h": str(h), "source_delta_per_C_h_s": str(normalized)})
    wrong_unstaggered = lambda z, axis: (chi(z) - chi(shift(z, axis, -1))) / 2
    checks.require(any(wrong_unstaggered(shift(z, 0, -1), axis)
                       != (chi(z) - chi(shift(z, axis, -1))) / 2
                       for z in interior for axis in (1, 2)),
                   "negative control: dropping native u stagger violates Cartan")

    # Exact Golden field and complete cleanup, with no floating-point values.
    r = G((0, 1, 0, 0))
    p = r * r
    checks.require(p + p * p == 1, "Golden identity")
    checks.require(r * (r + r ** 3) == 1, "exact positive-root inverse identity")
    c2, s2 = p - p * p, 2 * r ** 3
    checks.require(c2 == p ** 3 and c2 * c2 + s2 * s2 == 1, "actual G squared")
    q2, qp2 = s2 * s2, 4 * c2 * s2
    checks.require(q2 == 4 * p ** 3 and 1 - q2 == p ** 6, "exact k2 port law")
    checks.require(2 * r ** 3 * qp2 == q2 * q2,
                   "q2_prime/q2_squared equals 1/(2p^(3/2))")
    # log_phi((1-q2)/p)=log_phi(p^5)=-5, so T=5,k=2,ell=1 gives B=2.
    b2 = 5 + 2 - 5
    checks.require(b2 == 2 and b2 * qp2 * r ** 3 == q2 * q2,
                   "T5 source exactly -p^(-3/2)")
    checks.require(b2 * qp2 * r ** 3 != 2 * q2 * q2,
                   "negative control: erroneous extra factor two rejected")
    lo, hi = F(786151377757, 10 ** 12), F(786151377758, 10 ** 12)
    checks.require(lo > 0 and lo ** 4 + lo ** 2 - 1 < 0
                   and hi ** 4 + hi ** 2 - 1 > 0,
                   "exact rational bracket for positive Golden root")
    clean0, clean1 = [G(1), G(0), G(-2)], [G(0), G(2), G(0), G(-2)]
    dirty = [G(0), G(0), G(0), G(0), G(4), G(0), G(-4)]
    for k, c, s in ((1, r, p), (2, c2, s2)):
        alpha = poly_add(poly_scale(clean0, c), poly_scale(clean1, -s))
        beta = poly_add(poly_scale(clean0, s), poly_scale(clean1, c))
        q0 = poly_add(poly_mul(alpha, alpha), poly_scale(dirty, s * s))
        q1 = poly_add(poly_mul(beta, beta), poly_scale(dirty, c * c))
        total = poly_add(q0, q1)
        checks.require(total[0] == 1 and all(x == 0 for x in total[1:]),
                       "all-outcome polynomial normalization:k" + str(k))
        checks.require(q1[0] == s * s and q1[1] == 4 * c * s,
                       "full source at common-null:k" + str(k))
        for t in (F(-1, 1000), F(0), F(1, 1000)):
            checks.require(poly_eval(q0, t).interval(lo, hi)[0] > 0
                           and poly_eval(q1, t).interval(lo, hi)[0] > 0,
                           "both rotated outcomes possible across null:k" + str(k) + ":t" + str(t))
    checks.require(poly_eval(dirty, F(0)) == 0, "dirty certificate never fires on common-null")
    for t in (F(-1, 10), F(1, 10), F(1, 100)):
        mass = 4 * t ** 4 * (1 - t * t)
        checks.require(mass > 0 and mass < 4 * t ** 4 and 1 / mass > 1 / (4 * t ** 4),
                       "sound one-sided dirty certificate has divergent mean:" + str(t))

    return {
        "schema": "d0.prospective-field-realization-bridge.v1",
        "status": "PASS",
        "checks": len(checks.names),
        "arithmetic": "exact Fraction and Q[r]/(r^4+r^2-1); no floating point",
        "baseline": "63221d4f",
        "frozen_source_sha256": dict(sorted(PINS.items())),
        "controls": {
            "stencil_interior_sites": len(interior),
            "spike": list(centre),
            "source_site": list(z0),
            "normalized_source": stencil_receipt,
            "same_record_offshell_family": "f=q=t=0; native identity consumed, not geometry replayed",
            "golden_source_T5_ell1": "-p^(-3/2) dt; semantic-cost arithmetic control only",
            "general_cost_domain": "every finite fixed T>=5, ell>=1; all-cost minimizer theorem consumed",
        },
        "negative_controls": [
            "field reachability without complete-price fidelity",
            "restricted admitted tangent with nonzero full covector",
            "zero first ledger derivative does not identify a field minimum",
            "omitting the native one-u-step Cartan stagger",
            "historical erroneous factor two in the T5 source",
            "rotated Golden success bit is not a zero-error null certificate",
        ],
        "scope": [
            "price-graph realization and continuous-verification theorems proved analytically in companion",
            "no field-generation admission, future task, Info convention or compiler price is inferred",
            "no programme scan, geometry replay or proof of unrestricted field minimum",
            "all required checks are active under Python -O",
        ],
        "check_names": checks.names,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="Read-only pinned repository root")
    parser.add_argument("--output", type=Path, help="Optional JSON receipt destination")
    args = parser.parse_args()
    result = run(args.repo)
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(encoded)
        print(json.dumps({"status": result["status"], "checks": result["checks"]}, sort_keys=True))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
