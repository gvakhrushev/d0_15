#!/usr/bin/env python3
"""Real dimension of the shell-condition space V_k.

Carrier: Hermitian endomorphisms of an r-dimensional eigenshell.
Pi is an orthogonal projector of rank k inside that shell, 1 <= k <= r.
V_k = {S = S* : Tr S = 0 and (P - Pi) S (P - Pi) = 0}.

dim_R V_k = 2*r*k - k*k - 1.
This is not the rank of a field-to-shell map. No field operator is built.
"""
from __future__ import annotations

from fractions import Fraction

SHELL_RANK = 128
CERTIFIED_DIMENSIONS = {8: 1983, 128: 16383}


def require_shell_ranks(r: int, k: int) -> None:
    if type(r) is not int or type(k) is not int:
        raise TypeError("r and k must be integers")
    if r < 1 or k < 1 or k > r:
        raise ValueError("need integers 1 <= k <= r, got r=%s k=%s" % (r, k))


def closed_form(r: int, k: int) -> int:
    """2*r*k - k*k - 1."""
    require_shell_ranks(r, k)
    return 2 * r * k - k * k - 1


def pivot_count(r: int, k: int) -> int:
    """Free Hermitian coordinates after the unoccupied block and the trace.

    Occupied diagonal is fixed by the trace except for k-1 entries.
    Each complex occupied off-diagonal entry and each complex bridge entry
    contributes two real coordinates. The unoccupied block is absent.
    """
    require_shell_ranks(r, k)
    free_diagonal = k - 1
    occupied_off = k * (k - 1)
    bridge = 2 * (r - k) * k
    return free_diagonal + occupied_off + bridge


def codimension_form(r: int, k: int) -> int:
    """dim Herm(C^r) minus dim Herm(unoccupied) minus one real trace."""
    require_shell_ranks(r, k)
    unoccupied = r - k
    return r * r - unoccupied * unoccupied - 1


def coordinate_index_pair(r: int, i: int, j: int) -> tuple:
    """Real and imaginary coordinates of the Hermitian pair i < j."""
    if not (0 <= i < j < r):
        raise ValueError("pair requires 0 <= i < j < r")
    before = 0
    for a in range(i):
        before += r - a - 1
    before += j - i - 1
    real_index = r + 2 * before
    return real_index, real_index + 1


def coordinate_layout_ok(r: int) -> bool:
    if type(r) is not int or r < 1:
        return False
    seen = set(range(r))
    for i in range(r):
        for j in range(i + 1, r):
            real_index, imag_index = coordinate_index_pair(r, i, j)
            if real_index in seen or imag_index in seen or imag_index != real_index + 1:
                return False
            seen.add(real_index)
            seen.add(imag_index)
    return seen == set(range(r * r))


def realize(r: int, coords) -> tuple:
    """Hermitian matrix (real part, imaginary part) from real coordinates."""
    if len(coords) != r * r:
        raise ValueError("coordinate length must be r*r")
    real = [[Fraction(0) for _ in range(r)] for _ in range(r)]
    imag = [[Fraction(0) for _ in range(r)] for _ in range(r)]
    for i in range(r):
        real[i][i] = Fraction(coords[i])
    for i in range(r):
        for j in range(i + 1, r):
            real_index, imag_index = coordinate_index_pair(r, i, j)
            real[i][j] = Fraction(coords[real_index])
            real[j][i] = Fraction(coords[real_index])
            imag[i][j] = Fraction(coords[imag_index])
            imag[j][i] = -Fraction(coords[imag_index])
    return real, imag


def _zeros(n: int):
    return [Fraction(0)] * n


def _row_rank(rows) -> int:
    live = [row[:] for row in rows if any(entry != 0 for entry in row)]
    if not live:
        return 0
    width = len(live[0])
    rank = 0
    col = 0
    while rank < len(live) and col < width:
        pivot = None
        for i in range(rank, len(live)):
            if live[i][col] != 0:
                pivot = i
                break
        if pivot is None:
            col += 1
            continue
        live[rank], live[pivot] = live[pivot], live[rank]
        pivot_value = live[rank][col]
        for i in range(len(live)):
            if i == rank or live[i][col] == 0:
                continue
            factor = live[i][col] / pivot_value
            for j in range(col, width):
                live[i][j] -= factor * live[rank][j]
        rank += 1
        col += 1
    return rank


def coordinate_constraint_rows(r: int, occupied) -> list:
    """Rows of Phi(S) = ((P-Pi)S(P-Pi), Tr S) in the coordinate Hermitian basis.

    `occupied` is the set of basis labels of im Pi. Pi need not be the
    leading coordinate block. The trace row is last.
    """
    if type(r) is not int or r < 1:
        raise ValueError("r must be a positive integer")
    occupied_set = set(occupied)
    if len(occupied_set) != len(tuple(occupied)):
        raise ValueError("occupied labels must be unique")
    if any(type(i) is not int or i < 0 or i >= r for i in occupied_set):
        raise ValueError("occupied labels must lie in 0..r-1")
    width = r * r
    rows = []

    def unit(index: int):
        row = _zeros(width)
        row[index] = Fraction(1)
        return row

    unoccupied = [i for i in range(r) if i not in occupied_set]
    for a in unoccupied:
        rows.append(unit(a))
    for pos, a in enumerate(unoccupied):
        for b in unoccupied[pos + 1 :]:
            i, j = (a, b) if a < b else (b, a)
            real_index, imag_index = coordinate_index_pair(r, i, j)
            rows.append(unit(real_index))
            rows.append(unit(imag_index))
    trace = _zeros(width)
    for i in range(r):
        trace[i] = Fraction(1)
    rows.append(trace)
    return rows


def coordinate_nullity(r: int, occupied) -> int:
    rows = coordinate_constraint_rows(r, occupied)
    return r * r - _row_rank(rows)


def constraint_split_ranks(r: int, occupied) -> tuple:
    """Rank of the unoccupied-block rows, then rank after adding the trace."""
    rows = coordinate_constraint_rows(r, occupied)
    block_rank = _row_rank(rows[:-1])
    full_rank = _row_rank(rows)
    return block_rank, full_rank


def standard_kernel_basis(r: int, k: int) -> list:
    """Explicit real basis of V_k for Pi = span{e_0, ..., e_{k-1}}."""
    require_shell_ranks(r, k)
    width = r * r
    vectors = []
    for t in range(1, k):
        vector = _zeros(width)
        vector[t] = Fraction(1)
        vector[0] = Fraction(-1)
        vectors.append(vector)
    for i in range(k):
        for j in range(i + 1, k):
            real_index, imag_index = coordinate_index_pair(r, i, j)
            real_vector = _zeros(width)
            imag_vector = _zeros(width)
            real_vector[real_index] = Fraction(1)
            imag_vector[imag_index] = Fraction(1)
            vectors.append(real_vector)
            vectors.append(imag_vector)
    for occupied in range(k):
        for unoccupied in range(k, r):
            real_index, imag_index = coordinate_index_pair(r, occupied, unoccupied)
            real_vector = _zeros(width)
            imag_vector = _zeros(width)
            real_vector[real_index] = Fraction(1)
            imag_vector[imag_index] = Fraction(1)
            vectors.append(real_vector)
            vectors.append(imag_vector)
    return vectors


def assert_orthogonal_projector(pi) -> int:
    """Return Tr Pi after checking that Pi is a real orthogonal projector."""
    size = len(pi)
    if size < 1 or any(len(row) != size for row in pi):
        raise ValueError("projector must be square")
    for i in range(size):
        for j in range(size):
            if pi[i][j] != pi[j][i]:
                raise ValueError("projector is not symmetric")
    for i in range(size):
        for j in range(size):
            acc = sum((pi[i][p] * pi[p][j] for p in range(size)), Fraction(0))
            if acc != pi[i][j]:
                raise ValueError("Pi^2 != Pi")
    trace = sum((pi[i][i] for i in range(size)), Fraction(0))
    if trace != int(trace):
        raise ValueError("projector trace is not an integer rank")
    return int(trace)


def projector_from_orthogonal_vectors(vectors) -> list:
    """Real orthogonal projector onto the span of pairwise orthogonal vectors."""
    if not vectors:
        raise ValueError("need at least one vector")
    size = len(vectors[0])
    pi = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for left_index, left in enumerate(vectors):
        if len(left) != size:
            raise ValueError("vector length mismatch")
        norm2 = sum((Fraction(entry) * entry for entry in left), Fraction(0))
        if norm2 == 0:
            raise ValueError("zero vector")
        for right in vectors[left_index + 1 :]:
            inner = sum(
                (Fraction(a) * b for a, b in zip(left, right)),
                Fraction(0),
            )
            if inner != 0:
                raise ValueError("vectors are not orthogonal")
        for i in range(size):
            for j in range(size):
                pi[i][j] += Fraction(left[i]) * left[j] / norm2
    return pi


def _hermitian_symbols(r: int):
    width = r * r
    real = [[_zeros(width) for _ in range(r)] for _ in range(r)]
    imag = [[_zeros(width) for _ in range(r)] for _ in range(r)]
    for i in range(r):
        real[i][i][i] = Fraction(1)
    for i in range(r):
        for j in range(i + 1, r):
            real_index, imag_index = coordinate_index_pair(r, i, j)
            real[i][j][real_index] = Fraction(1)
            real[j][i][real_index] = Fraction(1)
            imag[i][j][imag_index] = Fraction(1)
            imag[j][i][imag_index] = Fraction(-1)
    return real, imag


def _scale(form, factor: Fraction):
    if factor == 0:
        return _zeros(len(form))
    return [factor * entry for entry in form]


def _add(left, right):
    return [a + b for a, b in zip(left, right)]


def _mul_num_sym(number, real, imag):
    size = len(number)
    width = len(real[0][0])
    out_real = [[_zeros(width) for _ in range(size)] for _ in range(size)]
    out_imag = [[_zeros(width) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            acc_real = _zeros(width)
            acc_imag = _zeros(width)
            for p in range(size):
                coeff = number[i][p]
                if coeff == 0:
                    continue
                acc_real = _add(acc_real, _scale(real[p][j], coeff))
                acc_imag = _add(acc_imag, _scale(imag[p][j], coeff))
            out_real[i][j] = acc_real
            out_imag[i][j] = acc_imag
    return out_real, out_imag


def _mul_sym_num(real, imag, number):
    size = len(number)
    width = len(real[0][0])
    out_real = [[_zeros(width) for _ in range(size)] for _ in range(size)]
    out_imag = [[_zeros(width) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            acc_real = _zeros(width)
            acc_imag = _zeros(width)
            for p in range(size):
                coeff = number[p][j]
                if coeff == 0:
                    continue
                acc_real = _add(acc_real, _scale(real[i][p], coeff))
                acc_imag = _add(acc_imag, _scale(imag[i][p], coeff))
            out_real[i][j] = acc_real
            out_imag[i][j] = acc_imag
    return out_real, out_imag


def projector_constraint_rows(pi) -> list:
    """Same Phi, for a real orthogonal projector that need not be coordinate."""
    rank = assert_orthogonal_projector(pi)
    size = len(pi)
    if rank < 1 or rank > size:
        raise ValueError("projector rank must satisfy 1 <= k <= r")
    complement = [
        [
            (Fraction(1) if i == j else Fraction(0)) - pi[i][j]
            for j in range(size)
        ]
        for i in range(size)
    ]
    real, imag = _hermitian_symbols(size)
    sq_real, sq_imag = _mul_sym_num(real, imag, complement)
    block_real, block_imag = _mul_num_sym(complement, sq_real, sq_imag)
    rows = []
    for i in range(size):
        if any(entry != 0 for entry in block_imag[i][i]):
            raise RuntimeError("complement block is not Hermitian")
        rows.append(block_real[i][i])
    for i in range(size):
        for j in range(i + 1, size):
            rows.append(block_real[i][j])
            rows.append(block_imag[i][j])
    trace = _zeros(size * size)
    for i in range(size):
        trace[i] = Fraction(1)
    rows.append(trace)
    return rows


def projector_nullity(pi) -> int:
    size = len(pi)
    return size * size - _row_rank(projector_constraint_rows(pi))


def certified_pair(r: int, k: int) -> int:
    value = closed_form(r, k)
    if pivot_count(r, k) != value or codimension_form(r, k) != value:
        raise RuntimeError("dimension expressions disagree for r=%s k=%s" % (r, k))
    return value


def main() -> int:
    failed = False
    for k, expected in CERTIFIED_DIMENSIONS.items():
        got = certified_pair(SHELL_RANK, k)
        ok = got == expected
        print("dim_R V_k(r=%s, k=%s) = %s" % (SHELL_RANK, k, got))
        if not ok:
            print("FAIL expected %s" % expected)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
