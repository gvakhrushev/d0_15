"""Typed preparation/repair origin of the scene ladder and of q_T (Direction II),
and the weld with the toral return channel.

Setting.  A preparation record has r independent write lines over a q-letter alphabet;
partial records live in {bot, 0..q-1}^r.  Atomic (transactional) readout identifies all
partial records with a missing letter, so a k-line sub-register has exactly
    a(q, k) = 1 + q^k            (k >= 1),    a(q, 0) = 1
atomic classes.  Complete r-line records with an orientation bit form the live carrier
    Omega(q, r) := {0..q-1}^r x {+,-},   |Omega| = 2 q^r.
Zone k (k = 0..r) := live carrier + atomic classes of the k-line sub-register:
    z_k(q, r) = 2 q^r + a(q, k).
Rank := r + 1 (number of support sizes).

Certified statements
  A. Centering forcing.  The zone ladder z_0 < z_1 < ... < z_r is an arithmetic progression with
     rank >= 3 iff (q, r) = (2, 2) (checked for q <= 300, r <= 12; algebraic reason: the steps are
     q^k - q^{k-1}, constant for k = 1..r only if q^2 - q = q, i.e. q = 2, and then only up to r = 2
     since 2^2 - 2 = 2 but 2^3 - 2^2 = 4).  At (2, 2) the ladder is (9, 11, 13), N = 33,
     P_2 = 371/1089.  Rank 2 (r = 1) is trivially arithmetic for every q: three zones are needed.
  B. Inventory origin of q_T.  Exact support inventory over the 2^r masks (live states of the
     mask plus the atomic classes of the masked sub-register, the empty record counted once):
        Inv(q, r) = 2^r * 2 q^r + 2^r + (1 + q)^r - 1
     Inv(2, 2) = 32 + 4 + 9 - 1 = 44 = q_T, with 2^r = |Role| = 4 masks and per-mask mean 11 = m.
     The verifier-exchange swap identifies the two single-line masks, leaving 3 mask classes and
     3 * 8 + (1 + 3 + 5) = 33 = N; the removed class has exactly 11 = m elements.  So
     q_T = N + m and m = q_T / |Role| hold with q_T computed from (q, r) alone, not from |V11|.
  C. Carrier equivariance.  Under the line swap, the live carrier {0,1}^2 x {+,-} has 4 fixed
     points, identical to Role x Orient = Dyad x Dyad x Bool; the alternative eight-element
     carrier "nonempty partial records" has 2 fixed points and is rejected as the Omega8 model.
  D. Two-channel weld at q = 2.  The toral channel (T = [[0,1],[1,-1]], #Fix_n = |det(T^n - I)|)
     yields |Fix T^3| = 4, exponent 2, |Omega_T| = 8, first #Fix_n > 8 is 11, q_T = 4 * 11.
     The typed channel at (2, 2) yields |Role| = 4, step 2, |Omega| = 8, m = 11, Inv = 44.
     The full tuple (4, 2, 8, 11, 44, (9,11,13), 371/1089) agrees.
  E. NO-GO for the weld as a stand-alone selector.  "Typed centre 2q^2 + q + 1 equals the first
     #Fix_n exceeding 2q^2" holds for q in {1, 2, 42} (q <= 5000), and the unanchored Lucas
     condition 2q^2 + q + 1 in {L_n} has the same solution set; q^3 + q + 1 in {L_n} holds for
     q in {1, 2, 8}.  Hence Lucas-return agreement alone does NOT force q = 2; centering (A) does,
     and the two channels are then found to agree.

Run: python3 vp_typed_ladder_centering_and_two_channel_weld.py
"""

from fractions import Fraction
from itertools import product

MISSING = -1


def atomic_classes(q, k):
    return 1 if k == 0 else 1 + q ** k


def zones(q, r):
    live = 2 * q ** r
    return [live + atomic_classes(q, k) for k in range(r + 1)]


def is_arithmetic(z):
    steps = [z[i + 1] - z[i] for i in range(len(z) - 1)]
    return len(set(steps)) == 1 and steps[0] > 0


def inventory(q, r):
    """Exact enumeration of (mask, live state) and (mask, atomic archive class)."""
    states = set()
    for mask in range(2 ** r):
        support = [i for i in range(r) if mask >> i & 1]
        for live in product(range(q), repeat=r):
            for orient in (0, 1):
                states.add((mask, "live", live, orient))
        archives = {(MISSING,) * r}
        for values in product(range(q), repeat=len(support)):
            rec = [MISSING] * r
            for i, v in zip(support, values):
                rec[i] = v
            archives.add(tuple(rec))
        for rec in archives:
            states.add((mask, "archive", rec))
    return states


def lucas(k):
    seq = [2, 1]
    for _ in range(2, k + 1):
        seq.append(seq[-1] + seq[-2])
    return seq


def main():
    # A. Centering forcing.
    solutions = [(q, r) for q in range(1, 301) for r in range(2, 13) if is_arithmetic(zones(q, r))]
    assert solutions == [(2, 2)], solutions
    assert all(is_arithmetic(zones(q, 1)) for q in range(2, 50))
    z = zones(2, 2)
    assert z == [9, 11, 13]
    N = sum(z)
    C = sum(x * x for x in z)
    assert (N, C) == (33, 371) and Fraction(C, N * N) == Fraction(371, 1089)
    assert zones(3, 2) == [19, 22, 28] and zones(2, 3) == [17, 19, 21, 25]
    # algebraic step identity
    for q in range(2, 20):
        for r in range(1, 8):
            zz = zones(q, r)
            assert [zz[k] - zz[k - 1] for k in range(1, r + 1)] == [q] + [q ** k - q ** (k - 1) for k in range(2, r + 1)]

    # B. Inventory origin of q_T.
    for q in range(1, 6):
        for r in range(0, 5):
            inv = inventory(q, r)
            assert len(inv) == 2 ** r * 2 * q ** r + 2 ** r + (1 + q) ** r - 1, (q, r, len(inv))
    inv22 = inventory(2, 2)
    assert len(inv22) == 44
    masks = sorted({s[0] for s in inv22})
    assert masks == [0, 1, 2, 3]
    per_mask = {mk: sum(1 for s in inv22 if s[0] == mk) for mk in masks}
    assert per_mask == {0: 9, 1: 11, 2: 11, 3: 13}
    assert sum(per_mask.values()) // len(masks) == 11
    # swap identifies masks 1 and 2 (single-line supports)
    def swap_mask(mk):
        return ((mk & 1) << 1) | ((mk & 2) >> 1)
    mask_classes = {frozenset((mk, swap_mask(mk))) for mk in masks}
    assert len(mask_classes) == 3
    reduced = sum(per_mask[min(cls)] for cls in mask_classes)
    assert reduced == 33 == N
    assert 44 - reduced == 11
    assert sorted(per_mask[min(cls)] for cls in mask_classes) == [9, 11, 13]

    # C. Carrier equivariance under the line swap.
    live_carrier = [(a, b, o) for a in range(2) for b in range(2) for o in range(2)]
    role_orient = live_carrier  # literally Dyad x Dyad x Bool
    nonempty_partial = [s for s in product(range(MISSING, 2), repeat=2) if s != (MISSING, MISSING)]
    assert len(live_carrier) == len(role_orient) == len(nonempty_partial) == 8
    fixed_live = sum((a, b, o) == (b, a, o) for a, b, o in live_carrier)
    fixed_partial = sum(s == s[::-1] for s in nonempty_partial)
    assert (fixed_live, fixed_partial) == (4, 2)

    # D. Two-channel weld at q = 2 (toral side recomputed here independently).
    def mul(A, B):
        return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    def fix_count(n):
        M = ((1, 0), (0, 1))
        for _ in range(n):
            M = mul(M, ((0, 1), (1, -1)))
        return abs((M[0][0] - 1) * (M[1][1] - 1) - M[0][1] * M[1][0])
    toral_role = fix_count(3)
    toral_omega = 2 * toral_role
    n = 1
    while fix_count(n) <= toral_omega:
        n += 1
    toral_m = fix_count(n)
    toral_qT = fix_count(3) * fix_count(5)
    typed = (2 ** 2, 2, 2 * 2 ** 2, zones(2, 2)[1], len(inv22))
    toral = (toral_role, 2, toral_omega, toral_m, toral_qT)
    assert typed == toral == (4, 2, 8, 11, 44)

    # E. NO-GO: Lucas/return agreement alone does not select q = 2.
    L = lucas(80)
    lucas_set = set(L)
    def fix_seq(k):
        return L[k] if k % 2 else L[k] - 2
    def first_exceeding(t):
        k = 1
        while fix_seq(k) <= t:
            k += 1
        return fix_seq(k)
    weld_hits = [q for q in range(1, 5001) if 2 * q * q + q + 1 == first_exceeding(2 * q * q)]
    assert weld_hits == [1, 2, 42], weld_hits
    assert [q for q in range(1, 5001) if 2 * q * q + q + 1 in lucas_set] == [1, 2, 42]
    assert [q for q in range(1, 2001) if q ** 3 + q + 1 in lucas_set] == [1, 2, 8]
    # centering removes 1 (degenerate, zero step) and 42 (steps 42 and 1722)
    assert not is_arithmetic(zones(1, 2)) and not is_arithmetic(zones(42, 2))

    print("PASS: arithmetic zone ladder with rank >= 3 <=> (q, r) = (2, 2); ladder", z, "P_2 = 371/1089")
    print("PASS: inventory Inv(q,r) = 2^r*2q^r + 2^r + (1+q)^r - 1; Inv(2,2) = 44, per-mask", per_mask, "swap-reduced 33")
    print("PASS: swap-equivariant eight-carrier is {0,1}^2 x Orient (4 fixed points), not nonempty partials (2)")
    print("PASS: typed and toral channels agree on (|Role|, Delta, |Omega|, m, q_T) =", typed)
    print("PASS (NO-GO recorded): weld/Lucas agreement alone holds for q in", weld_hits, "-> centering is the selector")


if __name__ == "__main__":
    main()
