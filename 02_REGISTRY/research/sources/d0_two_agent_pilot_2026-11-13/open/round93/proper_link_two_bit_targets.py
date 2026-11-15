#!/usr/bin/env python3
"""Four-valued A47 chart, actual B25 proper-link targets and lazy catalogue."""
from pathlib import Path
from itertools import product
import sys
P=Path(__file__).resolve().parent;B=P.parent
sys.path.insert(0,str(B/'round42'))
import proper_link_targets as base
try:
 sys.path.insert(0,str(B/'round42/.deps'));import gmpy2 as g
 class FastDyadic(base.Dyadic):
  def __init__(self,bits):self.bits=bits;self.scale=g.mpz(1)<<bits
  def sqrt(self,a):
   assert a[0]>=0;lo=g.isqrt(a[0]*self.scale);v=a[1]*self.scale;hi=g.isqrt(v);return lo,hi+(hi*hi<v)
 base.Dyadic=FastDyadic
except ImportError:pass
class Interval(base.Interval):
 def exp_theta(self,digits):
  assert len(digits)==6 and all(type(d) is int and 0<=d<4 for d in digits)
  eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]]
  theta=[[self.zero for _ in range(4)] for _ in range(4)];p2=self.square(self.c['p'])
  for (i,j),digit in zip(base.GEN,digits):
   d=self.mul(self.R(1,2**80),self.sub(self.R(digit),self.scalar(p2,3)))
   for k in range(4):
    if eta[k][i]:theta[k][j]=self.add(theta[k][j],self.scalar(d,eta[k][i]))
    if eta[k][j]:theta[k][i]=self.sub(theta[k][i],self.scalar(d,eta[k][j]))
  term=self.eye(4);out=term;fact=1;n=0
  # Each |digit-3p²|<3; row sum is <18*2^-80 <2^-75.
  while True:
   n+=1;fact*=n;term=self.mscale(self.mm(term,theta),self.R(1,n));out=self.madd(out,term)
   if 75*(n+1)+(fact*(n+1)).bit_length()-1>=self.bits+18:break
  return [[(v[0]-1,v[1]+1) for v in row] for row in out],n

def catalogue():
 """Return fixed entries and factorized variable templates, not million rows."""
 specs,banks=base.catalogue();out={};vary=[]
 for bank,entries in banks.items():
  fixed=[];groups={}
  for entry in entries:
   spec=specs[entry['family_id']];ids=entry['SAM_indices']
   if spec['type']=='f' and spec['bits'] is not None:
    assert bank=='f' and len(ids)==6
    key=(entry['address'],tuple(ids),str(spec['xy']))
    group=groups.setdefault(key,{'address':entry['address'],'indices':list(ids),'xy':spec['xy'],'patterns':set()})
    group['patterns'].add(tuple(entry['SAM_pattern']))
   else:fixed.append(entry)
  for group in groups.values():
   assert group.pop('patterns')==set(product((0,1),repeat=6))
   gens=[tuple(base.loc.COORD[i]['generator']) for i in group['indices']]
   assert set(gens)==set(base.GEN)
   group['indices_by_generator']=[group['indices'][gens.index(g)] for g in base.GEN]
  out[bank]={'fixed':fixed,'variable':list(groups.values())}
 assert len(specs)==336
 return specs,out

def entries(bank,cat):
 for row in cat[bank]['fixed']:yield row
 for group in cat[bank]['variable']:
  ids=group['indices_by_generator']
  for digits in product(range(4),repeat=6):
   yield {'address':group['address'],'SAM_indices':ids+[2688+i for i in ids],
    'SAM_pattern':[d&1 for d in digits]+[(d>>1)&1 for d in digits],
    'family_id':family_id(group['xy'],digits)}
def family_id(xy,digits):
 xykey='none' if xy is None else ''.join(str(i) for i in xy)
 return 'v_'+xykey+'_'+''.join(map(str,digits))
def variable_specs():
 for xy in (None,(1,1),(1,2),(2,1),(2,2)):
  for digits in product(range(4),repeat=6):yield family_id(xy,digits),{'type':'f','xy':xy,'bits':digits}
