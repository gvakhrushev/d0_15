from pathlib import Path
import re, csv, sys, json
ROOT=Path(__file__).resolve().parents[1]
book=(ROOT/'01_BOOKS'/'BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md').read_text(encoding='utf-8')
heading_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK06_FROM_OLD07_HEADING_CONSUMPTION_LEDGER.csv').open(encoding='utf-8')))
formula_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK06_FROM_OLD07_FORMULA_COVERAGE_LEDGER.csv').open(encoding='utf-8')))
claim_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK06_FROM_OLD07_CLAIM_COVERAGE.csv').open(encoding='utf-8')))
required=[
 'BOOK 06 — Evolution, forgetting and time',
 'Active/archive decomposition',
 'Forgetting maps as typed quotients',
 'Normalized tick operator',
 'Tick-to-scattering passport',
 'Archive-pressure runtime kernel',
 'legacy formulas retained from old Book 07'
]
errors=[]
for s in required:
    if s not in book: errors.append('missing required section/text: '+s)
for r in claim_rows:
    if r['Claim_ID'] not in book: errors.append('claim id not present in book: '+r['Claim_ID'])
for r in formula_rows:
    if r['formula_id'] not in book: errors.append('formula id not present in appendix: '+r['formula_id'])
for ch in ['\x08','\x0b','\x0c','\x7f']:
    if ch in book: errors.append('control char present')
result={'status':'PASS' if not errors else 'FAIL','headings':len(heading_rows),'formulas':len(formula_rows),'claims':len(claim_rows),'errors':errors[:20]}
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors: sys.exit(1)
