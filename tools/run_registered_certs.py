#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse,csv,re,subprocess,sys,collections,os

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'02_REGISTRY/claims.csv'
CERT=ROOT/'04_CERTIFICATES'

parser=argparse.ArgumentParser()
parser.add_argument('--workers',type=int,default=6)
parser.add_argument('--timeout',type=int,default=30)
parser.add_argument('--limit',type=int,default=0)
parser.add_argument('--offset',type=int,default=0)
parser.add_argument('--exclude',action='append',default=[],help='certificate basename or substring to exclude; repeatable')
args=parser.parse_args()

rows=list(csv.DictReader(REG.open(encoding='utf-8',newline='')))
idx=collections.defaultdict(list)
for p in CERT.rglob('*.py'): idx[p.name].append(p)
claims_by_cert=collections.defaultdict(set)
release_by_claim={r['claim_id']:r.get('release_status','') for r in rows}
for r in rows:
    for x in re.findall(r'[A-Za-z0-9_./-]+\.py',r.get('python_cert','')):
        claims_by_cert[Path(x).name].add(r['claim_id'])
items=[]; missing=[]
for name,cids in sorted(claims_by_cert.items()):
    ps=idx.get(name,[])
    if len(ps)!=1:
        missing.append((name,len(ps))); continue
    items.append((name,ps[0],sorted(cids)))
if args.exclude:
    items=[x for x in items if not any(pat in x[0] for pat in args.exclude)]
items=items[args.offset:]
if args.limit: items=items[:args.limit]
if missing:
    for x in missing: print('MISSING_OR_AMBIGUOUS',x)
    sys.exit(2)

def run(item):
    name,p,cids=item
    try:
        cp=subprocess.run([sys.executable,str(p)],cwd=ROOT,text=True,capture_output=True,timeout=args.timeout,env={**os.environ,'PYTHONHASHSEED':'0'})
        out=(cp.stdout or '')+'\n'+(cp.stderr or '')
        up=out.upper()
        if cp.returncode==0:
            status='PASS'
        elif 'HONEST-OPEN' in up or 'HONEST_OPEN' in up:
            status='OPEN'
        elif any(tok in up for tok in ['SKIP','EXTERNAL_DATA_REQUIRED','EXTERNAL DATA REQUIRED','ASTROPY_REQUIRED','REQUIRES ASTROPY','DATA NOT FOUND','MISSING EXTERNAL','MISSING PINNED INPUT']):
            status='SKIP'
        else:
            status='FAIL'
        return name,status,cp.returncode,cids,out[-4000:]
    except subprocess.TimeoutExpired as e:
        out=((e.stdout or '') if isinstance(e.stdout,str) else '')+'\n'+((e.stderr or '') if isinstance(e.stderr,str) else '')
        return name,'TIMEOUT',124,cids,out[-4000:]

results=[]
with ThreadPoolExecutor(max_workers=args.workers) as ex:
    futs={ex.submit(run,x):x for x in items}
    for i,f in enumerate(as_completed(futs),1):
        r=f.result();results.append(r)
        if r[1] not in {'PASS','SKIP','OPEN'}:
            print(f'{r[1]:7} {r[0]} rc={r[2]} claims={";".join(r[3])}\n{r[4]}')

cnt=collections.Counter(r[1] for r in results)
print('SUMMARY',dict(cnt),'total',len(results))
# machine-readable result in .build only
outdir=ROOT/'.build';outdir.mkdir(exist_ok=True)
with (outdir/'cert_results.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['cert','status','returncode','claims','tail'])
    for name,status,rc,cids,out in sorted(results): w.writerow([name,status,rc,';'.join(cids),out])
if cnt['FAIL'] or cnt['TIMEOUT']:
    sys.exit(1)
