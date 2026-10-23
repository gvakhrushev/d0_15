#!/usr/bin/env python3
"""Equal-weight Hilbert-Schmidt contraction of the golden CAR channel.

The four literal record returns and the pinned two-outcome Kraus rule collapse
to Phi(X) = p X + (p^2/4) sum_r U_r X U_r^T. On traceless Hermitian matrices
the equal-weight Hilbert-Schmidt norm gamma satisfies

    9442/10000 < gamma^2 < 9443/10000 < (49/50)^2,

so gamma < 49/50 < 1. The same norm is not bounded by 49/50 for every
positive return weight. This does not admit the channel, identify I_16/16
with native matter, or close a trace-norm, diamond-norm, or Einstein law.
"""
# D0_CI_TIMEOUT_SECONDS=600
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from itertools import permutations
from pathlib import Path

import sympy as s
from sympy import QQ
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parents[3]
STEM = "a4d_native_golden_channel_hs_contraction"
PROOF = "02_REGISTRY/research/A4D_NATIVE_GOLDEN_CHANNEL_HS_CONTRACTION.md"
CHRONOLOGY = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py"
FOCK = "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py"
PREP = "02_REGISTRY/research/A4D_NATIVE_GOLDEN_CHANNEL_ENDOGENOUS_PREPARATION.md"
PREP_CHECK = "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_check.py"
PREP_RESULT = "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_results.json"
CHRONOLOGY_CERT = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json"
CHRONOLOGY_PROOF = "02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md"

INPUTS = {
    CHRONOLOGY: "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    CHRONOLOGY_CERT: "0b91e13d823568898a006dd468f9963ffbbc1949f0976a21e8530af465ecfbbe",
    CHRONOLOGY_PROOF: "601e5bb9203789a66ad2a945aad30da92b6233ac40417d54c6b47c95dc43536b",
    FOCK: "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    PREP: "73187cd2a77d3350b01a29f780d939a0a86b2e65c4622b85dc6b18ca283f7df9",
    PREP_CHECK: "d78de07609370a307f30d1daeec9d45dd81de1eb7558654105ef32dc51ba89dd",
    PREP_RESULT: "13be7f995f36fb53bd837b43aaca51546b124a65aeb81ce840e06d951891c000",
}

LOWER = Fraction(9442, 10000)
UPPER = Fraction(9443, 10000)
LOOSE = Fraction(2401, 2500)  # (49/50)^2
HOSTILE = Fraction(9216, 10000)  # (96/100)^2
SKEW_DIMS = {6: 4, -6: 8, 0: 12, 2: 42, -2: 54}
SYM_DIMS = {6: 12, -6: 8, 0: 20, 2: 54, -2: 42}


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"OWNER_UNAVAILABLE:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class E:
    """Element of Q(a), a^4 + a^2 - 1 = 0, coefficients low-to-high."""

    def __init__(self, coeffs):
        self.c = tuple(Fraction(x) for x in coeffs)
        if len(self.c) != 4:
            raise ValueError(len(self.c))

    @classmethod
    def rat(cls, value):
        return cls((value, 0, 0, 0))

    def __add__(self, other):
        if not isinstance(other, E):
            other = E.rat(other)
        return E(tuple(self.c[i] + other.c[i] for i in range(4)))

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return E(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, E):
            return E(tuple(self.c[i] * Fraction(other) for i in range(4)))
        raw = [Fraction(0)] * 7
        for i in range(4):
            for j in range(4):
                raw[i + j] += self.c[i] * other.c[j]
        # a^4 = 1 - a^2, a^5 = a - a^3, a^6 = -1 + 2 a^2
        return E((
            raw[0] + raw[4] - raw[6],
            raw[1] + raw[5],
            raw[2] - raw[4] + 2 * raw[6],
            raw[3] - raw[5],
        ))

    def __rmul__(self, other):
        return self * other

    def is_zero(self):
        return all(x == 0 for x in self.c)


ZERO = E.rat(0)
ONE = E.rat(1)
A = E((0, 1, 0, 0))
P = A * A


def mul_matrix(entry: E):
    c0, c1, c2, c3 = entry.c
    return [
        [c0, c3, c2, c1 - c3],
        [c1, c0, c3, c2],
        [c2, c1 - c3, c0 - c2, -c1 + 2 * c3],
        [c3, c2, c1 - c3, c0 - c2],
    ]


def inv_E(entry: E) -> E:
    rows = [row[:] + [Fraction(1) if i == k else Fraction(0) for k in range(4)]
            for i, row in enumerate(mul_matrix(entry))]
    for col in range(4):
        pivot = next(i for i in range(col, 4) if rows[i][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        div = rows[col][col]
        rows[col] = [value / div for value in rows[col]]
        for i in range(4):
            if i == col or rows[i][col] == 0:
                continue
            factor = rows[i][col]
            rows[i] = [rows[i][j] - factor * rows[col][j] for j in range(8)]
    return E(tuple(rows[i][4] for i in range(4)))


def sign_uv(u: Fraction, v: Fraction) -> int:
    """Sign of u + v*sqrt(5) at the positive square root."""
    if u == 0 and v == 0:
        return 0
    if u >= 0 and v >= 0:
        return 1
    if u <= 0 and v <= 0:
        return -1
    disc = u * u - 5 * v * v
    if disc > 0:
        return 1 if u > 0 else -1
    if disc < 0:
        return 1 if v > 0 else -1
    return 0


def sign_E(entry: E) -> int:
    """Sign at the positive root a = sqrt((sqrt(5)-1)/2)."""
    c0, c1, c2, c3 = entry.c
    u = c0 - c2 / 2
    v = c2 / 2
    r = c1 - c3 / 2
    s = c3 / 2
    pu = u * u + 5 * v * v
    pv = 2 * u * v
    qu = r * r + 5 * s * s
    qv = 2 * r * s
    du = pu + qu / 2 - 5 * qv / 2
    dv = pv - qu / 2 + qv / 2
    delta = sign_uv(du, dv)
    left = sign_uv(u, v)
    right = sign_uv(r, s)
    if delta > 0:
        return left
    if delta < 0:
        return right
    if left == 0 and right == 0:
        return 0
    if left == right:
        return left
    return 0


def zeros():
    return [[ZERO for _ in range(16)] for _ in range(16)]


def matmul(left, right):
    n = len(right)
    out = [[ZERO for _ in range(len(right[0]))] for _ in range(len(left))]
    for i, row in enumerate(left):
        for k in range(n):
            lik = row[k]
            if lik.is_zero():
                continue
            rk = right[k]
            dest = out[i]
            for j, value in enumerate(rk):
                dest[j] = dest[j] + lik * value
    return out


def transpose(matrix):
    return [list(col) for col in zip(*matrix)]


def eye(scale):
    out = zeros()
    for i in range(16):
        out[i][i] = scale
    return out


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(16)] for i in range(16)]


def scale(matrix, factor):
    return [[factor * matrix[i][j] for j in range(16)] for i in range(16)]


def frob_sq(matrix) -> E:
    acc = ZERO
    for row in matrix:
        for value in row:
            acc = acc + value * value
    return acc


def trace(matrix) -> E:
    return sum((matrix[i][i] for i in range(16)), ZERO)


def parse_entry(owner, value) -> E:
    reduced = s.expand(owner.old.red(value).xreplace({owner.old.p: owner.old.a ** 2}))
    poly = s.Poly(s.together(reduced), owner.old.a)
    if poly.degree() > 3:
        raise AssertionError(f"DEGREE:{poly}")
    return E(tuple(Fraction(poly.nth(i)) for i in range(4)))


def load_returns(owner):
    eye4 = s.eye(4)
    out = []
    for r in range(4):
        matrix = owner.record(eye4, eye4[:, r])[0]
        out.append([[parse_entry(owner, matrix[i, j]) for j in range(16)] for i in range(16)])
    return out


SKEW_PAIRS = [(i, j) for i in range(16) for j in range(i + 1, 16)]
SKEW_INDEX = {pair: k for k, pair in enumerate(SKEW_PAIRS)}
SYM_KEYS = [("d", i) for i in range(16)] + [("o", i, j) for i, j in SKEW_PAIRS]
SYM_INDEX = {key: k for k, key in enumerate(SYM_KEYS)}


def perm_images(pi):
    out = []
    for mask in range(16):
        bits = [b for b in range(4) if mask & (1 << b)]
        images = [pi[b] for b in bits]
        sign = 1
        for i in range(len(images)):
            for j in range(i + 1, len(images)):
                if images[j] < images[i]:
                    sign = -sign
        newmask = 0
        for b in images:
            newmask |= 1 << b
        out.append((newmask, sign))
    return out


def ad_skew(pi):
    em = perm_images(pi)
    mapping = []
    for p, q in SKEW_PAIRS:
        raw = em[p][1] * em[q][1]
        a, b = em[p][0], em[q][0]
        if a < b:
            mapping.append((SKEW_INDEX[(a, b)], raw))
        else:
            mapping.append((SKEW_INDEX[(b, a)], -raw))
    return mapping


def ad_sym(pi):
    em = perm_images(pi)
    mapping = []
    for key in SYM_KEYS:
        if key[0] == "d":
            mapping.append((SYM_INDEX[("d", em[key[1]][0])], 1))
        else:
            _, p, q = key
            raw = em[p][1] * em[q][1]
            a, b = em[p][0], em[q][0]
            if a < b:
                mapping.append((SYM_INDEX[("o", a, b)], raw))
            else:
                mapping.append((SYM_INDEX[("o", b, a)], raw))
    return mapping


def exterior_matrix(pi):
    matrix = [[0 for _ in range(16)] for _ in range(16)]
    for old, (new, sign) in enumerate(perm_images(pi)):
        matrix[new][old] = sign
    return matrix


def int_matmul(left, right):
    n = len(right)
    p = len(right[0])
    out = [[0 for _ in range(p)] for _ in range(len(left))]
    for i, row in enumerate(left):
        for k, lik in enumerate(row):
            if lik == 0:
                continue
            for j in range(p):
                out[i][j] += lik * right[k][j]
    return out


def sym_matrix_from_coords(coords):
    matrix = [[0 for _ in range(16)] for _ in range(16)]
    for key, value in zip(SYM_KEYS, coords):
        if value == 0:
            continue
        if key[0] == "d":
            matrix[key[1]][key[1]] = value
        else:
            _, i, j = key
            matrix[i][j] = value
            matrix[j][i] = value
    return matrix


def sym_coords_from_matrix(matrix):
    coords = []
    for key in SYM_KEYS:
        if key[0] == "d":
            coords.append(matrix[key[1]][key[1]])
        else:
            _, i, j = key
            coords.append(matrix[i][j])
    return coords


def skew_matrix_from_coords(coords):
    matrix = [[0 for _ in range(16)] for _ in range(16)]
    for (i, j), value in zip(SKEW_PAIRS, coords):
        if value == 0:
            continue
        matrix[i][j] = value
        matrix[j][i] = -value
    return matrix


def skew_coords_from_matrix(matrix):
    return [matrix[i][j] for i, j in SKEW_PAIRS]


def gdiag(sector):
    if sector == "skew":
        return [Fraction(2) for _ in SKEW_PAIRS]
    return [Fraction(1) if key[0] == "d" else Fraction(2) for key in SYM_KEYS]


def frob_dot(left, right, scale):
    acc = Fraction(0)
    for x, y, weight in zip(left, right, scale):
        acc += x * y * weight
    return acc


def transpositions():
    out = []
    for perm in permutations(range(4)):
        diffs = [i for i in range(4) if perm[i] != i]
        if len(diffs) == 2 and perm[diffs[0]] == diffs[1]:
            out.append(perm)
    return out


def operator_matrix(ops, ad):
    n = len(ad((0, 1, 2, 3)))
    columns = [[0] * n for _ in range(n)]
    for coef, pi in ops:
        for src, (dst, sg) in enumerate(ad(pi)):
            columns[src][dst] += coef * sg
    return [[columns[src][dst] for src in range(n)] for dst in range(n)]


def kernel_basis(matrix):
    data = DomainMatrix.from_list(matrix, QQ).nullspace().to_list()
    return [[Fraction(int(value.numerator), int(value.denominator)) for value in row] for row in data]


def solve_rat(gram, rhs):
    aug = [row[:] + [rhs[i]] for i, row in enumerate(gram)]
    size = len(aug)
    for col in range(size):
        pivot = next((i for i in range(col, size) if aug[i][col] != 0), None)
        if pivot is None:
            raise AssertionError(f"SINGULAR:{col}")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        aug[col] = [entry / div for entry in aug[col]]
        for i in range(size):
            if i == col or aug[i][col] == 0:
                continue
            factor = aug[i][col]
            aug[i] = [aug[i][j] - factor * aug[col][j] for j in range(size + 1)]
    return [aug[i][size] for i in range(size)]


def coords_to_matrix(sector, coords):
    matrix = zeros()
    keys = SKEW_PAIRS if sector == "skew" else SYM_KEYS
    for key, value in zip(keys, coords):
        entry = value if isinstance(value, E) else E.rat(value)
        if entry.is_zero():
            continue
        if sector == "skew":
            i, j = key
            matrix[i][j] = entry
            matrix[j][i] = -entry
        elif key[0] == "d":
            matrix[key[1]][key[1]] = entry
        else:
            _, i, j = key
            matrix[i][j] = entry
            matrix[j][i] = entry
    return matrix


def matrix_to_coords(sector, matrix):
    if sector == "skew":
        return [matrix[i][j] for i, j in SKEW_PAIRS]
    coords = []
    for key in SYM_KEYS:
        if key[0] == "d":
            coords.append(matrix[key[1]][key[1]])
        else:
            _, i, j = key
            coords.append(matrix[i][j])
    return coords


def channel_average(returns, matrix):
    acc = None
    for u in returns:
        prod = matmul(u, matmul(matrix, transpose(u)))
        acc = prod if acc is None else add(acc, prod)
    return scale(acc, Fraction(1, 4))


def restrict(returns, sector, basis):
    n = len(basis[0])
    m = len(basis)
    images = [matrix_to_coords(sector, channel_average(returns, coords_to_matrix(sector, vec))) for vec in basis]
    btb = [[sum(basis[i][k] * basis[j][k] for k in range(n)) for j in range(m)] for i in range(m)]
    columns = []
    for image in images:
        rhs = [sum((image[k] * basis[i][k] for k in range(n)), ZERO) for i in range(m)]
        parts = [solve_rat(btb, [entry.c[power] for entry in rhs]) for power in range(4)]
        coeff = [E(tuple(parts[power][i] for power in range(4))) for i in range(m)]
        recon = [ZERO for _ in range(n)]
        for i in range(m):
            for k in range(n):
                recon[k] = recon[k] + coeff[i] * basis[i][k]
        for k in range(n):
            if not (recon[k] - image[k]).is_zero():
                raise AssertionError("EIGENSPACE_NOT_CHANNEL_INVARIANT")
        columns.append(coeff)
    t_mat = [[columns[j][i] for j in range(m)] for i in range(m)]
    p2 = P * P
    l_mat = [[(P if i == j else ZERO) + p2 * t_mat[i][j] for j in range(m)] for i in range(m)]
    scale_row = gdiag(sector)
    h = [[frob_dot(basis[i], basis[j], scale_row) for j in range(m)] for i in range(m)]
    hl = [[sum((E.rat(h[i][k]) * l_mat[k][j] for k in range(m)), ZERO) for j in range(m)] for i in range(m)]
    a_mat = [[sum((l_mat[k][i] * hl[k][j] for k in range(m)), ZERO) for j in range(m)] for i in range(m)]
    return h, l_mat, a_mat


def shift(h, a_mat, bound: Fraction):
    m = len(h)
    return [[E.rat(h[i][j] * bound) - a_mat[i][j] for j in range(m)] for i in range(m)]


def first_pivot_sign(matrix) -> int:
    """Unpivoted LDL sign of the first nonpositive pivot, or 1 if all are positive.

    After earlier pivots are positive, a negative pivot is a negative leading
    principal minor, so the quadratic form takes a strictly negative value.
    A zero pivot only makes that leading submatrix singular.
    """
    rows = [row[:] for row in matrix]
    n = len(rows)
    for k in range(n):
        sgn = sign_E(rows[k][k])
        if sgn <= 0:
            return sgn
        inv = inv_E(rows[k][k])
        for i in range(k + 1, n):
            factor = rows[i][k]
            if factor.is_zero():
                continue
            factor = factor * inv
            for j in range(k, n):
                rows[i][j] = rows[i][j] - factor * rows[k][j]
    return 1


def is_positive_definite(matrix) -> bool:
    return first_pivot_sign(matrix) == 1


def traceless_combinations(basis):
    traces = []
    for vec in basis:
        acc = Fraction(0)
        for value, key in zip(vec, SYM_KEYS):
            if key[0] == "d":
                acc += value
        traces.append(acc)
    null = DomainMatrix.from_list([traces], QQ).nullspace().to_list()
    out = []
    width = len(basis[0])
    for row in null:
        comb = [Fraction(int(v.numerator), int(v.denominator)) for v in row]
        vec = [Fraction(0) for _ in range(width)]
        for weight, old in zip(comb, basis):
            if weight == 0:
                continue
            for i, value in enumerate(old):
                vec[i] += weight * value
        out.append(vec)
    return out


def run():
    checks = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for path, digest in INPUTS.items():
        check(f"PIN:{path}", sha(path) == digest)

    # Positive square root of 5, not the negative one: 2^2 < 5 < 3^2.
    check("POSITIVE_SQRT5_SIGN", sign_uv(Fraction(-2), Fraction(1)) == 1 and sign_uv(Fraction(-3), Fraction(1)) == -1)
    check("GOLDEN_RELATIONS", (P * P + P - ONE).is_zero() and (A * A - P).is_zero() and sign_E(A) == 1 and sign_E(P - ONE) == -1)
    p_lo, p_hi = Fraction(309, 500), Fraction(619, 1000)
    a_lo, a_hi = Fraction(393, 500), Fraction(787, 1000)
    check(
        "POSITIVE_GOLDEN_BRACKETS",
        p_lo ** 2 + p_lo < 1 < p_hi ** 2 + p_hi and a_lo ** 4 + a_lo ** 2 < 1 < a_hi ** 4 + a_hi ** 2,
    )

    owner = load(CHRONOLOGY, "chronology_owner")
    fock = load(FOCK, "fock_owner")
    returns = load_returns(owner)
    for u in returns:
        prod = matmul(transpose(u), u)
        for i in range(16):
            for j in range(16):
                expect = ONE if i == j else ZERO
                if not (prod[i][j] - expect).is_zero():
                    raise AssertionError(f"RETURN_NOT_ORTHOGONAL:{i},{j}")
    check("FOUR_LITERAL_RETURNS_ORTHOGONAL", True)

    half = E.rat(Fraction(1, 2))
    quarter = E.rat(Fraction(1, 4))
    alpha = P * half
    beta = (P * P) * half
    gamma = A * P * half
    check("KRAUS_CROSS_TERM_CANCELS", (alpha * beta - gamma * gamma).is_zero())
    check(
        "KRAUS_COEFFICIENTS",
        (alpha * alpha + gamma * gamma - P * quarter).is_zero()
        and (beta * beta + gamma * gamma - (P * P) * quarter).is_zero(),
    )
    alpha_swap = (P * P) * half
    beta_swap = P * half
    check("SWAPPED_COEFFICIENTS_DIFFER", not (alpha_swap * alpha_swap + gamma * gamma - P * quarter).is_zero())

    def kraus_image(u, matrix):
        k0 = add(eye(alpha), scale(u, beta))
        k1 = scale(add(u, eye(-ONE)), gamma)
        return add(matmul(k0, matmul(matrix, transpose(k0))), matmul(k1, matmul(matrix, transpose(k1))))

    def simple_image(u, matrix):
        return add(scale(matrix, P * quarter), scale(matmul(u, matmul(matrix, transpose(u))), (P * P) * quarter))

    for u in returns:
        for col in range(16):
            for row in range(16):
                matrix = zeros()
                matrix[row][col] = ONE
                got = kraus_image(u, matrix)
                expect = simple_image(u, matrix)
                for i in range(16):
                    for j in range(16):
                        if not (got[i][j] - expect[i][j]).is_zero():
                            raise AssertionError(f"KRAUS_UNIT:{row},{col},{i},{j}")
        k0 = add(eye(alpha), scale(u, beta))
        k1 = scale(add(u, eye(-ONE)), gamma)
        acc = add(matmul(transpose(k0), k0), matmul(transpose(k1), k1))
        for i in range(16):
            for j in range(16):
                expect = quarter if i == j else ZERO
                if not (acc[i][j] - expect).is_zero():
                    raise AssertionError(f"KTK:{i},{j}")
    check("KRAUS_EQUALS_SIMPLIFIED_CHANNEL_ON_EVERY_MATRIX_UNIT", True)
    probe = zeros()
    probe[0][1] = ONE
    probe[1][0] = ONE
    mutant = add(scale(probe, (P * P) * quarter), scale(matmul(returns[0], matmul(probe, transpose(returns[0]))), P * quarter))
    check("SWAPPED_CHANNEL_DIFFERS_ON_A_MATRIX", any(not (mutant[i][j] - simple_image(returns[0], probe)[i][j]).is_zero() for i in range(16) for j in range(16)))

    # Owned signed CAR basis: a traceless commutant of the single return U_0.
    b0 = fock.record_basis()
    b0e = [[E.rat(int(b0[i, j])) for j in range(16)] for i in range(16)]
    gram = matmul(transpose(b0e), b0e)
    for i in range(16):
        for j in range(16):
            expect = ONE if i == j else ZERO
            if not (gram[i][j] - expect).is_zero():
                raise AssertionError("RECORD_BASIS")
    mid = zeros()
    for block in range(4):
        mid[4 * block][4 * block] = ONE
        mid[4 * block + 1][4 * block + 1] = -ONE
    witness = matmul(b0e, matmul(mid, transpose(b0e)))
    fixed = matmul(returns[0], matmul(witness, transpose(returns[0])))
    check(
        "ONE_RETURN_TRACELESS_COMMUTANT_WITNESS",
        trace(witness).is_zero() and not frob_sq(witness).is_zero()
        and all((fixed[i][j] - witness[i][j]).is_zero() for i in range(16) for j in range(16)),
    )
    weights = [Fraction(97, 100), Fraction(1, 100), Fraction(1, 100), Fraction(1, 100)]
    mixed = zeros()
    for weight, u in zip(weights, returns):
        mixed = add(mixed, scale(matmul(u, matmul(witness, transpose(u))), E.rat(weight)))
    image = add(scale(witness, P), scale(mixed, P * P))
    gap = frob_sq(image) * 2500 - frob_sq(witness) * 2401
    check("UNEQUAL_WEIGHT_EXCEEDS_EQUAL_WEIGHT_UPPER_BOUND", sign_E(gap) == 1)

    identity = eye(ONE)
    averaged = channel_average(returns, identity)
    equal = add(scale(identity, P), scale(averaged, P * P))
    check("EQUAL_WEIGHT_FIXES_IDENTITY", all((equal[i][j] - identity[i][j]).is_zero() for i in range(16) for j in range(16)))

    trans = transpositions()
    check("SIX_TRANSPOSITIONS", len(trans) == 6)
    for pi in trans:
        matrix = exterior_matrix(pi)
        prod = int_matmul(matrix, matrix)
        if matrix != transpose(matrix) or any(prod[i][j] != (1 if i == j else 0) for i in range(16) for j in range(16)):
            raise AssertionError("TRANSPOSITION_NOT_SYMMETRIC_INVOLUTION")
    check("EXTERIOR_TRANSPOSITIONS_ARE_SYMMETRIC_INVOLUTIONS", True)

    sym_coords = []
    for key in SYM_KEYS:
        if key[0] == "d":
            sym_coords.append(key[1] + 1)
        else:
            sym_coords.append(10 + key[1] + 17 * key[2])
    skew_coords = [3 + i + 5 * j for i, j in SKEW_PAIRS]
    for pi in trans:
        em = exterior_matrix(pi)
        emt = transpose(em)
        got_sym = sym_coords_from_matrix(int_matmul(em, int_matmul(sym_matrix_from_coords(sym_coords), emt)))
        image = [0 for _ in SYM_KEYS]
        for src, value in enumerate(sym_coords):
            dst, sg = ad_sym(pi)[src]
            image[dst] += sg * value
        if got_sym != image:
            raise AssertionError("SYM_AD")
        got_skew = skew_coords_from_matrix(int_matmul(em, int_matmul(skew_matrix_from_coords(skew_coords), emt)))
        image = [0 for _ in SKEW_PAIRS]
        for src, value in enumerate(skew_coords):
            dst, sg = ad_skew(pi)[src]
            image[dst] += sg * value
        if got_skew != image:
            raise AssertionError("SKEW_AD")
    check("COORDINATE_AD_MATCHES_MATRIX_CONJUGATION", True)

    diagonal = coords_to_matrix("sym", [ONE if key == ("d", 0) else ZERO for key in SYM_KEYS])
    off = coords_to_matrix("sym", [ONE if key == ("o", 0, 1) else ZERO for key in SYM_KEYS])
    diag_coords = [Fraction(1) if key == ("d", 0) else Fraction(0) for key in SYM_KEYS]
    off_coords = [Fraction(1) if key == ("o", 0, 1) else Fraction(0) for key in SYM_KEYS]
    check(
        "FROBENIUS_COORDINATES_MATCH_ENTRY_SQUARES",
        (frob_sq(diagonal) - ONE).is_zero()
        and frob_dot(diag_coords, diag_coords, gdiag("sym")) == 1
        and (frob_sq(off) - E.rat(2)).is_zero()
        and frob_dot(off_coords, off_coords, gdiag("sym")) == 2,
    )
    # Symmetric/skew cross term cancels entrywise.
    cross = ZERO
    for i, j in SKEW_PAIRS:
        cross = cross + off[i][j] * ONE + off[j][i] * (-ONE)
    check("SYMMETRIC_SKEW_ENTRY_CROSS_TERM_IS_ZERO", cross.is_zero())

    ads = {"skew": ad_skew, "sym": ad_sym}
    expected = {"skew": SKEW_DIMS, "sym": SYM_DIMS}
    bases = {}
    for sector, ad in ads.items():
        n = len(ad((0, 1, 2, 3)))
        class_sum = operator_matrix([(1, pi) for pi in trans], ad)
        found = {}
        for eig, dim in expected[sector].items():
            shifted = [[class_sum[i][j] - (eig if i == j else 0) for j in range(n)] for i in range(n)]
            basis = kernel_basis(shifted)
            if len(basis) != dim:
                raise AssertionError(f"DIM:{sector}:{eig}:{len(basis)}")
            found[eig] = basis
        if sum(len(rows) for rows in found.values()) != n:
            raise AssertionError(f"SPAN:{sector}")
        scale_row = gdiag(sector)
        eigs = list(expected[sector])
        for i, left in enumerate(eigs):
            for right in eigs[i + 1:]:
                for u in found[left]:
                    for v in found[right]:
                        if frob_dot(u, v, scale_row) != 0:
                            raise AssertionError(f"NOT_ORTHOGONAL:{sector}:{left}:{right}")
        bases[sector] = found
    check("CLASS_SUM_KERNELS_SPAN_AND_ARE_ORTHOGONAL", True)

    for eig, basis in bases["sym"].items():
        if eig == 6:
            continue
        for vec in basis:
            acc = sum(value for value, key in zip(vec, SYM_KEYS) if key[0] == "d")
            if acc != 0:
                raise AssertionError(f"NONEIGENVALUE_HAS_TRACE:{eig}")
    check("NONTRIVIAL_SYMMETRIC_KERNELS_ARE_TRACELESS", True)

    blocks = []
    for sector in ("skew", "sym"):
        for eig, basis in bases[sector].items():
            use = basis
            label = f"{sector}:{eig}"
            if sector == "sym" and eig == 6:
                use = traceless_combinations(basis)
                if len(use) != 11:
                    raise AssertionError(f"TRACELESS:{len(use)}")
                if any(sum(value for value, key in zip(vec, SYM_KEYS) if key[0] == "d") != 0 for vec in use):
                    raise AssertionError("TRACELESS_CUT")
                label = "sym:6:traceless"
            print(f"restrict {label}", file=sys.stderr, flush=True)
            h, l_mat, a_mat = restrict(returns, sector, use)
            blocks.append((label, h, l_mat, a_mat))
    check("CHANNEL_PRESERVES_EVERY_CLASS_SUM_KERNEL", True)

    winner = next(item for item in blocks if item[0] == "sym:6:traceless")
    _, h_w, l_w, a_w = winner
    winner_lower_sign = first_pivot_sign(shift(h_w, a_w, LOWER))
    check("WINNER_SQUARED_NORM_EXCEEDS_9442_OVER_10000", winner_lower_sign == -1)
    check("WINNER_SQUARED_NORM_BELOW_9443_OVER_10000", is_positive_definite(shift(h_w, a_w, UPPER)))
    check("WINNER_SQUARED_NORM_BELOW_49_OVER_50_SQUARED", is_positive_definite(shift(h_w, a_w, LOOSE)))
    for label, h, _l, a_mat in blocks:
        if label == "sym:6:traceless":
            continue
        if not is_positive_definite(shift(h, a_mat, LOWER)):
            raise AssertionError(f"BLOCK_NOT_BELOW_WINDOW:{label}")
    check("EVERY_OTHER_KERNEL_SQUARED_NORM_BELOW_9442_OVER_10000", True)
    runner = next(item for item in blocks if item[0] == "skew:2")
    runner_sign = first_pivot_sign(shift(runner[1], runner[3], HOSTILE))
    check("SKEW_RUNNER_UP_EXCEEDS_96_OVER_100_SQUARED", runner_sign == -1)
    check("WINDOW_SQUARE_BELOW_49_OVER_50_SQUARED", 9443 * 2500 < 2401 * 10000)

    # H-adjoint commutator on the winning block. Non-normality blocks reading
    # the singular-value bound as a spectral radius.
    m = len(h_w)
    hinv_cols = [solve_rat(h_w, [Fraction(1) if i == j else Fraction(0) for i in range(m)]) for j in range(m)]
    hinv = [[E.rat(hinv_cols[j][i]) for j in range(m)] for i in range(m)]
    lt = [[l_w[j][i] for j in range(m)] for i in range(m)]
    h_e = [[E.rat(value) for value in row] for row in h_w]

    def mul_small(left, right):
        size = len(left)
        out = [[ZERO for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for k in range(size):
                if left[i][k].is_zero():
                    continue
                for j in range(size):
                    out[i][j] = out[i][j] + left[i][k] * right[k][j]
        return out

    adjoint = mul_small(hinv, mul_small(lt, h_e))
    commutator = mul_small(l_w, adjoint)
    other = mul_small(adjoint, l_w)
    check(
        "WINNING_BLOCK_IS_NOT_H_NORMAL",
        any(not (commutator[i][j] - other[i][j]).is_zero() for i in range(m) for j in range(m)),
    )

    return {
        "schema": "d0-native-golden-channel-hs-contraction/1",
        "status": "PASS_CONDITIONAL_EQUAL_WEIGHT_HS_CONTRACTION",
        "proof": PROOF,
        "input_sha256": {path: sha(path) for path in INPUTS},
        "channel": {
            "returns": "U_r=record(I_4,e_r), r=0..3",
            "equal_weight": "Phi(X)=p*X+(p^2)/4*sum_r U_r*X*U_r^T",
            "golden_relations": "a^2=p, p^2+p=1, positive roots",
        },
        "exact_result": {
            "skew_class_sum_kernel_dimensions": {str(k): v for k, v in SKEW_DIMS.items()},
            "symmetric_class_sum_kernel_dimensions": {str(k): v for k, v in SYM_DIMS.items()},
            "traceless_symmetric_invariant_dimension": 11,
            "squared_hs_norm_lower_exclusive": "9442/10000",
            "squared_hs_norm_upper_exclusive": "9443/10000",
            "hs_norm_rational_upper_exclusive": "49/50",
            "window_times_denominator_check": [9443 * 2500, 2401 * 10000],
            "unequal_weight_numerator": [97, 1, 1, 1],
            "runner_up_hostile_square": "9216/10000",
            "winner_lower_pivot_sign": winner_lower_sign,
            "runner_up_hostile_pivot_sign": runner_sign,
        },
        "exact_controls": len(checks),
        "checks": checks,
        "scope": {
            "equal_weight_traceless_hermitian_hs_contraction": True,
            "hs_norm_strictly_below_49/50": True,
            "contraction_for_every_positive_return_weight": False,
            "singular_value_equals_spectral_radius": False,
            "trace_norm_or_diamond_norm_gap": False,
            "channel_admitted_as_physical_law": False,
            "equal_weights_selected_by_complete_core": False,
            "state_identified_with_native_joint_matter": False,
            "core_owned_qDbm_admission_map_derived": False,
            "G0_GR_or_parent_terminal_closed": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    result["checker_sha256"] = sha(str(Path(__file__).relative_to(ROOT)))
    result["proof_sha256"] = sha(PROOF)
    target = ROOT / "02_REGISTRY/research/certificates" / f"{STEM}_results.json"
    if target.exists() and not args.write:
        existing = json.loads(target.read_text())
        if existing != result:
            raise SystemExit("IMMUTABLE_RECEIPT_MISMATCH: rerun with --write after reviewing inputs")
        mode = "verified"
    else:
        target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        mode = "written"
    print(json.dumps({
        "status": result["status"],
        "exact_controls": result["exact_controls"],
        "mode": mode,
        "result": str(target.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
