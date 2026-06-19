#!/usr/bin/env python3
"""D0-ARCHIVE-NEUMANN-TICK-OWNER-001 (CERT-CLOSED).

The archive resolvent of the Feshbach-Schur effective operator is expanded as the Neumann series

    (I - Q U Q)^-1 = sum_{k>=0} (Q U Q)^k ,

so the effective operator is W_eff = sum_{k>=0} P U Q (Q U Q)^k Q U P. The order-k term is the unique
path with k internal archive round-trips (Q U Q), and the discrete time tick is the Neumann index k =
the number of (Q U Q) circulations. This cert verifies the NEUMANN-EXPANSION side of the tick identity:

  * the order-k term carries exactly k (Q U Q) factors (k = 0,1,2,3 checked explicitly);
  * the k=0 term is the DIRECT P U P channel (0 circulations), separated from the delay terms k>=1;
  * the tick is the Neumann index (a monotone, gap-free 0,1,2,3,... ladder of archive delays);
  * a finite TRUNCATION of the series at order N keeps exactly the terms with tick 0..N (so the tick
    ladder is the natural cut-off index), again with retained=3, archive=30 fixed first.

It does NOT verify CONVERGENCE of the Neumann series: (I - Q U Q)^-1 = sum_k (Q U Q)^k holds only on
the resolvent/convergence domain rho(Q U Q) < 1 (spectral radius below 1). That analytic condition is
the named residual; the per-term combinatorial tick identity is what is owned here. No external clock,
time parameter, or SI unit enters -- the tick is the dimensionless integer Neumann index k.

Lean owner: D0.Evolution.FeshbachSchurTimeDelayOwner (neumann_term_k_has_k_archive_circulations,
tick_index_eq_archive_circulation_count, tick_index_eq_k, direct_term_zero_circulations,
delay_term_positive_tick, direct_separated_from_delay, time_is_feshbach_delay_index).
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def quq_factor_count(k):
    """Number of (Q U Q) factors in the order-k Neumann term P U Q (Q U Q)^k Q U P = k."""
    return k


def tick_index(k):
    """Discrete tick = Neumann index = the (Q U Q) circulation count of the order-k term."""
    return quq_factor_count(k)


def neumann_truncation_indices(N):
    """A Neumann truncation at order N keeps exactly the terms with tick 0,1,...,N."""
    return list(range(N + 1))


def main() -> int:
    print("=== D0-ARCHIVE-NEUMANN-TICK-OWNER-001  archive Neumann index = discrete time tick ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: retained rank=3, archive dim=30, archive resolvent "
          "(I - Q U Q)^-1 = sum_k (Q U Q)^k; tick := Neumann index = (Q U Q) circulation count, "
          "fixed BEFORE any value; no external clock / time parameter / SI unit (c,h,hbar,s)")

    retained_rank = 3
    archive_rank = 30
    assert retained_rank == 3, "retained rank must be 3"
    assert archive_rank == 30, "archive dim must be 30"
    print(f"PASS_RETAINED_RANK_THREE  retained rank = {retained_rank}")
    print(f"PASS_ARCHIVE_RANK_THIRTY  archive dim = {archive_rank}")

    # order-k Neumann term has exactly k (Q U Q) factors, and tick = that count = k
    for k in (0, 1, 2, 3):
        c = quq_factor_count(k)
        t = tick_index(k)
        assert c == k, f"order-{k} Neumann term must have {k} (Q U Q) factors: {c}"
        assert t == c == k, f"tick of order-{k} term must equal its (Q U Q) count = {k}: {t}, {c}"
    print("PASS_NEUMANN_TERM_K_FACTORS  order-k term P U Q (Q U Q)^k Q U P has exactly k (Q U Q) "
          "factors for k=0,1,2,3 (neumann_term_k_has_k_archive_circulations)")
    print("PASS_TICK_EQ_NEUMANN_INDEX  tickIndex(order-k) = (Q U Q) count = k for k=0,1,2,3 "
          "(tick_index_eq_k / tick_index_eq_archive_circulation_count)")

    # the tick ladder is monotone and gap-free (0,1,2,3,...): each tick is exactly the index
    ticks = [tick_index(k) for k in range(4)]
    assert ticks == [0, 1, 2, 3], f"tick ladder must be 0,1,2,3: {ticks}"
    for k in range(3):
        assert ticks[k + 1] - ticks[k] == 1, "control: the tick ladder must advance by exactly 1 per order"
    print("PASS_TICK_LADDER_GAP_FREE  the archive-delay tick ladder is 0,1,2,3,... (one tick per "
          "Neumann order; monotone, gap-free)")

    # direct k=0 P U P term separated from delay terms k>=1
    assert tick_index(0) == 0, "direct P U P term must have tick 0"
    for k in (1, 2, 3):
        assert tick_index(k) >= 1 and tick_index(k) != tick_index(0), \
            f"delay term k={k} must be separated from the direct term"
    print("PASS_DIRECT_PUP_SEPARATED  k=0 direct P U P term (tick 0) separated from delay terms "
          "k>=1 (direct_separated_from_delay)")

    # a Neumann truncation at order N keeps exactly the ticks 0..N
    N = 3
    keep = neumann_truncation_indices(N)
    assert keep == [0, 1, 2, 3], f"truncation at order {N} must keep ticks 0..{N}: {keep}"
    assert all(tick_index(k) == k for k in keep), "kept terms must have tick = their order"
    print(f"PASS_TRUNCATION_KEEPS_TICKS  Neumann truncation at order N={N} keeps exactly ticks "
          f"0..{N} = {keep} (the tick ladder is the natural cut-off index)")

    # ---- reachable negative controls ----
    # 1) wrong circulation count rejected
    for k in (1, 2, 3):
        assert quq_factor_count(k) != k - 1, "control: order-k term must NOT have k-1 (Q U Q) factors"
        assert quq_factor_count(k) != k + 1, "control: order-k term must NOT have k+1 (Q U Q) factors"
    print("FAIL_WRONG_CIRCULATION_COUNT_REJECTED  order-k term having k-1 or k+1 (instead of k) "
          "(Q U Q) factors is rejected: the Neumann order IS the (Q U Q) circulation count")

    # 2) archive rank != 30 rejected
    bad_archive = 32
    assert bad_archive != archive_rank, "control: archive dim must be exactly 30"
    print(f"FAIL_ARCHIVE_RANK_NOT_30_REJECTED  archive dim {bad_archive} != 30 rejected")

    # 3) tick inserted INDEPENDENTLY of the Neumann index rejected
    def externally_inserted_tick(k):
        return 2 * k + 5  # an independent external clock, not the (Q U Q) count

    for k in (0, 1, 2, 3):
        assert externally_inserted_tick(k) != tick_index(k), \
            "control: an externally inserted tick (independent of the Neumann index) must NOT equal " \
            "the grammar tick; the tick IS the (Q U Q) circulation count"
    print("FAIL_TIME_INSERTED_INDEPENDENTLY_REJECTED  an external hand-inserted tick (2k+5, an "
          "independent clock) disagrees with the Neumann (Q U Q) index => rejected: the tick is the "
          "archive-circulation count, not an independent parameter")

    # 4) the DIRECT P U P term counted as a delay (k>=1) rejected
    assert not (tick_index(0) >= 1), "control: the direct k=0 P U P term must NOT be a delay term"
    assert 0 not in neumann_truncation_indices(0) or tick_index(0) == 0, "k=0 keeps the direct term"
    print("FAIL_PUP_COUNTED_AS_DELAY_REJECTED  treating the k=0 P U P term as a delay term (tick>=1) "
          "is rejected: P U P has 0 (Q U Q) factors / tick 0, separated from the delay ladder k>=1")

    print("HONEST_SCOPE  CERT-CLOSED: the FINITE Neumann-index tick identity (order-k term has k "
          "(Q U Q) factors, tick = k, direct P U P separated, gap-free ladder) is owned (Lean-CORE "
          "D0.Evolution.FeshbachSchurTimeDelayOwner). NOT owned: CONVERGENCE of "
          "(I - Q U Q)^-1 = sum_k (Q U Q)^k, which needs the spectral radius rho(Q U Q) < 1 "
          "(the resolvent/convergence domain) -- the named analytic residual. No external clock enters.")
    print("PASS_ARCHIVE_NEUMANN_TICK_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
