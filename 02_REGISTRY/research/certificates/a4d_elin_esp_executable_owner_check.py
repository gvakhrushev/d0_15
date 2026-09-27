#!/usr/bin/env python3
"""Exact executable owner recovery for the E-LIN Lorentz two-ray response space.

This certificate reconstructs the degree-two response tensor from the finite
axioms recorded by E-LIN. It does not read/import #262 or #265 data and never
uses a J2 orbit to choose a basis.

Coefficient convention
----------------------
Role order is (0,1,2,3), eta=diag(+1,-1,-1,-1), and every Sym^2 factor uses

  SYM = ((0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)).

The unrestricted coefficient tensor is
  C[out_sym, in_sym, deriv_sym], 10*10*10 = 1000 coefficients,
where deriv_sym=(r,s) denotes D_r D_s with r<=s and no hidden multiplicity.

The finite symmetry is the full signed-hypercubic subgroup preserving eta:
time is fixed by permutations, S3 permutes the spatial roles, and all four
independent sign reflections are allowed. Its order is 96.

Self-adjointness uses the Lorentz-induced pairing on covariant symmetric
two-tensors. In the stored Sym^2 coordinates its diagonal weight is
  w_(a,b) = (1 if a=b else 2) * eta_a * eta_b.
Gauge and divergence use
  (K xi)_ab = D_a xi_b + D_b xi_a,
  (div E)_b = D^a E_ab = sum_a eta_a D_a E_ab.

The exact solve reproduces a two-dimensional constrained space. The accepted
five-term E_eta ray lies in it. A complementary ray is selected without J2
data: take the canonical RREF null basis in the fixed reduced coefficient
ordering, primitive-normalize every ray with first nonzero coefficient
positive, and choose the lexicographically smallest basis ray independent of
E_eta. That ray is then independently checked to equal, up to the canonical
sign, the purely spatial 3D response predicted by the accepted prose memo.

Public API
----------
- esp_coefficients() -> immutable length-1000 primitive integer owner.
- eeta_coefficients() -> immutable length-1000 primitive integer owner.
- fourier_symbol(coeffs, p) -> exact 10x10 SymPy symbol for p=(p0,p1,p2,p3).
- esp_fourier_symbol(p), eeta_fourier_symbol(p).

Terminal on success:
  ELIN-ESP-EXECUTABLE-OWNER-CERTIFIED
"""
from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import permutations, product
from math import gcd
from typing import Iterable, NamedTuple

import sympy as sp

ROLE = tuple(range(4))
ETA = (1, -1, -1, -1)
SYM = tuple((a, b) for a in ROLE for b in ROLE if a <= b)
PAIR_INDEX = {pair: j for j, pair in enumerate(SYM)}
NSYM = len(SYM)
AMBIENT = NSYM**3
TRIPLES = tuple(
    (a, b, c)
    for a in ROLE
    for b in ROLE
    for c in ROLE
    if a <= b <= c
)
TRIPLE_INDEX = {triple: j for j, triple in enumerate(TRIPLES)}


class GroupElement(NamedTuple):
    # e_a -> signs[a] e_{perm[a]}
    perm: tuple[int, int, int, int]
    signs: tuple[int, int, int, int]


def coeff_index(out_sym: int, in_sym: int, deriv_sym: int) -> int:
    return (out_sym * NSYM + in_sym) * NSYM + deriv_sym


def decode_coeff_index(index: int) -> tuple[int, int, int]:
    out_sym, rem = divmod(index, NSYM * NSYM)
    in_sym, deriv_sym = divmod(rem, NSYM)
    return out_sym, in_sym, deriv_sym


def pair_index(a: int, b: int) -> int:
    return PAIR_INDEX[(a, b) if a <= b else (b, a)]


def triple_index(a: int, b: int, c: int) -> int:
    return TRIPLE_INDEX[tuple(sorted((a, b, c)))]


def pair_action(g: GroupElement, pair: tuple[int, int]) -> tuple[int, int]:
    a, b = pair
    aa, bb = g.perm[a], g.perm[b]
    sign = g.signs[a] * g.signs[b]
    return pair_index(aa, bb), sign


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
    return all(
        ETA[g.perm[a]] == ETA[a] and g.signs[a] in (-1, 1)
        for a in ROLE
    )


class SignedDSU:
    """Exact solver for incidence constraints x = sign*y, sign in {+1,-1}."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
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
        if sign not in (-1, 1):
            raise ValueError("constraint sign must be +/-1")
        rx, sx = self.find(x)
        ry, sy = self.find(y)
        if rx == ry:
            if sx != sign * sy:
                self.forced_zero[rx] = True
            return
        self.parent[rx] = ry
        self.relative[rx] = sign * sy * sx
        self.forced_zero[ry] = self.forced_zero[ry] or self.forced_zero[rx]

    def dimension(self) -> tuple[int, int, int]:
        roots: set[int] = set()
        for x in range(len(self.parent)):
            root, _ = self.find(x)
            roots.add(root)
        zero_roots = sum(1 for root in roots if self.forced_zero[root])
        return len(roots), zero_roots, len(roots) - zero_roots


def impose_equivariance(
    elements: Iterable[GroupElement],
) -> tuple[SignedDSU, int, int]:
    """Build exact rows C_i - sign*C_j = 0."""
    dsu = SignedDSU(AMBIENT)
    raw_rows = 0
    nontrivial_rows = 0
    for g in elements:
        actions = tuple(pair_action(g, pair) for pair in SYM)
        for out_sym, (out_new, out_sign) in enumerate(actions):
            for in_sym, (in_new, in_sign) in enumerate(actions):
                for deriv_sym, (deriv_new, deriv_sign) in enumerate(actions):
                    left = coeff_index(out_sym, in_sym, deriv_sym)
                    right = coeff_index(out_new, in_new, deriv_new)
                    sign = out_sign * in_sign * deriv_sign
                    raw_rows += 1
                    if left != right or sign != 1:
                        nontrivial_rows += 1
                    dsu.impose(left, right, sign)
    return dsu, raw_rows, nontrivial_rows


def canonical_reduction(
    dsu: SignedDSU,
) -> tuple[tuple[tuple[int, int] | None, ...], tuple[int, ...]]:
    """Canonical quotient map; C_x = sign*u_j, ordered by minimum index."""
    components: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for x in range(AMBIENT):
        root, sign = dsu.find(x)
        components[root].append((x, sign))

    free: list[tuple[int, int, int]] = []
    for root, items in components.items():
        if dsu.forced_zero[root]:
            continue
        representative = min(x for x, _ in items)
        rep_sign = next(sign for x, sign in items if x == representative)
        free.append((representative, root, rep_sign))
    free.sort()

    root_to_j = {root: j for j, (_, root, _) in enumerate(free)}
    root_rep_sign = {root: rep_sign for _, root, rep_sign in free}
    mapping: list[tuple[int, int] | None] = []
    for x in range(AMBIENT):
        root, sign_to_root = dsu.find(x)
        if dsu.forced_zero[root]:
            mapping.append(None)
        else:
            mapping.append(
                (root_to_j[root], sign_to_root * root_rep_sign[root])
            )
    return tuple(mapping), tuple(rep for rep, _, _ in free)


def add_reduced(
    row: list[int],
    mapping: tuple[tuple[int, int] | None, ...],
    ambient_index: int,
    scale: int,
) -> None:
    item = mapping[ambient_index]
    if item is None:
        return
    j, sign = item
    row[j] += scale * sign


def sym_pairing_weight(pair: tuple[int, int]) -> int:
    a, b = pair
    multiplicity = 1 if a == b else 2
    return multiplicity * ETA[a] * ETA[b]


def self_adjoint_rows(
    mapping: tuple[tuple[int, int] | None, ...],
    nred: int,
) -> list[tuple[int, ...]]:
    rows: list[tuple[int, ...]] = []
    for out_sym in range(NSYM):
        for in_sym in range(out_sym + 1, NSYM):
            w_out = sym_pairing_weight(SYM[out_sym])
            w_in = sym_pairing_weight(SYM[in_sym])
            for deriv_sym in range(NSYM):
                row = [0] * nred
                add_reduced(
                    row, mapping,
                    coeff_index(out_sym, in_sym, deriv_sym),
                    w_out,
                )
                add_reduced(
                    row, mapping,
                    coeff_index(in_sym, out_sym, deriv_sym),
                    -w_in,
                )
                if any(row):
                    rows.append(tuple(row))
    return rows


def divergence_rows(
    mapping: tuple[tuple[int, int] | None, ...],
    nred: int,
) -> list[tuple[int, ...]]:
    equations: dict[tuple[int, int, int], list[int]] = defaultdict(
        lambda: [0] * nred
    )
    for b in ROLE:
        for a in ROLE:
            out_sym = pair_index(a, b)
            for in_sym in range(NSYM):
                for deriv_sym, (r, s) in enumerate(SYM):
                    key = (b, in_sym, triple_index(a, r, s))
                    add_reduced(
                        equations[key], mapping,
                        coeff_index(out_sym, in_sym, deriv_sym),
                        ETA[a],
                    )
    return [tuple(row) for row in equations.values() if any(row)]


def gauge_null_rows(
    mapping: tuple[tuple[int, int] | None, ...],
    nred: int,
) -> list[tuple[int, ...]]:
    equations: dict[tuple[int, int, int], list[int]] = defaultdict(
        lambda: [0] * nred
    )
    for out_sym in range(NSYM):
        for in_sym, (c, d) in enumerate(SYM):
            if c == d:
                gauge_terms = ((c, c, 2),)
            else:
                gauge_terms = ((c, d, 1), (d, c, 1))
            for deriv_sym, (r, s) in enumerate(SYM):
                ambient_index = coeff_index(out_sym, in_sym, deriv_sym)
                for first_deriv, xi_component, scale in gauge_terms:
                    key = (
                        out_sym,
                        xi_component,
                        triple_index(first_deriv, r, s),
                    )
                    add_reduced(
                        equations[key], mapping, ambient_index, scale
                    )
    return [tuple(row) for row in equations.values() if any(row)]


def primitive_integer_ray(vector: sp.Matrix) -> sp.Matrix:
    rationals = [sp.Rational(x) for x in vector]
    lcm = 1
    for x in rationals:
        lcm = int(sp.ilcm(lcm, x.q))
    ints = [int(x * lcm) for x in rationals]
    common = 0
    for value in ints:
        if value:
            common = gcd(common, abs(value))
    if common == 0:
        raise ValueError("zero vector has no projective normalization")
    ints = [value // common for value in ints]
    for value in ints:
        if value:
            if value < 0:
                ints = [-x for x in ints]
            break
    return sp.Matrix(ints)


def canonical_null_basis(matrix: sp.Matrix) -> tuple[sp.Matrix, ...]:
    rref, pivots = matrix.rref()
    pivot_set = set(pivots)
    free_cols = [j for j in range(matrix.cols) if j not in pivot_set]
    basis = []
    for free_col in free_cols:
        v = [sp.Rational(0)] * matrix.cols
        v[free_col] = sp.Rational(1)
        for row, pivot_col in enumerate(pivots):
            v[pivot_col] = -rref[row, free_col]
        basis.append(primitive_integer_ray(sp.Matrix(v)))
    return tuple(basis)


def proportional(a: sp.Matrix, b: sp.Matrix) -> bool:
    return sp.Matrix.hstack(a, b).rank() < 2


def expand_reduced(
    reduced: sp.Matrix,
    mapping: tuple[tuple[int, int] | None, ...],
) -> sp.Matrix:
    values = []
    for item in mapping:
        if item is None:
            values.append(sp.Integer(0))
        else:
            j, sign = item
            values.append(sp.Integer(sign) * reduced[j])
    return sp.Matrix(values)


def reduce_ambient(
    ambient: sp.Matrix,
    dsu: SignedDSU,
    mapping: tuple[tuple[int, int] | None, ...],
    nred: int,
) -> sp.Matrix:
    values: list[sp.Rational | None] = [None] * nred
    for x, value in enumerate(ambient):
        item = mapping[x]
        if item is None:
            if value != 0:
                raise AssertionError(
                    f"candidate violates symmetry-forced zero at ambient {x}"
                )
            continue
        j, sign = item
        reduced_value = sp.Rational(value) * sign
        if values[j] is None:
            values[j] = reduced_value
        elif values[j] != reduced_value:
            raise AssertionError(
                f"candidate violates equivariance in reduced component {j}"
            )
    return sp.Matrix([sp.Rational(0) if v is None else v for v in values])


def add_ambient(
    coeffs: list[sp.Rational],
    out_pair: tuple[int, int],
    in_pair: tuple[int, int],
    deriv_pair: tuple[int, int],
    value: int | sp.Rational,
) -> None:
    coeffs[
        coeff_index(
            pair_index(*out_pair),
            pair_index(*in_pair),
            pair_index(*deriv_pair),
        )
    ] += sp.Rational(value)


def five_term_e_eta_raw() -> sp.Matrix:
    """Five-term Lorentz ray (A,B,C,D,F)=(1,-1,1,1,-1)."""
    coeffs = [sp.Rational(0)] * AMBIENT
    A, B, C, D, F = map(sp.Rational, (1, -1, 1, 1, -1))
    for a in ROLE:
        for b in range(a, 4):
            out_pair = (a, b)
            for r in ROLE:
                add_ambient(coeffs, out_pair, out_pair, (r, r), A * ETA[r])
            for c in ROLE:
                add_ambient(
                    coeffs, out_pair, (c, b), (a, c), B * ETA[c]
                )
                add_ambient(
                    coeffs, out_pair, (c, a), (b, c), B * ETA[c]
                )
            for c in ROLE:
                add_ambient(
                    coeffs, out_pair, (c, c), (a, b), C * ETA[c]
                )
            if a == b:
                eta_ab = ETA[a]
                for c in ROLE:
                    add_ambient(
                        coeffs, out_pair, (c, c), (c, c), D * eta_ab
                    )
                for c in ROLE:
                    for d in range(c + 1, 4):
                        add_ambient(
                            coeffs,
                            out_pair,
                            (c, d),
                            (c, d),
                            D * eta_ab * 2 * ETA[c] * ETA[d],
                        )
                for r in ROLE:
                    for c in ROLE:
                        add_ambient(
                            coeffs,
                            out_pair,
                            (c, c),
                            (r, r),
                            F * eta_ab * ETA[r] * ETA[c],
                        )
    return sp.Matrix(coeffs)


def purely_spatial_3d_raw() -> sp.Matrix:
    """Euclidean 3D five-term response embedded in roles {1,2,3}."""
    coeffs = [sp.Rational(0)] * AMBIENT
    spatial = (1, 2, 3)
    A, B, C, D, F = map(sp.Rational, (1, -1, 1, 1, -1))
    for a in spatial:
        for b in spatial:
            if a > b:
                continue
            out_pair = (a, b)
            for r in spatial:
                add_ambient(coeffs, out_pair, out_pair, (r, r), A)
            for c in spatial:
                add_ambient(coeffs, out_pair, (c, b), (a, c), B)
                add_ambient(coeffs, out_pair, (c, a), (b, c), B)
            for c in spatial:
                add_ambient(coeffs, out_pair, (c, c), (a, b), C)
            if a == b:
                for c in spatial:
                    add_ambient(coeffs, out_pair, (c, c), (c, c), D)
                for c in spatial:
                    for d in spatial:
                        if c < d:
                            add_ambient(
                                coeffs, out_pair, (c, d), (c, d), 2 * D
                            )
                for r in spatial:
                    for c in spatial:
                        add_ambient(
                            coeffs, out_pair, (c, c), (r, r), F
                        )
    return sp.Matrix(coeffs)


def _solve_owner() -> dict[str, object]:
    group = full_signature_preserving_group()
    gens = generators()
    dsu, raw_rows, nontrivial_rows = impose_equivariance(gens)
    mapping, representatives = canonical_reduction(dsu)
    nred = len(representatives)

    self_m = sp.Matrix(self_adjoint_rows(mapping, nred))
    div_m = sp.Matrix(divergence_rows(mapping, nred))
    gauge_m = sp.Matrix(gauge_null_rows(mapping, nred))
    combined = sp.Matrix.vstack(self_m, div_m, gauge_m)

    null_basis = canonical_null_basis(combined)
    eeta_raw = five_term_e_eta_raw()
    eeta_red = primitive_integer_ray(
        reduce_ambient(eeta_raw, dsu, mapping, nred)
    )

    candidates = [
        ray for ray in null_basis if not proportional(ray, eeta_red)
    ]
    if not candidates:
        raise AssertionError("no complementary constrained ray")
    esp_red = min(candidates, key=lambda v: tuple(int(x) for x in v))
    esp_ambient = primitive_integer_ray(expand_reduced(esp_red, mapping))
    eeta_ambient = primitive_integer_ray(eeta_raw)
    spatial = primitive_integer_ray(purely_spatial_3d_raw())

    return {
        "group": group,
        "gens": gens,
        "dsu": dsu,
        "raw_rows": raw_rows,
        "nontrivial_rows": nontrivial_rows,
        "mapping": mapping,
        "representatives": representatives,
        "self_m": self_m,
        "div_m": div_m,
        "gauge_m": gauge_m,
        "combined": combined,
        "null_basis": null_basis,
        "eeta_red": eeta_red,
        "esp_red": esp_red,
        "eeta_ambient": eeta_ambient,
        "esp_ambient": esp_ambient,
        "spatial": spatial,
    }


@lru_cache(maxsize=1)
def esp_coefficients() -> tuple[int, ...]:
    solved = _solve_owner()
    return tuple(int(x) for x in solved["esp_ambient"])


@lru_cache(maxsize=1)
def eeta_coefficients() -> tuple[int, ...]:
    solved = _solve_owner()
    return tuple(int(x) for x in solved["eeta_ambient"])


def fourier_symbol(
    coeffs: Iterable[int | sp.Rational],
    p: Iterable[int | sp.Rational | sp.Expr],
) -> sp.Matrix:
    """Evaluate the exact 10x10 degree-two symbol at p=(p0,p1,p2,p3)."""
    coeffs = tuple(sp.sympify(x) for x in coeffs)
    p = tuple(sp.sympify(x) for x in p)
    if len(coeffs) != AMBIENT:
        raise ValueError(f"expected {AMBIENT} coefficients")
    if len(p) != 4:
        raise ValueError("expected four derivative values")
    symbol = sp.zeros(NSYM, NSYM)
    for index, value in enumerate(coeffs):
        if value == 0:
            continue
        out_sym, in_sym, deriv_sym = decode_coeff_index(index)
        r, s = SYM[deriv_sym]
        symbol[out_sym, in_sym] += value * p[r] * p[s]
    return symbol


def esp_fourier_symbol(
    p: Iterable[int | sp.Rational | sp.Expr],
) -> sp.Matrix:
    return fourier_symbol(esp_coefficients(), p)


def eeta_fourier_symbol(
    p: Iterable[int | sp.Rational | sp.Expr],
) -> sp.Matrix:
    return fourier_symbol(eeta_coefficients(), p)


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
            (0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
            (1, 2), (1, 3), (2, 2), (2, 3), (3, 3),
        ),
    )
    check("AMBIENT_1000", AMBIENT == 1000)

    solved = _solve_owner()
    group = solved["group"]
    gens = solved["gens"]
    dsu = solved["dsu"]
    mapping = solved["mapping"]
    reps = solved["representatives"]
    self_m = solved["self_m"]
    div_m = solved["div_m"]
    gauge_m = solved["gauge_m"]
    combined = solved["combined"]
    null_basis = solved["null_basis"]
    eeta_red = solved["eeta_red"]
    esp_red = solved["esp_red"]
    esp_ambient = solved["esp_ambient"]
    spatial = solved["spatial"]

    check("GROUP_ORDER_96", len(group) == 96)
    check("GROUP_UNIQUE", len(set(group)) == 96)
    check(
        "EVERY_GROUP_ELEMENT_PRESERVES_ETA",
        all(preserves_eta(g) for g in group),
    )
    check("SIX_GENERATORS", len(gens) == 6)
    check("GENERATORS_SPAN_FULL_GROUP", generated_subgroup(gens) == set(group))

    roots, zero_components, raw_dim = dsu.dimension()
    check("GENERATOR_RAW_ROWS_6000", solved["raw_rows"] == 6000)
    check(
        "GENERATOR_NONTRIVIAL_ROWS_3744",
        solved["nontrivial_rows"] == 3744,
    )
    check("EQUIVARIANCE_COMPONENTS_199", roots == 199, str(roots))
    check(
        "EQUIVARIANCE_ZERO_COMPONENTS_162",
        zero_components == 162,
        str(zero_components),
    )
    check("RAW_INVARIANT_DIM_37", raw_dim == 37, str(raw_dim))
    check("EQUIVARIANCE_RANK_963", AMBIENT - raw_dim == 963)

    full_dsu, full_rows, full_nontrivial = impose_equivariance(group)
    _, _, full_dim = full_dsu.dimension()
    check("FULL_GROUP_ROWS_96000", full_rows == 96000)
    check("FULL_GROUP_NONTRIVIAL_ROWS_84672", full_nontrivial == 84672)
    check("FULL_GROUP_RAW_DIM_37", full_dim == 37, str(full_dim))

    check("REDUCED_VARIABLES_37", len(reps) == 37)
    check("SELF_ADJOINT_ROWS_48", self_m.rows == 48, str(self_m.rows))
    check("SELF_ADJOINT_RANK_11", self_m.rank() == 11, str(self_m.rank()))
    check("SELF_ADJOINT_DIM_26", 37 - self_m.rank() == 26)
    check("GAUGE_ROWS_124", gauge_m.rows == 124, str(gauge_m.rows))
    check("GAUGE_RANK_28", gauge_m.rank() == 28, str(gauge_m.rank()))
    check("GAUGE_DIM_9", 37 - gauge_m.rank() == 9)
    check("DIVERGENCE_ROWS_124", div_m.rows == 124, str(div_m.rows))
    check("DIVERGENCE_RANK_28", div_m.rank() == 28, str(div_m.rank()))
    check("DIVERGENCE_DIM_9", 37 - div_m.rank() == 9)
    check("COMBINED_RANK_35", combined.rank() == 35, str(combined.rank()))
    check("CONSTRAINED_DIMENSION_2", 37 - combined.rank() == 2)
    check("NULL_BASIS_HAS_TWO_RAYS", len(null_basis) == 2)

    check("EETA_IN_KERNEL", (combined * eeta_red).is_zero_matrix)
    check("ESP_IN_KERNEL", (combined * esp_red).is_zero_matrix)
    check(
        "EETA_ESP_INDEPENDENT",
        sp.Matrix.hstack(eeta_red, esp_red).rank() == 2,
    )
    check(
        "EETA_ESP_SPAN_CONSTRAINED_KERNEL",
        sp.Matrix.hstack(eeta_red, esp_red).rank() == len(null_basis) == 2,
    )
    check(
        "ESP_EQUALS_CANONICAL_SPATIAL_RAY",
        esp_ambient == spatial or esp_ambient == -spatial,
    )
    check(
        "ESP_CANONICAL_SIGN_FIRST_NONZERO_POSITIVE",
        next(x for x in esp_ambient if x != 0) > 0,
    )
    check(
        "ESP_PURELY_SPATIAL",
        all(
            value == 0
            for index, value in enumerate(esp_ambient)
            if 0 in SYM[decode_coeff_index(index)[0]]
            or 0 in SYM[decode_coeff_index(index)[1]]
            or 0 in SYM[decode_coeff_index(index)[2]]
        ),
    )

    hostile = sp.Matrix(esp_ambient)
    first_nonzero = next(i for i, value in enumerate(hostile) if value != 0)
    hostile[first_nonzero] += 1
    hostile_failed = False
    try:
        hostile_red = reduce_ambient(hostile, dsu, mapping, len(reps))
        hostile_failed = not (combined * hostile_red).is_zero_matrix
    except AssertionError:
        hostile_failed = True
    check("HOSTILE_SINGLE_COEFFICIENT_PERTURBATION_REJECTED", hostile_failed)

    p0, p1, p2, p3 = sp.symbols("p0 p1 p2 p3")
    esp_symbol = esp_fourier_symbol((p0, p1, p2, p3))
    eeta_symbol = eeta_fourier_symbol((p0, p1, p2, p3))
    check("ESP_SYMBOL_SHAPE_10x10", esp_symbol.shape == (10, 10))
    check("EETA_SYMBOL_SHAPE_10x10", eeta_symbol.shape == (10, 10))
    check(
        "ESP_SYMBOL_TIME_ROWS_ZERO",
        all(
            esp_symbol[j, k] == 0
            for j, pair in enumerate(SYM)
            if 0 in pair
            for k in range(NSYM)
        ),
    )
    check(
        "ESP_SYMBOL_TIME_COLS_ZERO",
        all(
            esp_symbol[j, k] == 0
            for k, pair in enumerate(SYM)
            if 0 in pair
            for j in range(NSYM)
        ),
    )

    esp_nz = [
        (
            SYM[decode_coeff_index(i)[0]],
            SYM[decode_coeff_index(i)[1]],
            SYM[decode_coeff_index(i)[2]],
            int(value),
        )
        for i, value in enumerate(esp_ambient)
        if value != 0
    ]
    check(
        "ESP_NONZERO_COEFFICIENT_COUNT_21",
        len(esp_nz) == 21,
        str(len(esp_nz)),
    )

    print("GROUP_ORDER:", len(group))
    print("AMBIENT_COEFFICIENTS:", AMBIENT)
    print("EQUIVARIANCE_RANK:", AMBIENT - raw_dim)
    print("RAW_INVARIANT_DIM:", raw_dim)
    print("SELF_ADJOINT_DIM:", 37 - self_m.rank())
    print("GAUGE_NULL_DIM:", 37 - gauge_m.rank())
    print("DIVERGENCE_FREE_DIM:", 37 - div_m.rank())
    print("CONSTRAINED_DIM:", 37 - combined.rank())
    print("ESP_NONZERO_COEFFICIENTS:")
    for item in esp_nz:
        print(" ", item)
    print("ELIN-ESP-EXECUTABLE-OWNER-CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
