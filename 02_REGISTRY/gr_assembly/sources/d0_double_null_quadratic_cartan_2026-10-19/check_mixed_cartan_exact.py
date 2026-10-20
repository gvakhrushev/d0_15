#!/usr/bin/env python3
"""Exact original six-based-plaquette Palatini mixed a*b coefficient.

Proves original full 24 proper-link + 16 independent coframe Euler at the
first mixed order for H=a (A_2 x+A_3 y), J=b (B_2 x+B_3 y).
All arithmetic is in Q[a,b]/(a^2,b^2); coordinates x,y symbolic.
The original full coframe/link first variation is taken BEFORE the
mixed-order link solution is substituted. No exact finite all-order root,
Book admission, preparation, controller, or physical GR closure is claimed.
"""
import itertools
import sympy as s

I=s.eye(4)
O=s.zeros(4)
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
E=lambda i,j:s.Matrix(4,4,lambda k,l:int(i==k and j==l))
N2,N3=E(1,2)+E(2,0),E(1,3)+E(3,0)
M2,M3=E(0,2)+E(2,1),E(0,3)+E(3,1)
Boost,Rot=E(1,1)-E(0,0),E(2,3)-E(3,2)
pairs=list(itertools.combinations(range(4),2))
G=[(E(i,j)-E(j,i))*eta for i,j in pairs]
half,eighth=s.Rational(1,2),s.Rational(1,8)
AA,BB=(1,0),(0,1)
CORR=None

def require(x,label):
    if not x:
        raise ArithmeticError(label)

class Jet:
    """Matrix coefficient tuple for 1,a,b,ab (a*a=b*b=0)."""
    def __init__(self,c0=None,ca=None,cb=None,cab=None):
        self.c=[O if t is None else t for t in (c0,ca,cb,cab)]
    def __add__(self,d):
        return Jet(*(a+b for a,b in zip(self.c,d.c)))
    def __sub__(self,d):
        return Jet(*(a-b for a,b in zip(self.c,d.c)))
    def __mul__(self,d):
        A,B=self.c,d.c
        return Jet(A[0]*B[0],
                   A[0]*B[1]+A[1]*B[0],
                   A[0]*B[2]+A[2]*B[0],
                   A[0]*B[3]+A[1]*B[2]+A[2]*B[1]+A[3]*B[0])
    def l_inv(self):
        return Jet(*(eta*a.T*eta for a in self.c))
    def left(self,X):
        return Jet(*(X*a for a in self.c))
    def right(self,X):
        return Jet(*(a*X for a in self.c))
    def times(self,c):
        return Jet(*(c*a for a in self.c))

one=Jet(I)

def shift(z,axis,k=1):
    p=list(z);p[axis]+=k
    return tuple(p)

def coframe(z):
    x,y=z[2],z[3]
    H=AA[0]*x+AA[1]*y
    J=BB[0]*x+BB[1]*y
    return Jet(I,half*H*E(1,0),half*J*E(0,1))

def link(z,r,back=False):
    """exp(omega_r) through mixed order at h=1; LC + Cartan correction."""
    x,y=z[2],z[3]
    H=AA[0]*x+AA[1]*y
    J=BB[0]*x+BB[1]*y
    W=(H*BB[0]-J*AA[0],H*BB[1]-J*AA[1])
    if r==0:
        T=Jet(I,half*(AA[0]*N2+AA[1]*N3),O,
              eighth*(W[0]*M2+W[1]*M3))
    elif r==1:
        T=Jet(I,O,half*(BB[0]*M2+BB[1]*M3),
              -eighth*(W[0]*N2+W[1]*N3))
    elif r==2:
        T=Jet(I,O,O,-eighth*W[0]*Boost)
    else:
        T=Jet(I,O,O,-eighth*W[1]*Boost)
    if CORR is not None:
        T=Jet(T.c[0],T.c[1],T.c[2],T.c[3]+CORR[r])
    return T.l_inv() if back else T

def edges(z,r,t):
    return ((z,r,False),(shift(z,r),t,False),
            (shift(z,t),r,True),(z,t,True))

def jm(a,b):
    return [a[0]*b[0],
            a[0]*b[1]+a[1]*b[0],
            a[0]*b[2]+a[2]*b[0],
            a[0]*b[3]+a[1]*b[2]+a[2]*b[1]+a[3]*b[0]]

def scalar_pair(e,u,v,R):
    """Exactly the based G2(e_u wedge e_v, star b(R))."""
    out=[s.Integer(0)]*4
    RR=[X*eta for X in R.c]
    for a,b in pairs:
        c,d=[k for k in range(4) if k not in (a,b)]
        sign=s.LeviCivita(a,b,c,d)
        vec=lambda i,j:[T[i,j] for T in e.c]
        p=jm(vec(a,u),vec(b,v))
        n=jm(vec(b,u),vec(a,v))
        w=[p[k]-n[k] for k in range(4)]
        val=jm(w,[X[c,d] for X in RR])
        for k in range(4):
            out[k]+=sign*val[k]
    return out

def plaquette(z,r,t,target=None,axis=None,X=None):
    P=one
    dP=Jet()
    for at,a,back in edges(z,r,t):
        U=link(at,a,back)
        hit=(X is not None and at==target and a==axis)
        dU=(U.right(-X) if back else U.left(X)) if hit else Jet()
        dP=dP*U+P*dU
        P=P*U
    return P,dP

def link_rows(z):
    result=[]
    for axis in range(4):
        for X in G:
            value=[s.Integer(0)]*4
            for r,t in pairs:
                if axis not in (r,t):
                    continue
                other=t if axis==r else r
                u,v=[k for k in range(4) if k not in (r,t)]
                for base in (z,shift(z,other,-1)):
                    P,dP=plaquette(base,r,t,z,axis,X)
                    Pi=P.l_inv()
                    dR=(dP+Pi*dP*Pi).times(half)
                    q=scalar_pair(coframe(base),u,v,dR)
                    sign=s.LeviCivita(r,t,u,v)
                    value=[x+sign*y for x,y in zip(value,q)]
            result.append(s.expand(value[3]))
    return s.Matrix(result)

def replace_column(e,col,internal):
    q=Jet(*(m.copy() for m in e.c))
    for k in range(4):
        for a in range(4):
            q.c[k][a,col]=int(a==internal) if k==0 else 0
    return q

def solder_rows(z):
    result=[s.Integer(0)]*16
    e=coframe(z)
    for r,t in pairs:
        u,v=[k for k in range(4) if k not in (r,t)]
        sign=s.LeviCivita(r,t,u,v)
        P,_=plaquette(z,r,t)
        R=(P-P.l_inv()).times(half)
        for a in range(4):
            result[4*a+u]+=sign*scalar_pair(replace_column(e,u,a),u,v,R)[3]
            result[4*a+v]+=sign*scalar_pair(replace_column(e,v,a),u,v,R)[3]
    return s.Matrix([s.expand(x) for x in result])

def flat_hessian():
    """Exact quadratic homogeneous link action on original six faces."""
    M=s.zeros(24)
    for r,t in pairs:
        u,v=[k for k in range(4) if k not in (r,t)]
        sign=s.LeviCivita(r,t,u,v)
        for j,X in enumerate(G):
            for k,Y in enumerate(G):
                value=sign*scalar_pair(Jet(I),u,v,Jet(X*Y-Y*X))[0]
                M[6*r+j,6*t+k]=value
                M[6*t+k,6*r+j]=value
    return M

def correction(A,B):
    ax,ay=A
    bx,by=B
    dx,dy=ax*bx,ay*by
    w=ax*by-ay*bx
    return [
      eighth*(dx*M2+dy*M3+w*Rot),
      eighth*(dx*N2+dy*N3-w*Rot),
      eighth*(w*(M3-N3)-dy*Rot),
      eighth*(w*(N2-M2)+dx*Rot),
    ]

if __name__=="__main__":
    x,y=s.symbols("x y",real=True)
    z=(0,0,x,y)
    M=flat_hessian()
    require(M.rank()==24 and M.det()==256,"flat Cartan Hessian rank/determinant")
    require(M.eigenvals()=={s.Integer(2):4,s.Integer(-2):4,
                           s.Integer(1):8,s.Integer(-1):8},
            "flat Hessian eigenvalues")
    print("PASS exact flat 24x24 Cartan Hessian det=256, spectrum 2^4 -2^4 1^8 -1^8")
    for A,B in (((1,0),(1,0)),((1,0),(0,1)),
                ((0,1),(1,0)),((0,1),(0,1))):
        AA,BB=A,B
        CORR=None
        dx,dy=A[0]*B[0],A[1]*B[1]
        d=dx+dy
        w=A[0]*B[1]-A[1]*B[0]
        wanted=s.zeros(24,1)
        # Generator G_23=(E_23-E_32)*eta=-Rot
        wanted[5]=-s.Rational(1,4)*w
        wanted[11]=s.Rational(1,4)*w
        wanted[17]=s.Rational(1,4)*dy
        wanted[23]=-s.Rational(1,4)*dx
        source=link_rows(z)
        require(source==wanted,"native link source coefficient at "+str((A,B)))
        sol=-M.inv()*source
        guess=correction(A,B)
        for r in range(4):
            matrix=sum((sol[6*r+j]*G[j] for j in range(6)),O)
            require(matrix==guess[r],"explicit Cartan correction")
        CORR=guess
        require(link_rows(z)==s.zeros(24,1),"all 24 corrected link rows")
        expected=s.zeros(16,1)
        expected[4*2+2]=-s.Rational(1,4)*d
        expected[4*3+3]=-s.Rational(1,4)*d
        require(solder_rows(z)==expected,"all 16 solder rows")
        P,_=plaquette(z,0,1)
        require(P.c[3]==(d*Boost+w*Rot)/4,
                "mixed uv plaquette stores dot/area")
        P,_=plaquette(z,2,3)
        require(P.c[3]==-w*Boost/4,
                "mixed xy plaquette stores oriented area")
        print("PASS original all 24 links, all 16 coframe, both mixed plaquette signatures:",
              A,B,"dot",d,"wedge",w)
    print("PASS symbolic x,y, four bilinear basis pairs ⇒ arbitrary affine slopes")
    print("SCOPE: exact coefficient [a*b] and linear flat Hessian; no all-order finite root, price, or GR closure.")
