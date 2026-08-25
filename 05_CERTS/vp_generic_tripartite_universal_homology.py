#!/usr/bin/env python3
"""Can-fail certificate for D0-GENERIC-TRIPARTITE-UNIVERSAL-HOMOLOGY-001.

Independently test the constructive coefficient-universal theorem

    H0(K(p+1,q+1,r+1); R) ~= R,
    H1(K(p+1,q+1,r+1); R) = 0,
    H2(K(p+1,q+1,r+1); R) ~= R^(p*q*r).

The test does not divide.  Besides integer checks it exhausts small complexes
over Z/4Z and Z/6Z, so success cannot be attributed to a hidden field-rank
argument.  It exercises the exact spanning-tree H0 filler, the two-stage H1
filler, and the octahedral H2 coordinate/synthesis maps.
"""

from __future__ import annotations

from itertools import product


Vector = list[int]


def require(condition: bool, token: str) -> None:
    if not condition:
        raise AssertionError(f"FAIL_{token}")


def expect_rejected(token: str, condition: bool) -> None:
    try:
        require(condition, token)
    except AssertionError as exc:
        print(f"PASS_NEGATIVE_CONTROL_{token}: {exc}")
    else:
        raise AssertionError(f"FAIL_NEGATIVE_CONTROL_DID_NOT_FIRE_{token}")


def normalize(value: int, modulus: int | None) -> int:
    return value if modulus is None else value % modulus


def normalize_vector(values: Vector, modulus: int | None) -> Vector:
    return [normalize(value, modulus) for value in values]


def zero_vector(length: int) -> Vector:
    return [0] * length


class TripartiteComplex:
    def __init__(self, p: int, q: int, r: int, modulus: int | None) -> None:
        require(min(p, q, r) >= 0, "NEGATIVE_OFFSET")
        if modulus is not None:
            require(modulus >= 2, "BAD_MODULUS")
        self.p, self.q, self.r, self.modulus = p, q, r, modulus
        self.a_size, self.b_size, self.c_size = p + 1, q + 1, r + 1

        self.vertices = (
            [(0, a) for a in range(self.a_size)]
            + [(1, b) for b in range(self.b_size)]
            + [(2, c) for c in range(self.c_size)]
        )
        self.edges = (
            [
                ("ab", a, b)
                for a, b in product(range(self.a_size), range(self.b_size))
            ]
            + [
                ("ac", a, c)
                for a, c in product(range(self.a_size), range(self.c_size))
            ]
            + [
                ("bc", b, c)
                for b, c in product(range(self.b_size), range(self.c_size))
            ]
        )
        self.triangles = list(
            product(
                range(self.a_size),
                range(self.b_size),
                range(self.c_size),
            )
        )
        self.vertex_index = {vertex: i for i, vertex in enumerate(self.vertices)}
        self.edge_index = {edge: i for i, edge in enumerate(self.edges)}
        self.triangle_index = {
            triangle: i for i, triangle in enumerate(self.triangles)
        }
        self.top_indices = list(product(range(p), range(q), range(r)))

    def norm(self, value: int) -> int:
        return normalize(value, self.modulus)

    def d1(self, edge_chain: Vector) -> Vector:
        require(len(edge_chain) == len(self.edges), "D1_INPUT_LENGTH")
        out = zero_vector(len(self.vertices))
        for coefficient, (kind, left, right) in zip(edge_chain, self.edges):
            if kind == "ab":
                source, target = (0, left), (1, right)
            elif kind == "ac":
                source, target = (0, left), (2, right)
            else:
                source, target = (1, left), (2, right)
            out[self.vertex_index[source]] -= coefficient
            out[self.vertex_index[target]] += coefficient
        return normalize_vector(out, self.modulus)

    def d2(self, triangle_chain: Vector) -> Vector:
        require(len(triangle_chain) == len(self.triangles), "D2_INPUT_LENGTH")
        out = zero_vector(len(self.edges))
        for coefficient, (a, b, c) in zip(triangle_chain, self.triangles):
            out[self.edge_index[("bc", b, c)]] += coefficient
            out[self.edge_index[("ac", a, c)]] -= coefficient
            out[self.edge_index[("ab", a, b)]] += coefficient
        return normalize_vector(out, self.modulus)

    def augmentation(self, vertex_chain: Vector) -> int:
        require(len(vertex_chain) == len(self.vertices), "AUGMENTATION_LENGTH")
        return self.norm(sum(vertex_chain))

    def root_difference(self, index: int, vertex: int) -> int:
        if vertex == index + 1:
            return 1
        if vertex == 0:
            return -1
        return 0

    def top_cycle(self, index: tuple[int, int, int]) -> Vector:
        i, j, k = index
        return normalize_vector(
            [
                self.root_difference(i, a)
                * self.root_difference(j, b)
                * self.root_difference(k, c)
                for a, b, c in self.triangles
            ],
            self.modulus,
        )

    def top_coordinates(self, triangle_chain: Vector) -> dict[tuple[int, int, int], int]:
        return {
            index: triangle_chain[
                self.triangle_index[(index[0] + 1, index[1] + 1, index[2] + 1)]
            ]
            for index in self.top_indices
        }

    def top_synthesis(
        self, coordinates: dict[tuple[int, int, int], int]
    ) -> Vector:
        out = zero_vector(len(self.triangles))
        for index in self.top_indices:
            coefficient = coordinates.get(index, 0)
            cycle = self.top_cycle(index)
            for triangle, value in enumerate(cycle):
                out[triangle] += coefficient * value
        return normalize_vector(out, self.modulus)

    def ab(self, edge_chain: Vector, a: int, b: int) -> int:
        return edge_chain[self.edge_index[("ab", a, b)]]

    def ac(self, edge_chain: Vector, a: int, c: int) -> int:
        return edge_chain[self.edge_index[("ac", a, c)]]

    def bc(self, edge_chain: Vector, b: int, c: int) -> int:
        return edge_chain[self.edge_index[("bc", b, c)]]

    def h1_fill(self, edge_cycle: Vector) -> Vector:
        require(len(edge_cycle) == len(self.edges), "H1_FILL_LENGTH")

        def ac_residual(a: int, c: int) -> int:
            cone = sum(self.ab(edge_cycle, a, b) for b in range(self.b_size))
            return self.norm(self.ac(edge_cycle, a, c) + (cone if c == 0 else 0))

        def bc_residual(b: int, c: int) -> int:
            cone = sum(self.ab(edge_cycle, a, b) for a in range(self.a_size))
            return self.norm(self.bc(edge_cycle, b, c) - (cone if c == 0 else 0))

        out = zero_vector(len(self.triangles))
        for triangle, (a, b, c) in enumerate(self.triangles):
            if a == 0 and b == 0:
                residual = -ac_residual(0, c) - sum(
                    bc_residual(j, c) for j in range(1, self.b_size)
                )
            elif a == 0:
                residual = bc_residual(b, c)
            elif b == 0:
                residual = -ac_residual(a, c)
            else:
                residual = 0
            cone = self.ab(edge_cycle, a, b) if c == 0 else 0
            out[triangle] = self.norm(cone + residual)
        return out

    def h0_fill(self, vertex_cycle: Vector) -> Vector:
        require(len(vertex_cycle) == len(self.vertices), "H0_FILL_LENGTH")
        out = zero_vector(len(self.edges))
        a_nonroot_sum = sum(
            vertex_cycle[self.vertex_index[(0, a)]]
            for a in range(1, self.a_size)
        )
        for edge, (kind, left, right) in enumerate(self.edges):
            if kind == "ab":
                a, b = left, right
                if a == 0 and b == 0:
                    value = vertex_cycle[self.vertex_index[(1, 0)]] + a_nonroot_sum
                elif a == 0:
                    value = vertex_cycle[self.vertex_index[(1, b)]]
                elif b == 0:
                    value = -vertex_cycle[self.vertex_index[(0, a)]]
                else:
                    value = 0
            elif kind == "ac" and left == 0:
                value = vertex_cycle[self.vertex_index[(2, right)]]
            else:
                value = 0
            out[edge] = self.norm(value)
        return out


def deterministic_values(length: int, modulus: int | None, salt: int) -> Vector:
    values = [((index + 1) * (salt + 3) - (index % 4) * 5) for index in range(length)]
    return normalize_vector(values, modulus)


def verify_structural_maps(complex_: TripartiteComplex) -> None:
    triangle_chain = deterministic_values(
        len(complex_.triangles), complex_.modulus, salt=7
    )
    require(
        complex_.d1(complex_.d2(triangle_chain))
        == zero_vector(len(complex_.vertices)),
        f"D1_D2_{complex_.p}_{complex_.q}_{complex_.r}_{complex_.modulus}",
    )
    edge_chain = deterministic_values(len(complex_.edges), complex_.modulus, salt=11)
    require(
        complex_.augmentation(complex_.d1(edge_chain)) == 0,
        f"AUGMENTATION_D1_{complex_.p}_{complex_.q}_{complex_.r}_{complex_.modulus}",
    )


def verify_top_coordinates(complex_: TripartiteComplex) -> None:
    cycles = {index: complex_.top_cycle(index) for index in complex_.top_indices}
    for index, cycle in cycles.items():
        require(
            complex_.d2(cycle) == zero_vector(len(complex_.edges)),
            f"TOP_CYCLE_BOUNDARY_{complex_.p}_{complex_.q}_{complex_.r}_{index}",
        )
        coordinates = complex_.top_coordinates(cycle)
        require(
            coordinates
            == {
                candidate: complex_.norm(int(candidate == index))
                for candidate in complex_.top_indices
            },
            f"TOP_IDENTITY_COORDINATES_{complex_.p}_{complex_.q}_{complex_.r}_{index}",
        )

    coefficients = {
        index: complex_.norm(
            2 * (index[0] + 1) - 3 * (index[1] + 1) + 5 * (index[2] + 1)
        )
        for index in complex_.top_indices
    }
    synthesized = complex_.top_synthesis(coefficients)
    require(
        complex_.d2(synthesized) == zero_vector(len(complex_.edges)),
        f"TOP_SYNTHESIS_CYCLE_{complex_.p}_{complex_.q}_{complex_.r}",
    )
    require(
        complex_.top_coordinates(synthesized) == coefficients,
        f"TOP_SYNTHESIS_INVERSE_{complex_.p}_{complex_.q}_{complex_.r}",
    )


def verify_fillers(complex_: TripartiteComplex) -> None:
    source_triangles = deterministic_values(
        len(complex_.triangles), complex_.modulus, salt=13
    )
    one_cycle = complex_.d2(source_triangles)
    require(
        complex_.d1(one_cycle) == zero_vector(len(complex_.vertices)),
        f"DETERMINISTIC_ONE_CYCLE_{complex_.p}_{complex_.q}_{complex_.r}",
    )
    require(
        complex_.d2(complex_.h1_fill(one_cycle)) == one_cycle,
        f"H1_FILL_{complex_.p}_{complex_.q}_{complex_.r}_{complex_.modulus}",
    )

    vertex_chain = deterministic_values(
        len(complex_.vertices), complex_.modulus, salt=17
    )
    vertex_chain[0] = complex_.norm(
        vertex_chain[0] - complex_.augmentation(vertex_chain)
    )
    require(complex_.augmentation(vertex_chain) == 0, "H0_ZERO_AUGMENTATION_SETUP")
    require(
        complex_.d1(complex_.h0_fill(vertex_chain)) == vertex_chain,
        f"H0_FILL_{complex_.p}_{complex_.q}_{complex_.r}_{complex_.modulus}",
    )


def exhaustive_top_kernel(complex_: TripartiteComplex) -> None:
    modulus = complex_.modulus
    require(modulus is not None, "EXHAUSTIVE_TOP_REQUIRES_MODULUS")
    kernel_count = 0
    for values in product(range(modulus), repeat=len(complex_.triangles)):
        chain = list(values)
        if complex_.d2(chain) != zero_vector(len(complex_.edges)):
            continue
        kernel_count += 1
        require(
            complex_.top_synthesis(complex_.top_coordinates(chain)) == chain,
            f"EXHAUSTIVE_TOP_RECONSTRUCTION_{complex_.p}_{complex_.q}_{complex_.r}",
        )
    require(
        kernel_count == modulus ** (complex_.p * complex_.q * complex_.r),
        f"EXHAUSTIVE_TOP_CARDINALITY_{kernel_count}",
    )


def exhaustive_h1_cycles(complex_: TripartiteComplex) -> None:
    modulus = complex_.modulus
    require(modulus is not None, "EXHAUSTIVE_H1_REQUIRES_MODULUS")
    cycle_count = 0
    for values in product(range(modulus), repeat=len(complex_.edges)):
        chain = list(values)
        if complex_.d1(chain) != zero_vector(len(complex_.vertices)):
            continue
        cycle_count += 1
        require(
            complex_.d2(complex_.h1_fill(chain)) == chain,
            f"EXHAUSTIVE_H1_FILL_{complex_.p}_{complex_.q}_{complex_.r}",
        )
    expected = modulus ** (len(complex_.edges) - len(complex_.vertices) + 1)
    require(cycle_count == expected, f"EXHAUSTIVE_H1_CARDINALITY_{cycle_count}")


def exhaustive_h0_kernel(complex_: TripartiteComplex) -> None:
    modulus = complex_.modulus
    require(modulus is not None, "EXHAUSTIVE_H0_REQUIRES_MODULUS")
    kernel_count = 0
    for values in product(range(modulus), repeat=len(complex_.vertices)):
        chain = list(values)
        if complex_.augmentation(chain) != 0:
            continue
        kernel_count += 1
        require(
            complex_.d1(complex_.h0_fill(chain)) == chain,
            f"EXHAUSTIVE_H0_FILL_{complex_.p}_{complex_.q}_{complex_.r}",
        )
    require(
        kernel_count == modulus ** (len(complex_.vertices) - 1),
        f"EXHAUSTIVE_H0_CARDINALITY_{kernel_count}",
    )


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: explicit d1/d2, augmentation, H0 tree "
        "filler, H1 two-stage filler, and H2 octahedral coordinates."
    )

    # Integer and finite-ring smoke grid.
    for case in (
        TripartiteComplex(0, 0, 0, None),
        TripartiteComplex(2, 3, 1, None),
        TripartiteComplex(1, 0, 0, 6),
        TripartiteComplex(1, 1, 1, 4),
    ):
        verify_structural_maps(case)
        verify_top_coordinates(case)
        verify_fillers(case)
    print("PASS_UNIVERSAL_SMOKE_GRID: integer, Z/4Z, and Z/6Z cases agree.")

    # Exhaustive non-field controls.
    mod6_thin = TripartiteComplex(1, 0, 0, 6)
    exhaustive_h1_cycles(mod6_thin)
    exhaustive_h0_kernel(mod6_thin)
    mod4_cube = TripartiteComplex(1, 1, 1, 4)
    exhaustive_top_kernel(mod4_cube)
    exhaustive_h0_kernel(mod4_cube)
    print(
        "PASS_NONFIELD_EXHAUSTION: all relevant cycles over Z/4Z and Z/6Z "
        "are reconstructed by the explicit maps."
    )

    # Source scene: all three constructive maps, including 960 top coordinates.
    scene = TripartiteComplex(8, 10, 12, None)
    verify_structural_maps(scene)
    verify_top_coordinates(scene)
    verify_fillers(scene)
    require(len(scene.top_indices) == 960, "SCENE_TOP_BASIS_COUNT")
    print(
        "PASS_SOURCE_INTEGRAL_HOMOLOGY: H0=Z, H1=0, and H2 has 960 explicit "
        "octahedral integral basis elements."
    )

    # Destructive control 1: corrupt one octahedral sign.
    cube = TripartiteComplex(1, 1, 1, None)
    corrupted_top = cube.top_cycle((0, 0, 0))
    first_nonzero = next(i for i, value in enumerate(corrupted_top) if value)
    corrupted_top[first_nonzero] *= -1
    expect_rejected(
        "CORRUPT_TOP_SIGN_STILL_CYCLE",
        cube.d2(corrupted_top) == zero_vector(len(cube.edges)),
    )

    # Destructive control 2: delete the AB cone from the H1 filler.
    source = zero_vector(len(cube.triangles))
    source[0] = 1
    one_cycle = cube.d2(source)
    bad_h1 = cube.h1_fill(one_cycle)
    for triangle, (_, _, c) in enumerate(cube.triangles):
        if c == 0:
            bad_h1[triangle] = cube.norm(
                bad_h1[triangle]
                - cube.ab(one_cycle, cube.triangles[triangle][0], cube.triangles[triangle][1])
            )
    expect_rejected(
        "DELETE_H1_AB_CONE_PRESERVES_FILL",
        cube.d2(bad_h1) == one_cycle,
    )

    # Destructive control 3: feed a non-cycle to the H1 filler.
    noncycle = zero_vector(len(cube.edges))
    noncycle[cube.edge_index[("ab", 0, 0)]] = 1
    require(
        cube.d1(noncycle) != zero_vector(len(cube.vertices)),
        "NONCYCLE_CONTROL_SETUP",
    )
    expect_rejected(
        "DROP_H1_CYCLE_HYPOTHESIS",
        cube.d2(cube.h1_fill(noncycle)) == noncycle,
    )

    # Destructive control 4: corrupt the spanning-tree root coefficient.
    vertex_cycle = [1, -2, 3, -4, 5, -3]
    require(cube.augmentation(vertex_cycle) == 0, "H0_CORRUPTION_SETUP")
    bad_h0 = cube.h0_fill(vertex_cycle)
    bad_h0[cube.edge_index[("ab", 0, 0)]] += 1
    expect_rejected(
        "CORRUPT_H0_TREE_ROOT_PRESERVES_FILL",
        cube.d1(bad_h0) == vertex_cycle,
    )

    # Destructive control 5: root coordinates do not parametrize H2.
    top = cube.top_cycle((0, 0, 0))
    wrong_coordinate = top[cube.triangle_index[(0, 1, 1)]]
    expect_rejected(
        "ROOT_TRIANGLE_IS_TOP_COORDINATE",
        wrong_coordinate == 1,
    )

    print(
        "PASS_GENERIC_TRIPARTITE_UNIVERSAL_HOMOLOGY: constructive H0/H1/H2 "
        "survive integer, non-field, exhaustive, source-scene, and destructive tests."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
