#!/usr/bin/env python3
"""Exact physical image/cokernel test for moving-q0 detune forcings.

Task: WRK-A4D-Q0-PHYSICAL-FORCING-IMAGE

Consumes the merged polarized symbol builder and tests, over Q(i),

    P(z) = [ H_AA(z) | H_AQ(conj z) ]

against

    q0(z) = vec_sym(d d^T),  d_r = z_r^-1 - 1,
    w_j(z) = (z_j d/dz_j H_AQ(z)) q0(z).

The direct H_AA block is the connection Euler correction operator.  The
historical H_AA^T augmented row-system is deliberately not used here.

Only orbit types 5 and 7 are evaluated.  The holomorphic comparison

    P_holo(z) = [ H_AA(z) | H_AQ(z) ]

is retained solely to separate exact moving-kernel transport from the
physical conjugate-paired correction image.

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

HAB = ns["HAB"]          # 24 x 24 polarized connection Euler block
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
Dq0 = [sp.simplify(z[j] * q0.diff(z[j])) for j in range(4)]

ORBITS = {
    5: (sp.I, sp.I, -sp.I, -sp.I),
    7: (-sp.Integer(1), sp.I, sp.I, -sp.Integer(1)),
}

# These membership patterns were obtained by an independent exact rank run
# after correcting the H_AA versus H_AA^T carrier orientation.  The present
# certificate rederives them and, additionally, computes the exact cokernel
# residual norms.
EXPECTED_MEMBERSHIP = {
    5: [False, False, True, True],
    7: [False, True, True, False],
}
EXPECTED_Q0_NORM2 = {
    5: sp.Integer(40),
    7: sp.Integer(92),
}
EXPECTED_RAW_RESIDUAL2 = {
    5: [sp.Rational(8, 5), sp.Rational(8, 5), 0, 0],
    7: [sp.Integer(2), 0, 0, sp.Integer(2)],
}

records = {}

for orbit, phase in ORBITS.items():
    sub = {z[j]: phase[j] for j in range(4)}
    csub = {z[j]: sp.conjugate(phase[j]) for j in range(4)}

    # The census variable is the table character zeta.  The physical
    # character is chi=zeta^-1=conj(zeta).  The owned physical convention
    # A_phys(chi)=H_AB(chi)^T therefore becomes H_AB(zeta) on these unit
    # characters; certify that conversion rather than relying on the name.
    A = HAB.subs(sub)
    Aphys = HAB.subs(csub).T
    Cphys = HAQ.subs(csub)
    Cholo = HAQ.subs(sub)
    check(
        f"ORBIT_{orbit}_TABLE_TO_PHYSICAL_CONNECTION",
        A == Aphys,
    )
    P = A.row_join(Cphys)
    Pholo = A.row_join(Cholo)

    rP = erank(P)
    rPh = erank(Pholo)
    check(f"ORBIT_{orbit}_PHYSICAL_RANK_23", rP == 23, str(rP))
    check(f"ORBIT_{orbit}_HOLOMORPHIC_FULL_ROW_RANK_24", rPh == 24, str(rPh))

    left = sp.conjugate(P).T.nullspace()
    check(f"ORBIT_{orbit}_PHYSICAL_COKERNEL_DIM_1", len(left) == 1, str(len(left)))
    if len(left) != 1:
        records[orbit] = {
            "rank_physical": rP,
            "rank_holomorphic": rPh,
            "q0_norm_squared": None,
            "membership": None,
            "rows": [],
        }
        continue
    ell = left[0]
    ellnorm2 = sp.factor(hinner(ell, ell))
    check(f"ORBIT_{orbit}_LEFT_COKERNEL_NORM_NONZERO", ellnorm2 != 0, str(ellnorm2))

    qv = sp.simplify(q0.subs(sub))
    qnorm2 = sp.factor(hinner(qv, qv))
    check(
        f"ORBIT_{orbit}_Q0_NORM2",
        sp.simplify(qnorm2 - EXPECTED_Q0_NORM2[orbit]) == 0,
        str(qnorm2),
    )

    rows = []
    membership = []
    for j in range(4):
        w = sp.simplify((DC[j] * q0).subs(sub))
        rAug = erank(P.row_join(w))
        inside = rAug == rP
        membership.append(inside)

        alpha = sp.factor(hinner(ell, w))
        raw_res2 = sp.factor(
            sp.simplify(sp.conjugate(alpha) * alpha / ellnorm2)
        )
        unit_res2 = sp.factor(sp.simplify(raw_res2 / qnorm2))

        # Exact rank membership must agree with the one-dimensional physical
        # left-cokernel pairing.
        check(
            f"ORBIT_{orbit}_D{j}_RANK_PAIRING_AGREE",
            inside == (sp.simplify(alpha) == 0),
            f"inside={inside} alpha={alpha}",
        )
        check(
            f"ORBIT_{orbit}_D{j}_RAW_RESIDUAL2_EXACT",
            sp.simplify(
                raw_res2 - sp.sympify(EXPECTED_RAW_RESIDUAL2[orbit][j])
            ) == 0,
            str(raw_res2),
        )
        if inside:
            check(
                f"ORBIT_{orbit}_D{j}_PHYSICAL_RESIDUAL_ZERO",
                sp.simplify(raw_res2) == 0,
                str(raw_res2),
            )
        else:
            check(
                f"ORBIT_{orbit}_D{j}_PHYSICAL_RESIDUAL_NONZERO",
                sp.simplify(raw_res2) != 0,
                str(raw_res2),
            )

        # Same-carrier physical moving-germ control.  The submitted "hot"
        # forcing above is w(zeta), while the physical mixed block is C(chi).
        # For the actual moving germ at chi, differentiate C(chi) q0(chi)=0.
        # It must be absorbed exactly by the transported metric tangent.
        w_same = sp.simplify((DC[j] * q0).subs(csub))
        dq_same = sp.simplify(Dq0[j].subs(csub))
        transport_same = sp.simplify(w_same + Cphys * dq_same)
        check(
            f"ORBIT_{orbit}_D{j}_SAME_CARRIER_TRANSPORT_ZERO",
            all(sp.simplify(x) == 0 for x in transport_same),
        )
        check(
            f"ORBIT_{orbit}_D{j}_SAME_CARRIER_FORCING_IN_PHYSICAL_IMAGE",
            erank(P.row_join(w_same)) == rP,
        )

        # Holomorphic moving-kernel transport should absorb every w_j.
        rh = erank(Pholo.row_join(w))
        holo_inside = rh == rPh
        check(
            f"ORBIT_{orbit}_D{j}_HOLOMORPHIC_IN_IMAGE",
            holo_inside,
            f"rank {rPh}->{rh}",
        )

        rows.append({
            "direction": j,
            "rank_aug": rAug,
            "inside_physical_image": inside,
            "holomorphic_inside": holo_inside,
            "cokernel_pairing": sp.factor(alpha),
            "raw_residual_squared": raw_res2,
            "unit_q0_residual_squared": unit_res2,
        })

    check(
        f"ORBIT_{orbit}_PHYSICAL_MEMBERSHIP_PATTERN",
        membership == EXPECTED_MEMBERSHIP[orbit],
        str(membership),
    )

    records[orbit] = {
        "rank_physical": rP,
        "rank_holomorphic": rPh,
        "q0_norm_squared": qnorm2,
        "left_norm_squared": ellnorm2,
        "membership": membership,
        "rows": rows,
    }

print()
for orbit in (5, 7):
    rec = records[orbit]
    print(
        f"ORBIT_{orbit}: rank P={rec['rank_physical']} "
        f"rank Pholo={rec['rank_holomorphic']} "
        f"q0_norm2={rec['q0_norm_squared']} "
        f"left_norm2={rec.get('left_norm_squared')}"
    )
    for row in rec["rows"]:
        print(
            "  D{direction}: physical_inside={inside_physical_image} "
            "holomorphic_inside={holomorphic_inside} rank_aug={rank_aug} "
            "pairing={cokernel_pairing} raw_res2={raw_residual_squared} "
            "unit_res2={unit_q0_residual_squared}"
            .format(**row)
        )

if FAILS:
    print("J2-Q0-PHYSICAL-FORCING-COKERNEL: FAIL (%d)" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    raise SystemExit(1)

print("J2-Q0-CROSS-CARRIER-COKERNEL-SAME-CARRIER-TRANSPORT-EXACT")
print(
    "ORBIT5_CROSS: membership [outside,outside,inside,inside], "
    "raw residual2 [8/5,8/5,0,0], unit-q0 residual2 [1/25,1/25,0,0]."
)
print(
    "ORBIT7_CROSS: membership [outside,inside,inside,outside], "
    "raw residual2 [2,0,0,2], unit-q0 residual2 [1/46,0,0,1/46]."
)
print(
    "SAME_CARRIER: at chi=conj(zeta), every moving-germ forcing is "
    "absorbed exactly by C(chi) Dq0(chi)."
)
print(
    "SCOPE: exact Q(i) carrier-comparison theorem on orbit types 5 and 7 only."
)
print(
    "FIREWALL: the nonzero cross-character cokernel is a carrier-mismatch "
    "diagnostic, not a stationary-sheet stress, nonlinear joint branch, "
    "or metric-response anomaly."
)
