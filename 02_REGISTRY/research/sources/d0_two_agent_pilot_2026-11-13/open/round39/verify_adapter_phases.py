#!/usr/bin/env python3
"""Independent integer-interval recomputation of both adapter phases."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import json
P=Path(__file__).resolve().parent;f=P/'ADAPTER_PHASE_CERTIFICATE.json';j=json.loads(f.read_text());source=sha256(f.read_bytes()).hexdigest();B=12288;S=1<<B;shift=B-j['precision_bits'];assert shift>0;fac=1<<shift
ceil=lambda x,d:-((-x)//d)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def mul(x,y):
 v=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(v)//S,ceil(max(v),S)
def div(x,y):
 assert y[0]>0
 return min(a*S//b for a in x for b in y),max(ceil(a*S,b) for a in x for b in y)
def sq(x):return (0 if x[0]<=0<=x[1] else min(x[0]**2,x[1]**2)//S),ceil(max(x[0]**2,x[1]**2),S)
def sqrt(x):
 assert x[0]>=0;u=isqrt(x[1]*S);return isqrt(x[0]*S),u+(u*u<x[1]*S)
def cmul(x,y):return (add(mul(x[0],y[0]),neg(mul(x[1],y[1]))),add(mul(x[0],y[1]),mul(x[1],y[0])))
# sqrt(1/65568), independently from direct integer division.
c0=isqrt((S*S)//65568);c=(c0,c0+1);eps=((S-c[1])//2,ceil(S-c[0],2));assert 0<eps[0]<=eps[1]<S//2
r3=isqrt(3*S*S);h=(r3//2,ceil(r3+1,2));e=eps;z=((S,S),(0,0))
for _ in range(8):
 g=(((e[0]-S)//2,ceil(e[1]-S,2)),mul(h,(S+e[0],S+e[1])));z=cmul(z,g);e=mul(mul(e,e),e)
assert e[1]<(S>>6561)
norm=sqrt(add(sq(z[0]),sq(z[1])));correct=(div(z[0],norm),neg(div(z[1],norm)));target={'phase_certificate':((S//2,S//2),h),'correction_certificate':correct}
# No-clamp rectangular interval power independent of the ball method.
r5=isqrt(5*S*S);p=((r5-S)//2,ceil(r5+1-S,2));aa=(isqrt(p[0]*S),isqrt(p[1]*S)+1)
def power(n):
 x=((S,S),(0,0));base=(aa,p)
 while n:
  if n&1:x=cmul(x,base)
  n>>=1
  if n:base=cmul(base,base)
 return x
for name,k,K in [('phase_certificate',int(j['phase_k']),1),('correction_certificate',int(j['correction_l']),0)]:
 part=j[name];got=power((1<<K)*k);wanted=target[name]
 for bounds,key in [(got[0],'native_cos_hex'),(got[1],'native_sin_hex'),(wanted[0],'target_cos_hex'),(wanted[1],'target_sin_hex')]:
  saved=[int(x,16) for x in part[key]]
  assert saved[0]*fac<=bounds[0] and bounds[1]<=saved[1]*fac,(name,key)
 err=max(abs(got[0][0]-wanted[0][1]),abs(got[0][1]-wanted[0][0]))+max(abs(got[1][0]-wanted[1][1]),abs(got[1][1]-wanted[1][0]));assert err>0 and (err<<4096)<=S
assert sha256(f.read_bytes()).hexdigest()==source
out={'status':'PASS_INDEPENDENT_ADAPTER_PHASE_INTERVALS','certificate_sha256':source,'independent_bits':B,'original_bits':j['precision_bits'],'both_native_and_target_saved_bounds_contain_independent_enclosures':True,'both_L1_errors_le':'2^-4096','ideal_failure_lt':'2^-6561','float_used':False,'GR_closed':False}
(P/'ADAPTER_PHASE_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
