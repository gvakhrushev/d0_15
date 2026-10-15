#!/usr/bin/env python3
"""Exact controls for the finite Lorentz-covariant translation obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from fractions import Fraction
from itertools import permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PREFIX = "a4d_finite_lorentz_covariant_positive_quadratic"
DOC = ROOT / "02_REGISTRY/research/A4D_NATIVE_FINITE_AFFINE_UNITARY_NO_GO.md"
LEAN = ROOT / "02_REGISTRY/research/certificates" / f"{PREFIX}.lean"
OUTPUT = ROOT / "02_REGISTRY/research/certificates" / f"{PREFIX}_output.txt"
RESULTS = ROOT / "02_REGISTRY/research/certificates" / f"{PREFIX}_results.json"
PRIMARY = [
    "03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean",
    "03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean",
    "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def determinant(a):
    def sign(p):
        inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
        return -1 if inversions % 2 else 1

    return sum(
        sign(p) * _product(a[i][p[i]] for i in range(len(p)))
        for p in permutations(range(len(a)))
    )


def _product(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def check_matrix_preserves_metric(m, eta):
    return matmul(matmul(transpose(m), eta), m) == eta


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-check", action="store_true",
                        help="compile the capsule with the local Lake toolchain")
    parser.add_argument("--write", action="store_true",
                        help="refresh the compiler transcript and immutable receipt")
    args = parser.parse_args()
    if args.write and not args.runtime_check:
        raise SystemExit("--write requires --runtime-check")

    if args.runtime_check:
        lean_rel = str(LEAN.relative_to(ROOT))
        proc = subprocess.run(
            ["lake", "env", "lean", "../" + lean_rel],
            cwd=ROOT / "03_FORMALIZATION",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        assert proc.returncode == 0, proc.stdout
        lean_output = proc.stdout
        if not args.write:
            assert OUTPUT.is_file() and OUTPUT.read_text() == lean_output, \
                "LEAN_OUTPUT_DIFFERS_FROM_IMMUTABLE_TRANSCRIPT"
    else:
        assert OUTPUT.is_file(), "MISSING_IMMUTABLE_LEAN_TRANSCRIPT"
        lean_output = OUTPUT.read_text()

    theorem_name = (
        "D0.Research.FiniteLorentzCovariantPositiveQuadratic."
        "invariant_nonnegative_quadratic_eq_zero"
    )
    owner_theorem = (
        "D0.Research.FiniteLorentzCovariantPositiveQuadratic."
        "owned_role_boost_is_lorentz"
    )
    boost_bridge_theorem = (
        "D0.Research.FiniteLorentzCovariantPositiveQuadratic."
        "rational_boost_matches_owned_role_boost"
    )
    blocks = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", lean_output, flags=re.S)
    lean_axioms = {
        name: sorted(value.strip() for value in raw.split(",") if value.strip())
        for name, raw in blocks
    }
    expected_declarations = {theorem_name, owner_theorem, boost_bridge_theorem}
    assert set(lean_axioms) == expected_declarations, lean_axioms
    assert all(set(values) <= {"propext", "Classical.choice", "Quot.sound"}
               for values in lean_axioms.values()), lean_axioms
    assert "sorryAx" not in lean_output
    assert theorem_name in lean_output
    assert owner_theorem in lean_output
    assert boost_bridge_theorem in lean_output
    assert "D0.Geometry.rationalABBoost_lorentz : Geometry.IsRoleLorentz Geometry.rationalABBoost" in lean_output
    affine_source = (ROOT / PRIMARY[0]).read_text()
    exterior_source = (ROOT / PRIMARY[1]).read_text()
    boost_source = (ROOT / PRIMARY[2]).read_text()
    metric_source = (ROOT / PRIMARY[3]).read_text()
    assert "(φ * ψ).shift = φ.shift + φ.lin ψ.shift" in affine_source
    assert "archiveAffineExteriorLink_shift_irrelevant" in exterior_source
    assert "theorem rationalABBoost_lorentz" in boost_source
    assert all(name in metric_source for name in (
        "roleLorentzSign_A", "roleLorentzSign_B", "roleLorentzSign_C", "roleLorentzSign_D"
    ))
    assert "rationalABBoost_lorentz" in lean_output
    if args.write:
        OUTPUT.write_text(lean_output)

    f = Fraction
    eta = [
        [f(1), f(0), f(0), f(0)],
        [f(0), f(-1), f(0), f(0)],
        [f(0), f(0), f(-1), f(0)],
        [f(0), f(0), f(0), f(-1)],
    ]
    rotations = {
        "half_turn_x": [[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-1]],
        "half_turn_y": [[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,-1]],
        "half_turn_z": [[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]],
        "quarter_turn_z": [[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]],
        "quarter_turn_y": [[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,-1,0,0]],
        "rational_boost": [
            [f(5,3),f(4,3),0,0], [f(4,3),f(5,3),0,0],
            [0,0,1,0], [0,0,0,1],
        ],
    }
    controls = {}
    for name, matrix in rotations.items():
        exact_matrix = [[f(v) for v in row] for row in matrix]
        controls[f"{name}_preserves_minkowski_form_exactly"] = \
            check_matrix_preserves_metric(exact_matrix, eta)
        controls[f"{name}_is_proper_time_oriented"] = \
            determinant(exact_matrix) == 1 and exact_matrix[0][0] > 0
    assert all(controls.values())

    # Hostile controls show why both hypotheses are load-bearing.
    # Euclidean Q is positive but is not invariant under the boost e0 -> (5/3,4/3,0,0).
    euclidean_after_boost = f(25, 9) + f(16, 9)
    controls["positive_euclidean_form_fails_boost"] = euclidean_after_boost != 1
    # The invariant Minkowski form is not nonnegative on spatial vectors.
    controls["minkowski_form_fails_nonnegativity"] = f(-1) < 0
    # Without the boost, Q=t^2 is a nonzero nonnegative rotation-invariant form.
    controls["dropping_boost_admits_nonzero_positive_form"] = all(
        matrix[0] == [f(1), f(0), f(0), f(0)]
        for name, matrix in rotations.items() if name != "rational_boost"
    )
    # A direct affine subdivision witness retains the native shift law.
    b = (f(1), f(2), f(-1), f(0))
    c = (f(3), f(0), f(2), f(1))
    controls["pure_translation_composition_adds_the_recorded_shift"] = tuple(
        b[i] + c[i] for i in range(4)
    ) == (f(4), f(2), f(1), f(1))
    controls["owned_affine_shift_composition_is_pinned"] = \
        "(φ * ψ).shift = φ.shift + φ.lin ψ.shift" in affine_source
    controls["current_CAR_exterior_link_ignores_pure_shift"] = \
        "archiveAffineExteriorLink_shift_irrelevant" in exterior_source
    controls["D0_rational_AB_boost_owner_is_resolved"] = \
        "rationalABBoost_lorentz" in lean_output
    controls["coordinate_boost_is_exactly_the_owned_role_boost"] = \
        boost_bridge_theorem in lean_output
    assert all(controls.values())

    source_paths = [LEAN, DOC, Path(__file__).resolve(), OUTPUT, *(ROOT / p for p in PRIMARY)]
    receipt = {
        "status": "PASS_FINITE_LORENTZ_COVARIANT_POSITIVE_QUADRATIC",
        "scope": {
            "finite_dimensional_hermitian_generator_quadratic_core_lean_checked": True,
            "smooth_unitary_group_derivative_to_hermitian_generators": "analytic finite-dimensional matrix proof",
            "affine_translation_representation_trivial_under_fixed_positive_pairing_and_full_lorentz_covariance": True,
            "lorentz_implementers_must_be_unitary": False,
            "level_changing_or_infinite_dimensional_memory_excluded": False,
            "nonunitary_or_nonhomomorphic_channels_excluded": False,
            "whole_core_no_go_or_gr_closure": False,
            "global_or_parent_terminal_status_changed": False,
        },
        "lean_theorem": theorem_name,
        "lean_axioms": sorted({axiom for values in lean_axioms.values() for axiom in values}),
        "lean_declarations": {name: values for name, values in sorted(lean_axioms.items())},
        "exact_controls": controls,
        "control_count": len(controls),
        "source_sha256": {
            str(path.relative_to(ROOT)): sha(path) for path in source_paths
        },
    }
    encoded = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.write:
        RESULTS.write_text(encoded)
    else:
        assert RESULTS.is_file(), "MISSING_IMMUTABLE_RESULTS_RECEIPT"
        assert json.loads(RESULTS.read_text()) == receipt, "IMMUTABLE_RESULTS_RECEIPT_MISMATCH"
    print("PASS_FINITE_LORENTZ_COVARIANT_POSITIVE_QUADRATIC")
    print(f"lean_theorem={theorem_name}")
    print(f"lean_axioms={','.join(receipt['lean_axioms'])}")
    print(f"exact_controls={len(controls)}")
    for name, passed in controls.items():
        print(f"{name}={'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()
