#!/usr/bin/env python3
"""Exact checks for dim_R V_k at r=128, k=8 and k=128.

The checks count Hermitian shell matrices. They do not build a field operator
and they do not rank a native field-to-shell map.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import vk_dimension as vk


FAILURES = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILURES.append(name)


def _dot(row, vector) -> Fraction:
    return sum((a * b for a, b in zip(row, vector)), Fraction(0))


def _occupied_subsets(r: int):
    labels = range(r)
    for k in range(1, r + 1):
        for occupied in combinations(labels, k):
            yield occupied


def test_required_integers() -> None:
    check("literal k=8", 2 * 128 * 8 - 8 * 8 - 1 == 1983)
    check("literal k=128", 2 * 128 * 128 - 128 * 128 - 1 == 16383)
    check("closed k=8", vk.closed_form(128, 8) == 1983)
    check("closed k=128", vk.closed_form(128, 128) == 16383)
    check("pivot k=8", vk.pivot_count(128, 8) == 1983)
    check("pivot k=128", vk.pivot_count(128, 128) == 16383)
    check("codim k=8", vk.codimension_form(128, 8) == 1983)
    check("codim k=128", vk.codimension_form(128, 128) == 16383)
    # k=8: free diagonal 7, occupied off-diagonal 56, bridge 1920.
    check("parts k=8", (8 - 1) + (8 * 7) + (2 * 120 * 8) == 1983)
    # k=128: Pi = P, bridge is empty, traceless Hermitian matrices.
    check("parts k=128", (128 - 1) + (128 * 127) + 0 == 16383)
    check("shell square minus complement k=8", 128 * 128 - 120 * 120 - 1 == 1983)
    check("shell square minus complement k=128", 128 * 128 - 0 - 1 == 16383)
    check("full shell is traceless", vk.closed_form(128, 128) == 128 * 128 - 1)


def test_expression_identity() -> None:
    for r in range(1, 33):
        for k in range(1, r + 1):
            if vk.pivot_count(r, k) != vk.closed_form(r, k):
                check("identity r=%s k=%s" % (r, k), False)
                return
            if vk.codimension_form(r, k) != vk.closed_form(r, k):
                check("codim identity r=%s k=%s" % (r, k), False)
                return
    check("three expressions agree for 1 <= k <= r <= 32", True)
    check("layout r=8", vk.coordinate_layout_ok(8))
    check("layout r=128", vk.coordinate_layout_ok(128))


def test_domain() -> None:
    for args in ((128, 0), (128, 129), (0, 1), (-1, 1)):
        try:
            vk.closed_form(*args)
            check("reject %s" % (args,), False)
        except ValueError:
            check("reject %s" % (args,), True)
        except Exception as exc:  # noqa: BLE001 — domain must be ValueError
            check("reject %s (%s)" % (args, type(exc).__name__), False)
    try:
        vk.closed_form(True, 1)  # type: ignore[arg-type]
        check("reject bool", False)
    except TypeError:
        check("reject bool", True)


def test_coordinate_kernel() -> None:
    for r in range(1, 7):
        for occupied in _occupied_subsets(r):
            k = len(occupied)
            m = r - k
            block_rank, full_rank = vk.constraint_split_ranks(r, occupied)
            nullity = r * r - full_rank
            if block_rank != m * m or full_rank != m * m + 1 or nullity != vk.closed_form(r, k):
                check(
                    "coordinate r=%s occupied=%s block=%s full=%s null=%s"
                    % (r, occupied, block_rank, full_rank, nullity),
                    False,
                )
                return
    check("coordinate Phi rank is m^2+1 for every occupied set, r<=6", True)

    # k=0 makes the trace redundant. The closed form is not applied.
    block_rank, full_rank = vk.constraint_split_ranks(4, ())
    check("k=0 block rank", block_rank == 16 and full_rank == 16)
    check("k=0 nullity", vk.coordinate_nullity(4, ()) == 0)


def test_standard_basis_spans_kernel() -> None:
    for r in range(1, 7):
        for k in range(1, r + 1):
            basis = vk.standard_kernel_basis(r, k)
            rows = vk.coordinate_constraint_rows(r, tuple(range(k)))
            if len(basis) != vk.closed_form(r, k):
                check("basis count r=%s k=%s" % (r, k), False)
                return
            if any(_dot(row, vector) != 0 for vector in basis for row in rows):
                check("basis in kernel r=%s k=%s" % (r, k), False)
                return
            if vk._row_rank(basis) != len(basis):
                check("basis independent r=%s k=%s" % (r, k), False)
                return
            for vector in basis:
                real, imag = vk.realize(r, vector)
                trace = sum(real[i][i] for i in range(r))
                if trace != 0:
                    check("basis trace r=%s k=%s" % (r, k), False)
                    return
                for i in range(r):
                    if imag[i][i] != 0:
                        check("basis hermitian diagonal r=%s k=%s" % (r, k), False)
                        return
                    for j in range(r):
                        if real[j][i] != real[i][j] or imag[j][i] != -imag[i][j]:
                            check("basis hermitian r=%s k=%s" % (r, k), False)
                            return
                for i in range(k, r):
                    for j in range(k, r):
                        if real[i][j] != 0 or imag[i][j] != 0:
                            check("basis block r=%s k=%s" % (r, k), False)
                            return
    check("standard basis is a real basis of V_k for r<=6", True)


def test_surjectivity_witness() -> None:
    """Hit every Hermitian direction on the complement and the trace axis."""
    for r in range(1, 6):
        for occupied in _occupied_subsets(r):
            occupied = tuple(occupied)
            unoccupied = tuple(i for i in range(r) if i not in occupied)
            anchor = occupied[0]
            width = r * r
            zero = [Fraction(0)] * width
            targets = []
            for index in unoccupied:
                vector = [Fraction(0)] * width
                vector[index] = Fraction(1)
                targets.append(vector)
            for pos, i in enumerate(unoccupied):
                for j in unoccupied[pos + 1 :]:
                    a, b = (i, j) if i < j else (j, i)
                    real_index, imag_index = vk.coordinate_index_pair(r, a, b)
                    real_vector = [Fraction(0)] * width
                    imag_vector = [Fraction(0)] * width
                    real_vector[real_index] = Fraction(1)
                    imag_vector[imag_index] = Fraction(1)
                    targets.append(real_vector)
                    targets.append(imag_vector)
            if len(targets) != (r - len(occupied)) ** 2:
                check("witness basis count r=%s occ=%s" % (r, occupied), False)
                return

            def shift_trace(vector, trace_target):
                shifted = [Fraction(value) for value in vector]
                real, _imag = vk.realize(r, shifted)
                current = sum((real[i][i] for i in range(r)), Fraction(0))
                shifted[anchor] += Fraction(trace_target) - current
                return shifted

            for target in targets:
                vector = shift_trace(target, 0)
                if not _matches(r, vector, unoccupied, target, 0):
                    check("witness block r=%s occ=%s" % (r, occupied), False)
                    return
            trace_vector = shift_trace(zero, 1)
            if not _matches(r, trace_vector, unoccupied, zero, 1):
                check("witness trace r=%s occ=%s" % (r, occupied), False)
                return
    check("trace is independent and the complement block is hit, r<=5", True)


def _matches(r, vector, unoccupied, target, trace_target) -> bool:
    """Phi(S) = (C, tau). Bridge and occupied blocks stay free apart from the trace."""
    real, imag = vk.realize(r, vector)
    target_real, target_imag = vk.realize(r, target)
    trace = sum((real[i][i] for i in range(r)), Fraction(0))
    if trace != Fraction(trace_target):
        return False
    for i in unoccupied:
        for j in unoccupied:
            if real[i][j] != target_real[i][j] or imag[i][j] != target_imag[i][j]:
                return False
    return True


def test_tilted_projectors() -> None:
    samples = [
        [[1, 1, 0]],
        [[1, 1, 1]],
        [[1, 1, 1, 1]],
        [[1, 0, 0], [0, 1, 1]],
        [[1, 1, 0, 0], [1, -1, 0, 0]],
        [[1, 0, 0, 0], [0, 1, 1, 1]],
    ]
    for vectors in samples:
        pi = vk.projector_from_orthogonal_vectors(vectors)
        rank = vk.assert_orthogonal_projector(pi)
        size = len(pi)
        got = vk.projector_nullity(pi)
        expect = vk.closed_form(size, rank)
        # Coordinate projector with the same rank must agree with the fast path.
        coordinate = vk.coordinate_nullity(size, tuple(range(rank)))
        check(
            "tilted r=%s k=%s dim=%s" % (size, rank, got),
            got == expect and coordinate == expect,
        )
    # A coordinate projector reproduced by the general matrix path.
    pi = vk.projector_from_orthogonal_vectors([[1, 0, 0], [0, 1, 0]])
    rows = vk.projector_constraint_rows(pi)
    fast = vk.coordinate_constraint_rows(3, (0, 1))
    check(
        "general path matches coordinate path",
        vk._row_rank(rows) == vk._row_rank(fast) == 1 * 1 + 1,
    )


def test_negative_controls() -> None:
    def real_symmetric(r, k):
        return k * (k + 1) // 2 + (r - k) * k - 1

    def forget_trace(r, k):
        return 2 * r * k - k * k

    def one_real_bridge(r, k):
        return k * k + (r - k) * k - 1

    def traceless_only(r):
        return r * r - 1

    def trace_as_two_reals(r, k):
        return 2 * r * k - k * k - 2

    check("real symmetric k=8", real_symmetric(128, 8) == 995 and 995 != 1983)
    check("real symmetric k=128", real_symmetric(128, 128) == 8255 and 8255 != 16383)
    check("forget trace k=8", forget_trace(128, 8) == 1984 and 1984 != 1983)
    check("forget trace k=128", forget_trace(128, 128) == 16384 and 16384 != 16383)
    check("one real bridge k=8", one_real_bridge(128, 8) == 1023 and 1023 != 1983)
    check("traceless only misses k=8", traceless_only(128) == 16383 and 16383 != 1983)
    check("trace counted twice k=8", trace_as_two_reals(128, 8) == 1982)
    check("trace counted twice k=128", trace_as_two_reals(128, 128) == 16382)
    # k=r collides with some wrong counts; k=8 separates them.
    check(
        "k=r collisions do not survive k=8",
        one_real_bridge(128, 128) == 16383 and traceless_only(128) == 16383,
    )


def test_no_field_operator() -> None:
    source = Path(vk.__file__).read_text(encoding="utf-8")
    for token in ("X_v", "T_k", "Feshbach", "kappa", "Delta", "field_to_shell"):
        if token in source:
            check("source has no %s" % token, False)
            return
    check("module builds no field operator", True)
    check("public count is the shell dimension", vk.certified_pair(128, 8) == 1983)


def main() -> int:
    test_required_integers()
    test_expression_identity()
    test_domain()
    test_coordinate_kernel()
    test_standard_basis_spans_kernel()
    test_surjectivity_witness()
    test_tilted_projectors()
    test_negative_controls()
    test_no_field_operator()
    if FAILURES:
        print("FAILED %s" % ", ".join(FAILURES))
        return 1
    if vk.main() != 0:
        print("FAILED module main")
        return 1
    print("PASS vk dimension 1983 and 16383")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
