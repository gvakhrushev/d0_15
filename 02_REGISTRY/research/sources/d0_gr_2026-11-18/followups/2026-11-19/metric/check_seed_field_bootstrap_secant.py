"""Actual common native word; exact sector bootstrap field secant.

Two physical invariant programme sectors, both Hodge grades and full input
cuts. The seed-input programme factory and full Einstein field bank are not
included; no Book vertex Info is selected.
"""
from collections import Counter
import math
import numpy as np
from scipy.linalg import eigvalsh
from mpmath import iv

from check_local_gibbs_records import mm, scene
from check_seed_nc1_record_clock import make_clock
from check_source_price import load_control, need


def main():
    ne, digest = load_control()
    p, a = float(ne.P), float(ne.A)
    gate = ne.Gate
    source = dict(profile=ne.G_CX_SOURCE_I, source_port=1, source_spin=(2,3))
    spec = ne.Execution(7, (), (), (gate('G',(6,)),), **source)
    inv = ne.inverse_word(spec, max_qubits=7, max_expanded_stages=100)
    need(Counter(g.op for g in inv) == Counter({'CX':6,'SourceI':4,'G':1}),
         'all physical inverse-G routes')
    stages=[]
    current=4
    def birth():
        nonlocal current
        b=np.kron(np.eye(1<<current), np.array([[a],[p]]))
        stages.append((b,b,'birth'))
        current+=1
    def append(g):
        spec=ne.Execution(current,(),(),(g,),**source)
        op=np.array(ne.gate_matrix(spec,g,max_qubits=7,max_expanded_stages=100),dtype=float)
        stages.append((op,np.eye(1<<current),g.op))
    birth() # H
    append(gate('CX',(0,4))) # saved programme k controls H
    birth() # NC1 tail
    for g in (gate('CX',(4,5)),gate('G',(5,)),gate('CX',(4,5))): append(g)
    birth() # orthogonal record environment, genuinely prepared as zero
    for g in inv: append(g)
    append(gate('CX',(4,6)))
    need(len(stages)==19, 'one genuine finite 19-stage word')
    need(Counter(kind for _,_,kind in stages)==Counter({'birth':3,'CX':10,'G':2,'SourceI':4}),
         'full birth/gate inventory')
    V=E=np.eye(16)
    for real,passive,_ in stages:
        V,E=mm(real,V),mm(passive,E)
    need(np.max(np.abs(mm(V.T,V)-np.eye(16)))<5e-13,'all 16 old columns')
    C=mm(E.T,V)
    c0=p*p+a*p**3
    c1=a*p*p+p**3
    need(np.max(np.abs(C-np.diag([c0]*8+[c1]*8)))<5e-13,
         'exact input-sector raw-return formula')
    bits=np.arange(128)
    k=(bits>>6)&1
    h=(bits>>2)&1
    tail=(bits>>1)&1
    env=bits&1
    need(np.linalg.norm(V[env!=h])<5e-13,'actual complete recording environment')
    need(np.linalg.norm(V[(h==1)&(tail==1)])<5e-13,'forbidden NC1 sector dark')
    VH=V[h==1,:]
    effect=mm(VH.T,VH)
    need(np.max(np.abs(effect-np.diag([p*p]*8+[p]*8)))<5e-13,
         'actual all-input programme-sector field effects')
    need(np.linalg.norm(V[(k==1),:8])<5e-13 and np.linalg.norm(V[(k==0),8:])<5e-13,
         'programme preserved on all final columns')

    sectors=[]
    for kval in (0,1):
        seq=[]
        for real,passive,kind in stages:
            nr,nc=real.shape[0]//2,real.shape[1]//2
            # Every gate and every birth commutes with the actual k projector.
            need(np.max(np.abs(real[:nr,nc:]))<5e-13 and np.max(np.abs(real[nr:,:nc]))<5e-13,
                 'real stage preserves both complete programme sectors')
            seq.append((real[kval*nr:(kval+1)*nr,kval*nc:(kval+1)*nc],
                        passive[kval*nr:(kval+1)*nr,kval*nc:(kval+1)*nc],kind))
        T=make_clock(seq)
        need(len(T)==936, 'complete growing clock in each programme sector')
        min_loop=min(len(seq)-(j+1) for j,(_,_,kind) in enumerate(seq[:-1]) if kind=='birth')
        need(min_loop==12, 'last actual birth leaves a twelve-stage minimum loop')
        sectors.append(T)
    beta=2*p*p; z=2**-20
    B,S=scene()
    def heat(clock):
        vals=eigvalsh(clock+clock.T,check_finite=False)
        Z=359*len(clock)
        for lam in vals:
            eig=eigvalsh(np.eye(len(B))-B-lam*S,check_finite=False)
            Z+=2*float(np.exp(-beta*eig).sum())
        return Z
    Z0,Z1=map(heat,sectors)
    j0=-8*math.log1p(-z*(1-c0*c0))
    j1=-8*math.log1p(-z*(1-c1*c1))
    b0=math.log(Z0)/beta+j0
    b1=math.log(Z1)/beta+j1
    bfull=math.log(Z0+Z1)/beta+j0+j1

    iv.dps=80
    one=iv.mpf(1);pp=(iv.sqrt(5)-one)/2;aa=iv.sqrt(pp)
    zz=one/(2**20); bb=2*pp**2
    cc0=pp**2+aa*pp**3;cc1=aa*pp**2+pp**3
    dj=8*iv.log((one-zz*(one-cc0**2))/(one-zz*(one-cc1**2)))
    # The shortest possible loop after the final actual birth is 12.
    # Two complete sector heat traces lie within 66D e_L of D z_infinity.
    L=12; xx=bb/11
    e=2*xx**L/(math.factorial(L)*(one-xx/(L+1)))
    heat_error=132*e/(359*bb)
    delta=pp-pp**2
    total_lo,total_hi=dj-heat_error,dj+heat_error
    need(total_lo>iv.mpf('0.0000002627') and total_hi<iv.mpf('0.0000002629'),
         'strict positive two-grade bootstrap secant')
    need(ne.GOLDEN_FIELD.from_sympy(ne.P-ne.P**2-ne.P**3)==ne.GOLDEN_FIELD.zero,
         'exact golden genuine record probability secant')
    ps=ne.P
    Bpoly=lambda x: 1-2*x+2*x*x
    Q=lambda s,t: -((Bpoly(s)-s*s)*Bpoly(t)+t*t*Bpoly(s))
    matter_contrast=Q(ps,ps**2)-Q(ps**2,ps**2)
    need(ne.GOLDEN_FIELD.from_sympy(matter_contrast-(18*ps-11))==ne.GOLDEN_FIELD.zero,
         'exact conditional two-copy catalogue contrast')
    need(ne.GOLDEN_FIELD.from_sympy((18*ps-11)-ps**3*(3-4*ps))==ne.GOLDEN_FIELD.zero,
         'exact material contrast factorization')
    print('native source sha256:',digest)
    print('literal word: 3 births, 10 CX, 2 G, 4 SourceI; 19 stages')
    print('both fixed k sectors: q0=p^2, q1=p; actual k retained')
    print('each sector: full input cut 8; growing-clock D=936; modes=',425*936)
    print('raw return c0,c1:',c0,c1)
    print('feedback secant interval:',dj)
    print('absolute full heat secant bound:',heat_error)
    print('certified full bootstrap secant enclosure:',total_lo,total_hi)
    print('secant per physical q interval:',total_lo/delta,total_hi/delta)
    print('numerical heat Z0,Z1:',Z0,Z1,'numerical full secant:',b1-b0)
    print('common full-rank 16-cut master:',bfull,'one graph for both input programmes')
    print('conditional separate two-copy CAR catalogue contrast: 18p-11 = p^3(3-4p)')
    print('programme-preparation and full Einstein geometry/source remain open')


if __name__=='__main__':
    main()
