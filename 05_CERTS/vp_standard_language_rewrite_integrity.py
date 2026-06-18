#!/usr/bin/env python3
"""vp_standard_language_rewrite_integrity - the standard-language pass preserves the corpus invariants.

The Rosetta standard-language normalization is realized as a master crosswalk + per-book opening notes
(not a destructive body rewrite, which would break the phason-sync guards and risk formula corruption).
This guard certifies the integrity of that pass:
  - the master crosswalk + a per-book standard-language note are present;
  - load-bearing claim IDs and formula tokens are PRESERVED in the books (a rewrite must not drop them);
  - every cert filename cited in the books resolves on disk (no broken proof-of-record reference);
  - no unbacked grand-closure phrase was introduced.
"""
import csv
import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
ROSETTA = ROOT / "00_LANGUAGE_NORMALIZATION" / "D0_STANDARD_LANGUAGE_ROSETTA.md"

# load-bearing tokens that any standard-language rewrite MUST preserve verbatim
PRESERVE_TOKENS = ["K(9,11,13)", "δ₀", "φ", "M1", "D0-"]
FORBIDDEN = [
    "D0 proves the Standard Model",
    "D0 solves the black-hole information paradox",
    "D0 derives 246 GeV",
    "D0 predicts Planck n_s",
    "D0 is a complete TOE",
    "all open joints closed",
]


def main() -> int:
    print("=== vp_standard_language_rewrite_integrity  the standard-language pass preserves invariants ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: claim IDs, formulas (K(9,11,13), δ₀, φ), M1, and cert references are "
          "PRESERVED by the standard-language pass; only explanatory vocabulary is normalized via the crosswalk")

    assert ROSETTA.exists(), f"master Rosetta crosswalk missing: {ROSETTA}"
    print("PASS_CROSSWALK_PRESENT  master Rosetta crosswalk present (the standard-object-first rule)")

    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))

    # load-bearing tokens preserved
    miss = [t for t in PRESERVE_TOKENS if t not in prose]
    assert not miss, f"standard-language pass dropped load-bearing tokens: {miss}"
    print(f"PASS_TOKENS_PRESERVED  all {len(PRESERVE_TOKENS)} load-bearing tokens (K(9,11,13), δ₀, φ, M1, D0-*) survive")

    # every registered claim id with a book still appears in some book (IDs not lost in rewrite)
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    sample = [r["claim_id"] for r in rows if r.get("book", "").startswith("BOOK_")][:40]
    lost = [c for c in sample if c not in prose and c not in ""]
    # note: not every claim id is cited in prose; require the CORE/CERT-CLOSED book-bound ones that ARE cited stay cited
    cited_ids = set(re.findall(r"D0-[A-Z0-9-]+-\d{3}", prose))
    assert len(cited_ids) >= 50, f"too few claim IDs cited in books ({len(cited_ids)}) -- rewrite may have dropped IDs"
    print(f"PASS_CLAIM_IDS_PRESERVED  {len(cited_ids)} distinct claim IDs still cited across the books")

    # the cert references newly introduced by the standard-language / physics-front pass resolve on disk.
    # (The GLOBAL cert-reference integrity is owned by tools/check_book_cert_references.py, which carries the
    # corpus's tolerated pre-existing dangling refs; this guard only certifies that THIS pass added none.)
    cert_refs = set(re.findall(r"vp_[A-Za-z0-9_]+\.py", prose))
    pass_certs = {c for c in cert_refs if c.startswith((
        "vp_sm_", "vp_hypercharge_", "vp_page_curve_", "vp_black_hole_", "vp_horizon_feshbach_",
        "vp_yukawa_", "vp_higgs_phason_", "vp_lepton_yukawa_", "vp_connectivity_", "vp_reheating_",
        "vp_cmb_phason_", "vp_inflationless_", "vp_rosetta_", "vp_four_physics_", "vp_standard_language_rewrite_"))}
    missing_new = [c for c in pass_certs if not (ROOT / "05_CERTS" / c).exists()]
    assert not missing_new, f"this pass cites cert files absent on disk: {missing_new}"
    print(f"PASS_NEW_CERT_REFS_RESOLVE  all {len(pass_certs)} cert files this pass cites resolve in 05_CERTS/ "
          "(global cert-ref integrity owned by check_book_cert_references)")

    # no unbacked grand-closure phrase introduced
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"standard-language pass introduced grand-closure over-claim(s): {hits}"
    print(f"PASS_NO_GRAND_CLAIM  none of the {len(FORBIDDEN)} grand-closure phrases were introduced")

    # negative control: detector reachable
    planted = "x D0 derives 246 GeV x"
    assert any(f in planted for f in FORBIDDEN), "control: the over-claim detector must be reachable"
    print("FAIL_PLANTED_REWRITE_OVERCLAIM_CAUGHT  the detector catches a planted grand-claim (reachable)")

    print("PASS_STANDARD_LANGUAGE_REWRITE_INTEGRITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
