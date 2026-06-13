#!/usr/bin/env python3
"""Guardrail cert for Book 09 GW/interferometry bridge."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
BOOK09 = ROOT / '01_BOOKS' / 'BOOK_09_GRAVITATIONAL_WAVES_AND_QUANTUM_INTERFEROMETRY.md'
BOOK07 = ROOT / '01_BOOKS' / 'BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md'

FORBIDDEN_CLAIMS = [
    'LIGO confirms D0',
    'LIGO proves D0',
    'GWOSC confirms D0',
    'proved by LIGO',
    'empirical confirmation of D0 by LIGO',
]
REQUIRED = [
    'No LIGO confirmation claim is allowed in v16',
    'apple-torus',
    'spindle-torus',
    'Tr}(2\\Pi_{axis}-\\Pi_{transverse})=0',
    'horizon hum',
    'Born-rule beat',
    'I_A = \\varphi^{-1}',
    'I_f = \\log\\varphi',
    'V3--V12',
    'negative-control',
]

def main():
    assert BOOK09.exists(), 'BOOK_09 missing'
    txt = BOOK09.read_text(encoding='utf-8')
    for token in REQUIRED:
        assert token in txt, f'missing required Book09 token: {token}'
    low = txt.lower()
    assert 'does not claim ligo confirmation' in low or 'no ligo confirmation claim' in low
    for bad in FORBIDDEN_CLAIMS:
        assert bad.lower() not in low, f'forbidden overclaim present: {bad}'
    b7 = BOOK07.read_text(encoding='utf-8')
    assert 'Book 09' in b7 and 'no LIGO confirmation claim' in b7
    print('PASS_BOOK09_GW_BRIDGE_PRESENT')
    print('PASS_BOOK09_NEGATIVE_CONTROL_GUARDED')
    print('PASS_BOOK07_BOOK09_CROSS_REFERENCE')
    print('PASS_GW_PUBLICATION_GUARDRAIL')

if __name__ == '__main__':
    main()
