#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Shared-link quadratic stationary completion of a slow interaction moment.

Two previously owned physical joint-circle modes are inputs. A direct mixed
jet of the literal action retains every factor and inverse incidence. The
connection forcing is removed exactly in its full 24-row output fibre.
The resulting metric response is nonzero. This is a quadratic jet, not an
exact nonlinear root or a fixed smooth-source theory counterexample.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json

import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

import a4d_identity_quarter_nonlinear_response_check as N
import a4d_identity_physical_resonance_circles_check as P


INPUT_HEAD = "135d6a74cc6318bb9c4bcca0c52f6203b19f8a3a"
QI = P.QI
II = QI(0, 1)
ZERO = (0, 0, 0, 0)
ETA = np.diag(N.SIG).astype(object)
T = sp.Symbol("t")


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def qpower(a, n):
    if n < 0:
        return qpower(QI.of(1) / a, -n)
    out = QI.of(1)
    for _ in range(n):
        out *= a
    return out


def clean(terms):
    return {k: v for k, v in terms.items() if np.any(v)}


def genmat(coords):
    return sum((g * c for g, c in zip(N.G, coords)),
               np.zeros((4, 4), dtype=object))


@dataclass
class Mode:
    bases: tuple
    powers: tuple
    # Laurent coefficients of the 24 right-log coordinates.
    vector: dict

    def phase(self, offset):
        base = QI.of(1)
        for z, n in zip(self.bases, offset):
            base *= qpower(z, n)
        return base, sum(x * y for x, y in zip(self.powers, offset))


def circle_mode(role, conjugate=False):
    c, l, _ = P.circle_kernel(role)
    sign = -1 if conjugate else 1
    if conjugate:
        c = np.array([x.conjugate() for x in c], dtype=object)
        l = np.array([x.conjugate() for x in l], dtype=object)
    return Mode(tuple([II * sign] * 4),
                tuple(sign * int(j in (0, role)) for j in range(4)),
                clean({0: c, sign: l * (II * sign)}))


def jmul(a, b):
    """Mixed-amplitude jet, with untruncated Laurent powers in t."""
    out = {}
    for (u, v, p), x in a.items():
        for (s, w, q), y in b.items():
            if u + s > 1 or v + w > 1:
                continue
            key = (u + s, v + w, p + q)
            out[key] = out.get(key, np.zeros((4, 4), dtype=object)) + x @ y
    return clean(out)


def jinv(a):
    return {k: ETA @ v.T @ ETA for k, v in a.items()}


def factor(left, right, role, offset):
    bl, pl = left.phase(offset)
    br, pr = right.phase(offset)
    xs = {p + pl: genmat(v[6 * role:6 * role + 6]) * bl
          for p, v in left.vector.items()}
    ys = {p + pr: genmat(v[6 * role:6 * role + 6]) * br
          for p, v in right.vector.items()}
    # exp(epsilon*x + delta*y); no epsilon^2 or delta^2 is needed for
    # the exact coefficient of epsilon*delta.
    out = {(0, 0, 0): N.I}
    for p, x in xs.items():
        out[1, 0, p] = x
    for p, y in ys.items():
        out[0, 1, p] = y
    for p, x in xs.items():
        for q, y in ys.items():
            key = (1, 1, p + q)
            out[key] = (out.get(key, np.zeros((4, 4), dtype=object))
                        + (x @ y + y @ x) * F(1, 2))
    return clean(out)


def literal_pair(left, right):
    """Differentiate every incident factor, then scatter to its link base.

    Action pairings with P equal those with (P-P^-1)/2 on Lorentz jets.
    The inverse factor variation is -X*L^-1, and the direct one is L*X.
    """
    amps = ((1, 0), (0, 1), (1, 1))
    ek = {a: {} for a in amps}
    eq = {a: {} for a in amps}
    for face, (r, s) in enumerate(N.PAIRS):
        er = tuple(int(j == r) for j in range(4))
        es = tuple(int(j == s) for j in range(4))
        locations = ((r, ZERO, False), (s, er, False),
                     (r, es, True), (s, ZERO, True))
        factors = [jinv(factor(left, right, role, offset)) if inverse
                   else factor(left, right, role, offset)
                   for role, offset, inverse in locations]
        prefix = [{(0, 0, 0): N.I}]
        for f in factors:
            prefix.append(jmul(prefix[-1], f))
        suffix = [None] * 5
        suffix[4] = {(0, 0, 0): N.I}
        for j in range(3, -1, -1):
            suffix[j] = jmul(factors[j], suffix[j + 1])
        for (u, v, p), matrix in prefix[4].items():
            if (u, v) in eq:
                out = eq[u, v].setdefault(p, np.zeros(10, dtype=object))
                for q in range(10):
                    out[q] += np.sum(N.DWEIGHT[face][q] * matrix)
        for slot, (role, offset, inverse) in enumerate(locations):
            weighted = {k: N.WEIGHT[face].T @ x
                        for k, x in prefix[slot].items()}
            covector = jmul(suffix[slot + 1], weighted)
            jet = ({k: -v for k, v in jmul(factors[slot], covector).items()}
                   if inverse else jmul(covector, factors[slot]))
            bl, pl = left.phase(offset)
            br, pr = right.phase(offset)
            for (u, v, p), matrix in jet.items():
                if (u, v) not in ek:
                    continue
                scale = QI.of(1) / (qpower(bl, u) * qpower(br, v))
                # Crucial input-minus-output placement for a shared link.
                power = p - u * pl - v * pr
                out = ek[u, v].setdefault(power, np.zeros(24, dtype=object))
                for g in range(6):
                    out[6 * role + g] += scale * np.sum(matrix.T * N.G[g])
    return ({a: clean(v) for a, v in ek.items()},
            {a: clean(v) for a, v in eq.items()})


def symbol_terms(stencil, bases, powers, rows):
    out = {}
    for shift, entries in stencil.items():
        phase = QI.of(1)
        for z, n in zip(bases, shift):
            phase *= qpower(z, n)
        p = sum(x * y for x, y in zip(shift, powers))
        matrix = out.setdefault(p, np.zeros((rows, 24), dtype=object))
        for rc, v in entries.items():
            matrix[rc] += phase * v
    return clean(out)


def papply(a, b, rows):
    out = {}
    for p, matrix in a.items():
        for q, vector in b.items():
            key = p + q
            out[key] = out.get(key, np.zeros(rows, dtype=object)) + matrix @ vector
    return clean(out)


def equal_terms(a, b):
    # QI(0) and the integer 0 have different dataclass representations.
    # Compare their exact arithmetic difference, not object equality.
    return set(a) == set(b) and all(not np.any(a[k] - b[k]) for k in a)


def scalar(x):
    x = QI.of(x)
    return (sp.Rational(x.re.numerator, x.re.denominator)
            + sp.I * sp.Rational(x.im.numerator, x.im.denominator))


def symbolic(terms, rows, cols=1):
    out = sp.zeros(rows, cols)
    for p, values in terms.items():
        a = np.asarray(values, dtype=object).reshape(rows, cols)
        for i, j in product(range(rows), range(cols)):
            out[i, j] += scalar(a[i, j]) * T ** p
    return out


def at_one(terms, shape):
    return sum(terms.values(), np.zeros(shape, dtype=object))


def check_linear(left, right, ek, eq):
    for amp, mode in (((1, 0), left), ((0, 1), right)):
        h = symbol_terms(P.H_LITERAL, mode.bases, mode.powers, 24)
        c = symbol_terms(P.C_LITERAL, mode.bases, mode.powers, 10)
        assert equal_terms(ek[amp], papply(h, mode.vector, 24))
        assert equal_terms(eq[amp], papply(c, mode.vector, 10))
        assert not ek[amp] and not eq[amp]
    check("LITERAL_AND_PHYSICAL_JOINT_INPUTS_LAURENTWISE", True)


def mixed_transfer():
    left, right = circle_mode(1), circle_mode(2, True)
    ek, eq = literal_pair(left, right)
    check_linear(left, right, ek, eq)
    bases = tuple(x * y for x, y in zip(left.bases, right.bases))
    powers = tuple(x + y for x, y in zip(left.powers, right.powers))
    assert bases == (QI.of(1),) * 4 and powers == (0, 1, -1, 0)
    h = symbol_terms(P.H_LITERAL, bases, powers, 24)
    c = symbol_terms(P.C_LITERAL, bases, powers, 10)
    H, C = symbolic(h, 24, 24), symbolic(c, 10, 24)
    f, q = symbolic(ek[1, 1], 24), symbolic(eq[1, 1], 10)
    # Both matrices are cleared by t^2. All arithmetic is in QQ(i)[t].
    hd = DomainMatrix.from_Matrix((T ** 2 * H).applyfunc(sp.expand))
    hd = hd.convert_to(sp.QQ_I.poly_ring(T))
    fd = DomainMatrix.from_Matrix((-T ** 2 * f).applyfunc(sp.expand))
    fd = fd.convert_to(hd.domain)
    numerator, denominator = hd.solve_den(fd)
    w = (numerator.to_Matrix() / hd.domain.to_sympy(denominator)).applyfunc(sp.cancel)
    stress = (q + C * w).applyfunc(sp.cancel)
    check("FULL_24_ROW_QUADRATIC_CONNECTION_COMPLETION",
          (H * w + f).applyfunc(sp.cancel) == sp.zeros(24, 1))
    check("CORRECTED_SLOW_Q11_EXACT", sp.cancel(stress[4] - sp.I * (T - 1) / T) == 0)
    check("CORRECTED_SLOW_Q22_EXACT", sp.cancel(stress[7] - sp.I * (T - 1)) == 0)
    zero = stress.applyfunc(lambda x: sp.simplify(sp.cancel(x).subs(T, 1)))
    derivative = stress.applyfunc(lambda x: sp.expand(sp.cancel(sp.diff(x, T)).subs(T, 1)))
    expected = sp.Matrix([0, 1-sp.I, -1-sp.I, 2*sp.I,
                          sp.I, 0, 0, sp.I, 0, -2*sp.I])
    check("SLOW_RESPONSE_ZERO_MEAN_BUT_NONZERO_FIRST_DERIVATIVE",
          zero == sp.zeros(10, 1) and derivative == expected)
    check("FIRST_TRANSFER_TRACE_ZERO", derivative[0]-derivative[4]-derivative[7]-derivative[9] == 0)
    check("DELETING_CONNECTION_CORRECTION_CHANGES_RESPONSE",
          (q - stress).applyfunc(sp.cancel) != sp.zeros(10, 1))
    H0 = sp.Matrix(N.real_matrix(N.A0).T.tolist())
    H2 = sp.Matrix(N.real_matrix(N.A2).T.tolist())
    assert (H.subs(T, 1) - H0).applyfunc(sp.expand) == sp.zeros(24)
    check("ALL_QUADRATIC_PRODUCT_OUTPUTS_HAVE_IR_GAPS", H0.det() == H2.det() == 256)
    check("COMPLETION_IS_REGULAR_NEAR_UNIT_FREQUENCY", all(sp.denom(x).subs(T, 1) != 0 for x in w))
    # A hostile non-kernel control distinguishes physical H from H^T.
    hc = symbol_terms(P.H_LITERAL, left.bases, left.powers, 24)
    column = next(j for j in range(24)
                  if any(np.any(m[:, j] - m.T[:, j]) for m in hc.values()))
    control = Mode(left.bases, left.powers, {0: np.eye(24, dtype=object)[column]})
    kc, _ = literal_pair(control, right)
    wrong = {p: m.T for p, m in hc.items()}
    check("HOSTILE_EULER_PLACEMENT_CONTROL",
          equal_terms(kc[1, 0], papply(hc, control.vector, 24))
          and not equal_terms(kc[1, 0], papply(wrong, control.vector, 24)))
    return {
        "output_character": ["1", "t", "1/t", "1"],
        "forcing_laurent_support": sorted(ek[1, 1]),
        "metric_laurent_support_before_completion": sorted(eq[1, 1]),
        "q11": "I*(t-1)/t", "q22": "I*(t-1)",
        "response_at_t1": ["0"] * 10,
        "response_first_derivative": [str(x) for x in derivative],
        "connection_correction": [str(x) for x in w],
        "response": [str(x) for x in stress],
        "det_H_plus1": 256, "det_H_minus1": 256,
        "scope": "full shared-link quadratic stationary jet; not exact nonlinear root",
    }


def fast_source_gate():
    mode = circle_mode(1)
    ek, eq = literal_pair(mode, mode)
    check_linear(mode, mode, ek, eq)
    bases = tuple(x * x for x in mode.bases)
    powers = tuple(2 * x for x in mode.powers)
    h = symbol_terms(P.H_LITERAL, bases, powers, 24)
    c = symbol_terms(P.C_LITERAL, bases, powers, 10)
    H = at_one(h, (24, 24))
    C = at_one(c, (10, 24))
    assert not np.any(H - N.real_matrix(N.A2).T)
    f = at_one(ek[1, 1], (24,)) * F(1, 2)
    q = at_one(eq[1, 1], (10,)) * F(1, 2)
    w = -N.H2INV @ f
    check("FAST_SELF_CHANNEL_CONNECTION_COMPLETE", not np.any(H @ w + f))
    stress = q + C @ w
    check("FAST_SELF_SOURCE_IS_NONZERO", np.any(stress))
    # Independent existing four-phase Euler assembly, for Re(i^p v(i)).
    _, real_fast = N.quadratic(np.array([0, 0, 1, 1, 0, 0, 1, 1], dtype=object))
    expected = np.array([2, -2, -1, -1, 0, 1, 1, 0, 0, 0], dtype=object)
    check("INDEPENDENT_REAL_FAST_SOURCE_REPLAY", np.array_equal(real_fast, expected))
    # Re(chi*v) has coefficient v/2 at each of +/- chi. Their self
    # products coincide at t=1, so the fast coefficient is Re(stress)/2.
    check("MIXED_JET_MATCHES_REAL_FOURPHASE_CONTROL",
          np.array_equal(np.array([QI.of(x).re / 2 for x in stress], dtype=object), real_fast))
    return {"positive_self_response_at_t1": [str(scalar(x)) for x in stress],
            "independent_real_fast_response": [str(x) for x in real_fast],
            "scope": "nonzero fast order-two source excludes this packet as a fixed-source witness"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = {"input_head": INPUT_HEAD, "mixed_transfer": mixed_transfer(),
              "fast_source_gate": fast_source_gate(), "parent_status": "PARTIAL / OPEN"}
    path = Path(__file__).with_name("a4d_joint_quadratic_beat_transfer_results.json")
    if args.write:
        path.write_text(json.dumps(result, indent=2) + "\n")
    else:
        check("PINNED_EXACT_RESULT_MATCHES", json.loads(path.read_text()) == result)
    print("RESULT QUADRATIC_STATIONARY_BEAT_SOURCE_NONZERO", flush=True)
    print("RESULT FAST_SOURCE_GATE_PREVENTS_FIXED_SOURCE_NOGO", flush=True)
    print("RESULT FIXED_SOURCE_GLOBAL_RESPONSE_THEOREM_OPEN", flush=True)


if __name__ == "__main__":
    main()
