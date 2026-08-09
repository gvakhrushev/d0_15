#!/usr/bin/env python3
"""Exact compute layer for the setwise-stable observable-algebra lattice.

Target (DRAFT): on the frozen K(9,11,13) scene, GraphAut-stable unital
subalgebras of Q^V that contain the computed degree are indexed by the three
independent decisions "resolve this zone completely / leave it whole".  Thus
there are 2^3 = 8, ordered as the Boolean lattice of subsets of the zone set.

This script does NOT construct the answer from that conclusion.  It first
builds adjacency and degree, obtains full-GraphAut pair orbits from permutation
generators, enumerates every invariant relation in the 2^12 orbit-union domain,
and filters for equivalence relations whose blocks carry constant degree.  The
three-bit representation is recovered only after enumeration.

All arithmetic is integer/Fraction.  --selftest runs conclusion-failing mutants.
"""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from itertools import permutations

FAILURES: list[str] = []
PASSES: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> bool:
    tag = "PASS" if condition else "FAIL"
    print(f"[{tag}] {name}" + (f" -- {detail}" if detail else ""))
    (PASSES if condition else FAILURES).append(name)
    return condition


def build_scene(sizes: tuple[int, ...]):
    zone: list[int] = []
    for z, size in enumerate(sizes):
        zone.extend([z] * size)
    n = len(zone)
    adjacency = [
        [int(i != j and zone[i] != zone[j]) for j in range(n)]
        for i in range(n)
    ]
    degree = [sum(row) for row in adjacency]
    return zone, adjacency, degree


def zone_blocks(zone: list[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(i for i, value in enumerate(zone) if value == z)
        for z in sorted(set(zone))
    )


def zone_starts(sizes: tuple[int, ...]) -> list[int]:
    starts: list[int] = []
    cursor = 0
    for size in sizes:
        starts.append(cursor)
        cursor += size
    return starts


def aut_generators(
    sizes: tuple[int, ...], *, drop_equal_zone_swaps: bool = False
) -> list[list[int]]:
    """Generators for the full Aut of a complete multipartite graph.

    Adjacent transpositions generate each within-part symmetric group.  Equal
    parts can additionally be swapped; the selftest drops those swaps to make
    the repeated-size conclusion fail.
    """
    n = sum(sizes)
    starts = zone_starts(sizes)
    generators: list[list[int]] = []
    for z, size in enumerate(sizes):
        for i in range(starts[z], starts[z] + size - 1):
            p = list(range(n))
            p[i], p[i + 1] = p[i + 1], p[i]
            generators.append(p)
    if not drop_equal_zone_swaps:
        for a in range(len(sizes)):
            for b in range(a + 1, len(sizes)):
                if sizes[a] != sizes[b]:
                    continue
                p = list(range(n))
                for k in range(sizes[a]):
                    p[starts[a] + k] = starts[b] + k
                    p[starts[b] + k] = starts[a] + k
                generators.append(p)
    return generators


def is_automorphism(p: list[int], adjacency: list[list[int]]) -> bool:
    n = len(p)
    return all(
        adjacency[p[i]][p[j]] == adjacency[i][j]
        for i in range(n)
        for j in range(n)
    )


def pair_orbits(n: int, generators: list[list[int]]) -> list[tuple[tuple[int, int], ...]]:
    parent = list(range(n * n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for j in range(n):
            base = find(i * n + j)
            for p in generators:
                image = find(p[i] * n + p[j])
                if base != image:
                    parent[base] = image
                    base = find(base)
    groups: dict[int, list[tuple[int, int]]] = {}
    for i in range(n):
        for j in range(n):
            groups.setdefault(find(i * n + j), []).append((i, j))
    return [tuple(group) for group in groups.values()]


def relation_is_equivalence(
    relation: set[tuple[int, int]], n: int, *, require_symmetry: bool = True,
    require_transitivity: bool = True
) -> bool:
    if any((i, i) not in relation for i in range(n)):
        return False
    if require_symmetry and any((j, i) not in relation for i, j in relation):
        return False
    if require_transitivity:
        neighborhoods = {i: {j for a, j in relation if a == i} for i in range(n)}
        for i in range(n):
            for j in neighborhoods[i]:
                if not neighborhoods[j] <= neighborhoods[i]:
                    return False
    return True


def relation_to_partition(
    relation: set[tuple[int, int]], n: int
) -> tuple[tuple[int, ...], ...] | None:
    if not relation_is_equivalence(relation, n):
        return None
    neighborhoods = {i: {j for a, j in relation if a == i} for i in range(n)}
    seen: set[int] = set()
    blocks: list[tuple[int, ...]] = []
    for i in range(n):
        if i in seen:
            continue
        block = tuple(sorted(neighborhoods[i]))
        blocks.append(block)
        seen.update(block)
    return tuple(sorted(blocks))


def relation_separates_degree(
    relation: set[tuple[int, int]], degree: list[int]
) -> bool:
    return all(degree[i] == degree[j] for i, j in relation)


def enumerate_stable_relations(
    sizes: tuple[int, ...], *, require_symmetry: bool = True,
    require_transitivity: bool = True, separates_degree: bool = True,
    drop_equal_zone_swaps: bool = False
):
    zone, adjacency, degree = build_scene(sizes)
    generators = aut_generators(sizes, drop_equal_zone_swaps=drop_equal_zone_swaps)
    assert all(is_automorphism(p, adjacency) for p in generators)
    orbits = pair_orbits(len(zone), generators)
    if len(orbits) > 22:
        raise RuntimeError(f"pair-orbit domain too large: {len(orbits)}")
    relations: list[frozenset[tuple[int, int]]] = []
    for mask in range(1 << len(orbits)):
        relation: set[tuple[int, int]] = set()
        for bit, orbit in enumerate(orbits):
            if (mask >> bit) & 1:
                relation.update(orbit)
        if not relation_is_equivalence(
            relation,
            len(zone),
            require_symmetry=require_symmetry,
            require_transitivity=require_transitivity,
        ):
            continue
        if separates_degree and not relation_separates_degree(relation, degree):
            continue
        relations.append(frozenset(relation))
    return zone, adjacency, degree, generators, orbits, sorted(set(relations), key=lambda r: (len(r), sorted(r)))



def enumerate_stable_partitions(
    sizes: tuple[int, ...], *, require_symmetry: bool = True,
    require_transitivity: bool = True, separates_degree: bool = True,
    drop_equal_zone_swaps: bool = False
):
    zone, adjacency, degree, generators, orbits, relations = enumerate_stable_relations(
        sizes,
        require_symmetry=require_symmetry,
        require_transitivity=require_transitivity,
        separates_degree=separates_degree,
        drop_equal_zone_swaps=drop_equal_zone_swaps,
    )
    partitions = [relation_to_partition(set(relation), len(zone)) for relation in relations]
    if not require_symmetry or not require_transitivity:
        return zone, adjacency, degree, generators, orbits, relations
    assert all(partition is not None for partition in partitions)
    return zone, adjacency, degree, generators, orbits, sorted(set(partitions))


def recovered_bits(
    partition: tuple[tuple[int, ...], ...], zone: list[int]
) -> frozenset[int] | None:
    """Recover zones resolved into singletons; reject any partial zone split."""
    blocks = [set(block) for block in partition]
    result: set[int] = set()
    for z, whole_tuple in enumerate(zone_blocks(zone)):
        whole = set(whole_tuple)
        restricted = [block for block in blocks if block <= whole]
        if len(restricted) == 1 and restricted[0] == whole:
            continue
        if len(restricted) == len(whole) and all(len(block) == 1 for block in restricted):
            result.add(z)
            continue
        return None
    return frozenset(result)


def partition_for_bits(zone: list[int], bits: frozenset[int]):
    blocks: list[tuple[int, ...]] = []
    for z, whole in enumerate(zone_blocks(zone)):
        if z in bits:
            blocks.extend((i,) for i in whole)
        else:
            blocks.append(whole)
    return tuple(sorted(blocks))


def refines(p, q) -> bool:
    """Partition p refines q."""
    return all(any(set(block) <= set(coarse) for coarse in q) for block in p)


def exact_rank(rows: list[list[int | Fraction]]) -> int:
    matrix = [[Fraction(x) for x in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    for col in range(len(matrix[0])):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][col]
        matrix[rank] = [x / value for x in matrix[rank]]
        for r in range(len(matrix)):
            if r == rank or not matrix[r][col]:
                continue
            factor = matrix[r][col]
            matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[rank])]
        rank += 1
    return rank


def run_real_scene() -> None:
    sizes = (9, 11, 13)
    zone, adjacency, degree, generators, orbits, partitions = enumerate_stable_partitions(sizes)
    bits = [recovered_bits(partition, zone) for partition in partitions]
    expected_bits = {frozenset(s) for mask in range(8) for s in [
        [z for z in range(3) if (mask >> z) & 1]
    ]}

    print("STRUCTURE_FIXED_BEFORE_NUMBER: adjacency -> full GraphAut pair orbits -> invariant equivalence relations -> degree filter")
    check("A1 full generator list preserves adjacency", all(is_automorphism(p, adjacency) for p in generators), f"{len(generators)} generators")
    check("A2 degrees computed from adjacency", tuple(degree[sum(sizes[:z])] for z in range(3)) == (24, 22, 20))
    check("A3 pair-orbit domain independently computed", len(orbits) == 12, f"2^{len(orbits)} relations scanned")
    check("B1 exactly eight stable degree-containing partitions", len(partitions) == 8, f"computed {len(partitions)}")
    check("B2 every stable partition has whole/discrete zone dichotomy", all(bit is not None for bit in bits))
    check("B3 recovered bitsets exhaust Finset(Fin 3)", set(bits) == expected_bits, f"{sorted(map(lambda x: tuple(sorted(x)), set(bits)))}")
    check("B4 reconstruction from recovered bits is exact", all(partition_for_bits(zone, bit) == partition for partition, bit in zip(partitions, bits) if bit is not None))

    dimensions = sorted(len(partition) for partition in partitions)
    check("C1 exact dimension set", dimensions == [3, 11, 13, 15, 21, 23, 25, 33], str(dimensions))
    formula_ok = all(
        len(partition) == 3 + sum(sizes[z] - 1 for z in bit)
        for partition, bit in zip(partitions, bits)
        if bit is not None
    )
    check("C2 dimension formula 3 + sum(|Vz|-1)", formula_ok)
    indicator_ranks = [
        exact_rank([[int(i in block) for i in range(sum(sizes))] for block in partition])
        for partition in partitions
    ]
    check("C3 dimensions independently equal exact indicator-span ranks", sorted(indicator_ranks) == dimensions)

    bit_to_partition = {bit: partition for bit, partition in zip(bits, partitions) if bit is not None}
    order_ok = all(
        refines(bit_to_partition[t], bit_to_partition[s]) == (s <= t)
        for s in expected_bits for t in expected_bits
    )
    check("D1 refinement order is Boolean subset order", order_ok)
    meet_join_ok = all(
        partition_for_bits(zone, s & t) in partitions and partition_for_bits(zone, s | t) in partitions
        for s in expected_bits for t in expected_bits
    )
    check("D2 meet/intersection and join/union stay in the eight-object family", meet_join_ok)
    check("D3 bottom is three whole zones", len(bit_to_partition[frozenset()]) == 3)
    check("D4 top is the discrete 33-block partition", len(bit_to_partition[frozenset({0, 1, 2})]) == 33)

    p11 = bit_to_partition[frozenset({0})]
    check("E1 named second object P11 exists", len(p11) == 11 and p11 != bit_to_partition[frozenset()])
    check("E2 trap-d guard: dim 11 is 9+1+1 only", len(p11) == sizes[0] + 1 + 1)


def run_selftests() -> None:
    print("\nSELFTEST: each mutant must fail a conclusion")
    # Full-GraphAut orbit unions happen to make symmetry/transitivity redundant on
    # the real three-zone degree-separated carrier. Use a deliberately asymmetric
    # relation to check those predicates themselves, rather than pretending the
    # real-scene count depends on clauses it does not need.
    asymmetric = {(0, 0), (1, 1), (0, 1)}
    check(
        "M1 symmetry clause rejects a reflexive asymmetric relation",
        not relation_is_equivalence(asymmetric, 2)
        and relation_is_equivalence(asymmetric, 2, require_symmetry=False),
    )
    nontransitive = {(0, 0), (1, 1), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)}
    check(
        "M2 transitivity clause rejects a reflexive symmetric non-equivalence",
        not relation_is_equivalence(nontransitive, 3)
        and relation_is_equivalence(nontransitive, 3, require_transitivity=False),
    )
    _, _, _, _, _, no_sep = enumerate_stable_partitions((3, 4, 5), separates_degree=False)
    check("M3 replacing degree-separation by True admits extra objects", len(no_sep) != 8, f"computed {len(no_sep)}")

    _, _, degree, _, _, correct = enumerate_stable_partitions((2, 2, 3))
    _, _, _, _, _, dropped = enumerate_stable_partitions((2, 2, 3), drop_equal_zone_swaps=True)
    check("M4 dropping equal-zone swap changes repeated-size conclusion", len(correct) != len(dropped), f"full={len(correct)}, dropped={len(dropped)}, degrees={sorted(set(degree))}")

    _, _, _, _, _, mutated = enumerate_stable_partitions((9, 12, 13))
    mutated_dims = sorted(len(p) for p in mutated)
    check("M5 mutating a zone size breaks the frozen dimension set", mutated_dims != [3, 11, 13, 15, 21, 23, 25, 33], str(mutated_dims))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    run_real_scene()
    if args.selftest:
        run_selftests()
    print(f"\nchecks passed: {len(PASSES)}; failed: {len(FAILURES)}")
    if FAILURES:
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
