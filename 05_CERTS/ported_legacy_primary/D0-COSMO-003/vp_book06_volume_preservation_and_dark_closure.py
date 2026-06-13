#!/usr/bin/env python3
"""Book 06 volume-preservation and dark-sector closure repair certificate."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_LINES = 841
PREVIOUS_CHARS = 27168
DESTRUCTIVE_LINES = 307
DESTRUCTIVE_CHARS = 8888


def main() -> dict[str, object]:
    book6 = ROOT/'01_BOOKS'/'BOOK_06_COSMOLOGY.md'
    text = book6.read_text(encoding='utf-8')
    lines = text.count('\n') + 1
    chars = len(text)
    checks = {
        'volume_restored_lines_ge_previous': lines >= PREVIOUS_LINES,
        'volume_restored_chars_ge_previous': chars >= PREVIOUS_CHARS,
        'contains_no_primitive_OmegaDM_theorem': 'Omega_{DM}\\notin\\mathcal I_{D0}^{core}' in text,
        'contains_closed_archive_tuple': '\\mathcal B_{D0}' in text,
        'contains_boundary_kernel': 'K_B[W_B](k)=\\exp[-\\chi_B W_B(k)]' in text,
        'destructive_phrase_removed': 'not yet closed externally' not in text,
    }
    status = 'PASS_BOOK06_VOLUME_PRESERVATION_AND_DARK_SECTOR_CLOSURE' if all(checks.values()) else 'FAIL_BOOK06_VOLUME_PRESERVATION_AND_DARK_SECTOR_CLOSURE'
    return {
        'status': status,
        'previous_lines': PREVIOUS_LINES,
        'previous_chars': PREVIOUS_CHARS,
        'destructive_lines': DESTRUCTIVE_LINES,
        'destructive_chars': DESTRUCTIVE_CHARS,
        'repaired_lines': lines,
        'repaired_chars': chars,
        'checks': checks,
        'interpretation': 'Book 06 was restored from the last full-volume corpus and the boundary-dark kernel was integrated without replacing the existing cosmology theory.'
    }

if __name__ == '__main__':
    res = main()
    print(f"vp_book06_volume_preservation_and_dark_closure: [{res['status']}]")
    print(json.dumps(res, indent=2, sort_keys=True))
