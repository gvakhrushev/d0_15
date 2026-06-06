from pathlib import Path
import csv, re, json, sys
root=Path(__file__).resolve().parents[1]
book=root/'01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md'
heading=root/'06_COVERAGE/BOOK03_FROM_OLD02_HEADING_CONSUMPTION_LEDGER.csv'
formula=root/'06_COVERAGE/BOOK03_FROM_OLD02_FORMULA_COVERAGE_LEDGER.csv'
claims=root/'06_COVERAGE/BOOK03_FROM_OLD02_CLAIM_COVERAGE.csv'
text=book.read_text(encoding='utf-8')
rows=list(csv.DictReader(heading.open(encoding='utf-8')))
forms=list(csv.DictReader(formula.open(encoding='utf-8')))
cl=list(csv.DictReader(claims.open(encoding='utf-8')))
required=['S_{gate}','J_{scene}','S_\\Lambda','S_\\partial','\\Lambda_{act}','I_B','quadratic readout','single-section']
missing=[r for r in required if r not in text]
# at least one handoff to Book02, Book04, Book07 or 08
handoffs={r['canonical_destination'] for r in rows if r['canonical_destination']!='BOOK_03'}
errors=[]
if missing: errors.append({'missing_required_terms':missing})
if len(rows)<80: errors.append({'heading_rows_too_low':len(rows)})
if len(forms)<100: errors.append({'formula_rows_too_low':len(forms)})
if not cl: errors.append({'claim_rows_zero':0})
if 'BOOK_04' not in handoffs: errors.append({'missing_matter_handoff':sorted(handoffs)})
if not any(x in handoffs for x in ['BOOK_07','BOOK_07_OR_08','BOOK_08']): errors.append({'missing_gravity_cosmo_handoff':sorted(handoffs)})
if any('\x00' in text for _ in [0]): errors.append({'control_char':'NUL'})
status='PASS' if not errors else 'FAIL'
result={'status':status,'heading_rows':len(rows),'formula_rows':len(forms),'claim_rows':len(cl),'handoff_destinations':sorted(handoffs),'errors':errors}
out=root/'06_COVERAGE/BOOK03_SYNTHESIS_CERT_RESULTS.json'
out.write_text(json.dumps(result,indent=2),encoding='utf-8')
(root/'06_COVERAGE/BOOK03_SYNTHESIS_CERT_RESULTS.txt').write_text(status+'\n'+json.dumps(result,indent=2),encoding='utf-8')
print(status)
print(json.dumps(result,indent=2))
sys.exit(0 if status=='PASS' else 1)
