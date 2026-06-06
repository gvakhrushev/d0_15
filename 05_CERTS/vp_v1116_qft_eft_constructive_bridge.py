#!/usr/bin/env python3
from pathlib import Path
import re, sys, json

root = Path(__file__).resolve().parents[1]
book_dir = root / "01_BOOKS"

checks = {
    "Book00_constructive_EFT": (book_dir / "BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md",
        ["Constructive formalization", "proof object", "EFT", "renormalization scheme", "Lambda_{\\mathrm{act}}"]),
    "Book04_dressing_functor": (book_dir / "BOOK_04_SPECTRUM_MATTER_AND_PARTICLE_PASSPORTS.md",
        ["QFT/EFT dressing functor", "\\mathfrak D_{\\mathrm{SM}}^{D0}", "Ward/anomaly guardrail", "Bare invariant versus dressed passport"]),
    "Book05_bridge_obligations": (book_dir / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        ["Bridge-claim obligations", "BRIDGE-PROOF-CELL-MISSING", "Scheme discipline", "Ward and anomaly discipline", "Constructive proof-assistant discipline"]),
    "Book06_RG_forgetting": (book_dir / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        ["Wilsonian RG as a typed forgetting map", "\\Delta_N", "\\mathcal R_{\\mathrm{SM}}", "declared external evolution law"]),
}

results = {}
ok = True
for name, (path, terms) in checks.items():
    txt = path.read_text(encoding="utf-8")
    missing = [t for t in terms if t not in txt]
    results[name] = {"missing": missing, "pass": not missing}
    ok = ok and not missing

combined = book_dir / "03_COMBINED" / "D0_V11_16_FULL_CANONICAL_BOOKS_ACTIVE.md"
ctxt = combined.read_text(encoding="utf-8")
for t in ["Constructive formalization", "QFT/EFT dressing functor", "BRIDGE-PROOF-CELL-MISSING", "Wilsonian RG as a typed forgetting map"]:
    if t not in ctxt:
        ok = False
        results.setdefault("combined", {"missing": [], "pass": True})["missing"].append(t)
        results["combined"]["pass"] = False

out = root / "07_GLOBAL_AUDIT" / "V11_16_QFT_EFT_CONSTRUCTIVE_CERT_RESULTS.json"
out.write_text(json.dumps({"pass": ok, "checks": results}, indent=2), encoding="utf-8")
print("PASS" if ok else "FAIL")
print(out)
sys.exit(0 if ok else 1)
