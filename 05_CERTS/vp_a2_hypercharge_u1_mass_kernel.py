#!/usr/bin/env python3
"""
A2 certificate: hypercharge U(1) mass-kernel operator test.

Claim under test (new A2 concrete entry point): can the existing frozen graph-flow
objects force a real abelian coupling operator

    C_U1 : H_abelian -> K_arch,      M_U1 = C_U1^T C_U1,

such that ker(M_U1) is exactly span{Y}, excluding B-L?

Honest verdict: NO-GO+ from the checked repository state.  The repo closes the
cycle lattice dim ker(B_graph)=327 and the anomaly variety span{Y,B-L}, but it
contains no source-defined C_U1 / Phi / flow-to-Weyl-ledger map.  Any operator
that kills exactly B-L's coefficient is equivalent to the nu^c-localization bridge
already recorded as ASSUMP-KERNEL-CHARGE-LOCALIZATION, not a forced graph-flow
operator.

This cert is deterministic, stdlib-only, and includes reachable FAIL controls.
"""
from fractions import Fraction as F
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def emit(tag, ok, msg=""):
    print(("PASS_" if ok else "FAIL_") + tag + ((": " + msg) if msg else ""))
    return ok


def dot(u, v):
    return sum(a*b for a, b in zip(u, v))


def mat_vec(M, x):
    return [dot(row, x) for row in M]


def rank_q(rows):
    M = [list(r) for r in rows if any(x != 0 for x in r)]
    if not M:
        return 0
    nrows, ncols = len(M), len(M[0])
    rank = 0
    for col in range(ncols):
        piv = None
        for r in range(rank, nrows):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][col]
        M[rank] = [x / pv for x in M[rank]]
        for r in range(nrows):
            if r != rank and M[r][col] != 0:
                fac = M[r][col]
                M[r] = [x - fac*y for x, y in zip(M[r], M[rank])]
        rank += 1
        if rank == nrows:
            break
    return rank


def nullity_q(M, ncols):
    return ncols - rank_q(M)


def build_tripartite_counts():
    V = 9 + 11 + 13
    E = 9*11 + 9*13 + 11*13
    rankB = V - 1
    cycle_dim = E - rankB
    return V, E, rankB, cycle_dim


def anomaly_rows():
    # field order q_L,u^c,d^c,l_L,e^c,nu^c
    A = [
        [F(6), F(3), F(3), F(2), F(1), F(1)],
        [F(3), F(0), F(0), F(1), F(0), F(0)],
        [F(2), F(1), F(1), F(0), F(0), F(0)],
    ]
    Y = [F(1,6), F(-2,3), F(1,3), F(-1,2), F(1), F(0)]
    BL = [F(1,3), F(-1,3), F(-1,3), F(-1), F(1), F(1)]
    return A, Y, BL


def main():
    print("=== vp_a2_hypercharge_u1_mass_kernel (A2 FORCE-or-NOGO test) ===")
    print("SOURCE_STATUS: repo defines B_graph/cycle lattice and anomaly rows; no source-defined C_U1 was found.")

    ok = True
    V, E, rankB, cycle_dim = build_tripartite_counts()
    ok &= emit("GRAPH_FLOW_LATTICE_327", (V, E, rankB, cycle_dim) == (33, 359, 32, 327),
               f"V={V}, E={E}, rank(B)={rankB}, dim ker(B)={cycle_dim}")

    A, Y, BL = anomaly_rows()
    rankA = rank_q(A)
    ok &= emit("ANOMALY_LINEAR_RANK_3", rankA == 3, f"rank={rankA}, linear nullity={6-rankA}")
    ok &= emit("Y_AND_BL_INDEPENDENT", rank_q([Y, BL]) == 2,
               "span{Y,B-L} is at least 2-dimensional")
    ok &= emit("Y_BL_SATISFY_LINEAR_CONSTRAINTS", mat_vec(A, Y) == [0,0,0] and mat_vec(A, BL) == [0,0,0])

    # Existing frozen constraints do not distinguish Y from B-L.
    ok &= emit("EXISTING_FROZEN_LINEAR_KERNEL_CONTAINS_Y_AND_BL",
               mat_vec(A, Y) == [0,0,0] and mat_vec(A, BL) == [0,0,0],
               "any M built only from these linear constraints has ker containing both")

    # Candidate bridge that WOULD select Y: nu^c coordinate functional. This is known bridge, not forced.
    nu = [F(0), F(0), F(0), F(0), F(0), F(1)]
    ok &= emit("BRIDGE_NU_COORDINATE_SELECTS_Y_CONDITIONALLY",
               dot(nu, Y) == 0 and dot(nu, BL) == 1,
               "nu^c charge reads B-L coefficient; this is ASSUMP-KERNEL-CHARGE-LOCALIZATION, not graph-flow forced")

    # NO-GO+ gate: no forced C_U1 in the source, so positive closure must fail.
    emit("FORCED_C_U1_SOURCE_DERIVED", False,
         "no C_U1: H_abelian -> K_arch definition or rigidity owner exists in the inspected source")
    emit("A2_KERNEL_EXACTLY_SPAN_Y", False,
         "cannot prove ker(M_U1)=span{Y}; M_U1 itself is the missing primitive")

    # Reachable FAIL controls.
    # (i) zero coupling: mass matrix kernel contains both Y and BL.
    M_zero = []  # 0x6 matrix, kernel all Q^6
    if nullity_q(M_zero, 6) >= 2 and mat_vec(M_zero, Y) == [] and mat_vec(M_zero, BL) == []:
        emit("CONTROL_ZERO_COUPLING_KERNEL_TOO_LARGE", False,
             "C_U1=0 leaves ker dimension 6, including span{Y,B-L}")
    else:
        emit("CONTROL_ZERO_COUPLING_KERNEL_TOO_LARGE", True)

    # (ii) anomaly coupling rows: still keeps Y and BL massless.
    if mat_vec(A, Y) == [0,0,0] and mat_vec(A, BL) == [0,0,0]:
        emit("CONTROL_ANOMALY_COUPLING_STILL_2D", False,
             "using anomaly rows as C kills both Y and B-L; does not select hypercharge")
    else:
        emit("CONTROL_ANOMALY_COUPLING_STILL_2D", True)

    # (iii) hand-picked nu functional selects Y but is inadmissible as forced graph-flow operator.
    if dot(nu, Y) == 0 and dot(nu, BL) != 0:
        emit("CONTROL_HANDPICKED_NU_SELECTOR_INADMISSIBLE", False,
             "nu^c coordinate would exclude B-L, but this is exactly the bridge assumption, not forced")
    else:
        emit("CONTROL_HANDPICKED_NU_SELECTOR_INADMISSIBLE", True)

    # (iv) source-derived-claim overclaim must fail.
    emit("CONTROL_SM_TABLE_AS_OPERATOR_REJECTED", False,
         "defining C_U1 from the desired Y row assumes the conclusion")

    print("VERDICT_A2_NO_GO_PLUS: exact missing primitive = PRIM-U1-MASS-COUPLING-FLOW-TO-LEDGER (a source-derived C_U1/Phi).")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
