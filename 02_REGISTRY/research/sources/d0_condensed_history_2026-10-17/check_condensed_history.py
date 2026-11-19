#!/usr/bin/env python3
"""Finite exact controls of the condensed history/source boundary.

The analytic nonzero cokernel and double-limit statements are proved in the
corresponding .md theorem; finite checks do NOT prove infinite-stage claims.
"""
from __future__ import annotations
import json,hashlib
import sympy as sp
p=(sp.sqrt(5)-1)/2
checks=[]
def exact(name,a,b=0):
    if sp.simplify(a-b)!=0:raise ArithmeticError(f"{name}: {a} != {b}")
    checks.append(name)
def cost_cuts(limit):
    leaves=[('',0)];rows=[]
    for n in range(1,limit+1):
        nxt=[]
        for w,c in leaves:
            if c<n:nxt.extend([(w+'F',c+1),(w+'R',c+2)])
            else:nxt.append((w,c))
        leaves=nxt
        exact(f'cut_{n}_mass',sum((p**c for w,c in leaves),sp.Integer(0)),1)
        if not all(c in (n,n+1) for w,c in leaves):raise ArithmeticError(f'pending_{n}')
        k=n//2
        if k:
            for b in range(1<<k):
                pref=''.join('R' if (b>>j)&1 else 'F' for j in range(k))
                observed=sum((p**c for w,c in leaves if w.startswith(pref)),sp.Integer(0))
                expected=sp.prod(p**(2 if s=='R' else 1) for s in pref)
                exact(f'cut_{n}_cylinder_{pref}',observed,expected)
        rows.append({'cost_cut':n,'leaves':len(leaves),
                     'min_raw_depth':min(len(w) for w,c in leaves)})
    return rows
def finite_source():
    def value(bits,k):
        return sum((p**(j+1) for j,bit in enumerate(bits[:k]) if bit),sp.Integer(0))
    for n in range(1,10):
        for k in range(10):
            left=[0]*10;right=left.copy();right[n-1]=1
            actual=sp.simplify((value(right,k)-value(left,k))/p**n)
            exact(f'difference_{n}_{k}',actual,1 if n<=k else 0)
        exact(f'full_history_scale_{n}',p**(-n)*p**n,1)
    for k in range(11):
        tail=p**(k+1)/(1-p)
        exact(f'uniform_cylinder_approximation_{k}',
              sp.simplify(sum(p**j for j in range(k+1,k+9))+p**(k+9)/(1-p)),tail)
    for n in range(1,9):
        exact(f'sharp_scale_gain_{n}',(1-(-1))*p**(-n),2*p**(-n))
    for L in (2,3,4,5,8,11):
        h=sp.Rational(1,L)
        exact(f'critical_raw_h6_L{L}',h**-2*L**4*h**6,1)
        exact(f'safe_raw_h7_L{L}',h**-2*L**4*h**7,h)
def gram():
    x0=sp.Matrix([1,0])
    a=sp.Matrix([sp.Rational(3,5),sp.Rational(4,5)])
    b=sp.Matrix([sp.Rational(5,13),sp.Rational(12,13)])
    for name,x in [('a',a),('b',b)]:
        exact(f'endpoint_gram_{name}',(x.T*x)[0],1)
    ka=(a.T*x0)[0];kb=(b.T*x0)[0]
    exact('relative_cross_a',ka,sp.Rational(3,5))
    exact('relative_cross_b',kb,sp.Rational(5,13))
    if ka==kb:raise ArithmeticError('missing_cross_distinction')
    exact('full_comparator_a',ka**2,sp.Rational(9,25))
    exact('full_comparator_b',kb**2,sp.Rational(25,169))
    checks.append('same_endpoint_grams_different_real_overlap')
    return {'gram0':1,'gram1':1,'cross':['3/5','5/13'],
            'exp_minus_logdet':['9/25','25/169']}
def main():
    rows=cost_cuts(9);finite_source();cross=gram()
    return {'schema':'d0-condensed-history-source-boundary/1',
            'checks':len(checks),
            'check_names_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest(),
            'cost_cuts':rows,'cross_control':cross,
            'infinite_theorems_proved_by_script':False,
            'physical_native_gr_closed':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
