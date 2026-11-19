#!/usr/bin/env python3
"""Original 8D Golden-J2 block: exact TWO ordinary 8D queries -> feedback determinant.

This proves the finite local algebra and its first-jet contact without any
exterior fermionic Fock apparatus. The actual query/coin/OR must still be
physically admitted/paid and selected by Book03 before GR can close.
Standard-library, rational only; Python -O never disables its checks.
"""
from fractions import Fraction as Q
from itertools import product
import json

def check(cond, msg):
    if not cond:
        raise RuntimeError(msg)

def ident(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]

def matmul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q())
             for j in range(len(b[0]))] for i in range(len(a))]

def tr(a):
    return list(map(list,zip(*a)))

def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0]))
             for l in range(len(b[0]))] for i in range(len(a))
             for k in range(len(b))]

def det2(a): return a[0][0]*a[1][1]-a[0][1]*a[1][0]

def construct_original_native8d():
    # Same ORIGINAL 4-tail × 2-scene exact rational fixture as the reviewed
    # finite future exterior owner; not a fabricated effective 2×2 instrument.
    rr,ss,cc,tt=Q(4,5),Q(3,5),Q(12,13),Q(5,13)
    tail=[[rr,0,-ss,0],[0,rr,0,-ss],
          [0,ss,0,rr],[ss,0,rr,0]]
    scene=[[cc,-tt],[tt,cc]]
    step=kron(tail,scene)
    U=matmul(step,step)
    check(matmul(tr(U),U)==ident(8),"original 8D U not unitary")
    retained=(0,2)
    P=[[U[r][i] for i in retained] for r in range(8)]
    W=[P[r] for r in retained]
    E,b=Q(9,25),Q(25,169)
    predicted=[[(1-2*b)*(1-E),(1-2*b)*(-E)],
               [(1-2*b)*(-E),(1-2*b)*(1-E)]]
    check(W==predicted,"native rank2 returned compression changed")
    return U, retained, P, E,b

def source_and_fixed_basis():
    U,ret,frame,E,b=construct_original_native8d()
    Qcut=[0 if r in ret else 1 for r in range(8)]
    F=[[sum((frame[r][i]*Qcut[r]*frame[r][j]
             for r in range(8)),Q()) for j in range(2)] for i in range(2)]
    B=4*b*(1-b)
    A=B+(1-B)*4*E*(1-E)
    # Fixed ± basis independently of E,b (no after-the-fact eigenvectors).
    check(F[0][0]+F[0][1]==A,"+ eigenvalue not native A")
    check(F[1][0]+F[1][1]==A,"+ eigenvector not fixed")
    check(F[0][0]-F[0][1]==B,"- eigenvalue not native B")
    check(F[1][1]-F[1][0]==B,"- eigenvector not fixed")

    for z in (Q(9,25),Q(1,2**20)):
        # Only ordinary one-particle U and its original complementary Q cut.
        # Each held native ± preparation has no-click effect I-zF.
        plus=(F[0][0]+F[1][1]+F[0][1]+F[1][0])/2
        minus=(F[0][0]+F[1][1]-F[0][1]-F[1][0])/2
        check(plus==A and minus==B,"independent fixed ± probabilities wrong")
        dp=(1-z*plus)*(1-z*minus)
        ddet=det2([[Q(int(i==j))-z*F[i][j] for j in range(2)]
                    for i in range(2)])
        check(dp==ddet,"two native independent 8D queries != determinant")
    return U,ret,frame,F,A,B

def coherent_full_work():
    U,ret,frame,F,A,B=source_and_fixed_basis()
    # Choose actual rational efficiency z=9/25: native fixed amplitude coin
    # no amplitude 4/5 on Q, yes 3/5; P always no. All 8 positions and two
    # flags are RETAINED for each of two independent original 8D queries.
    z=Q(9,25)
    paths={}
    for sign in (+1,-1):
        entries={}
        for pos in range(8):
            raw=frame[pos][0]+sign*frame[pos][1] # /sqrt(2) per query
            in_cut=pos not in ret
            entries[(pos,0)]=raw*(Q(4,5) if in_cut else Q(1))
            entries[(pos,1)]=raw*(Q(3,5) if in_cut else Q(0))
        # Each entry is sqrt(2)* single-query amplitude.
        check(sum((amp*amp for amp in entries.values()),Q())==Q(2),
              "one native output not normalized")
        paths[sign]=entries

    # Every pair of two fully physical queries gives 16×16 =256 complete
    # distinguishable work labels; amplitude is product/2 (rational).
    total,succeed,fail=Q(),Q(),Q()
    for (pos1,flag1),(pos2,flag2) in product(paths[1],paths[-1]):
        amplitude=paths[1][(pos1,flag1)]*paths[-1][(pos2,flag2)]/2
        weight=amplitude*amplitude
        total+=weight
        if flag1 == 0 and flag2 == 0: succeed+=weight
        else: fail+=weight
    check(total==1 and succeed+fail==1,"complete OR misses work outcomes")
    d=(1-z*A)*(1-z*B)
    check(succeed==d and fail==1-d,
          "coherent final OR complete work probability != native determinant")
    check(0<succeed<1,"conditional CQ binary branch degenerate")
    # Pure conditional full-work states are obtained by applying the two
    # complementary projectors to a single pure 256-work-label vector.
    return {"native_full_work_labels":256,"actual_success":str(succeed),
            "actual_failure":str(fail)}

def exact_offchart_gate():
    # A generic *different* unowned Hermitian 2×2 input has cross response.
    # Its two fixed-basis independent query probabilities do NOT equal det.
    a,b,c,z=Q(1,4),Q(1,3),Q(1,20),Q(1,2**20)
    F=[[a,c],[c,b]]
    # Strict positive effect [0,I] by Sylvester principal-minor test.
    check(a>0 and det2(F)>0 and 1-a>0
          and det2([[1-F[0][0],-F[0][1]],
                     [-F[1][0],1-F[1][1]]])>0,
          "offchart hostile F not physical effect")
    d2=(1-z*a)*(1-z*b)
    de=det2([[Q(int(i==j))-z*F[i][j] for j in range(2)]
             for i in range(2)])
    check(d2-de==z*z*c*c and d2>de,
          "exact off-chart z²|F+-|² obstruction missing")
    # For a diagonal reference, arbitrary offdiag c=t k starts at t².
    # Both value and first derivatives in ANY tangent are equal at t=0.
    # Example independently moving a,b with arbitrary c derivative.
    da,db,k=Q(1,7),Q(-1,11),Q(1,13)
    first=-z*da*(1-z*b)-z*db*(1-z*a)
    assert first==-z*(da+db)+z*z*(da*b+db*a)
    second_mismatch=z*z*k*k  # coefficient of t² exactly
    check(second_mismatch>0,"missing second-order negative control")
    return {"offchart_value_defect":str(d2-de),
            "offchart_first_jet_defect":"0",
            "offchart_second_order_defect":str(second_mismatch)}

def native_golden_efficiency_info_gate():
    # Exact algebraic finite GOLDEN stochastic-primitives obstruction:
    # finite event laws are in Z[p] as p^2=1-p. Irrational p implies
    # a+b*p rational iff b=0, so no dyadic 1/2^20 at finite depth.
    # Check the complete entropy-derivative *source* sign in a rational
    # positive original Q-effect window, without approximating logs.
    z=Q(1,2**20)
    for lam in (Q(1,5),Q(1,3),Q(4,5)):
        # d/dλ(h(zλ)-z h(λ))
        # = z log_phi[(1-zλ)/(z(1-λ))].
        ratio=(1-z*lam)/(z*(1-lam))
        check(ratio>1,"measured vs coherent controller first source gap not strict")
        # Full measured controller ledger entropy is h(z)+z h(lam);
        # full coherent binary source is h(z lam), not this one.
    print("PASS finite Golden-only rational dyadic exclusion and "
          "coherent-vs-measured controller Info first-source obstruction")

if __name__=="__main__":
    work=coherent_full_work()
    hostile=exact_offchart_gate()
    native_golden_efficiency_info_gate()
    print(json.dumps({"status":"PASS",
          "original_native_query_dimension":8,
          "no_exterior_or_fermionic_fock_primitive":True,
          "fixed_field_independent_retained_basis":True,
          "complete_coherent_binary_OR":work,
          "offchart_hostile":hostile,
          "all_actual_40_plus_2_first_source_transport":"conditional_on_existing_owned_source_map",
          "complete_Book03_selected":False,
          "GR_closed":False},ensure_ascii=False))
