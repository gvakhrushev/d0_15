#!/usr/bin/env python3
"""Full temporal-slab negative control for the old 42->12 pureboost zero test.

All 12 original spatial-link target sources have a full-row-rank Jacobian
against independent REAL 18 spatial Lorentz components per interior time
node. We numerically zero the 12 targets with a proper exponential link
update and fixed time-end link data; OTHER original Euler source entries
then become nonzero, because the new backgrounds are no longer pure boosts.
This is a deliberate strict regression against false full42 root claims.

Scope: same ORIGINAL full4 G2/STAR six-face action, original rank-two Cauchy
starting geometry and fixed original CAR matter. Not physical Book selection.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.optimize import root
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import lsqr
from check_star_rank2_seam import I,LORENTZ,star_density,matter_query,KAPPA
from check_diagonal_coframe_cauchy_recurrence import clock,radius,golden_curve,comm

PINS={
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py":"a57f0e3e845290923c2ac88d39ba5c08af4f6fd6",
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_diagonal_coframe_cauchy_recurrence.py":"487705f27a32ca1ee65348c5ddb2e4f4d32f5b55"}
ROOT=Path(__file__).resolve().parents[4]
TARGETS=[(1,0),(1,1),(1,2),(1,3),(1,4),
         (2,1),(2,3),(2,5),
         (3,1),(3,2),(3,4),(3,5)]

def checkpins():
    for p,sha in PINS.items():
        v=(ROOT/p).read_bytes()
        got=hashlib.sha1(b"blob "+str(len(v)).encode()+b"\0"+v).hexdigest()
        assert got==sha,(p,got,sha)

def slab(n):
    t=np.linspace(clock(1.),clock(1.2),n+1)
    h=float(t[1]-t[0])
    amp=(2*KAPPA)**-.5
    k1=golden_curve(1.)[1]
    nodes=[]
    for t0,t1 in zip(t[:-1],t[1:]):
        r=radius(t0)
        r1=radius(t1)
        A,_,k2=golden_curve(r)
        k2next=golden_curve(r1)[2]
        S2=np.sinh(h*(k2next-k2))
        C12=comm(h*k1,h*k2)
        C22=comm(h*k2,h*k2)
        def F(x):
            X,R=x
            return [(2*R*C12+C22/X)/h**2-X,
                    (2*R*S2+X*C22)/h**2+X**3]
        sol=root(F,[A,r],tol=1e-11)
        assert sol.success and max(abs(x) for x in F(sol.x))<1e-9
        X,R=sol.x
        s1=-(S2/X+X*C12)/R
        k1_next=k1+np.arcsinh(s1)/h
        U=np.asarray([I]+[
              expm(h*k*LORENTZ[j]) for j,k in enumerate((k1,k2,k2))
            ],dtype=complex)
        nodes.append(dict(e=np.diag([X,1/X,R,R]).astype(complex),u=U,
                          v=np.array([[amp*X**2,0,0,0],[0,amp,0,0]],
                                     dtype=complex)))
        k1=k1_next
    lastU=np.asarray([I]+[
          expm(h*k*LORENTZ[j]) for j,k in
          enumerate((k1,golden_curve(1.2)[2],golden_curve(1.2)[2]))
        ],dtype=complex)
    nodes.append(dict(e=np.diag([1,1,1.2,1.2]).astype(complex),u=lastU,
                      v=np.zeros((2,4),dtype=complex)))
    return nodes,h

def target12(nodes,j,h):
    prev,cur,nex=nodes[j-1:j+2]
    eps=1e-20
    out=[]
    for axis,k in TARGETS:
        old=cur['u'][axis].copy()
        cur['u'][axis]=expm(1j*eps*LORENTZ[k])@old
        out.append((star_density(prev,cur,h)+
                    star_density(cur,nex,h)).imag/eps)
        cur['u'][axis]=old
    return np.asarray(out,float)

def first_12_slab(nodes,h):
    return np.concatenate([
        target12(nodes,j,h) for j in range(1,len(nodes)-1)])

def jacobian(nodes,h):
    n=len(nodes)-1
    M=lil_matrix((12*(n-1),18*(n-1)))
    for j in range(1,n):
        base=j-1
        # ALL THREE original time-coupled based spatial links affect the
        # local Euler: predecessor, current and future.
        for site in (j-1,j,j+1):
            if not 1<=site<n:continue
            for k in range(18):
                axis=1+k//6
                g=k%6
                eps=2e-5
                out=np.zeros(12)
                for sign in (-1,1):
                    copy=[dict(e=nodes[s]['e'],v=nodes[s]['v'],
                               u=nodes[s]['u'].copy())
                          for s in (j-1,j,j+1)]
                    loc=site-(j-1)
                    copy[loc]['u'][axis]=(
                        expm(sign*eps*h*LORENTZ[g])@
                        copy[loc]['u'][axis])
                    old=target12(copy,1,h)
                    out+=sign*old/(2*eps)
                M[12*base:12*(base+1),18*(site-1)+k]=out
    return M.tocsr()

def change_links(nodes,h,domega):
    n=len(nodes)-1
    for j in range(1,n):
        for axis in (1,2,3):
            z=domega[18*(j-1)+6*(axis-1):
                     18*(j-1)+6*axis]
            A=sum(z[k]*LORENTZ[k] for k in range(6))
            nodes[j]['u'][axis]=expm(h*A)@nodes[j]['u'][axis]

def other_sources(nodes,h):
    n=len(nodes)-1
    F=max(float(abs(star_density(nodes[j],nodes[j+1],h)))
          for j in range(n))
    j=n//2
    prev,cur,nex=nodes[j-1:j+2]
    eps=1e-20
    forbidden=0.
    diagonal=0.
    allowed={(a,a) for a in range(4)}|{(a,0) for a in (1,2,3)}
    for a in range(4):
        for b in range(4):
            old=cur['e'][a,b]
            cur['e'][a,b]=old+1j*eps
            v=(star_density(cur,nex,h)+KAPPA*matter_query(cur)).imag/eps
            cur['e'][a,b]=old
            if (a,b) not in allowed:
                forbidden=max(forbidden,abs(v))
            if a==b:diagonal=max(diagonal,abs(v))
    temporal=0.
    for k,Z in enumerate(LORENTZ):
        old=cur['u'][0].copy()
        cur['u'][0]=expm(1j*eps*Z)@old
        v=(star_density(prev,cur,h)+star_density(cur,nex,h)).imag/eps
        cur['u'][0]=old
        temporal=max(temporal,abs(v))
    return dict(max_original_star_value=F,
                previously_forbidden_coframe=forbidden,
                formerly_zero_temporal_link=temporal,
                previously_solved_diagonal_coframe=diagonal)

def one_run(n):
    nodes,h=slab(n)
    before=other_sources(nodes,h)
    J=jacobian(nodes,h)
    r=first_12_slab(nodes,h)
    sv=np.linalg.svd(J.toarray(),compute_uv=False)
    assert np.min(sv)>10 and len(sv)==12*(n-1)
    firststep=lsqr(J,-r,atol=1e-12,btol=1e-12,iter_lim=350)[0]
    bound_change=float(max(abs(x) for x in firststep))
    time_end_a=nodes[0]['u'].copy()
    time_end_b=nodes[-1]['u'].copy()
    iterations=[]
    for t in range(4):
        delta=lsqr(J,-r,atol=1e-13,btol=1e-13,
                   iter_lim=350)[0]
        change_links(nodes,h,delta)
        r=first_12_slab(nodes,h)
        iterations.append(float(max(abs(x) for x in r)))
        if iterations[-1]<1e-9:break
    assert np.allclose(time_end_a,nodes[0]['u'],atol=0,rtol=0)
    assert np.allclose(time_end_b,nodes[-1]['u'],atol=0,rtol=0)
    after=other_sources(nodes,h)
    assert iterations[-1]<1e-9
    assert after['max_original_star_value']>.5
    assert after['formerly_zero_temporal_link']>.3
    assert after['previously_forbidden_coframe']>.01
    return dict(n=n,h=h,target12_shape=list(J.shape),
                full_target12_row_rank=12*(n-1),
                singular_min=float(np.min(sv)),
                singular_condition=float(np.max(sv)/np.min(sv)),
                max_correction_spin=bound_change,
                target12_max_before=float(max(abs(x) for x in first_12_slab(slab(n)[0],h))),
                target12_max_after=iterations[-1],
                correction_iterations=iterations,
                before=before,after=after,
                negative_control="ZERO target12 outside pure-boost stratum != ZERO full42 Euler")

if __name__=="__main__":
    checkpins()
    runs=[one_run(n) for n in (12,16)]
    print(json.dumps(dict(
       status="PASS_SCOPED_12_TARGET_FALSE_FULL_ROOT_NEGATIVE_CONTROL",
       runs=runs,
       scope=dict(no_physical_Book_selected=True,
                  no_full42_root=True,
                  all_original_fixed_temporal_link_ends_preserved=True,
                  corrected_fields_outside_pure_boost_support=True,
                  false_12_zero_sufficiency_rejected=True,
                  GR_closed=False)),indent=2))
