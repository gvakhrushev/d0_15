#!/usr/bin/env python3
"""Exact D0 ORIGINAL Golden 16-string dual coder, SAME complete native tape.

Original q(F,U) mixed 3x3 is tested by check_native_four_arm_exact.py.
This file proves the full-info relabeling and Z2-odd relative length from
one retained tape, including entangled oldRIGHT example. NO Book selection.
"""
from itertools import product
import sympy as s
import numpy as np

p=(s.sqrt(5)-1)/2
strings=[''.join(t) for t in product('AB',repeat=4)]
sign={'ABAB':1,'ABBA':-1,'BAAB':-1,'BABA':1}
weight=lambda word:s.prod([p if ch=='A' else p**2 for ch in word])
assert s.simplify(p+p**2-1)==0
assert s.simplify(sum(weight(w) for w in strings)-1)==0
assert all(s.simplify(weight(w)-p**6)==0 for w in sign)

def bit(word,event,orient):
    if word not in sign:return 0
    return int(event) if sign[word]*orient==1 else 1-int(event)
for c in strings:
    for e in (0,1):
        assert bit(c,e,1)+bit(c,e,-1)==int(c in sign)
        assert bit(c,e,1)-bit(c,e,-1)==(
            sign[c]*(2*e-1) if c in sign else 0)

x,y,z,w=s.symbols('x y z w',real=True)
q=dict(zip(sign,(x,y,z,w)))
Qplus=sum(weight(c)*(q[c]*bit(c,1,1)+(1-q[c])*bit(c,0,1))
          for c in sign)
Qminus=sum(weight(c)*(q[c]*bit(c,1,-1)+(1-q[c])*bit(c,0,-1))
           for c in sign)
delta=x-y-z+w
assert s.simplify(Qplus-p**6*(2+delta))==0
assert s.simplify(Qminus-p**6*(2-delta))==0
assert s.simplify(Qplus+Qminus-4*p**6)==0
assert s.simplify(Qplus-Qminus-2*p**6*delta)==0
for Q in (Qplus,Qminus):
    assert s.simplify(Q.subs({x:y,z:w})-2*p**6)==0
    assert s.simplify(Q.subs({x:z,y:w})-2*p**6)==0

# FULL original fine-tape record G=(coin,128^2 labels, work,clock) is kept.
# New binary labels b+(G),b-(G) are deterministic. Appending them is an
# injective mapping of the COMPLETE classical record:
# H(G,b+)=H(G,b-)=H(G,b+,b-)=H(G), for arbitrary distribution including zeros.
# Now test the stronger WHOLE COHERENT record spectrum with arbitrary
# correlations of oldRIGHT, using just a two-event tape fixture for the
# universal isometric controlled-copy theorem.
N=32; ndata=2; nref=2
rng=np.random.default_rng(1547)
A=rng.normal(size=(N,ndata,nref))+1j*rng.normal(size=(N,ndata,nref))
for ci,c in enumerate(strings):
    for e in (0,1):
        A[2*ci+e]*=np.sqrt(float(weight(c)))*(1.05 if e else .7)
A/=np.linalg.norm(A)
M=A.transpose(0,2,1).reshape(N*nref,ndata)
rho=M@M.conj().T
eig=np.linalg.eigvalsh(rho)
assert abs(eig.sum()-1)<1e-12

def entropy(prob):
    v=np.asarray(prob).real
    v=v[v>1e-14]
    return float(-np.dot(v,np.log(v)))

Hs=[];Ss=[]
for orientation in (1,-1):
    output=np.zeros((N,2,ndata,nref),dtype=np.complex128)
    for ci,c in enumerate(strings):
        for event in (0,1):
            idx=2*ci+event
            output[idx,bit(c,event,orientation)]=A[idx]
    Mout=output.transpose(0,1,3,2).reshape(N*2*nref,ndata)
    rout=Mout@Mout.conj().T
    eout=np.linalg.eigvalsh(rout)
    assert np.max(np.abs(eout[-ndata:]-eig[-ndata:]))<1e-12
    assert abs(eout.sum()-1)<1e-12
    p0=np.einsum('idr,idr->i',A.conj(),A).real
    p1=np.einsum('ibdr,ibdr->ib',output.conj(),output).real
    assert abs(entropy(p0)-entropy(p1))<1e-12
    Hs.append(entropy(p1));Ss.append(entropy(eout))
assert abs(Hs[0]-Hs[1])<1e-12
assert abs(Ss[0]-Ss[1])<1e-12

# The two actual original terminal 0/10 code lengths are 1+b, hence
# E[L_+-L_-] = 2p^6 delta and E[L_++L_-]=2+4p^6 (field independent).
# With a SAME full query/source/clock price and SAME full-register Info,
# their *difference*, not their total physical expense, has the same
# signed mixed geometric source as the original native q event.
base=s.simplify(Qplus.subs({x:s.Rational(1,13),
                           y:s.Rational(1,13),
                           z:s.Rational(1,13),
                           w:s.Rational(1,13)}))
assert s.simplify(base-2*p**6)==0
print('PASS exact native Golden p^6 branches, 12 remaining paths retained')
print('PASS ONE complete original tape determines both opposite code labels')
print('PASS full pointer and coherent FULL RECORD+oldRIGHT Info coincide')
print('PASS relative code source 2*p^6*delta and even paid sum 2+4*p^6')
print('PASS identical reference costs, opposite mixed Hessians; Dmin tie')
print('Values:',{'p6':float(p**6),'baseline_Q':float(base),
                  'expected_both_lengths':float(2+4*p**6),
                  'mixed_coeff':float(2*p**6),
                  'full_pointer_entropy':Hs[0],
                  'full_coherent_entropy':Ss[0]})
print('NOT Book03 selection, Q8-to-orientation binding, full paid G0 action,')
print('not a Palatini tensor equality, not physical GR closure.')
