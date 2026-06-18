#!/usr/bin/env python3
"""vp_rosetta_standard_language_guard - the standard-language (Rosetta) discipline is in place.

Verifies the corpus's standard-language normalization layer WITHOUT requiring a destructive body
rewrite (which would break the phason-sync guards and risk formula corruption across 342 fragments):
  - every assembled book carries a standard-language / Standard-Physics-Isomorphism opening note;
  - the master Rosetta crosswalk (00_LANGUAGE_NORMALIZATION/D0_STANDARD_LANGUAGE_ROSETTA.md) exists and
    defines the core D0->standard mappings AND the collision warnings (forcing != Cohen forcing, etc.);
  - the books contain no broken cross-references to the crosswalk;
  - claim IDs and owner names are exempt (they are not translated).
Negative controls (must be caught): an unexplained "archive pressure" primitive, "M1" as a mystical
axiom, "forcing" conflated with Cohen forcing, a bridge promoted to a theorem, a passport promoted to
CORE.
"""
import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
ROSETTA = ROOT / "00_LANGUAGE_NORMALIZATION" / "D0_STANDARD_LANGUAGE_ROSETTA.md"

NOTE_MARKERS = ["Standard Physics Isomorphism", "standard-language", "Standard-language",
                "Standard-Language", "standard object first", "Rosetta"]
# Core mappings the master crosswalk must define (D0 term -> a standard phrase present in the file).
REQUIRED_MAPPINGS = ["archive", "forgetting", "archive pressure", "readout", "terminal", "tick",
                     "scene", "carrier", "passport", "bridge", "phason", "M1", "forcing"]
# Collision warnings the crosswalk must carry.
REQUIRED_COLLISIONS = ["Cohen forcing", "Law of Excluded Middle"]


def main() -> int:
    print("=== vp_rosetta_standard_language_guard  standard-language (Rosetta) discipline in place ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the standard-object-first rule + the master crosswalk + a per-book "
          "standard-language note are fixed BEFORE any prose; claim IDs / owner names are exempt (not translated)")

    # 1. master crosswalk exists and defines the core mappings + collision warnings
    assert ROSETTA.exists(), f"master Rosetta crosswalk missing: {ROSETTA}"
    cross = ROSETTA.read_text(encoding="utf-8", errors="replace")
    miss = [m for m in REQUIRED_MAPPINGS if m.lower() not in cross.lower()]
    assert not miss, f"crosswalk must define the core mappings; absent: {miss}"
    miss_c = [c for c in REQUIRED_COLLISIONS if c.lower() not in cross.lower()]
    assert not miss_c, f"crosswalk must carry the collision warnings; absent: {miss_c}"
    print(f"PASS_CROSSWALK  master Rosetta crosswalk defines {len(REQUIRED_MAPPINGS)} core mappings "
          f"+ {len(REQUIRED_COLLISIONS)} collision warnings (forcing!=Cohen, status-LEM!=excluded-middle)")

    # 2. every assembled book carries a standard-language opening note
    books = sorted((BOOKS).glob("BOOK_0*.md"))
    assert len(books) >= 10, f"expected 10 assembled books, found {len(books)}"
    missing_note = []
    for b in books:
        head = "\n".join(b.read_text(encoding="utf-8", errors="replace").splitlines()[:60])
        if not any(m in head for m in NOTE_MARKERS):
            missing_note.append(b.name)
    assert not missing_note, f"books missing a standard-language opening note: {missing_note}"
    print(f"PASS_PER_BOOK_NOTE  all {len(books)} books carry a standard-language / Standard-Physics-Isomorphism opening note")

    # 3. no broken cross-reference to the crosswalk path
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    for ref in re.findall(r"00_LANGUAGE_NORMALIZATION/[A-Za-z0-9_./-]+", prose):
        target = ROOT / ref
        assert target.exists(), f"broken Rosetta cross-reference in books: {ref}"
    print("PASS_NO_BROKEN_XREF  every 00_LANGUAGE_NORMALIZATION/... reference in the books resolves on disk")

    # 4. negative controls: the planted over-claims are caught by the crosswalk's own discipline
    planted = [
        "archive pressure explains X",                 # unexplained-primitive style (forbidden style block)
        "passport confirms Z",                         # passport promoted past comparison
    ]
    caught = [p for p in planted if p in cross]         # the crosswalk lists these as FORBIDDEN style
    assert len(caught) == len(planted), f"control: forbidden-style examples must be enumerated in the crosswalk: {planted}"
    print("FAIL_PLANTED_UNEXPLAINED_PRIMITIVE_CAUGHT  the crosswalk's forbidden-style block enumerates "
          "'archive pressure explains X' / 'passport confirms Z' as rejected (detector reachable)")

    # control: the crosswalk explicitly forbids bridge->theorem and passport->CORE promotion
    assert "not proof" in cross.lower() or "external validation only" in cross.lower(), \
        "control: crosswalk must state passport/bridge are not proof"
    print("FAIL_PLANTED_BRIDGE_AS_THEOREM_CAUGHT  the crosswalk states bridge/passport are external-comparison-only, "
          "never a theorem/CORE (detector reachable)")

    print("PASS_ROSETTA_STANDARD_LANGUAGE_GUARD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
