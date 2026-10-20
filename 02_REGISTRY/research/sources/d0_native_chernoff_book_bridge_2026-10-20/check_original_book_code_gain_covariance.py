#!/usr/bin/env python3
"""D0 conditional Book gain: recoding ONE SAME native tape is source-neutral
if Info=log_phi(q/mu) relative to the physically SUPPLIED prefix reference.
This does NOT assert that Book03 has selected that Info law.
"""
import sympy as s
p=(s.sqrt(5)-1)/2
phi=1/p
assert s.simplify(p+p*p-1)==0
x,y,z,w=s.symbols('x y z w',real=True)
Qp=p**6*(2+x-y-z+w)
Qm=p**6*(2-x+y+z-w)
assert s.simplify(Qp+Qm-4*p**6)==0
assert s.simplify(Qp.subs({x:y,z:w})-2*p**6)==0
assert s.simplify(Qm.subs({x:z,y:w})-2*p**6)==0
# A genuine complete history gamma retains its normalized q_gamma under
# BOTH deterministic output-code conventions. Full product code alphabet
# contains unused opposite-bit branches (zero native Born probability).
q,mu=s.symbols('q mu',positive=True)
for b0,b1 in ((0,1),(1,0)):
    C0,C1=1+b0,1+b1
    mu0,mu1=mu*p**C0,mu*p**C1
    # For positive measures log(q/(mu*p^C))=log(q/mu)+C*log(phi).
    gain0=s.log(q/mu)/s.log(phi)+C0
    gain1=s.log(q/mu)/s.log(phi)+C1
    assert s.simplify(gain1-gain0-(C1-C0))==0
    oldC=-s.log(mu)/s.log(phi)
    assert s.simplify(oldC+C0-gain0+s.log(q)/s.log(phi))==0
    assert s.simplify(oldC+C1-gain1+s.log(q)/s.log(phi))==0
    assert s.simplify((C1-gain1)-(C0-gain0))==0
print('PASS Golden four-arm equal p^6 histories and orientation antisymmetry')
print('PASS original 0/10 RAW price difference = true code-GAIN difference')
print('PASS full per-history net price unchanged under deterministic recoding')
print('Only distinct ORIGINAL positive ± histories retain signed likelihood odds.')
print('Physical Book gain law and compulsory action remain unproved.')
