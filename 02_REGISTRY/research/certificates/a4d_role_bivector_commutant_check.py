#!/usr/bin/env python3
"""Exact-rational Role-bivector Lorentz commutant certificate.

WRK-A4D-BIVECTOR-COMMUTANT-CERT

Finite linear algebra only.  Role order A,B,C,D with
eta = diag(1,-1,-1,-1) and ordered bivector basis
(AB, AC, AD, BC, BD, CD).

Positive:
  - six so(1,3) generators induce a 6x6 action rho2 on Lambda^2 V;
  - End_{so(1,3)}(Lambda^2 V) has exact rank 34 / nullity 2 (36-34=2);
  - nullspace basis I, J with J^2 = -I (Hodge-like);
  - spacelike odd Role swap B<->C preserves eta, has det -1;
  - adding its commutation constraint yields rank 35 / nullity 1 (36-35=1);
  - Ad_{rho2(B<->C)} J = -J, so the 1D survivor is span{I}.

Negative (reachable FAIL modes):
  - omit one boost from the three-boost set -> centralizer enlarges;
  - non-Lorentz shear fails the metric-preservation precheck;
  - mutate one entry of J -> fail commutation or J^2=-I;
  - testing only 1-2 generators is insufficient to certify the full commutant.

Scope: does NOT claim the odd Role swap is a mandatory physical symmetry,
does NOT call the 1D result a selected gravitational action, and does NOT
promote claim release status.  No continuum epsilon tensors.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import permutations
import sys


def zeros(n: int, m: int | None = None) -> list[list[Q]]:
    m = n if m is None else m
    return [[Q(0) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> list[list[Q]]:
    return [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]


def add(A: list[list[Q]], B: list[list[Q]]) -> list[list[Q]]:
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def scale(c: Q, A: list[list[Q]]) -> list[list[Q]]:
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def transpose(A: list[list[Q]]) -> list[list[Q]]:
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def mul(A: list[list[Q]], B: list[list[Q]]) -> list[list[Q]]:
    n, p, m = len(A), len(A[0]), len(B[0])
    C = zeros(n, m)
    for i in range(n):
        for j in range(m):
            C[i][j] = sum((A[i][k] * B[k][j] for k in range(p)), Q(0))
    return C


def mat_eq(A: list[list[Q]], B: list[list[Q]]) -> bool:
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A[0])))


def det4(M: list[list[Q]]) -> Q:
    total = Q(0)
    for perm in permutations(range(4)):
        sign = Q(1)
        for a in range(4):
            for b in range(a + 1, 4):
                if perm[a] > perm[b]:
                    sign = -sign
        prod = Q(1)
        for i in range(4):
            prod *= M[i][perm[i]]
        total += sign * prod
    return total


def fmt(M: list[list[Q]]) -> str:
    lines = []
    for row in M:
        lines.append("  [" + ", ".join(str(x) for x in row) + "]")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Fixed Role metric and bivector basis
# ---------------------------------------------------------------------------

ETA = [
    [Q(1), Q(0), Q(0), Q(0)],
    [Q(0), Q(-1), Q(0), Q(0)],
    [Q(0), Q(0), Q(-1), Q(0)],
    [Q(0), Q(0), Q(0), Q(-1)],
]

# Ordered bivector basis: AB, AC, AD, BC, BD, CD
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
PAIR_INDEX = {p: i for i, p in enumerate(PAIRS)}
BASIS_NAMES = ["AB", "AC", "AD", "BC", "BD", "CD"]


def eij(i: int, j: int, val: Q = Q(1)) -> list[list[Q]]:
    M = zeros(4)
    M[i][j] = val
    return M


def boost(space: int) -> list[list[Q]]:
    """Boost generator in the (A, space) plane; space in {B,C,D} = {1,2,3}."""
    return add(eij(0, space), eij(space, 0))


def rotation(i: int, j: int) -> list[list[Q]]:
    """Spatial rotation generator in the (i,j) plane."""
    return add(eij(i, j), scale(Q(-1), eij(j, i)))


def is_lorentz_tangent(X: list[list[Q]]) -> bool:
    """X^T eta + eta X = 0."""
    return mat_eq(add(mul(transpose(X), ETA), mul(ETA, X)), zeros(4))


def induced_rho2_lie(X: list[list[Q]]) -> list[list[Q]]:
    """Induced 6x6 Lie action of X on Lambda^2 V.

    rho2(X)(e_a ∧ e_b) = X e_a ∧ e_b + e_a ∧ X e_b.
    """
    R = zeros(6)
    for col, (a, b) in enumerate(PAIRS):
        coeffs = [Q(0)] * 6
        for c in range(4):
            xa = X[c][a]
            if xa != 0 and c != b:
                if c < b:
                    coeffs[PAIR_INDEX[(c, b)]] += xa
                else:
                    coeffs[PAIR_INDEX[(b, c)]] -= xa
            xb = X[c][b]
            if xb != 0 and a != c:
                if a < c:
                    coeffs[PAIR_INDEX[(a, c)]] += xb
                else:
                    coeffs[PAIR_INDEX[(c, a)]] -= xb
        for row in range(6):
            R[row][col] = coeffs[row]
    return R


def induced_rho2_group(P: list[list[Q]]) -> list[list[Q]]:
    """Induced 6x6 group action: rho2(P)(e_a ∧ e_b) = P e_a ∧ P e_b."""
    R = zeros(6)
    for col, (a, b) in enumerate(PAIRS):
        ia = next(c for c in range(4) if P[c][a] != 0)
        sa = P[ia][a]
        ib = next(c for c in range(4) if P[c][b] != 0)
        sb = P[ib][b]
        coeff = sa * sb
        if ia == ib:
            continue
        if ia < ib:
            R[PAIR_INDEX[(ia, ib)]][col] = coeff
        else:
            R[PAIR_INDEX[(ib, ia)]][col] = -coeff
    return R


def build_commutation_rows(actions: list[list[list[Q]]]) -> list[list[Q]]:
    """Rows of the linear system T A = A T for each 6x6 action A.

    Unknowns are the 36 entries of T in row-major order.
    """
    rows: list[list[Q]] = []
    for A in actions:
        for i in range(6):
            for j in range(6):
                row = [Q(0)] * 36
                for k in range(6):
                    row[i * 6 + k] += A[k][j]
                    row[k * 6 + j] -= A[i][k]
                rows.append(row)
    return rows


def rref_rank_nullspace(rows: list[list[Q]], n_vars: int) -> tuple[int, list[list[Q]]]:
    """Exact-rational Gaussian elimination to RREF; return (rank, nullspace)."""
    A = [row[:] for row in rows]
    m = len(A)
    pivots: list[int] = []
    r = 0
    for c in range(n_vars):
        piv = None
        for i in range(r, m):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        piv_val = A[r][c]
        A[r] = [x / piv_val for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                factor = A[i][c]
                A[i] = [A[i][j] - factor * A[r][j] for j in range(n_vars)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n_vars) if c not in pivots]
    basis: list[list[Q]] = []
    for f in free:
        v = [Q(0)] * n_vars
        v[f] = Q(1)
        for i, p in enumerate(pivots):
            v[p] = -A[i][f]
        basis.append(v)
    return r, basis


def vec_to_mat(v: list[Q]) -> list[list[Q]]:
    return [[v[i * 6 + j] for j in range(6)] for i in range(6)]


def commutes_all(T: list[list[Q]], actions: list[list[list[Q]]]) -> bool:
    return all(mat_eq(mul(T, A), mul(A, T)) for A in actions)


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

BOOSTS = [
    ("K_AB", boost(1)),
    ("K_AC", boost(2)),
    ("K_AD", boost(3)),
]
ROTATIONS = [
    ("R_BC", rotation(1, 2)),
    ("R_BD", rotation(1, 3)),
    ("R_CD", rotation(2, 3)),
]
GENERATORS = BOOSTS + ROTATIONS


def hodge_like_J() -> list[list[Q]]:
    """Hodge-like complex structure on the ordered bivector basis.

    Orientation A∧B∧C∧D with eta = diag(+---):
      J(AB)=CD, J(AC)=-BD, J(AD)=BC,
      J(BC)=-AD, J(BD)=AC, J(CD)=-AB.
    Satisfies J^2 = -I.
    """
    J = zeros(6)
    J[5][0] = Q(1)   # AB -> CD
    J[4][1] = Q(-1)  # AC -> -BD
    J[3][2] = Q(1)   # AD -> BC
    J[2][3] = Q(-1)  # BC -> -AD
    J[1][4] = Q(1)   # BD -> AC
    J[0][5] = Q(-1)  # CD -> -AB
    return J


def odd_role_swap_BC() -> list[list[Q]]:
    """Spacelike odd Role swap B <-> C (indices 1 <-> 2)."""
    P = eye(4)
    P[1][1] = Q(0)
    P[2][2] = Q(0)
    P[1][2] = Q(1)
    P[2][1] = Q(1)
    return P


# ---------------------------------------------------------------------------
# Positive checks
# ---------------------------------------------------------------------------

def positive_checks() -> tuple[list[list[Q]], list[list[Q]], list[list[Q]]]:
    print("STRUCTURE_FIXED_BEFORE_NUMBER:")
    print("  Role order A,B,C,D; eta=diag(1,-1,-1,-1)")
    print("  bivector basis (AB,AC,AD,BC,BD,CD)")

    for name, X in GENERATORS:
        if not is_lorentz_tangent(X):
            raise AssertionError(f"FAIL metric-preservation for {name}")
    print("PASS all 6 generators satisfy X^T eta + eta X = 0")

    actions = [induced_rho2_lie(X) for _, X in GENERATORS]
    print("PASS induced 6x6 rho2 actions built for 3 boosts + 3 rotations")

    rows = build_commutation_rows(actions)
    rank, nullspace = rref_rank_nullspace(rows, 36)
    if rank != 34 or len(nullspace) != 2:
        raise AssertionError(f"FAIL expected rank 34 nullity 2, got {rank}/{len(nullspace)}")
    print("PASS 36-34=2: exact system rank 34, nullity 2")

    I6 = eye(6)
    J = hodge_like_J()
    if not mat_eq(mul(J, J), scale(Q(-1), I6)):
        raise AssertionError("FAIL J^2 != -I")
    if not commutes_all(I6, actions):
        raise AssertionError("FAIL I does not commute with all rho2 generators")
    if not commutes_all(J, actions):
        raise AssertionError("FAIL J does not commute with all rho2 generators")

    # Nullspace must be exactly span{I, J}.
    mats = [vec_to_mat(v) for v in nullspace]
    found_I = any(mat_eq(M, I6) for M in mats)
    found_J = any(mat_eq(M, J) or mat_eq(M, scale(Q(-1), J)) for M in mats)
    if not found_I or not found_J:
        # Accept any basis that spans the same plane.
        # Reconstruct: every null vector must be a I + b J.
        for M in mats:
            # M = a I + b J  =>  diagonal entries give a; off-diag pattern gives b.
            a = M[0][0]
            # J has zero diagonal; check residual is multiple of J.
            residual = add(M, scale(-a, I6))
            if residual[5][0] == 0 and not mat_eq(residual, zeros(6)):
                raise AssertionError("FAIL nullspace vector not in span{I,J}")
            if residual[5][0] != 0:
                b = residual[5][0]
                if not mat_eq(residual, scale(b, J)):
                    raise AssertionError("FAIL nullspace vector not in span{I,J}")
            elif not mat_eq(residual, zeros(6)):
                raise AssertionError("FAIL nullspace residual not zero")
        found_I = True
        found_J = True
    if not (found_I and found_J):
        raise AssertionError("FAIL nullspace is not span{I,J}")
    print("PASS nullspace basis I,J with J^2=-I")

    P = odd_role_swap_BC()
    if not mat_eq(mul(mul(transpose(P), ETA), P), ETA):
        raise AssertionError("FAIL B<->C does not preserve eta")
    if det4(P) != Q(-1):
        raise AssertionError(f"FAIL det(B<->C) = {det4(P)}, expected -1")
    print("PASS spacelike odd Role swap B<->C preserves eta and has det=-1")

    rho_P = induced_rho2_group(P)
    # P^2 = I => rho2(P)^2 = I, so inverse is itself.
    if not mat_eq(mul(rho_P, rho_P), I6):
        raise AssertionError("FAIL rho2(B<->C)^2 != I")

    rows_aug = build_commutation_rows(actions + [rho_P])
    rank_aug, null_aug = rref_rank_nullspace(rows_aug, 36)
    if rank_aug != 35 or len(null_aug) != 1:
        raise AssertionError(
            f"FAIL expected rank 35 nullity 1 after odd swap, got {rank_aug}/{len(null_aug)}"
        )
    survivor = vec_to_mat(null_aug[0])
    if not mat_eq(survivor, I6):
        # Allow nonzero scale.
        if survivor[0][0] == 0 or not mat_eq(survivor, scale(survivor[0][0], I6)):
            raise AssertionError("FAIL 1D survivor is not span{I}")
    print("PASS 36-35=1: after odd Role swap, exact rank 35, nullity 1")

    conj = mul(rho_P, mul(J, rho_P))  # rho_P^{-1} = rho_P
    if not mat_eq(conj, scale(Q(-1), J)):
        raise AssertionError("FAIL Ad_{rho2(B<->C)} J != -J")
    print("PASS rho2(B<->C) J rho2(B<->C)^{-1} = -J")

    print("BASIS_I:")
    print(fmt(I6))
    print("BASIS_J:")
    print(fmt(J))
    print("SURVIVOR_AFTER_ODD_SWAP (span{I}; reduction CONDITIONAL on odd Role swap):")
    print(fmt(I6))
    print("CAVEAT: odd Role swap is an algebraic selector, not claimed as mandatory physical symmetry")
    print("CAVEAT: 1D survivor is not a selected gravitational action")

    return I6, J, rho_P


# ---------------------------------------------------------------------------
# Negative controls
# ---------------------------------------------------------------------------

def negative_controls(I6: list[list[Q]], J: list[list[Q]]) -> None:
    # 1. Omit one boost from the three-boost set -> centralizer enlarges.
    boost_actions = [induced_rho2_lie(X) for _, X in BOOSTS]
    rank3, null3 = rref_rank_nullspace(build_commutation_rows(boost_actions), 36)
    if rank3 != 34 or len(null3) != 2:
        raise AssertionError(
            f"precondition FAIL: three boosts alone should give nullity 2, got {len(null3)}"
        )
    two_boost_actions = boost_actions[:2]  # omit K_AD
    rank2, null2 = rref_rank_nullspace(build_commutation_rows(two_boost_actions), 36)
    if len(null2) <= len(null3):
        raise AssertionError(
            f"FAIL expected enlarged centralizer after omitting one boost, "
            f"got nullity {len(null2)} (was {len(null3)})"
        )
    print(
        f"PASS NEG omit-one-boost: 3-boost nullity={len(null3)} -> "
        f"2-boost nullity={len(null2)} (enlarged)"
    )

    # 2. Non-Lorentz shear fails metric-preservation precheck.
    shear = zeros(4)
    shear[0][1] = Q(1)  # pure upper-triangular shear, not a Lorentz tangent
    if is_lorentz_tangent(shear):
        raise AssertionError("FAIL shear unexpectedly passed Lorentz precheck")
    print("PASS NEG non-Lorentz shear fails X^T eta + eta X = 0 precheck")

    # 3. Mutate one entry of J -> fail commutation or J^2=-I.
    J_bad = [row[:] for row in J]
    J_bad[0][0] = Q(1)  # destroy the zero diagonal / Hodge pattern
    sq_ok = mat_eq(mul(J_bad, J_bad), scale(Q(-1), I6))
    full_actions = [induced_rho2_lie(X) for _, X in GENERATORS]
    comm_ok = commutes_all(J_bad, full_actions)
    if sq_ok and comm_ok:
        raise AssertionError("FAIL mutated J still satisfies both J^2=-I and commutation")
    print(
        f"PASS NEG mutate-J: J^2=-I? {sq_ok}; commutes-all? {comm_ok} "
        f"(at least one fails)"
    )

    # 4. Testing only 1-2 generators is insufficient to certify the full commutant.
    one = [induced_rho2_lie(BOOSTS[0][1])]
    two = [induced_rho2_lie(BOOSTS[0][1]), induced_rho2_lie(BOOSTS[1][1])]
    _, null_one = rref_rank_nullspace(build_commutation_rows(one), 36)
    _, null_two = rref_rank_nullspace(build_commutation_rows(two), 36)
    if len(null_one) <= 2 or len(null_two) <= 2:
        raise AssertionError(
            f"FAIL expected >2 nullity for 1-2 generators, got "
            f"{len(null_one)}, {len(null_two)}"
        )
    print(
        f"PASS NEG insufficient-generators: 1-gen nullity={len(null_one)}, "
        f"2-gen nullity={len(null_two)} (both > 2; cannot certify full commutant)"
    )


def main() -> int:
    I6, J, _rho_P = positive_checks()
    negative_controls(I6, J)
    print("TERMINAL ROLE-BIVECTOR-COMMUTANT-CERTIFIED")
    print("  36-34=2 (Lorentz commutant)")
    print("  36-35=1 (CONDITIONAL on odd Role swap B<->C)")
    print("  J^2=-I (Hodge-like complex structure)")
    print("  reduction to 1D is CONDITIONAL, not a physical-action selection")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        sys.exit(1)
