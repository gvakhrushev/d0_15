#!/usr/bin/env python3
"""Evaluate covariantShift and affineOpenTorsion on one common translation.

Identity linear part and one translation b give a forward step b, a backward
step -b, a two-step sum 2b, and open torsion 0. The forward value meets the
positive unit ray only when b is already that ray. Open torsion stays 0 even
at that coincidence. A swap link makes based torsion differ from open torsion.

The path algebra and the based/open distinction are already owned. This does
not select a record ray or close GR.
"""

# D0_CI_TIMEOUT_SECONDS=600

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROOF = "02_REGISTRY/research/A4D_NATIVE_COVARIANT_SHIFT_OPEN_TORSION_RAY.md"
STEM = "a4d_native_covariant_shift_open_torsion_ray"

INPUTS = {
    "03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean":
        "9a342468ef9c04f28c68b59acb32263e141ed184f2bf49a085869632930c1549",
    "02_REGISTRY/research/A4D_227_TORSION_DIAGNOSTIC.md":
        "8f5d30d7e551f140c0458e5a8fd6d82ba28868e29a39d67bb4710cad90f8a7fe",
    "02_REGISTRY/research/certificates/a4d_native_shift_vector_record_ray_separation_check.py":
        "d14d7dc1d7cb63e978f146961f9b4092c3818f6fb95bc43825d5412eac5bf3ef",
}


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


Vec = tuple[Fraction, Fraction, Fraction, Fraction]
Lin = tuple[Vec, Vec, Vec, Vec]
Edge = tuple[Lin, Vec]
ZERO: Vec = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))


def basis(i: int) -> Vec:
    return tuple(Fraction(1) if j == i else Fraction(0) for j in range(4))  # type: ignore[return-value]


def add(u: Vec, v: Vec) -> Vec:
    return tuple(a + b for a, b in zip(u, v))  # type: ignore[return-value]


def sub(u: Vec, v: Vec) -> Vec:
    return tuple(a - b for a, b in zip(u, v))  # type: ignore[return-value]


def smul(c: Fraction, u: Vec) -> Vec:
    return tuple(c * a for a in u)  # type: ignore[return-value]


def dot(u: Vec, v: Vec) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def apply(lin: Lin, v: Vec) -> Vec:
    return tuple(dot(row, v) for row in lin)  # type: ignore[return-value]


def eye() -> Lin:
    return (basis(0), basis(1), basis(2), basis(3))


def swap01() -> Lin:
    return (basis(1), basis(0), basis(2), basis(3))


def mat_inv(lin: Lin) -> Lin:
    """Inverse by exact elimination. No integer division."""
    n = 4
    aug = [
        [lin[r][c] for c in range(n)]
        + [Fraction(1) if c == r else Fraction(0) for c in range(n)]
        for r in range(n)
    ]
    for col in range(n):
        pivot = next(r for r in range(col, n) if aug[r][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col] ** -1
        aug[col] = [entry * scale for entry in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [aug[row][c] - factor * aug[col][c] for c in range(2 * n)]
    return tuple(tuple(aug[r][n + c] for c in range(n)) for r in range(n))  # type: ignore[return-value]


def mul(left: Edge, right: Edge) -> Edge:
    """(U, a)(V, b) = (UV, a + U b), right factor first."""
    images = [apply(left[0], apply(right[0], basis(j))) for j in range(4)]
    lin = tuple(tuple(images[j][i] for j in range(4)) for i in range(4))
    shift = add(left[1], apply(left[0], right[1]))
    return (lin, shift)  # type: ignore[return-value]


def inv_edge(edge: Edge) -> Edge:
    """(U, a)^{-1} = (U^{-1}, -U^{-1} a)."""
    lin = mat_inv(edge[0])
    return (lin, smul(Fraction(-1), apply(lin, edge[1])))


def covariant_shift(steps: list[Edge]) -> Vec:
    """Head translation plus its linear part on the remaining sum."""
    if not steps:
        return ZERO
    head, *tail = steps
    return add(head[1], apply(head[0], covariant_shift(tail)))


def squares(edge_r: Edge, edge_s_after_r: Edge, edge_s: Edge, edge_r_after_s: Edge):
    square_a = mul(edge_r, edge_s_after_r)
    square_b = mul(edge_s, edge_r_after_s)
    return square_a, square_b


def open_torsion(edge_r: Edge, edge_s_after_r: Edge, edge_s: Edge, edge_r_after_s: Edge) -> Vec:
    return sub(add(edge_r[1], apply(edge_r[0], edge_s_after_r[1])),
               add(edge_s[1], apply(edge_s[0], edge_r_after_s[1])))


def based_shift(edge_r: Edge, edge_s_after_r: Edge, edge_s: Edge, edge_r_after_s: Edge) -> Vec:
    square_a, square_b = squares(edge_r, edge_s_after_r, edge_s, edge_r_after_s)
    return mul(square_a, inv_edge(square_b))[1]


def parallel(u: Vec, v: Vec) -> bool:
    return all(
        u[i] * v[j] - u[j] * v[i] == 0
        for i in range(4)
        for j in range(i + 1, 4)
    )


def is_positive_unit_ray(seed: Vec, b: Vec) -> bool:
    """Unit, parallel to b, and acute. No square root and no zero branch."""
    return dot(seed, seed) == 1 and dot(seed, b) > 0 and parallel(seed, b)


def edge(lin: Lin, shift: Vec) -> Edge:
    return (lin, shift)


def run():
    checks: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    receipt_path = (
        "02_REGISTRY/research/certificates/"
        "a4d_native_shift_vector_record_ray_separation_results.json"
    )
    pinned = dict(INPUTS)
    pinned[receipt_path] = sha(receipt_path)
    for path, digest in pinned.items():
        check(f"PIN:{path}", sha(path) == digest)

    cartan = (ROOT / "03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean").read_text()
    check("MUL_SHIFT_IS_THE_OWNED_SUM",
          "(φ * ψ).shift = φ.shift + φ.lin ψ.shift" in cartan)
    check("INV_SHIFT_IS_THE_OWNED_OPPOSITE",
          "(φ⁻¹).shift = -φ.lin.symm φ.shift" in cartan)
    check("COVARIANT_SHIFT_IS_DEFINED", "def covariantShift" in cartan)
    check("OPEN_TORSION_EXPAND_IS_OWNED", "theorem affineOpenTorsion_expand" in cartan)
    check("BASED_HOLONOMY_IS_SQUARE_TIMES_INVERSE",
          "affineSquareA A r s x * (affineSquareB A r s x)⁻¹" in cartan)
    check("BASED_AND_OPEN_STAY_DISTINCT_IN_THE_HEADER",
          "so it agrees\nwith open torsion only when `P` fixes `b`." in cartan)
    def span(start: str, end: str) -> str:
        begin = cartan.index(start)
        return cartan[begin:cartan.index(end, begin + len(start))]

    covariant_body = span("def covariantShift", "def covariantLin")
    torsion_body = span("def affineOpenTorsion", "theorem affineOpenTorsion_expand")
    check("COVARIANT_SHIFT_BODY_READS_THE_STEP_SHIFT", ".shift" in covariant_body)
    check("COVARIANT_SHIFT_BODY_DOES_NOT_CALL_THE_EXTERIOR_CREATOR",
          "archiveExteriorCreator" not in covariant_body)
    check("OPEN_TORSION_BODY_READS_SQUARE_SHIFTS", ".shift" in torsion_body)
    check("OPEN_TORSION_BODY_DOES_NOT_CALL_THE_EXTERIOR_CREATOR",
          "archiveExteriorCreator" not in torsion_body)

    prior = json.loads((ROOT / receipt_path).read_text())
    closure = set(prior["exact_result"]["shift_vector_closure"])
    check("COVARIANT_SHIFT_IS_OUTSIDE_THE_TEN_NAME_CLOSURE",
          "covariantShift" not in closure and len(closure) == 10)
    check("OPEN_TORSION_IS_OUTSIDE_THE_TEN_NAME_CLOSURE",
          "affineOpenTorsion" not in closure)

    claims = (ROOT / "02_REGISTRY/claims.csv").read_text()
    row_at = claims.index("D0-AFFINE-CARTAN-PATH-CLOSURE-001")
    row = claims[row_at:claims.index("\n", row_at)]
    check("PATH_ALGEBRA_ROW_OWNS_THE_COVARIANT_SUM",
          "affinePath_shift_eq_covariant_sum" in row)
    check("PATH_ALGEBRA_ROW_OWNS_THE_TORSION_GAUGE",
          "affineOpenTorsion_gauge" in row)
    check("PATH_ALGEBRA_ROW_SELECTS_NO_ACTION",
          "No physical Hodge kernel or constitutive action is selected." in row)

    diagnostic = (ROOT / "02_REGISTRY/research/A4D_227_TORSION_DIAGNOSTIC.md").read_text()
    check("LORENTZ_DIAGNOSTIC_IS_NOT_THIS_TRANSLATION",
          "It is not the affine open torsion of `affineOpenTorsion`" in diagnostic
          and "that translation defect is the zero vector" in diagnostic)

    check("INVERSE_OF_IDENTITY_IS_IDENTITY", mat_inv(eye()) == eye())
    check("INVERSE_OF_SWAP_IS_SWAP", mat_inv(swap01()) == swap01())
    check("SWAP_SQUARE_IS_IDENTITY",
          mul(edge(swap01(), ZERO), edge(swap01(), ZERO))[0] == eye())

    e0 = basis(0)
    e1 = basis(1)
    two = smul(Fraction(2), e0)
    opposite = smul(Fraction(-1), e0)
    identity = eye()
    samples = [
        e0,
        two,
        opposite,
        (Fraction(3), Fraction(4), Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(-1), Fraction(2), Fraction(-3), Fraction(5)),
    ]
    check("EMPTY_PATH_SUM_IS_ZERO", covariant_shift([]) == ZERO)
    check("ONE_SAMPLE_IS_ALREADY_THE_POSITIVE_RAY", is_positive_unit_ray(e0, e0))
    for b in samples:
        forward = covariant_shift([edge(identity, b)])
        backward = covariant_shift([inv_edge(edge(identity, b))])
        double = covariant_shift([edge(identity, b), edge(identity, b)])
        edges = (edge(identity, b),) * 4
        face = open_torsion(*edges)
        square_a, square_b = squares(*edges)
        based = based_shift(*edges)
        check("FORWARD_STEP_EQUALS_THE_TRANSLATION", forward == b)
        check("BACKWARD_STEP_EQUALS_THE_OPPOSITE_TRANSLATION",
              backward == smul(Fraction(-1), b) and backward != b)
        check("TWO_FORWARD_STEPS_EQUAL_TWICE_THE_TRANSLATION",
              double == smul(Fraction(2), b))
        check("OPEN_TORSION_OF_A_CONSTANT_TRANSLATION_IS_ZERO", face == ZERO)
        check("EXPAND_AGREES_WITH_THE_SQUARE_DIFFERENCE",
              face == sub(square_a[1], square_b[1]))
        check("IDENTITY_HOLONOMY_KEEPS_BASED_TORSION_EQUAL_TO_OPEN",
              based == face == ZERO)

    check("UNIT_FORWARD_STEP_MEETS_THE_POSITIVE_RAY",
          covariant_shift([edge(identity, e0)]) == e0
          and is_positive_unit_ray(covariant_shift([edge(identity, e0)]), e0))
    check("DOUBLE_FORWARD_STEP_IS_NOT_THE_POSITIVE_RAY",
          covariant_shift([edge(identity, two)]) == two
          and is_positive_unit_ray(e0, two)
          and not is_positive_unit_ray(covariant_shift([edge(identity, two)]), two))
    check("OPPOSITE_UNIT_TRANSLATION_IS_ITS_OWN_RAY_AND_NOT_THE_RAY_OF_E0",
          covariant_shift([edge(identity, opposite)]) == opposite
          and is_positive_unit_ray(opposite, opposite)
          and parallel(opposite, e0)
          and dot(opposite, opposite) == 1
          and not is_positive_unit_ray(opposite, e0))
    check("BACKWARD_UNIT_STEP_IS_NOT_THE_POSITIVE_RAY",
          covariant_shift([inv_edge(edge(identity, e0))]) == opposite
          and not is_positive_unit_ray(
              covariant_shift([inv_edge(edge(identity, e0))]), e0))
    check("OPEN_TORSION_STAYS_ZERO_WHERE_THE_FORWARD_STEP_MEETS_THE_RAY",
          open_torsion(*((edge(identity, e0),) * 4)) == ZERO
          and not is_positive_unit_ray(ZERO, e0))

    # Predecessor shift 0 is not used. Site-dependent translations, identity lin.
    nonconstant = open_torsion(
        edge(identity, e0),
        edge(identity, e1),
        edge(identity, ZERO),
        edge(identity, e0),
    )
    check("NONCONSTANT_OPEN_TORSION_IS_E1",
          nonconstant == e1 and nonconstant != ZERO)

    swapped = covariant_shift([edge(swap01(), e0), edge(identity, e0)])
    check("SWAP_ON_THE_FIRST_STEP_CHANGES_THE_TWO_STEP_SUM",
          swapped == add(e0, e1) and swapped != two)

    hostile_edges = (
        edge(swap01(), e0),
        edge(identity, e0),
        edge(identity, e0),
        edge(identity, e0),
    )
    hostile_open = open_torsion(*hostile_edges)
    hostile_based = based_shift(*hostile_edges)
    square_a, square_b = squares(*hostile_edges)
    holonomy_lin = mul(square_a, inv_edge(square_b))[0]
    transported = sub(square_b[1], apply(holonomy_lin, square_b[1]))
    check("HOSTILE_BASED_TORSION_DIFFERS_FROM_OPEN_TORSION",
          hostile_open == sub(e1, e0)
          and hostile_based == sub(e0, e1)
          and hostile_based != hostile_open)
    check("HOSTILE_PAIR_STILL_OBEYS_THE_OWNED_TORSION_RELATION",
          hostile_based == add(hostile_open, transported))

    check("OPPOSITE_UNIT_IS_REJECTED_BY_THE_SIGN",
          parallel(opposite, e0)
          and dot(opposite, opposite) == 1
          and not is_positive_unit_ray(opposite, e0))
    check("DOUBLE_VECTOR_IS_REJECTED_BY_THE_LENGTH",
          parallel(two, two)
          and dot(two, two) == 4
          and dot(two, two) > 0
          and not is_positive_unit_ray(two, two))
    check("ZERO_SHIFT_IS_REJECTED_BY_THE_SIGN_TEST",
          parallel(e0, ZERO)
          and dot(e0, e0) == 1
          and dot(e0, ZERO) == 0
          and not is_positive_unit_ray(e0, ZERO))

    return {
        "schema": "d0-native-covariant-shift-open-torsion-ray/1",
        "status": "PASS_CONDITIONAL_CONSTANT_SHIFT_PATH_SUM_AND_ZERO_OPEN_TORSION",
        "proof": PROOF,
        "input_sha256": {path: sha(path) for path in pinned},
        "exact_result": {
            "identity_linear_forward_step": "b",
            "identity_linear_backward_step": "-b",
            "identity_linear_two_forward_steps": "2b",
            "identity_linear_open_torsion": "0",
            "unit_forward_meets_positive_ray": True,
            "double_forward_meets_positive_ray": False,
            "open_torsion_at_unit_shift": "0",
        },
        "exact_controls": len(checks),
        "checks": checks,
        "scope": {
            "constant_identity_linear_forward_equals_b": True,
            "that_forward_value_is_the_normalization_map": False,
            "open_torsion_vanishes_for_every_connection": False,
            "based_torsion_equals_open_torsion_for_every_connection": False,
            "path_algebra_reproved": False,
            "same_edge_record_readout_selected": False,
            "ten_slot_total_source_compared": False,
            "whole_core_interface_exhausted": False,
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
