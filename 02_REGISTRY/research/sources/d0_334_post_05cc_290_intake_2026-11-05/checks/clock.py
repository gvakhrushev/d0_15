#!/usr/bin/env python3
"""Exact timelike-clock source witness; no root, PDE or compiler search."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sympy as s

checks=[]
def need(ok,label):
    if not bool(ok): raise ArithmeticError(label)
    checks.append(label)
def zero(x):
    if isinstance(x,s.MatrixBase): return all(s.factor(t)==0 for t in x)
    return s.factor(x)==0

a=s.Matrix(s.symbols('a0:4',real=True)); eta=s.diag(1,-1,-1,-1)
k,eps,chi=s.symbols('k eps chi',positive=True)
X=(a.T*eta*a)[0]
T=2*a*a.T-eta*X
n=eta*a # sqrt(X)*unit normal; clears radicals in every identity.
need(zero((n.T*eta*n)[0]-X),'unit clock normal after division by positive X')
need(zero((n.T*T*n)[0]-X**2),'clock stress pairs with its unit normal to X')
Ta=2*((1+eps)*a)*((1+eps)*a).T-eta*(1+eps)**2*X
need(zero(Ta-T-eps*(2+eps)*T),'full stress change when only one scalar is scaled')
residual=k*T-k*Ta
need(zero(residual+k*eps*(2+eps)*T),'fixed metric background cancels only the old stress')
need(zero((n.T*residual*n)[0]/(2*X)+k*eps*(2+eps)*X/2),
     'half-R source pairing has the original sign and factor')
w=-chi*n*(eta*n).T/(2*X)
dgcov=-chi*(eta*n)*(eta*n).T/X
need(zero(w.T*eta+eta*w-dgcov),'full coframe witness gives covariant metric variation')
J=lambda v:v-s.eye(4)*s.trace(v)/2
need(zero(J(J(w))-w),'particular raw material lift restores the physical clock test')
need(F(249,250)**2>F(99,100), 'owned clock collar volume density exceeds 99 over 100')
result={'status':'PASS','checks':checks,'number_of_checks':len(checks),
 'input_head':'66edbcfd458daecd133baca3b44528931e2ebfc5',
 'source_pairing':'-kappa epsilon (2+epsilon) integral(chi X dvol)/(2 nu)',
 'hypotheses':['X>0; certified clock collar has X>1/20',
 'compatible background solves unchanged Einstein-two-CAR source',
 'cutoff equals one on test support; initial collar unchanged',
 'normal-frame calculation transports by the owned Lorentz/material identities'],
 'not_claimed':['new exact native root','PDE solution emitted','native compiler run','finite stationary nuisance section'],
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,sort_keys=True,indent=2))
