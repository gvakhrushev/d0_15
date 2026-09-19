#!/usr/bin/env python3
"""D0-SEDENION-SIGNED-BASIS-S3-NOGO-001.

Exhaustive no-go for the *signed canonical-basis* route to permuting the three
canonical octonion-sized blocks in the integer sedenion carrier.

The Cayley--Dickson convention is exactly the repository convention:
  (a,b)(c,d) = (ac - conj(d)b, da + b conj(c)).

For canonical basis units e_i, the product index is i XOR j. Therefore every
unital signed-basis algebra automorphism e_i -> s_i e_{p(i)} forces p to be an
F_2-linear automorphism of the four-bit index space. Requiring the quaternion
block H={0,1,2,3} to be preserved setwise leaves exactly 576 linear
permutations. Signs are determined by the four generator signs, so exactly
576*16 = 9216 exhaustive candidates remain.

The certificate checks all 9216 candidates against all 256 basis products.
Exactly 384 are algebra automorphisms. Every one stabilizes each of the three
canonical 8-basis blocks H+<4>, H+<8>, H+<12>; none induces a nontrivial S3
permutation on those blocks.

Scope is deliberately narrow: this does NOT exclude automorphisms after
rational/real/complex scalar extension or non-monomial changes of basis.
"""
from functools import lru_cache
from itertools import product


GEN_BITS = (1, 2, 4, 8)
H = frozenset((0, 1, 2, 3))
BLOCKS = (
    frozenset(range(0, 8)),
    frozenset((0, 1, 2, 3, 8, 9, 10, 11)),
    frozenset((0, 1, 2, 3, 12, 13, 14, 15)),
)


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
        # (a,0)(0,d) = (0,d*a)
        s, k = basis_mul(level - 1, j - half, i)
        return (s, k + half)
    if j < half <= i:
        # (0,b)(c,0) = (0,b*conj(c))
        sc, cj = basis_conj(j)
        s, k = basis_mul(level - 1, i - half, cj)
        return (sc * s, k + half)

    # (0,b)(0,d) = (-conj(d)*b,0)
    sd, dj = basis_conj(j - half)
    s, k = basis_mul(level - 1, dj, i - half)
    return (-sd * s, k)


TABLE = tuple(tuple(basis_mul(4, i, j) for j in range(16)) for i in range(16))


def span_f2(vs: tuple[int, ...]) -> frozenset[int]:
    out = {0}
    for v in vs:
        out |= {x ^ v for x in tuple(out)}
    return frozenset(out)


def linear_map(images: tuple[int, int, int, int]):
    def p(i: int) -> int:
        out = 0
        for bit, image in zip(GEN_BITS, images):
            if i & bit:
                out ^= image
        return out
    return p


def h_preserving_linear_maps():
    """All GL(4,2) maps preserving H=span(1,2) setwise."""
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            if a == b or span_f2((a, b)) != H:
                continue
            for c in range(1, 16):
                if c in span_f2((a, b)):
                    continue
                for d in range(1, 16):
                    if d in span_f2((a, b, c)):
                        continue
                    yield (a, b, c, d)


def forced_signs(p, generator_signs: tuple[int, int, int, int]) -> dict[int, int]:
    """Extend generator signs to every basis unit using canonical products."""
    signs = {0: 1}
    signs.update(dict(zip(GEN_BITS, generator_signs)))
    for i in range(1, 16):
        if i in signs:
            continue
        bit = 1 << (i.bit_length() - 1)
        a = i ^ bit
        source_sign, source_index = TABLE[a][bit]
        target_sign, target_index = TABLE[p(a)][p(bit)]
        assert source_index == i
        assert target_index == p(i)
        signs[i] = signs[a] * signs[bit] * target_sign * source_sign
    return signs


def is_signed_basis_automorphism(p, signs: dict[int, int]) -> bool:
    images = [p(i) for i in range(16)]
    if sorted(images) != list(range(16)) or p(0) != 0 or signs[0] != 1:
        return False
    for i in range(16):
        for j in range(16):
            source_sign, k = TABLE[i][j]
            target_sign, target_k = TABLE[p(i)][p(j)]
            if target_k != p(k):
                return False
            if source_sign * signs[k] != signs[i] * signs[j] * target_sign:
                return False
    return True


def block_permutation(p) -> tuple[int, int, int] | None:
    image_blocks = tuple(frozenset(p(i) for i in block) for block in BLOCKS)
    try:
        return tuple(BLOCKS.index(b) for b in image_blocks)
    except ValueError:
        return None


def main() -> int:
    # Structural checksum: the concrete CD table really has XOR index law.
    assert all(TABLE[i][j][1] == (i ^ j) for i in range(16) for j in range(16))
    print("PASS_CD_XOR_INDEX_LAW 256/256 basis products")

    linear_candidates = list(h_preserving_linear_maps())
    assert len(linear_candidates) == 576
    assert all(span_f2((a, b)) == H for a, b, _, _ in linear_candidates)
    print("PASS_H_PRESERVING_GL4_COUNT 576")

    automorphisms = []
    for images in linear_candidates:
        p = linear_map(images)
        for generator_signs in product((-1, 1), repeat=4):
            signs = forced_signs(p, generator_signs)
            if is_signed_basis_automorphism(p, signs):
                automorphisms.append((images, generator_signs, p, signs))

    # 576 underlying linear candidates × 16 possible generator signs = 9216.
    assert len(linear_candidates) * 16 == 9216
    assert len(automorphisms) == 384
    print("PASS_SIGNED_BASIS_AUTOMORPHISM_COUNT 384/9216")

    # All 384 stabilize each of the three octonion-sized carriers individually.
    perms = [block_permutation(p) for _, _, p, _ in automorphisms]
    assert perms and set(perms) == {(0, 1, 2)}
    print("PASS_NO_NONTRIVIAL_BLOCK_S3 all 384 induce identity on the three blocks")

    # Stronger checksum: 24 underlying index automorphisms, each with all 16
    # generator-sign lifts.
    underlying = {}
    for images, _, _, _ in automorphisms:
        underlying[images] = underlying.get(images, 0) + 1
    assert len(underlying) == 24
    assert set(underlying.values()) == {16}
    print("PASS_UNDERLYING_INDEX_AUTOMORPHISMS 24 each with 16 sign lifts")

    # Reachable negative control: swapping quotient generators 4<->8 preserves
    # H and would swap block 1 with block 2, but NO sign choice makes it an
    # algebra automorphism. Thus the test is capable of seeing a nontrivial
    # block permutation and rejects it specifically because multiplication fails.
    swap_images = (1, 2, 8, 4)
    p_swap = linear_map(swap_images)
    assert block_permutation(p_swap) == (1, 0, 2)
    swap_lifts = 0
    for generator_signs in product((-1, 1), repeat=4):
        signs = forced_signs(p_swap, generator_signs)
        swap_lifts += int(is_signed_basis_automorphism(p_swap, signs))
    assert swap_lifts == 0
    print("SELFTEST_OK_BLOCK_SWAP_REJECTED nontrivial quotient swap has 0/16 multiplicative sign lifts")

    print("HONEST_NOGO signed canonical-basis automorphisms over the integer CD carrier cannot realize the claimed S3 block permutation; scalar extension/non-monomial routes remain open")
    print("PASS_SEDENION_SIGNED_BASIS_S3_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
