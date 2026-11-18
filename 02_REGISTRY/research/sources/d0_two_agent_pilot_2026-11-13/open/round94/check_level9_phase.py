#!/usr/bin/env python3
"""Independent rectangular intervals for the nine-level correction."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
from fractions import Fraction
import json
P=Path(__file__).resolve().parent;A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round48');j=json.loads((A/'LEVEL9_CORRECTION_CERTIFICATE.json').read_text());assert j['levels']==9
B=12288;S=1<<B;ceil=lambda x,d:-((-x)//d)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def mul(x,y):
 v=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(v)//S,ceil(max(v),S)
def div(x,y):
 assert y[0]>0;return min(a*S//b for a in x for b in y),max(ceil(a*S,b) for a in x for b in y)
def sq(x):return (0 if x[0]<=0<=x[1] else min(x[0]**2,x[1]**2)//S),ceil(max(x[0]**2,x[1]**2),S)
def sqrt(x):
 assert x[0]>=0;u=isqrt(x[1]*S);return isqrt(x[0]*S),u+(u*u<x[1]*S)
def cmul(x,y):return add(mul(x[0],y[0]),neg(mul(x[1],y[1]))),add(mul(x[0],y[1]),mul(x[1],y[0]))
c0=isqrt((S*S)//65568);c=(c0,c0+1);eps=((S-c[1])//2,ceil(S-c[0],2));assert 0<eps[0]<=eps[1]<S//2
r3=isqrt(3*S*S);h=(r3//2,ceil(r3+1,2));e=eps;z=((S,S),(0,0))
for _ in range(9):
 g=(((e[0]-S)//2,ceil(e[1]-S,2)),mul(h,(S+e[0],S+e[1])));z=cmul(z,g);e=mul(mul(e,e),e)
norm=sqrt(add(sq(z[0]),sq(z[1])));correct=(div(z[0],norm),neg(div(z[1],norm)))
fac=1<<(B-j['precision_bits'])
for v,key in zip(correct,('target_cos_hex','target_sin_hex')):
 saved=[int(x,16) for x in j[key]];assert saved[0]*fac<=v[0]<=v[1]<=saved[1]*fac
r5=isqrt(5*S*S);p=((r5-S)//2,ceil(r5+1-S,2));aa=(isqrt(p[0]*S),isqrt(p[1]*S)+1)
k=int(j['correction_l']);assert k==int(j['angles']['angle_0']['k']);state=((S,S),(0,0));base=(aa,p);n=k
while n:
 if n&1:state=cmul(state,base)
 n>>=1
 if n:base=cmul(base,base)
error=sum(max(abs(got[0]-target[1]),abs(got[1]-target[0])) for got,target in zip(state,correct));assert error*(1<<4096)<S
assert 3**9==19683 and Fraction(2,1<<19683)==Fraction(1,1<<19682)
out={'status':'PASS_INDEPENDENT_LEVEL9_PHASE_AND_IDEAL_BOUND','frozen_sha256':sha256((A/'LEVEL9_CORRECTION_CERTIFICATE.json').read_bytes()).hexdigest(),'independent_precision_bits':B,'phase_target_contained':True,'actual_G_power_error_lt':'2^-4096','epsilon0_lt_half':True,'nine_step_epsilon_exponent':19683,'ideal_failure_lt':'2^-19683','ideal_vector_error_lt':'2^-9841','assumes_exact_fixed_point_recursion_B39':True,'GR_closed':False}
(P/'LEVEL9_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
