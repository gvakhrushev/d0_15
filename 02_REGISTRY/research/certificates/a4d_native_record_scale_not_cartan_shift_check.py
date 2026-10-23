#!/usr/bin/env python3
"""The owned chronology record reads the supplied observer, including its scale.

At the identity Gram, record(I, 2 e_0) is not record(I, e_0). The positive
unit ray of 2 e_0 is e_0, so the record output at that vector is not the
record output at its ray. The price cut is even in the observer. Neither
the record nor the preparation binding reads a Cartan shift.

This does not select a record ray, exhaust the core, or close GR.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from fractions import Fraction
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
PROOF = "02_REGISTRY/research/A4D_NATIVE_RECORD_SCALE_NOT_CARTAN_SHIFT.md"
STEM = "a4d_native_record_scale_not_cartan_shift"
CHRONOLOGY = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py"
FOCK = "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py"
PREP = "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_check.py"
NILPOTENT = "03_FORMALIZATION/D0/Geometry/A4DNilpotentAffineMatterLift.lean"
EXTERIOR = "03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean"
QUOTIENT = "02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md"

INPUTS = {
    CHRONOLOGY: "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    FOCK: "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    PREP: "d78de07609370a307f30d1daeec9d45dd81de1eb7558654105ef32dc51ba89dd",
    NILPOTENT: "643182331ff9ecddb031ea44d829ea3d0900d8e551166bab68706683ad245563",
    EXTERIOR: "2ccca18cf8ca66b9e1aa020301ce0d84d6fcd12563e913323482ce139928e5fe",
    QUOTIENT: "991b42eac645bb7e5e4df55f9be439f8e873b9403b4ff2a6dc1061a49dfe3e2e",
}

EXPECTED_SHIFT_DEFS = {
    "ResponseDecomposition.shift",
    "barB",
    "deltaB",
    "predecessorTorsion",
    "apply",
    "mul",
    "inv",
    "covariantShift",
    "affineOpenTorsion",
}
DECL = re.compile(
    r"\n(?=(?:@[A-Za-z0-9_. \(\)\n]+)*(?:private |protected |noncomputable )*"
    r"(?:theorem|def|abbrev) )"
)
HEAD = re.compile(
    r"(?:@[^\n]+\n)*(?:private |protected |noncomputable )*(theorem|def|abbrev)\s+(\S+)"
)

Vec = tuple[Fraction, Fraction, Fraction, Fraction]
ZERO: Vec = (Fraction(0),) * 4


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


def extract_def(path: Path, name: str) -> str:
    text = "\n" + path.read_text()
    for part in DECL.split(text)[1:]:
        match = HEAD.match(part.lstrip("\n"))
        if match and match.group(2) == name and match.group(1) == "def":
            return code_lines(part)
    raise AssertionError(name)


def dot(u: Vec, v: Vec) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def parallel(u: Vec, v: Vec) -> bool:
    return all(
        u[i] * v[j] - u[j] * v[i] == 0
        for i in range(4)
        for j in range(i + 1, 4)
    )


def is_positive_unit_ray(seed: Vec, b: Vec) -> bool:
    """Unit, parallel to b, and acute. No square root and no zero branch."""
    return dot(seed, seed) == 1 and dot(seed, b) > 0 and parallel(seed, b)


def rational_sqrt(q: Fraction) -> Fraction:
    if q <= 0:
        raise ValueError(q)
    def isqrt(n: int) -> int:
        r = 0
        bit = 1 << ((n.bit_length() + 1) // 2)
        while bit:
            trial = r + bit
            if trial * trial <= n:
                r = trial
            bit >>= 1
        if r * r != n:
            raise ValueError(n)
        return r
    return Fraction(isqrt(q.numerator), isqrt(q.denominator))


def normalize(b: Vec) -> Vec:
    root = rational_sqrt(dot(b, b))
    return tuple(component / root for component in b)  # type: ignore[return-value]


def column(b: Vec):
    return s.Matrix(4, 1, [s.Integer(component.numerator) / component.denominator for component in b])


def load_chronology():
    spec = importlib.util.spec_from_file_location("chronology_record_owner", ROOT / CHRONOLOGY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    checks = []

    def check(name, condition):
        assert bool(condition), name
        checks.append(name)

    for path, expected in INPUTS.items():
        check("PINNED_INPUT_UNCHANGED_" + Path(path).name, sha(path) == expected)

    chronology = load_chronology()
    a, p = chronology.a, chronology.p
    check(
        "GOLDEN_RELATION_REDUCES",
        chronology.red(a**2 - p) == 0
        and chronology.red(p**2 + p - 1) == 0
        and chronology.red(p) != 0,
    )
    check("RECORD_USES_THE_FOCK_CREATOR", chronology.creator is chronology.old.creator)

    symbols = s.symbols("v0:4")
    generic = s.Matrix(4, 1, symbols)
    other = s.Matrix(4, 1, s.symbols("w0:4"))
    scale = s.symbols("c")
    creator = chronology.creator
    check(
        "CREATOR_IS_LINEAR_ON_A_GENERIC_OBSERVER",
        creator(generic + other) == creator(generic) + creator(other)
        and creator(scale * generic) == scale * creator(generic)
        and creator(-generic) == -creator(generic),
    )
    gram = s.eye(4)
    frame = chronology.ext(gram)
    frame_inv = chronology.ext(gram.inv())
    number = creator(generic) * (frame_inv * creator(generic).T * frame)
    opposite_number = creator(-generic) * (frame_inv * creator(-generic).T * frame)
    check(
        "PRICE_CUT_FORMULA_IS_EVEN_IN_EVERY_OBSERVER_AT_THE_IDENTITY_GRAM",
        number == opposite_number
        and "N = cr * an" in (ROOT / CHRONOLOGY).read_text()
        and "an = Si * cr.T * S" in (ROOT / CHRONOLOGY).read_text()
        and "P = I - N" in (ROOT / CHRONOLOGY).read_text(),
    )

    def record_at(vector, metric=None):
        return chronology.record(s.eye(4) if metric is None else metric, column(vector))

    e0: Vec = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    e1: Vec = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    two: Vec = (Fraction(2), Fraction(0), Fraction(0), Fraction(0))
    opposite: Vec = (Fraction(-1), Fraction(0), Fraction(0), Fraction(0))
    opposite_e1: Vec = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0))
    raw34: Vec = (Fraction(3), Fraction(4), Fraction(0), Fraction(0))
    ray34 = normalize(raw34)
    unit_u, unit_p = record_at(e0)
    double_u, double_p = record_at(two)
    sign_u, sign_p = record_at(opposite)
    axis_u, axis_p = record_at(e1)
    axis_sign_u, axis_sign_p = record_at(opposite_e1)
    raw_u, _raw_p = record_at(raw34)
    ray_u, _ray_p = record_at(ray34)
    zero_u, _zero_p = record_at(ZERO)
    probed = s.diag(2, 1, 1, 1)
    probed_u, _probed_p = chronology.record(probed, column(e0))

    def entry(matrix, i, j):
        return chronology.red(matrix[i, j])

    double_gap = double_u - unit_u
    sign_gap = sign_u - unit_u
    gram_gap = probed_u - unit_u
    ray_gap = raw_u - ray_u
    zero_gap = zero_u - unit_u
    check(
        "DOUBLE_RECORD_DIFFERS_FROM_THE_UNIT_RECORD",
        not chronology.zero(double_gap)
        and entry(double_gap, 0, 1) == -p
        and entry(double_gap, 1, 0) == -103 * p
        and double_p != unit_p,
    )
    check(
        "RAY_OF_THE_DOUBLE_IS_THE_UNIT_AND_THE_DOUBLE_IS_NOT",
        normalize(two) == e0
        and is_positive_unit_ray(e0, two)
        and not is_positive_unit_ray(two, two)
        and is_positive_unit_ray(e0, e0),
    )
    check(
        "SIGN_FLIPS_THE_RECORD_AND_NOT_THE_PRICE_CUT",
        not chronology.zero(sign_gap)
        and entry(sign_gap, 0, 1) == 2 * p
        and entry(sign_gap, 1, 0) == -2 * p
        and sign_p == unit_p,
    )
    check(
        "SECOND_AXIS_SIGN_FLIPS_THE_RECORD_AND_NOT_THE_PRICE_CUT",
        not chronology.zero(axis_sign_u - axis_u) and axis_sign_p == axis_p,
    )
    check(
        "OPPOSITE_UNIT_IS_ITS_OWN_RAY_AND_NOT_THE_RAY_OF_E0",
        normalize(opposite) == opposite
        and is_positive_unit_ray(opposite, opposite)
        and not is_positive_unit_ray(opposite, e0),
    )
    check(
        "RAW_34_RECORD_DIFFERS_FROM_THE_RECORD_AT_ITS_RAY",
        ray34 == (Fraction(3, 5), Fraction(4, 5), Fraction(0), Fraction(0))
        and is_positive_unit_ray(ray34, raw34)
        and not is_positive_unit_ray(raw34, raw34)
        and not chronology.zero(ray_gap)
        and entry(ray_gap, 0, 1) == -s.Rational(12, 5) * p
        and entry(ray_gap, 0, 2) == -s.Rational(16, 5) * p,
    )
    check(
        "ZERO_OBSERVER_RECORD_DIFFERS_AND_THE_RAY_PREDICATE_REJECTS_IT",
        not chronology.zero(zero_gap)
        and entry(zero_gap, 0, 1) == p
        and entry(zero_gap, 1, 0) == -p
        and parallel(e0, ZERO)
        and dot(e0, e0) == 1
        and dot(e0, ZERO) == 0
        and not is_positive_unit_ray(e0, ZERO),
    )
    check(
        "ANOTHER_GRAM_CHANGES_THE_RECORD_BY_A_DIFFERENT_MATRIX",
        not chronology.zero(gram_gap)
        and entry(gram_gap, 0, 1) == -p
        and entry(gram_gap, 1, 0) == -6 * p
        and not chronology.zero(double_gap - gram_gap),
    )

    prep = (ROOT / PREP).read_text()
    returns_at = prep.index("returns = [chronology.record(I4, n)[0] for n in basis]")
    channel_at = prep.index("    def channel(X):")
    binding_at = prep.index("    b = [I4[:, r] for r in range(4)]")
    normalized_at = prep.index(
        "    normalized = [vector / s.sqrt((vector.T * G * vector)[0]) for vector in b]"
    )
    check(
        "CHANNEL_IS_CLOSED_BEFORE_THE_SHIFT_BINDING",
        returns_at < channel_at < binding_at < normalized_at
        and "b = [" not in prep[returns_at:channel_at]
        and "record(G" not in prep[returns_at:channel_at],
    )
    check(
        "RECONSTRUCTION_IS_NOT_CALLED_A_SELECTED_IDENTIFICATION",
        "not a physical identification currently selected by the core." in prep,
    )
    check("PREPARATION_FILE_HAS_NO_CARTAN_SHIFT_TOKEN", ".shift" not in prep and "AffineCartan" not in prep)
    chronology_text = (ROOT / CHRONOLOGY).read_text()
    check(
        "CHRONOLOGY_FILE_HAS_NO_CARTAN_SHIFT_TOKEN",
        ".shift" not in chronology_text and "AffineCartan" not in chronology_text,
    )
    check(
        "RECORD_SIGNATURE_IS_GRAM_AND_OBSERVER",
        "def record(G, n, dG=None, dn=None):" in chronology_text,
    )

    nilpotent_text = (ROOT / NILPOTENT).read_text()
    nilpotent_body = extract_def(ROOT / NILPOTENT, "nilpotentAffineGenerator")
    check(
        "NILPOTENT_GENERATOR_IS_A_FREE_ROLESPACE_CREATOR",
        "def nilpotentAffineGenerator (b : RoleSpace) :" in nilpotent_body
        and "(archiveExteriorCreatorLM b).comp vacuumProjector" in nilpotent_body
        and ".shift" not in nilpotent_text
        and "AffineCartan" not in nilpotent_text,
    )

    found = {}
    creator_on_connection = []
    for name, path, code in definitions():
        if ".shift" in code:
            found[name] = code
        if "archiveExteriorCreator" in code and ("AffineCartan" in code or ".shift" in code):
            creator_on_connection.append(name)
    check("SHIFT_TOKEN_DEFINITIONS_ARE_EXACTLY_THE_NINE", set(found) == EXPECTED_SHIFT_DEFS)
    check(
        "NONE_OF_THE_NINE_APPLIES_THE_EXTERIOR_CREATOR",
        all("archiveExteriorCreator" not in code for code in found.values()),
    )
    check(
        "SOLDERED_DIRECTION_IS_THE_ONLY_CREATOR_ON_AN_AFFINE_CONNECTION",
        creator_on_connection == ["archiveSolderedCreateDirection"],
    )
    soldered = extract_def(ROOT / EXTERIOR, "archiveSolderedCreateDirection")
    check(
        "SOLDERED_CREATOR_READS_THE_LEG",
        "archiveExteriorCreator (solderLegVector" in soldered and ".shift" not in soldered,
    )
    scalar_shift = found["ResponseDecomposition.shift"]
    check(
        "SCALAR_SHIFT_GAUGE_IS_NOT_A_CARTAN_TRANSLATION",
        "g : X → ℝ" in scalar_shift and "AffineCartan" not in scalar_shift,
    )
    quotient = (ROOT / QUOTIENT).read_text()
    check(
        "QUOTIENT_STILL_LEAVES_B_E_ARBITRARY",
        "b_e = F_x a_e," in quotient
        and "b_e arbitrary in R^4," in quotient
        and "constraints on b or m." in quotient,
    )

    return {
        "schema": "d0-native-record-scale-not-cartan-shift/1",
        "status": "PASS_CONDITIONAL_RECORD_READS_SUPPLIED_SCALE_NOT_CARTAN_SHIFT",
        "proof": PROOF,
        "input_sha256": {path: sha(path) for path in sorted(INPUTS)},
        "exact_result": {
            "identity_gram_record_gap_at_double_observer": "(0,1)=-p,(1,0)=-103*p",
            "positive_unit_ray_of_2e0": "e0",
            "price_cut_at_identity_gram": "even in the observer",
            "preparation_binding": "b_r=e_r after the channel closes",
            "cartan_shift_token_in_record_or_preparation": False,
            "shift_token_definitions": sorted(EXPECTED_SHIFT_DEFS),
        },
        "exact_controls": len(checks),
        "checks": checks,
        "scope": {
            "record_at_double_equals_record_at_unit": False,
            "record_output_is_the_positive_unit_ray": False,
            "price_cut_sees_the_observer_sign_at_the_identity_gram": False,
            "gram_probe_is_a_native_admitted_metric": False,
            "preparation_channel_reads_the_later_binding": False,
            "nilpotent_generator_reads_a_cartan_shift": False,
            "shift_token_scan_is_a_whole_core_exhaustion": False,
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
