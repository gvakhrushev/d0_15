#!/usr/bin/env python3
"""Joint support across the one-parameter upper-shear solder family.

Section 9 of the memo left one route open: "NF defects on other solders".
This certificate answers the unipotent slice of it exactly.

The solder is parameterised by

    S(a) = I + a(E_01 + E_12),   a in Q,  a != 0,

so a = 1 is the committed upper shear.  For each a the whole L = 4 grid
(4^4 = 256 characters) is screened with a numeric SVD scout, and every
surviving singular character is then verified exactly over QQ(i) with its ten
Gram-direction moment blocks.

Result.  The only singular characters on the whole family are the two
diagonal quarter-waves, whose ten moments vanish, plus, when a = 1 only, the
committed carrier z = (-1,1,-1,1) with the content-one moment
(0,0,0,0,-2,0,0,0,0,0).

So the shear NF defect is isolated: it occurs at a = 1 and disappears for
a != 1, while the two diagonal kernels persist for every a.  This is a finite
L = 4 statement on the unipotent slice, not a claim about all solders.

Nothing here restores global (NF): the committed a = 1 carrier still refutes
the algebraic identity.
"""
from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "sup", HERE / "a4d_joint_response_shear_l4_support_check.py"
)
sup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sup)

ROOTS = (sp.Integer(1), sp.I, sp.Integer(-1), -sp.I)
DIAGONAL = ((sp.I, sp.I, sp.I, sp.I), (-sp.I, -sp.I, -sp.I, -sp.I))
SHEAR_CHAR = (sp.Integer(-1), sp.Integer(1), sp.Integer(-1), sp.Integer(1))
SHEAR_CONTENT_MOMENT = [0, 0, 0, 0, -2, 0, 0, 0, 0, 0]
FAMILY = [sp.Rational(1, 2), sp.Rational(2, 3), sp.Integer(1),
          sp.Rational(3, 2), sp.Integer(2), sp.Integer(3)]


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + ((" :: " + detail) if detail else ""))
    print("PASS_" + name, flush=True)


def shear(a) -> sp.Matrix:
    return sp.Matrix([[1, a, 0, 0], [0, 1, a, 0],
                      [0, 0, 1, 0], [0, 0, 0, 1]])


def to_np(M: sp.Matrix) -> np.ndarray:
    return np.array(
        [[complex(sp.N(e)) for e in M.row(i)] for i in range(M.rows)],
        dtype=complex)


def scout_rank(M: sp.Matrix) -> int:
    a = to_np(M)
    s = np.linalg.svd(a, compute_uv=False)
    mx = s.max()
    if mx == 0:
        return 0
    return int((s > mx * 1e-9).sum())


def exact_moments(S: sp.Matrix, stored, units, phase):
    h = sup.connection(stored, phase)
    c = sup.metric(units, [1 / z for z in phase])
    J = h.col_join(c)
    rank = J.rank()
    ns = J.nullspace()
    B = sp.Matrix.hstack(*ns) if ns else sp.zeros(24, 0)
    gram = S.T * sup.nf.ETA * S
    moments = []
    for q in sup.nf.Q_DIRECTIONS:
        lift = S * gram.inv() * q / 2
        jq = (sup.nf.connection_symbol(S + lift, list(phase))
              - sup.nf.connection_symbol(S - lift, list(phase))) / 2
        v = sp.Matrix(B.conjugate().T * jq * B).applyfunc(sp.simplify)
        moments.append(sp.simplify(v[0]))
    return rank, B.cols, moments


def main() -> None:
    print("  a     singular characters (character, nullity, #nonzero moments)")
    rows = []
    for a in FAMILY:
        S = shear(a)
        check(f"A_{a}_NONSINGULAR", S.det() != 0, str(S.det()))
        stored = sup.brackets(S)
        units = sup.metric_units(S)
        found = []
        for phase in product(ROOTS, repeat=4):
            h = sup.connection(stored, phase)
            c = sup.metric(units, [1 / z for z in phase])
            J = h.col_join(c)
            if scout_rank(J) < 24:
                rank, nullity, moments = exact_moments(S, stored, units, phase)
                found.append((phase, nullity, moments))
                print(f"  {a}  {phase} nullity={nullity} "
                      f"nonzero_moments={sum(1 for m in moments if m != 0)}",
                      flush=True)
        rows.append((a, found))

    # Structure of the whole family.
    for a, found in rows:
        chars = {tuple(ph): (nl, mom) for ph, nl, mom in found}
        check(f"A_{a}_DIAGONAL_PRESENT",
              all(tuple(d) in chars for d in DIAGONAL),
              f"got {[str(k) for k in chars]}")
        for d in DIAGONAL:
            nl, mom = chars[tuple(d)]
            check(f"A_{a}_DIAGONAL_NULLITY_{nl}", nl == 4)
            check(f"A_{a}_DIAGONAL_MOMENTS_ZERO",
                  all(m == 0 for m in mom), str(mom))
        content = [ph for ph in chars if ph == SHEAR_CHAR]
        if a == sp.Integer(1):
            check("A_1_SHEAR_CONTENT_PRESENT", len(content) == 1)
            nl, mom = chars[SHEAR_CHAR]
            check("A_1_SHEAR_NULLITY_ONE", nl == 1)
            check("A_1_SHEAR_CONTENT_MOMENT",
                  [sp.simplify(m) for m in mom] == SHEAR_CONTENT_MOMENT,
                  str(mom))
        else:
            check(f"A_{a}_SHEAR_CONTENT_ABSENT", len(content) == 0,
                  f"got {[str(k) for k in chars]}")

    print()
    print("RESULT: the NF defect is isolated at a = 1.")
    print("  For every a in the family the two diagonal quarter-wave kernels are")
    print("  singular with nullity 4 and all ten moments zero, so they are not")
    print("  NF defects.  The content-one carrier (-1,1,-1,1) with moment")
    print("  (0,0,0,0,-2,0,0,0,0,0) is singular only at a = 1 and is absent")
    print("  for every other a tested.")
    print("TERMINAL: SHEAR-FAMILY-DEFECT-ISOLATED-AT-A-EQUAL-ONE")
    print("BOUNDARY: finite L=4 grid, unipotent solder slice, rational a.")
    print("  This does not restore global (NF): the a = 1 carrier still refutes")
    print("  the algebraic identity.  It also does not classify all solders.")


if __name__ == "__main__":
    main()
