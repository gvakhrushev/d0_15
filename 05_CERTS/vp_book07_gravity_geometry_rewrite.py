from pathlib import Path
import csv, json, sys
ROOT=Path(__file__).resolve().parents[1]
book=(ROOT/'01_BOOKS'/'BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md').read_text(encoding='utf-8')
heading_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK07_FROM_OLD08_HEADING_CONSUMPTION_LEDGER.csv').open(encoding='utf-8')))
formula_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK07_FROM_OLD08_FORMULA_COVERAGE_LEDGER.csv').open(encoding='utf-8')))
claim_rows=list(csv.DictReader((ROOT/'06_COVERAGE'/'BOOK07_FROM_OLD08_CLAIM_COVERAGE.csv').open(encoding='utf-8')))
required=[
 'BOOK 07 — Gravity limit and finite geometry',
 'Length-depth theorem before Newton',
 'Geometric heat trace and Einstein target',
 'pi0 is phase holonomy, not Newton repair',
 'Cosmology and archive pressure handoff',
 'legacy formulas retained from old Book 08'
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
# protect core guardrail phrases
for s in ['length-depth first; Newton coefficient second', 'not Newton repair', 'survey residual', 'q_res']:
    if s not in book: errors.append('missing guardrail phrase: '+s)
result={'status':'PASS' if not errors else 'FAIL','headings':len(heading_rows),'formulas':len(formula_rows),'claims':len(claim_rows),'errors':errors[:30]}
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors: sys.exit(1)
