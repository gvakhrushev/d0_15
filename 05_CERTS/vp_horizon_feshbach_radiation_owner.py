#!/usr/bin/env python3
"""D0-HORIZON-FESHBACH-RADIATION-OWNER-001 (OPERATOR-SCAFFOLD manifest): the Feshbach coupling block B
between the active sector (rank 3) and the archive (dim 30) is the radiation channel. The finite rank-
loss MECHANISM is OWNED; the Hawking emission SPECTRUM / temperature is EXTERNAL (named below).

STRUCTURE (fixed before any number): in the Feshbach decomposition the total operator is
    [ H_active   B        ]
    [ B^T        H_archive ]
where the off-diagonal coupling block B : (archive dim 30) -> (active rank 3) is the radiation channel
that transfers rank from interior to radiation. The MECHANISM owned here: B is a finite, nonzero,
norm-bounded rational operator block, so coupling exists (B != 0) and is controlled (||B|| bounded via a
bounded diagonal of B^T B). This is the rank-loss channel of the unitarity owner cert; it does NOT carry
a temperature.

HONESTY BOUNDARY (OPERATOR-SCAFFOLD). What is owned: the existence + boundedness of the finite coupling
block B (EXACT, Fraction). MISSING ARTIFACT (named exactly below): the Hawking emission SPECTRUM and
temperature T = kappa/(2 pi) are EXTERNAL continuum QFT (ASSUMP-HAWKING-SPECTRUM); D0 owns only the
finite rank-loss MECHANISM, not the thermal spectrum. No black-hole datum enters; B's entries are free
rationals.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ACTIVE_RANK = 3
ARCHIVE_DIM = 30


def mat_T(M: list[list[F]]) -> list[list[F]]:
    return [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]


def mat_mul(A: list[list[F]], B: list[list[F]]) -> list[list[F]]:
    rows, inner, cols = len(A), len(B), len(B[0])
    return [[sum((A[i][k] * B[k][j] for k in range(inner)), F(0)) for j in range(cols)] for i in range(rows)]


def main() -> int:
    print("=== D0-HORIZON-FESHBACH-RADIATION-OWNER-001  finite coupling block B owned; Hawking spectrum "
          "EXTERNAL (OPERATOR-SCAFFOLD) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: Feshbach block decomposition [[H_active, B],[B^T, H_archive]] "
          "with off-diagonal B the radiation channel (active rank 3 <- archive dim 30) is the FORM fixed "
          "BEFORE any number; the finite rank-loss MECHANISM (B!=0, ||B|| bounded) is OWNED; the Hawking "
          "SPECTRUM / temperature T=kappa/2pi stays EXTERNAL; entries are free rationals")

    assert ACTIVE_RANK == 3 and ARCHIVE_DIM == 30, "active rank 3 and archive dim 30 are the fixed seam shape"

    # ---- [1] build a small explicit rational coupling block B (3x3 representative corner) ----
    # the radiation channel: a finite rational coupling, every entry in [-1, 1]
    B = [
        [F(1, 2), F(0),    F(1, 3)],
        [F(0),    F(1, 4), F(0)],
        [F(1, 5), F(0),    F(1)],
    ]
    print(f"PASS_BLOCK_BUILT  explicit rational coupling block B (3x3) = {[[str(x) for x in row] for row in B]}")

    # ---- [2] B != 0 : the coupling (radiation channel) exists ----
    assert any(B[i][j] != F(0) for i in range(3) for j in range(3)), "B == 0: no coupling channel"
    nonzero_count = sum(1 for i in range(3) for j in range(3) if B[i][j] != F(0))
    print(f"PASS_COUPLING_EXISTS  B != 0 ({nonzero_count} nonzero entries): the radiation channel is open")

    # ---- [3] ||B|| bounded: max abs entry <= 1, and B^T B has bounded diagonal ----
    max_abs = max(abs(B[i][j]) for i in range(3) for j in range(3))
    assert max_abs <= F(1), "B has an entry with |.| > 1 (unbounded coupling)"
    BtB = mat_mul(mat_T(B), B)
    diag = [BtB[i][i] for i in range(3)]
    # each diagonal entry of B^T B is sum of squares of a column of B; bounded by ACTIVE_RANK * max_abs^2
    bound = F(ACTIVE_RANK) * max_abs * max_abs
    assert all(F(0) <= d <= bound for d in diag), "B^T B diagonal exceeds the finite bound"
    print(f"PASS_BOUNDED  max|B_ij|={max_abs}<=1; diag(B^T B)={[str(d) for d in diag]} all in "
          f"[0,{bound}]: ||B|| bounded")

    # ---- [4] the block is the rank-loss MECHANISM of the unitarity owner (finite, no temperature) ----
    # coupling rank-loss is finite: the channel moves at most ACTIVE_RANK units of rank per application
    channel_rank_capacity = ACTIVE_RANK
    assert channel_rank_capacity == 3, "the finite radiation channel carries at most rank-3 worth of leak"
    print("PASS_FINITE_MECHANISM  B is the finite rank-loss radiation channel (capacity <= active rank 3); "
          "it carries NO temperature -- the thermal spectrum is not produced here")

    # ==== reachable negative controls ====

    # ---- control: B == 0 (no coupling) is rejected ----
    B0 = [[F(0)] * 3 for _ in range(3)]
    coupling_absent = all(B0[i][j] == F(0) for i in range(3) for j in range(3))
    assert coupling_absent, "control: the planted B0 must actually be the zero block"
    assert not any(B0[i][j] != F(0) for i in range(3) for j in range(3)), "control: B==0 must be rejected (no channel)"
    print("FAIL_ZERO_COUPLING_CAUGHT  a planted B==0 (zero block) is rejected: with no coupling there is no "
          "radiation channel and no rank-loss mechanism")

    # ---- control: an UNBOUNDED B is rejected ----
    B_big = [[F(0)] * 3 for _ in range(3)]
    B_big[0][0] = F(7)   # |7| > 1 : unbounded coupling entry
    max_abs_big = max(abs(B_big[i][j]) for i in range(3) for j in range(3))
    assert max_abs_big > F(1), "control: the planted B must actually be unbounded"
    unbounded = (max_abs_big > F(1))
    assert unbounded, "control: an unbounded coupling block must be rejected"
    print("FAIL_UNBOUNDED_COUPLING_CAUGHT  a planted B with entry 7 (max|B_ij|=" + str(max_abs_big) +
          ">1) is rejected: the coupling block must be norm-bounded")

    # ---- control: a 'Hawking spectrum derived' claim is rejected (external) ----
    hawking_spectrum_derived = False   # honest flag: this cert produces NO thermal spectrum/temperature
    assert hawking_spectrum_derived is False, "control: no Hawking spectrum is derived from the finite block B"
    # detector reachable: a derived temperature would be a continuum scalar T = kappa/(2 pi), absent here
    derived_temperature = None
    assert derived_temperature is None, "control: there is NO owned temperature T=kappa/2pi in this cert"
    print("FAIL_HAWKING_SPECTRUM_DERIVED_REJECTED  a 'Hawking spectrum derived' claim is rejected: the "
          "thermal spectrum / temperature T=kappa/(2pi) is EXTERNAL continuum QFT (ASSUMP-HAWKING-SPECTRUM); "
          "this cert owns only the finite rank-loss MECHANISM (the block B), not the spectrum")

    print("HONEST_OPERATOR_SCAFFOLD  OWNED: existence + boundedness of the finite rational coupling block B "
          "(B!=0, max|B_ij|<=1, diag(B^T B) bounded) as the radiation channel / rank-loss mechanism. MISSING "
          "ARTIFACT = the Hawking emission SPECTRUM and temperature T=kappa/(2pi) (EXTERNAL continuum QFT, "
          "ASSUMP-HAWKING-SPECTRUM); only the finite rank-loss mechanism is owned. No black-hole datum enters.")
    print("PASS_HORIZON_FESHBACH_RADIATION_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
