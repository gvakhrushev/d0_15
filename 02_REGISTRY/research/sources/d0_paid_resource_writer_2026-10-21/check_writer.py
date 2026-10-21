#!/usr/bin/env python3
"""Bounded author checks for a paid rational resource writer.

Exact tests use every output row of a finite coherent writer isometry.
The native 32D Julia tests verify exact rational orthogonality and bounded
floating approximation separately. They do not replay the repository's
all42/GR, all-site full128, or Lean certificates.
"""
from __future__ import annotations
import json
import math
from fractions import Fraction as Q
from functools import reduce
from itertools import product
from pathlib import Path
import argparse
import numpy as np
import sympy as sp
from scipy.linalg import expm

checks=[]

def require(ok, name):
    if not bool(ok):
        raise ArithmeticError(name)
    checks.append(name)


def cx(n,c,t):
    M=sp.zeros(2**n)
    for j in range(2**n):
        k=j ^ (((j>>c)&1)<<t)
        M[k,j]=1
    return M


def bit_writer():
    A=cx(3,0,1); B=cx(3,1,2)
    zero=B*B*A*A
    one=B*A*B*A
    require(zero==sp.eye(8), 'zero table bit: A A B B is identity on all columns')
    require(one==cx(3,0,2), 'one table bit: A B A B is CX(c,b) on all columns')
    for a in (0,1):
        inp=1+2*a
        require(one[:,inp]==sp.eye(8)[:,inp+4], f'known-one writes bit and preserves scratch a={a}')
    require(sorted('AABB')==sorted('ABAB'), 'same original CNOT addresses and multiplicities')
    # Complements on the same 1D input corner differ, despite equal counted costs.
    require(zero[1,1]==1 and one[1,1]==0, 'same-count hostile control: different true blank corners')
    return {'zero_word':'A A B B','one_word':'A B A B','CNOT_per_table_bit':4,
            'whole_Book_price_invariance_claimed':False}


def signed_table(U, R):
    N=U*R
    require(all(x.q==1 for x in N), 'common denominator gives actual integer table')
    return np.array(N.tolist(),dtype=np.int64)


def complete_isometry_numerators(N, B):
    """All coherent work rows after comparator, sign, and Walsh transforms.

    V = W/(D*B). Row indices are (output i, transformed input j0,
    transformed uniform l0, comparison f). The only measured bit is the
    aggregate success predicate (j0=l0=0,f=1). Failure work is not measured.
    """
    d=N.shape[0]
    require(d>1 and d&(d-1)==0 and B&(B-1)==0, 'power-of-two work dimensions')
    require(np.max(np.abs(N))<=B, 'integer comparator threshold fits actual uniform register')
    parity=lambda x: bin(x).count('1')&1
    H=np.array([[(-1)**parity(x&y) for y in range(B)] for x in range(B)], dtype=np.int64)
    W=np.zeros((d*d*B*2,d),dtype=np.int64)
    success=[]
    for i in range(d):
        for j in range(d):
            n=int(N[i,j]); mag=abs(n); sign=-1 if n<0 else 1
            q0=(np.arange(B)>=mag).astype(np.int64)
            q1=sign*(np.arange(B)<mag).astype(np.int64)
            v0=H@q0; v1=H@q1
            for jout in range(d):
                phase=(-1)**parity(jout&j)
                start=((i*d+jout)*B)*2
                W[start:start+B*2:2,j]=phase*v0
                W[start+1:start+B*2:2,j]=phase*v1
        success.append(((i*d)*B)*2+1)
    return W, np.array(success,dtype=int)


def entropy_phi(q):
    p=(math.sqrt(5)-1)/2; ell=-math.log(p)
    return -sum(float(x)*math.log(float(x))/ell for x in q if x>0)


def exact_writer():
    U0=sp.Matrix([[Q(3,5),-Q(4,5)],[Q(4,5),Q(3,5)]])
    U1=sp.Matrix([[Q(5,13),-Q(12,13)],[Q(12,13),Q(5,13)]])
    R=65; B=128; d=2; den=d*B
    receipts=[]; fine_entropies=[]
    Craw=sp.Matrix([[1,2],[2,1]])
    gram=Craw.T*Craw/10
    for a,U in enumerate((U0,U1)):
        N=signed_table(U,R)
        W,rows=complete_isometry_numerators(N,B)
        K=W[rows]
        require(np.array_equal(K,N), f'writer {a}: literal successful amplitude equals table/(d B)')
        require(np.array_equal(W.T@W,den**2*np.eye(d,dtype=np.int64)), f'writer {a}: all-output isometry')
        require(np.array_equal(K.T@K,R**2*np.eye(d,dtype=np.int64)), f'writer {a}: success effect scalar exactly')
        failure=np.delete(W,rows,axis=0)
        require(np.array_equal(failure.T@failure,(den**2-R**2)*np.eye(d,dtype=np.int64)), f'writer {a}: full coherent failure effect scalar')
        rS=(Craw.T*sp.Matrix(K.T@K)*Craw)/(10*den**2)
        rF=(Craw.T*sp.Matrix(failure.T@failure)*Craw)/(10*den**2)
        s=sp.Rational(R**2,den**2)
        require(rS==s*gram, f'writer {a}: success preserves non-diagonal oldRIGHT')
        require(rF==(1-s)*gram, f'writer {a}: failure also preserves non-diagonal oldRIGHT')
        require(rS+rF==gram, f'writer {a}: no discarded-reference branch')
        # A changed interface that reads every work basis vector has a different entropy.
        qfine=np.sum(W.astype(float)**2,axis=1)/(d*den**2)
        fine_entropies.append(entropy_phi(qfine))
        receipts.append({'matrix':str(U),'all_work_rows':len(W),'success':str(s),
                         'coherent_herald_entropy_phi':entropy_phi([s,1-s]),
                         'additional_fine_work_measurement_entropy_phi':fine_entropies[-1]})
    require(abs(fine_entropies[0]-fine_entropies[1])>1e-4, 'negative control: measuring failure work changes the declared entropy law')
    s=sp.Rational(R**2,den**2)
    require(s>sp.Rational(1,4*d*d) and s<=sp.Rational(1,d*d), 'success lower bound independent of denominator bits')
    # Full 128-column algebraic effect; no small reference is substituted in the theorem.
    big=sp.kronecker_product(sp.eye(64),U0)
    require(big.T*big==sp.eye(128), '128-dimensional LEFT orthogonal matrix retains every column')
    require((s*big.T*big)/128 == s*sp.eye(128)/128, 'full RIGHT128 success Gram identity')
    # Nonunitary data weighting does not pass the same test.
    bad=sp.diag(sp.Rational(3,5),sp.Rational(4,5))
    require(bad.T*bad!=sp.trace(bad.T*bad)*sp.eye(2)/2, 'negative control: nonunitary target leaves operator normalization')
    return {'cases':receipts,'exact_reference_Gram':str(gram),'no_quantum_work_erased':True}


ORDER=(0,2,3,1)
def creators():
    out=[]
    for role in range(4):
        C=np.zeros((16,16))
        prev=ORDER[:ORDER.index(role)]
        for mask in range(16):
            if not (mask>>role)&1:
                C[mask+(1<<role),mask]=(-1)**sum((mask>>j)&1 for j in prev)
        out.append(C)
    return out


def psqrt(X):
    ev,V=np.linalg.eigh((X+X.T)/2)
    require(ev.min()>1e-6,'strict native positive Julia defect')
    return (V*np.sqrt(ev))@V.T


def native_julia(theta):
    cs=creators(); gen=cs[0]@cs[1].T+cs[1]@cs[0].T
    X=(3/5)*cs[1]@expm(theta*gen)
    L=psqrt(np.eye(16)-X@X.T); R=psqrt(np.eye(16)-X.T@X)
    return np.block([[X,L],[R,-X.T]])


def native_julia_rational_base():
    cs=[sp.Matrix(c.astype(int)) for c in creators()]
    X=sp.Rational(3,5)*cs[1]
    L=sp.diag(*[sp.sqrt(v) for v in (sp.eye(16)-X*X.T).diagonal()])
    R=sp.diag(*[sp.sqrt(v) for v in (sp.eye(16)-X.T*X).diagonal()])
    return X.row_join(L).col_join(R.row_join(-X.T))


def rationalize_near(O,J0,scale):
    base=np.array(J0.tolist(),float)
    V=O@base.T
    A=np.linalg.solve((V+np.eye(len(V))).T,(V-np.eye(len(V))).T).T
    A=(A-A.T)/2
    Aq=sp.zeros(len(V))
    for i in range(len(V)):
        for j in range(i):
            v=sp.Rational(round(A[i,j]*scale),scale)
            Aq[i,j]=v; Aq[j,i]=-v
    I=sp.eye(len(V))
    Oq=(I-Aq).inv(method='DM')*(I+Aq)*J0
    require(Oq.T*Oq==I, 'exact rational 32D native-program orthogonality')
    return Oq


def native_targets():
    J0=native_julia_rational_base()
    require(J0.T*J0==sp.eye(32), 'literal rational base Julia on full CAR16 plus coefficient')
    require(np.linalg.norm(native_julia(0)-np.array(J0.tolist(),float))<1e-13,'native float and rational base match')
    targets=[]
    for scale in (10**4,10**6):
        J=native_julia(.08)
        Jq=rationalize_near(J,J0,scale)
        Jf=np.array(Jq.tolist(),float)
        err=float(np.linalg.norm(Jf-J,2))
        require(err<40/scale, 'explicit approximation controlled without a continuous primitive')
        choierr=float(np.linalg.norm(Jf-J,'fro')/math.sqrt(32))
        require(choierr<=err+1e-12,'full32 Choi state error bounded by operator error')
        R=sp.ilcm(*[int(v.q) for v in Jq])
        b=int(R).bit_length()
        if int(R)==1<<(b-1): b-=1
        ratio=float(sp.Rational(int(R),2**b))
        s=ratio**2/32**2
        require(s>1/(4*32**2)-1e-16 and s<=1/32**2+1e-16,'32D local writer readiness bound independent of address multiplicity')
        targets.append({'coefficient_rounding_denominator':scale,'operator_error':err,
                        'full32_Choi_error':choierr,'integer_table_bits_per_entry':b+2,
                        'local_writer_herald_success':s})
    require(targets[1]['operator_error']<targets[0]['operator_error']/10,'native resource approximation improves')
    # The real program consumes all Bell/Pauli outcomes, with exactly equal effects.
    X=sp.Matrix([[0,1],[1,0]]); Z=sp.diag(1,-1); I2=sp.eye(2)
    u=J0
    for idx in range(5):
        factors=[I2]*5; factors[idx]=X
        pa=reduce(sp.kronecker_product,factors)
        require((u*pa).T*(u*pa)==sp.eye(32),'five-qubit original Bell X-frame effect')
        factors=[I2]*5; factors[idx]=Z
        pa=reduce(sp.kronecker_product,factors)
        require((u*pa).T*(u*pa)==sp.eye(32),'five-qubit original Bell Z-frame effect')
    # Noncommutativity with other generators is not replaced by scalar rotations.
    require(np.linalg.norm(native_julia(.08)-native_julia(.07))>1e-5,'actual native proper-link parameter moves program state')
    return {'carrier':'all16 CAR + coefficient, d=32; original ACDB order',
            'targets':targets,'no_all42_replay_claimed':True}


def native_source_composition():
    """Nonzero first/second sources through a supplied original Julia block.

    This is an input-stage test, NOT a replay of the full GR detector. A fixed
    coefficient report after accepted Bell teleportation has probability
    r(theta)=9 cosh(theta)^2/50 for a trace CAR input with coefficient zero.
    Wrong Bell labels and writer failures use a separately paid fair report.
    Their probabilities and their CQ entropies are code-independent.
    """
    theta=.08; ell=math.log((1+math.sqrt(5))/2)
    a=9/50
    r=a*math.cosh(theta)**2
    dr=a*math.sinh(2*theta)
    ddr=2*a*math.cosh(2*theta)
    hp=math.log((1-r)/r)/ell
    hpp=-1/(ell*r*(1-r))
    exact_first=-hp*dr; exact_second=-hpp*dr*dr-hp*ddr
    J0=native_julia_rational_base(); out=[]
    for delta in (.02,.01,.005):
        scale=math.ceil(delta**-5)
        matrices=[]; qs=[]
        for t in (theta-delta,theta,theta+delta):
            J=native_julia(t); Jq=rationalize_near(J,J0,scale)
            Xq=Jq[:16,:16]
            rq=sp.trace(Xq.T*Xq)/16
            require(0<rq<1,'actual rational Julia coefficient-report probability')
            matrices.append(Jq);qs.append(float(rq))
        denoms=[int(x.q) for M in matrices for x in M]
        R=int(sp.ilcm(*denoms));b=R.bit_length()
        if R==1<<(b-1): b-=1
        writer_gain=float(sp.Rational(R,32*2**b))**2
        bell_gain=1/32**2
        values=[-entropy_phi([q,1-q]) for q in qs]
        first=(values[2]-values[0])/(2*delta)
        second=(values[2]-2*values[1]+values[0])/delta**2
        require(abs(first-exact_first)<2*delta**2,'native first source through rational writer converges')
        require(abs(second-exact_second)<2*delta**2,'native second source through rational writer converges')
        # Same exact success scalar for all three tables. No target-dependent
        # normalization is thrown away or divided out without recording it.
        for M in matrices:
            require((M*R).T*(M*R)==R**2*sp.eye(32),'one denominator for the whole actual field stencil')
        out.append({'delta':delta,'table_rounding_denominator':scale,
                    'common_integer_denominator_bits':b,'writer_gain':writer_gain,
                    'Bell_accept_gain':bell_gain,
                    'complete_source_gain_before_factory_readiness':writer_gain*bell_gain,
                    'first_source_after_recorded_gain_division':first,
                    'second_source_after_recorded_gain_division':second,
                    'first_error':abs(first-exact_first),'second_error':abs(second-exact_second)})
    require(out[-1]['first_error']<out[0]['first_error']/8,'nonzero native first-source convergence observed')
    require(out[-1]['second_error']<out[0]['second_error']/8,'native second-source convergence observed')
    return {'source_type':'coefficient report for actual proper-link Julia block, all CAR16',
            'ideal_probability_formula':'9 cosh(theta)^2/50',
            'ideal_first_source':exact_first,'ideal_second_source':exact_second,
            'samples':out,'entire42_source_replayed':False}


def source_jet_checks():
    # Exact rational countercontrols for the stationarity-assisted jet estimate.
    h=sp.symbols('h',positive=True)
    x,y,u,v=sp.symbols('x y u v',real=True)
    F=x*y+sp.Rational(1,3)*x**3+sp.Rational(2,5)*y**4+u*u+3*v*v+u*x
    require(sp.Matrix([sp.diff(F,z) for z in (x,y,u,v)]).subs({x:0,y:0,u:0,v:0})==sp.zeros(4,1),
            'declared parent product-resource critical point')
    def val(a,b,du,dv): return F.subs({x:a,y:b,u:du,v:dv})
    # Perturb prepared resources at stencil nodes by <=h^3; include a genuine normal component.
    plus=val(h,0,h**3,-h**3); minus=val(-h,0,-h**3,h**3)
    d1=sp.expand((plus-minus)/(2*h))
    require(sp.limit(d1/h**2,h,0)==sp.Rational(1,3),'first-source error remains order h^2')
    pp=val(h,h,h**3,h**3); pm=val(h,-h,-h**3,h**3)
    mp=val(-h,h,h**3,-h**3); mm=val(-h,-h,-h**3,-h**3)
    dxy=sp.expand((pp-pm-mp+mm)/(4*h*h))
    require(sp.limit(dxy,h,0)==1,'whole mixed source converges to parent Hessian')
    require(sp.limit((dxy-1)/h**2,h,0).is_finite,'mixed-source accuracy is order h^2')
    # The constant writer charge never disappears from values; it cancels only in comparisons.
    C,eta=sp.symbols('C eta',positive=True)
    require(sp.simplify(((C+eta*plus)-(C+eta*minus))/(2*h)/eta-d1)==0,
            'full paid baseline retained and common readiness divided explicitly')
    # If independent upstream charge varies with the code, it cannot be removed by this theorem.
    require(sp.simplify(((C+h+eta*plus)-(C-h+eta*minus))/(2*h)/eta-d1)==1/eta,
            'negative control: unpriced moving upstream term survives')
    # A genuinely retained uniform programme selector has an averaged price,
    # not the source of either conditional programme.
    z=sp.symbols('z',real=True)
    s0=C+z; s1=C-z
    require(sp.diff((s0+s1)/2,z)==0 and sp.diff(s0,z)==1,
            'negative control: fixed-selector mixture is not one conditional field price')
    M,dmax=100,32
    L=math.ceil(8*dmax*dmax*math.log(2*M))
    require(M*math.exp(-L/(8*dmax*dmax))<=.5,
            'finite paid bank readiness union bound')
    return {'first_difference':str(d1),'mixed_difference':str(dxy),
            'readiness_example':{'resources':M,'local_d_max':dmax,'attempts_per_resource':L},
            'convergence_is_not_exact_finite_stationarity':True} 


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--json',type=Path); args=ap.parse_args()
    out={'status':'PASS_PAID_RATIONAL_WRITER_AUTHOR_CHECKS',
         'bit_word':bit_writer(),'complete_writer':exact_writer(),
         'native_program':native_targets(),'native_source_composition':native_source_composition(),
         'source_stencil':source_jet_checks(),
         'scope':{'actual_Book03_selected':False,'same_supplied_addressed_gate_grammar':True,
                  'old_RIGHT_preserved_on_each_coarse_branch':True,
                  'native_primitive_clock_selection_proved':False,
                  'single_autonomous_continuous_field_writer':False,
                  'exact_finite_GR_root_proved':False,'GR_closed':False}}
    out['check_count']=len(checks); out['checks']=checks
    text=json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if args.json: args.json.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__': main()
