#!/usr/bin/env python3
"""Lazy complete two-bit proper-link G/CX/SourceI emitter; no giant repeats expanded."""
from pathlib import Path
from functools import lru_cache
from hashlib import sha256
from itertools import islice
import sys,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));sys.path.insert(0,str(P.parent/'round42'))
import proper_link_two_bit_targets as target
import proper_link_native as old
D=target.base.D;sys.path.insert(0,str(D/'round41'))
import sam_only_compiler as a41
GRID=json.loads((P/'SHORT_GRID_CERTIFICATE.json').read_text());Q=int(GRID['denominator_hex'],16);PN=int(GRID['numerator_hex'],16);INV=pow(PN,-1,Q)
PREC=4096;COMMON=29
@lru_cache(maxsize=2)
def constants(bits=PREC):
 iv=target.Interval(bits);ctx=a41.e.Dyadic(bits)
 return iv,ctx

def power_for(c,s,bits=PREC):
 """Outward atan2, exact modular grid selection, strict universal error."""
 iv,ctx=constants(bits);S=ctx.S
 c=(max(-S,int(c[0])),min(S,int(c[1])));s=(max(-S,int(s[0])),min(S,int(s[1])))
 low=lambda x:0 if x[0]<=0<=x[1] else min(abs(x[0]),abs(x[1]))
 # Select a dominant nonzero component. |minor/major|<2 even on ties.
 cosine=low(c)>=low(s);major,minor=(c,s) if cosine else (s,c)
 assert low(major)*10>6*S
 if major[1]<0:major=ctx.neg(major);minor=ctx.neg(minor);negative=True
 else:assert major[0]>0;negative=False
 r=ctx.div(minor,major);assert -2*S<r[0]<=r[1]<2*S
 # One exact half-angle reduction handles ratios up to two.
 r2=ctx.mul(r,r);half=ctx.div(r,ctx.add(ctx.rat(1),ctx.sqrt(ctx.add(ctx.rat(1),r2))))
 angle=(2*a41.atan_signed(ctx,half[0])[0],2*a41.atan_signed(ctx,half[1])[1])
 pi=iv.c['pi'];pi=(int(pi[0]),int(pi[1]));halfpi=(pi[0]//2,-((-pi[1])//2))
 if cosine:
  if negative:angle=ctx.add(pi,angle)
 else:
  angle=ctx.add(ctx.neg(halfpi) if negative else halfpi,ctx.neg(angle))
 tau=ctx.div(angle,(2*pi[0],2*pi[1]))
 if 2*Q*(tau[1]-tau[0])>S:raise a41.e.NeedPrecision()
 j=(Q*(tau[0]+tau[1])+S)//(2*S);k=(j*INV)%Q
 return k or Q

def fixed_and_catalogue():return target.catalogue()
@lru_cache(maxsize=64)
def family(name):
 specs,_=fixed_and_catalogue()
 if name.startswith('v_'):
  _,xy,digits=name.split('_');xy=None if xy=='none' else (int(xy[0]),int(xy[1]))
  assert len(digits)==6 and all(x in '0123' for x in digits)
  spec={'type':'f','xy':xy,'bits':tuple(map(int,digits))}
 else:spec=specs[name]
 bits=PREC
 while True:
  try:return family_at_precision(name,spec,bits)
  except a41.e.NeedPrecision:bits*=2

def family_at_precision(name,spec,bits):
 iv,_=constants(bits);f=target.base.factor(iv,spec,{})
 result={'family':name,'L':[],'R':[],'diagonal':{}}
 for label in ('L','R'):
  identity=spec['type']=='identity' or label=='L' and spec['type'] in ('ref_rot_plus','ref_rot_minus')
  for r in target.base.givens(iv,f[label],identity):
   result[label].append({'i':r['i'],'j':r['j'],'k':str(power_for(r['cos'],r['sin'],bits))})
 for key,d in target.base.diagonal_targets(iv,f).items():
  if key==(1,1):continue
  result['diagonal'][''.join(map(str,key))]={'k':str(power_for(d['cos'],d['sin'],bits))}
 return result
@lru_cache(maxsize=1)
def controlled_x():
 iv,_=constants();return {'k':str(power_for(iv.zero,iv.one)),'phase':{'k':str(power_for(iv.neg(iv.one),iv.zero))}}

def bind(global_lay,entry):
 assert len(global_lay['all_SAM'])==5376
 return old.bind_global(global_lay,entry)
def sector_blocks(global_lay,entry,reverse=False):
 lay=bind(global_lay,entry)
 yield from old.sector_blocks(lay,entry,family(entry['family_id']),controlled_x(),common_controls=COMMON,reverse=reverse)
def bank_entries(bank,reverse=False):
 """Family-major order, reducing repeated angle synthesis; exact inverse order."""
 from itertools import product
 _,cat=fixed_and_catalogue();section=cat[bank]
 groups={}
 for row in section['variable']:
  xy=None if row['xy'] is None else tuple(row['xy']);groups.setdefault(xy,[]).append(row)
 keys=list(groups);digitlist=list(product(range(4),repeat=6))
 if not reverse:
  yield from section['fixed']
 for xy in (reversed(keys) if reverse else keys):
  for digits in (reversed(digitlist) if reverse else digitlist):
   for row in (reversed(groups[xy]) if reverse else groups[xy]):
    ids=row['indices_by_generator']
    yield {'address':row['address'],'SAM_indices':ids+[2688+i for i in ids],
     'SAM_pattern':[d&1 for d in digits]+[(d>>1)&1 for d in digits],
     'family_id':target.family_id(xy,digits)}
 if reverse:
  yield from reversed(section['fixed'])

def bank_blocks(bank,global_lay,reverse=False):
 for entry in bank_entries(bank,reverse):yield from sector_blocks(global_lay,entry,reverse)

def sector_cost(global_lay,entry,reverse=False):
 return old.sector_cost(bind(global_lay,entry),entry,family(entry['family_id']),controlled_x(),common_controls=COMMON,reverse=reverse)
