"""Exact equal-length inverse on the original directed scene with one-step memory."""

from collections import Counter, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def shortest(start, neighbors):
    paths = {start: [start]}
    queue = deque([start])
    while queue:
        here = queue.popleft()
        for other in neighbors[here]:
            if other not in paths:
                paths[other] = paths[here] + [other]
                queue.append(other)
    return paths


def main():
    parts = (tuple(range(9)), tuple(range(9, 20)), tuple(range(20, 33)))
    zone = {v: i for i, part in enumerate(parts) for v in part}
    states = [(u, v) for u, v in product(range(33), repeat=2) if zone[u] != zone[v]]
    successors = {(u, v): [(v, w) for w in range(33) if zone[v] != zone[w]]
                  for u, v in states}
    predecessors = {(v, w): [(u, v) for u in range(33) if zone[u] != zone[v]]
                    for v, w in states}
    arcs = [(x, y) for x in states for y in successors[x]]
    arc_set = set(arcs)
    require(len(states) == 718 and len(arcs) == 15708, "Wrong primary graph")
    hidden = [(x, y) for x, y in arcs if x[0] != y[1] and zone[x[0]] == zone[y[1]]]
    require(len(hidden) == 7268, "Wrong unseen contextual support")

    root = (0, 9)
    outward = shortest(root, successors)
    inward = {x: list(reversed(path)) for x, path in shortest(root, predecessors).items()}
    radius = max(len(path) - 1 for path in (*outward.values(), *inward.values()))
    require(len(outward) == len(inward) == 718 and radius == 3, "Bad physical routes")
    back = [root, (9, 0), root]
    tri = [root, (9, 20), (20, 0), root]

    # Any exact log-weight table is allowed. Exercise all edges with signed,
    # nonconstant integer scores, keeping the same lifted root in every test.
    weight = {(x, y): (19*x[0]+23*x[1]+31*y[1]+x[0]*y[1]) % 137 - 66 for x, y in arcs}

    def join(*paths):
        out = []
        for path in paths:
            if out:
                require(out[-1] == path[0], "Different retained address at stitch")
                out.extend(path[1:])
            else:
                out.extend(path)
        return out

    def cost(path):
        return sum(weight[pair] for pair in zip(path, path[1:]))

    def pad(path):
        left = 9 - (len(path)-1)
        n3 = left % 2
        n2 = (left-3*n3)//2
        require(n2 >= 0 and n3 >= 0, "No exact same-length padding")
        wrapped = join(path, *([back]*n2), *([tri]*n3))
        require(len(wrapped)-1 == 9 and wrapped[0] == wrapped[-1] == root,
                "Reference layout changed")
        return wrapped, n2

    anchor = join(tri, tri, tri)
    calibration = join(back, back, back, tri)
    delta = cost(calibration)-cost(anchor)
    require(delta == 3*cost(back)-2*cost(tri), "Wrong 6-step calibration")
    source_times_three = cost(tri)

    def residual3(path):
        padded, n2 = pad(path)
        return 3*(cost(padded)-cost(anchor))-n2*delta

    bases = {x: join(outward[x], inward[x]) for x in states}
    max_closed = 0
    digest = sha256()
    for x, y in arcs:
        test = join(outward[x], [x, y], inward[y])
        max_closed = max(max_closed, len(test)-1)
        actual = residual3(test)-residual3(bases[y])
        length_difference = 1+len(outward[x])-len(outward[y])
        predicted = 3*(weight[x, y]+cost(outward[x])-cost(outward[y]))
        predicted -= length_difference*source_times_three
        require(actual == predicted, "Failed to reconstruct a contextual edge")
        digest.update((str((x, y, actual))+"\n").encode())
    require(max_closed == 7, "The short route length changed")

    witness = [root, (9, 1), (1, 9), (9, 0), root]
    hidden_key = (root, (9, 1))
    require(all(e in arc_set for e in zip(witness, witness[1:])), "Bad physical square")
    require(list(zip(witness, witness[1:])).count(hidden_key) == 1, "Hidden witness mismatch")

    Z = "ABAUUABA"
    def macro_counts(body):
        return Counter(zip("A"+body, body))
    expected_counts = Counter({("A", "A"): 4, ("A", "B"): 4, ("B", "A"): 4,
                               ("A", "U"): 2, ("U", "A"): 2, ("U", "U"): 2})
    require(macro_counts(Z+Z+"AA") == macro_counts(Z+"A"+Z+"A") == expected_counts,
            "A68 macro occupation mismatch")
    ledger = Counter()
    for word, multiplicity in (("A", 4), ("BA", 4), ("UUA", 2)):
        for edge, count in macro_counts(word).items():
            ledger[edge] += multiplicity*count
    require(ledger == expected_counts, "Four-event A68 calibration mismatch")
    backtracks = len(states)//2
    oriented_triangles = 2*9*11*13
    abs_rank = backtracks+oriented_triangles
    result = {
        "original_scene": "K(9,11,13)",
        "context_states": len(states),
        "context_arcs": len(arcs),
        "unseen_in_any_old_2_or_3_cycle": len(hidden),
        "old_cycle_rank_before_bin_normalization": abs_rank,
        "old_cycle_rank_after_bin_normalization": abs_rank-1,
        "remaining_old_modes_modulo_context_endpoint_gauge": len(arcs)-717-(abs_rank-1),
        "new_equal_length_rank": len(arcs)-717-1,
        "base_root_context": list(root),
        "maximum_unpadded_route": max_closed,
        "all_primary_padded_words_have_length": 9,
        "Q8_single_class_safe_replayed_length": 36,
        "exact_reconstruction_checked_on_arcs": len(arcs),
        "reconstructed_integer_witness_sha256": digest.hexdigest(),
        "A68_shared_macro_body_ratio_checked": True,
        "physical_scene_to_H1_context_binding_closed": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
