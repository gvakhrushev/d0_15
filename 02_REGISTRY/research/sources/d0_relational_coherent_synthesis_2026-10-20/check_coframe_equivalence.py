"""Explicit all-order radial dressing: full source, matter/history and singular root.
Structural homogeneous model only; physical native action selection not asserted.
"""
import json
import numpy as np
import sympy as s

e1,e2,A1,A2,psi,z=s.symbols('e1 e2 A1 A2 psi z',real=True)
qs=s.Matrix([e1,e2,A1,A2,psi,z])
u=A1-A2+psi**2
t=s.Matrix([e1**2*u,-e2**2*u])
w=s.Matrix([1+z,4+z**2])
B=z**4
H=s.Matrix([[e1+z**2+A1,(z+e1*e2+psi)/2],
            [(z+e1*e2+psi)/2,e2+A2**2]])
a=H*t
scales=s.Matrix([s.sqrt(1+a[i]/w[i]) for i in range(2)])
theta=s.Matrix([scales[0]*e1,scales[1]*e2,A1,A2,psi,z])
S0=B+(w.T*t)[0]
S=S0+(t.T*H*t)[0]
sub=dict(zip(qs,theta))
# Simultaneous substitution is essential: scale coefficients use original fields.
tp=t.subs(sub,simultaneous=True)
assert all(s.simplify(tp[i]-scales[i]**2*t[i])==0 for i in range(2))
assert s.simplify(S0.subs(sub,simultaneous=True)-S)==0
print('PASS exact symbolic all-order action identity with nonfactorable H')

L=t.jacobian(qs)
Z=s.zeros(6,2);Z[0,0]=e1;Z[1,1]=e2
assert s.simplify(L*Z-2*s.diag(*t))==s.zeros(2)
J=theta.jacobian(qs)
grad=lambda f:s.Matrix([s.diff(f,x) for x in qs])
num=lambda expr:s.lambdify(tuple(qs),expr,'numpy',cse=True)
thetaf,Jf=num(theta),num(J)
g0f,gf=num(grad(S0)),num(grad(S))
h0f,hf=num(s.hessian(S0,qs)),num(s.hessian(S,qs))
s0f,sf=num(S0),num(S)

q=np.array([2.03,1.01,.02,.063,.2,.05])
qp=np.asarray(thetaf(*q),float).ravel();j=np.asarray(Jf(*q),float)
action_error=float(abs(sf(*q)-s0f(*qp)))
source_error=float(np.max(abs(np.asarray(gf(*q)).ravel()-j.T@np.asarray(g0f(*qp)).ravel())))
assert action_error<1e-12 and source_error<1e-11
assert np.array_equal(qp[2:],q[2:]) and min(qp[:2])>0
assert abs(j[0,4])+abs(j[1,4])>1e-3
assert abs(j[0,5])+abs(j[1,5])>1e-5
print('PASS complete first source including moving matter/history coframe pullbacks')

root={e1:s.Rational(2),e2:s.Rational(1),A1:0,A2:s.Rational(1,9),psi:s.Rational(1,3),z:0}
assert t.subs(root)==s.zeros(2,1)
assert L.subs(root).rank()==1
assert grad(S0).subs(root)==s.zeros(6,1) and grad(S).subs(root)==s.zeros(6,1)
assert theta.subs(root)==qs.subs(root)
jr=s.simplify(J.subs(root))
n=jr-s.eye(6)
assert n*n==s.zeros(6) and jr.det()==1 and jr.inv()==s.eye(6)-n
assert s.simplify(s.hessian(S,qs).subs(root)-jr.T*s.hessian(S0,qs).subs(root)*jr)==s.zeros(6)
assert s.diff(B,z,2).subs(root)==0
print('PASS EXACT singular-Dt root, nilpotent unit-det Jacobian, full Hessian with degenerate B')

# Positive radicands alone need not guarantee a global diffeomorphism.
x=s.symbols('x',positive=True)
hostile_map=x*s.sqrt(1-x*x)
assert s.diff(hostile_map,x).subs(x,s.sqrt(2)/2)==0
assert (1-x*x).subs(x,s.sqrt(2)/2)>0
shell={**root,e1:s.Rational(3)}
assert t.subs(shell)==s.zeros(2,1) and ((e1-2)**2).subs(shell)==1
print('PASS hostile shell term; PASS positive-radicand/global-Jacobian distinction')
print(json.dumps({'action_error':action_error,'full_source_error':source_error,
    'root_hessian_identity':'exact rational','root_density_rank':1,
    'root_internal_B_hessian':0,'coframe_before':q[:2].tolist(),
    'coframe_after':qp[:2].tolist(),'matter_pullback':j[:2,4].tolist(),
    'history_pullback':j[:2,5].tolist(),'native_price_selected':False},indent=2))
