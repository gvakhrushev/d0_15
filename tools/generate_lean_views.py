#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,csv

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'02_REGISTRY'
LEAN=ROOT/'03_FORMALIZATION'
ALL=LEAN/'D0/All.lean'
CLAIMMAP=LEAN/'D0/TheoremLedger/ClaimMap.lean'

def rows(name):
    with (REG/name).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))

def module_from_file(f:str)->str:
    s=f.strip()
    if s.endswith('.lean'): s=s[:-5]
    return s.replace('/','.')

def esc(s:str)->str:
    return s.replace('\\','\\\\').replace('"','\\"').replace('\n',' ')

def claim_status(r):
    ls=r.get('lean_status','').strip()
    rs=r.get('release_status','').strip()
    bridge=r.get('uses_bridge_assumptions','').strip().lower()=='true' or 'BRIDGE' in ls
    if ls=='DEPRECATED' or rs=='DEPRECATED': return 'deprecated'
    if not r.get('lean_module','').strip(): return 'notInLeanScope'
    if rs in {'NO-GO','NO_GO_PROVED'}: return 'leanNoGoProved' if ls.startswith('LEAN_') else 'pythonCertClosed'
    if bridge: return 'leanBridgeAssumptionsExplicit'
    if ls=='LEAN_PROVED': return 'leanCoreProved'
    if ls=='PYTHON_CERTIFIED': return 'pythonCertClosed'
    if rs=='EMPIRICAL-PASSPORT': return 'empiricalDataRequired'
    if ls=='OPEN' or rs=='PROOF-TARGET': return 'openObligation'
    return 'pythonCertRequired'

def render_all():
    mods=set()
    for r in rows('claims.csv'):
        mods.update(x.strip() for x in r.get('lean_module','').split(';') if x.strip())
    for r in rows('assumptions.csv'):
        f=r.get('lean_file','').strip()
        if f: mods.add(module_from_file(f))
    for r in rows('formal_support.csv'):
        m=r.get('lean_module','').strip()
        if m: mods.add(m)
    body=['-- AUTO-GENERATED from 02_REGISTRY/{claims,assumptions,formal_support}.csv.',
          '-- Release proof roots only; support imports are transitive.', '']
    body += [f'import {m}' for m in sorted(mods)]
    body += ['']
    return '\n'.join(body)

def render_claimmap():
    cr=rows('claims.csv')
    body=['-- AUTO-GENERATED from 02_REGISTRY/claims.csv by tools/generate_lean_views.py.',
          '-- Do not edit by hand; run `python tools/generate_lean_views.py`.', '',
          'namespace D0','',
          'inductive ClaimStatus where',
          '  | leanCoreProved','  | leanBridgeAssumptionsExplicit','  | pythonCertRequired',
          '  | pythonCertClosed','  | empiricalDataRequired','  | leanNoGoProved',
          '  | openObligation','  | deprecated','  | notInLeanScope',
          '  deriving DecidableEq, Repr','',
          'structure ClaimMapEntry where','  claimId : String','  moduleName : String',
          '  theoremName : String','  status : ClaimStatus','',
          'def claimMap : List ClaimMapEntry :=','  [']
    entries=[]
    for r in cr:
        m=r.get('lean_module','').strip()
        if not m: continue
        entries.append(
          f'    {{ claimId := "{esc(r["claim_id"])}", moduleName := "{esc(m)}",\n'
          f'      theoremName := "{esc(r.get("lean_theorem", "").strip())}", status := ClaimStatus.{claim_status(r)} }}')
    body.append(',\n'.join(entries))
    body += ['  ]','',
             'theorem claimMap_nonempty : claimMap ≠ [] := by',
             '  intro h',
             '  cases h',
             '',
             'end D0','']
    return '\n'.join(body)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); a=ap.parse_args()
    wanted={ALL:render_all(),CLAIMMAP:render_claimmap()}
    stale=[]
    for p,text in wanted.items():
        old=p.read_text(encoding='utf-8') if p.exists() else ''
        if old!=text:
            stale.append(p)
            if not a.check:
                p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
    if a.check and stale:
        for p in stale: print('STALE',p.relative_to(ROOT))
        raise SystemExit(1)
    print(('PASS' if a.check else 'UPDATED'), 'lean_views', 'stale=0' if a.check else f'files={len(stale)}')
if __name__=='__main__': main()
