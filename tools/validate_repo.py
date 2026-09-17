#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import csv, re, sys, collections, os

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / '02_REGISTRY'
LEAN = ROOT / '03_FORMALIZATION'
CERT = ROOT / '04_CERTIFICATES'
BOOKS = ROOT / '01_BOOKS'

errors=[]; warnings=[]

def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

def read_csv(path, required):
    try:
        with path.open(encoding='utf-8', newline='') as f:
            rows=list(csv.DictReader(f))
    except Exception as e:
        err(f'{path.relative_to(ROOT)}: CSV parse error: {e}')
        return []
    if not rows:
        err(f'{path.relative_to(ROOT)}: empty')
        return []
    missing=[x for x in required if x not in rows[0]]
    if missing: err(f'{path.relative_to(ROOT)}: missing columns {missing}')
    return rows

claims_path=REG/'claims.csv'
claims=read_csv(claims_path, ['claim_id','lean_module','lean_theorem','python_cert','release_status','notes'])
# Catch malformed quoted rows that csv.DictReader can silently merge across physical lines.
physical_claim_rows=sum(1 for line in claims_path.read_text(encoding='utf-8').splitlines() if line.startswith('D0-'))
if physical_claim_rows != len(claims):
    err(f'claims.csv: physical claim rows={physical_claim_rows} but parsed rows={len(claims)} (likely malformed CSV quoting)')
assumptions=read_csv(REG/'assumptions.csv', ['assumption_id','lean_file','claim_id','status'])
support=read_csv(REG/'formal_support.csv', ['lean_module','lean_file','role','referenced_by'])
aliases=read_csv(REG/'aliases.csv', ['legacy_id','kind','canonical_claim_id','first_reference','note'])

# IDs are unique and nonempty.
for rows,key,label in [(claims,'claim_id','claim'),(assumptions,'assumption_id','assumption')]:
    vals=[r.get(key,'').strip() for r in rows]
    dup=[k for k,v in collections.Counter(vals).items() if k and v>1]
    if any(not x for x in vals): err(f'{label}: blank {key}')
    if dup: err(f'{label}: duplicate IDs: {dup[:20]}')

claim_ids={r['claim_id'].strip() for r in claims}
assump_ids={r['assumption_id'].strip() for r in assumptions}
alias_ids={r['legacy_id'].strip() for r in aliases}

# Registry notes describe current scope, not development-session history.
process_note_re = re.compile(
    r"POST-SKEPTIC|GROUPE|RAISE\[|UPLIFT\[|\bIter\d+\b|CAMPAIGN|"
    r"\bMINT(?:ED| ORDER)?\b|PR-review|HYGIENE|\bCLOSING:|this pass|"
    r"20\d{2}-\d{2}-\d{2}|memo\.md|_LOG\.md|F4-UPGRADE-APPLIED|"
    r"FLIP APPLIED|R-A-REGISTERED|DESYNC REPAIR",
    re.I,
)
for r in claims:
    if process_note_re.search(r.get("notes", "")):
        err(f"{r['claim_id']}: process-history marker remains in notes")

# Lean roots.
root_modules=set()
def module_path(m): return LEAN / (m.replace('.','/') + '.lean')
for r in claims:
    for m in [x.strip() for x in r['lean_module'].split(';') if x.strip()]:
        p=module_path(m)
        if not p.exists(): err(f"{r['claim_id']}: missing Lean module {m}")
        else: root_modules.add(p)
for r in assumptions:
    f=r['lean_file'].strip()
    if f:
        p=LEAN/f
        if not p.exists(): err(f"{r['assumption_id']}: missing Lean file {f}")
        else: root_modules.add(p)
for r in support:
    f=r['lean_file'].strip(); p=LEAN/f
    if not p.exists(): err(f"formal_support: missing {f}")
    else: root_modules.add(p)

# All internal Lean imports resolve and all modules belong to release closure.
imp_re=re.compile(r'^import\s+([A-Za-z0-9_.]+)', re.M)
closure=set(); q=list(root_modules)
while q:
    p=q.pop()
    if p in closure or not p.exists(): continue
    closure.add(p)
    for m in imp_re.findall(p.read_text(errors='ignore')):
        if m.startswith('D0.'):
            dep=module_path(m)
            if not dep.exists(): err(f'{p.relative_to(ROOT)}: missing import {m}')
            elif dep not in closure: q.append(dep)
all_lean=set((LEAN/'D0').rglob('*.lean'))
allowed=closure | {LEAN/'D0/All.lean'}
orphans=sorted(all_lean-allowed)
if orphans: err('orphan Lean modules outside registry/support closure: '+', '.join(str(x.relative_to(LEAN)) for x in orphans[:30]))


# Certificate release-tree hygiene: proof code + immutable inputs only.
allowed_cert_dirs = {"data", "schemas", "__pycache__"}
for child in CERT.iterdir():
    if child.is_dir() and child.name not in allowed_cert_dirs:
        err(f"04_CERTIFICATES: unexpected runtime/output directory {child.name}")
    elif child.is_file() and child.suffix != ".py":
        err(f"04_CERTIFICATES: generated/non-code artifact at root {child.name}")
for name in [
    "D0_FTHEORY_LW2016_CHIRAL_RECOMBINATION_NUMBERS.json",
    "D0_FTHEORY_LW2016_CHIRAL_RECOMBINATION_RESULTS.md",
    "D0_FTHEORY_LW2016_D0_FILTER_NUMBERS.json",
    "D0_FTHEORY_LW2016_D0_FILTER_RESULTS.md",
    "hull_manifest.json",
]:
    if (ROOT / name).exists():
        err(f"generated runtime artifact escaped .build: {name}")

# Certificate refs resolve uniquely.
cert_index=collections.defaultdict(list)
for p in CERT.rglob('*.py'): cert_index[p.name].append(p)
for r in claims:
    for token in re.findall(r'[A-Za-z0-9_./-]+\.py', r['python_cert'] or ''):
        b=Path(token).name; ps=cert_index.get(b,[])
        if not ps: err(f"{r['claim_id']}: missing cert {b}")
        elif len(ps)>1: err(f"{r['claim_id']}: ambiguous cert {b}: {[str(x.relative_to(ROOT)) for x in ps]}")

# Every claim-like ID in books resolves to registry or assumptions.
id_re=re.compile(r'\bD0-[A-Z0-9][A-Z0-9._-]*-\d{3}\b')
unknown=collections.defaultdict(set)
for b in BOOKS.glob('BOOK_*.md'):
    for cid in id_re.findall(b.read_text(errors='ignore')):
        if cid not in claim_ids and cid not in assump_ids and cid not in alias_ids:
            unknown[cid].add(b.name)
if unknown:
    for cid,bs in sorted(unknown.items())[:50]: err(f'book references unknown ID {cid}: {sorted(bs)}')

# Architecture firewall: removed top-level namespaces must not be runtime paths.
legacy=['00_PUBLICATION/','00_LANGUAGE_NORMALIZATION/','03_THEORY_MAP/','04_VERIFICATION/','05_CERTS/','06_AUDIT/','08_PASSPORTS/','09_LEAN_FORMALIZATION/','_TASKS_','_QUARANTINE/']
scan_ext={'.py','.md','.json','.csv','.lean','.yml','.yaml','.toml','.txt'}

def source_files(top):
    # A relocated Lean cache legitimately retains old paths in setup metadata.
    # Inspect release sources, not dependencies, build outputs or runtime caches.
    for directory, dirs, files in os.walk(top):
        dirs[:] = [d for d in dirs if d not in {'.lake', '.build', '__pycache__'}]
        for name in files:
            yield Path(directory) / name

for top in [BOOKS,REG,CERT,LEAN,ROOT/'05_EXPERIMENTS',ROOT/'tools']:
    for p in source_files(top):
        if not p.is_file() or p.suffix.lower() not in scan_ext or p == Path(__file__).resolve(): continue
        text=p.read_text(errors='ignore')
        for old in legacy:
            if old in text:
                err(f'{p.relative_to(ROOT)} contains legacy token {old}')

print(f'claims={len(claims)} assumptions={len(assumptions)} aliases={len(aliases)} formal_support={len(support)} lean_closure={len(closure)}')
for w in warnings[:100]: print('WARN',w)
for e in errors: print('ERROR',e)
if errors:
    print(f'FAIL errors={len(errors)} warnings={len(warnings)}')
    sys.exit(1)
print(f'PASS warnings={len(warnings)}')
