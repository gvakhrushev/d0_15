#!/usr/bin/env python3
"""Exact original scene free-path capacity / finite ordered archive / native Perron pressure.
Scope: algebraic path composition, NOT compulsory physical Book action or GR.
"""
from itertools import product
import sympy as s

zones=[list(range(9)),list(range(9,20)),list(range(20,33))]
vertices=sum(zones,[])
zone={v:i for i,g in enumerate(zones) for v in g}
edges={(u,v) for u in vertices for v in vertices if zone[u]!=zone[v]}
assert len(vertices)==33 and len(edges)==718
root=0
A=(root,9,20,root)
B=(root,10,21,root)
for cyc in (A,B):
    assert all((u,v) in edges for u,v in zip(cyc,cyc[1:]))

def full_path(word):
    hist=[root]
    for letter in word:hist.extend((A if letter==0 else B)[1:])
    return tuple(hist)

for m in range(9):
    full={full_path(word) for word in product((0,1),repeat=m)}
    assert len(full)==2**m
    assert all(len(hist)==3*m+1 for hist in full)
print('PASS all ORIGINAL rooted loop-words A/B distinct, 2^m at length 3m')

for dim,first_fail_m in ((4,5),(16,9),(33,11),(718,19)):
    assert 2**(first_fail_m-1)<=dim**2<2**first_fail_m
    print(f'PASS algebra-linear fixed dimension={dim} fails at depth={3*first_fail_m}')

# Finite original loop-depth archive: |empty> plus every A/B word <=m.
# Truncated left creation L_i|w>=|i w> for |w|<m, else0.
# All formal polynomial coefficients are the VACUUM COLUMN of its operator.
for m in range(1,6):
    basis=[()] + [w for k in range(1,m+1)
                     for w in product((0,1),repeat=k)]
    index={w:j for j,w in enumerate(basis)}
    assert len(index)==2**(m+1)-1
    vacuum=()
    for w in basis:
        out=vacuum
        for ch in reversed(w):
            assert len(out)<m
            out=(ch,)+out
        assert out==w and index[out]==index[w]
print('PASS bounded loop-depth left-creation archive, faithful vacuum-column encoding')
print('NOTE not an unrestricted path-* representation; adjoint/reversal needs owner')

# Raw scalar Book weights from native cost=1/edge, Info=0
p=(s.sqrt(5)-1)/2
assert (20*p-1).is_positive
for u in vertices:
    assert sum(1 for v in vertices if (u,v) in edges)>=20
assert s.simplify(p*p+p-1)==0
print('PASS Z_raw(n) >= 33*(20*p)^n diverges as n increases')

x=s.symbols('x')
M=s.Matrix([[0,11,13],[9,0,13],[9,11,0]])
assert s.factor(M.charpoly(x).as_expr())==x**3-359*x-2574
rho=max(float(s.re(y)) for y in s.nroots(M.charpoly(x).as_expr()))
assert 21<rho<22 and 13<float(p)*rho<14
print('PASS original Perron adjacency polynomial x^3-359x-2574')
print('rho:',rho,'p*rho:',float(p)*rho)
print('SCOPE finite-depth path archive and native growth; GR_closed=false')
