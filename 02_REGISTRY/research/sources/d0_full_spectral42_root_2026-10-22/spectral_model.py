"""Declared paired-Hodge spectral action on the unchanged original 42 map.
This is not a compulsory native Book03 action-selection theorem.
"""
from mpmath import mp,iv
from original_model import CQ
class Spectral42(CQ):
    def __init__(self,ctx):
        super().__init__(ctx)
        self.beta=2*self.p**2
        self.mult=ctx.mpf(528)
    def _rigorous_expm(self,X):
        # Keep the imported owner's preconditions active under python -O.
        if self.c is iv:
            from math import factorial
            bound=max(sum((abs(X[i,j]).b for j in range(4)),iv.mpf(0)) for i in range(4))
            if not bound<iv.mpf(1):raise RuntimeError('complex exponential chart failed')
            if not 2*10**120 < factorial(31)*2048**31:raise RuntimeError('Taylor tail failed')
        return super()._rigorous_expm(X)
    def operands(self,z):
        C=self.c;e,U,ps=self.nodes(z);out=[]
        for j in (0,1):
            co=self.E[0] if j==0 else e
            us=self.U[0] if j==0 else U
            vs=U if j==0 else self.U[2]
            f=self.curvature(co,us,vs)
            g=(co.T*self.eta*co)**-1
            Q=C.mpf(0)
            for a in (0,1):
                v=C.matrix([(ps[j+1][a]-ps[j][a])/self.h,
                             self.amp if a==1 else C.mpf(0),0,0])
                Q+=(v.T*g*v)[0]
            out.extend((-self.tau*f,self.tau*Q))
        return out
    def bands(self,z):
        q=self.operands(z);out=[]
        for x,y in zip(q[::2],q[1::2]):
            E=self.p**2*(1+x);L=4*E*(1-E)
            b=self.p-self.p**2*y;B=4*b*b*(1-b*b);A=L+(1-L)*B
            out.extend((A,B))
        return out
    def price(self,z):
        C=self.c;bands=self.bands(z)
        Z=2*self.mult*sum(C.exp(-self.beta*v) for v in bands)
        for v in bands:
            if C is iv and (1-self.Z*v).real.a<=0:raise RuntimeError('log branch not validated')
        if C is iv and Z.real.a<=0:raise RuntimeError('heat log branch not validated')
        J=-self.mult*sum(C.log(1-self.Z*v) for v in bands)
        return 6*(C.log(Z)/self.beta+J)

def gradient(model,z,step):
    C=model.c;out=[]
    for k in range(len(z)):
        v=list(z);v[k]+=C.mpc(0,step)
        out.append(model.price(v).imag/step)
    return C.matrix(out)
