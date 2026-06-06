#!/usr/bin/env python3
"""
D0 Glossary and Standard-Language Compression Consistency Check.

Enforces:
1. High-frequency internal terms appear in Book 00 or Book 05 glossary.
2. Every book has a short standard-language paragraph / first-use block.
3. No undefined D0-local term in headings (unless it has an owner like D0-XXX or Lean module).
4. No metaphor terms in active theorem / proof paths.
"""

from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime, timezone

INTERNAL_TERMS = [
    "archive", "readout", "terminal", "runtime", "tick",
    "scene", "gate", "selector", "passport", "bridge",
    "shadow", "capacity", "horizon archive", "dark sector",
    "archive pressure", "phason glass", "EchoCapacityOperator",
    "D0 vacuum", "D0 gravity", "D0 cosmology"
]

METAPHOR_TERMS = [
    "lift", "ladder", "pendulum", "DDoS", "fluid", "surface tension",
    "light sector", "dark sector as poetic", "archive as place",
    "vacuum crystal as material", "D0 as mythology"
]

def has_glossary_block(text: str) -> bool:
    patterns = [
        r"standard-language reading",
        r"D0 term \| Standard object",
        r"first-use glossary",
        r"standard language protocol",
        r"compression rule"
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    books_dir = root / "01_BOOKS"
    books = sorted(books_dir.glob("BOOK_*.md"))

    issues = []
    for book in books:
        text = book.read_text(encoding="utf-8", errors="replace")
        book_name = book.name

        # Check 2: glossary block
        if not has_glossary_block(text):
            issues.append((book_name, 0, "MISSING_STANDARD_LANGUAGE_BLOCK", "No first-use / glossary paragraph found"))

        # Check 3 & 4: headings and metaphors
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("#"):
                for term in INTERNAL_TERMS:
                    if re.search(rf"\b{re.escape(term)}\b", line, re.IGNORECASE):
                        if not re.search(r"D0-[A-Z0-9-]+|Lean|owner|theorem|module", line, re.IGNORECASE):
                            issues.append((book_name, i, "UNDEFINED_D0_TERM_IN_HEADING", line.strip()[:120]))

            for m in METAPHOR_TERMS:
                if m.lower() in line.lower():
                    issues.append((book_name, i, "METAPHOR_IN_PROSE", line.strip()[:120]))

        # Check 1: frequency (simple count)
        for term in INTERNAL_TERMS:
            count = len(re.findall(rf"\b{re.escape(term)}\b", text, re.IGNORECASE))
            if count > 20 and "BOOK_00" not in book_name and "BOOK_05" not in book_name:
                if term not in text[:2000]:  # rough "not in early glossary"
                    issues.append((book_name, 0, "HIGH_FREQ_TERM_MISSING_GLOSSARY", f"{term} appears {count} times, not defined early"))

    out_dir = root / "06_AUDIT"
    out_dir.mkdir(parents=True, exist_ok=True)

    if issues:
        status = "FAIL_STANDARD_LANGUAGE_GLOSSARY"
        md = ["# Glossary Consistency Failures", f"Generated {datetime.now(timezone.utc).isoformat()}", ""]
        for b, ln, typ, ctx in issues:
            md.append(f"- **{b}**:{ln} [{typ}] {ctx}")
        (out_dir / "glossary_consistency_fail.md").write_text("\n".join(md), encoding="utf-8")
    else:
        status = "PASS_STANDARD_LANGUAGE_GLOSSARY"
        (out_dir / "glossary_consistency_pass.md").write_text(status + "\n", encoding="utf-8")

    print(status)
    print(f"Issues: {len(issues)}")
    if issues:
        print("See 06_AUDIT/glossary_consistency_fail.md")

if __name__ == "__main__":
    main()
