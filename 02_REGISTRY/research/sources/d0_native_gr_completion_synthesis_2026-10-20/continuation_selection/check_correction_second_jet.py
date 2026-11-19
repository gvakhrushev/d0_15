"""Exact 2x2 controls; the differentiability/ridge theorem is analytical."""
import json
import sympy as s


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


x,u = s.symbols('x u', real=True)
k,g,D = s.symbols('k g D', nonzero=True, real=True)
A,B,C,beta,lam = s.symbols('A B C beta lam', real=True)
S0 = -k*g*x*u-k*g*D*u*u
H0 = s.hessian(S0,(x,u))
require(H0==s.Matrix([[0,-k*g],[-k*g,-2*k*g*D]]), 'native slice form')
total = H0+s.Matrix([[A,B],[B,C]])
require(s.expand(total.det()-(A*(C-2*k*g*D)-(B-k*g)**2))==0,
        'exact PSD determinant criterion')
require(s.simplify(total.det().subs(A,0)+(B-k*g)**2)==0,
        'zero coframe diagonal forces mixed cancellation')
padding = beta*u*u
require(s.diff(padding,x).subs(u,0)==0 and
        s.diff(padding,u).subs(u,0)==0, 'padding zero source along curve')
require(s.simplify(s.hessian(S0+padding,(x,u)).det()+(k*g)**2)==0,
        'source-preserving transverse padding keeps saddle')
counter = k*g*x*u+(k*g*D+lam)*u*u
require(s.expand(S0+counter)==lam*u*u, 'algebraic cancelling control')
require(s.diff(counter,u).subs(u,0)==k*g*x,
        'cancelling control changes neighboring first source')

mu,gamma = s.symbols('mu gamma', nonzero=True, real=True)
J_u = -g*x/gamma
require(s.diff(mu*J_u,x)==-mu*g/gamma, 'J2 multiplier normalization')

print(json.dumps({
    'status':'PASS',
    'source_preserving_padding_determinant':'-(kappa*g)^2',
    'general_correction_determinant':'Kaa*(Kuu-2*kappa*g*D)-(Kau-kappa*g)^2',
    'zero_Kaa_requires':'Kau=kappa*g',
    'J2_multiplier_mixed_entry':'-mu*g/gamma_h',
    'controls':'Exact algebra only; no admitted correction or physical closure claimed.'
},indent=2))
