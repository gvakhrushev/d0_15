#!/usr/bin/env python3
"""D0-PAGE-TURNING-POINT-RANK-THEOREM-001 (CERT-CLOSED): the Page rank turning point, EXACT (can FAIL).

Owner of D0.Gravity.PageTurningPointRank (Lean, built): rankSupport D a = Nat.min a (D - a);
min_le_page_turn (a<=D -> rankSupport D a <= rankSupport D (D/2)); page_turn_value
(rankSupport D (D/2) = D/2); page_turning_point_owner (D/2 is argmax AND max value).

STRUCTURE (fixed before any number): a D-dimensional finite split carries two integer ranks
(rank P, rank Q) with rank P = a, rank Q = D - a, and the rank-entropy SUPPORT that bounds the
active-sector entropy is the purely combinatorial Nat quantity
    f(a) = min(a, D - a) ,    a in 0..D .
This FORM is fixed BEFORE any number. The Page turn is the claim that f is MAXIMAL exactly at the
balanced split a = D//2, where it equals D//2 (rank P = rank Q). The integer-floor convention makes
this hold for odd D too: D//2 is the smaller half, so min(D//2, D-D//2) = D//2.

HONESTY BOUNDARY. What is owned here (CERT-CLOSED): the finite Nat-extremum facts -- argmax = D//2,
peak value = D//2, the single-peak rise/fall shape, swap symmetry f(a)=f(D-a) -- all EXACT integer
arithmetic, no continuum. What stays EXTERNAL: the analytic von Neumann entropy S(rho)=-Tr(rho log rho)
that this integer support bounds; no continuum object enters. D and a are free finite Nat inputs.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def rank_support(a: int, D: int) -> int:
    """The rank-entropy support f(a) = min(a, D - a) (exact integer)."""
    return min(a, D - a)


def argmax_and_value(D: int):
    """Return (set of argmax indices, max value) of f over a = 0..D (exact integer sweep)."""
    curve = [rank_support(a, D) for a in range(0, D + 1)]
    mx = max(curve)
    argmax = {a for a in range(0, D + 1) if curve[a] == mx}
    return argmax, mx, curve


def main() -> int:
    print("=== D0-PAGE-TURNING-POINT-RANK-THEOREM-001  Page turn argmax/value of min(a,D-a) "
          "(CERT-CLOSED, exact) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: D-dim split with ranks (rank P=a, rank Q=D-a); rank-entropy "
          "support f(a)=min(a,D-a) over a=0..D is the FORM fixed BEFORE any number; the Page turn = f "
          "maximal at the balanced split a=D//2 with value D//2; analytic von Neumann entropy stays "
          "EXTERNAL; D,a are finite Nat")

    cases = [8, 33]   # one even (D//2 exact), one odd (D//2 is the smaller floor-half)
    expected_peak = {8: 4, 33: 16}

    for D in cases:
        argmax, mx, curve = argmax_and_value(D)
        turn = D // 2

        # ---- [1] the maximum value equals D//2 ----
        assert mx == turn, f"max f over a=0..{D} must equal D//2={turn}, got {mx}"
        assert mx == expected_peak[D], f"peak for D={D} must be {expected_peak[D]}, got {mx}"
        print(f"PASS_PEAK_VALUE_D{D}  max_a min(a,{D}-a) = D//2 = {turn} (= {expected_peak[D]})")

        # ---- [2] the argmax is achieved at a = D//2 (turn point is a maximizer) ----
        assert turn in argmax, f"the balanced split a=D//2={turn} must be an argmax of f"
        print(f"PASS_ARGMAX_AT_TURN_D{D}  a=D//2={turn} attains the max; argmax set = {sorted(argmax)}")

        # ---- [3] balanced split: f(D//2) = min(D//2, D-D//2) = D//2 exactly ----
        assert rank_support(turn, D) == turn, f"f(D//2) must equal D//2={turn} for D={D}"
        assert min(turn, D - turn) == turn, "D//2 is the smaller (floor) half so the min is D//2"
        print(f"PASS_BALANCED_VALUE_D{D}  f(D//2)=min({turn},{D - turn})={turn} (rank P=rank Q at the turn)")

        # ---- [4] single peak: f RISES (non-strictly) to the turn then FALLS, with a strict net climb ----
        rising = all(curve[i] <= curve[i + 1] for i in range(0, turn))
        falling = all(curve[i] >= curve[i + 1] for i in range(turn, D))
        assert rising, f"f must be non-decreasing up to the turn for D={D}"
        assert falling, f"f must be non-increasing after the turn for D={D}"
        assert curve[0] < curve[turn] and curve[turn] > curve[D], \
            f"f must strictly peak at the turn for D={D} (genuine single peak, not flat)"
        print(f"PASS_SINGLE_PEAK_D{D}  f rises to a={turn} (peak {mx}) then falls; strict net climb "
              f"from endpoints")

        # ---- [5] swap symmetry f(a) = f(D-a) over the full sweep ----
        assert all(rank_support(a, D) == rank_support(D - a, D) for a in range(0, D + 1)), \
            f"f must be symmetric under a<->D-a for D={D}"
        print(f"PASS_SWAP_SYMMETRY_D{D}  f(a)=f(D-a) over a=0..{D} (rank P <-> rank Q)")

    # ==== reachable negative controls (planted WRONG claims are rejected) ====

    D = 8
    argmax8, mx8, curve8 = argmax_and_value(D)

    # ---- control: 'max is at a=0' is rejected (the empty split is the MINIMUM, not the peak) ----
    claimed_argmax = 0
    assert 0 not in argmax8, "control: a=0 must NOT be an argmax (it is the f=0 endpoint minimum)"
    assert curve8[claimed_argmax] < mx8, \
        f"control: f(0)={curve8[claimed_argmax]} must be strictly below the peak {mx8}"
    print(f"FAIL_MAX_AT_ZERO_REJECTED  a planted argmax a=0 (f(0)={curve8[0]} < peak {mx8}) is "
          f"rejected: the empty split is the MINIMUM, the peak sits at a=D//2={D // 2}")

    # ---- control: 'peak value > D//2' is rejected (D//2 is the exact ceiling on the support) ----
    turn8 = D // 2
    planted_value = turn8 + 1   # claim a support strictly above D//2
    assert planted_value > mx8, "control planted value must actually exceed the true peak"
    exceeds_bound = all(curve8[a] < planted_value for a in range(0, D + 1))
    assert exceeds_bound, "control: no a may reach a value > D//2; the planted over-peak is unattainable"
    print(f"FAIL_VALUE_OVER_HALF_REJECTED  a planted peak value {planted_value} > D//2={turn8} is "
          f"rejected: no split a=0..{D} reaches it (D//2 is the exact maximum of min(a,D-a))")

    # ---- control: an ASYMMETRIC max claim is rejected (the true peak is balanced, f is swap-symmetric) ----
    #     plant a one-sided support g(a)=a (NOT min) whose 'max' sits at a=D, breaking the balance
    def g_onesided(a: int, D_: int) -> int:
        return a   # ignores the env rank D-a -> peaks at the unbalanced a=D, not at the turn
    g_curve = [g_onesided(a, D) for a in range(0, D + 1)]
    g_argmax = {a for a in range(0, D + 1) if g_curve[a] == max(g_curve)}
    assert g_argmax == {D} and turn8 not in g_argmax, \
        "control: the planted one-sided support must peak at the UNBALANCED a=D, not at the turn"
    assert g_onesided(2, D) != g_onesided(D - 2, D), \
        "control: the planted support must be visibly NON-symmetric under a<->D-a"
    print(f"FAIL_ASYMMETRIC_MAX_REJECTED  a planted one-sided support g(a)=a peaks at the unbalanced "
          f"a={D} (not the turn {turn8}) and is non-symmetric -> rejected: the true Page support "
          f"min(a,D-a) is swap-symmetric and peaks at the balanced split")

    print("HONEST_CERT_CLOSED  Page rank turning point OWNED exactly: argmax(min(a,D-a))=D//2 and "
          "max=D//2 for D in {8,33}, single-peak rise/fall, swap symmetry -- all exact integer; the "
          "analytic von Neumann entropy this support bounds stays EXTERNAL (no continuum object enters)")
    print("PASS_PAGE_TURNING_POINT_RANK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
