#!/usr/bin/env python3
"""Original native Dirac protected 2-grade B=M_nu (S-I)/h, actual rank128
fixedRIGHT spectral MINIMUM: exact fourfold cutoff derivative
{-nu*q,-nu*q,+nu*q,+nu*q} for smooth Fourier coframe field.
Original 65/131/257 full finite doubled singular spectra independently
reproduce the non-C1 source kink with NONZERO fixed-period h->0 limit.
NO physical G0 selected R-minimization or full16 boundary is asserted.
"""
import math
import numpy as np

RANK=128
K=32
NU=0.7
PERIOD=1.3
for L in (65,131,257):
    h=PERIOD/L
    w=2*math.pi*K/L
    x=np.arange(L)
    D=np.zeros((L,L))
    for a in range(L):
        D[a,a]=-1/h
        D[a,(a+1)%L]=1/h
    Q=D.T@D
    band=4*math.sin(w/2)**2/h**2
    F=np.column_stack((
        np.sqrt(2/L)*np.cos(w*x),
        np.sqrt(2/L)*np.sin(w*x)))
    assert np.max(np.abs((Q-band*np.eye(L))@F))<1e-7
    W=np.diag(np.cos(2*w*x))
    # Actual original grade0 R=||M_nu D f||^2.
    # Grade1 R=||D^T M_nu f||^2 (true positive shifted adjoint).
    H0=F.T@(2*NU*D.T@W@D)@F
    H1=F.T@(NU*(W@(D@D.T)+(D@D.T)@W))@F
    slopes=np.sort(np.concatenate((np.linalg.eigvalsh(H0),
                                     np.linalg.eigvalsh(H1))))
    slopes_exact=np.array([-NU*band,-NU*band,NU*band,NU*band])
    assert np.allclose(slopes,slopes_exact,atol=3e-7,rtol=1e-11)
    assert 2+4*31+2==RANK

    # Four true cutoff slopes split into two orthogonal rank2 minimizers
    # for +/- smooth coframe perturbation. The full LEFT density has a
    # gauge-independent trace-NORM jump 4/128=1/32 at fixed RIGHT Gram.
    plus=np.zeros((4,4))
    minus=np.zeros((4,4))
    for j,blk in enumerate((H0,H1)):
        vals,vecs=np.linalg.eigh(blk)
        plus[2*j:2*j+2,2*j:2*j+2]=np.outer(vecs[:,0],vecs[:,0])
        minus[2*j:2*j+2,2*j:2*j+2]=np.outer(vecs[:,1],vecs[:,1])
    assert np.max(np.abs(plus@minus))<1e-10
    assert np.max(np.abs(plus+minus-np.eye(4)))<1e-10
    trace_norm=float(np.linalg.svd((plus-minus)/RANK,compute_uv=False).sum())
    assert abs(trace_norm-1/32)<1e-12
    print("PASS LEFT reference128 trace norm jump",trace_norm,
          "trace-distance",trace_norm/2,
          "no continuous two-sided lowest-R selector")
    # Two grades have EXACT duplicate singular-value spectra at any
    # nonconstant nu_x; count all original 2L spectral states honestly.
    def min_rayleigh(eps):
        profile=NU+eps*np.cos(2*w*x)
        B=profile[:,None]*D
        vals=np.linalg.eigvalsh(B.T@B)
        all_e=np.sort(np.concatenate((vals,vals)))
        return float(all_e[:RANK].sum()/RANK)
    r0=min_rayleigh(0.)
    expected_jump=4*NU*band/RANK
    for eps in (1e-5,1e-6):
        rp=min_rayleigh(eps);rm=min_rayleigh(-eps)
        left=(r0-rm)/eps
        right=(rp-r0)/eps
        jump=left-right
        assert abs(jump/expected_jump-1)<.006
    print("PASS original L",L,"full",2*L,"states, rank",RANK,
          "native pp Fourier q",band,
          "exact derivative jump",expected_jump,
          "measured",jump,
          "cusp",NU*band/64)
limit=NU*(2*math.pi*K/PERIOD)**2/64
assert limit>0
print("PASS fixed physical period limiting cusp coefficient",limit)
print("PASS exact FOUR cutoff slopes +/-nu*q twice; full lowest-128 source NOT C1")
print("FIREWALL original fully selected G0/M1 H+J+R/oldRIGHT or DIRICHLET boundary OPEN")
print("GR_closed=false")


# EXACT Ky Fan maximality for the original all-NONZERO occupied
# 128-state preparation at the minimal original two/four-grade capacities.
# And symmetry-invariant rank-half cutoff twirl requires MORE than 128
# nonzero LEFT eigenvalues, contrary to any pure fixedRIGHT128 amplitude.
for grades,Lcut in ((2,65),(4,33)):
    kcut=32 if grades==2 else 16
    lower=grades*(1+2*(kcut-1))
    cutoff_dim=2*grades
    occupied_cutoff=128-lower
    assert occupied_cutoff==grades
    avg_cutoff_occupancy=occupied_cutoff/cutoff_dim
    assert avg_cutoff_occupancy==.5
    left_rank_after_twirling=lower+cutoff_dim
    assert left_rank_after_twirling==grades*Lcut
    assert left_rank_after_twirling in (130,132)
    assert lower/128+cutoff_dim*(.5/128)==1
    # At the minimal grid all nonzero protected eigenvectors are exactly
    # 128; their uniform rank128 projector is the global Ky Fan MAX.
    nonzero=grades*(Lcut-1)
    assert nonzero==128
    qsum=sum(4*math.sin(math.pi*j/Lcut)**2 for j in range(Lcut))
    assert abs(qsum-2*Lcut)<1e-12
    protected_maxR=grades*NU**2*qsum/(128*(PERIOD/Lcut)**2)
    analytic_maxR=grades*Lcut*NU**2/(64*(PERIOD/Lcut)**2)
    assert abs(protected_maxR-analytic_maxR)<1e-9
    print("PASS g",grades,"L",Lcut,
          "nonzero-only 128 global R MAX on protected carrier",
          "invariant twirled LEFT rank",left_rank_after_twirling,
          "cannot be purified by RIGHT128")
print("PASS extra archive or a paid symmetry-breaking selector mandatory for invariant mixed cutoff")


# POSITIVE branch: track one actual k32 cutoff eigenbranch analytically,
# rather than insisting on the instantaneous global minimum on BOTH sides.
# Each finite stationary projector commutes with TRUE B^T B and BB^T.
L=131
h=PERIOD/L
w=2*math.pi*K/L
D=np.zeros((L,L))
for i in range(L):
    D[i,i]=-1/h
    D[i,(i+1)%L]=1/h
x=np.arange(L)
weight=np.cos(2*w*x)
band=4*math.sin(w/2)**2/h**2
for eps in (-1e-6,-1e-7,1e-7,1e-6):
    B=(NU+eps*weight)[:,None]*D
    e0,V=np.linalg.eigh(B.T@B)
    e1,U=np.linalg.eigh(B@B.T)
    # k<32: 63 states per grade. Select the SAME k32 first-slope-
    # negative eigenbranch: lower of 2 cutoff eigenvalues if eps>0,
    # higher if eps<0. This is a smooth STATIONARY rather than always
    # MINIMIZING choice.
    cutoff=63 if eps>0 else 64
    ids=list(range(63))+[cutoff]
    P0=V[:,ids]@V[:,ids].T
    P1=U[:,ids]@U[:,ids].T
    assert abs(float(np.trace(P0)+np.trace(P1))-RANK)<1e-7
    assert np.linalg.norm((B.T@B)@P0-P0@(B.T@B))<1e-7
    assert np.linalg.norm((B@B.T)@P1-P1@(B@B.T))<1e-7
    Rstationary=float((e0[ids].sum()+e1[ids].sum())/RANK)
    Rminimum=float((e0[:64].sum()+e1[:64].sum())/RANK)
    if eps<0:
        expected=(NU*band/32)*abs(eps)
        assert abs((Rstationary-Rminimum)/expected-1)<.002
    else:
        assert abs(Rstationary-Rminimum)<2e-8
print("PASS genuine full fixedRIGHT stationarity exists smoothly on both field signs")
print("PASS smooth excited branch pays native Rayleigh gap nu*q/32*abs(eps)")
