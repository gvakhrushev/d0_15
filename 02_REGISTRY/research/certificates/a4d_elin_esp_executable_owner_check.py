#!/usr/bin/env python3
"""Exact representation scaffold for the E-LIN Lorentz E_sp owner recovery.

This file deliberately stops at the symmetry-equivariant coefficient space.
It does NOT impose the accepted constrained dimension, name E_sp, read J2
orbit data, or import any #262/#265 artifact.

Carrier convention
------------------
Role basis: e_0,e_1,e_2,e_3 with eta = diag(+1,-1,-1,-1).
Input/output metric amplitudes and degree-two derivative monomials use the
same ordered symmetric-pair basis

    [(0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)].

The unrestricted degree-two response tensor therefore has
10 * 10 * 10 = 1000 rational coefficients C[out_sym,in_sym,deriv_sym].

The finite group is the full signed hypercubic subgroup preserving eta:
the time role is fixed by permutations, the three spatial roles are
arbitrarily permuted, and every role can be independently sign-reflected.
Its order is 3! * 2^4 = 96.

Equivariance rows have the exact two-variable form x_i - s x_j = 0,
s in {+1,-1}.  Their exact rank is computed by a signed union-find:
each connected signed component contributes one free rational parameter unless
it contains an odd-sign cycle, in which case the whole component is forced
to zero.  This is exact row-rank arithmetic for this incidence-type matrix.
"""
from __future__ import annotations

from itertools import permutations, product
from typing import Iterable, NamedTuple

ROLE = tuple(range(4))
ETA = (1, -1, -1, -1)
SYM = tuple((a, b) for a in ROLE for b in ROLE if a <= b)
PAIR_INDEX = {pair: j for j, pair in enumerate(SYM)}
NSYM = len(SYM)
AMBIENT = NSYM**3


class GroupElement(NamedTuple):
    # e_a -> signs[a] e_{perm[a]}
    perm: tuple[int, int, int, int]
    signs: tuple[int, int, int, int]


def coeff_index(out_sym: int, in_sym: int, deriv_sym: int) -> int:
    return (out_sym * NSYM + in_sym) * NSYM + deriv_sym


def pair_action(g: GroupElement, pair: tuple[int, int]) -> tuple[int, int]:
    """Return (new symmetric-pair index, sign) for a basis pair."""
    a, b = pair
    aa, bb = g.perm[a], g.perm[b]
    sign = g.signs[a] * g.signs[b]
    if aa <= bb:
        return PAIR_INDEX[(aa, bb)], sign
    return PAIR_INDEX[(bb, aa)], sign


def compose(g: GroupElement, h: GroupElement) -> GroupElement:
    """Composition g after h in the declared basis-action convention."""
    perm = tuple(g.perm[h.perm[a]] for a in ROLE)
    signs = tuple(h.signs[a] * g.signs[h.perm[a]] for a in ROLE)
    return GroupElement(perm, signs)


def full_signature_preserving_group() -> tuple[GroupElement, ...]:
    elements = []
    for spatial_perm in permutations((1, 2, 3)):
        perm = (0,) + spatial_perm
        for signs in product((-1, 1), repeat=4):
            elements.append(GroupElement(perm, signs))
    return tuple(elements)


def generators() -> tuple[GroupElement, ...]:
    ident = (0, 1, 2, 3)
    gens = []
    for k in ROLE:
        signs = [1, 1, 1, 1]
        signs[k] = -1
        gens.append(GroupElement(ident, tuple(signs)))
    gens.append(GroupElement((0, 2, 1, 3), (1, 1, 1, 1)))
    gens.append(GroupElement((0, 1, 3, 2), (1, 1, 1, 1)))
    return tuple(gens)


def generated_subgroup(gens: Iterable[GroupElement]) -> set[GroupElement]:
    identity = GroupElement((0, 1, 2, 3), (1, 1, 1, 1))
    subgroup = {identity}
    frontier = [identity]
    gens = tuple(gens)
    while frontier:
        h = frontier.pop()
        for g in gens:
            gh = compose(g, h)
            if gh not in subgroup:
                subgroup.add(gh)
                frontier.append(gh)
    return subgroup


def preserves_eta(g: GroupElement) -> bool:
    """For signed permutations, g^T eta g = eta iff eta is preserved rolewise."""
    return all(ETA[g.perm[a]] == ETA[a] and g.signs[a] in (-1, 1) for a in ROLE)


class SignedDSU:
    """Exact solver for constraints x = sign*y, sign in {+1,-1}."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        # x = relative[x] * parent[x]
        self.relative = [1] * n
        self.forced_zero = [False] * n

    def find(self, x: int) -> tuple[int, int]:
        p = self.parent[x]
        if p == x:
            return x, 1
        root, rel_parent = self.find(p)
        self.relative[x] *= rel_parent
        self.parent[x] = root
        return root, self.relative[x]

    def impose(self, x: int, y: int, sign: int) -> None:
        """Impose x = sign*y exactly."""
        if sign not in (-1, 1):
            raise ValueError("constraint sign must be +/-1")
        rx, sx = self.find(x)
        ry, sy = self.find(y)
        if rx == ry:
            if sx != sign * sy:
                self.forced_zero[rx] = True
            return

        # sx*rx = sign*sy*ry, hence rx=(sign*sy*sx)*ry because sx^-1=sx.
        root_relation = sign * sy * sx
        self.parent[rx] = ry
        self.relative[rx] = root_relation
        self.forced_zero[ry] = self.forced_zero[ry] or self.forced_zero[rx]

    def dimension(self) -> tuple[int, int, int]:
        roots: set[int] = set()
        for x in range(len(self.parent)):
            root, _ = self.find(x)
            roots.add(root)
        zero_roots = sum(1 for root in roots if self.forced_zero[root])
        free_roots = len(roots) - zero_roots
        return len(roots), zero_roots, free_roots


def equivariance_constraints(
    elements: Iterable[GroupElement],
) -> tuple[SignedDSU, int, int]:
    """Build exact rows x_i - sign*x_j = 0 and return their signed-DSU solver.

    `raw_rows` counts one row per coefficient per supplied group element.
    `nontrivial_rows` omits literal 0=0 rows.  The rows themselves are exact
    integer/rational rows with two possible nonzero entries (+1 and +/-1).
    """
    dsu = SignedDSU(AMBIENT)
    raw_rows = 0
    nontrivial_rows = 0

    for g in elements:
        out_actions = tuple(pair_action(g, pair) for pair in SYM)
        in_actions = out_actions
        deriv_actions = out_actions
        for out_sym, (out_new, out_sign) in enumerate(out_actions):
            for in_sym, (in_new, in_sign) in enumerate(in_actions):
                for deriv_sym, (deriv_new, deriv_sign) in enumerate(deriv_actions):
                    left = coeff_index(out_sym, in_sym, deriv_sym)
                    right = coeff_index(out_new, in_new, deriv_new)
                    sign = out_sign * in_sign * deriv_sign
                    raw_rows += 1
                    if left != right or sign != 1:
                        nontrivial_rows += 1
                    dsu.impose(left, right, sign)

    return dsu, raw_rows, nontrivial_rows


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        suffix = f" :: {detail}" if detail else ""
        raise AssertionError(f"FAIL_{name}{suffix}")
    print(f"PASS_{name}")


def main() -> int:
    check("ROLE_ORDER_0123", ROLE == (0, 1, 2, 3))
    check("ETA_PLUS_MINUS_MINUS_MINUS", ETA == (1, -1, -1, -1))
    check(
        "SYM_ORDER",
        SYM
        == (
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 2),
            (2, 3),
            (3, 3),
        ),
    )
    check("AMBIENT_1000", AMBIENT == 1000)

    group = full_signature_preserving_group()
    check("GROUP_ORDER_96", len(group) == 96)
    check("GROUP_UNIQUE", len(set(group)) == 96)
    check("EVERY_GROUP_ELEMENT_PRESERVES_ETA", all(preserves_eta(g) for g in group))

    gens = generators()
    generated = generated_subgroup(gens)
    check("SIX_GENERATORS", len(gens) == 6)
    check("GENERATORS_SPAN_FULL_GROUP", generated == set(group))

    dsu_gen, gen_rows, gen_nontrivial = equivariance_constraints(gens)
    roots_gen, zero_gen, dim_gen = dsu_gen.dimension()
    rank_gen = AMBIENT - dim_gen

    # Hostile/redundancy-independent control: all 96 group elements must give
    # the same exact invariant space dimension as the six-generator matrix.
    dsu_full, full_rows, full_nontrivial = equivariance_constraints(group)
    roots_full, zero_full, dim_full = dsu_full.dimension()
    rank_full = AMBIENT - dim_full

    check("GENERATOR_RAW_ROWS_6000", gen_rows == 6000, str(gen_rows))
    check("GENERATOR_NONTRIVIAL_ROWS_3744", gen_nontrivial == 3744, str(gen_nontrivial))
    check("GENERATOR_COMPONENTS_199", roots_gen == 199, str(roots_gen))
    check("GENERATOR_ZERO_COMPONENTS_162", zero_gen == 162, str(zero_gen))
    check("RAW_INVARIANT_DIM_37", dim_gen == 37, str(dim_gen))
    check("EQUIVARIANCE_RANK_963", rank_gen == 963, str(rank_gen))
    check("FULL_GROUP_ROWS_96000", full_rows == 96000, str(full_rows))
    check("FULL_GROUP_NONTRIVIAL_ROWS_84672", full_nontrivial == 84672, str(full_nontrivial))
    check("FULL_GROUP_COMPONENTS_199", roots_full == 199, str(roots_full))
    check("FULL_GROUP_ZERO_COMPONENTS_162", zero_full == 162, str(zero_full))
    check("FULL_GROUP_DIMENSION_MATCHES_GENERATORS", dim_full == dim_gen, f"{dim_full} != {dim_gen}")
    check("FULL_GROUP_RANK_MATCHES_GENERATORS", rank_full == rank_gen, f"{rank_full} != {rank_gen}")

    print("ROLE_ORDER:", ROLE)
    print("ETA:", ETA)
    print("SYM_ORDER:", SYM)
    print("GROUP_ORDER:", len(group))
    print("AMBIENT_COEFFICIENTS:", AMBIENT)
    print("EQUIVARIANCE_ROWS_GENERATORS:", gen_rows)
    print("EQUIVARIANCE_NONTRIVIAL_ROWS_GENERATORS:", gen_nontrivial)
    print("EQUIVARIANCE_RANK:", rank_gen)
    print("RAW_INVARIANT_DIM:", dim_gen)
    print("SCOPE: equivariance scaffold only; no self-adjoint/gauge/divergence constraints; no E_sp named")
    print("ELIN-ESP-REPRESENTATION-SCAFFOLD-EXACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
