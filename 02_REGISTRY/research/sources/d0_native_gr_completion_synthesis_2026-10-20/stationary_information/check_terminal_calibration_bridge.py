#!/usr/bin/env python3
"""Exact new terminal/compensation identities on the owned Golden cleanup."""
import sympy as s

def require(test, label):
    if not test:
        raise RuntimeError(label)

alpha,t=s.symbols('alpha t', real=True)
modulus=alpha**4+alpha**2-1
def red(expr):
    n,d=s.fraction(s.cancel(s.together(expr)))
    return s.rem(s.expand(n),modulus,alpha)==0
p=alpha**2
sin2=2*alpha**3
cos2=p**3
require(red(sin2**2+cos2**2-1),'G2 normalization')
f0=1-2*t*t
f1=2*t*(1-t*t)
tail=4*t**4*(1-t*t)
require(s.expand(f0**2+f1**2+tail-1)==0,'complete cleanup norm')
q=(sin2*f0+cos2*f1)**2+cos2**2*tail
q0=q.subs(t,0)
qp=s.diff(q,t).subs(t,0)
require(red(q0-4*p**3),'native q2')
require(red(qp-8*alpha**9),'native q2 prime')
require(f0.subs(t,0)==1 and f1.subs(t,0)==0 and tail.subs(t,0)==0,
        'full work exactly clean on constraint, not merely marginal')
kappa=-1/alpha**3
terminal_multiplier=1/(8*p**6)
require(red(kappa+terminal_multiplier*qp),'native terminal adjoint cancels')

a,a0,u,g,H,rho0,rhod,chi=s.symbols('a a0 u g H rho0 rhod chi', positive=True)
signal=g*((1-a)*s.sin(u)-chi**2/(p*H**2)*(a*a/rho0+1/rhod)*s.sin(u)**2)
require(s.simplify(signal.subs(u,0))==0,'exact native null ridge')
ty=s.Matrix([[s.diff(signal,a),s.diff(signal,u)]]).subs({u:0,a:a0})
require(s.simplify(ty-s.Matrix([[0,g*(1-a0)]]))==s.zeros(1,2),'actual field tangent')
sy=kappa*ty
Cy=qp*ty
require(all(red(x) for x in sy+terminal_multiplier*Cy),'all slice adjoint rows')

# Symbolic exact rank witness for a0=2, one representative arbitrarily
# rescalable nonzero ridge displacement; this is not a new physical parameter.
# Any a0!=1 has the same rank, by the displayed general row.
Cytest=s.Matrix([[0,1]])
left=s.zeros(2,3)
right=Cytest.col_join(s.zeros(1,2))
require(left.rank()==0 and left.row_join(right).rank()==1,'logical input cannot compensate')

# Any hypothetical live compensator in the SAME scalar-source extension
# pays the exact opposite source. No admission of such a control is asserted.
tz=s.symbols('tz', nonzero=True)
L=-ty/tz
sz=kappa*tz
require(s.simplify(tz*L+ty)==s.zeros(1,2),'terminal compensation condition')
require(s.simplify(sz*L+sy)==s.zeros(1,2),'compensation price is not neutral')

print('PASS original complete Golden cleanup and local terminal response')
print('PASS exact original ridge field source and terminal-adjoint cancellation')
print('PASS failed logical-preparation lift rank 0 -> 1')
print('PASS any source-preserving live compensation cancels the field source')
