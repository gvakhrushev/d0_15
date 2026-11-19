#!/usr/bin/env python3
"""Independent full K(9,11,13) Hodge/Book/Green-Kubo/third-vertex replay.
Mathematical scalar Book-history sector; NOT native physical GR selection.
Requires numpy, sympy (the repository already declares these dependencies).
"""
import math
import numpy as np
import sympy as sp

part=np.repeat(np.arange(3), [9,11,13]); n=33
A=(part[:,None]!=part[None,:]).astype(float)
src,dst=np.where(A); m=len(src); assert m==718
rho=float(np.linalg.eigvalsh(A)[-1]); ev,vectors=np.linalg.eigh(A)
r=np.abs(vectors[:,-1]); r/=np.linalg.norm(r)
pi=r*r; P=A*r[None,:]/(rho*r[:,None]); mu=pi[src]*P[src,dst]
assert np.max(abs(mu-pi[dst]*P[dst,src]))<1e-13
assert np.max(abs(P.sum(axis=1)-1))<1e-13
J0=np.zeros((m,n)); J1=np.zeros((m,n))
J0[np.arange(m),src]=np.sqrt(P[src,dst]); J1[np.arange(m),dst]=np.sqrt(mu/pi[dst])
R=J1-J0@(J0.T@J1); F=R.T@R
we,vec=np.linalg.eigh(F)
assert sum(we>0.1)==32 and we[0]>-1e-12
Finv=vec@np.diag([1/x if x>0.1 else 0 for x in we])@vec.T
L=np.diag(pi)-pi[:,None]*P
Lfix=L+np.ones((n,n))/n
fund=np.linalg.inv(np.eye(n)-P+np.outer(np.ones(n),pi))
root=math.log((1+math.sqrt(5))/2)
pairs={(int(a),int(b)):j for j,(a,b) in enumerate(zip(src,dst))}
flip=np.array([pairs[int(b),int(a)] for a,b in zip(src,dst)])
rng=np.random.default_rng(1821)

def force(d):
    c=np.dot(mu,d[src,dst]); b=np.sum(P*d,axis=1)-c
    xi=fund@b
    g=np.sqrt(mu)*(d[src,dst]-c-xi[src]+xi[dst])
    assert np.linalg.norm(J0.T@g)<1e-11
    return g

def future(g): return R@Finv@(R.T@g)

def cycle(g):
    skew=(g-g[flip])/2
    b=np.bincount(src, weights=np.sqrt(mu)*skew, minlength=n)
    chi=np.linalg.solve(Lfix,b)
    out=skew-np.sqrt(mu)*(chi[src]-chi[dst])
    assert np.linalg.norm(J0.T@out)<1e-11
    return out

# Construct FOUR explicit mutually orthogonal projectors on ALL 718 edges.
for _ in range(13):
    y=rng.normal(size=m)
    now=J0@(J0.T@y); fut=future(y); cyc=cycle(y)
    dark=y-now-fut-cyc
    blocks=[now,fut,dark,cyc]
    assert max(abs(blocks[i]@blocks[j]) for i in range(4) for j in range(i))<1e-10
    assert np.linalg.norm(cycle(cyc)-cyc)<1e-11
    assert np.linalg.norm(cycle(dark))<1e-11
    assert np.linalg.norm(R.T@dark)<1e-11

# Reversal parity is EXACTLY orthogonal in actual Book archive Hessian.
maxcross=maxfuture=0.0
for _ in range(24):
    d=rng.normal(size=(n,n))*A
    ge=force((d+d.T)/2); go=force((d-d.T)/2)
    maxcross=max(maxcross, abs(ge@go)); maxfuture=max(maxfuture,np.linalg.norm(R.T@go))
    assert np.max(abs(go+go[flip]))<1e-12
assert maxcross<1e-11 and maxfuture<1e-11

# Original vertex-sum price is future-ONLY; a local reversal-even pair is not.
alpha=np.select([part==0,part==1,part==2],[.5,.5,-.5])
gsum=force(A*(alpha[:,None]+alpha[None,:]))
assert np.linalg.norm(gsum-future(gsum))<1e-11
one=np.zeros((n,n)); one[0,9]=one[9,0]=1
gloc=force(one)
darkfraction=np.linalg.norm(gloc-future(gloc))**2/np.linalg.norm(gloc)**2
assert .83<darkfraction<.85

# Whole original vertex-Info family: moving first and SECOND source in 32.
I=rng.normal(size=n); Ic=I-(pi@I); h=-np.sqrt(pi)*(fund@Ic)
errs=[]
for theta in (0.0,.23,.5,.9,1.0):
    d=-A*(theta*I[:,None]+(1-theta)*I[None,:])
    errs.append(np.linalg.norm(force(d)-R@h))
assert max(errs)<1e-11
GK=root*(Ic@(np.diag(pi)@((np.eye(n)+P)@(fund@Ic))))
assert abs(GK-root*np.linalg.norm(R@h)**2)<2e-12

def bookinfo(theta,s):
    K=A*np.exp(root*s*(theta*I[:,None]+(1-theta)*I[None,:]))
    return -math.log(max(np.linalg.eigvals(K).real))/root
step=1.2e-4; d2=[]
for theta in (0,.5,1):
    fd=(bookinfo(theta,step)+bookinfo(theta,-step)-2*bookinfo(theta,0))/step**2
    d2.append(fd)
assert max(abs(x+GK) for x in d2)<4e-7

# Symmetric-even and oriented-odd costs: genuine finite nonlinear cubic.
x,u,t=sp.symbols('x u t')
zone=sp.Matrix([[0,11*sp.exp(u+t),13],[9*sp.exp(u-t),0,13],[9,11,0]])
assert sp.simplify(sp.expand(zone.charpoly(x).as_expr())-(x**3-(99*sp.exp(2*u)+260)*x-1287*sp.exp(u)*(sp.exp(t)+sp.exp(-t))))==0
D=3*rho*rho-359; lu=(198*rho+2574)/D
G=2574/(rho*D)
G_u=G*(1-lu/rho-(6*rho*lu-198)/D)
assert abs(G_u-0.011327808455607455)<1e-11

print('PASS original native HE = 718; canonical orthogonal 33 + 32 + 326 + 327')
print('PASS original Book Hessian: even/odd cross <= %.3e; odd future <= %.3e'%(maxcross,maxfuture))
print('PASS symmetric local edge: even dark Schur fraction %.12f'%darkfraction)
print('PASS all original vertex-Info source: five theta controls max %.3e'%max(errs))
print('PASS 32-mode full Green-Kubo curvature %.12f, finite Perron %.12f'%(GK,-sum(d2)/len(d2)))
print('PASS exact 33-site cubic Perron polynomial; mixed even/odd² ln rho %.12f'%G_u)
print('PASS native Book Golden cost cubic source %.12f'%(root**2*G_u))
print('NOT a physically selected full Book/CAR/40-row GR action')
