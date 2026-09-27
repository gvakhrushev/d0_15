#!/usr/bin/env python3
"""Exact physical image/cokernel test for moving-q0 detune forcings.

Task: WRK-A4D-Q0-PHYSICAL-FORCING-IMAGE

Consumes the merged polarized symbol builder and tests, over Q(i),

    P(z) = [ A(z) | C(conj z) ],
    A(z) = H_AA(z)^T,
    C(z) = H_AQ(z),

against

    q0(z) = vec_sym(d d^T),  d_r = z_r^-1 - 1,
    w_j(z) = (z_j d/dz_j C(z)) q0(z).

Only orbit types 5 and 7 are evaluated.  The holomorphic map
[A(z)|C(z)] is retained solely as a contrast.

No floating point, SVD threshold, or pseudoinverse is used.
"""
from __future__ import annotations

import os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "a4d_joint_resonance_linear_kernel_check.py")

text = open(SRC, encoding="utf-8").read()
cut = text.index(
    "# ---------------------------------------------------------------------------\n"
    "# 2. Reproduce the nine owned singular orbit types"
)
ns = {"__name__": "_q0_physical_owner", "__file__": SRC}
exec(compile(text[:cut], SRC, "exec"), ns)

HAB = ns["HAB"]          # 24 x 24 polarized connection block
HAQ = ns["HAQ"]          # 24 x 10 connection x metric block
z = ns["z"]
SYM = ns["SYM"]

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


def erank(M: sp.Matrix) -> int:
    return M.to_DM(extension=True).rank()


def hinner(x: sp.Matrix, y: sp.Matrix) -> sp.Expr:
    return sp.simplify((sp.conjugate(x).T * y)[0])


q0 = sp.Matrix([
    (1 / z[a] - 1) * (1 / z[b] - 1)
    for a, b in SYM
])
DC = [sp.simplify(z[j] * HAQ.diff(z[j])) for j in range(4)]

ORBITS = {
    5: (sp.I, sp.I, -sp.I, -sp.I),
    7: (-sp.Integer(1), sp.I, sp.I, -sp.Integer(1)),
}

# Submitted finite scout claim to be checked, not assumed in construction:
# orbit 5: directions 0,1 outside physical image; 2,3 inside.
EXPECTED_ORBIT5_MEMBERSHIP = [False, False, True, True]

records = {}

for orbit, phase in ORBITS.items():
    sub = {z[j]: phase[j] for j in range(4)}
    csub = {z[j]: sp.conjugate(phase[j]) for j in range(4)}

    A = HAB.subs(sub).T
    Cphys = HAQ.subs(csub)
    Cholo = HAQ.subs(sub)
    P = A.row_join(Cphys)
    Pholo = A.row_join(Cholo)

    rP = erank(P)
    rPh = erank(Pholo)
    check(f"ORBIT_{orbit}_PHYSICAL_RANK_23", rP == 23, str(rP))

    left = sp.conjugate(P).T.nullspace()
    check(f"ORBIT_{orbit}_PHYSICAL_COKERNEL_DIM_1", len(left) == 1, str(len(left)))
    ell = left[0]

    qv = sp.simplify(q0.subs(sub))
    qnorm2 = sp.simplify(hinner(qv, qv))
    check(f"ORBIT_{orbit}_Q0_NORM_POSITIVE", qnorm2.is_positive is True, str(qnorm2))

    rows = []
    membership = []
    for j in range(4):
        w = sp.simplify((DC[j] * q0).subs(sub))
        rAug = erank(P.row_join(w))
        inside = rAug == rP
        membership.append(inside)

        alpha = sp.simplify(hinner(ell, w))
        ellnorm2 = sp.simplify(hinner(ell, ell))
        raw_res2 = sp.simplify(sp.conjugate(alpha) * alpha / ellnorm2)
        unit_res2 = sp.simplify(raw_res2 / qnorm2)

        # Rank and exact orthogonal-cokernel tests must agree.
        check(
            f"ORBIT_{orbit}_D{j}_RANK_PAIRING_AGREE",
            inside == (sp.simplify(alpha) == 0),
            f"inside={inside} alpha={alpha}",
        )
        if inside:
            check(f"ORBIT_{orbit}_D{j}_RESIDUAL_ZERO", raw_res2 == 0, str(raw_res2))
        else:
            check(f"ORBIT_{orbit}_D{j}_RESIDUAL_NONZERO", raw_res2 != 0, str(raw_res2))

        # Holomorphic contrast: moving-kernel transport places w in im C(z).
        rh = erank(Pholo.row_join(w))
        check(
            f"ORBIT_{orbit}_D{j}_HOLOMORPHIC_CONTRAST_IN_IMAGE",
            rh == rPh,
            f"rank {rPh}->{rh}",
        )

        rows.append({
            "direction": j,
            "rank_aug": rAug,
            "inside_physical_image": inside,
            "raw_residual_squared": sp.factor(raw_res2),
            "unit_q0_residual_squared": sp.factor(unit_res2),
        })

    if orbit == 5:
        check(
            "ORBIT_5_SUBMITTED_SPLIT_EXACT",
            membership == EXPECTED_ORBIT5_MEMBERSHIP,
            str(membership),
        )
        # The old floating scout quoted sqrt(8/5) after unit-q normalization.
        outs = [r for r in rows if not r["inside_physical_image"]]
        check(
            "ORBIT_5_UNIT_RESIDUAL_SQ_8_OVER_5",
            len(outs) == 2
            and all(sp.simplify(r["unit_q0_residual_squared"] - sp.Rational(8, 5)) == 0
                    for r in outs),
            str([r["unit_q0_residual_squared"] for r in outs]),
        )

    records[orbit] = {
        "rank_physical": rP,
        "rank_holomorphic": rPh,
        "q0_norm_squared": sp.factor(qnorm2),
        "membership": membership,
        "rows": rows,
    }

print()
for orbit in (5, 7):
    rec = records[orbit]
    print(f"ORBIT_{orbit}: rank P={rec['rank_physical']} "
          f"rank Pholo={rec['rank_holomorphic']} q0_norm2={rec['q0_norm_squared']}")
    for row in rec["rows"]:
        print(
            "  D{direction}: inside={inside_physical_image} rank_aug={rank_aug} "
            "raw_res2={raw_residual_squared} unit_res2={unit_q0_residual_squared}"
            .format(**row)
        )

if FAILS:
    print("J2-Q0-PHYSICAL-FORCING-IMAGE: FAIL (%d)" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    raise SystemExit(1)

print("J2-Q0-PHYSICAL-FORCING-IMAGE-EXACT")
print("SCOPE: exact Q(i) image/cokernel membership on physical orbit types 5 and 7 only.")
print("FIREWALL: nonzero cokernel class is not a nonlinear stress or joint-critical solution.")
