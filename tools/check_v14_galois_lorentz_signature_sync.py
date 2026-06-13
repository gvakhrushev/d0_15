#!/usr/bin/env python3
"""v14 QUASI-006 Galois/Lorentz signature sync guard."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"
CERTS = ROOT / "05_CERTS"
RUNNER = ROOT / "tools" / "run_hard_theorem_closure.py"

CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Galois/Lorentz Lean owner",
        LEAN / "Physics" / "GaloisLorentzSignature.lean",
        [
            "GaloisLorentzSignatureClosure",
            "galoisLorentzSignatureClosure",
            "galois_lorentz_signature_closed",
            "D0.Dynamics.d0_integer_trace_layers",
            "D0.roleSignature_eq_1_3",
            "D0.no_euclidean_SO4",
        ],
    ),
    (
        "Galois/Lorentz cert",
        CERTS / "vp_galois_lorentz_signature.py",
        [
            "PASS_GALOIS_LORENTZ_SIGNATURE",
            "ActiveArchiveTrace",
            "det(T^n)^2=1",
            "roleSignature=(1,3)",
        ],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_galois_lorentz_signature_closed",
            "D0.Physics.GaloisLorentzSignature",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-QUASI006-GALOIS-LORENTZ-SIGNATURE-001",
            "D0.Physics.GaloisLorentzSignature",
            "vp_galois_lorentz_signature.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        ["galois-lorentz-signature", "PASS_GALOIS_LORENTZ_SIGNATURE"],
    ),
]

FORBIDDEN_LEAN_TOKENS = ["sorry", "admit", "axiom", "unsafe", "Float", "opaque"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


def main() -> int:
    errors: list[str] = []
    for label, path, tokens in CHECKS:
        if not path.exists():
            errors.append(f"{label}: missing {path.relative_to(ROOT)}")
            continue
        text = read(path)
        for token in tokens:
            if token not in text:
                errors.append(f"{label}: missing token {token!r}")

    lean_path = LEAN / "Physics" / "GaloisLorentzSignature.lean"
    if lean_path.exists():
        code = code_without_line_comments(lean_path)
        for token in FORBIDDEN_LEAN_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"{lean_path.relative_to(ROOT)} contains forbidden token {token!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_GALOIS_LORENTZ_SIGNATURE_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
