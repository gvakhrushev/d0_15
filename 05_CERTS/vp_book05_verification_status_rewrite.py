#!/usr/bin/env python3
from pathlib import Path
import csv, json
root=Path(__file__).resolve().parents[1]
book=(root/'01_BOOKS'/'BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md').read_text(encoding='utf-8')
heads=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK05_FROM_OLD04_HEADING_CONSUMPTION_LEDGER.csv',encoding='utf-8')))
forms=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK05_FROM_OLD04_FORMULA_COVERAGE_LEDGER.csv',encoding='utf-8')))
claims=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK05_FROM_OLD04_CLAIM_COVERAGE.csv',encoding='utf-8')))
B=chr(92)
required=[
 'certificate never replaces a proof',
 'CORE-FOUNDATION',
 'EMPIRICAL-PASSPORT',
 'NO-GO',
 '3960'+B+'not'+B+'rightarrow m_p',
 '400'+B+'not'+B+'rightarrow m_'+B+'pi',
 'External data are allowed only in declared passports',
 'Falsification matrix',
 B+'text{claim coverage}'+B+'neq'+B+'text{script count}',
 B+'text{claim}'+B+'rightarrow'+B+'text{support}'
]
missing=[r for r in required if r not in book]
ctrl=[(i,ord(ch)) for i,ch in enumerate(book) if ord(ch)<32 and ch not in '\n\t\r']
result={'status':'PASS' if not missing and not ctrl and len(heads)>=100 and len(forms)>=100 and len(claims)>=30 else 'FAIL','missing_required':missing,'control_chars':ctrl[:10],'headings':len(heads),'formulas':len(forms),'claims':len(claims)}
print(json.dumps(result,indent=2))
assert result['status']=='PASS'
