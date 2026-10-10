#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact all-role commuting-B extension of the curved shared-link flux identity.

Every link in every role is an independent real Cayley(a*B) element with
B=K1+K2+K3.  The checker assembles all six based faces on an L=4 periodic
warp and verifies:
  * every face curvature is z_rs B;
  * spatial faces contribute zero to Xi_11,Xi_22,Xi_33;
  * those three diagonal slots still reconstruct exactly the three temporal
    face curvatures by the existing T_f matrix;
  * the full temporal-link B Euler row equals the backward divergence of
    w_i*c_0i, c_0i^2-3 z_0i^2=1, even with nonidentity spatial links.

This closes spatial compensation inside the same commuting subgroup.  It does
not cover noncommuting Lorentz generators.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import numpy as np

import a4d_coupled_boost_curved_realizability_check as C
import a4d_identity_quarter_nonlinear_response_check as N

I, B, ETA = C.I, C.B, C.ETA
PAIRS = N.PAIRS


def ck(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name, flush=True)


def shift(x, r, step=1, L=4):
    return tuple((v + step*(j == r)) % L for j,v in enumerate(x))


def face_factors(links, x, r, s):
    return [links[x,r], links[shift(x,r),s],
            C.adjoint(links[shift(x,s),r]), C.adjoint(links[x,s])]


def prod(fs):
    p=I.copy()
    for a in fs:
        p=p@a
    return p


def coframe(sample):
    return np.diag([F(1),F(1),sample,sample]).astype(object)


def face_weight(S,r,s):
    a,b=[j for j in range(4) if j not in (r,s)]
    return N.orient(r,s)*N.weight(N.wedge(S[:,a],S[:,b]))


def face_diag_memory(S,r,s,curvature):
    """Actual Xi_11,Xi_22,Xi_33 from the Gram lift at one based face."""
    qi=N.inverse(S.T@ETA@S)
    a,b=[j for j in range(4) if j not in (r,s)]
    out=[]
    for j in (1,2,3):
        dq=np.zeros((4,4),dtype=object); dq[j,j]=1
        ds=S@qi@dq*F(1,2)
        dw=N.orient(r,s)*N.weight(
            N.wedge(ds[:,a],S[:,b])+N.wedge(S[:,a],ds[:,b]))
        out.append(np.sum(dw*curvature))
    return np.array(out,dtype=object)


def temporal_B_euler(links,samples,x):
    """Full independent variation of the one temporal edge along B."""
    total=F(0)
    for r,s in PAIRS:
        if r!=0:
            continue
        for base,corner in ((x,0),(shift(x,s,-1),2)):
            fs=face_factors(links,base,r,s)
            p=prod(fs); pinv=C.adjoint(p)
            varied=fs.copy()
            varied[corner]=(fs[corner]@B if corner<2 else -B@fs[corner])
            dp=prod(varied)
            dc=(dp + pinv@dp@pinv)*F(1,2)
            S=coframe(samples[base[1]])
            total += np.sum(face_weight(S,r,s)*dc)
    return total


def main():
    L=4
    sites=list(product(range(L),repeat=4))
    samples=(F(1),F(51,50),F(26,25),F(51,50))

    # Independent values in all roles/all coordinates, safely inside chart.
    amp={}
    for x in sites:
        for r in range(4):
            n=(3*x[0]+5*x[1]+7*x[2]+11*x[3]+13*r) % 13
            amp[x,r]=F(n-6,24)
    links={(x,r):C.cayley(amp[x,r]) for x in sites for r in range(4)}

    ztemp={}
    ctemp={}
    xi={}
    spatial_diag_nonzero=0

    for x in sites:
        S=coframe(samples[x[1]])
        xi[x]=np.zeros(3,dtype=object)
        ztemp[x]=np.zeros(3,dtype=object)
        ctemp[x]=np.zeros(3,dtype=object)
        for r,s in PAIRS:
            fs=face_factors(links,x,r,s)
            p=prod(fs); pinv=C.adjoint(p)
            curv=(p-pinv)*F(1,2)
            z=curv[0,1]
            ck_face=np.array_equal(curv,z*B)
            if not ck_face:
                raise AssertionError(f"FACE_CURVATURE_NOT_B_{x}_{r}_{s}")

            dmem=face_diag_memory(S,r,s,curv)
            xi[x]+=dmem
            if r>0:
                if np.any(dmem):
                    spatial_diag_nonzero+=1
            else:
                k=s-1
                ztemp[x][k]=z
                # Right variation of the temporal factor along B.
                dc=(p@B + B@pinv)*F(1,2)
                c=dc[0,1]
                if not np.array_equal(dc,c*B):
                    raise AssertionError("TEMPORAL_FACE_DERIVATIVE_NOT_B")
                if c*c-3*z*z != 1:
                    raise AssertionError("TEMPORAL_FACE_HYPERBOLA")
                ctemp[x][k]=c

    ck("ALL_SPATIAL_FACES_ZERO_DIAGONAL_MEMORY", spatial_diag_nonzero==0)

    for x in sites:
        f=samples[x[1]]
        Tf=np.array([[1/f**2,-1,-1],[-1/f,f,-f],[-1/f,-f,f]],dtype=object)
        ck("DIAGONAL_MEMORY_RECOVERS_TEMPORAL_CURVATURE_"+str(x),
           np.array_equal(Tf@xi[x],ztemp[x]))

    # Independent temporal-edge variation with every spatial link nonidentity.
    for x in sites:
        actual=temporal_B_euler(links,samples,x)
        expected=F(0)
        for i in (1,2,3):
            prev=shift(x,i,-1)
            f=samples[x[1]]; fp=samples[prev[1]]
            w=f*f if i==1 else f
            wp=fp*fp if i==1 else fp
            expected += w*ctemp[x][i-1]-wp*ctemp[prev][i-1]
        ck("FULL_TEMPORAL_B_EULER_FLUX_"+str(x), actual==expected)

    # Plane sum: transverse divergences cancel with actual all-role fields.
    planes=[[x for x in sites if x[1]==n] for n in range(L)]
    eplane=[sum(temporal_B_euler(links,samples,x) for x in xs) for xs in planes]
    qplane=[sum(samples[n]**2*ctemp[x][0] for x in xs)
            for n,xs in enumerate(planes)]
    ck("ALLROLE_PLANE_CONSERVATION",
       eplane==[qplane[n]-qplane[n-1] for n in range(L)])

    print("RESULT COUPLED-BOOST-ALLROLE-COMMUTING-B-FLUX-IDENTITY-CERTIFIED",
          flush=True)
    print("RESULT SPATIAL-B-LINKS-DO-NOT-ALTER-DIAGONAL-MEMORY-INVERSE",flush=True)
    print("RESULT SAME-OWNER-SUM-BARRIER-EXTENDS-TO-ALLROLE-COMMUTING-B",flush=True)


if __name__=="__main__":
    main()
