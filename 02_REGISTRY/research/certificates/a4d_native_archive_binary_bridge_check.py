#!/usr/bin/env python3
"""Exact cofinal binary quotient of the existing flattened archive tower.

No repository mutation, no new gate or action, no assumed physical measure.
Default replay compares an immutable adjacent JSON ledger. --output writes one.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


INPUTS = (
    "03_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseCarrier.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveLaplacianRG.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveLightProfinite.lean",
    "03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean",
)


def mass_mul(x, y):
    # Q[p]/(p^2+p-1): (a+bp)(c+dp)=(ac+bd)+(ad+bc-bd)p.
    a, b = x
    c, d = y
    return a * c + b * d, a * d + b * c - b * d


def mass_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mass_scale(c, x):
    return c * x[0], c * x[1]


def cylinder(word):
    mass = (1, 0)
    for bit in word:
        mass = mass_mul(mass, (0, 1) if bit == 0 else (1, -1))
    return mass


def next_level(n):
    # L=n+2 divisible by 4; N=L^2+1; new level N+1.
    return (n + 2) ** 2 + 2


def modes(n):
    return (n + 2) ** 4


def projection(x, fine, coarse):
    assert 0 <= x < modes(fine)
    assert 0 <= coarse <= fine
    for j in range(fine - 1, coarse - 1, -1):
        x %= modes(j)
    return x


def encoded(word, levels):
    x = 0
    for k, bit in enumerate(word):
        x += bit * modes(levels[k + 1] - 1)
        assert x < modes(levels[k + 1])
    return x


def beta(x, k, levels):
    if k == 0:
        return ()
    cutoff = modes(levels[k] - 1)
    bit = int(x >= cutoff)
    old = projection(x, levels[k], levels[k - 1])
    return beta(old, k - 1, levels) + (bit,)


def run(repo):
    bindings = {}
    for name in INPUTS:
        data = (repo / name).read_bytes()
        bindings[name] = hashlib.sha256(data).hexdigest()
    raw = (repo / INPUTS[0]).read_text()
    assert "def archiveFibers (n : Nat) : Nat := n + 2" in raw
    assert "x.val % (archiveTower n).modes" in raw
    role = (repo / INPUTS[1]).read_text()
    assert "fun x r => archiveRGPhaseProjection n (x r)" in role
    phase = (repo / INPUTS[2]).read_text()
    assert "x.val % (archiveFibers n)" in phase

    levels = [2]
    for _ in range(4):
        levels.append(next_level(levels[-1]))
    inequalities = []
    for old, new in zip(levels, levels[1:]):
        assert (old + 2) % 4 == 0 and (new + 2) % 4 == 0
        cutoff, delta = modes(new - 1), modes(new) - modes(new - 1)
        assert cutoff > modes(old)
        assert delta >= modes(old)
        assert modes(old) - 1 + cutoff < modes(new)
        inequalities.append({"old_level": old, "new_level": new,
                             "old_modes": modes(old), "branch_cutoff": cutoff,
                             "new_modes": modes(new), "new_tail": delta})

    sections, full_projection_checks, weight_checks = [], 0, 0
    for k in range(4):
        total = (0, 0)
        for word in itertools.product((0, 1), repeat=k):
            x = encoded(word, levels)
            assert beta(x, k, levels) == word
            sections.append({"word": list(word), "level": levels[k], "point": x})
            total = mass_add(total, cylinder(word))
            if k:
                assert projection(x, levels[k], levels[k - 1]) == encoded(word[:-1], levels)
                full_projection_checks += 1
            for bit in (0, 1):
                child = encoded(word + (bit,), levels)
                # First native successor map sends the B-child to x; remaining
                # maps fix x since x<modes(old). This avoids enormous loops.
                assert child % modes(levels[k + 1] - 1) == x
                assert x < modes(levels[k])
            assert mass_add(cylinder(word + (0,)), cylinder(word + (1,))) == cylinder(word)
            weight_checks += 1
        assert total == (1, 0)

    # Surjection is not merely onto the selected section: at k=1 check every
    # actual finite archive point and its recursively assigned word.
    histogram = {"0": 0, "1": 0}
    fibers = [[0, 0] for _ in range(modes(levels[0]))]
    for x in range(modes(levels[1])):
        label = beta(x, 1, levels)[0]
        histogram[str(label)] += 1
        y = projection(x, levels[1], levels[0])
        fibers[y][label] += 1
    assert all(histogram.values())
    assert all(a > 0 and b > 0 for a, b in fibers)

    # Full-support native kernel, not a supported section measure:
    # K(y,x)=p_bit/N_ybit on its actual composite-modulo fiber.
    golden = [(Fraction(0), Fraction(1)), (Fraction(1), Fraction(-1))]
    measure_total = (Fraction(0), Fraction(0))
    golden_pushforward = [(Fraction(0), Fraction(0)) for _ in range(2)]
    kernel_checks = 0
    for counts in fibers:
        conditional = [mass_scale(Fraction(1, counts[b]), golden[b]) for b in range(2)]
        row_mass = (Fraction(0), Fraction(0))
        for b in range(2):
            bit_mass = mass_scale(counts[b], conditional[b])
            assert bit_mass == golden[b]
            row_mass = mass_add(row_mass, bit_mass)
            golden_pushforward[b] = mass_add(golden_pushforward[b],
                mass_scale(Fraction(1, len(fibers)), bit_mass))
        assert row_mass == (1, 0)
        measure_total = mass_add(measure_total, mass_scale(Fraction(1, len(fibers)), row_mass))
        kernel_checks += 1
    assert measure_total == (1, 0) and golden_pushforward == golden

    # Exact conditional-expectation intertwiner for all old native fibers
    # and the full two-dimensional golden fine space. Also test a genuine
    # nonconstant native detail channel orthogonal to the binary pullback.
    conditional_operator_checks = 0
    for counts in fibers:
        for basis_bit in range(2):
            left = mass_scale(counts[basis_bit],
                mass_scale(Fraction(1, counts[basis_bit]), golden[basis_bit]))
            assert left == golden[basis_bit]
            conditional_operator_checks += 1
    # Weighted-value golden D=3JP+5(I-JP)=5I-2JP. The kernel computation
    # gives P_native D_tilde(y,x')/mu_fine(x')=5-2=3 for every source bit.
    # Independent response check uses D^2=9JP+25(I-JP)=25I-16JP.
    D = [[mass_add((5 if i == j else 0, 0), mass_scale(-2, golden[j]))
          for j in range(2)] for i in range(2)]
    R = [[mass_add((25 if i == j else 0, 0), mass_scale(-16, golden[j]))
          for j in range(2)] for i in range(2)]
    for i, j in itertools.product(range(2), repeat=2):
        square = (0, 0)
        for a in range(2):
            square = mass_add(square, mass_mul(D[i][a], D[a][j]))
        assert square == R[i][j]
    for j in range(2):
        pd, pr = (0, 0), (0, 0)
        for i in range(2):
            pd = mass_add(pd, mass_mul(golden[i], D[i][j]))
            pr = mass_add(pr, mass_mul(golden[i], R[i][j]))
        assert pd == mass_scale(3, golden[j])
        assert pr == mass_scale(9, golden[j])
    native_detail = [1, -1] + [0] * (len(fibers) - 2)
    for b in range(2):
        overlap = (0, 0)
        for y, counts in enumerate(fibers):
            conditional = mass_scale(Fraction(1, counts[b]), golden[b])
            overlap = mass_add(overlap, mass_scale(
                Fraction(native_detail[y] * counts[b], len(fibers)), conditional))
        assert overlap == (0, 0)
    # Uniform conditional disintegration does NOT yield golden weights.
    uniform_conditional_A = Fraction(fibers[0][0], sum(fibers[0]))
    assert uniform_conditional_A ** 2 + uniform_conditional_A - 1 != 0

    # Actual Role-coordinate projection is x mod L, not the flattened map.
    # Every compatible finite coordinate path equals zero until its first
    # positive m, then equals m for every remaining refinement level.
    role_cases = []
    for last_L in range(3, 13):
        for last in range(last_L):
            path = [last]
            for L in range(last_L - 1, 1, -1):
                path.append(path[-1] % L)
            path.reverse()
            positive = [(L, x) for L, x in zip(range(2, last_L + 1), path) if x]
            if positive:
                m = positive[0][1]
                assert all(x == m for _, x in positive)
                assert all(x == 0 for x in path[:positive[0][0] - 2])
            role_cases.append({"last_L": last_L, "last": last, "path": path})
    # Zero has two immediate lifts, positive coordinates exactly one.
    for L in range(2, 65):
        counts = [sum(x % L == y for x in range(L + 1)) for y in range(L)]
        assert counts == [2] + [1] * (L - 1)
    flat_fiber = sum(x % 16 == 0 for x in range(81))
    product_fiber = 2 ** 4
    assert flat_fiber == 6 and product_fiber == 16

    # Records may be singletons. The quotient handles both cases without
    # assigning distinct physical states to a singleton output.
    sample_records = [(Fraction(-3, 8), Fraction(-1, 4)),
                      (Fraction(1, 7),),
                      (Fraction(2, 5), Fraction(1, 2))]
    record_checks = 0
    for k in range(1, 4):
        realized = set()
        for word in itertools.product((0, 1), repeat=k):
            point = encoded(word, levels)
            read = tuple(B[beta(point, k, levels)[j] if len(B) == 2 else 0]
                         for j, B in enumerate(sample_records[:k]))
            realized.add(read)
            if k > 1:
                old = projection(point, levels[k], levels[k - 1])
                old_read = tuple(B[beta(old, k - 1, levels)[j] if len(B) == 2 else 0]
                                 for j, B in enumerate(sample_records[:k - 1]))
                assert old_read == read[:-1]
            record_checks += 1
        assert realized == set(itertools.product(*sample_records[:k]))

    # Existing site counting weights do not give golden cylinder weights.
    # Histogram probabilities are rational; p has irreducible polynomial
    # p^2+p-1. The section PUSHFORWARD measure is an explicit new choice,
    # never an identity with native counting measure.
    uniform_A = Fraction(histogram["0"], modes(levels[1]))
    assert uniform_A ** 2 + uniform_A - 1 != 0
    return {"status": "PASS", "input_sha256": bindings,
            "cofinal_levels": levels, "cofinal_L": [n + 2 for n in levels],
            "inequalities": inequalities, "section_points": sections,
            "full_composite_projection_checks": full_projection_checks,
            "golden_cylinder_checks": weight_checks,
            "first_quotient_fiber_histogram": histogram,
            "native_bit_fiber_counts": fibers,
            "full_support_kernel_rows_checked": kernel_checks,
            "conditional_operator_basis_checks": conditional_operator_checks,
            "full_support_golden_pushforward": [[str(c) for c in x] for x in golden_pushforward],
            "uniform_conditional_A_at_zero": str(uniform_conditional_A),
            "native_measure_constructed_not_identified": True,
            "record_checks": record_checks,
            "role_finite_path_checks": len(role_cases),
            "role_path_control_examples": role_cases[-12:],
            "native_flat_fiber": flat_fiber, "native_product_fiber": product_fiber,
            "uniform_A_probability": str(uniform_A),
            "uniform_measure_equals_golden": False,
            "physical_action_or_gate_transfer_claimed": False}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = run(args.repo)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        expected = Path(__file__).with_name("a4d_native_archive_binary_bridge_results.json")
        assert json.loads(expected.read_text()) == result, "Immutable ledger mismatch"
    print(json.dumps({"status": "PASS", "cofinal_L": result["cofinal_L"],
                      "physical_action_or_gate_transfer_claimed": False}))


if __name__ == "__main__":
    main()
