#!/usr/bin/env python3
"""Rebuild all A12 report weights and demonstrate exact correlated/site limits."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');f=D/'round12/TEN_SIGN_REPORT_PALETTE.json';palette=json.loads(f.read_text())
Z=(F(0),F(0));ONE=(F(1),F(0));P=(F(0),F(1))
def q(x,y=0):return (F(x),F(y))
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[0],-x[1]
def mul(x,y):return x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1]
def scale(x,z):return (x[0]*z,x[1]*z)
def padd(x,y):
 z=dict(x)
 for k,v in y.items():z[k]=add(z.get(k,Z),v)
 return {k:v for k,v in z.items() if v!=Z}
def pneg(x):return {k:neg(v) for k,v in x.items()}
def pmul(x,y):
 z={}
 for (a,b),v in x.items():
  for (i,j),w in y.items():z[a+i,b+j]=add(z.get((a+i,b+j),Z),mul(v,w))
 return {k:v for k,v in z.items() if v!=Z}
def pscale(x,z):return {k:mul(v,z) for k,v in x.items()}
def sign(x):
 u=2*x[0]-x[1];v=x[1]
 if not v:return (u>0)-(u<0)
 if not u:return (v>0)-(v<0)
 if (u>0)==(v>0):return (u>0)-(u<0)
 return ((u>0)-(u<0)) if u*u>5*v*v else ((v>0)-(v<0))
def poly(sigma):
 one={(0,0):ONE};S={(1,0):ONE};T={(0,1):ONE};p2=mul(P,P)
 E=pscale(padd(one,pscale(S,q(F(1,64)))),p2)
 uu=padd(pscale(one,P),pscale(T,scale(p2,F(sigma,64))))
 ell=pscale(pmul(E,padd(one,pneg(E))),q(4));u2=pmul(uu,uu);B=pscale(pmul(u2,padd(one,pneg(u2))),q(4))
 A=padd(ell,pmul(padd(one,pneg(ell)),B));z=q(F(1,2**20))
 return padd(one,pneg(pmul(padd(one,pneg(pscale(B,z))),padd(one,pneg(pscale(A,z))))))
def value(coeff,mask):
 signs=[1 if mask>>i&1 else -1 for i in range(10)];v=Z
 for (n,m),x in coeff.items():
  ss=1
  for t in signs[:n]+signs[2:2+m]:ss*=t
  v=add(v,scale(x,ss))
 return v
polys={sigma:poly(sigma) for sigma in (-1,1)};assert all(len(c)==27 for c in polys.values());cases=0
for sigma in (-1,1):
 for mask in range(1024):
  index=mask+1024*int(sigma==1);assert palette['palette_keys'][index]==[sigma,mask]
  weights=[tuple(F(c) for c in pair) for pair in palette['partitions'][index]['weights']]
  assert len(weights)==2 and add(*weights)==ONE and sign(weights[0])>0 and sign(weights[1])>0
  assert weights[0]==value(polys[sigma],mask);cases+=1
# Independent scalar expectation from beta(mask) for rational product marginals.
for sigma in (-1,1):
 for fval,tval in [(F(0),F(0)),(F(1,3),F(-2,5)),(F(-1),F(1))]:
  total=Z
  for mask in range(1024):
   prob=F(1)
   for i in range(10):prob*=F(1,2)*(1+(1 if mask>>i&1 else -1)*(fval if i<2 else tval))
   total=add(total,scale(value(polys[sigma],mask),prob))
  target=Z
  for (n,m),c in polys[sigma].items():target=add(target,scale(c,(fval**n)*(tval**m)))
  assert total==target
# Perfect S1/S2 correlation with all other signs unbiased: same 1-copy mean 0,
# but E[S1*S2]=1. Exact beta shift is [S²] coefficient, nonzero.
for sigma in (-1,1):
 coef=polys[sigma][(2,0)];assert coef!=Z
 independent=Z;correlated=Z
 for mask in range(1024):
  v=value(polys[sigma],mask);independent=add(independent,scale(v,F(1,1024)))
  if (mask&3) in (0,3):correlated=add(correlated,scale(v,F(1,512)))
 assert add(correlated,neg(independent))==coef
 # The same difference occurs for shared SITE x in {0,1} with equal weights,
 # conditional product copies and f_x=-1,+1, t_x=0. Thus β does not commute
 # with SITE average, although product factorization holds conditional on x.
 site_average=scale(add(add(polys[sigma][(0,0)],polys[sigma][(2,0)]),add(polys[sigma][(0,0)],polys[sigma][(2,0)])),F(1,2))
 beta_of_mean=polys[sigma][(0,0)];assert site_average==correlated and beta_of_mean==independent and add(site_average,neg(beta_of_mean))==coef
out={'status':'PASS_INDEPENDENT_EXACT_REPORT_OPERATOR_WEIGHTS','input_sha256':sha256(f.read_bytes()).hexdigest(),'sigma_mask_palette_cases':cases,'beta_coefficients_per_sigma':27,'product_scalar_expectation_checks':6,'full_effect':'E_sigma=Q_pre sum_mask beta_sigma,mask product_i (I+s_i O_i)/2, with O_i acting on disjoint copies and common SITE','correlated_copies_same_marginals_change_probability':True,'shared_SITE_requires_average_of_conditional_beta':True,'counterexample_exact_difference':'nonzero polynomial coefficient of f^2 in original beta','limitations':'exact ideal target effect only; requires compiled Boolean/fair targets and read-only shared SITE, and scalar factorization requires conditionally product sources','GR_closed':False}
Path(__file__).with_name('REPORT_EFFECT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
