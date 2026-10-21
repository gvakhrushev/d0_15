#!/usr/bin/env python3
"""Original six-face G2/STAR + native N=1 GoldenMaster, actual analytic
unrestricted 16 coframe +24 proper-Lorentz +2 real-scalar first-source.

Spatially homogeneous time-slab representation with ALL based temporal
predecessors and spatial outgoing/inverse occurrences. It is a real exact
chain-derivative of the chosen scalar CQ price, NOT a physical selection
of compulsory Book03, and not a globally covariant continuum action.
"""
import numpy as np
from scipy.linalg import expm
from check_star_rank2_seam import (PAIRS,G2,STAR,LORENTZ as L,ETA,I,
                                   orientation,star_density,matter_query)
SGNS={(r,s):orientation(r,s) for r,s in PAIRS}
P=(np.sqrt(5.)-1)/2
Z=2**-20
LP=np.log(1/P)

def wv(f,q,rho=1,tau=.05):
    """Exact ORIGINAL cap-one N1 derivative ratios from real two-query
    conditional report probability; fixed readiness cancels in ratios.
    Includes ORIGINAL sigma-minus, x_null=-tau*f_canonical/rho.
    """
    x=-tau*f/rho;y=tau*q/rho
    def dat(x,y):
        E=P*P*(1+x);ell=4*E*(1-E)
        b=P-P*P*y;B=4*b*b*(1-b*b)
        A=ell+(1-ell)*B
        r=Z*(A+B)-Z*Z*A*B
        ellx=4*P*P*(1-2*E)
        rx=Z*(1-Z*B)*ellx*(1-B)
        By=-8*P*P*b*(1-2*b*b)
        ry=Z*((1-Z*A)*By+(1-Z*B)*(1-ell)*By)
        hp=np.log((1-r)/r)/LP
        return hp*rx,hp*ry
    den=dat(0,0)[0]
    a,b=dat(x,y)
    return a/den,-b/den

def wedge(a,b):
    return np.array([a[i]*b[j]-a[j]*b[i] for i,j in PAIRS])

def bvec(F):
    T=F@ETA
    return np.array([T[i,j] for i,j in PAIRS])

def facelist(nodes,j,r,s):
    Uj=nodes[j]['U'];nxt=nodes[j+1]['U']
    # r=0 (time) has a real future Ui(t+h). A spatial shift of a
    # homogeneous field has the SAME current Ui(t), not a new time.
    a=(j,r,False,Uj[r])
    b=(j+1 if r==0 else j,s,False,nxt[s] if r==0 else Uj[s])
    c=(j,r,True,np.linalg.inv(Uj[r]))
    d=(j,s,True,np.linalg.inv(Uj[s]))
    return (a,b,c,d)

def full_source(nodes,h,rhos=None,tau=.05):
    """Return actual SOURCE for ALL time nodes; boundary Euleri are reported
    but not solved, and must be treated as real collar reactions.
    Group coordinate for links is LEFT multiplication delta U=X U.
    Two matter fields use exact time-forward differences, with the second
    carrying fixed x-forward gradient epsilon. Spatial predecessor scalar
    contributions cancel only because the field is homogeneous in x.
    """
    n=len(nodes)
    Ee=np.zeros((n,4,4),float)
    EU=np.zeros((n,4,6),float)
    EG=np.zeros((n,2),float)
    qlist=[];flist=[];wlist=[];vlist=[]
    for j in range(n-1):
        e=nodes[j]['e']
        volume=0.
        epart=np.zeros((4,4))
        upart=np.zeros((n,4,6))
        for r,s in PAIRS:
            factors=facelist(nodes,j,r,s)
            A,B,invA,invB=[f[3] for f in factors]
            prod=[I,A,A@B,A@B@invA,A@B@invA@invB]
            Pmat=prod[-1]
            Pinv=np.linalg.inv(Pmat)
            R=(Pmat-Pinv)/2
            u,v=[i for i in range(4) if i not in (r,s)]
            beta=wedge(e[:,u],e[:,v])
            coeff=SGNS[r,s]*(beta*G2)@STAR/h**2
            volume+=coeff@bvec(R)
            for a in range(4):
                va=np.zeros(4);va[a]=1.
                jet=STAR@bvec(R)
                epart[a,u]+=SGNS[r,s]*(wedge(va,e[:,v])*G2)@jet/h**2
                epart[a,v]+=SGNS[r,s]*(wedge(e[:,u],va)*G2)@jet/h**2
            suffix=[None]*5;suffix[4]=I
            for t in range(3,-1,-1):
                suffix[t]=factors[t][3]@suffix[t+1]
            for t,(site,axis,invmat,Ufac) in enumerate(factors):
                for k,X in enumerate(L):
                    dF=-Ufac@X if invmat else X@Ufac
                    dP=prod[t]@dF@suffix[t+1]
                    dR=(dP+Pinv@dP@Pinv)/2
                    upart[site,axis,k]+=coeff@bvec(dR)
        q=matter_query(nodes[j]).real
        rho=1 if rhos is None else rhos[j]
        w,vv=wv(volume,q,rho,tau)
        Ee[j]+=w*epart
        EU+=w*upart
        g=e.T@ETA@e
        gg=np.linalg.inv(g)
        pp=nodes[j]['v']
        currents=gg@pp.T  # (coordinate mu, scalar A)
        for a in range(4):
            for mu in range(4):
                Ee[j,a,mu]+=vv*(-2)*sum(
                    (ETA@e@currents[:,i])[a]*currents[mu,i]
                    for i in range(2))
        for i in range(2):
            value=2*vv*currents[0,i]/h
            EG[j,i]-=value
            EG[j+1,i]+=value
        qlist.append(q);flist.append(volume)
        wlist.append(w);vlist.append(vv)
    return dict(e=Ee,U=EU,psi=EG,
                f=np.array(flist),q=np.array(qlist),
                w=np.array(wlist),v=np.array(vlist))

def unit_test():
    """Independent literal original six-face complex-step controls."""
    rng=np.random.default_rng(678)
    h=.047
    nodes=[]
    for j in range(4):
        e=np.diag(rng.uniform(.8,1.3,4))
        e+=rng.uniform(-.05,.05,(4,4))
        U=np.array([expm(h*sum(rng.normal(scale=.4)*X for X in L))
                    for _ in range(4)])
        v=rng.normal(scale=.07,size=(2,4))
        nodes.append(dict(e=e,U=U,v=v))
    actual=full_source(nodes,h)
    j=1;dx=1e-19
    for a,mu in [(0,1),(1,0),(2,3),(1,1)]:
        k=[dict(e=c['e'].astype(complex),
                U=c['U'].astype(complex),
                v=c['v'].astype(complex)) for c in nodes]
        k[j]['e'][a,mu]+=1j*dx
        dff=star_density(k[j],k[j+1],h).imag/dx
        dqq=matter_query(k[j]).imag/dx
        expected=actual['w'][j]*dff+actual['v'][j]*dqq
        assert abs(actual['e'][j,a,mu]-expected)<1e-6
    for axis,kid in [(0,2),(1,3),(2,0),(3,5)]:
        x=[dict(e=c['e'].astype(complex),
                U=c['U'].astype(complex),
                v=c['v'].astype(complex)) for c in nodes]
        old=x[j]['U'][axis].copy()
        x[j]['U'][axis]=expm(1j*dx*L[kid])@old
        prev=star_density(x[j-1],x[j],h).imag/dx
        cur=star_density(x[j],x[j+1],h).imag/dx
        expected=actual['w'][j-1]*prev+actual['w'][j]*cur
        assert abs(actual['U'][j,axis,kid]-expected)<1e-6
    print("PASS original analytic all16+24 N1 CQ jets vs literal independent complex-step")
if __name__=="__main__":
    unit_test()
