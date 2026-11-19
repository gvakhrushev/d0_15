#!/usr/bin/env python3
"""Exact first-source discrimination on original physical full128 J23 one-step channel.
Consumes immutable original all128 receipt when executed in the repository.
Distinct candidate source functionals are NEVER summed into a new D0 action.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as s

p=(s.sqrt(5)-1)/2; h=s.Rational(1,4); lam=s.Rational(288,25)
dlam=-s.Rational(144,25); ell=s.log((1+s.sqrt(5))/2)
eps=p*p*h*h/64
B=1-eps*lam/2
F=s.factor(1-B*B)
dF=s.factor(eps*B*dlam)
q0=s.expand(B*B)
dq0=-dF
z=s.symbols('z',real=True,positive=True)
# Book03 defines S_fb=-Tr log(I-zF), but identifying THIS exit F as the
# compulsory original full Book03 F is not yet proved.
dS=s.factor(16*z*dF/(1-z*F))
assert s.simplify(dS-16*z*eps*B*dlam/(1-z*F))==0
assert all(float(s.N(expr))>0 for expr in (B,F,1-p**2*F))
assert float(s.N(dF))<0
assert s.simplify(dS.subs(z,p*p))!=0
assert abs(float(s.N(dS.subs(z,p*p),30))+0.013124128877287944489)<1e-14

# The original full128 conditional nonblank-port code, no guessed reference.
P_label=s.simplify(eps*lam*(1-h*h*lam/256))
dP_label=s.simplify(eps*(1-h*h*lam/128)*dlam)
dK_label=s.simplify(p**3*dP_label)
assert s.simplify(dP_label-(-42957+14319*s.sqrt(5))/5120000)==0
assert s.simplify(dK_label-(157509-71595*s.sqrt(5))/5120000)==0
assert s.simplify(p**3-(p-p*p))==0

# Full native expected Golden port cost and individual blank modal surprisal
# are DIFFERENT readings of one unchanged all128 complete channel.
dCost_port=s.simplify(p*eps*dlam)
dModal=s.simplify(-dq0/(q0*ell))
assert abs(float(s.N(dCost_port,35))+0.001327882373436317)<1e-14
assert abs(float(s.N(dModal,35))+0.00447450570805938)<1e-13

# Pin original complete all128 first-source grouped receipt and verify its
# full physical probabilities rather than substitute a made-up Born alphabet.
HERE=Path(__file__).resolve().parent
src=HERE.parent/'d0_native_full128_order_readout_2026-10-19'/'COMPLETE_SHANNON_SOURCE.json'
if src.exists():
    data=src.read_bytes()
    gh=hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()
    assert gh=='d5f816d6e77532d91950fa3f99598844a5349a6f',gh
    j=json.loads(data)
    assert j['status']=='PASS_SCOPED_COMPLETE_FULL128_SHANNON_FIRST_SOURCE'
    assert j['checks']==29 and j['probability_law']['positive_outcomes']==42
    assert j['probability_law']['zero_outcomes']==86
    groups=[]
    for item in j['probability_law']['groups']:
        groups.append((item['multiplicity'],s.sympify(item['probability'],locals={'sqrt':s.sqrt}),s.sympify(item['source_sum'],locals={'sqrt':s.sqrt})))
    assert sum(k for k,q,dq in groups)==128
    assert s.simplify(sum(k*q for k,q,dq in groups)-1)==0
    assert s.simplify(sum(dq for k,q,dq in groups))==0
    assert s.simplify(groups[0][1]-q0)==0
    assert s.simplify(groups[0][2]-dq0)==0
    Hfull=-sum(dq*s.log(q)/ell for k,q,dq in groups if q!=0)
    value=s.Float(j['complete_pointer_shannon']['first_source_numeric_70_digits'],70)
    assert abs(float(s.N(Hfull-value,45)))<1e-27
    print('PASS: ORIGINAL SHA-pinned full128 Q(sqrt5) receipt, 42 positive and 86 dark zero-first-jet outcomes')
    print('complete-pointer Shannon first source (phi units):',s.N(Hfull,22))
else:
    print('ORIGINAL FULL128 RECEIPT UNAVAILABLE LOCALLY: symbolic native first-source checks run, NOT full128 replay')
print('PASS: native exit F=I-(I-epsilon Delta/2)^2, noncommuting field jet by trace cyclicity at scalar base')
print('PASS: dS_exit(z) strictly negative for z>0, zF<1; no fitted gravity coefficient')
print('d S_exit(z=p²), natural logs=',s.N(dS.subs(z,p*p),22))
print('h^-2 d S_exit(z=p²)=',s.N(dS.subs(z,p*p)/h**2,22))
print('d original Golden port cost (phi code units)=',s.N(dCost_port,22))
print('d original conditional port KL (phi units)=',s.N(dK_label,22))
print('d original full-blank modal surprisal (phi units)=',s.N(dModal,22))
print('FULL BORN normalized sum=1; no absolute -log partition source')
print('FIREWALL: Book03 exit identification, compulsory complete Cost-Info/clock/work/prep, source cancellation, GR OPEN')
