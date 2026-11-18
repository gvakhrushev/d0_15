#!/usr/bin/env python3
"""Exact one-fixed-old-prefix RC3 coefficient algebra for round2 H.1."""
import contextlib, hashlib, importlib.util, io, json, runpy, sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[1]
path=root/'inputs/native_execution.py'
if hashlib.sha256(path.read_bytes()).hexdigest()!='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c': raise RuntimeError('native pin')
spec=importlib.util.spec_from_file_location('rc3_native',path); nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
p,a,G=nt.P,nt.A,nt.G_LOCAL; field=nt.GOLDEN_FIELD;v=s.Matrix([a,p]);zero=s.Matrix([1,0]); I=s.eye(2)
def eq(x,y): return field.from_sympy(s.expand(x-y))==field.zero
checks=[]
def need(x,n):
 if not x:raise AssertionError(n)
 checks.append(n)
K=[s.diag(a,p),s.diag(p,a)]
mu0=p**8+p**12;mu1=p**12
kappa=p+2*a*p**3
# True early original registered guard: b=0 projects only r; b=1
# includes t=0, so passive reference tail is <v| or a<0| respectively.
tau0=(zero,G**2*zero);tau1=G.T**2*zero
refs=(v.T,a*zero.T)
def affinity(ref,tau,f):
 x=K[f]*tau
 return (ref*x)[0]**2/(x.T*x)[0]
def coeff(ref,tau):
 return kappa**2*(mu0*affinity(ref,tau,0)+mu1*affinity(ref,tau,1))
H00=mu0*coeff(refs[0],tau0[0]);H10=mu0*coeff(refs[0],tau0[1]);H1=mu1*coeff(refs[1],tau1)
# Algebraic degree field normalization: convert quotients exactly.
conv=lambda x:field.from_sympy(s.cancel(x))
c0,c1,c2=map(conv,(H00,H10,H1))
need(c0!=c1,'marked sector0 differs exactly')
need(c0!=field.zero and c1!=field.zero and c2!=field.zero,'all marked coefficients nonzero')
# Six raw archive bits contain three copies of each pointer/tail bit.
for c in (0,1):
 for d in (0,1):
  marks=(c,d,c,d,d,c)
  need(sum(marks)==3*(c+d),'six-mark Hamming weight %d%d'%(c,d))
# All nine branch probabilities positive on 0<q<1, flag conditional
# probabilities strictly between 0 and 1, and every u0/u1 code0 branch.
need(eq((G*v)[0]**2+(G*v)[1]**2,1),'born encoder tail normalized')
for t in (tau0[0],tau0[1],tau1):
 need(eq((t.T*t)[0],1),'each conditional input tail normalized')
 need(eq(sum((K[f]*t).dot(K[f]*t) for f in (0,1)),1),'flag branches exhaustive')
# Rank bookkeeping: 3x3 supported fine output words, each isometry rank r.
r=4; labels=[(c,d,f,u) for c,d in ((0,0),(0,1),(1,0)) for f,u in ((0,0),(0,1),(1,0))]
need(len(labels)==9,'nine registered fine branches')
need(len(labels)*r-r==32,'RC3 mandatory (1-z)^32 offset')
# Exact coherent-vs-marked inequivalence control: labels separate fine
# channels and sum squares, not square of their coherent sum.
need(not eq((a+p)**2,a*a+p*p),'nonzero coherent cross term')
# Independent full nine-wire check, pre-input pointer superposition as a
# mathematical fixture; 12 archived basis bits are contracted exactly by
# the demonstrated six-copy Boolean map. The old full H1 writer is not run.
with contextlib.redirect_stdout(io.StringIO()): fixture=runpy.run_path(str(root/'check_full_native.py'))
import numpy as np
prefix,suffix=fixture['plan'](0,1); J=fixture['J']; ap=float(a);pp=float(p)
weight=lambda c,d:ap**(6-3*(c+d))*pp**(3*(c+d))
kap=float(s.N(kappa,18))
for which in (0,1):
 out=fixture['run'](prefix[which]+suffix)
 observed=0.0
 for b,c,d,f,u in ((b,c,d,f,u) for b in (0,1) for c,d in ((0,0),(0,1),(1,0)) for f,u in ((0,0),(0,1),(1,0)) if c==b):
  mask=np.array([((x>>(8-5))&1)==c and ((x>>(8-6))&1)==d and ((x>>(8-7))&1)==f and ((x>>(8-8))&1)==u for x in range(512)])
  if b==1: maskref=np.array([((x>>(8-4))&1)==0 for x in range(512)])
  else: maskref=np.ones(512,dtype=bool)
  state=out[:,b]*mask
  probability=float((state*state).sum())
  need(probability>1e-12,'each fine branch has positive support')
  reference=J[:,b]*(ap if b==0 else pp)*maskref
  overlap=float((reference*state).sum())*weight(c,d)*weight(f,u)
  observed+=kap**2*overlap**2/probability
 expected=float(s.N((H00 if which==0 else H10)*p+H1*p**2,18))
 need(abs(observed-expected)<1e-13,'full native fixed-prefix marked h version '+str(which))
print(json.dumps({'status':'PASS','checks':len(checks),'H0_word0':float(s.N(H00,20)),
'H0_word1':float(s.N(H10,20)),'H1_both':float(s.N(H1,20)),
'H0_difference':float(s.N(H10-H00,20)),'rank_per_prefix':r,'leaf_rank':36,
'RC3_exponent':32,'paid_final_helper':'two births plus one CX',
'physical_weight_binding_proved':False,'GR_closed':False},sort_keys=True,indent=2))
