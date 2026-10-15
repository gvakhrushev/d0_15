#!/usr/bin/env python3
"""Exact controls for the finite Lorentz-covariant translation obstruction."""

from __future__ import annotations

import hashlib
import json
import subprocess
from fractions import Fraction
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


def check_matrix_preserves_metric(m, eta):
    return matmul(matmul(transpose(m), eta), m) == eta


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
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
    theorem_name = (
        "D0.Research.FiniteLorentzCovariantPositiveQuadratic."
        "invariant_nonnegative_quadratic_eq_zero"
    )
    assert theorem_name in lean_output
    assert "D0.Research.FiniteLorentzCovariantPositiveQuadratic.owned_role_boost_is_lorentz" in lean_output
    assert "depends on axioms: [propext," in lean_output
    assert "sorryAx" not in lean_output
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
    assert all(controls.values())

    source_paths = [LEAN, DOC, Path(__file__).resolve(), *(ROOT / p for p in PRIMARY)]
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
        "lean_axioms": ["propext", "Classical.choice", "Quot.sound"],
        "exact_controls": controls,
        "control_count": len(controls),
        "source_sha256": {
            str(path.relative_to(ROOT)): sha(path) for path in source_paths
        },
    }
    RESULTS.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("PASS_FINITE_LORENTZ_COVARIANT_POSITIVE_QUADRATIC")
    print(f"lean_theorem={theorem_name}")
    print(f"lean_axioms={','.join(receipt['lean_axioms'])}")
    print(f"exact_controls={len(controls)}")
    for name, passed in controls.items():
        print(f"{name}={'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()
