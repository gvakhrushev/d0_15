#!/usr/bin/env python3
"""Exact lifting of all six flat physical resonance circles at one coframe.

This is a frozen-symbol theorem on three complex lines and their conjugates,
not a full four-torus or varying-coframe response theorem.  The literal face
Hessian is independently assembled from the coframe and checked against the
owned physical (A.T; C) placement at the identity.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import reduce
from itertools import combinations
import json
from math import lcm
from pathlib import Path

import sympy as sp

import a4d_y_curved_joint_rational_stencil as S
from a4d_designated_full_gap_check import QI, elimination, flat_symbols
from a4d_identity_fourphase_circle_check import determinant, tr, evaluate, qpoly

HERE = Path(__file__).resolve().parent
PIN = HERE / "a4d_generic_coframe_circle_lift_results.json"
IMAG = QI(0, 1)


def symbol(coframe, phases, with_metric=False):
    """Literal frozen identity-link connection Hessian and optional Gram rows."""
    h = [[QI() for _ in range(24)] for _ in range(24)]
    c = [[QI() for _ in range(24)] for _ in range(10)]
    if with_metric:
        eta = [[F(S.ETA_SIG[i]) if i == j else F(0)
                for j in range(4)] for i in range(4)]
        ct = [[coframe[j][i] for j in range(4)] for i in range(4)]
        gram = sp.Matrix(S.mm(ct, S.mm(eta, coframe)))
        qi = [[F(x) for x in row] for row in gram.inv().tolist()]

    def character(shift):
        value = QI.of(1)
        for z, power in zip(phases, shift):
            if power == 1:
                value *= z
            elif power == -1:
                value /= z
            else:
                assert power == 0
        return value

    for r, s in S.PAIRS:
        u, v = [j for j in range(4) if j not in (r, s)]
        su, sv = ([coframe[j][k] for j in range(4)] for k in (u, v))
        area = S.wedge(su, sv)
        roles, signs = (r, s, r, s), (1, 1, -1, -1)
        offsets = ((0, 0, 0, 0), tuple(int(j == r) for j in range(4)),
                   tuple(int(j == s) for j in range(4)), (0, 0, 0, 0))
        for i, j in combinations(range(4), 2):
            shift = tuple(offsets[j][k] - offsets[i][k] for k in range(4))
            phase = character(shift)
            back = character(tuple(-x for x in shift))
            for gi, left in enumerate(S.GEN):
                for gj, right in enumerate(S.GEN):
                    bracket = S.msub(S.mm(left, right), S.mm(right, left))
                    coefficient = (F(S.orient(r, s) * signs[i] * signs[j], 2)
                                   * S.pair_star(area, S.biv(bracket)))
                    h[6 * roles[i] + gi][6 * roles[j] + gj] += phase * coefficient
                    h[6 * roles[j] + gj][6 * roles[i] + gi] += back * coefficient
        if with_metric:
            for row, (a, b) in enumerate(S.SYM):
                dq = S.zero()
                dq[a][b] = dq[b][a] = F(1)
                ds = S.mscale(F(1, 2), S.mm(coframe, S.mm(qi, dq)))
                du, dv = ([ds[j][k] for j in range(4)] for k in (u, v))
                darea = [x + y for x, y in zip(S.wedge(du, sv),
                                                 S.wedge(su, dv))]
                for pos in range(4):
                    for g, generator in enumerate(S.GEN):
                        coefficient = (S.orient(r, s) * signs[pos]
                                       * S.pair_star(darea, S.biv(generator)))
                        c[row][6 * roles[pos] + g] += (
                            character(offsets[pos]) * coefficient)
    return h, c


def line(coframe, role, with_metric=False):
    def at(a):
        phases = [IMAG] * 4
        phases[0] = phases[role] = a
        return symbol(coframe, phases, with_metric)
    plus, minus, quarter = [at(a) for a in (QI.of(1), QI.of(-1), IMAG)]
    zero = [[(plus[0][r][k] + minus[0][r][k]) / 2
             for k in range(24)] for r in range(24)]
    positive = [[(plus[0][r][k] - zero[r][k]
                  + (quarter[0][r][k] - zero[r][k]) / IMAG) / 2
                 for k in range(24)] for r in range(24)]
    negative = [[plus[0][r][k] - zero[r][k] - positive[r][k]
                 for k in range(24)] for r in range(24)]
    held = QI(F(3, 5), F(4, 5))
    direct_h, direct_c = at(held)
    assert direct_h == [[negative[r][k] / held + zero[r][k]
                         + positive[r][k] * held for k in range(24)]
                        for r in range(24)]
    return (negative, zero, positive), (plus, minus, quarter), (direct_h, direct_c)


def enc(z):
    return [str(F(str(sp.re(z)))), str(F(str(sp.im(z))))]


def run():
    identity = S.eye()
    # A real determinant-one coframe; its Gram matrix is Lorentzian.
    witness = S.eye()
    witness[1][0] = witness[2][1] = F(1, 2)
    assert sp.Matrix(witness).det() == 1
    records = []
    for role in (1, 2, 3):
        _, nodes, held = line(identity, role, with_metric=True)
        for a, (h, c) in zip((QI.of(1), QI.of(-1), IMAG,
                              QI(F(3, 5), F(4, 5))),
                             nodes + (held,)):
            phases = [IMAG] * 4
            phases[0] = phases[role] = a
            owner_h, owner_c = flat_symbols(phases)
            assert h == [list(row) for row in zip(*owner_h)]
            assert c == owner_c

        coefficients, _, _ = line(witness, role)
        denominator = reduce(
            lcm,
            (q for matrix in coefficients for row in matrix for z in row
             for q in (z.re.denominator, z.im.denominator)), 1)
        polynomial = []
        for row in range(24):
            cells = []
            for column in range(24):
                values = [denominator * matrix[row][column]
                          for matrix in coefficients]
                assert all(z.re.denominator == z.im.denominator == 1
                           for z in values)
                cells.append(tr([(int(z.re), int(z.im)) for z in values]))
            polynomial.append(cells)
        determinant_coefficients = determinant(polynomial)
        assert len(determinant_coefficients) == 35
        a = sp.symbols("a")
        full = sp.Poly(sum((sp.Integer(re) + sp.I * sp.Integer(im)) * a**j
                           for j, (re, im) in enumerate(determinant_coefficients)),
                       a, extension=sp.I)
        factor = sp.Poly(a**14 * (a - sp.I)**8, a, extension=sp.I)
        quotient, remainder = sp.div(full, factor, domain=sp.QQ_I)
        assert remainder.is_zero and quotient.degree() == 12
        scalar, irreducibles = sp.factor_list(quotient, extension=sp.I)
        assert sorted([p.degree() for p, _ in irreducibles]) == (
            [3, 3, 3, 3] if role == 1 else [6, 6])
        for poly, multiplicity in irreducibles:
            assert multiplicity == 1
            reverse_conjugate = sp.Poly(
                sum(sp.conjugate(z) * a**j
                    for j, z in enumerate(poly.all_coeffs())),
                a, extension=sp.I)
            # A unit-modulus root of poly is also a root of its reverse
            # conjugate. Coprimality rules out all such roots exactly.
            assert sp.gcd(poly, reverse_conjugate).degree() == 0
        at_quarter, quarter_metric = symbol(witness, [IMAG] * 4, True)
        assert elimination(at_quarter)[0] == 16
        assert elimination(at_quarter + quarter_metric)[0] == 20
        held_value = QI(F(3, 5), F(4, 5))
        for control in (("single_shear", "diagonal_warp") if role == 1 else ()):
            test = S.eye()
            if control == "single_shear":
                test[1][0] = F(1, 2)
            else:
                test[2][2] = test[3][3] = F(3, 2)
            control_h, _ = symbol(
                test,
                [held_value if j in (0, role) else IMAG for j in range(4)])
            assert elimination(control_h)[0] == 22
        at_held, _ = symbol(
            witness,
            [held_value if j in (0, role) else IMAG for j in range(4)])
        rank, determinant_value = elimination(at_held)
        assert rank == 24
        scale = QI.of(1)
        for _ in range(24):
            scale *= denominator * held_value
        assert evaluate(qpoly(determinant_coefficients), held_value) == (
            scale * determinant_value)
        records.append({
            "spatial_role": role,
            "clearing_denominator": denominator,
            "determinant_degree": 34,
            "determinant_quotient_coefficients": [
                enc(z) for z in reversed(quotient.all_coeffs())],
            "quotient_factor_degrees": [p.degree() for p, _ in irreducibles],
            "each_factor_coprime_to_reverse_conjugate": True,
            "connection_rank_at_quarter": 16,
            "joint_rank_at_quarter": 20,
            "rank_at_held_out_unit_character": rank,
        })
        print(f"PASS_ROLE_{role}_WHOLE_UNIT_CIRCLE_LIFT_EXCEPT_QUARTER", flush=True)
    return {
        "schema": "a4d-generic-coframe-flat-circle-lift-v1",
        "coframe": [[str(z) for z in row] for row in witness],
        "physical_placement_control": "literal Hessian and Gram rows equal (A.T;C) on each line coefficientwise",
        "determinant_formula": "det[(den*a)*H_S(a,a,i,i)] = a^14*(a-i)^8*P(a)",
        "negative_circle_controls": "on role-1 circle, single shear and diagonal warp retain rank 22; two-shear witness lifts",
        "records": records,
        "conclusion": "All three old flat plus-i circles and real conjugates have full connection rank except at the diagonal quarter points for this fixed nonorthogonal coframe.",
        "scope": "frozen lines only; no all-torus or varying-coframe uniform inverse; no task terminal",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.write:
        PIN.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", PIN, flush=True)
    else:
        assert result == json.loads(PIN.read_text())
        print("PASS_PINNED_RESULTS", flush=True)
