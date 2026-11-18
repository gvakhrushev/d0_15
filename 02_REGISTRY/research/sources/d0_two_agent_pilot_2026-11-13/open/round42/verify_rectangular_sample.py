#!/usr/bin/env python3
"""Second, rectangular interval powering for one actual angle per family."""
from pathlib import Path
from hashlib import sha256
import sys,gzip,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'.deps'))
try:import gmpy2 as g
except ImportError:g=None
import proper_link_targets as p
if g:
 class Fast(p.Dyadic):
  def __init__(self,bits):self.bits=bits;self.scale=g.mpz(1)<<bits
  def sqrt(self,a):
   lo=g.isqrt(a[0]*self.scale);v=a[1]*self.scale;hi=g.isqrt(v);return lo,hi+(hi*hi<v)
 p.Dyadic=Fast
iv=p.Interval(8448);S=iv.S;bits=8448
with gzip.open(P/'PROPER_LINK_ANGLE_LIBRARY.json.gz','rt') as f:j=json.load(f)
specs,_=p.catalogue()
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def mul(x,y):
 v=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(v)>>bits,-((-max(v))>>bits)
def cmul(x,y):return add(mul(x[0],y[0]),neg(mul(x[1],y[1]))),add(mul(x[0],y[1]),mul(x[1],y[0]))
powers=[(iv.c['sqrtp'],iv.c['p'])]
for _ in range(3364):powers.append(cmul(powers[-1],powers[-1]))
def power(n):
 q=((S,S),(0,0));i=0
 while n:
  if n&1:q=cmul(q,powers[i])
  n>>=1;i+=1
 return q
def err(a,b,c,d):return max(abs(a[0]-c[1]),abs(a[1]-c[0]))+max(abs(b[0]-d[1]),abs(b[1]-d[0]))
cache={};count=0
for rec in j['families']:
 sp=specs[rec['family']];f=p.factor(iv,sp,cache)
 if rec['L']:
  target=p.givens(iv,f['L'])[0];angle=rec['L'][0];cc,ss=target['cos'],target['sin']
 elif rec['R']:
  target=p.givens(iv,f['R'])[0];angle=rec['R'][0];cc,ss=target['cos'],target['sin']
 else:
  target=p.diagonal_targets(iv,f)[(0,0)];angle=rec['diagonal']['00'];cc,ss=target['cos'],target['sin']
 cc=(max(-S,cc[0]),min(S,cc[1]));ss=(max(-S,ss[0]),min(S,ss[1]));c,s=power(int(angle['k'])<<23)
 assert err(c,s,cc,ss)<=(S>>3264),rec['family'];count+=1
 if count%80==0:print('rectangular independent families',count,flush=True)
out={'status':'PASS_INDEPENDENT_RECTANGULAR_POWER_SAMPLE','families_checked':count,'angles_checked':count,'precision_bits':8448,'ball_method_not_used':True,'float_used':False,'library_sha256':sha256((P/'PROPER_LINK_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest(),'GR_closed':False}
(P/'RECTANGULAR_SAMPLE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
