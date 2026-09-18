"""Toral return-group origin of the scene invariants (Direction I).

Question addressed: can q_T = 44, the centre m = 11, the half-width Delta = 2 and the
collision invariant P_2 = 371/1089 be read off the toral operator T alone, WITHOUT
using |V11| = 11 as an input?  (The registered formula q_T = lcm(|Role|, |V11|) uses
|V11| as an input, and the Lean capacityCenter = qT / |Role| then reads 11 back out,
so that route is circular.)

Exact finite checks, stdlib only.  Conventions:
  T = [[0, 1], [1, -1]]         (trace -1, det -1, charpoly X^2 + X - 1)
  Fix(T^n) := Z^2 / (T^n - I) Z^2  (periodic points of period dividing n on the torus)
  #Fix_n = |det(T^n - I)|,  group structure via Smith normal form.

Certified statements
  1. #Fix_n = L_n (n odd), L_n - 2 (n even), n = 1..60, L = Lucas numbers.
  2. Fix(T^1) = Fix(T^2) = 0 ("sterile" first two returns); Fix(T^3) ~ (Z/2)^2 (Klein),
     the canonical 2-torsion T^2[2] (T = I mod 2 iff 3 | n); Fix(T^4) ~ Z/5; Fix(T^5) ~ Z/11.
  3. Among all integral 2x2 unimodular classes with |trace| <= 10, sterility of returns 1 and 2
     holds iff (trace, det) in {(-1,-1), (1,-1)}: the golden class.
  4. Toral definitions (no scene input):
        Role_T  := Fix(T^3),  |Role_T| = 4,  exponent = 2 =: Delta_T
        Orient  := Z/2 from det T = -1 (orientation reversal)
        Omega_T := Role_T x Orient,  |Omega_T| = 8
        m_T     := #Fix_n at the FIRST n with #Fix_n > |Omega_T|   -> n = 5, m_T = 11
        q_T'    := |Fix(T^3)| * |Fix(T^5)| = 44
     reproduce q_T = 44, m = 11, Delta = 2, |Omega8| = 8 and hence the ladder (9, 11, 13).
  5. Invariant identities for the centred triple (m - Delta, m, m + Delta), N = 3m:
        sum n_i^2 - N^2 / 3 = 2 Delta^2 = |Omega_T| = 8
        P_2 = 1/3 + |Omega_T| / N^2 = 371/1089
        m^3 - prod n_i = m Delta^2 = 44 = q_T   (triangle deficit equals the return window)
        tr A^2 = N^2 - sum n_i^2 = 718,  tr A^3 = 6 prod n_i = 7722.
  6. Negative controls: the cat map (trace 3, det 1) has cyclic first return Z/5 (no Klein,
     Delta undefined as a square exponent); alternative thresholds |Role| = 4 or |V11| = 11 give
     different centres (5, 16) and different P_2, so the threshold |Omega_T| is load-bearing and
     is recorded as the residual internal selection rule.

Run: python3 vp_toral_return_group_origin_of_scene.py
"""

from fractions import Fraction
from itertools import product
from math import gcd

T = ((0, 1), (1, -1))
I2 = ((1, 0), (0, 1))


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def mpow(a, n):
    r = I2
    for _ in range(n):
        r = mul(r, a)
    return r


def minus_i(a):
    return ((a[0][0] - 1, a[0][1]), (a[1][0], a[1][1] - 1))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def smith(a):
    """Smith normal form (d1, d2) with d1 | d2 of a nonsingular 2x2 integer matrix."""
    d = abs(det(a))
    assert d != 0
    g = gcd(gcd(abs(a[0][0]), abs(a[0][1])), gcd(abs(a[1][0]), abs(a[1][1])))
    return (g, d // g)


def fix_group(a, n):
    return smith(minus_i(mpow(a, n)))


def fix_count(a, n):
    return abs(det(minus_i(mpow(a, n))))


def lucas(k):
    seq = [2, 1]
    for _ in range(2, k + 1):
        seq.append(seq[-1] + seq[-2])
    return seq


def group_exponent(snf):
    return snf[1]


def main():
    L = lucas(70)

    # 1. Lucas identity for the fixed-point counts.
    for n in range(1, 61):
        expected = L[n] if n % 2 else L[n] - 2
        assert fix_count(T, n) == expected, (n, fix_count(T, n), expected)

    # 2. Group structures of the first returns.
    structures = {n: fix_group(T, n) for n in range(1, 13)}
    assert structures[1] == (1, 1) and structures[2] == (1, 1)
    assert structures[3] == (2, 2)          # Klein four-group = 2-torsion of the torus
    assert structures[4] == (1, 5)
    assert structures[5] == (1, 11)
    assert structures[6] == (4, 4)
    assert structures[10] == (11, 11)
    # T == I mod 2 exactly when 3 | n, so Fix(T^n) contains the full 2-torsion iff 3 | n.
    for n in range(1, 31):
        tn = mpow(T, n)
        is_id_mod2 = all((tn[i][j] - I2[i][j]) % 2 == 0 for i in range(2) for j in range(2))
        assert is_id_mod2 == (n % 3 == 0)
    # T acts on the three nonzero half-periods as a single 3-cycle (the primitive period-3 seed).
    half = [(1, 0), (0, 1), (1, 1)]
    act = {v: ((T[0][0] * v[0] + T[0][1] * v[1]) % 2, (T[1][0] * v[0] + T[1][1] * v[1]) % 2) for v in half}
    orbit = {half[0]}
    v = half[0]
    for _ in range(3):
        v = act[v]
        orbit.add(v)
    assert orbit == set(half) and act[act[act[half[0]]]] == half[0]

    # 3. Sterile first two returns characterise the golden class.
    sterile = []
    for tr in range(-10, 11):
        for d in (-1, 1):
            # det(A - I) = 1 - tr + det, det(A^2 - I) = det(A - I) det(A + I), det(A + I) = 1 + tr + det
            if abs(1 - tr + d) == 1 and abs(1 + tr + d) == 1:
                sterile.append((tr, d))
    assert sorted(sterile) == [(-1, -1), (1, -1)]
    # Concrete matrix check over a box: any unimodular integral matrix in the golden class has the
    # same return sequence as T (conjugacy invariance is not assumed; we test all such matrices).
    golden_seqs = set()
    for a, b, c, d in product(range(-4, 5), repeat=4):
        if a * d - b * c == -1 and abs(a + d) == 1:
            A = ((a, b), (c, d))
            golden_seqs.add(tuple(fix_group(A, n) for n in range(1, 9)))
    assert golden_seqs == {tuple(structures[n] for n in range(1, 9))}

    # 4. Toral definitions and the scene ladder.
    role_T = structures[3]
    card_role = role_T[0] * role_T[1]
    delta_T = group_exponent(role_T)
    assert (card_role, delta_T) == (4, 2)
    assert det(T) == -1                       # orientation reversal -> Orient = Z/2
    card_orient = 2
    card_omega = card_role * card_orient
    assert card_omega == 8
    n_star = 1
    while fix_count(T, n_star) <= card_omega:
        n_star += 1
    m_T = fix_count(T, n_star)
    assert (n_star, m_T) == (5, 11)
    assert fix_group(T, n_star) == (1, 11)    # cyclic of prime order
    q_T = fix_count(T, 3) * fix_count(T, 5)
    assert q_T == 44
    ladder = (m_T - delta_T, m_T, m_T + delta_T)
    assert ladder == (9, 11, 13)
    # Consistency with the registered capacity reading: centre = q_T / |Role|.
    assert q_T // card_role == m_T and q_T % card_role == 0

    # 5. Invariant identities.
    N = sum(ladder)
    C = sum(x * x for x in ladder)
    triangles = ladder[0] * ladder[1] * ladder[2]
    assert (N, C, triangles) == (33, 371, 1287)
    assert Fraction(C, N * N) == Fraction(371, 1089)
    assert C - Fraction(N * N, 3) == 2 * delta_T ** 2 == card_omega
    assert Fraction(C, N * N) == Fraction(1, 3) + Fraction(card_omega, N * N)
    assert m_T ** 3 - triangles == m_T * delta_T ** 2 == q_T
    assert N * N - C == 718 and 6 * triangles == 7722
    # General centred identity, any (m, Delta).
    for m in range(1, 40):
        for dl in range(0, m):
            z = (m - dl, m, m + dl)
            assert sum(x * x for x in z) * 3 - (3 * m) ** 2 == 6 * dl * dl
            assert m ** 3 - z[0] * z[1] * z[2] == m * dl * dl

    # 6. Negative controls.
    cat = ((2, 1), (1, 1))                    # trace 3, det 1
    assert fix_group(cat, 1) == (1, 1) and fix_group(cat, 2) == (1, 5)
    first_nontrivial_cat = next(n for n in range(1, 20) if fix_count(cat, n) > 1)
    assert first_nontrivial_cat == 2 and fix_group(cat, 2)[0] == 1   # cyclic, not Klein
    alt = {}
    for label, thr in (("Role", 4), ("Omega", 8), ("V9", 9), ("V11", 11)):
        n = 1
        while fix_count(T, n) <= thr:
            n += 1
        m = fix_count(T, n)
        z = (m - 2, m, m + 2)
        alt[label] = (n, m, Fraction(sum(x * x for x in z), (3 * m) ** 2))
    assert alt["Omega"] == alt["V9"] == (5, 11, Fraction(371, 1089))
    assert alt["Role"] == (4, 5, Fraction(83, 225))
    assert alt["V11"] == (6, 16, Fraction(97, 288))

    print("PASS: #Fix_n(T) = L_n (odd) / L_n - 2 (even), n <= 60")
    print("PASS: Fix(T^n) for n=1..6:", [structures[n] for n in range(1, 7)])
    print("PASS: sterile returns 1,2 <=> golden class {(-1,-1),(1,-1)}; T is a 3-cycle on T^2[2]\\{0}")
    print("PASS: toral-only definitions give |Role|=4, Delta=2, |Omega|=8, m=11 (n*=5), q_T=44, ladder", ladder)
    print("PASS: C - N^2/3 = |Omega| = 8, P_2 = 1/3 + 8/1089 = 371/1089, m^3 - triangles = 44 = q_T")
    print("PASS: negative controls: cat map first return Z/5 (cyclic); thresholds", {k: (v[0], v[1], str(v[2])) for k, v in alt.items()})


if __name__ == "__main__":
    main()
