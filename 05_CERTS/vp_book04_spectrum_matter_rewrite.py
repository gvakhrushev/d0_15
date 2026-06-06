#!/usr/bin/env python3
from pathlib import Path
import csv, re, json
root=Path(__file__).resolve().parents[1]
book=(root/'01_BOOKS'/'BOOK_04_SPECTRUM_MATTER_AND_PARTICLE_PASSPORTS.md').read_text(encoding='utf-8')
heads=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK04_FROM_OLD03_HEADING_CONSUMPTION_LEDGER.csv',encoding='utf-8')))
forms=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK04_FROM_OLD03_FORMULA_COVERAGE_LEDGER.csv',encoding='utf-8')))
claims=list(csv.DictReader(open(root/'06_COVERAGE'/'BOOK04_FROM_OLD03_CLAIM_COVERAGE.csv',encoding='utf-8')))
required = [
    'finite support}\\neq\\text{physical mass',
    'D_e^2=1+{\\delta_0\\over3}',
    'M_\\ell^{D0}=D_\\ell^TG_R^+D_\\ell+\\kappa I',
    'T_{CKM}^{D0}=O_{cyc}G_R^+D_{PNO}',
    '\\lambda_{B2}^{deg}=3960',
    '\\lambda_{mes}^{min}=400=20^2',
    '400\\Rightarrow m_\\pi',
    '3960',
    'Y_f^{D0}',
    'S_{matter}(u)'
]
missing=[r for r in required if r not in book]
result={'status':'PASS' if not missing and len(heads)>=70 and len(forms)>=150 and len(claims)>=10 else 'FAIL', 'missing_required':missing, 'headings':len(heads), 'formulas':len(forms), 'claims':len(claims)}
print(json.dumps(result,indent=2))
assert result['status']=='PASS'
