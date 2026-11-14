#!/usr/bin/env python3
"""Reconstruct full ten-sign report polynomial from every A12 palette row."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');file=D/'round12/TEN_SIGN_REPORT_PALETTE.json';z=json.loads(file.read_text());assert len(z['partitions'])==2048
# Polynomials in (f,q) with coefficients a+b p and p^2=1-p.
def add(a,b):
 out=dict(a)
 for x,(u,v) in b.items():
  w=out.get(x,(F(),F()));out[x]=(w[0]+u,w[1]+v)
 return {k:v for k,v in out.items() if v!=(0,0)}
def neg(a):return {k:(-x,-y) for k,(x,y) in a.items()}
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 out={}
 for (i,j),(x,y) in a.items():
  for (k,l),(u,v) in b.items():
   aa=x*u+y*v;bb=x*v+y*u-y*v;key=(i+k,j+l);old=out.get(key,(F(),F()));out[key]=(old[0]+aa,old[1]+bb)
 return {k:v for k,v in out.items() if v!=(0,0)}
def scale(a,n):return {k:(x*n,y*n) for k,(x,y) in a.items()}
I={(0,0):(F(1),F())};p={(0,0):(F(),F(1))};p2=mul(p,p);f={(1,0):(F(1),F())};q={(0,1):(F(1),F())};den=F(1,64);zeta=F(1,2**20)
def analytic(sigma):
 E=mul(p2,add(I,scale(f,den)));ell=scale(mul(E,sub(I,E)),4);u=add(p,scale(mul(p2,q),sigma*den));u2=mul(u,u);B=scale(mul(u2,sub(I,u2)),4);A=add(ell,mul(sub(I,ell),B));return sub(scale(add(A,B),zeta),scale(mul(A,B),zeta*zeta))
results={}
for sigma in (-1,1):
 rows=[row for key,row in zip(z['palette_keys'],z['partitions']) if key[0]==sigma];keys=[key[1] for key in z['palette_keys'] if key[0]==sigma];assert keys==list(range(1024))
 pair=[tuple(F(x) for x in row['weights'][0]) for row in rows];denom=lcm(*(a.denominator for pair0 in pair for a in pair0));ints=[[int(c*denom) for c in ab] for ab in pair]
 step=1
 while step<1024:
  for start in range(0,1024,2*step):
   for j in range(step):
    left=ints[start+j];right=ints[start+j+step];ints[start+j]=[left[k]+right[k] for k in (0,1)];ints[start+j+step]=[left[k]-right[k] for k in (0,1)]
  step*=2
 actual={}
 for mask,(a,b) in enumerate(ints):
  sign=(-1)**bin(mask).count('1');key=(bin(mask&3).count('1'),bin(mask>>2).count('1'));w=actual.get(key,(F(),F()));actual[key]=(w[0]+F(sign*a,1024*denom),w[1]+F(sign*b,1024*denom))
 actual={k:v for k,v in actual.items() if v!=(0,0)};want=analytic(sigma);assert actual==want,(sigma,actual,want)
 results[str(sigma)]={'palette_rows':len(rows),'exact_nonzero_bivariate_coefficients':len(actual),'maximum_f_degree':max(a for a,b in actual),'maximum_q_degree':max(b for a,b in actual),'identity':'sum(sign-product weights) = r(f/64, sigma*q/64)'}
out={'status':'PASS_ALL_A12_REPORT_PALETTE_POLYNOMIAL_EXACT','input_sha256':sha256(file.read_bytes()).hexdigest(),'sigma_results':results,'scope':'Algebraic identity for ten sign variables whose 2 f-sign and 8 q-sign expectations factor; multiplying by READY alpha assumes the proved ideal selector effect and conditional fresh resources. Does not establish physical source moments or marks.','GR_closed':False}
(P/'REPORT_BETA_EXACT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'results':results}))
