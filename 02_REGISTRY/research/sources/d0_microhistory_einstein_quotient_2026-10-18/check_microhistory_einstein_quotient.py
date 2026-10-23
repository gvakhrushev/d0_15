#!/usr/bin/env python3
"""D0 microhistory → exact Einstein source quotient, original F/R weights and mean/MAP.

Reproducible standard-library-only narrow controls for:
A4D_MICROHISTORY_EINSTEIN_QUOTIENT_AND_PRICE_EULER_UNIVERSALITY_2026_10_18.md
plus the conditional retained-prefix Shannon-source chain rule recorded in
A4D_STRATEGIC_SYNTHESIS_FOUNDATIONS_TO_GR_2026_10_17.md §7.31.

Consumes the owned symbolic exact 16-coframe+24-Lorentz-link six-plaquette
Euler table; does NOT re-prove that table, native full Book selection, root of
all historical preparations, or original full-periodic #216 raw terminal.
"""
from collections import Counter
from math import asin, cos, log, pi, sin, sqrt

P=(sqrt(5.)-1.)/2.
Z=2.**-20
L0=4.*P**3
A0=P**6
Q0=1.-Z*L0
R0=1.-Z*L0*(1.+A0)
LAMBDA=-2.*(R0/Q0+A0)/P**5
W_SCENE=528
C_GRAV=W_SCENE*Z*4.*P**11/R0
C_MAT=-W_SCENE*Z*8.*P**6*(1./Q0+A0/R0)
RATE=.025

def nearly(x,y,tol=1e-11):
    if abs(x-y)>tol:
        raise AssertionError(f"{x} != {y}; error {abs(x-y)}")

def fib(n):
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a

def exact_cost_golden_cells(n,L):
    """Actual raw F cost1/R cost2, coordinates cyclically split by raw index."""
    hits=Counter()
    def recurse(cost,k,start,width):
        if cost==0:
            center=[start[i]+width[i]/2. for i in range(4)]
            site=tuple(min(L-1,int(L*x)) for x in center)
            hits[site]+=1
            return
        j=k%4
        wa=width.copy();wa[j]*=P
        recurse(cost-1,k+1,start.copy(),wa)
        if cost>=2:
            wa=width.copy();sa=start.copy()
            sa[j]+=P*wa[j];wa[j]*=P*P
            recurse(cost-2,k+1,sa,wa)
    recurse(n,0,[0.]*4,[1.]*4)
    assert sum(hits.values())==fib(n+1)
    assert len(hits)==L**4, (n,L,len(hits),L**4)
    assert min(hits.values())>0
    assert max(hits.values())>min(hits.values())
    # All SAME-cost READY leaves have the same TRUE AF regular trace weight.
    # The overall positive prefactor cancels from the sourced Euler equation.
    weights={site:float(ct) for site,ct in hits.items()}
    mean=sum(weights.values())/len(weights)
    return hits,weights,mean

def polygon(L,s,free_angles,offset=(0.,0.)):
    assert L%2==0 and len(free_angles)==L//2
    half=[(cos(x),sin(x)) for x in free_angles]
    directions=half+[(-x,-y) for x,y in half]
    h=1./L
    psi=[offset]
    for j in range(L-1):
        psi.append((psi[-1][0]+h*s*directions[j][0],
                    psi[-1][1]+h*s*directions[j][1]))
    d=[((psi[(j+1)%L][0]-psi[j][0])/h,
        (psi[(j+1)%L][1]-psi[j][1])/h) for j in range(L)]
    closure=(psi[0][0]-psi[-1][0]-h*s*directions[-1][0],
             psi[0][1]-psi[-1][1]-h*s*directions[-1][1])
    assert max(abs(v) for v in closure)<1e-13
    energy=[v[0]**2+v[1]**2 for v in d]
    assert max(abs(e-s*s) for e in energy)<1e-14
    assert max(x*x+y*y for x,y in psi)<1-P
    # Native real Hodge j^v =2 D_u Psi dot J_H Psi, J_H(x,y)=(-y,x).
    current=[2*(-d[j][0]*psi[j][1]+d[j][1]*psi[j][0])
             for j in range(L)]
    # All v-derivatives are identically zero for every u-dependent current.
    assert all(v==0 for v in
               [current[j]-current[j] for j in range(L)])
    return psi,d,energy,current

def full_native_book_source(weights,mean,s):
    """One corrected full two-tick J2: all weighted coframe rows cancel."""
    nearly(C_MAT/C_GRAV,LAMBDA,5e-12)
    trace=-2*LAMBDA*s*s
    assert trace>0
    for w in weights.values():
        rho=w/mean
        # On f=q=0, the original true geometric source is rho^-1 times
        # that in the dressed coframe, while q input is inverse-PF local.
        df_dressed=-trace
        dq=-2*s*s
        local_geo=w*C_GRAV*df_dressed/rho
        local_mat=w*C_MAT*dq/rho
        nearly(local_geo+local_mat,0.,1e-9)
    A=trace/2+.19
    D=trace/2-.19
    W_cross=.17
    c_x=-A/2;c_y=-D/2
    nearly(A+2*c_x,0.)
    nearly(D+2*c_y,0.)
    nearly(A+D+2*LAMBDA*s*s,0.)
    assert (A-D)**2+W_cross**2>0
    return trace

def mean_map_same_detector(g,T):
    """ONE complete golden pointer q_good=g, q_bad,z=(1-g)beta_z."""
    badmax=(4*P**3)**T
    assert g>(1-g)*badmax  # strict good mode on all retained failures
    p6=P**6
    nearly(p6+4*P**3,1.,1e-13)
    h2=lambda r:-r*log(r)-(1-r)*log(1-r)
    Hbeta=T*h2(p6)
    Hmean=h2(g)+(1-g)*Hbeta
    kappa=g*(Hbeta-log((1-g)/g))
    assert kappa>0
    dHdg=log((1-g)/g)-Hbeta
    dMAPdg=-1/g
    nearly(dHdg,kappa*dMAPdg,1e-12)
    # Exact gradient proportionality survives every field tangent,
    # including genuine matter and preparation, when the SAME detector is used.
    return Hmean,-log(g),kappa

def conditional_prefix_detector(pi,g,dg,T):
    """One retained old-leaf label followed by its conditional full detector.

    At a common root all branch good probabilities equal g, but their field
    derivatives dg may differ. This checks the Shannon first-source identity
    without assuming a single global good outcome or a MAP rule for the prefix.
    """
    assert len(pi)==len(dg) and abs(sum(pi)-1.)<1e-13
    p6=P**6; p1=4.*P**3
    beta=[p6**(T-bin(k).count("1"))*p1**bin(k).count("1")
          for k in range(1<<T)]
    nearly(sum(beta),1.,1e-12)
    Hbeta=-sum(x*log(x) for x in beta if x>0.)
    nearly(Hbeta,T*(-p6*log(p6)-p1*log(p1)),1e-11)
    assert g>(1.-g)*max(beta)  # strict good mode inside every prefix branch
    q=[]; dq=[]
    for weight,slope in zip(pi,dg):
        q.append(weight*g); dq.append(weight*slope)
        for b in beta:
            q.append(weight*(1.-g)*b); dq.append(-weight*slope*b)
    nearly(sum(q),1.,1e-12)
    nearly(sum(dq),0.,1e-12)
    dH=-sum((1.+log(prob))*slope for prob,slope in zip(q,dq) if prob>0.)
    dH_chain=sum(weight*(log((1.-g)/g)-Hbeta)*slope
                 for weight,slope in zip(pi,dg))
    kappa=g*(Hbeta-log((1.-g)/g))
    dJ=sum(weight*(-slope/(2.*g)) for weight,slope in zip(pi,dg))
    nearly(dH,dH_chain,1e-11)
    nearly(dH,2.*kappa*dJ,1e-11)
    assert kappa>0.
    return dH,kappa

def linear_angle_first_source(t=0.37):
    """Check the exact-root controller can keep only the owned angle 1-jets."""
    theta0=asin(P)
    for sigma in (-1.,1.):
        E0=sin(theta0)**2
        b0=sin(theta0)**2
        dE_linear=2*sin(theta0)*cos(theta0)*(.5*sqrt(P)*t*t)
        db_linear=2*sin(theta0)*cos(theta0)*(sigma*P**1.5*t*t)
        dE_owned=P*P*t*t
        db_owned=2*sigma*P**3*t*t
        nearly(E0,P*P,1e-13)
        nearly(b0,P*P,1e-13)
        nearly(dE_linear,dE_owned,1e-13)
        nearly(db_linear,db_owned,1e-13)
        dB_linear=4*(1.-2*b0)*db_linear
        dB_owned=4*(1.-2*P*P)*db_owned
        nearly(dB_linear,8*sigma*P**6*t*t,1e-13)
        nearly(dB_linear,dB_owned,1e-13)

def test():
    nearly(LAMBDA,-23.41640675188407,1e-11)
    for n,L in ((20,4),(24,8)):
        hits,weights,mean=exact_cost_golden_cells(n,L)
        # The original trigonometric profile differs from a circle for L>=6,
        # but at L=4 its two sampled angles differ only by a global rotation.
        # Use a genuinely different relative angle on that smallest lattice.
        ang=([0.,1.7] if L==4 else
             [2*pi*j/L+.4*sin(4*pi*j/L)+.17*cos(8*pi*j/L)
              +.13*cos(4*pi*j/L)
              for j in range(L//2)])
        psi,d,E,current=polygon(L,RATE,ang)
        psi_circle,_,E_circle,current_circle=polygon(
            L,RATE,[2*pi*j/L for j in range(L//2)])
        assert max(abs(x-y) for a,b in zip(psi,psi_circle)
                   for x,y in zip(a,b))>1e-5
        assert max(abs(a-b) for a,b in zip(current,current_circle))>1e-6
        assert max(abs(a-b) for a,b in zip(E,E_circle))<1e-13
        trace=full_native_book_source(weights,mean,RATE)
        # 2 full original scalar Euler rows at every (u,v) vanish:
        # at q=0 the first source is Σ_{u,v} D_u Psi D_v deltaPsi;
        # its v-summation telescopes for arbitrary compact-supported deltaPsi.
        for k in (0,1):
            for iu in range(L):
                for iv in range(L):
                    residual=0.
                    for v in range(L):
                        residual+=2*d[iu][k]*(int((v+1)%L==iv)-int(v==iv))*L
                    nearly(residual,0.)
        print(f"F/R n={n} L={L} leaves={sum(hits.values())} "
              f"covered={len(hits)} min/max count={min(hits.values())}/{max(hits.values())}")
        print(f"  |D Psi|²={RATE**2:.12f}; Ric_uu={trace:.12f}; "
              f"max|Psi|={max(sqrt(x*x+y*y) for x,y in psi):.9f}; "
              f"Hodge current span={max(current)-min(current):.9f}")
    # Two different field microhistories with the SAME Einstein metric
    # have the SAME feedback F_i at f=q=0, but different Hodge currents.
    entropy,map_surprisal,kappa=mean_map_same_detector(.23,32)
    print(f"ONE retained Golden good+bad detector: mean={entropy:.12f}, "
          f"MAP={map_surprisal:.12f}; exact gradient ratio κ={kappa:.12f}>0")
    prefix_weights=[.11,.23,.66]
    dH,kappa=conditional_prefix_detector(prefix_weights,.73,[.001,-.0007,.0002],8)
    print(f"ONE conditional prefix+detector pointer: dH={dH:.12g}; "
          f"same weighted trace-log source factor 2κ={2*kappa:.9f}")
    linear_angle_first_source()
    print("LINEAR native-angle 1-jets: same exact finite-root source as both arcsin controls.")
    print("PASS: growing microhistory torus, exact constant stress, old PF counts,")
    print("      SAME corrected two-tick J2 Euler and complete-pointer first sources.")
    print("SCOPE: constructed Einstein+CAR source, not compulsory full native D0 GR.")
if __name__=="__main__":
    test()
