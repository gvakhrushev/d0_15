"""Independent finite controls for the relational repair theorem; standard library only."""
from itertools import product
import json
from pathlib import Path

supports = tuple(frozenset(i for i in range(2) if mask & (1 << i)) for mask in range(4))
swap = lambda s: frozenset(1 - i for i in s)
key = lambda a, b: (tuple(sorted(a)), tuple(sorted(b)))
orbit = lambda a, b: min(key(a, b), key(swap(a), swap(b)))
pairs = tuple(product(supports, repeat=2))
orbits = {orbit(a, b) for a, b in pairs}
assert len(orbits) == 10
assert len({(len(a), len(b)) for a, b in pairs}) == 9
for a, b in pairs:
    assert len(a ^ b) == len(a) + len(b) - 2 * len(a & b)
    for c, d in pairs:
        assert (orbit(a, b) == orbit(c, d)) == (
            (len(a), len(b), len(a & b)) == (len(c), len(d), len(c & d)))

# Full inputs are the existing two triples (member,value,history); equality
# reads retained history bits. Other current bits remain part of the input.
observations = tuple(product((False, True), repeat=3))
same_results, opposite_results = set(), set()
for left, right in product(observations, repeat=2):
    same_results.add(left[2] == left[2])
    opposite_results.add(left[2] == right[2])
assert same_results == {True} and opposite_results == {False, True}

checked_packets = 0
for n in range(9):
    joint_orbits = set()
    for packet in product((0, 1), repeat=n + 1):
        anchor, *readings = packet
        relative = tuple(anchor ^ x for x in readings)
        recorded = (anchor, *relative)
        restored = (recorded[0], *(recorded[0] ^ x for x in recorded[1:]))
        assert restored == packet
        flipped = tuple(1 ^ x for x in packet)
        assert relative == tuple(flipped[0] ^ x for x in flipped[1:])
        joint_orbits.add(relative)
        checked_packets += 1
    assert len(joint_orbits) == 2 ** n

result = dict(status="PASS", support_pair_orbits=10, marginal_rank_pairs=9,
              overlap_classification="exact for two sides", full_observation_pairs=64,
              reversible_packets_checked=checked_packets, largest_relative_bits=8,
              scope="finite controls; all-n capacity theorem proved separately in Lean")
Path(__file__).with_name("verification.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
