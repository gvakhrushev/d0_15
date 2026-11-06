"""Original full 42-coordinate N=1 CQ scalar price: interval-valid model.

All original canonical six based Lorentz G2*STAR faces, two real CAR fields,
actual p=phi^-1, z=2^-20, and same original sigma-minus detector transported
by x_null=-x_canonical. One spatial-homogeneous two-time-interval carrier,
one unrestricted 16-coframe +24 proper-Lorentz+2 scalar interior node.
Fixed collars are SHA-verified exact decimal rationals from inputs.py.

The iv.mpc Taylor remainder is PROVEN, unlike mpmath.iv.expm's tolerance
stopping rule. No Einstein proxy, compensator or free alternative sigma.
"""
from __future__ import annotations
from math import factorial
from mpmath import mp, iv
from inputs import get_inputs

COLLAR, CENTER = get_inputs()
PAIRS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
def levi(a):
    if len(set(a))<4:return 0
    return (-1)**sum(a[i]>a[j] for i in range(4) for j in range(i+1,4))

class CQ:
    def __init__(self,ctx,weights=("1","1")):
        self.c=ctx
        self.m=lambda v:ctx.mpf(str(v))
        self.h=self.m(COLLAR["h"])
        self.tau=self.m(".05")
        self.eta=ctx.diag([1,-1,-1,-1])
        self.I=ctx.eye(4)
        self.rho=[self.m(v) for v in weights]
        self.L=[]
        for j in (1,2,3):
            X=ctx.zeros(4)
            X[0,j]=X[j,0]=1
            self.L.append(X)
        for i,j in ((1,2),(1,3),(2,3)):
            X=ctx.zeros(4)
            X[i,j]=1
            X[j,i]=-1
            self.L.append(X)
        self.E=[];self.U=[]
        for j in range(3):
            ee=ctx.diag([self.m(v) for v in COLLAR["e_diag"][j]])
            uu=[self.I]+[self._boost(k,w) for k,w in enumerate(COLLAR["spatial_boost_ks"][j])]
            self.E.append(ee)
            self.U.append(uu)
        self.psi=[[self.m(COLLAR["psi1"][j]),self.m(COLLAR["psi2"][j])]
                  for j in range(3)]
        p=(ctx.sqrt(5)-1)/2
        self.p=p
        self.Z=self.m(2)**(-20)
        kappa=2*p**(-5)*(
            (1-self.Z*4*p**3*(1+p**6))/(1-self.Z*4*p**3)+p**6)
        self.amp=1/ctx.sqrt(2*kappa)
        lp=ctx.log(1/p)
        b0=4*p*p*(1-p*p)
        ell0=b0
        A0=ell0+(1-ell0)*b0
        self.r0=self.Z*(A0+b0)-self.Z*self.Z*A0*b0
        self.ent0=-(self.r0*ctx.log(self.r0)+(1-self.r0)*ctx.log(1-self.r0))/lp
        hp=ctx.log((1-self.r0)/self.r0)/lp
        rx0=self.Z*(1-self.Z*b0)*4*p*p*(1-2*p*p)*(1-b0)
        self.norm=-(self.tau*hp*rx0)**(-1)
        self.lp=lp
        self.K=[[levi(PAIRS[i]+PAIRS[j]) for j in range(6)] for i in range(6)]
        self.last_clicks=[]

    def _boost(self,j,v):
        t=self.h*self.m(v)
        c=(self.c.exp(t)+self.c.exp(-t))/2
        s=(self.c.exp(t)-self.c.exp(-t))/2
        B=self.c.eye(4)
        B[0,0]=B[j+1,j+1]=c
        B[0,j+1]=B[j+1,0]=s
        return B

    def _rigorous_expm(self,X):
        """Certified complex 4x4 exp for the ENTIRE rectangular input box.

        Require ||X||_inf < 1. Y=X/2^11. Its degree-30 Taylor tail has
        ||tail||_inf <= exp(1/2048)/(31!*2048^31) < 10^-120.
        Strict last inequality is checked with integer arithmetic using
        exp(1/2048)<2. Add a rectangular complex 1e-120 interval to every
        entry; 11 interval matrix squarings then enclose true exp(X).
        """
        if self.c is not iv:
            return self.c.expm(X)  # point candidate, never a proof bound
        norm=max(sum((abs(X[i,j]).b for j in range(4)),iv.mpf(0))
                 for i in range(4))
        assert norm<iv.mpf(1),("full complex chart exp norm exceeded",norm)
        scale=2**11
        N=30
        assert 2*10**120 < factorial(N+1)*scale**(N+1)
        Y=X/scale
        total=iv.eye(4)
        term=iv.eye(4)
        for n in range(1,N+1):
            term=(term*Y)/n
            total+=term
        slack=iv.mpc(["-1e-120","1e-120"],["-1e-120","1e-120"])
        for i in range(4):
            for j in range(4):
                total[i,j]+=slack
        for _ in range(11):
            total=total*total
        return total

    def nodes(self,z):
        C=self.c
        e=self.E[1].copy()
        U=list(self.U[1])
        ps=[list(q) for q in self.psi]
        for i in range(4):
            for j in range(4):
                e[i,j]+=z[4*i+j]
        for r in range(4):
            X=C.zeros(4)
            for k in range(6):
                X+=z[16+6*r+k]*self.L[k]
            U[r]=self._rigorous_expm(self.h*X)*U[r]
        ps[1][0]+=z[40]
        ps[1][1]+=z[41]
        return e,U,ps

    def curvature(self,e,U,V):
        C=self.c
        value=C.mpc(0) if C is mp else C.mpc([0,0],[0,0])
        for r,s in PAIRS:
            # Based true original 4x4 link plaquette.
            if r==0:
                P=U[r]*V[s]*(self.eta*U[r].T*self.eta)*(self.eta*U[s].T*self.eta)
            else:
                P=U[r]*U[s]*(self.eta*U[r].T*self.eta)*(self.eta*U[s].T*self.eta)
            # Every real original Lorentz generator exponent remains in SO+.
            RR=(P-self.eta*P.T*self.eta)/2
            B=RR*self.eta
            u,v=[i for i in range(4) if i not in (r,s)]
            wedge=[e[a,u]*e[b,v]-e[b,u]*e[a,v] for a,b in PAIRS]
            blade=[B[a,b] for a,b in PAIRS]
            value+=levi((r,s,u,v))*sum(
                -wedge[a]*self.K[a][b]*blade[b]
                for a in range(6) for b in range(6) if self.K[a][b])
        return value/self.h**2

    def price(self,z):
        C=self.c
        e,U,ps=self.nodes(z)
        result=self.m(0)
        clicks=[]
        for j in (0,1):
            co=self.E[0] if j==0 else e
            us=self.U[0] if j==0 else U
            vs=U if j==0 else self.U[2]
            f=self.curvature(co,us,vs)
            g=(co.T*self.eta*co)**-1
            Q=self.m(0)
            for a in (0,1):
                v=C.matrix([(ps[j+1][a]-ps[j][a])/self.h,
                       self.amp if a==1 else self.m(0),
                       self.m(0),self.m(0)])
                Q+=(v.T*g*v)[0]
            rho=self.rho[j]
            # Same originally paid sigma-minus N=1 scalar price.
            x=-self.tau*f/rho
            y=self.tau*Q/rho
            E=self.p*self.p*(1+x)
            ell=4*E*(1-E)
            b=self.p-self.p*self.p*y
            B=4*b*b*(1-b*b)
            A=ell+(1-ell)*B
            click=self.Z*(A+B)-self.Z*self.Z*A*B
            clicks.append(click)
            entropy=-(click*C.log(click)+(1-click)*C.log(1-click))/self.lp
            result+=self.norm*rho*(entropy-self.ent0)
        self.last_clicks=clicks
        return result

def rational_center(ctx):
    return [ctx.mpf(v) for v in CENTER["z42"]]
