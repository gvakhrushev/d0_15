#!/usr/bin/env python3
"""
D0 Standard Language Compression Audit.

Scans Books 00-08 for internal D0 terms and classifies occurrences.
Outputs CSV and MD report with suggested standard replacements.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from datetime import datetime, timezone

INTERNAL_TERMS = [
    "archive", "readout", "terminal readout", "runtime", "tick",
    "scene", "gate", "selector", "passport", "bridge",
    "shadow", "capacity boundary", "horizon archive", "dark sector",
    "archive pressure", "phason glass", "EchoCapacityOperator",
    "D0 vacuum", "D0 gravity", "D0 cosmology", "D0 horizon",
    "archive boundary", "Einstein shadow", "length-depth",
    "finite line covariance", "TT carrier", "spin-2 carrier",
    "heat-trace gravity", "echo lattice", "spacetime crystal",
    "terminal matter triad", "meson phason domain wall",
    "baryon S3 symmetrizer", "CKM phason holonomy",
    "Higgs scalar projector", "survey transfer", "S_DE",
    "internal archive cosmology object", "closure", "hard closure",
    "owner", "no-go"
]

REPLACEMENT_MAP = {
    "archive": "traced-out complement / quotient sector",
    "readout": "positive measurement outcome / positive response functional",
    "terminal readout": "absorbing rank-reducing measurement channel",
    "runtime": "ordered finite evolution / finite record dynamics",
    "tick": "discrete evolution endomorphism",
    "scene": "finite incidence / clique complex",
    "gate": "finite variational test functional",
    "selector": "finite variational selector / strict minimizer",
    "passport": "external comparison protocol",
    "bridge": "typed transfer / calibration dictionary",
    "shadow": "macro interface / smooth limit",
    "capacity boundary": "finite boundary-capacity saturation",
    "horizon archive": "terminal boundary quotient into traced-out sector",
    "dark sector": "Galois-conjugate unresolved branch",
    "archive pressure": "effective boundary response of traced-out sector",
    "phason glass": "phason-strain disorder in the internal/Galois branch",
    "D0 vacuum": "condensed/profinite φ-quasicrystalline tiling hull (D0 model)",
    "D0 gravity": "finite spectral geometry and its macro Einstein interface",
    "D0 cosmology": "finite survey readout and transfer/comparison protocols",
    "archive boundary": "boundary of traced-out complement",
    "Einstein shadow": "Einstein-Hilbert macro-interface",
    "length-depth": "dimensionless spectral scale-separation invariant (D_L)",
    "finite line covariance": "covariance of finite edge/line probes",
    "TT carrier": "transverse-traceless quotient",
    "spin-2 carrier": "finite transverse-traceless symmetric tensor quotient",
    "heat-trace gravity": "spectral heat-kernel expansion / A2 coefficient response",
    "echo lattice": "discrete self-similar log-time lattice",
    "spacetime crystal": "discrete self-similar critical-collapse solution",
    "terminal matter triad": "three terminal measurement roles for matter readout",
    "meson phason domain wall": "gap-labeled phason domain-wall excitation",
    "baryon S3 symmetrizer": "S3-symmetric 2-simplex projection",
    "CKM phason holonomy": "non-abelian holonomy of generation-basis transport",
    "Higgs scalar projector": "rank-2 scalar intertwiner / scalar projector",
    "survey transfer": "empirical likelihood transfer kernel",
    "S_DE": "finite-window spectral transfer function",
    "internal archive cosmology object": "frozen internal spectral-transfer object",
    "closure": "proved theorem / executable certificate / verified comparison (context-dependent)",
    "hard closure": "machine-checked theorem/certificate closure",
    "owner": "formal proof / Lean / certificate owner",
    "no-go": "negative theorem / forbidden promotion / negative control",
}

BOOKS = [f"BOOK_{i:02d}_*.md" for i in range(9)]  # 00 to 08

def classify(term: str, context: str, book: str, line: int) -> str:
    """Classify occurrence."""
    context_lower = context.lower()
    if "lean" in context_lower or "owner" in context_lower or "D0-" in context or "certificate" in context_lower or "theorem" in context_lower or "manifest" in context_lower:
        return "OK_OWNER"
    if "first use" in context_lower or "glossary" in context_lower or "standard-language" in context_lower or line < 100:
        return "OK_FIRST_USE"
    if "`" in context or "$" in context or "\\" in context or "math" in context_lower:
        return "OK_CODE_OR_FORMULA"
    if any(m in context_lower for m in ["metaphor", "poetic", "as a", "called"]):
        return "NEEDS_STANDARD_REWRITE"
    return "NEEDS_STANDARD_REWRITE"

def main() -> None:
    root = Path(__file__).resolve().parents[1] / "01_BOOKS"
    results = []
    for book_file in sorted(root.glob("BOOK_*.md")):
        if not book_file.is_file():
            continue
        book_name = book_file.name
        lines = book_file.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, line in enumerate(lines, 1):
            for term in INTERNAL_TERMS:
                if re.search(rf"\b{re.escape(term)}\b", line, re.IGNORECASE):
                    cls = classify(term, line, book_name, i)
                    suggested = REPLACEMENT_MAP.get(term, term)
                    results.append({
                        "book": book_name,
                        "line": i,
                        "term": term,
                        "context": line.strip()[:200],
                        "classification": cls,
                        "suggested_replacement": suggested,
                    })

    out_dir = Path(__file__).resolve().parents[1] / "06_AUDIT"
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "standard_language_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["book", "line", "term", "context", "classification", "suggested_replacement"])
        writer.writeheader()
        writer.writerows(results)

    md_path = out_dir / "standard_language_audit.md"
    md_lines = [
        "# D0 Standard Language Audit Report",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Total occurrences scanned: {len(results)}",
        "",
        "## Summary by Classification",
    ]
    counts = {}
    for r in results:
        counts[r["classification"]] = counts.get(r["classification"], 0) + 1
    for cls, cnt in sorted(counts.items()):
        md_lines.append(f"- {cls}: {cnt}")

    md_lines.append("")
    md_lines.append("## Needs Rewrite (sample)")
    for r in [r for r in results if r["classification"] == "NEEDS_STANDARD_REWRITE"][:30]:
        md_lines.append(f"- {r['book']}:{r['line']} `{r['term']}` → {r['suggested_replacement']}")
        md_lines.append(f"  > {r['context']}")

    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Audit complete. CSV: {csv_path}")
    print(f"MD: {md_path}")
    print(f"Total flagged for rewrite: {counts.get('NEEDS_STANDARD_REWRITE', 0)}")

if __name__ == "__main__":
    main()
