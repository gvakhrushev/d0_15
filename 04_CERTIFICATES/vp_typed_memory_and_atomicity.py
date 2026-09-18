"""Exact finite checks for d0_typed_memory_and_atomicity.md.

No external packages. The proofs are in the note; this checks finite models,
behavioral minimization, distinguishing continuations, and symmetry actions.
Run: python3 vp_typed_memory_and_atomicity.py
"""

from fractions import Fraction
from itertools import combinations, product
from math import comb

MISSING = -1


def partials(q, r):
    return tuple(product(range(MISSING, q), repeat=r))


def read(state):
    return None if MISSING in state else state


def write(state, i, value):
    return state[:i] + (value,) + state[i + 1:]


def atomic_projection(state):
    return (MISSING,) * len(state) if MISSING in state else state


def normalize(signatures):
    labels = {}
    return {s: labels.setdefault(sig, len(labels)) for s, sig in signatures.items()}


def minimize(q, r):
    states = partials(q, r)
    commands = tuple(product(range(r), range(q)))
    partition = normalize({s: read(s) for s in states})
    sizes = [len(set(partition.values()))]
    while True:
        refined = normalize({
            s: (partition[s], tuple(partition[write(s, i, b)] for i, b in commands))
            for s in states
        })
        count = len(set(refined.values()))
        if count == sizes[-1]:
            return count, sizes
        partition = refined
        sizes.append(count)


def check_partial_memory(q, r):
    states = partials(q, r)
    reached = {(MISSING,) * r}
    frontier = set(reached)
    while frontier:
        nxt = {write(s, i, b) for s in frontier for i in range(r) for b in range(q)}
        frontier = nxt - reached
        reached |= frontier
    assert reached == set(states)
    # Constructively distinguish every pair by at most r-1 writes and one read.
    for a, b in combinations(states, 2):
        i = next(i for i in range(r) if a[i] != b[i])
        aa, bb = a, b
        for j in range(r):
            if j != i:
                aa, bb = write(aa, j, 0), write(bb, j, 0)
        assert read(aa) != read(bb)
    count, rounds_ = minimize(q, r)
    assert count == (q + 1) ** r
    expected = [1] if r == 0 else [
        1 + sum(comb(r, m) * q ** (r - m) for m in range(k + 1))
        for k in range(r)
    ]
    assert rounds_ == expected
    atomic = {atomic_projection(s) for s in states}
    assert len(atomic) == (1 if r == 0 else 1 + q ** r)
    assert len({read(s) for s in states}) == len(atomic)
    return rounds_


def swap_mask(mask):
    return ((mask & 1) << 1) | ((mask & 2) >> 1)


def exact_support_inventory(b, q=2):
    states = []
    for mask in range(4):
        states.extend((mask, "live", j) for j in range(b))
        archives = {(MISSING, MISSING)}
        support = tuple(i for i in range(2) if mask & (1 << i))
        for values in product(range(q), repeat=len(support)):
            state = [MISSING, MISSING]
            for i, v in zip(support, values):
                state[i] = v
            archives.add(tuple(state))
        states.extend((mask, "archive", s) for s in sorted(archives))
    return tuple(states)


def check_orbits(b, transpositions):
    inv = list(range(b))
    for j in range(transpositions):
        inv[2 * j], inv[2 * j + 1] = 2 * j + 1, 2 * j

    def swap(t):
        mask, mode, state = t
        return (swap_mask(mask), mode, inv[state] if mode == "live" else state[::-1])

    inventory = exact_support_inventory(b)
    assert len(inventory) == 4 * (b + 3)
    assert all(swap(swap(t)) == t for t in inventory)
    fixed = sum(swap(t) == t for t in inventory)
    orbits = {frozenset((t, swap(t))) for t in inventory}
    f = b - 2 * transpositions
    assert fixed == 2 * f + 4
    assert len(orbits) == 2 * b + 8 + f
    assert len(orbits) < 3 * b + 9
    # An explicitly retained two-valued frame makes the diagonal action free.
    framed = [(t, frame) for t in inventory for frame in (0, 1)]
    framed_orbits = {frozenset(((t, frame), (swap(t), 1 - frame))) for t, frame in framed}
    assert len(framed_orbits) == len(inventory)
    return f, len(orbits)


def main():
    checked = []
    for q in (2, 3):
        for r in range(5):
            rounds_ = check_partial_memory(q, r)
            checked.append((q, r, rounds_))

    # Snapshot equivalence is not a congruence for independent writes.
    s, t = (-1, -1), (0, -1)
    assert atomic_projection(s) == atomic_projection(t)
    assert atomic_projection(write(s, 1, 0)) != atomic_projection(write(t, 1, 0))

    # Eight nonempty partial records and Role x Orient have different swap characters.
    nonempty = [s for s in partials(2, 2) if s != (-1, -1)]
    role_orient = list(product(range(2), repeat=3))
    partial_fixed = sum(s == s[::-1] for s in nonempty)
    product_fixed = sum((a, b, o) == (b, a, o) for a, b, o in role_orient)
    assert len(nonempty) == len(role_orient) == 8
    assert (partial_fixed, product_fixed) == (2, 4)

    # A fixed parity question sees two classes, while future coordinate writes force four.
    full = tuple(product(range(2), repeat=2))
    assert len({a ^ b for a, b in full}) == 2
    for s, t in combinations(full, 2):
        i = next(i for i in range(2) if s[i] != t[i])
        ss, tt = write(s, 1 - i, 0), write(t, 1 - i, 0)
        assert (ss[0] ^ ss[1]) != (tt[0] ^ tt[1])

    assert [8 + len({atomic_projection(s) for s in partials(2, r)}) for r in range(3)] == [9, 11, 13]
    assert [8 + len(partials(2, r)) for r in range(3)] == [9, 11, 17]
    assert Fraction(9 ** 2 + 11 ** 2 + 13 ** 2, 33 ** 2) == Fraction(371, 1089)
    assert Fraction(9 ** 2 + 11 ** 2 + 17 ** 2, 37 ** 2) == Fraction(491, 1369)

    orbit_counts = [check_orbits(8, t) for t in range(5)]
    for b in range(1, 21):
        x, y, z = b + 1, b + 3, b + 5
        m = b + 3
        assert x + y + z == 3 * m
        assert x * x + y * y + z * z == 3 * m * m + 8
        assert 3 * m * m - (x * y + x * z + y * z) == 4
        assert m ** 3 - x * y * z == 4 * m == len(exact_support_inventory(b))
        check_orbits(b, b // 2)
    for q in range(2, 20):
        assert ((q + 1) - 1 == (q * q + 1) - (q + 1)) == (q == 2)

    print("PASS: complete state minimization and all pairwise continuation witnesses")
    for q, r, rounds_ in checked:
        print(f"  alphabet={q}, lines={r}: observation refinement {rounds_}")
    print("PASS: snapshot projection fails the transition-congruence test")
    print("PASS: two eight-state carriers have swap fixed-point counts 2 and 4")
    print("PASS: conditional atomic sizes 9,11,13; asynchronous sizes 9,11,17")
    print("PASS: exact support inventory 44; (live fixed states, orbit counts):", orbit_counts)
    print("PASS: general capacity identities; centered alphabet is binary")


if __name__ == "__main__":
    main()
