#!/usr/bin/env python3
"""Controls for M6 and its nine-leaf H.1 specialization; no physical source assertion."""
import contextlib,io,json,math,runpy
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()): exact=runpy.run_path(str(root/'round3/check_rc3.py'))
p=float(exact['p']); H0=[float(x.evalf(20)) for x in (exact['H00'],exact['H10'])]; H1=float(exact['H1'].evalf(20))
checks=[]
def need(ok,name):
 if not ok: raise AssertionError(name)
 checks.append(name)
# The actual q collar and fixed native fine conditional probabilities.
min_seen=1.0
for q in (p*p+1e-6,.4,.5):
 for word in (0,1):
  s0=p*p if word==0 else p*p+4*p**6
  s1=p*p+4*p**6
  probabilities=[]
  for b in (0,1):
   qb=1-q if b==0 else q
   ds=(p**6,4*p**3) if b==0 else (1.0,)
   flag=s0 if b==0 else s1
   for pd in ds:
    for f in (0,1):
     pf=1-flag if f==0 else flag
     us=(p**6,4*p**3) if f==0 else (1.0,)
     for pu in us: probabilities.append(qb*pd*pf*pu)
  need(len(probabilities)==9,'nine fixed-support fine leaves')
  need(abs(sum(probabilities)-1)<1e-12,'fine probabilities sum to one')
  need(min(probabilities)>=p**16-1e-14,'all fine probabilities above p^16')
  min_seen=min(min_seen,min(probabilities))
# Frozen scalar-root fixture: the two endpoint normalized compressed maps
# are contractions; evaluate exact marked logdet and the h-specific M6 bound.
z=.7;r=4;t=.02;gamma=1.3
for word in (0,1):
 a0p,a0m=.35,.4; a1p,a1m=.2,.18
 hp=H0[word]*a0p*a0p+H1*a1p*a1p
 hm=H0[word]*a0m*a0m+H1*a1m*a1m
 jp=-r*math.log(1-z+z*hp); jm=-r*math.log(1-z+z*hm)
 actual=abs(jp-jm)/(2*t*gamma)
 bound=z*r*(H0[word]*abs(a0p-a0m)+H1*abs(a1p-a1m))/((1-z)*t*gamma)
 need(actual<=bound+1e-12,'explicit compressed-root finite comparison bound')
# A tiny absolute branch error does not imply a small normalized projector
# error without the actual probability: V=e1 and W=e2 with pi=1e-12.
pi=1e-12; delta=math.sqrt(2*pi); alpha=delta/math.sqrt(pi)
need(delta<2e-6 and alpha>1,'negative control retains pi^(-1/2)')
# Original coarse p,p^3 masses do not force polar return overlaps.
# A unit tail orthogonal to v is still in the identical registered r=0 sector.
a=math.sqrt(p)
need(abs(a*p+p*(-a))<1e-15,'same sector can have zero born overlap')
need(abs(p*p+a*a-1)<1e-14,'orthogonal conditional tail is normalized')
need(abs(p-(a*a))<1e-14,'coarse born mass p does not fix conditional isometry')
# Direct M6 one-leaf scalar-root example.
z=.5; hp=1.;hm=9/25;alpha=2/math.sqrt(5)
need(abs(-math.log(1-z+z*hp)+math.log(1-z+z*hm))<=2*z*alpha/(1-z),'M6 finite logdet bound')
print(json.dumps({'status':'PASS','checks':len(checks),'p16':p**16,
 'smallest_sample_leaf_probability':min_seen,'H0':H0,'H1':H1,
 'scope':'conditional finite comparison, fixed old prefix, original physical full source not computed',
 'physical_cost_info_binding_proved':False,'GR_closed':False},indent=2,sort_keys=True))
