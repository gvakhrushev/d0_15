#!/usr/bin/env python3
"""Source-bound native exponents, certified by dyadic integer complex balls.

Candidate search uses mpmath but the acceptance inequalities use only integers.
Uses optional gmpy2 for speed; normal Python integers give identical results.
"""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json,gzip,os
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'.deps'))
try:
 import gmpy2 as g
except ImportError:g=None
import mpmath as mp
import proper_link_targets as p
if g:
 class FastDyadic(p.Dyadic):
  def __init__(self,bits):self.bits=bits;self.scale=g.mpz(1)<<bits
  def sqrt(self,a):
   assert a[0]>=0;lo=g.isqrt(a[0]*self.scale);v=a[1]*self.scale;hi=g.isqrt(v);return lo,hi+(hi*hi<v)
 p.Dyadic=FastDyadic
z=(lambda n:g.mpz(n)) if g else int
bits=3264;prec=7168;K=23
iv=p.Interval(prec);S=iv.S;specs,banks=p.catalogue();hashbytes=lambda x:sha256(x).hexdigest();h=lambda x:hashbytes(Path(x).read_bytes())
def ballmul(x,y):
 c,s,r=x;C,T,R=y
 return ((c*C-s*T)>>prec,(c*T+s*C)>>prec,r+R+((r*R+S-1)>>prec)+2)
a,b=iv.c['sqrtp'],iv.c['p'];base=(a[0],b[0],a[1]-a[0]+b[1]-b[0]);powers=[base]
for _ in range(bits+100):powers.append(ballmul(powers[-1],powers[-1]))
def ballpower(n):
 x=(S,z(0),z(0));j=0
 while n:
  if n&1:x=ballmul(x,powers[j])
  n>>=1;j+=1
 c,s,r=x;return (c-r,c+r),(s-r,s+r)
def candidate_grid():
 x=(2**K)*mp.acos(mp.sqrt((mp.sqrt(5)-1)/2))/(2*mp.pi);p0,p1=0,1;q0,q1=1,0;n=0
 while True:
  a=int(mp.floor(x));pn=a*p1+p0;qn=a*q1+q0;n+=1
  if qn.bit_length()>=bits+32:return pn,qn,n
  p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-a)
def clip(v):
 x=max(-S,v[0]);y=min(S,v[1]);assert x<=y;return x,y
def target_digest(c,s):return hashbytes(('|'.join(hex(int(x)) for x in (*c,*s))).encode())
def error(c,s,cc,ss):return max(abs(c[0]-cc[1]),abs(c[1]-cc[0]))+max(abs(s[0]-ss[1]),abs(s[1]-ss[0]))
cache={};records=[];total_angles=0;minimum_h=None
with mp.workprec(3*bits+256):
 pn,qn,steps=candidate_grid();inv=pow(pn,-1,qn)
 def certify(c,s):
  global total_angles
  c=clip(c);s=clip(s);assert max(c[1]-c[0],s[1]-s[0])<(S>>3400)
  cm=mp.mpf(c[0]+c[1])/(2*S);sm=mp.mpf(s[0]+s[1])/(2*S);turn=(mp.atan2(sm,cm)/(2*mp.pi))%1
  target=int(mp.nint(qn*turn))%qn;k=(target*inv)%qn
  if k==0:k=qn
  nc,ns=ballpower(z(k)<<K);err=error(nc,ns,c,s);assert err<=(S>>bits),('native interval failed',total_angles)
  total_angles+=1
  return {'k':str(k),'target_sha256':target_digest(c,s),'error_numerator_hex':hex(int(err))}
 # X: first a conditional Z on arbitrary aux, then a π/2 target rotation.
 x=certify(iv.zero,iv.one);xp=certify(iv.neg(iv.one),iv.zero)
 xe=int(x['error_numerator_hex'],16)+int(xp['error_numerator_hex'],16);assert xe<=(S>>bits)
 x['phase']=xp;x['combined_X_error_numerator_hex']=hex(int(xe))
 for number,(name,spec) in enumerate(specs.items(),1):
  f=p.factor(iv,spec,cache)
  if not f['zero_boost_exact']:minimum_h=f['h'][0] if minimum_h is None else min(minimum_h,f['h'][0])
  L=p.givens(iv,f['L'],spec['type'] in ('identity','ref_rot_plus','ref_rot_minus'));R=p.givens(iv,f['R'],spec['type']=='identity');diag=p.diagonal_targets(iv,f)
  r={'family':name,'spec':spec,'zero_boost_exact':f['zero_boost_exact'],'frame_index':f.get('frame_index'),'L':[],'R':[],'diagonal':{}}
  for key,rot in (('L',L),('R',R)):
   for t in rot:
    rec={'i':t['i'],'j':t['j'],'pivot':t['selected_pivot'],'maximal_pivot_certified':t['largest_certified']};rec.update(certify(t['cos'],t['sin']));r[key].append(rec)
  # gamma+h and gamma-h are exact reciprocals, hence 00 and 11 both 1/2.
  for pattern in ((0,0),(1,0),(0,1)):
   d=diag[pattern];r['diagonal'][''.join(map(str,pattern))]=certify(d['cos'],d['sin'])
  records.append(r)
  if number%16==0:print('families certified',number,'angles',total_angles,flush=True)
inputs=[Path(__file__),P/'proper_link_targets.py',p.D/'round18/material_targets.py',p.D/'round19/julia_locality.py',p.loc.COORD_PATH,p.loc.ADDR_PATH,p.loc.B/'round25/precision_name.py',p.loc.B/'round25/targets.py',p.loc.B/'round21/REFERENCE_METADATA.json']
out={'status':'CERTIFIED_SOURCE_BOUND_PROPER_LINK_NATIVE_ROTATION_POWERS','precision_bits':prec,'controls':K,'per_macro_error_le':'2^-3264','ideal_macro_limit':101,'per_sector_error_lt':'2^-3257','target_families':len(records),'sector_entries':sum(map(len,banks.values())),'angles':total_angles,'source_sha256':{str(x):h(x) for x in inputs},'all_nonzero_boost_interval_lower_positive':True,'boost_lower_bound_hex':hex(int(minimum_h)),'all_selected_pivots_maximal_and_radius_certified':True,'candidate_grid_not_proof':{'numerator':str(pn),'denominator':str(qn),'steps':steps},'controlled_X':x,'families':records,'catalogue':banks,'literal_native_emitter_complete':False,'full_Julia_SELECT_complete':False,'GR_closed':False}
path=P/'PROPER_LINK_ANGLE_LIBRARY.json.gz'
with path.open('wb') as raw:
 with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(json.dumps(out,separators=(',',':')).encode())
print(json.dumps({'status':out['status'],'families':len(records),'angles':total_angles,'bytes':path.stat().st_size,'sectors':out['sector_entries']}),flush=True)
