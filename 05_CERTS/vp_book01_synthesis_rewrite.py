
from pathlib import Path
import csv, re, json
root = Path(__file__).resolve().parents[1]
book = (root/'01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md').read_text(encoding='utf-8')
claims = list(csv.DictReader(open(root/'06_COVERAGE/BOOK01_CLAIM_COVERAGE.csv', encoding='utf-8')))
formulas = list(csv.DictReader(open(root/'06_COVERAGE/BOOK01_FORMULA_COVERAGE_LEDGER.csv', encoding='utf-8')))
headings = list(csv.DictReader(open(root/'06_COVERAGE/BOOK01_HEADING_CONSUMPTION_LEDGER.csv', encoding='utf-8')))
required_terms = ['S_{D0}', 'M^{D0}', 'R_N', 'x^2=x+1', '\\delta_0', '\\Omega_8', 'K(9,11,13)', 'J_{scene}', 'c_{D0}', 'q_{mass}', 'I_B', '\\pi_0']
missing_claims = [c['ID'] for c in claims if c['ID'] not in book]
missing_terms = [t for t in required_terms if t not in book]
classes = sorted(set(f['class'] for f in formulas))
# all formulas are represented by id in appendix, rather than exact string after escaping
missing_formula_ids = [f['formula_id'] for f in formulas if f['formula_id'] not in book]
result = {
  'book': 'BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md',
  'claims_total': len(claims),
  'missing_claims': missing_claims,
  'legacy_formulas_total': len(formulas),
  'missing_formula_ids': missing_formula_ids[:20],
  'missing_formula_id_count': len(missing_formula_ids),
  'legacy_headings_total': len(headings),
  'formula_classes': classes,
  'missing_required_terms': missing_terms,
  'status': 'PASS' if not missing_claims and not missing_terms and not missing_formula_ids else 'FAIL'
}
out = root/'06_COVERAGE/BOOK01_SYNTHESIS_CERT_RESULTS.json'
out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(result, indent=2, ensure_ascii=False))
if result['status'] != 'PASS':
    raise SystemExit(1)
