#!/usr/bin/env python3
"""D0-SEDENION-BROWN-S3-SCALAR-EXTENSION-001.

Exact positive certificate for the Brown/Gresnigt-Gourlay-Varma S3 action on
the scalar-extended sedenion carrier.

Coefficient field is represented exactly as Q(sqrt(3)) = {a+b*r : r^2=3}.
The Cayley-Dickson convention is the repository convention
    (a,b)(c,d) = (ac - conj(d)b, da + b conj(c)).

The order-three map is the literature Brown automorphism:
    psi(e_i)     = -1/2 e_i - sqrt(3)/2 e_(i+8),  i=1..7
    psi(e_(i+8)) =  sqrt(3)/2 e_i - 1/2 e_(i+8),  i=1..7
    psi(e_0)=e_0, psi(e_8)=e_8.
The order-two map is epsilon(a+b e8)=a-b e8.

This certificate checks:
* the repository multiplication table / known zero-divisor witness;
* the three literature octonion subalgebras and their common quaternion;
* closure of each literature subalgebra;
* basis-level multiplicativity of psi and epsilon on all 256 products;
* psi^3=1, epsilon^2=1, epsilon psi = psi^2 epsilon;
* both S3 generators stabilize each literature octonion subalgebra setwise.

Scope: this closes the scalar-extension automorphism layer only. It does not
by itself construct the complex Clifford left-action, minimal ideals, or the
typed D0 generation-carrier map.
"""
from fractions import Fraction
from functools import lru_cache


# Exact Q(sqrt(3)) element a + b*r, r^2=3.
Q3 = tuple[Fraction, Fraction]
ZERO: Q3 = (Fraction(0), Fraction(0))
ONE: Q3 = (Fraction(1), Fraction(0))
MHALF: Q3 = (Fraction(-1, 2), Fraction(0))
PSQ3HALF: Q3 = (Fraction(0), Fraction(1, 2))
MSQ3HALF: Q3 = (Fraction(0), Fraction(-1, 2))


def qadd(x: Q3, y: Q3) -> Q3:
    return (x[0] + y[0], x[1] + y[1])


def qneg(x: Q3) -> Q3:
    return (-x[0], -x[1])


def qmul(x: Q3, y: Q3) -> Q3:
    a, b = x
    c, d = y
    return (a * c + 3 * b * d, a * d + b * c)


@lru_cache(None)
def basis_mul(level: int, i: int, j: int) -> tuple[int, int]:
    """Return (sign,k) with e_i*e_j = sign*e_k in CD^level(Z)."""
    if level == 0:
        return (1, 0)
    half = 1 << (level - 1)

    def basis_conj(k: int) -> tuple[int, int]:
        return (1 if k == 0 else -1, k)

    if i < half and j < half:
        return basis_mul(level - 1, i, j)
    if i < half <= j:
        s, k = basis_mul(level - 1, j - half, i)
        return (s, k + half)
    if j < half <= i:
        sc, cj = basis_conj(j)
        s, k = basis_mul(level - 1, i - half, cj)
        return (sc * s, k + half)

    sd, dj = basis_conj(j - half)
    s, k = basis_mul(level - 1, dj, i - half)
    return (-sd * s, k)


TABLE = tuple(tuple(basis_mul(4, i, j) for j in range(16)) for i in range(16))
Vec = tuple[Q3, ...]


def basis(i: int, coeff: Q3 = ONE) -> Vec:
    out = [ZERO] * 16
    out[i] = coeff
    return tuple(out)


def vadd(x: Vec, y: Vec) -> Vec:
    return tuple(qadd(a, b) for a, b in zip(x, y))


def vscale(c: Q3, x: Vec) -> Vec:
    return tuple(qmul(c, a) for a in x)


def vmul(x: Vec, y: Vec) -> Vec:
    out = [ZERO] * 16
    for i, a in enumerate(x):
        if a == ZERO:
            continue
        for j, b in enumerate(y):
            if b == ZERO:
                continue
            sign, k = TABLE[i][j]
            term = qmul(a, b)
            if sign < 0:
                term = qneg(term)
            out[k] = qadd(out[k], term)
    return tuple(out)


def psi_basis(i: int) -> Vec:
    if i in (0, 8):
        return basis(i)
    if 1 <= i <= 7:
        return vadd(basis(i, MHALF), basis(i + 8, MSQ3HALF))
    if 9 <= i <= 15:
        j = i - 8
        return vadd(basis(j, PSQ3HALF), basis(i, MHALF))
    raise AssertionError(i)


def epsilon_basis(i: int) -> Vec:
    return basis(i) if i < 8 else basis(i, qneg(ONE))


def linear_extension(images: tuple[Vec, ...], x: Vec) -> Vec:
    out = basis(0, ZERO)
    for i, c in enumerate(x):
        if c != ZERO:
            out = vadd(out, vscale(c, images[i]))
    return out


PSI_IMAGES = tuple(psi_basis(i) for i in range(16))
EPS_IMAGES = tuple(epsilon_basis(i) for i in range(16))


def psi(x: Vec) -> Vec:
    return linear_extension(PSI_IMAGES, x)


def epsilon(x: Vec) -> Vec:
    return linear_extension(EPS_IMAGES, x)


LITERATURE_BLOCKS = (
    frozenset((0, 1, 4, 5, 8, 9, 12, 13)),
    frozenset((0, 2, 4, 6, 8, 10, 12, 14)),
    frozenset((0, 3, 4, 7, 8, 11, 12, 15)),
)
LITERATURE_COMMON_H = frozenset((0, 4, 8, 12))


def block_closed(block: frozenset[int]) -> bool:
    return all(TABLE[i][j][1] in block for i in block for j in block)


def image_supported_in(image: Vec, block: frozenset[int]) -> bool:
    return all(c == ZERO for i, c in enumerate(image) if i not in block)


def main() -> int:
    # Repository convention checks.
    assert all(TABLE[i][j][1] == (i ^ j) for i in range(16) for j in range(16))
    zx = tuple(ONE if i in (1, 10) else ZERO for i in range(16))
    zy = tuple(ONE if i == 4 else (qneg(ONE) if i == 15 else ZERO) for i in range(16))
    assert vmul(zx, zy) == (ZERO,) * 16
    print("PASS_REPOSITORY_CD_CONVENTION_AND_ZERO_DIVISOR")

    # Correct literature octonion triple, not the old H={0,1,2,3}-containing triple.
    assert set.intersection(*map(set, LITERATURE_BLOCKS)) == set(LITERATURE_COMMON_H)
    assert all(len(b) == 8 for b in LITERATURE_BLOCKS)
    assert all(block_closed(b) for b in LITERATURE_BLOCKS)
    print("PASS_LITERATURE_OCTONION_TRIPLE_AND_COMMON_QUATERNION")

    # Exact Brown automorphisms on all basis products.
    for f, name in ((psi, "psi"), (epsilon, "epsilon")):
        for i in range(16):
            for j in range(16):
                assert f(vmul(basis(i), basis(j))) == vmul(f(basis(i)), f(basis(j))), (name, i, j)
    print("PASS_BROWN_GENERATORS_MULTIPLICATIVE 2x256 basis products")

    # S3 presentation on the canonical basis, hence on the linear extension.
    for i in range(16):
        ei = basis(i)
        assert psi(psi(psi(ei))) == ei
        assert epsilon(epsilon(ei)) == ei
        assert epsilon(psi(ei)) == psi(psi(epsilon(ei)))
    print("PASS_S3_RELATIONS psi^3=epsilon^2=1, epsilon*psi=psi^2*epsilon")

    # The literature octonion subalgebras are stabilized setwise by both S3 generators.
    for block in LITERATURE_BLOCKS:
        for i in block:
            assert image_supported_in(psi_basis(i), block)
            assert image_supported_in(epsilon_basis(i), block)
    print("PASS_LITERATURE_BLOCKS_STABILIZED_SETWISE")

    # Reachability control: psi genuinely leaves the signed canonical-basis class.
    assert psi_basis(1) != basis(1)
    assert sum(c != ZERO for c in psi_basis(1)) == 2
    assert psi_basis(1)[1] == MHALF and psi_basis(1)[9] == MSQ3HALF
    print("SELFTEST_OK_PSI_NONMONOMIAL_REQUIRES_QSQRT3")

    print("HONEST_SCOPE scalar-extended sedenion S3 automorphism layer closed; Clifford/minimal-ideal/D0 generation functor remains")
    print("PASS_SEDENION_BROWN_S3_SCALAR_EXTENSION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
