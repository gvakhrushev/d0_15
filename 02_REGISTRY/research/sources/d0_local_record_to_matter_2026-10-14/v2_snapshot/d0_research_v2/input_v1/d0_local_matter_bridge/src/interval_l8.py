"""Outward-rounded Krawczyk/Banach certificate of the L=8 kinetic/heat balance.
The exact features live in Q(sqrt(2)); no floating point signs prove existence.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
import json
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1]

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def mul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def features():
    re=[(0,0),(-8,4),(-8,0),(-8,-4),(-16,0),(-8,-4),(-8,0),(-8,4)]
    im=[(0,0),(0,4),(8,0),(0,4),(0,0),(0,-4),(-8,0),(0,-4)]
    out=Counter()
    for ks in product(range(8),repeat=4):
        sr=si=A=(0,0)
        for k in ks:
            sr=add(sr,re[k]);si=add(si,im[k])
            A=add(A,add(mul(re[k],re[k]),mul(im[k],im[k])))
        B=sub(add(mul(sr,sr),mul(si,si)),A)
        out[(A,B)]+=1
    return sorted(out.items())


def main():
    mp.mp.dps=70;mp.iv.dps=55
    rows=features();iv=mp.iv
    def val(v,ctx):return ctx.mpf(v[0])+ctx.mpf(v[1])*ctx.sqrt(2)
    beta=mp.log(2);l1=128-64*mp.sqrt(2)
    dat=[(val(A,mp),val(B,mp),count) for (A,B),count in rows]
    def moments(d,o):
        w=[n*mp.exp(-beta*(A*d+B*o)) for A,B,n in dat]
        Z=sum(w);EA=sum(wi*A for wi,(A,B,n) in zip(w,dat))/Z
        EB=sum(wi*B for wi,(A,B,n) in zip(w,dat))/Z
        AA=sum(wi*A*A for wi,(A,B,n) in zip(w,dat))/Z
        AB=sum(wi*A*B for wi,(A,B,n) in zip(w,dat))/Z
        BB=sum(wi*B*B for wi,(A,B,n) in zip(w,dat))/Z
        return mp.matrix([EA-l1,EB]),-beta*mp.matrix([[AA-EA*EA,AB-EA*EB],[AB-EA*EB,BB-EB*EB]])
    d,o=mp.findroot(lambda d,o:tuple(moments(d,o)[0]),(mp.mpf('.07035'),mp.mpf('.00442')),tol=mp.mpf('1e-60'))
    # Decimal rationals fixed before interval evaluation, not arbitrary point floats.
    center=[mp.nstr(d,45),mp.nstr(o,45)]
    inv=moments(mp.mpf(center[0]),mp.mpf(center[1]))[1]**-1
    P=[[iv.mpf(mp.nstr(inv[i,j],45)) for j in range(2)] for i in range(2)]
    radius=iv.mpf('1e-12')
    X=[iv.mpf(c)+iv.mpf(['-1e-12','1e-12']) for c in center]
    dataiv=[(val(A,iv),val(B,iv),n) for (A,B),n in rows]
    b=iv.ln(2);target=iv.mpf(128)-64*iv.sqrt(2)
    def imom(x):
        Z=iv.mpf(0);sx=[iv.mpf(0),iv.mpf(0)];sxx=[[iv.mpf(0) for _ in range(2)]for _ in range(2)]
        for A,B,n in dataiv:
            t=[A,B];w=n*iv.exp(-b*(A*x[0]+B*x[1]));Z+=w
            for i in range(2):
                sx[i]+=w*t[i]
                for j in range(2):sxx[i][j]+=w*t[i]*t[j]
        E=[s/Z for s in sx]
        F=[E[0]-target,E[1]]
        J=[[-b*(sxx[i][j]/Z-E[i]*E[j]) for j in range(2)] for i in range(2)]
        return F,J
    F0,_=imom([iv.mpf(c) for c in center]);_,JI=imom(X)
    C=[[iv.mpf(int(i==j))-sum(P[i][k]*JI[k][j] for k in range(2))for j in range(2)]for i in range(2)]
    # Direct bounds use exact decimal rational thresholds. Both are strict interval inequalities.
    rowbounds=[sum(abs(C[i][j]) for j in range(2)) for i in range(2)]
    residual=[abs(sum(P[i][j]*F0[j] for j in range(2))) for i in range(2)]
    for q,e in zip(rowbounds,residual):
        if not(q < iv.mpf('1e-6')):raise AssertionError(('CONTRACTION_BOUND',q))
        if not(e+q*radius < radius):raise AssertionError(('SELF_MAPPING',e,q))
    if not(X[0]-X[1] > iv.mpf('.065')):raise AssertionError('SPD_TRANSVERSE')
    if not(X[0]+3*X[1] > iv.mpf('.083')):raise AssertionError('SPD_LONGITUDINAL')
    # The first positive shell is still exactly the selected 8-mode shell.
    gaps=[];shell_count=0;zero_count=0
    shellpair=(128,-64)
    for (A,B),n in rows:
        if A==(0,0) and B==(0,0):zero_count+=n;continue
        if A==shellpair and B==(0,0):shell_count+=n;continue
        gap=(val(A,iv)-target)*X[0]+val(B,iv)*X[1]
        if not(gap>iv.mpf('1')):raise AssertionError(('SHELL_NOT_LOWEST',A,B,gap))
        gaps.append(gap)
    if shell_count!=8 or zero_count!=1:raise AssertionError('SHELL_MULTIPLICITY')
    record={
        'status':'PASS','type':'ANALYTIC_EXISTENCE_FROM_OUTWARD_INTERVAL_CONTRACTION',
        'L':8,'beta':'log(2)','number_of_modes':4096,'Fock_dimension':16,
        'grouped_exact_feature_pairs':len(rows),'center_decimal_rationals':center,
        'coordinate_radius':'1e-12','contraction_infinity_norm_upper':'1e-6',
        'self_mapping_verified':True,'SPD_transverse_lower':'.065','SPD_longitudinal_lower':'.083',
        'next_shell_gap_lower':'1','selected_momentum_modes':shell_count,
        'selected_Fock_modes':shell_count*16,'zero_Fock_modes':16,
        'row_contraction_interval':[str(v) for v in rowbounds],
        'preconditioned_center_residual_interval':[str(v) for v in residual],
        'preconditioner_decimal_rationals':[[mp.nstr(inv[i,j],45)for j in range(2)]for i in range(2)],
        'matter_admission_from_D0_pi0':False,'curved_GR_derived':False,
        'proof_boundary':'Analytic translation/Fock-trace identities extend this homogeneous root to all local metric and specified linear-link first variations; other D0 action terms are not included.'}
    (ROOT/'results/interval_L8.json').write_text(json.dumps(record,indent=2)+'\n')
    print('PASS_INTERVAL_L8',len(rows),'exact grouped pairs',center)
    print('contraction bounds',*[str(v) for v in rowbounds])
    print('center residual bounds',*[str(v) for v in residual])

if __name__=='__main__':main()
