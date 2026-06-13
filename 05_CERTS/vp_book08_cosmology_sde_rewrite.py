from pathlib import Path
import csv, json, sys
ROOT=Path(__file__).resolve().parents[1]
book=(ROOT/'01_BOOKS'/'BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md').read_text(encoding='utf-8')
heading_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK08_FROM_OLD06_HEADING_CONSUMPTION_LEDGER.csv').open(encoding='utf-8')))
formula_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK08_FROM_OLD06_FORMULA_COVERAGE_LEDGER.csv').open(encoding='utf-8')))
claim_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK08_FROM_OLD06_CLAIM_COVERAGE.csv').open(encoding='utf-8')))
required=[
 'BOOK 08 — Cosmology, archive and S_DE transfer',
 'Archive-pressure operator',
 'Scalar survey amplitude passport',
 'Static coefficient versus dynamic transfer',
 'S_DE finite-window transfer',
 'BAO archive-transfer passport',
 'external-data discipline',
 'legacy formulas retained from old Book 06'
]
errors=[]
for s in required:
    if s not in book: errors.append('missing required section/text: '+s)
for r in claim_rows:
    if r['Claim_ID'] and r['Claim_ID'] not in book:
        errors.append('claim id not present in book: '+r['Claim_ID'])
for r in formula_rows:
    if r['formula_id'] not in book:
        errors.append('formula id not present in appendix: '+r['formula_id'])
for bad in ['\x08','\x0b','\x0c','\x7f']:
    if bad in book: errors.append('control char present')
for s in ['not a dark-particle catalogue', 'denominator is not a fit parameter', 'closed archive coefficient', 'external data allowed at passport stage only']:
    if s not in book: errors.append('missing guardrail phrase: '+s)
result={'status':'PASS' if not errors else 'FAIL','headings':len(heading_rows),'formulas':len(formula_rows),'claims':len(claim_rows),'errors':errors[:50]}
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors: sys.exit(1)
