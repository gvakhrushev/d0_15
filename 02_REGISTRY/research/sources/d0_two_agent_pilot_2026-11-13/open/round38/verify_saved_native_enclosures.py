#!/usr/bin/env python3
"""Show every stored native interval contains an independent tighter ball."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import json
p=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round18/MATERIAL_PREPARATION_LIBRARY.json');lib=json.loads(p.read_text());digest=sha256(p.read_bytes()).hexdigest();bits=15744;S=1<<bits;shift=lib['precision_bits']-bits;assert shift>0;scale=1<<shift
r=isqrt(5*S*S);pi=((r-S)//2,(r+2-S)//2);a=(isqrt(pi[0]*S),isqrt(pi[1]*S)+1)
def mul(x,y):
 c,s,r=x;d,t,u=y
 return (c*d-s*t)//S,(c*t+s*d)//S,r+u-((-r*u)//S)+2
checked=0;minmargin=None
for aid,z in lib['angles'].items():
 e=8192*int(z['k']);acc=(S,0,0);base=(a[0],pi[0],a[1]-a[0]+pi[1]-pi[0])
 while e:
  if e&1:acc=mul(acc,base)
  e>>=1
  if e:base=mul(base,base)
 for center,name in [(acc[0],'native_cos_hex'),(acc[1],'native_sin_hex')]:
  lo,hi=[int(x,16) for x in z[name]]
  ml=(center-acc[2])*scale-lo;mr=hi-(center+acc[2])*scale
  assert ml>=0 and mr>=0,(aid,name);minmargin=min(ml,mr) if minmargin is None else min(minmargin,ml,mr)
 checked+=1
 if checked%4==0:print('saved native enclosures verified',checked,'of',len(lib['angles']),flush=True)
assert checked==38 and sha256(p.read_bytes()).hexdigest()==digest
out={'status':'PASS_ALL_SAVED_NATIVE_INTERVALS_CONTAIN_INDEPENDENT_BALL','library_sha256':digest,'independent_precision_bits':bits,'library_precision_bits':lib['precision_bits'],'angles_verified':checked,'each_saved_cos_sin_contains_independent_true_value_ball':True,'min_containment_margin_nonnegative':minmargin>=0,'proof':'integer Euclidean complex ball; |z_true|=1; radius r1+r2+ceil(r1*r2/S)+2','source_builder_reexecuted':False,'GR_closed':False}
Path(__file__).with_name('SAVED_NATIVE_INTERVALS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
