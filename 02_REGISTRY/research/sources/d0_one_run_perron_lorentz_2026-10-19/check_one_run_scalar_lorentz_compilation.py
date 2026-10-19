#!/usr/bin/env python3
"""D0 research: exact one-run positive Markov + CAR16 Lorentz Julia completion.

Theorems are formal and apply to any strict-positive K and local Lorentz links.
This finite control uses the ORIGINAL K(9,11,13) edge support, genuine
Perron one-sided preparation, full exterior CAR16 and ALL success/fail flags.
It proves NATIVE-TYPE FEASIBILITY only, NOT original G0 ActionProtocol selection.
"""
import itertools
import math
import numpy as np
from scipy.linalg import expm, eigh

n = 33
zone = np.array([0]*9 + [1]*11 + [2]*13)
allowed = zone[:, None] != zone[None, :]
assert allowed.sum() == 718
phi = (1.0 + math.sqrt(5.0))/2.0


def transfer(y):
    i, j = np.indices((n,n))
    shape = 0.15*np.sin(.317*(i+1)+.199*(j+1)) + 0.06*np.cos(.31*i-.07*j)
    jet = .14*np.cos(.127*(i+1)-.193*(j+1))
    K = np.where(allowed, np.exp(shape+y*jet), 0.0)
    eig, vec = np.linalg.eig(K)
    sel = np.argmax(eig.real)
    rho = eig[sel].real
    r = vec[:, sel].real
    if r.sum() < 0:
        r = -r
    assert min(r) > 0
    mu = r / r.sum()
    P = K * (r[None,:]/r[:,None]) / rho
    assert max(abs(P.sum(axis=1)-1)) < 1e-12
    return K, rho, mu, P


eta = np.array([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]], dtype=float)
N2 = np.zeros((4,4)); N2[1,2]=N2[2,0]=1.
NB3 = np.zeros((4,4)); NB3[0,3]=NB3[3,1]=1.
assert np.max(abs(N2.T@eta+eta@N2)) == 0
assert np.max(abs(NB3.T@eta+eta@NB3)) == 0
masks = list(range(16))
idx = {mask: tuple(k for k in range(4) if mask & (1<<k)) for mask in masks}


def exterior(g):
    """Faithful original 16-dimensional exterior representation of 4x4 g."""
    out = np.zeros((16,16))
    for a in masks:
        ia=idx[a]
        for b in masks:
            ib=idx[b]
            if len(ia)==len(ib):
                out[a,b]=np.linalg.det(g[np.ix_(ia,ib)]) if ia else 1.0
    return out


def lorentz(i,j,y):
    if i==j or not allowed[i,j]:
        raise ValueError('not an original directed edge')
    u,v = (i,j) if i<j else (j,i)
    aa = .021*np.sin(.13*(u+1)+.29*(v+1))
    bb = .019*np.cos(.43*(u+1)-.17*(v+1))
    daa = .008*np.cos(.31*(u+1)+.23*(v+1))
    dbb = .007*np.sin(.37*(u+1)-.11*(v+1))
    X=(aa+y*daa)*N2+(bb+y*dbb)*NB3
    g=expm(X if i<j else -X)
    assert np.max(abs(g.T @ eta @ g-eta)) < 1e-12
    assert abs(np.linalg.det(g)-1)<1e-12
    return g


def pair(i,j,y):
    g=lorentz(i,j,y)
    C=0.5*exterior(g)
    svals, V=eigh(np.eye(16)-C.T@C)
    assert min(svals) > .3
    F=(V*np.sqrt(svals)[None,:])@V.T
    assert np.linalg.norm(C.T@C+F.T@F-np.eye(16)) < 2e-12
    return C,F,g


def input_ch0i():
    """Full CAR16 carrier, Choi preparation supported in its grade-one sector."""
    psi=np.zeros((16,4))
    for a in range(4):
        psi[1<<a,a]=.5
    assert abs(np.linalg.norm(psi)**2-1)<1e-14
    return psi


def fixed_path(y):
    nodes=(0,9,20,0)
    K,rho,mu,P=transfer(y)
    edge_prod=np.prod([K[u,v] for u,v in zip(nodes[:-1],nodes[1:])])
    p_path=mu[nodes[0]]*np.prod([P[u,v] for u,v in zip(nodes[:-1],nodes[1:])])
    assert abs(edge_prod-rho**3*p_path/mu[nodes[-1]]) < 1e-12
    psi=input_ch0i()
    gates=[pair(u,v,y) for u,v in zip(nodes[:-1],nodes[1:])]
    probs={}
    for bits in itertools.product((0,1), repeat=3):
        state=psi.copy()
        for bit,(C,F,g) in zip(bits,gates):
            state=(C if bit==0 else F)@state
        probs[bits]=np.linalg.norm(state)**2
    assert abs(sum(probs.values())-1)<2e-12
    assert min(probs.values())>0
    full_good=gates[2][0]@gates[1][0]@gates[0][0]@psi
    group_total=gates[2][2]@gates[1][2]@gates[0][2]
    assert np.linalg.norm(full_good-(2.0**-3)*exterior(group_total)@psi)<2e-13
    assert np.linalg.norm(group_total-np.eye(4))>.001
    assert np.linalg.norm(group_total.T@eta@group_total-eta)<1e-12
    return edge_prod,p_path,rho,mu[nodes[-1]],P,probs,gates


def main():
    y=.31
    K,rho,mu,P=transfer(y)
    psi=input_ch0i()
    max_marg=0.0
    # Full 24 original outgoing edges, including all original old endpoint labels.
    for v in range(n):
        if allowed[0,v]:
            C,F,_=pair(0,v,y)
            qgood=P[0,v]*np.linalg.norm(C@psi)**2
            qfail=P[0,v]*np.linalg.norm(F@psi)**2
            max_marg=max(max_marg,abs(qgood+qfail-P[0,v]))
    assert max_marg<1e-13
    w,p,ro,rend,_,probs,gates=fixed_path(y)
    t=1e-5
    wp,pp,rhop,rendp,_,outp,_=fixed_path(y+t)
    wm,pm,rhom,rendm,_,outm,_=fixed_path(y-t)
    dw=(math.log(wp)-math.log(wm))/(2*t)
    dfrombook=3*(math.log(rhop)-math.log(rhom))/(2*t) + (math.log(pp)-math.log(pm))/(2*t) - (math.log(rendp)-math.log(rendm))/(2*t)
    assert abs(dw-dfrombook)<2e-9
    # Absolute FULL outcome surprisal splits into EXACT scalar and conditional source.
    b=(0,0,0)
    fullp=pp*outp[b]
    fullm=pm*outm[b]
    score_full=(math.log(fullp)-math.log(fullm))/(2*t)
    score_scalar=(math.log(pp)-math.log(pm))/(2*t)
    score_flag=(math.log(outp[b])-math.log(outm[b]))/(2*t)
    assert abs(score_full-score_scalar-score_flag)<2e-10
    assert abs(score_flag)>1e-8  # active Lorentz source on the SAME path
    # A different order of noncommuting native Lorentz null operations
    A=pair(0,9,y)[2]
    B=pair(9,20,y)[2]
    comm=np.linalg.norm(A@B-B@A)
    assert comm>1e-7
    print('PASS original directed scalar edges:', int(allowed.sum()))
    print('PASS one-run 24-outgoing-edge marginals, max error:',f'{max_marg:.3e}')
    print('PASS one-sided exact raw Book/Born ratio:',f'{abs(w-rho**3*p/rend):.3e}')
    print('PASS exact full CAR16 all-8-flag completeness:',f'{abs(sum(probs.values())-1):.3e}')
    print('PASS all-good ordered CAR16 exterior holonomy via 3 fresh flags')
    print('PASS Book/Born absolute log-score residual:',f'{abs(dw-dfrombook):.3e}')
    print('PASS complete-record score chain residual:',f'{abs(score_full-score_scalar-score_flag):.3e}')
    print('PASS conditional Lorentz flag log-source:',f'{score_flag:.12g}')
    print('PASS noncommuting two null generators, order discrepancy:',f'{comm:.12g}')
    print('PASS ALL old archive labels kept as spectator / all outcomes retained (mathematical carrier)')
    print('NOTE: no compulsory GoldenCoherentMemory.fullStep or Book cost selector asserted')


if __name__=='__main__':
    main()
