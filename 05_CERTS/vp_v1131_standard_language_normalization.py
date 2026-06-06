#!/usr/bin/env python3
from pathlib import Path
import csv, json
root=Path(__file__).resolve().parents[1]
books=root/'01_BOOKS'
rosetta=root/'00_LANGUAGE_NORMALIZATION'/'D0_STANDARD_LANGUAGE_ROSETTA.csv'
assert rosetta.exists(), 'Rosetta CSV missing'
rows=list(csv.DictReader(rosetta.open(encoding='utf-8')))
assert len(rows)>=15, 'Rosetta too small'
required_terms=['archive','forgetting','terminal-destructive readout','witness','tick','scene','passport','carrier','stiffness','ambient-Hom leakage','ABCD']
rosetta_text=rosetta.read_text(encoding='utf-8')
for t in required_terms: assert t in rosetta_text, f'missing term {t}'
book_results=[]
for p in sorted(books.glob('BOOK_*.md')):
    txt=p.read_text(encoding='utf-8'); head=txt[:4500]
    has_standard=('Standard-language' in head or 'Standard reading' in head or 'Standard proof-language' in head)
    anchors=['conditional expectation','partial trace','positive operator','profinite','condensed','external comparison','finite incidence','spectral geometry','EFT','coarse-graining','representation carrier','POVM']
    anchor_hits=[a for a in anchors if a in head or a in txt[:10000]]
    book_results.append({'book':p.name,'has_standard_section':has_standard,'anchor_hits':anchor_hits})
    assert has_standard, f'{p.name} lacks standard-language section'
    assert anchor_hits, f'{p.name} lacks external anchor terms'
combined=books/'03_COMBINED'/'D0_V11_31_FULL_CANONICAL_BOOKS_ACTIVE.md'
assert combined.exists(), 'combined v11.31 missing'
ctxt=combined.read_text(encoding='utf-8')
assert 'Standard-language protocol' in ctxt
assert 'admissible subfunctor' in ctxt
out={'status':'PASS_V11_31_STANDARD_LANGUAGE_NORMALIZATION','book_results':book_results,'rosetta_terms':len(rows)}
(root/'05_CERTS'/'vp_v1131_standard_language_normalization.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
(root/'05_CERTS'/'vp_v1131_standard_language_normalization.md').write_text('# v11.31 Standard-language normalization cert\n\n```text\nPASS_V11_31_STANDARD_LANGUAGE_NORMALIZATION\n```\n\nAll active books contain a standard-language normalization section and the Rosetta table is present.\n',encoding='utf-8')
print('PASS_V11_31_STANDARD_LANGUAGE_NORMALIZATION')
