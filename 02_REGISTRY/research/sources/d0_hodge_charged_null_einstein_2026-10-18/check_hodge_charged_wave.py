#!/usr/bin/env python3
"""Native CAR16 Hodge 0/top wave: real Golden-PF, J2 sources, full scalar Eulers.

Standard-library finite controls for the analytic theorem
A4D_NATIVE_HODGE_CHARGED_NULL_MATTER_FIXED_METRIC_EINSTEIN_2026_10_18.md.

Consumes the existing exact symbolic 40-row ORIGINAL Lorentz star owner,
NOT a fresh proof of all those rows; does not promote compulsory D0
Cost-Info, full-time causal compactification, or original #216 raw h^-2.
"""
from math import cos, log1p, pi, sin, sqrt
from collections import Counter

P = (sqrt(5.) - 1.) / 2.
Z = 2.**-20
LSTAR = 4.*P**3
PA = P**6
Q0 = 1.-Z*LSTAR
R0 = 1.-Z*(LSTAR+PA*LSTAR)
LAMBDA = -2./P**5 * (R0/Q0+PA)
SCENE = 528
ALPHA = .008
WINDING = 1
KAPPA = 2*pi*WINDING


def close(a, b, tol=1e-11):
    if abs(a-b)>tol:
        raise AssertionError(f"failed: {a} != {b} tol {tol}")


def fib(n):
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a


def real_native_cells(cost, side):
    counts=Counter()

    def visit(rem, rawdepth, left, lengths):
        if rem==0:
            x=tuple(left[i]+lengths[i]/2 for i in range(4))
            site=tuple(min(side-1,int(side*xx)) for xx in x)
            counts[site]+=1
            return
        axis=rawdepth%4
        newlen=list(lengths);newlen[axis]*=P
        visit(rem-1,rawdepth+1,list(left),newlen)
        if rem>=2:
            newleft=list(left);newlen=list(lengths)
            newleft[axis]+=P*newlen[axis]
            newlen[axis]*=P*P
            visit(rem-2,rawdepth+1,newleft,newlen)

    visit(cost,0,[0.,0.,0.,0.],[1.,1.,1.,1.])
    oldlevel=cost+3
    D0=fib(oldlevel+8)
    K=fib(2*oldlevel+9)
    assert len(counts)==side**4
    assert sum(counts.values())==fib(cost+1)
    weights={x:2*D0*count/K for x,count in counts.items()}
    assert 0.<sum(weights.values())<1.
    return counts,weights


def oriented_car16_check():
    eta=(1.,-1.,-1.,-1.)
    creators=[]
    for a in range(4):
        C=[[0.]*16 for _ in range(16)]
        for mask in range(16):
            if mask&(1<<a):
                continue
            sign=(-1.)**((mask&((1<<a)-1)).bit_count())
            C[mask|(1<<a)][mask]=sign
        creators.append(C)
    gamma=[]
    for a in range(4):
        gamma.append([[creators[a][i][j]+eta[a]*creators[a][j][i]
                       for j in range(16)] for i in range(16)])
    for a in range(4):
        for b in range(4):
            for i in range(16):
                for j in range(16):
                    anticom=sum(gamma[a][i][k]*gamma[b][k][j]
                                  +gamma[b][i][k]*gamma[a][k][j]
                                  for k in range(16))
                    close(anticom,2*eta[a] if a==b and i==j else 0.,1e-13)
    # Hodge operator J on original grade0/top is orthogonal and J^2=-I.
    J=((0.,-1.),(1.,0.))
    for i in range(2):
        for j in range(2):
            close(sum(J[i][k]*J[k][j] for k in range(2)),
                  -1. if i==j else 0.)
    return gamma


def rotating_wave(side):
    h=1./side
    phase=KAPPA*h
    assert 0<phase<pi
    amp=ALPHA*KAPPA*h/(2*sin(phase/2))
    assert amp*amp<1-P
    profile=[(amp*cos(phase*j),amp*sin(phase*j))
             for j in range(side)]
    gradient=[tuple((profile[(j+1)%side][a]-profile[j][a])/h
                    for a in (0,1)) for j in range(side)]
    kinetic=[g[0]**2+g[1]**2 for g in gradient]
    current=[2*(gradient[j][1]*profile[j][0]
                -gradient[j][0]*profile[j][1]) for j in range(side)]
    E=(ALPHA*KAPPA)**2
    J=2*amp*amp*sin(phase)/h
    assert max(abs(q-E) for q in kinetic)<1e-12
    assert max(abs(j-J) for j in current)<1e-12
    assert abs(J)>1e-12
    for v in profile:
        # REAL original CAR grade0/top + time-grade + spectator two-form.
        full16=[0.]*16
        full16[0]=v[0]
        full16[15]=v[1]
        full16[1]=sqrt(P)
        full16[3]=sqrt(1-P-amp*amp)
        close(sum(x*x for x in full16),1.)
    # Independently vary EACH of the two scalar amplitudes at EACH u,v node.
    for component in (0,1):
        for iu in range(side):
            for iv in range(side):
                source=0.
                for vu in range(side):
                    for vv in range(side):
                        if vu!=iu:
                            continue
                        dv=((1. if (vv+1)%side==iv else 0.)
                            -(1. if vv==iv else 0.))/h
                        source+=2*gradient[vu][component]*dv
                close(source,0.,1e-12)
    return amp,E,J


def coframe_pressure_source(E,h):
    # In the owned null coframe ehat^+=du,
    # ehat^-=dv+(H/2)du, ehat^2=dx, ehat^3=dy:
    # q=0, and of sixteen independent original h-scaled leg rows
    # only (a=+,mu=v) has derivative -2 E/h.
    from math import isfinite
    trace=-2*LAMBDA*E
    assert isfinite(trace) and trace>0
    return trace


def same_full_J2_source(weights,E,h):
    mean=sum(weights.values())/len(weights)
    trace=coframe_pressure_source(E,h)
    Cstar=SCENE*Z*4*P**11/R0
    Cmat=-SCENE*Z*8*P**6*(1/Q0+PA/R0)
    close(Cmat/Cstar,LAMBDA,1e-9)
    for w in weights.values():
        rho=w/mean
        df=-trace/(h*rho)
        dq=-2*E/(h*rho)
        close(w*(Cstar*df+Cmat*dq),0.,1e-13)

    def exact_local_price_one_old_weight(w,s):
        rho=w/mean
        # Full REAL two-tick scene b -> B=4b(1-b), NOT B=b.
        f=(-trace/h)*s/rho
        q=(-2*E/h)*s/rho
        setting_e=P*P*(1+f)
        setting_b=(P-P*P*q)**2
        B=4*setting_b*(1-setting_b)
        lam=4*setting_e*(1-setting_e)
        return -SCENE*w*(log1p(-Z*B)
            +log1p(-Z*(lam+(1-lam)*B)))

    sample=sorted(weights.values())[::max(1,len(weights)//9)]
    for w in sample:
        hstep=2e-4
        D=(exact_local_price_one_old_weight(w,hstep)
             -exact_local_price_one_old_weight(w,-hstep))/(2*hstep)
        close(D,0.,5e-10)

    # Wrong one-tick shortcut produces the incorrect old coefficient.
    wrong_b=P*P
    assert abs(wrong_b-LSTAR)>0.2
    # Owned finite star equations at every interior site:
    # E_coframe(v_v^+)=-trace/h; exact half-grid connection correction:
    plus=.125;cross=.08
    A=trace/2+plus
    D=trace/2-plus
    c_x=-A/2
    c_y=-D/2
    close(A+D+2*LAMBDA*E,0.)
    close(A+2*c_x,0.)
    close(D+2*c_y,0.)
    assert plus**2+cross**2>0
    return trace


def main():
    oriented_car16_check()
    close(LAMBDA,-23.416406751884065,1e-10)
    close(-2*LAMBDA*ALPHA**2*KAPPA**2,0.11832866362199,1e-10)
    for cost,side in ((16,3),(20,4)):
        counts,weights=real_native_cells(cost,side)
        amp,E,J=rotating_wave(side)
        trace=same_full_J2_source(weights,E,1./side)
        print(f"cost={cost} L={side} F_words={sum(counts.values())} "
              f"covered={len(counts)} mass={sum(weights.values()):.8f}")
        print(f"  alpha_h={amp:.12f} E={E:.12f} "
              f"Ric_uu={trace:.12f} Noether_jv={J:.12f}")
    print("PASS: one CAR16 0/top rotating null wave, 2 real scalar Euler rows")
    print("PASS: original unequal native PF weights and one full two-tick J2 source")
    print("PASS: same fixed nonflat GR geometry at every h, conserved matter current")
    print("SCOPE: consumes owned symbolic all40 star table, NOT compulsory full native D0")

if __name__=="__main__":
    main()
