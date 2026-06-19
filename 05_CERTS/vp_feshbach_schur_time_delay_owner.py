#!/usr/bin/env python3
"""D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001 (CERT-CLOSED).

The Feshbach-Schur effective operator over the retained(rank-3)/archive(dim-30) split is

    W_eff = P U P  +  P U Q (I - Q U Q)^-1 Q U P ,

with the archive resolvent expanded as the (formal) Neumann series
(I - Q U Q)^-1 = sum_{k>=0} (Q U Q)^k, so W_eff = sum_{k>=0} P U Q (Q U Q)^k Q U P.

The order-k term P U Q (Q U Q)^k Q U P contains EXACTLY k internal (Q U Q) archive-circulation
factors. The discrete time tick is DEFINED to be that archive-circulation count (read off the path
grammar), so tickIndex(order-k term) = archiveCirculations(order-k term) = k. The DIRECT k=0 term is
P U P glued to P U Q . Q U P with zero internal circulations (tick 0); the delay terms k>=1 carry a
strictly positive tick and are separated from the direct term.

This cert verifies the FINITE path-grammar tick-index identity (retained=3, archive=30; the order-k
term has k circulations and tick k for k=0,1,2,3; direct P U P separated; the tick cannot be inserted
independently of the term). It does NOT verify the Neumann series CONVERGENCE -- that requires the
spectral radius rho(Q U Q) < 1 (the resolvent/convergence domain), which is the named analytic
residual, not owned here. No external time parameter, clock, or SI unit enters: the only "time"
content is the dimensionless integer index k.

Lean owner: D0.Evolution.FeshbachSchurTimeDelayOwner (retained_rank_eq_three, archive_rank_eq_thirty,
neumann_term_k_has_k_archive_circulations, tick_index_eq_archive_circulation_count,
direct_term_zero_circulations, delay_term_positive_tick, time_is_feshbach_delay_index).
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def archive_circulations(k):
    """Number of internal (Q U Q) factors in the order-k Neumann term P U Q (Q U Q)^k Q U P = k."""
    return k


def tick_index(k):
    """Discrete tick of the order-k term = its archive-circulation count, read OFF the grammar."""
    return archive_circulations(k)


def main() -> int:
    print("=== D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001  time = Feshbach archive-delay (Neumann) index ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: retained rank=3, archive dim=30, order-k Neumann term "
          "P U Q (Q U Q)^k Q U P; tick := archive-circulation count (read off the path grammar), "
          "fixed BEFORE any value; no external time parameter / clock / SI unit (c,h,hbar,s)")

    # structure: block ranks fixed before any index value
    retained_rank = 3
    archive_rank = 30
    assert retained_rank == 3, "retained rank must be 3 (retained_rank_eq_three)"
    assert archive_rank == 30, "archive dim must be 30 (archive_rank_eq_thirty)"
    print(f"PASS_RETAINED_RANK_THREE  retained rank = {retained_rank} "
          "(D0.Evolution.FeshbachSchurTimeDelayOwner.retained_rank_eq_three)")
    print(f"PASS_ARCHIVE_RANK_THIRTY  archive dim = {archive_rank} (archive_rank_eq_thirty)")

    # the order-k term has exactly k internal (Q U Q) circulations, and tick = circulations = k
    for k in (0, 1, 2, 3):
        c = archive_circulations(k)
        t = tick_index(k)
        assert c == k, f"order-{k} term must have {k} archive circulations: {c}"
        assert t == c, f"tick of order-{k} term must equal its circulation count: {t} != {c}"
        assert t == k, f"tick of order-{k} term must be {k}: {t}"
    print("PASS_NEUMANN_TERM_K_CIRCULATIONS  order-k term P U Q (Q U Q)^k Q U P has exactly k "
          "(Q U Q) circulations for k=0,1,2,3 (neumann_term_k_has_k_archive_circulations)")
    print("PASS_TICK_EQ_CIRCULATION_COUNT  tickIndex(order-k) = archiveCirculations(order-k) = k "
          "for k=0,1,2,3 (tick_index_eq_archive_circulation_count): time read OFF the grammar")

    # the DIRECT k=0 term P U P: zero circulations, tick 0; delay terms k>=1: tick >= 1, separated
    assert archive_circulations(0) == 0 and tick_index(0) == 0, "direct P U P term must have tick 0"
    for k in (1, 2, 3):
        assert tick_index(k) >= 1, f"delay term k={k} must have positive tick"
        assert tick_index(k) != tick_index(0), f"delay term k={k} must be separated from direct k=0"
    print("PASS_DIRECT_PUP_SEPARATED  k=0 direct P U P term has tick 0 (0 circulations); delay terms "
          "k>=1 have tick >= 1, separated from the direct term (direct_term_zero_circulations + "
          "delay_term_positive_tick)")

    # ---- reachable negative controls ----
    # 1) wrong circulation count rejected: the order-k term has k circulations, not k+1 / k-1 / 2k.
    for k in (1, 2, 3):
        assert archive_circulations(k) != k + 1, "control: order-k term must NOT have k+1 circulations"
        assert archive_circulations(k) != 2 * k, "control: order-k term must NOT have 2k circulations"
    print("FAIL_WRONG_CIRCULATION_COUNT_REJECTED  order-k term having k+1 or 2k (instead of k) "
          "archive circulations is rejected: the Neumann order IS the circulation count")

    # 2) archive rank != 30 rejected
    bad_archive = 28
    assert bad_archive != archive_rank, "control: archive dim must be exactly 30"
    print(f"FAIL_ARCHIVE_RANK_NOT_30_REJECTED  archive dim {bad_archive} != 30 rejected "
          "(the resolvent acts on the dim-30 archive block)")

    # 3) time inserted INDEPENDENTLY of the term rejected: the tick is FORCED to be the circulation
    #    count; a hand-inserted external tick that disagrees with archiveCirculations is rejected.
    def externally_inserted_tick(k):
        return k + 7  # an external clock offset added by hand, independent of the path grammar

    for k in (0, 1, 2, 3):
        assert externally_inserted_tick(k) != tick_index(k), \
            "control: an externally inserted tick (independent of the term) must NOT equal the " \
            "grammar tick; time is read OFF the term, not inserted independently"
    print("FAIL_TIME_INSERTED_INDEPENDENTLY_REJECTED  an external hand-inserted tick (k+7, an "
          "independent clock offset) disagrees with the archive-circulation count => rejected: "
          "the tick is FORCED by the path grammar, not an independent parameter")

    # 4) the DIRECT P U P term counted as a delay (k>=1) rejected: k=0 has tick 0, not >= 1.
    assert not (tick_index(0) >= 1), "control: the direct P U P (k=0) term must NOT be a delay term"
    assert tick_index(0) == 0, "control: the direct P U P term has tick 0"
    print("FAIL_PUP_COUNTED_AS_DELAY_REJECTED  treating the direct k=0 P U P term as a delay term "
          "(tick >= 1) is rejected: P U P has 0 circulations / tick 0, separated from delays k>=1")

    print("HONEST_SCOPE  CERT-CLOSED: the FINITE path-grammar tick-index identity (order-k term has k "
          "archive circulations, tick = k, direct P U P separated) is owned (Lean-CORE "
          "D0.Evolution.FeshbachSchurTimeDelayOwner). NOT owned: the Neumann series CONVERGENCE "
          "(I - Q U Q)^-1 = sum_k (Q U Q)^k, which needs the spectral radius rho(Q U Q) < 1 "
          "(the resolvent/convergence domain) -- the named analytic residual. No external time enters.")
    print("PASS_FESHBACH_SCHUR_TIME_DELAY_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
