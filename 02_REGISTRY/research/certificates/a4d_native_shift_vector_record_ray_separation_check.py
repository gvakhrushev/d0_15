#!/usr/bin/env python3
"""Separate the owned affine-shift vectors from the positive record ray.

On a constant shift with identity linear part, the owned diagonal seed equals
-b for every supplied comparison endomorphism. For every nonzero b that vector
is not the positive unit ray b/|b|. The soldered CAR creator reads the solder
leg, not the shift. Predecessor torsion equals that creator only for the
special value b = e_r.

This does not exhaust the core, select a record law, or close GR.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROOF = "02_REGISTRY/research/A4D_NATIVE_SHIFT_VECTOR_RECORD_RAY_SEPARATION.md"
STEM = "a4d_native_shift_vector_record_ray_separation"

INPUTS = {
    "03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean":
        "9a342468ef9c04f28c68b59acb32263e141ed184f2bf49a085869632930c1549",
    "03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean":
        "2ccca18cf8ca66b9e1aa020301ce0d84d6fcd12563e913323482ce139928e5fe",
    "03_FORMALIZATION/D0/Geometry/A4DConditionalSourcedDiagonalTransport.lean":
        "651260a51bdc0246dd8edb1bf2db93efa442cbf6dbe001d30cb69c747b5c3ddb",
    "03_FORMALIZATION/D0/Geometry/A4DSourcedMismatchFactorPassport.lean":
        "4c12e04b45c386512100337122d6f41c8b30d74398196b2de55232e192a3b849",
    "03_FORMALIZATION/D0/Geometry/A4DActiveSpanExtensionIndependence.lean":
        "94cd3fd0cf0619f28d9523753d7ab4cd6471fdecebd6891f6e1ba08f4446fc1d",
    "03_FORMALIZATION/D0/Geometry/A4DReferenceLocalCandidateNoGo.lean":
        "e3b32ccaa208377e07ce78e25087688a8f74929fcffe7c8cef3e058d0e4cbfb2",
    "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_check.py":
        "d78de07609370a307f30d1daeec9d45dd81de1eb7558654105ef32dc51ba89dd",
    "02_REGISTRY/research/A4D_NATIVE_AFFINE_LINK_SHIFT_BLINDNESS.md":
        "01dcfe75fed1e3c74317f9e98ce523e63334c626e2f89f1df373d6157f5ede3f",
    "02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md":
        "991b42eac645bb7e5e4df55f9be439f8e873b9403b4ff2a6dc1061a49dfe3e2e",
}

EXPECTED_CLOSURE = {
    "barB",
    "deltaB",
    "diagonalSeed",
    "relativeDefect",
    "pathSource",
    "parallelResidual",
    "predecessorTorsion",
    "IncrementsInActiveSpan",
    "seedAsSuppliedDiagonal",
    "conditionalMismatchFromSeed",
}
SEEDS = {"barB", "deltaB", "predecessorTorsion"}
DECL = re.compile(
    r"\n(?=(?:@[A-Za-z0-9_. \(\)\n]+)*(?:private |protected |noncomputable )*"
    r"(?:theorem|def|abbrev) )"
)
HEAD = re.compile(
    r"(?:@[^\n]+\n)*(?:private |protected |noncomputable )*(theorem|def|abbrev)\s+(\S+)"
)


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def code_lines(part: str) -> str:
    return "\n".join(
        line for line in part.splitlines() if not line.strip().startswith("--")
    )


def definitions():
    root = ROOT / "03_FORMALIZATION/D0"
    for path in sorted(root.rglob("*.lean")):
        text = "\n" + path.read_text()
        for part in DECL.split(text)[1:]:
            match = HEAD.match(part.lstrip("\n"))
            if not match:
                continue
            kind, name = match.group(1), match.group(2)
            if kind not in ("def", "abbrev"):
                continue
            yield name, path, code_lines(part)


def calls(code: str, name: str) -> bool:
    return re.search(r"(?<![\w.])" + re.escape(name) + r"\b", code) is not None


def closure():
    defs = list(definitions())
    found = set(SEEDS)
    changed = True
    while changed:
        changed = False
        for name, _path, code in defs:
            if name in found:
                continue
            if any(calls(code, token) for token in found):
                found.add(name)
                changed = True
    return found


def extract_def(path: Path, name: str) -> str:
    text = "\n" + path.read_text()
    for part in DECL.split(text)[1:]:
        match = HEAD.match(part.lstrip("\n"))
        if match and match.group(2) == name and match.group(1) == "def":
            return code_lines(part)
    raise AssertionError(name)


Vec = tuple[Fraction, Fraction, Fraction, Fraction]
ZERO: Vec = (Fraction(0),) * 4


def add(u: Vec, v: Vec) -> Vec:
    return tuple(a + b for a, b in zip(u, v))  # type: ignore[return-value]


def sub(u: Vec, v: Vec) -> Vec:
    return tuple(a - b for a, b in zip(u, v))  # type: ignore[return-value]


def smul(c: Fraction, u: Vec) -> Vec:
    return tuple(c * a for a in u)  # type: ignore[return-value]


def dot(u: Vec, v: Vec) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def basis(i: int) -> Vec:
    return tuple(Fraction(1) if j == i else Fraction(0) for j in range(4))  # type: ignore[return-value]


def apply_J(rows: tuple[Vec, ...], v: Vec) -> Vec:
    return tuple(dot(row, v) for row in rows)  # type: ignore[return-value]


def diagonal_seed(shift_y: Vec, shift_pred: Vec, J: tuple[Vec, ...]) -> Vec:
    """Identity linear part: barB = shift at the predecessor, seed = -barB - J deltaB."""
    bar = shift_pred
    delta = sub(shift_y, bar)
    return sub(smul(Fraction(-1), bar), apply_J(J, delta))


def predecessor_torsion(shift: Vec, solder_y: Vec, solder_x: Vec) -> Vec:
    """Identity linear part of predecessorTorsion."""
    return sub(add(shift, solder_y), solder_x)


def parallel(u: Vec, v: Vec) -> bool:
    return all(
        u[i] * v[j] - u[j] * v[i] == 0
        for i in range(4)
        for j in range(i + 1, 4)
    )


def is_positive_unit_ray(seed: Vec, b: Vec) -> bool:
    """Whether seed is b/sqrt(b·b), with no square root.

    Three clauses, with no separate zero branch: squared length 1, parallel
    to b, and positive inner product with b. The zero shift fails the sign
    clause, because every inner product with it is 0.
    """
    return dot(seed, seed) == 1 and dot(seed, b) > 0 and parallel(seed, b)


def run():
    checks = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for path, digest in INPUTS.items():
        check(f"PIN:{path}", sha(path) == digest)

    found = closure()
    check("SHIFT_VECTOR_CLOSURE_IS_THE_TEN_NAMED_DEFINITIONS", found == EXPECTED_CLOSURE)

    formal = ROOT / "03_FORMALIZATION"
    for path in sorted(formal.rglob("*.lean")):
        text = path.read_text()
        if "archiveExteriorCreator" not in text:
            continue
        for name in sorted(EXPECTED_CLOSURE):
            check(
                f"CREATOR_FILE_DOES_NOT_MENTION:{path.name}:{name}",
                not calls(text, name),
            )

    creator = extract_def(
        ROOT / "03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean",
        "archiveSolderedCreateDirection",
    )
    check("SOLDERED_CREATOR_USES_SOLDER_LEG", "solderLegVector" in creator)
    check("SOLDERED_CREATOR_BODY_HAS_NO_AFFINE_SHIFT", ".shift" not in creator)
    cartan = (ROOT / "03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean").read_text()
    check("AFFINE_IDENTITY_SHIFT_IS_ZERO", "shift := 0" in cartan)
    link = (ROOT / "03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean").read_text()
    check(
        "SOLDER_LEG_OF_ZERO_COFRAME_IS_THE_BASIS",
        "solderLegVector N (0 : LocalCoframeField N) x r = archiveRoleBasis r" in link,
    )

    # A nonzero supplied J. It must not be able to change the constant-shift seed.
    swap = (
        basis(1),
        basis(0),
        basis(2),
        basis(3),
    )
    check("HOSTILE_J_IS_NOT_ZERO", apply_J(swap, basis(0)) == basis(1))
    samples = [basis(0), smul(Fraction(2), basis(0)), (Fraction(3), Fraction(4), Fraction(0), Fraction(0)),
               (Fraction(1), Fraction(1), Fraction(0), Fraction(0)),
               (Fraction(-1), Fraction(2), Fraction(-3), Fraction(5))]
    e0 = basis(0)
    two = smul(Fraction(2), e0)
    opposite = smul(Fraction(-1), e0)
    check(
        "POSITIVE_UNIT_RAY_PREDICATE_ACCEPTS_THE_UNIT_VECTOR",
        is_positive_unit_ray(e0, e0),
    )
    check(
        "POSITIVE_UNIT_RAY_PREDICATE_ACCEPTS_THE_NORMALIZED_DOUBLE",
        is_positive_unit_ray(e0, two),
    )
    check(
        "OPPOSITE_UNIT_IS_PARALLEL_AND_UNIT_BUT_NOT_POSITIVE",
        parallel(opposite, e0)
        and dot(opposite, opposite) == 1
        and not is_positive_unit_ray(opposite, e0),
    )
    check(
        "DOUBLE_SHIFT_IS_PARALLEL_AND_ACUTE_BUT_NOT_UNIT",
        parallel(two, two)
        and dot(two, two) == 4
        and dot(two, two) > 0
        and not is_positive_unit_ray(two, two),
    )
    check(
        "ZERO_SHIFT_IS_REJECTED_BY_THE_SIGN_TEST",
        parallel(e0, ZERO)
        and dot(e0, e0) == 1
        and dot(e0, ZERO) == 0
        and not is_positive_unit_ray(e0, ZERO),
    )
    check("ONE_SAMPLE_IS_ALREADY_UNIT", any(dot(b, b) == 1 for b in samples))
    for b in samples:
        seed = diagonal_seed(b, b, swap)
        check("CONSTANT_SHIFT_SEED_EQUALS_MINUS_B", seed == smul(Fraction(-1), b))
        check(
            "COMPUTED_SEED_IS_NOT_THE_POSITIVE_UNIT_RAY",
            not is_positive_unit_ray(seed, b),
        )
        torsion = predecessor_torsion(b, basis(0), basis(0))
        check("ZERO_COFRAME_TORSION_EQUALS_SHIFT", torsion == b)

    coincidence = predecessor_torsion(basis(0), basis(0), basis(0))
    check(
        "TORSION_COINCIDES_WITH_CREATOR_ONLY_AT_THE_BASIS_SHIFT",
        coincidence == basis(0),
    )
    separated = predecessor_torsion(smul(Fraction(2), basis(0)), basis(0), basis(0))
    check(
        "DOUBLE_SHIFT_TORSION_IS_NOT_THE_CREATOR",
        separated == smul(Fraction(2), basis(0)) and separated != basis(0),
    )
    other_edge = predecessor_torsion(basis(1), basis(0), basis(0))
    check("OFF_EDGE_SHIFT_TORSION_IS_NOT_THE_CREATOR", other_edge == basis(1) and other_edge != basis(0))

    nonconstant = diagonal_seed(basis(0), ZERO, swap)
    check(
        "NONCONSTANT_SHIFT_LETS_J_ACT",
        nonconstant == smul(Fraction(-1), basis(1))
        and nonconstant != smul(Fraction(-1), basis(0)),
    )

    prep = (
        ROOT / "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_check.py"
    ).read_text()
    returns_at = prep.index("returns = [chronology.record(I4, n)[0] for n in basis]")
    channel_at = prep.index("    def channel(X):")
    shift_at = prep.index("    b = [I4[:, r] for r in range(4)]")
    channel_slice = prep[returns_at:channel_at]
    check(
        "CHANNEL_IS_CLOSED_BEFORE_THE_SHIFT_CANDIDATE",
        returns_at < channel_at < shift_at
        and "b = [" not in channel_slice
        and "record(G" not in channel_slice,
    )
    check(
        "SHIFT_RECONSTRUCTION_IS_NOT_CALLED_A_SELECTED_IDENTIFICATION",
        "not a physical identification currently selected by the core." in prep,
    )
    check(
        "SUPPLIED_COMPARISON_IS_NOT_SELECTED",
        "does not construct or select it." in (
            ROOT / "03_FORMALIZATION/D0/Geometry/A4DConditionalSourcedDiagonalTransport.lean"
        ).read_text(),
    )
    blind = (ROOT / "02_REGISTRY/research/A4D_NATIVE_AFFINE_LINK_SHIFT_BLINDNESS.md").read_text()
    check(
        "DIRAC_BLINDNESS_NOTE_STILL_SEPARATES_THE_TRANSPORT",
        "their outputs do not respond when" in blind and r"hence \(b_e\), changes" in blind,
    )

    return {
        "schema": "d0-native-shift-vector-record-ray-separation/1",
        "status": "PASS_CONDITIONAL_CONSTANT_SHIFT_SEED_IS_OPPOSITE_RAY",
        "proof": PROOF,
        "input_sha256": {path: sha(path) for path in INPUTS},
        "exact_result": {
            "shift_vector_closure": sorted(EXPECTED_CLOSURE),
            "constant_shift_seed": "-b",
            "positive_ray": "b/sqrt(b·b)",
            "zero_coframe_creator": "e_r",
            "zero_coframe_torsion": "b",
            "torsion_creator_agreement": "b = e_r only",
        },
        "exact_controls": len(checks),
        "checks": checks,
        "scope": {
            "constant_shift_identity_linear_seed_equals_minus_b": True,
            "that_seed_is_the_positive_record_ray": False,
            "torsion_equals_soldered_creator_for_every_shift": False,
            "shift_closure_is_an_argument_of_archiveExteriorCreator": False,
            "comparison_endomorphism_selected_by_core": False,
            "whole_core_interface_exhausted": False,
            "same_edge_record_readout_selected": False,
            "ten_slot_total_source_compared": False,
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
