#!/usr/bin/env python3
"""All-six original CAR16 -> complete positive Julia/Choi Palatini event.
RESEARCH: constructed mathematical tester, NOT the selected full128 Book source.
"""
import numpy as np
import sympy as s

def E(i,j):
    a=s.zeros(4); a[i,j]=1; return a
K=[E(0,i)+E(i,0) for i in (1,2,3)]
J=[E(2,3)-E(3,2),E(3,1)-E(1,3),E(1,2)-E(2,1)]
G=K+J
eta=s.diag(1,-1,-1,-1)
assert all(X.T*eta+eta*X==s.zeros(4) for X in G)
assert s.Matrix([[s.trace(X*Y) for Y in G] for X in G])==s.diag(2,2,2,-2,-2,-2)
x,y=s.symbols("x y",real=True)
for X in G:
    boost=X in K
    U=s.eye(4)+(s.sinh(x) if boost else s.sin(x))*X+(s.cosh(x)-1 if boost else 1-s.cos(x))*X**2
    marked=(s.det(s.eye(4)+U)/32)**2
    good=s.det(s.eye(4)+U.T*U)/64
    assert s.simplify(marked-(s.cosh(x/2) if boost else s.cos(x/2))**4/4)==0
    assert s.simplify(good-(s.cosh(x)**2/4 if boost else s.Rational(1,4)))==0
    hmark=s.diff(s.log(marked),x,2).subs(x,0)
    hgood=s.diff(s.log(good),x,2).subs(x,0)
    assert hmark==(1 if boost else -1)
    assert hgood==(2 if boost else 0)
    assert hmark-hgood==-1
for X in G:
    for Y in G:
        # exact st-jet of exp(xX)exp(yY), not an assumed finite SO matrix
        U=s.eye(4)+x*X+y*Y+x*y*X*Y
        d=(s.eye(4)+U).det()
        d0=d.subs({x:0,y:0})
        dx=s.diff(d,x).subs({x:0,y:0})
        dy=s.diff(d,y).subs({x:0,y:0})
        dxy=s.diff(d,x,y).subs({x:0,y:0})
        assert s.simplify(2*(d0*dxy-dx*dy)/d0**2-s.trace(X*Y)/2)==0

subsets=[[i for i in range(4) if (mask>>i)&1] for mask in range(16)]
def exterior(U):
    return np.array([[0. if len(a)!=len(b) else
        float(np.linalg.det(U[np.ix_(a,b)])) if a else 1.
        for b in subsets] for a in subsets])
def exp_lorentz(X,t,boost):
    A=np.array(X,dtype=float)
    return np.eye(4)+(np.sinh(t) if boost else np.sin(t))*A+(np.cosh(t)-1 if boost else 1-np.cos(t))*(A@A)
def rates(U):
    # original CAR16 full exterior; native Julia contraction T=Lambda(U)/2
    T=exterior(U)/2
    good=np.trace(T.T@T)/16
    mark=(np.trace(T)/16)**2
    assert abs(good-np.linalg.det(np.eye(4)+U.T@U)/64)<1e-12
    assert abs(mark-np.linalg.det(np.eye(4)+U)**2/1024)<1e-12
    assert np.linalg.eigvalsh(np.eye(16)-T.T@T).min()>0
    out=np.array([mark,good-mark,1-good])
    assert out.min()>-1e-12 and abs(out.sum()-1)<1e-12
    return out
for i,X in enumerate(G):
    for t in (-.13,-.07,0,.07,.13):
        rates(exp_lorentz(X,t,i<3))
for i,X in enumerate(G):
    for j,Y in enumerate(G):
        if i<=j:
            rates(exp_lorentz(X,.06,i<3)@exp_lorentz(Y,-.04,j<3))

# Gauge-sensitive COMPLETENESS witness: marked trace is conjugation-invariant;
# the standard positive-norm Julia success/failure masses are not under boosts.
U=exp_lorentz(K[0],.17,True)
H=exp_lorentz(K[1],.26,True)
Uconj=H@U@np.linalg.inv(H)
p,q=rates(U),rates(Uconj)
assert abs(p[0]-q[0])<1e-12
assert abs((p[0]+p[1])-(q[0]+q[1]))>1e-5
print("PASS all-six Lorentz: marked-event log Hessian diag(+++---)")
print("PASS full 3-outcome original CAR16 Julia/Choi normalized positive and conditional -I6")
print("PASS finite frame kill-control: marked gauge invariant, Julia failures frame dependent")
print("GR_closed=false: real native full128 reference/prep/action selection not proved")
