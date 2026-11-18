#!/usr/bin/env python3
"""Certify real native powers for B25 SITE tree and phase, no float proof."""
from pathlib import Path
from hashlib import sha256
import sys,json,gzip
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'round42/.deps'))
try:import gmpy2 as g
except ImportError:g=None
import mpmath as mp
import site_targets as t
if g:
 class Fast(t.Dyadic):
  def __init__(self,bits):self.bits=bits;self.scale=g.mpz(1)<<bits
  def sqrt(self,a):
   assert a[0]>=0;lo=g.isqrt(a[0]*self.scale);z=a[1]*self.scale;hi=g.isqrt(z);return lo,hi+(hi*hi<z)
 t.Dyadic=Fast
iv=t.Dyadic(7168);S=iv.scale;c=t.old.constants(iv);counts,specs,nodes=t.tree_names();bits=3264;K=8
def ballmul(x,y):
 a,b,r=x;A,B,R=y;return ((a*A-b*B)>>7168,(a*B+b*A)>>7168,r+R+((r*R+S-1)>>7168)+2)
a,b=c['sqrtp'],c['p'];powers=[(a[0],b[0],a[1]-a[0]+b[1]-b[0])]
for _ in range(bits+100):powers.append(ballmul(powers[-1],powers[-1]))
def power(n):
 q=(S,0,0);i=0
 while n:
  if n&1:q=ballmul(q,powers[i])
  n>>=1;i+=1
 a,b,r=q;return (a-r,a+r),(b-r,b+r)
def err(a,b,c,d):return max(abs(a[0]-c[1]),abs(a[1]-c[0]))+max(abs(b[0]-d[1]),abs(b[1]-d[0]))
def digest(a,b):return sha256(('|'.join(hex(int(v)) for v in (*a,*b))).encode()).hexdigest()
with mp.workprec(3*bits+256):
 z=(2**K)*mp.acos(mp.sqrt((mp.sqrt(5)-1)/2))/(2*mp.pi);p0,p1,q0,q1=0,1,1,0;steps=0
 while True:
  a=int(mp.floor(z));pn=a*p1+p0;qn=a*q1+q0;steps+=1
  if qn.bit_length()>=bits+32:break
  p0,p1,q0,q1=p1,pn,q1,qn;z=1/(z-a)
 inv=pow(pn,-1,qn)
 def certify(cc,ss):
  turn=(mp.atan2(mp.mpf(ss[0]+ss[1]),mp.mpf(cc[0]+cc[1]))/(2*mp.pi))%1;point=int(mp.nint(qn*turn))%qn;k=(point*inv)%qn
  if k==0:k=qn
  a,b=power(k<<K);e=err(a,b,cc,ss);assert e<=S>>bits
  return {'k':str(k),'target_sha256':digest(cc,ss),'error_numerator_hex':hex(int(e))}
 angles={name:{'spec':sp,**certify(*t.targets(iv,sp,counts))} for name,sp in specs.items()}
 phase=certify(iv.rational(-1),iv.rational(0))
inputs=[P/'site_targets.py',Path(__file__),t.PF,t.D/'round18/material_targets.py',t.B/'round25/targets.py',t.B/'round25/precision_name.py'];sha=lambda q:sha256(Path(q).read_bytes()).hexdigest()
out={'status':'CERTIFIED_SOURCE_SITE_TREE_AND_PHASE_NATIVE_POWERS','precision_bits':7168,'per_macro_error_le':'2^-3264','native_multiplier_power':8,'source_sha256':{str(q):sha(q) for q in inputs},'PF_total':sum(counts),'PF_anchor':counts[0],'tree_nodes':nodes,'angles':angles,'reflection_phase':phase,'candidate_not_proof':{'numerator':str(pn),'denominator':str(qn),'steps':steps},'native_word_emitted':False,'full_physical_C_proved':False,'GR_closed':False}
with (P/'SITE_ANGLE_LIBRARY.json.gz').open('wb') as raw:
 with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(json.dumps(out,separators=(',',':')).encode())
print(json.dumps({'status':out['status'],'distinct_tree_angles':len(angles),'tree_nodes':len(nodes),'phase_angles':1,'sectors':256}))
