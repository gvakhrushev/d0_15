from pathlib import Path
import csv, sys
root=Path(__file__).resolve().parents[1]
book=(root/'01_BOOKS'/'BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md').read_text(encoding='utf-8')
claim_rows=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK00_CLAIM_COVERAGE.csv',encoding='utf-8')))
formula_rows=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK00_FORMULA_COVERAGE_LEDGER.csv',encoding='utf-8')))
heading_rows=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK00_HEADING_CONSUMPTION_LEDGER.csv',encoding='utf-8')))
fail=[]
if len(claim_rows)!=6: fail.append(f'expected 6 Book00 claims, got {len(claim_rows)}')
if any(r['coverage']!='PASS' for r in claim_rows): fail.append('claim coverage failure')
if len(formula_rows)<100: fail.append(f'formula inventory too small: {len(formula_rows)}')
if any(r['coverage_location'] not in {'main_text','formula_appendix'} for r in formula_rows): fail.append('bad formula coverage location')
if len(heading_rows)<40: fail.append(f'heading ledger too small: {len(heading_rows)}')
required=['SCIENTIFIC-FRONT-MATTER','p+p^2=1','S_{D0}^\\varphi','ABCD','spectrum','D0-FOUND-001','D0-META-001']
for term in required:
    if term not in book: fail.append(f'missing term {term}')
if fail:
    print('FAIL')
    for x in fail: print('-',x)
    sys.exit(1)
print('PASS')
print('claims',len(claim_rows))
print('formulas',len(formula_rows))
print('headings',len(heading_rows))
