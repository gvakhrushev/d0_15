#!/usr/bin/env python3
"""Finite certificate for D0-SCENE-2OF3-INVARIANT-RECONSTRUCTION-001.

The certificate independently enumerates ordered positive complete-tripartite
partitions and checks that every pair among the frozen raw invariants

    V = a+b+c = 33,
    E = ab+ac+bc = 359,
    T = abc = 1287

has the unique solution `(a,b,c)=(9,11,13)`.  It also proves the reconstruction
is genuinely two-of-three: each single invariant has a named second object.

Honest scope: ordered positive complete tripartite partitions only.  The cert
does not derive that class from M1 and does not replace the carrier-forcing
owner.
"""

from __future__ import annotations

from math import isqrt


TARGET = (9, 11, 13)
V_TARGET = 33
E_TARGET = 359
T_TARGET = 1287


def invariants(triple: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = triple
    return a + b + c, a * b + a * c + b * c, a * b * c


def ordered_positive(triple: tuple[int, int, int]) -> bool:
    a, b, c = triple
    return 0 < a <= b <= c


def candidates_from_vertex_count(v: int) -> set[tuple[int, int, int]]:
    out: set[tuple[int, int, int]] = set()
    for a in range(1, v + 1):
        for b in range(a, v + 1):
            c = v - a - b
            if c < b:
                continue
            triple = (a, b, c)
            if ordered_positive(triple):
                out.add(triple)
    return out


def candidates_from_edge_count(e: int) -> set[tuple[int, int, int]]:
    out: set[tuple[int, int, int]] = set()
    # E = ab + (a+b)c, so c is determined once (a,b) is fixed.
    # b^2 <= bc <= E for ordered positive triples, hence b <= sqrt(E).
    for a in range(1, isqrt(e) + 1):
        for b in range(a, isqrt(e) + 1):
            numerator = e - a * b
            denominator = a + b
            if numerator <= 0 or numerator % denominator:
                continue
            c = numerator // denominator
            triple = (a, b, c)
            if ordered_positive(triple) and invariants(triple)[1] == e:
                out.add(triple)
    return out


def candidates_from_triangle_count(t: int) -> set[tuple[int, int, int]]:
    out: set[tuple[int, int, int]] = set()
    for a in range(1, isqrt(t) + 1):
        if t % a:
            continue
        rem = t // a
        for b in range(a, isqrt(rem) + 1):
            if rem % b:
                continue
            c = rem // b
            triple = (a, b, c)
            if ordered_positive(triple) and invariants(triple)[2] == t:
                out.add(triple)
    return out


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


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: ordered positive complete-tripartite "
        "partitions are the audited class; V/E/T are computed before the "
        "(9,11,13) reconstruction claim."
    )

    v_set = candidates_from_vertex_count(V_TARGET)
    e_set = candidates_from_edge_count(E_TARGET)
    t_set = candidates_from_triangle_count(T_TARGET)

    require(TARGET in v_set and TARGET in e_set and TARGET in t_set, "TARGET_REALIZED")
    print(
        "PASS_TARGET_REALIZED: (9,11,13) has "
        f"(V,E,T)={invariants(TARGET)}."
    )

    ve = v_set & e_set
    vt = v_set & t_set
    et = e_set & t_set

    require(ve == {TARGET}, f"VE_NOT_UNIQUE_{sorted(ve)}")
    require(vt == {TARGET}, f"VT_NOT_UNIQUE_{sorted(vt)}")
    require(et == {TARGET}, f"ET_NOT_UNIQUE_{sorted(et)}")

    print(f"PASS_VERTEX_EDGE_RECONSTRUCTION: V=33 and E=359 -> {sorted(ve)}")
    print(f"PASS_VERTEX_TRIANGLE_RECONSTRUCTION: V=33 and T=1287 -> {sorted(vt)}")
    print(f"PASS_EDGE_TRIANGLE_RECONSTRUCTION: E=359 and T=1287 -> {sorted(et)}")
    cubic = {
        triple
        for triple in e_set
        if 2 * invariants(triple)[2] == 2574
    }
    require(cubic == {TARGET}, f"CUBIC_COEFFICIENTS_NOT_UNIQUE_{sorted(cubic)}")
    print(
        "PASS_CUBIC_COEFFICIENT_RECONSTRUCTION: "
        "the rank-3 cubic coefficients (-E,-2T)=(-359,-2574) "
        "reconstruct (9,11,13) without supplying V=33."
    )

    # Minimality: every single invariant has a named second ordered positive object.
    v_control = (8, 11, 14)
    e_control = (7, 10, 17)
    t_control = (3, 3, 143)
    require(v_control in v_set and v_control != TARGET, "VERTEX_SINGLETON_FALSE")
    require(e_control in e_set and e_control != TARGET, "EDGE_SINGLETON_FALSE")
    require(t_control in t_set and t_control != TARGET, "TRIANGLE_SINGLETON_FALSE")
    print(
        "PASS_SINGLE_INVARIANT_INSUFFICIENT: "
        f"same V -> {v_control}, same E -> {e_control}, same T -> {t_control}."
    )

    # Reachable conclusion-failing mutations.
    expect_rejected(
        "DROP_ORDERING_CREATES_SIX_PERMUTATIONS",
        len(set(__import__("itertools").permutations(TARGET))) == 1,
    )
    expect_rejected(
        "MUTATE_EDGE_TARGET_358",
        (v_set & candidates_from_edge_count(358)) == {TARGET},
    )
    expect_rejected(
        "MUTATE_TRIANGLE_TARGET_1288",
        (v_set & candidates_from_triangle_count(1288)) == {TARGET},
    )

    # Third-invariant inheritance: after reconstruction, the unused count is fixed.
    require(invariants(next(iter(ve)))[2] == T_TARGET, "VE_DOES_NOT_FORCE_T")
    require(invariants(next(iter(vt)))[1] == E_TARGET, "VT_DOES_NOT_FORCE_E")
    require(invariants(next(iter(et)))[0] == V_TARGET, "ET_DOES_NOT_FORCE_V")
    print("PASS_UNUSED_INVARIANT_INHERITED: every unique pair fixes the third count.")

    print(
        "PASS_SCENE_2OF3_INVARIANT_RECONSTRUCTION: the raw scene passport is "
        "self-certifying at two-of-three strength; no single count suffices."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
