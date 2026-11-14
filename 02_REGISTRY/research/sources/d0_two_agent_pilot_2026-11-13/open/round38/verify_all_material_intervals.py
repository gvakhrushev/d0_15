#!/usr/bin/env python3
"""Independent exact outward interval checks of all A18 target/native angles.

Uses 8448 bits and independent arithmetic rather than rerunning A18 builder or
calling the owned _rotation_intervals.  It reads the finished library only.
"""
from pathlib import Path
from hashlib import sha256
from math import isqrt
from fractions import Fraction
import json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open');p=D/'round18/MATERIAL_PREPARATION_LIBRARY.json';assert p.exists(),'await completed A18 library'
lib=json.loads(p.read_text());digest=sha256(p.read_bytes()).hexdigest();bits=8448;S=1<<bits
class I:
 def q(self,n,d=1):assert d>0;return n*S//d,-((-n*S)//d)
 def add(self,x,y):return x[0]+y[0],x[1]+y[1]
 def neg(self,x):return -x[1],-x[0]
 def sub(self,x,y):return self.add(x,self.neg(y))
 def mul(self,x,y):
  z=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(z)//S,-((-max(z))//S)
 def div(self,x,y):
  assert y[0]>0
  lo=min(a*S//b for a in x for b in y);hi=max(-((-a*S)//b) for a in x for b in y);return lo,hi
 def sqrt(self,x):
  assert x[0]>=0
  l=isqrt(x[0]*S);u=isqrt(x[1]*S)
  return l,u+(u*u<x[1]*S)
 def pow(self,x,n):
  z=self.q(1)
  for _ in range(n):z=self.mul(z,x)
  return z
 def atan_recip(self,q):
  total=(0,0);power=q;j=0
  while True:
   z=self.q(1,(2*j+1)*power);total=self.add(total,z if j%2==0 else self.neg(z));j+=1;power*=q*q
   den=(2*j+1)*power
   if den>S:
    e=self.q(1,den)[1];return total[0]-e,total[1]+e
 def pi(self):return self.sub(self.mul(self.q(16),self.atan_recip(5)),self.mul(self.q(4),self.atan_recip(239)))
I=I();Q=I.q;one=Q(1);p0=I.div(I.sub(I.sqrt(Q(5)),one),Q(2));a=I.sqrt(p0);z=Q(1,2**20);L=I.mul(Q(4),I.pow(p0,3));p6=I.pow(p0,6);R=I.sub(one,I.mul(I.mul(z,L),I.add(one,p6)));Qv=I.sub(one,I.mul(z,L));k0=I.mul(I.div(Q(2),I.pow(p0,5)),I.add(I.div(R,Qv),p6));meta=json.loads((O/'round21/REFERENCE_METADATA.json').read_text());Fh=Fraction(meta['F_h_rational']);ref=I.div(I.sqrt(I.div(Q(Fh.numerator,Fh.denominator),k0)),Q(8));phys=I.div(I.pi(),I.mul(Q(200),I.sqrt(Q(2))));den=I.sqrt(I.mul(Q(2),I.add(one,a)))
def own_target(spec):
 if spec['kind']=='q':
  x=spec['x0'];psi=[I.mul(Q((1,0,-1,0)[x]),phys),I.mul(Q((0,1,0,-1)[x]),phys)]
  if spec['bits'] is not None:psi=[I.add(psi[j],I.mul(Q(1,2**30),I.sub(Q(spec['bits'][j]),I.pow(p0,2)))) for j in range(2)]
 else:psi=[I.mul(Q(spec['sign']),ref),Q(0)]
 slack=I.sub(I.sub(one,p0),I.add(I.pow(psi[0],2),I.pow(psi[1],2)));assert slack[0]>0
 v={1:I.div(I.add(one,a),den),14:I.div(I.sqrt(slack),den),0:I.div(psi[0],den),15:I.div(psi[1],den)}
 r1=I.sqrt(I.add(I.pow(v[1],2),I.add(I.pow(v[0],2),I.pow(v[15],2))));r2=I.sqrt(I.add(I.pow(v[1],2),I.pow(v[15],2)))
 return v,[(r1,v[14]),(I.div(r2,r1),I.div(v[0],r1)),(I.div(v[1],r2),I.div(v[15],r2))]
def ballmul(x,y):
 # Each exact factor is a power of G and has complex modulus 1.  If centres
 # have Euclidean errors <=r1/S,r2/S, then the product error is bounded by
 # (r1+r2+ceil(r1*r2/S)+2)/S; the final 2 covers both coordinate roundings.
 # This disk bound avoids exponential rectangle dependency inflation.
 xc,xs,xr=x;yc,ys,yr=y
 cc=(xc*yc-xs*ys)//S;ss=(xc*ys+xs*yc)//S
 radius=xr+yr-((-xr*yr)//S)+2
 return cc,ss,radius

def native_power(k):
 exponent=8192*k;acc=(S,0,0);base=(a[0],p0[0],(a[1]-a[0])+(p0[1]-p0[0]))
 while exponent:
  if exponent&1:acc=ballmul(acc,base)
  exponent>>=1
  if exponent:base=ballmul(base,base)
 c,s,r=acc
 return (c-r,c+r),(s-r,s+r)
assert lib['precision_bits']>bits;factor=1<<(lib['precision_bits']-bits);angles=lib['angles'];bounds={};progress=0
for aid,x in angles.items():
 k=int(x['k']);assert k>0 and x['native_exponent_multiplier']==8192 and x['denominator_power_of_two']==lib['precision_bits'] and x['certified_error_bits']==4096
 c,s=native_power(k);bounds[aid]=(c,s);progress+=1
 if progress%4==0:print('independently audited native powers',progress,'of',len(angles),flush=True)
 for own,key in [(c,'native_cos_hex'),(s,'native_sin_hex')]:
  other=[int(y,16) for y in x[key]];assert own[0]*factor<=other[1] and other[0]<=own[1]*factor,(aid,key)
used=set();maxerr=0;checks=0;zeros=0
for vid,entry in lib['vectors'].items():
 v,rots=own_target(entry['spec']);assert len(rots)==len(entry['rotations'])==3
 for grade,val in v.items():
  bounds_hex=entry['half_vector_bounds_hex'][str(grade)];lo,hi=[int(x,16) for x in bounds_hex];assert val[0]*factor<=hi and lo<=val[1]*factor,(vid,grade)
 for other,(tc,ts),r in zip((14,0,15),rots,entry['rotations']):
  assert other==r['other'];aid=r['angle_id']
  if aid is None:assert ts==(0,0) and tc[0]<=S<=tc[1];zeros+=1;continue
  # (1,14) and (1,0) use source pivot=1 -> negate native sine.
  if other in (14,0):ts=I.neg(ts)
  item=angles[aid];used.add(aid)
  for own,key in [(tc,'target_cos_hex'),(ts,'target_sin_hex')]:
   lo,hi=[int(x,16) for x in item[key]];assert own[0]*factor<=hi and lo<=own[1]*factor,(vid,other,key)
  nc,ns=bounds[aid];err=max(abs(nc[0]-tc[1]),abs(nc[1]-tc[0]))+max(abs(ns[0]-ts[1]),abs(ns[1]-ts[0]));assert err>0 and (err<<4096)<=S,(vid,other,'native error')
  maxerr=max(maxerr,err);checks+=1
assert used==set(angles) and len(lib['vectors'])==22 and checks+zeros==66
assert sha256(p.read_bytes()).hexdigest()==digest
out={'status':'PASS_INDEPENDENT_A18_ALL_TARGET_AND_NATIVE_INTERVALS','library_sha256':digest,'independent_precision_bits':bits,'library_precision_bits':lib['precision_bits'],'unique_native_powers_checked':len(angles),'all_vector_rotation_targets_checked':checks,'exact_identity_rotations':zeros,'full_half_vectors_checked':len(lib['vectors']),'weakest_independent_L1_error_strictly_below':'2^-'+str(bits-maxerr.bit_length()),'required_per_plane_error_le':'2^-4096','arithmetic':'integer outward dyadic targets and certified complex Euclidean balls for native powers, independently implemented; includes Machin pi and square roots','uses_float_in_proof':False,'does_not_reexecute_A18_builder':True,'physical_admission_or_full_bank_preparation':False,'GR_closed':False}
Path(__file__).with_name('ALL_MATERIAL_INTERVALS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
