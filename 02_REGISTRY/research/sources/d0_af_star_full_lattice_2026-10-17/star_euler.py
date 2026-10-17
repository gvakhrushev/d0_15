"""Exact unrestricted derivatives of the owned six-plaquette star action.

All 16 solder and 24 link directions, evaluated on a quadratic pp-wave.
This is a local fixed-boundary geometric result, not native admission.
Use rational null frame eta01=eta10=1, eta22=eta33=-1.
"""
from functools import lru_cache
from itertools import combinations
import sympy as s

x,y,h,a,b,d,cx,cy=s.symbols('x y h a b d cx cy', real=True)
ETA=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
I=s.eye(4)
PAIRS=list(combinations(range(4),2))
EPS=lambda p: s.LeviCivita(*p)
N=[]
for j in (2,3):
    m=s.zeros(4); m[1,j]=1; m[j,0]=1; N.append(m)
LIE=[]
for i,j in PAIRS:
    q=s.zeros(4); q[i,j]=1; q[j,i]=-1
    LIE.append(q*ETA)

def shift(z,r,k=1):
    w=list(z); w[r]+=k; return tuple(w)

@lru_cache(None)
def coframe(z):
    xx=x+h*z[2]; yy=y+h*z[3]
    H=a*xx**2+d*yy**2+2*b*xx*yy
    e=s.eye(4); e[1,0]=H/2
    return h*e

@lru_cache(None)
def link(z,r,inv=False):
    if r!=0: return I
    xx=x+h*z[2]; yy=y+h*z[3]
    K=h*((a*xx+b*yy+cx*h)*N[0]+(b*xx+d*yy+cy*h)*N[1])
    if K**3!=s.zeros(4):
        raise ArithmeticError('pp-wave generator must be nilpotent of order at most three')
    return I+(-K if inv else K)+K*K/2

def edges(z,r,t):
    return [(z,r,False),(shift(z,r),t,False),(shift(z,t),r,True),(z,t,True)]

@lru_cache(None)
def plaquette(z,r,t):
    P=I
    for zz,rr,iv in edges(z,r,t): P=P*link(zz,rr,iv)
    return P.applyfunc(s.expand)

def wedge(u,v):
    return [u[i]*v[j]-u[j]*v[i] for i,j in PAIRS]

def pairing(W,R):
    C=R*ETA
    return s.expand(sum(EPS((aa,bb,cc,dd))*W[k]*C[cc,dd]
                       for k,(aa,bb) in enumerate(PAIRS) for cc,dd in PAIRS))

def density(z):
    e=coframe(z); total=0
    for r,t in PAIRS:
        u,v=[j for j in range(4) if j not in (r,t)]
        P=plaquette(z,r,t); Pi=ETA*P.T*ETA
        total+=EPS((r,t,u,v))*pairing(wedge(e[:,u],e[:,v]),(P-Pi)/2)
    return s.factor(total)

def solder_source(z):
    e=coframe(z); out=s.zeros(4)
    for r,t in PAIRS:
        u,v=[j for j in range(4) if j not in (r,t)]
        P=plaquette(z,r,t); Pi=ETA*P.T*ETA; R=(P-Pi)/2
        for k in range(4):
            ek=I[:,k]
            out[k,u]+=EPS((r,t,u,v))*pairing(wedge(ek,e[:,v]),R)
            out[k,v]+=EPS((r,t,u,v))*pairing(wedge(e[:,u],ek),R)
    return out.applyfunc(s.factor)

def link_source(z,axis):
    out=[]
    for X in LIE:
        total=0
        for r,t in PAIRS:
            if axis not in (r,t): continue
            other=t if axis==r else r
            for base in [z,shift(z,other,-1)]:
                ed=edges(base,r,t)
                P=I; dP=s.zeros(4)
                for zz,rr,iv in ed:
                    U=link(zz,rr,iv)
                    dU=(-U*X if iv else X*U) if (zz==z and rr==axis) else s.zeros(4)
                    dP=dP*U+P*dU; P=P*U
                Pi=ETA*P.T*ETA
                dR=(dP+Pi*dP*Pi)/2
                u,v=[j for j in range(4) if j not in (r,t)]
                e=coframe(base)
                total+=EPS((r,t,u,v))*pairing(wedge(e[:,u],e[:,v]),dR)
        out.append(s.factor(total))
    return out

if __name__=='__main__':
    z=(0,0,0,0)
    print('density',density(z),flush=True)
    print('solder',solder_source(z),flush=True)
    for axis in range(4): print('link',axis,link_source(z,axis),flush=True)
