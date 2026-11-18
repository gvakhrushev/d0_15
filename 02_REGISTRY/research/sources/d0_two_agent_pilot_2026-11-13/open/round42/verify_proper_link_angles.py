#!/usr/bin/env python3
"""Independent high-precision replay of every source-bound native exponent.

Reconstructs names and targets at two scales, re-powers each saved exponent
at 8448 bits, checks all certified errors, and verifies the original pins.
No candidate-grid or mpmath result is trusted or imported.
"""
from pathlib import Path
from hashlib import sha256
import sys,json,gzip
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'.deps'))
try:import gmpy2 as g
except ImportError:g=None
import proper_link_targets as p
if g:
 class FastDyadic(p.Dyadic):
  def __init__(self,bits):self.bits=bits;self.scale=g.mpz(1)<<bits
  def sqrt(self,a):
   assert a[0]>=0;lo=g.isqrt(a[0]*self.scale);v=a[1]*self.scale;hi=g.isqrt(v);return lo,hi+(hi*hi<v)
 p.Dyadic=FastDyadic
with gzip.open(P/'PROPER_LINK_ANGLE_LIBRARY.json.gz','rt') as f:j=json.load(f)
for f,h in j['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h
specs,banks=p.catalogue();assert banks==j['catalogue'];orig=p.Interval(7168);iv=p.Interval(8448);S=iv.S;shift=8448-7168;scale=1<<shift;K=23
# Independent Euclidean-ball recurrence. Exact complex targets have modulus
# one. Multiplication rounds each centre coordinate downward by <1 ulp.
def product(x,y):
 c,s,r=x;C,T,R=y
 return ((c*C-s*T)>>8448,(c*T+s*C)>>8448,r+R+((r*R+S-1)>>8448)+2)
a,b=iv.c['sqrtp'],iv.c['p'];powers=[(a[0],b[0],a[1]-a[0]+b[1]-b[0])]
for _ in range(3364):powers.append(product(powers[-1],powers[-1]))
def power(n):
 acc=(S,0,0);i=0
 while n:
  if n&1:acc=product(acc,powers[i])
  n//=2;i+=1
 c,s,r=acc;return (c-r,c+r),(s-r,s+r)
def clip(scale0,x):return max(-scale0,x[0]),min(scale0,x[1])
def digest(c,s):return sha256(('|'.join(hex(int(v)) for v in (*c,*s))).encode()).hexdigest()
def err(c,s,tc,ts):return max(abs(c[0]-tc[1]),abs(c[1]-tc[0]))+max(abs(s[0]-ts[1]),abs(s[1]-ts[0]))
def verify(rec,cc,ss,C,T):
 cc=clip(orig.S,cc);ss=clip(orig.S,ss);C=clip(S,C);T=clip(S,T)
 assert digest(cc,ss)==rec['target_sha256']
 for small,big in ((cc,C),(ss,T)):assert small[0]*scale<=big[0] and big[1]<=small[1]*scale
 c,s=power(int(rec['k'])<<K);e=err(c,s,C,T);assert e<=S>>3264
 assert e<=int(rec['error_numerator_hex'],16)*scale
cache1={};cache2={};total=0
for index,r in enumerate(j['families'],1):
 name=r['family'];spec=specs[name];assert r['spec']==json.loads(json.dumps(spec))
 f=p.factor(orig,spec,cache1);F=p.factor(iv,spec,cache2)
 for key in ('L','R'):
  identity=spec['type']=='identity' or key=='L' and spec['type'] in ('ref_rot_plus','ref_rot_minus')
  a=p.givens(orig,f[key],identity);b=p.givens(iv,F[key],identity);assert len(a)==len(b)==len(r[key])
  for rec,x,y in zip(r[key],a,b):
   assert (rec['i'],rec['j'],rec['pivot'])==(x['i'],x['j'],x['selected_pivot'])==(y['i'],y['j'],y['selected_pivot']) and rec['maximal_pivot_certified'] and x['largest_certified'] and y['largest_certified']
   verify(rec,x['cos'],x['sin'],y['cos'],y['sin']);total+=1
 a=p.diagonal_targets(orig,f);b=p.diagonal_targets(iv,F)
 for key,pat in [('00',(0,0)),('10',(1,0)),('01',(0,1))]:
  verify(r['diagonal'][key],a[pat]['cos'],a[pat]['sin'],b[pat]['cos'],b[pat]['sin']);total+=1
 if index%40==0:print('independent high-precision families',index,'angles',total,flush=True)
x=j['controlled_X'];verify(x,orig.zero,orig.one,iv.zero,iv.one);total+=1
verify(x['phase'],orig.neg(orig.one),orig.zero,iv.neg(iv.one),iv.zero);total+=1
c,s=power(int(x['phase']['k'])<<K);phase=err(c,s,iv.neg(iv.one),iv.zero)
c,s=power(int(x['k'])<<K);rot=err(c,s,iv.zero,iv.one);assert phase+rot<=S>>3264
assert total==j['angles'] and len(j['families'])==336
out={'status':'PASS_ALL_INDEPENDENT_HIGH_PRECISION_NATIVE_POWERS','library_sha256':sha256((P/'PROPER_LINK_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest(),'original_bits':7168,'replay_bits':8448,'families':len(j['families']),'angles':total,'all_original_target_hashes_and_pins_match':True,'all_original_target_intervals_contain_replay':True,'all_native_error_bounds_hold':True,'controlled_X_combined_error_le':'2^-3264','candidate_grid_used':False,'GR_closed':False}
(P/'INDEPENDENT_PROPER_LINK_ANGLES.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
