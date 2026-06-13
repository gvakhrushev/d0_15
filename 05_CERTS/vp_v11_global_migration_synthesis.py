from pathlib import Path
import csv, json, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
books=list(csv.DictReader((ROOT/'07_GLOBAL_AUDIT'/'V11_ACTIVE_BOOKS_MANIFEST.csv').open(encoding='utf-8')))
summary=list(csv.DictReader((ROOT/'07_GLOBAL_AUDIT'/'V11_GLOBAL_BOOK_MIGRATION_SUMMARY.csv').open(encoding='utf-8')))
combined=(ROOT/'01_BOOKS'/'03_COMBINED'/'D0_V11_10_FULL_CANONICAL_BOOKS.md').read_text(encoding='utf-8')
if len(books)!=9: errors.append('expected 9 active books')
if len(summary)!=9: errors.append('expected 9 migration summary rows')
for r in summary:
    for k in ['heading_rows','formula_rows','claim_rows']:
        if r[k] in ('','None'):
            errors.append(f'missing {k} for {r["legacy_book"]}')
        else:
            try:
                if int(r[k]) < 0: errors.append(f'negative {k} for {r["legacy_book"]}')
            except Exception:
                errors.append(f'bad integer {k} for {r["legacy_book"]}: {r[k]}')
for row in books:
    p=ROOT/'01_BOOKS'/row['file']
    if not p.exists(): errors.append('missing active book '+row['file'])
    else:
        title=p.read_text(encoding='utf-8').splitlines()[0]
        if title not in combined: errors.append('combined missing title '+title)
for needed in ['BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md','D0_V11_10_FULL_CANONICAL_BOOKS.md','V11_GLOBAL_MIGRATION_AND_SYNTHESIS_AUDIT.md']:
    if not any(p.name==needed for p in ROOT.rglob('*')):
        errors.append('missing artifact '+needed)
result={'status':'PASS' if not errors else 'FAIL','active_books':len(books),'migration_rows':len(summary),'combined_chars':len(combined),'errors':errors[:50]}
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors: sys.exit(1)
