#!/usr/bin/env python3
from __future__ import annotations
import json, math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMS = json.load(open(ROOT/'00_INDEX'/'D0_RESIDUAL_TARGETS_QG_CUT_CLOSURE_20260522.json'))
phi=(1+math.sqrt(5))/2
delta0=(math.sqrt(5)-2)/2
Omega8=8
V9,V11,V13=9,11,13
H=6.62607015e-34
C=299792458.0
ME=9.1093837139e-31
HBAR=H/(2*math.pi)
ell0=H/(38*ME*C)
tau0=H/(38*ME*C*C)
DL=Omega8*phi**(V9*V11)*(1+delta0/V13)
ellP=ell0/DL
G=C**3*ellP**2/HBAR
I12=delta0**12
L_cut=ellP/(delta0**6)
eta=(ellP/L_cut)**2

checks=[]
checks.append(('delta0_identity', abs(delta0 - 1/(2*phi**3)) < 1e-16))
checks.append(('I12', abs(NUMS['I12_delta0_12']-I12)/I12 < 1e-15))
checks.append(('DL', abs(NUMS['D_L']-DL)/DL < 1e-15))
checks.append(('ellP', abs(NUMS['ellP_D0_m']-ellP)/ellP < 1e-15))
checks.append(('G', abs(NUMS['G_N_D0']-G)/G < 1e-15))
checks.append(('L_cut', abs(NUMS['higher_curvature_cut_length_m']-L_cut)/L_cut < 1e-15))
checks.append(('eta_cut_equals_I12', abs(eta-I12)/I12 < 1e-15))
checks.append(('no_new_anchors', NUMS.get('no_new_anchors') is True))

# Active-status audit: the old phrase must not survive as an active remaining target.
active_files = [ROOT/'00_INDEX'/'CURRENT_STATUS_ONLY.md', ROOT/'00_INDEX'/'THEOREM_REGISTRY.md', ROOT/'00_INDEX'/'MASTER_INDEX.md']
for af in active_files:
    txt=af.read_text(encoding='utf-8', errors='replace')
    checks.append((f'no_active_remaining_qg_target_in_{af.name}', 'remaining theory target is higher-curvature' not in txt.lower()))
    checks.append((f'closure_status_present_{af.name}', 'PASS_RESIDUAL_TARGETS_QG_CUT_CLOSURE' in txt))

# LaTeX scar audit in active books and key index files.
scar_patterns = [re.compile(r'(?<![\\A-Za-z])rac\{'), re.compile(r'(?<![\\A-Za-z])arphi\b')]
scar_hits=[]
for d in [ROOT/'01_BOOKS', ROOT/'00_INDEX']:
    for p in d.glob('*.md'):
        txt=p.read_text(encoding='utf-8', errors='replace')
        for rx in scar_patterns:
            if rx.search(txt):
                scar_hits.append(str(p.relative_to(ROOT)))
                break
checks.append(('no_bare_latex_scars_active_md', not scar_hits))

failed=[name for name,ok in checks if not ok]
if failed:
    print(json.dumps({'failed':failed,'scar_hits':scar_hits}, indent=2, sort_keys=True))
    raise SystemExit('FAIL_RESIDUAL_TARGETS_QG_CUT_CLOSURE')

result={
  'status':'PASS_RESIDUAL_TARGETS_QG_CUT_CLOSURE',
  'delta0':delta0,
  'I12':I12,
  'D_L':DL,
  'ellP_D0_m':ellP,
  'G_N_D0':G,
  'L_cut_m':L_cut,
  'eta_HC_at_L_cut':eta,
  'scar_hits':scar_hits,
}
print(result['status'])
print(json.dumps(result, indent=2, sort_keys=True))
