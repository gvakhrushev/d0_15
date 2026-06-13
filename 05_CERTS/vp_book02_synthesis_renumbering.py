from pathlib import Path
import csv, json
root=Path(__file__).resolve().parents[1]
book=root/'01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md'
text=book.read_text(encoding='utf-8')
checks={
 'book02_exists': book.exists(),
 'renumber_manifest_exists': (root/'00_REFACTOR_STRATEGY/D0_CANONICAL_RENUMBERING_MANIFEST.csv').exists(),
 'contains_proof_chain': 'finite support' in text and 'normalized readout/passport' in text,
 'contains_condensed_subfunctor': '\\mathcal M^{D0}' in text,
 'contains_response_operator': 'R_N=\\mathcal D_N^\\dagger\\mathcal D_N' in text,
 'contains_transfer_schema': 'S_{DE}(u)' in text,
 'contains_formula_appendix': 'Formula preservation ledger' in text,
}
with open(root/'06_COVERAGE/BOOK02_FROM_OLD05_FORMULA_COVERAGE_LEDGER.csv',encoding='utf-8') as fp:
    formulas=sum(1 for _ in csv.DictReader(fp))
with open(root/'06_COVERAGE/BOOK02_FROM_OLD05_HEADING_CONSUMPTION_LEDGER.csv',encoding='utf-8') as fp:
    headings=sum(1 for _ in csv.DictReader(fp))
with open(root/'06_COVERAGE/BOOK02_FROM_OLD05_CLAIM_COVERAGE.csv',encoding='utf-8') as fp:
    claims=sum(1 for _ in csv.DictReader(fp))
checks.update({'formula_rows':formulas,'heading_rows':headings,'claim_rows':claims,'formula_rows_positive':formulas>100,'heading_rows_positive':headings>100,'claim_rows_positive':claims>20})
status='PASS' if all(v for k,v in checks.items() if isinstance(v,bool)) else 'FAIL'
out={'status':status,'checks':checks}
(root/'06_COVERAGE/BOOK02_SYNTHESIS_CERT_RESULTS.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
(root/'06_COVERAGE/BOOK02_SYNTHESIS_CERT_RESULTS.txt').write_text(status+'\n'+json.dumps(checks,indent=2),encoding='utf-8')
print(status)
