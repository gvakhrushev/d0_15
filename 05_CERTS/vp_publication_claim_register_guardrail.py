#!/usr/bin/env python3
"""Publication claim-register guardrail for D0."""
from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / '00_PUBLICATION'
STATUS = ROOT / '00_PUBLICATION' / 'D0_CLAIMS_REGISTER.csv'  # publication register owns the bridge/negative rows

REQUIRED = [
    'D0_CLAIMS_REGISTER.md',
    'D0_CLAIMS_REGISTER.csv',
    'D0_THEOREM_DEPENDENCY_GRAPH.md',
    'D0_PUBLICATION_ABSTRACT.md',
    'D0_REVIEWER_RISK_LEDGER.md',
    'D0_DO_NOT_CLAIM.md',
    'D0_FINAL_PUBLICATION_CHECKLIST.md',
    'D0_RELEASE_NOTES.md',
    'D0_MINIMAL_THEORY_SPINE.md',
]


def boolish(x):
    return str(x).strip().lower() in {'true','1','yes','y'}


def main():
    missing = [name for name in REQUIRED if not (PUB/name).exists()]
    assert not missing, f'missing publication files: {missing}'
    print('PASS_PUBLICATION_FILES_PRESENT')

    with STATUS.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    dusty = [r for r in rows if r['claim_id'] == 'D0-DUSTY-TABLETOP-BRIDGE-001']
    ligo = [r for r in rows if r['claim_id'] == 'D0-LIGO-DISCOVERY-NEGATIVE-001']
    assert dusty and ligo, 'required publication bridge/negative rows missing'
    assert 'LAB-BRIDGE' in dusty[0]['release_status'], dusty[0]['release_status']
    assert boolish(dusty[0]['uses_bridge_assumptions'])
    assert 'NEGATIVE' in ligo[0]['release_status'], ligo[0]['release_status']
    assert boolish(ligo[0]['uses_bridge_assumptions'])
    print('PASS_EXTERNAL_ROWS_GUARDED')

    reg = (PUB/'D0_CLAIMS_REGISTER.csv').read_text(encoding='utf-8')
    assert 'LAB-BRIDGE / EMPIRICAL-PASSPORT' in reg or 'LAB-BRIDGE' in reg
    assert 'EMPIRICAL-NEGATIVE' in reg
    print('PASS_CLAIMS_REGISTER_CLASSES_PRESENT')

    dep = (PUB/'D0_THEOREM_DEPENDENCY_GRAPH.md').read_text(encoding='utf-8')
    assert 'does not depend on' in dep.lower()
    assert 'LIGO/GWOSC' in dep
    assert 'dusty-plasma' in dep or 'dusty plasma' in dep
    print('PASS_CORE_INSULATION_DECLARED')

    abstract = (PUB/'D0_PUBLICATION_ABSTRACT.md').read_text(encoding='utf-8')
    assert 'negative-control' in abstract or 'negative controls' in abstract
    assert 'not as proof of quantum gravity' in abstract
    print('PASS_ABSTRACT_CLAIM_SAFE')

    print('PASS_PUBLICATION_CLAIM_REGISTER_GUARDRAIL')

if __name__ == '__main__':
    main()
