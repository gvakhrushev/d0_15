#!/usr/bin/env python3
"""Exact one-scalar observer/clock compensation for the lost GR null polarization.
A mathematical extension, explicitly NOT admitted by the fixed-own-edge D0 law.
"""
import sympy as s, json
eta=s.diag(1,-1,-1,-1); lam=s.Matrix([205,144,96,72])/83; tau=eta*lam
k=s.Matrix([13,3,4,12]); zz=s.symbols('z',real=True)
P=lambda i,j: s.Matrix(4,4,lambda a,b:int((a,b)==(i,j) or (a,b)==(j,i)))
H0=s.Rational(9,13)*P(0,2)-s.Rational(3,13)*P(0,3)-3*P(1,2)+P(1,3)
checks=0
def eq(a,b,name):
 global checks
 if isinstance(a,s.MatrixBase): ok=a.shape==b.shape and all(s.simplify(x-y)==0 for x,y in zip(a,b))
 else:ok=s.simplify(a-b)==0
 if not ok:raise RuntimeError(name)
 checks+=1

eq(s.trace(eta*H0),0,'tracefree independent null physical wave')
eq((k.T*eta*k)[0],0,'true null wavevector')
phi=(tau.T*(eta+zz*H0).inv()*tau)[0]
g=eta+zz*H0
tau_new=tau/s.sqrt(phi)
eq(s.simplify((tau_new.T*g.inv()*tau_new)[0]),1,'exact future norm maintained by scalar compensation')
for i in range(4):eq(g[i,i],eta[i,i],'own-leg Q diagonal invariant')
ct=s.factor(s.diff(phi,zz).subs(zz,0))
expected=s.factor((lam.T*H0*lam)[0])
eq(ct,-expected,'native scalar normalization first order')
cdt=tau_new.diff(zz).subs(zz,0)
eq(cdt,expected*tau/2,'single clock first jet restores observer normalization')
# Fixed same-edge native stored law forbids this moving tau for any varying Fourier field.
for i in range(4):
 if s.simplify(cdt[i])==0:raise RuntimeError('missing observer invariant is not moved')
 checks+=1
# Artificially freezing tau would fail observer norm at first order.
if expected==0:raise RuntimeError('lost polarization was secretly native')
checks+=1
print(json.dumps({'status':'PASS','exact_controls':checks,
  'lost_polarization_lambda_H_lambda':str(expected),
  'needed_single_scalar_clock_derivative':str(s.factor(expected/2)),
  'physical_fixed_tau_edge_law_violated':True,
  'clock_extension_physically_selected':False,
  'all_ten_offshell_GR_derived':False},sort_keys=True))
