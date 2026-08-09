#!/usr/bin/env python3
"""D0-EDGE-INVARIANT-CROSS-SECTOR-001 — the edge count 359 = e2(9,11,13) = |E(K(9,11,13))|
(origin owner: D0-SCENE-001, edge_count_K_9_11_13) is the SAME owned object consumed by five
registered sector chains (spectral action / alpha / metric-signature / matter / S_DE-phason
window). COR grade in the D0-XI5-CROSS-SECTOR-001 sense (note-level tag): correlation of
consumers of one invariant; NO intertwiner claimed (ceiling owned twice:
D0-SDE-CUBIC-SPECTRAL-DISJOINTNESS-001 Bezout certificate 39590739579959;
D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001 "No trace/det coincidence is an intertwiner").
This row is NOT the "predeclared cross-sector transfer" of the Bezout row's unless-clause —
COR is not a transfer. Consumer list enumerated, not exhaustive (sixth-plus consumers exist:
Tr G = 4|E|, Perron 718/33, cycle space E-V+1).

REQUIRED clause carried verbatim from BOOK_07:1789 (Iter27-CAP): the identity is structural
while the VALUE is scene-specific — the identities hold on any finite complete-tripartite
scene; the scene content is only the identification of the five registered constants as one
edge count, never the identities themselves.

Faces (each rebuilt from its OWN sector definition by shared face-functions, applied to the
scene AND to the rival K(9,11,15) in the lockstep control):
  1. combinatorial: |E| counted from the adjacency matrix (origin owner D0-SCENE-001);
  2. spectral action: a0 = Tr L and EH proxy = sum of squared off-diagonal LAPLACIAN entries
     (-1 on edges) — D0-SCENE-SPECTRAL-ACTION-001 mechanism, minted in the same session's
     Campaign 0 (mint order: this row only after items 2/20/25 of
     REGISTRY_ROW_PROPOSALS_2026_08.md — done);
  3. alpha: alpha_top^-1 = |E|*phi^-2 - phi^-5 (D0-EDGE-ALPHA-001, zetaEdge edge-indexed BY
     CONSTRUCTION as 358 bulk + 1 seam = |E| slots); exact Z[phi], tethered to the
     independently hand-derived pair (726, -364); SCOPED OUT of the lockstep (no owned
     rival-scene alpha formula exists);
  4. metric/matter: secular cubic charpoly of Q = 1 n^T - diag n by exact determinant
     expansion — linear coefficient -e2, constant -2*prod(zones)
     (D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001 pairwise_is_edgecount; irreducibility face:
     D0-SCENE-JOINT-COMMUTANT-SIX-001 / D0-YUKAWA-COMMUTANT-SPECTRUM-001, same Campaign 0);
  5. S_DE/phason window: normalized-Laplacian zone-quotient charpoly x(x^2 - 3x + e2*2V/prod
     deg) — product of the two nontrivial eigenvalues = 359/160, Lean-owned at
     D0-SCENE-ACTIVE-EIGENVALUES-001 (scene_active_eigenvalues_prod); window scales
     VALUE-OWNED per BOOK_08 Iter23; discriminant 1/40 at
     D0-WINDOW-SCALE-DISCRIMINANT-FORCED-001.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCENE = (9, 11, 13)
RIVAL = (9, 11, 15)


# ---------- face functions (shared by scene and rival — the lockstep discipline) ------------

def adjacency(zones):
    V = sum(zones)
    zone_of = []
    for k, n in enumerate(zones):
        zone_of += [k] * n
    A = [[1 if zone_of[i] != zone_of[j] else 0 for j in range(V)] for i in range(V)]
    return A


def laplacian(zones):
    A = adjacency(zones)
    V = len(A)
    degs = [sum(row) for row in A]
    return [[(degs[i] if i == j else 0) - A[i][j] for j in range(V)] for i in range(V)]


def edge_count(zones):
    A = adjacency(zones)
    V = len(A)
    return sum(A[i][j] for i in range(V) for j in range(V) if i < j)


def sym_e2(zones):
    a, b, c = zones
    return a * b + a * c + b * c


def trace_L(zones):
    L = laplacian(zones)
    return sum(L[i][i] for i in range(len(L)))


def eh_proxy(zones):
    # the D0-SCENE-SPECTRAL-ACTION-001 mechanism: off-diagonal Laplacian entries are -1
    # exactly on edges; their SQUARES are edge indicators; half-sum = |E|
    L = laplacian(zones)
    V = len(L)
    return sum(L[i][j] * L[i][j] for i in range(V) for j in range(V) if i < j)


def charpoly_coeffs_3x3(m):
    # det(x I - m) = x^3 + c2 x^2 + c1 x + c0, exact arithmetic
    tr = m[0][0] + m[1][1] + m[2][2]
    minors = 0
    for i in range(3):
        for j in range(3):
            if i < j:
                minors += m[i][i] * m[j][j] - m[i][j] * m[j][i]
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
           - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
           + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    return (-tr, minors, -det)


def secular_cubic(zones):
    Q = [[zones[j] - (zones[i] if i == j else 0) for j in range(3)] for i in range(3)]
    return charpoly_coeffs_3x3(Q)


def normalized_quotient_pair_product(zones):
    # random-walk normalized Laplacian on the zone quotient (similar to the symmetric form,
    # same spectrum {0, lambda_c, lambda_r}); returns (sum, product) of the nontrivial pair
    V = sum(zones)
    RW = [[F(0) if i == j else F(zones[j], V - zones[i]) for j in range(3)] for i in range(3)]
    Lhat = [[(F(1) if i == j else F(0)) - RW[i][j] for j in range(3)] for i in range(3)]
    h2, h1, h0 = charpoly_coeffs_3x3(Lhat)
    assert h0 == 0, h0  # spectrum contains 0
    return (-h2, h1)


def zphi_mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def zphi_pow(n):
    r = (F(1), F(0))
    step = (F(0), F(1)) if n >= 0 else (F(-1), F(1))
    for _ in range(abs(n)):
        r = zphi_mul(r, step)
    return r


def poly_resultant_deg2_deg3(p, q):
    p2, p1, p0 = p
    q3, q2, q1, q0 = q
    rows = [
        [p2, p1, p0, 0, 0],
        [0, p2, p1, p0, 0],
        [0, 0, p2, p1, p0],
        [q3, q2, q1, q0, 0],
        [0, q3, q2, q1, q0],
    ]
    m = [[F(x) for x in row] for row in rows]
    n = 5
    det = F(1)
    for k in range(n):
        piv = None
        for r in range(k, n):
            if m[r][k] != 0:
                piv = r
                break
        assert piv is not None, "singular Sylvester matrix"
        if piv != k:
            m[k], m[piv] = m[piv], m[k]
            det = -det
        det *= m[k][k]
        for r in range(k + 1, n):
            f = m[r][k] / m[k][k]
            for c in range(k, n):
                m[r][c] -= f * m[k][c]
    assert det.denominator == 1
    return det.numerator


def main() -> int:
    print("=== D0-EDGE-INVARIANT-CROSS-SECTOR-001  359 = e2 = |E|: one invariant, five registered consumers ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: shared object = |E(K(9,11,13))| = e2(zone sizes), origin owner "
          "D0-SCENE-001; every structural face is a FUNCTION applied identically to scene and rival; "
          "COR not THE; list enumerated, not exhaustive; identities structural, VALUE scene-specific "
          "(BOOK_07:1789 clause)")

    # Laplacian well-formedness pin (skeptic RD-1): degree diagonal + entries in {0,-1} is
    # equivalent to every row summing to zero; kills the D+A sign-flip mutant.
    assert all(sum(row) == 0 for row in laplacian(SCENE))
    assert all(sum(row) == 0 for row in laplacian(RIVAL))

    # -- face 1: combinatorial ------------------------------------------------------------------
    E = edge_count(SCENE)
    e2 = sym_e2(SCENE)
    assert E == e2 == 359, (E, e2)
    print(f"PASS_EDGE_COUNT  |E| counted from adjacency = {E} = e2(9,11,13) = {e2}  (origin owner D0-SCENE-001)")

    # -- face 2: spectral action (Laplacian-built) ----------------------------------------------
    a0 = trace_L(SCENE)
    proxy = eh_proxy(SCENE)
    assert a0 == 2 * E == 718
    assert proxy == E
    print(f"PASS_SPECTRAL_ACTION_FACE  a0 = Tr L = {a0} = 2E; EH proxy = sum of squared off-diagonal "
          f"Laplacian entries = {proxy} = |E|  (mechanism: (-1)^2 edge indicators)")

    # -- face 3: alpha (edge-indexed by construction; lockstep-EXEMPT) --------------------------
    alpha_pair = zphi_mul((F(E), F(0)), zphi_pow(-2))
    alpha_pair = (alpha_pair[0] - zphi_pow(-5)[0], alpha_pair[1] - zphi_pow(-5)[1])
    # independent tether: 359*phi^-2 - phi^-5 with phi^-2 = 2-phi, phi^-5 = 5*phi-8 gives
    # (359*2+8, -359-5) = (726, -364), derived by hand from the registered form
    assert alpha_pair == (F(726), F(-364)), alpha_pair
    # mirror of the Lean zetaEdge construction: 358 bulk + 1 seam slots, edge-indexed = |E|
    assert 358 + 1 == E
    phi = (1 + 5 ** 0.5) / 2
    a_val = float(alpha_pair[0]) + float(alpha_pair[1]) * phi
    assert abs(a_val - 137.0356) < 1e-3, a_val
    print(f"PASS_ALPHA_FACE  alpha_top^-1 = |E|*phi^-2 - phi^-5 = (726, -364) in Z[phi] (~{a_val:.4f}); "
          "zetaEdge is edge-indexed BY CONSTRUCTION (358 bulk + 1 seam = |E| slots); "
          "SCOPE: no owned rival-scene alpha formula -- this face is exempt from the lockstep control")

    # -- face 4: metric/matter ------------------------------------------------------------------
    c2, c1, c0 = secular_cubic(SCENE)
    assert (c2, c1, c0) == (0, -e2, -2 * SCENE[0] * SCENE[1] * SCENE[2]), (c2, c1, c0)
    print(f"PASS_METRIC_FACE  charpoly(Q) = x^3 - {-c1}x - {-c0}  (linear coeff = -e2 = -|E|; const = -2*prod zones)")
    divisors = [d for d in range(1, 2575) if 2574 % d == 0]
    rational_roots = [s * d for d in divisors for s in (1, -1) if (s * d) ** 3 - 359 * (s * d) - 2574 == 0]
    assert rational_roots == [], rational_roots
    print(f"PASS_MATTER_FACE  cubic x^3-359x-2574 has NO rational root ({len(divisors)}-divisor sweep x2 signs) "
          "= the Yukawa non-degeneracy face (D0-YUKAWA-COMMUTANT-SPECTRUM-001 / D0-SCENE-JOINT-COMMUTANT-SIX-001)")

    # -- face 5: S_DE/phason window -------------------------------------------------------------
    pair_sum, pair_prod = normalized_quotient_pair_product(SCENE)
    V = sum(SCENE)
    prod_deg = 1
    for z in SCENE:
        prod_deg *= (V - z)
    assert pair_sum == 3 and pair_prod == F(E, 160) and F(prod_deg, 2 * V) == 160
    print(f"PASS_WINDOW_FACE  normalized-quotient charpoly = x(x^2 - 3x + {pair_prod}); lambda_c*lambda_r = "
          f"|E|/160 exactly (Lean owner D0-SCENE-ACTIVE-EIGENVALUES-001; 160 = prod(deg)/(2V) = {prod_deg}/{2*V})")

    # ---- NEGATIVE CONTROLS (each can fail the CONCLUSION) --------------------------------------
    # control 1: lockstep — the SAME face functions on the rival K(9,11,15). Every structural
    # face must land on the rival's e2 = 399 together; a hardcoded or wrongly-built face lands
    # on 359 (or anything else) and dies here.
    rE, re2 = edge_count(RIVAL), sym_e2(RIVAL)
    rc2, rc1, rc0 = secular_cubic(RIVAL)
    r_prod_zones = RIVAL[0] * RIVAL[1] * RIVAL[2]
    r_sum, r_prod = normalized_quotient_pair_product(RIVAL)
    rV = sum(RIVAL)
    r_prod_deg = 1
    for z in RIVAL:
        r_prod_deg *= (rV - z)
    assert rE == re2 == 399 and re2 != e2
    assert trace_L(RIVAL) == 2 * rE and eh_proxy(RIVAL) == rE
    assert (rc2, rc1, rc0) == (0, -re2, -2 * r_prod_zones)
    assert r_sum == 3 and r_prod == F(re2 * 2 * rV, r_prod_deg)
    print(f"FAIL_LOCKSTEP_RIVAL  K(9,11,15): edge count, Tr L, EH proxy, cubic coefficient and window "
          f"product ALL land on e2 = {re2} != 359 via the SAME face functions (alpha face exempt by "
          "scope); a face that does not track e2 structurally dies here")

    # control 2: rival constants of the SAME scene pass no face; the a2 remainder is
    # e2-COUPLED, not e2-free: 15708 = sum n_z*deg_z^2 = V*e2 + 3*e3 = 33*359 + 3*1287, and
    # = 14990 + 2|E| (the owned backtracking gap). Only the VALUE inequality is the control.
    L = laplacian(SCENE)
    diag_sq = sum(L[i][i] * L[i][i] for i in range(V))
    e3 = SCENE[0] * SCENE[1] * SCENE[2]
    assert diag_sq == 15708 == V * e2 + 3 * e3 == 14990 + 2 * E
    for wrong in (V, e3, diag_sq, 160):
        assert wrong != E
    print("FAIL_WRONG_INVARIANT  e1=33, e3=1287, diag-square term 15708, window 160: none equals |E| "
          "(15708 is e2-COUPLED -- V*e2+3*e3 and 14990+2|E| -- but is not the shared object itself)")

    # control 3: the intertwiner ceiling
    res = poly_resultant_deg2_deg3((160, -480, 359), (1, 0, -359, -2574))
    assert res != 0 and abs(res) == 39590739579959, res
    print(f"FAIL_NO_INTERTWINER  resultant(P,Q) = {res} != 0 reproduces the minted Bezout certificate "
          "39590739579959: shared numerator, NO common spectral structure — COR is the ceiling")

    print("HONEST_COR_NOT_THE  five registered consumer chains of one owned edge count; correlation row "
          "(COR, note-level tag in the D0-XI5-CROSS-SECTOR-001 sense); no intertwiner, no identification "
          "beyond the shared object, no EH promotion beyond the finite proxy; list not claimed exhaustive")
    print("PASS_EDGE_INVARIANT_CROSS_SECTOR")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
