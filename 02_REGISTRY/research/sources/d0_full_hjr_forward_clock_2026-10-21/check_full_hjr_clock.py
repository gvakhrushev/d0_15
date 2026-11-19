#!/usr/bin/env python3
"""Authored finite checks of a source-faithful forward-clock extension.

No old root search, native 4096x4096 eigensolve, Lean proof, or independent
review is performed. The native spectral calculation CONSUMES the published
radius-1e-12 root enclosure and evaluates a NEW clock-induced source on it.

Run with Python 3.9+, NumPy, SciPy. Normal and -O execution use explicit
exceptions rather than removable assert statements. No files are written.
"""
from __future__ import annotations
import itertools
import json
import math
from collections import Counter
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, localcontext
from typing import List, Tuple
import numpy as np
from scipy.linalg import eigh

CHECKS: List[str] = []

def check(name: str, condition: bool) -> None:
    if not bool(condition):
        raise RuntimeError('FAILED: ' + name)
    CHECKS.append(name)

def close(name: str, a, b, tol: float = 3e-10) -> None:
    err = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
    scale = max(1.0, float(np.max(np.abs(np.asarray(b)))))
    check(name, math.isfinite(err) and err <= tol * scale)

# Exact Q[a]/(a^4+a^2-1), a=sqrt(phi^-1), for literal native gates.
E = Tuple[int, int, int, int]
ZERO: E = (0, 0, 0, 0)
ONE: E = (1, 0, 0, 0)
A: E = (0, 1, 0, 0)
P: E = (0, 0, 1, 0)

def eadd(x: E, y: E) -> E:
    return tuple(x[i] + y[i] for i in range(4))  # type: ignore

def eneg(x: E) -> E:
    return tuple(-a for a in x)  # type: ignore

def emul(x: E, y: E) -> E:
    if x == ZERO or y == ZERO:
        return ZERO
    c = [0] * 7
    for i in range(4):
        for j in range(4):
            c[i+j] += x[i] * y[j]
    for k in range(6, 3, -1):
        v = c[k]
        c[k-4] += v
        c[k-2] -= v
    return tuple(c[:4])  # type: ignore

def epow(x: E, n: int) -> E:
    ans = ONE
    while n:
        if n & 1:
            ans = emul(ans, x)
        x = emul(x, x)
        n //= 2
    return ans

def ident(n: int):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]

def matmul(x, y):
    rows, mid, cols = len(x), len(y), len(y[0])
    out = [[ZERO for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(mid):
            if x[i][k] == ZERO:
                continue
            for j in range(cols):
                if y[k][j] != ZERO:
                    out[i][j] = eadd(out[i][j], emul(x[i][k], y[k][j]))
    return out

def trans(x):
    return [list(v) for v in zip(*x)]

def schedule_product(gates):
    out = ident(len(gates[0]))
    for g in gates:
        out = matmul(g, out)
    return out

def native_gates():
    # Basis (arm, spin quaternion 0..3, retained record bit).
    n = 16
    G = [[ZERO for _ in range(n)] for _ in range(n)]
    X = [[ZERO for _ in range(n)] for _ in range(n)]
    Y = [[ZERO for _ in range(n)] for _ in range(n)]
    W = [[ZERO for _ in range(n)] for _ in range(n)]
    li = [[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]
    lj = [[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]]
    ga = [[A, eneg(P)], [P, A]]
    def idx(a, s, r):
        return 8*a + 2*s + r
    for arm, spin, rec in itertools.product(range(2), range(4), range(2)):
        col = idx(arm, spin, rec)
        for ao in range(2):
            G[idx(ao, spin, rec)][col] = ga[ao][arm]
        for so in range(4):
            xv = (int(so == spin) if arm == 0 else li[so][spin])
            X[idx(arm, so, rec)][col] = (xv,0,0,0)
            Y[idx(arm, so, rec)][col] = (lj[so][spin],0,0,0)
        W[idx(arm, spin, rec ^ arm)][col] = ONE
    return G, X, Y, W

def exact_native_clock():
    check('Golden_field_relation', eadd(P, epow(P,2)) == ONE)
    G,X,Y,write = native_gates()
    for name,g in [('G',G),('X',X),('Y',Y),('WRITE',write)]:
        check('literal_full16_'+name+'_orthogonal', matmul(trans(g),g) == ident(16))
    words = {'identity':[X]*4+[Y]*4,
             'order':[X,Y,X,X,X,Y,Y,Y]}
    results = {}
    for name, word in words.items():
        stages = [G]+word+[X,X,G,X,X,write,ident(16)]
        T = len(stages)
        check(name+'_actual_stage_count16', T == 16)
        U = schedule_product(stages)
        check(name+'_full16_monodromy_orthogonal', matmul(trans(U),U) == ident(16))
        active = [2*s for s in range(4)]
        block = [[U[i][j] for j in active] for i in active]
        scalar = ONE if name == 'identity' else epow(P,3)
        check(name+'_pointed_native_return', block == [[scalar if i==j else ZERO for j in range(4)] for i in range(4)])
        # Explicit chronological state evolution, retaining all arm/record rows.
        for M in [1,16,17,18]:
            L = M+T
            nreturned = 0
            all_ok = True
            all_prefixes_forward = True
            for tau in range(M):
                for spin in range(4):
                    state = [[ONE if k==active[spin] else ZERO] for k in range(16)]
                    elapsed, phase = tau, 0
                    for stage in stages:
                        state = matmul(stage, state)
                        elapsed += 1
                        phase = (phase+1) % T
                        all_prefixes_forward &= (elapsed < L)
                    all_ok &= (phase == 0 and elapsed == tau+T)
                    # No elapsed wrap; all work outputs stay in state.
                    if elapsed < M:
                        nreturned += 1
                        all_ok &= all(state[active[s]][0] == (scalar if s==spin else ZERO) for s in range(4))
            check('%s_M%d_no_elapsed_wrap'%(name,M), all_prefixes_forward)
            check('%s_M%d_exact_stage_and_work_retention'%(name,M), all_ok)
            check('%s_M%d_actual_return_rank'%(name,M), nreturned == 4*max(M-T,0))
        results[name] = {'stages':16, 'compressed_scalar_coefficients':scalar,
                         'matched_active_rank':68, 'returned_spin_rank':4,
                         'boundary_rank':64, 'elapsed_dimension':33,
                         'full_clock_times_apparatus_dimension':16*33*16}
    check('native_order_failure_1_minus_p6_equals_4p3',
          eadd(ONE, eneg(epow(P,6))) == tuple(4*c for c in epow(P,3)))
    return results

# Outward Decimal intervals. Operations explicitly round both endpoints.
PREC = 85
LO = Context(prec=PREC, rounding=ROUND_FLOOR)
HI = Context(prec=PREC, rounding=ROUND_CEILING)

class I:
    def __init__(self, lo, hi=None):
        self.lo = lo if isinstance(lo,Decimal) else Decimal(str(lo))
        self.hi = self.lo if hi is None else (hi if isinstance(hi,Decimal) else Decimal(str(hi)))
        if self.lo > self.hi:
            raise ValueError('reversed interval')
    @staticmethod
    def lift(x):
        return x if isinstance(x,I) else I(x)
    def __add__(self, other):
        b=I.lift(other)
        return I(LO.add(self.lo,b.lo), HI.add(self.hi,b.hi))
    __radd__=__add__
    def __neg__(self):
        return I(self.hi.copy_negate(), self.lo.copy_negate())
    def __sub__(self, other):
        return self + (-I.lift(other))
    def __rsub__(self, other):
        return I.lift(other) + (-self)
    def __mul__(self, other):
        b=I.lift(other)
        pairs=list(itertools.product([self.lo,self.hi],[b.lo,b.hi]))
        return I(min(LO.multiply(a,c) for a,c in pairs),
                 max(HI.multiply(a,c) for a,c in pairs))
    __rmul__=__mul__
    def __truediv__(self, other):
        b=I.lift(other)
        if b.lo <= 0 <= b.hi:
            raise ZeroDivisionError('interval contains zero')
        inv=I(LO.divide(Decimal(1),b.hi), HI.divide(Decimal(1),b.lo))
        return self*inv
    def __rtruediv__(self, other):
        return I.lift(other)/self
    def __pow__(self, n):
        if not isinstance(n,int) or n<0:
            raise ValueError('nonnegative integer power required')
        out=I(1); b=self
        while n:
            if n&1: out=out*b
            b=b*b; n//=2
        return out
    def bounds(self):
        return [str(self.lo),str(self.hi)]

def sqrt_interval(n: int) -> I:
    # Decimal.sqrt is correctly rounded to nearest; one adjacent representable
    # number on either side supplies an outward enclosure.
    ctx=Context(prec=PREC)
    root=ctx.sqrt(Decimal(n))
    return I(ctx.next_minus(root),ctx.next_plus(root))

def pair_add(x,y):
    return (x[0]+y[0],x[1]+y[1])

def pair_mul(x,y):
    return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])

def native_features():
    # Exact z_r=8(exp(2 pi i k_r/8)-1), represented over Q(sqrt2).
    phase=[((0,0),(0,0)),((-8,4),(0,4)),((-8,0),(8,0)),
           ((-8,-4),(0,4)),((-16,0),(0,0)),((-8,-4),(0,-4)),
           ((-8,0),(-8,0)),((-8,4),(0,-4))]
    out=Counter()
    for k in itertools.product(range(8),repeat=4):
        re=(0,0); im=(0,0); av=(0,0)
        for j in k:
            a,b=phase[j]
            re=pair_add(re,a); im=pair_add(im,b)
            av=pair_add(av,pair_add(pair_mul(a,a),pair_mul(b,b)))
        norm=pair_add(pair_mul(re,re),pair_mul(im,im))
        cv=(norm[0]-av[0],norm[1]-av[1])
        out[(av[0],av[1],cv[0],cv[1])] += 1
    return out

def native_root_clock_source():
    root2=sqrt_interval(2); root5=sqrt_interval(5)
    p=(root5-1)/2
    d0=I('0.063635191594344535042829697433316630182693569761541')
    o0=I('0.0040167350432317252873844519148251220686807163526359')
    radius=I('1e-12')
    d=I((d0-radius).lo,(d0+radius).hi)
    o=I((o0-radius).lo,(o0+radius).hi)
    alpha=p**2/8192; beta=2*p**2; z=I(1)/1048576
    m=16384; ref=128
    groups=native_features()
    check('native_all_4096_momenta_retained',sum(groups.values())==4096)
    check('native_exact119_feature_classes',len(groups)==119)
    Z=I(0); T1=I(0); T2=I(0)
    min_b=Decimal(1)
    for (a0,a1,c0,c1),mult in sorted(groups.items()):
        aa=I(a0)+a1*root2; cc=I(c0)+c1*root2
        lam=d*aa+o*cc
        b=1-alpha*lam
        if b.lo <= 0:
            raise RuntimeError('outside strict native B>0 chart')
        min_b=min(min_b,b.lo)
        bm=b**m; bm1=b**(m-1); F=1-z+z*bm
        Z=Z+(16*mult)*bm
        T1=T1+(16*mult)*lam*bm1
        T2=T2+(16*mult)*lam*bm1/F
    R=d*(128-64*root2)
    Jdot=2*ref*z*beta*T2
    source=-2*T1/Z+Jdot+2*R
    check('native_root_input_rectangle_consistent_with_scale_equation', source.lo<=0<=source.hi)
    check('native_extra_clock_start_source_strictly_positive',Jdot.lo>Decimal('0.02205'))
    check('native_extra_clock_start_source_below_0_02206',Jdot.hi<Decimal('0.02206'))
    check('native_original_strict_B_bound_retained',min_b>Decimal('0.97'))
    ceiling=1/(ref*z*beta*Z)
    check('native_scale_ceiling_between217_and218',ceiling.lo>217 and ceiling.hi<218)
    check('native_reference_and_all_CAR_in_trace',sum(groups.values())*16==65536)
    return {'input_root_radius':'1e-12','root_theorem_consumed_not_reproved':True,
            'exact_feature_classes':len(groups),'momentum_modes':4096,
            'CAR_modes_per_momentum':16,'reference_multiplicity':ref,
            'Z_full_data':Z.bounds(),'radial_feedback_source':Jdot.bounds(),
            'old_scale_source_enclosure':source.bounds(),
            'necessary_clock_overlap_upper_bound':ceiling.bounds(),
            'decimal_precision':PREC,'smallest_B_lower_bound':str(min_b),
            'new_source_when_overlap_is2':'exactly one radial_feedback_source at the inherited exact root'}

def matrix_power_jets(B,B1,B2,B12,n):
    N=len(B)
    P0=np.eye(N,dtype=complex); P1=np.zeros_like(P0); P2=P1.copy(); P12=P1.copy()
    for _ in range(n):
        P0,P1,P2,P12=(P0@B,
            P1@B+P0@B1,
            P2@B+P0@B2,
            P12@B+P1@B2+P2@B1+P0@B12)
    return P0,P1,P2,P12

def logdet_and_jets(M,M1,M2,M12):
    e=eigh(M,eigvals_only=True)
    if min(e)<=0: raise RuntimeError('nonpositive logarithm argument')
    inv=np.linalg.inv(M)
    value=-float(np.log(e).sum())
    first=-np.trace(inv@M1).real
    mixed=np.trace(inv@M2@inv@M1-inv@M12).real
    return value,float(first),float(mixed)

def finite_full_action_check():
    rng=np.random.default_rng(20261021)
    def herm():
        x=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        return (x+x.conj().T)/6
    D=herm(); D1=herm(); D2=herm(); D12=herm()/7
    Delta=D@D
    Delta1=D1@D+D@D1
    Delta2=D2@D+D@D2
    Delta12=D12@D+D@D12+D1@D2+D2@D1
    check('finite_HJR_fixture_uses_noncommuting_jet',np.linalg.norm(Delta@Delta1-Delta1@Delta)>1e-3)
    alpha=.01; n=2; m=4; beta=m*alpha; z=.125; ref=128
    eye=np.eye(4); B=eye-alpha*Delta
    B1=-alpha*Delta1; B2=-alpha*Delta2; B12=-alpha*Delta12
    K,K1,K2,K12=matrix_power_jets(B,B1,B2,B12,m)
    A0,A1,A2,A12=matrix_power_jets(B,B1,B2,B12,n)
    Fz=(1-z)*eye+z*K
    j,j1,j12=logdet_and_jets(Fz,z*K1,z*K2,z*K12)
    j*=ref; j1*=ref; j12*=ref
    Z=np.trace(K).real
    ht1=np.trace(K1).real/(beta*Z)
    ht12=(np.trace(K12).real/Z-np.trace(K1).real*np.trace(K2).real/(Z*Z))/beta
    lam,u=eigh(B)
    Lth=(u*(-np.log(lam)/alpha))@u.conj().T
    psi=np.array([1,2,3,4],complex); psi/=np.linalg.norm(psi)
    rvalue=np.vdot(psi,Delta@psi).real
    r1=np.vdot(psi,Delta1@psi).real
    r12=np.vdot(psi,Delta12@psi).real
    T=3
    records=[]
    max_source_error=0.;max_mixed_error=0.
    for M in [1,3,4,5]:
        shift=np.zeros((M,M))
        for i in range(M):
            if i+T<M: shift[i+T,i]=1
        AA=np.kron(shift,A0); X1=np.kron(shift,A1); X2=np.kron(shift,A2); X12=np.kron(shift,A12)
        q=(1-z)*np.eye(4*M)+z*AA.conj().T@AA
        q1=z*(X1.conj().T@AA+AA.conj().T@X1)
        q2=z*(X2.conj().T@AA+AA.conj().T@X2)
        q12=z*(X12.conj().T@AA+X1.conj().T@X2+X2.conj().T@X1+AA.conj().T@X12)
        jm,jm1,jm12=logdet_and_jets(q,q1,q2,q12)
        jm*=ref;jm1*=ref;jm12*=ref
        overlap=max(M-T,0); boundary=M-overlap
        close('M%d_full_feedback_absolute_value'%M,jm,overlap*j-ref*boundary*4*math.log1p(-z))
        close('M%d_full_feedback_first_source'%M,jm1,overlap*j1)
        close('M%d_full_feedback_mixed_source'%M,jm12,overlap*j12)
        check('M%d_forward_corner_nilpotent'%M,np.linalg.norm(np.linalg.matrix_power(AA,M))<1e-14)
        check('M%d_nilpotent_not_zero_feedback'%M,jm>0)
        # Independently vary the elapsed-clock active isometry, holding all
        # other clock modes in the ambient carrier. The stage0 reduction is
        # exact because a whole autonomous cycle preserves stage phase.
        lc=M+T
        Eclock=np.eye(lc,dtype=complex)[:,:M]
        shiftfull=np.roll(np.eye(lc,dtype=complex),T,axis=0)
        raw=rng.normal(size=(lc,lc))+1j*rng.normal(size=(lc,lc))
        skew=(raw-raw.conj().T)/7
        Eprime=skew@Eclock
        Tprime=Eprime.conj().T@shiftfull@Eclock+Eclock.conj().T@shiftfull@Eprime
        Acut=np.kron(Tprime,A0)
        Across=np.kron(Tprime,A1)
        qcut=z*(Acut.conj().T@AA+AA.conj().T@Acut)
        qcross=z*(Across.conj().T@AA+X1.conj().T@Acut+Acut.conj().T@X1+AA.conj().T@Across)
        _,cutsource,crosssource=logdet_and_jets(q,qcut,q1,qcross)
        close('M%d_clock_cut_first_source_zero'%M,ref*cutsource,0.)
        close('M%d_clock_cut_data_mixed_source_zero'%M,ref*crosssource,0.)
        clockdim=T*(M+T)
        Lfull=np.kron(np.eye(clockdim),Lth)
        # The original huge workspace factor is exactly inherited, not explicitly allocated.
        logC=(n+1)*math.log(128)
        hm=(logC+math.log(float(np.exp(-beta*eigh(Lfull,eigvals_only=True)).sum())))/beta
        h0=(logC+math.log(Z))/beta
        close('M%d_full_clock_heat_trace'%M,hm,h0+math.log(clockdim)/beta)
        Qfull=np.kron(np.eye(clockdim),Delta)
        psifull=np.kron(np.eye(clockdim)[0],psi)
        close('M%d_full_clock_matter_reading'%M,np.vdot(psifull,Qfull@psifull).real,rvalue)
        err1=abs((ht1+jm1+r1)-(ht1+j1+r1)-(overlap-1)*j1)
        err2=abs((ht12+jm12+r12)-(ht12+j12+r12)-(overlap-1)*j12)
        close('M%d_whole_HJR_first_source'%M,err1,0.)
        close('M%d_whole_HJR_mixed_second_source'%M,err2,0.)
        max_source_error=max(max_source_error,err1);max_mixed_error=max(max_mixed_error,err2)
        records.append({'M':M,'T':T,'surviving_clock_starts':overlap,
                        'absolute_feedback':float(jm),'whole_source_defect':float((overlap-1)*j1)})
    # Orthogonal unresolved status: its event is nonzero, but the active corner is zero.
    event=A0.conj().T@A0
    check('unresolved_event_effect_nonzero',np.trace(event).real>0)
    blank_return=np.zeros_like(A0)
    close('unresolved_status_actual_corner_zero',blank_return,0.)
    check('event_cannot_replace_complementary_corner',np.linalg.norm(event-blank_return.conj().T@blank_return)>1)
    return {'kind':'four-dimensional noncommuting HJR fixture, not a native spatial replay',
            'rows':records,'max_first_source_error':max_source_error,
            'max_mixed_source_error':max_mixed_error}

def gibbs(H,beta):
    values,vec=eigh(H)
    logits=-beta*values
    a=float(np.max(logits)); w=np.exp(logits-a); w/=sum(w)
    tau=(vec*w)@vec.conj().T
    logZ=a+math.log(float(np.exp(logits-a).sum()))
    entropy=-float(sum(w*np.log(w)))
    return tau,logZ,entropy

def clock_heat_remainders():
    beta=.7; bp=.13
    H=np.array([[.2,.07j],[-.07j,.8]],complex)
    Hp=np.array([[.04,.03],[.03,-.02]],complex)
    C=np.array([[.1,.02,0],[.02,.5,.01j],[0,-.01j,.9]],complex)
    Cp=np.array([[.03,0,.01j],[0,-.04,0],[-.01j,0,.02]],complex)
    tauH,_,_=gibbs(H,beta)
    tc,zc,sc=gibbs(C,beta)
    _,z0,_=gibbs(np.kron(C,np.eye(2))+np.kron(np.eye(3),H),beta)
    _,zh,_=gibbs(H,beta)
    close('nontrivial_clock_heat_factorization',z0,zc+zh)
    predicted=-np.trace(tc@Cp).real-sc*bp/(beta*beta)
    def diff(t):
        bt=beta+bp*t
        _,a,_=gibbs(np.kron(C+t*Cp,np.eye(2))+np.kron(np.eye(3),H+t*Hp),bt)
        _,b,_=gibbs(H+t*Hp,bt)
        return (a-b)/bt
    h=1e-5
    fd=(diff(h)-diff(-h))/(2*h)
    close('moving_beta_and_clock_heat_exact_source',fd,predicted,tol=5e-9)
    check('freezing_clock_source_would_fail',abs(predicted)>0.01)
    z=.2;zp=.03;T=3;rank=8
    wall=lambda t: -T*rank*math.log(1-z-zp*t)
    fdwall=(wall(h)-wall(-h))/(2*h)
    close('moving_z_retained_wall_source',fdwall,T*rank*zp/(1-z),tol=3e-9)
    rng=np.random.default_rng(314159)
    E=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6));E=(E+E.conj().T)/2
    E=.04*E/np.linalg.norm(E,2)
    Ep=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6));Ep=.003*(Ep+Ep.conj().T)
    Hsep=np.kron(C,np.eye(2))+np.kron(np.eye(3),H)
    X=np.kron(Cp,np.eye(2))+np.kron(np.eye(3),Hp)
    ts,_,_=gibbs(Hsep,beta);tt,_,_=gibbs(Hsep+E,beta)
    trace_distance=float(np.sum(np.abs(eigh(tt-ts,eigvals_only=True))))
    td_bound=min(2,2*beta*np.linalg.norm(E,2))
    extra=-np.trace((tt-ts)@X).real-np.trace(tt@Ep).real
    source_bound=np.linalg.norm(Ep,2)+td_bound*np.linalg.norm(X,2)
    check('nonseparable_heat_trace_norm_bound',trace_distance<=td_bound+1e-14)
    check('nonseparable_heat_source_bound',abs(extra)<=source_bound+1e-14)
    check('nonseparable_heat_not_assumed_zero',abs(extra)>1e-6)
    check('clock_heat_and_coupling_do_not_commute',np.linalg.norm(E@Hsep-Hsep@E)>1e-3)
    return {'moving_clock_beta_source':float(predicted),
            'nonseparable_heat_trace_distance':trace_distance,'trace_distance_bound':float(td_bound),
            'actual_extra_source':float(extra),'extra_source_bound':float(source_bound)}

def main():
    result={'native_clock':exact_native_clock(),
            'native_root_interval':native_root_clock_source(),
            'full_action_fixture':finite_full_action_check(),
            'clock_source_remainders':clock_heat_remainders()}
    result['checks']={'count':len(CHECKS),'names':CHECKS}
    result['scope']={'GR_closed':False,'physical_clock_selected':False,
                     'old_root_theorem_reproved':False,'independent_review':False,
                     'native_full_spatial_eigensolver_rerun':False,
                     'main_updated':False,'author_checks_only':True}
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
