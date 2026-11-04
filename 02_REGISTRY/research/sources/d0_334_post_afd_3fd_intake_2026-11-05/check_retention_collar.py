#!/usr/bin/env python3
"""Exact positive native retention macros with shared, unreset helpers.

The sparse growing clock is an explicit q=0 finite check, not a replacement
for the owned q>=3 asymptotic theorem. No continuous native primitive,
physical task selector, full Cost-Info binding or Einstein closure is added.
"""
from __future__ import annotations
import os
for task_thread_option in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[task_thread_option] = '1'
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy import sparse
import sympy as sp

CHECKS: list[dict[str,str]] = []
RESIDUALS: dict[str,float] = {}
def need(condition: object, label: str, kind: str='exact_golden') -> None:
    if not bool(condition):
        raise ArithmeticError(label)
    CHECKS.append({'label':label,'kind':kind})
def close(actual: object, expected: object, label: str, tolerance: float=2e-11) -> None:
    error=float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    RESIDUALS[label]=error
    need(np.isfinite(error) and error<=tolerance,label,'nominal_numeric')

a=sp.symbols('a',positive=True)
p=a*a
modulus=a**4+a**2-1
v=sp.Matrix([a,p])
G=sp.Matrix([[a,-p],[p,a]])
J=sp.Matrix([[0,-1],[1,0]])
X=sp.Matrix([[0,1],[1,0]])
Z=sp.diag(1,-1)
def red(value: sp.Expr) -> sp.Expr:
    if value==0:
        return sp.S.Zero
    num,den=sp.fraction(sp.cancel(value))
    return sp.rem(sp.expand(sp.rem(num,modulus,a)*sp.invert(sp.rem(den,modulus,a),modulus,a)),modulus,a)
def reduced(matrix: sp.MatrixBase) -> sp.MatrixBase:
    return matrix.applyfunc(red)
def equal(left: sp.MatrixBase,right: sp.MatrixBase) -> bool:
    return left.shape==right.shape and all(red(x)==0 for x in left-right)

# Exact rational root isolation and Horner bounds, not floating admission.
root_intervals=sp.Poly(modulus,a).intervals(eps=sp.Rational(1,10**60))
positive_intervals=[bounds for bounds,multiplicity in root_intervals if bounds[0]>0 and multiplicity==1]
need(len(positive_intervals)==1,'exact polynomial isolator finds one positive real root')
alo,ahi=positive_intervals[0]
need(modulus.subs(a,alo)<0 and modulus.subs(a,ahi)>0 and alo>0,
     'rational interval isolates the unique positive Golden root')
def interval(poly: sp.Expr) -> tuple[sp.Rational,sp.Rational]:
    lo=hi=sp.S.Zero
    for coefficient in sp.Poly(red(poly),a).all_coeffs():
        corners=[lo*alo,lo*ahi,hi*alo,hi*ahi]
        lo,hi=min(corners)+coefficient,max(corners)+coefficient
    return lo,hi

def gate(bits: int, instruction: tuple) -> sp.Matrix:
    kind=instruction[0]
    if kind=='G':
        wire=instruction[1]
        return sp.kronecker_product(sp.eye(2**wire),G,sp.eye(2**(bits-wire-1)))
    if kind=='CX':
        control,target=instruction[1:]
        need(0<=control<bits and 0<=target<bits and control!=target,
             'literal CX address is valid','structural')
        matrix=sp.zeros(2**bits)
        for col in range(2**bits):
            row=col^(1<<(bits-1-target)) if col&(1<<(bits-1-control)) else col
            matrix[row,col]=1
        return matrix
    raise ValueError('unsupported actual instruction')
def execute(bits: int,word: list[tuple]) -> sp.Matrix:
    U=sp.eye(2**bits)
    for instruction in word:
        U=reduced(gate(bits,instruction)*U)
    return U

def macros(ret: int) -> tuple[list[tuple],list[tuple],list[tuple]]:
    # Rightmost-first displayed U = CX G^19 CX G means this chronology.
    first=[('G',ret),('CX',0,ret)]+[('G',ret)]*19+[('CX',0,ret)]
    second=[('G',ret),('CX',ret,0)]+[('G',ret)]*19+[('CX',ret,0)]
    i5=[('CX',ret,0),('CX',0,1),('CX',ret,0),('CX',0,1),('CX',ret,1)]
    i2=[('CX',ret,0),('CX',ret,0)]
    baseline=[('G',ret)]+i5+i2*8
    return first,second,baseline

need(equal(G.T*G,sp.eye(2)) and equal(v.T*v,sp.ones(1)),
     'original G and its canonical birth are normalized')
Gn=sp.eye(2)
for _ in range(19):
    Gn=reduced(G*Gn)
cn,sn=Gn[0,0],Gn[1,0]
need(equal(Gn,sp.Matrix([[cn,-sn],[sn,cn]])), 'positive nineteen-call power has the exact rotation form')
need(red(cn*cn+sn*sn-1)==0,'nineteen-call cosine and sine normalize exactly')
cbar=sp.Rational(9,10)
delta0=sp.Rational(1,10)
near_margin=red(delta0**2-2*(1-cn))
need(interval(near_margin)[0]>0,
     'exact rational collar proves norm(G^19-I)<one tenth')
need(ahi<sp.Rational(4,5) and ahi+delta0<cbar,
     'actual one-tenth operator collar implies strict compression bound nine tenths')
need(interval(sn)[0]>0,'nineteen-call sine is strictly positive on the exact root collar')

u1_word,_,baseline1=macros(2)
_,u2_word,baseline2=macros(3)
need(len(u1_word)==len(u2_word)==len(baseline1)==len(baseline2)==22,
     'all comparison macros have exactly22 positive native calls','structural')
need(all(op[0] in ('G','CX') for word in (u1_word,u2_word,baseline1,baseline2) for op in word),
     'there is no inverse reset or continuously adjustable primitive','structural')
U1=execute(3,u1_word)
U2=execute(4,u2_word)
need(equal(execute(3,baseline1),gate(3,('G',2))), 'paid22-call first baseline has full endpoint G_ret tensor I_helpers')
need(equal(execute(4,baseline2),gate(4,('G',3))), 'paid22-call second baseline has full endpoint G_ret tensor I_helpers')
J1=sp.kronecker_product(sp.eye(4),v)
B1=reduced(J1.T*U1*J1)
J2=sp.kronecker_product(sp.eye(8),v)
B2_with_old=reduced(J2.T*U2*J2)
B1_expected=sp.kronecker_product(a*cn*sp.eye(2)-p*sn*Z,sp.eye(2))
B2=sp.kronecker_product(a*cn*sp.eye(2)-p*sn*X,sp.eye(2))
need(equal(B1,B1_expected),'first actual macro compresses to a cn I-p sn Z on helper0')
need(equal(B2_with_old,sp.kronecker_product(B2,sp.eye(2))),
     'second actual macro compresses to a cn I-p sn X and leaves earlier sealed retention untouched')
need(not equal(B1*B2,B2*B1),'shared-helper compression operators genuinely do not commute')
for sign in (-1,1):
    need(interval(red(cbar*cbar-(a*cn+sign*p*sn)**2))[0]>0,
         'both exact compression eigenvalues lie strictly inside cbar, sign '+str(sign))
initial=sp.kronecker_product(sp.eye(4),v,v)
full=reduced(U2*sp.kronecker_product(U1,sp.eye(2)))
compression=reduced(initial.T*full*initial)
need(equal(compression,B2*B1),'complete cold helper map is the ordered noncommutative product B2 B1')
eta=sp.kronecker_product(v,v)
actual_cold=red((eta.T*compression*eta)[0])
fake_product=red((eta.T*B2*eta)[0]*(eta.T*B1*eta)[0])
need(red(actual_cold-fake_product)!=0,'reset/product-of-expectations replacement is false')
need(red(actual_cold-fake_product+2*a*p**6*sn**2)==0,
     'missing helper correlation is exactly minus2 a p^6 sin(19alpha)^2')

def build_clock(which: str) -> dict:
    events: list[tuple]=[('birth',),('birth',),('birth',)]
    events+=u1_word if which=='noncommuting' else baseline1
    events+=[('birth',)]
    events+=u2_word if which=='noncommuting' else baseline2
    events+=[('birth',),('G',4),('G',4)]
    dims=[]; actions=[]; passive=[]; bits=0
    for event in events:
        dims.append(2**bits)
        if event[0]=='birth':
            Fj=sp.kronecker_product(sp.eye(2**bits),v)
            bits+=1
            actions.append(Fj); passive.append(Fj)
        else:
            actions.append(gate(bits,event)); passive.append(sp.eye(2**bits))
    N,D=len(events),sum(dims)
    need((N,D,bits)==(51,623,5),which+' actual clock has N51 D623 and five separate births','exact_integer')
    starts=[sum(dims[:j]) for j in range(N)]
    final_dim=dims[-1]
    B=[sp.zeros(1)]*N; B[-1]=sp.eye(final_dim)
    for j in range(N-2,-1,-1):
        B[j]=reduced(B[j+1]*passive[j])
    details=[sp.eye(1)]
    for j in range(1,N):
        details.append(reduced(sp.eye(dims[j])-passive[j-1]*passive[j-1].T))
    R_blocks=[B[0].T]+[reduced(details[j]*B[j].T) if details[j]!=sp.zeros(dims[j])
                          else sp.zeros(dims[j],final_dim) for j in range(1,N)]
    # Only the genuinely nonzero birth-detail blocks are used in this exact sum.
    closure_sum=sp.zeros(final_dim)
    for block in R_blocks:
        if block!=sp.zeros(*block.shape):
            closure_sum+=block.T*block
    need(equal(closure_sum,sp.eye(final_dim)),which+' complete canonical birth closure obeys R*R=I exactly')
    need(details[-1]==sp.zeros(final_dim),which+' final actual G follows a square stage and D_final=0')
    # Verify all local pieces exactly; GROWING G4-G6 then give full unitarity.
    all_isometries=all(equal(Fj.T*Fj,sp.eye(dims[j])) for j,Fj in enumerate(actions[:-1]))
    need(all_isometries,which+' every actual stage is exactly isometric on its own carrier')
    range_identities=all(equal(Fj*Fj.T,sp.eye(dims[j+1])-details[j+1]) for j,Fj in enumerate(actions[:-1]))
    need(range_identities,which+' each exact stage range is the complement of its actual birth detail')
    af=float(np.sqrt((np.sqrt(5.0)-1)/2))
    def numeric(matrix: sp.MatrixBase) -> np.ndarray:
        return np.asarray(matrix.subs(a,af),dtype=float)
    def exact_support(matrix: sp.MatrixBase) -> sparse.csr_matrix:
        # The support is derived over the exact Golden field. Numeric entries
        # and floating cancellation thresholds play no role in this graph.
        rows=[]; columns=[]
        for row in range(matrix.rows):
            for col in range(matrix.cols):
                if matrix[row,col]!=0 and red(matrix[row,col])!=0:
                    rows.append(row); columns.append(col)
        return sparse.csr_matrix((np.ones(len(rows),dtype=np.int64),(rows,columns)),
                                 shape=matrix.shape,dtype=np.int64)
    S=sparse.lil_matrix((D,D),dtype=float)
    S_support=sparse.lil_matrix((D,D),dtype=np.int64)
    for j,Fj in enumerate(actions[:-1]):
        S[starts[j+1]:starts[j+1]+dims[j+1],starts[j]:starts[j]+dims[j]]=numeric(Fj)
        S_support[starts[j+1]:starts[j+1]+dims[j+1],starts[j]:starts[j]+dims[j]]=exact_support(Fj)
    S=S.tocsr()
    R=sparse.vstack([sparse.csr_matrix(numeric(block)) for block in R_blocks],format='csr')
    closing=R@sparse.csr_matrix(numeric(actions[-1]))
    T=S+sparse.hstack([sparse.csr_matrix((D,D-final_dim)),closing],format='csr')
    R_support=sparse.vstack([exact_support(block) for block in R_blocks],format='csr')
    closing_support=R_support@exact_support(actions[-1])
    # Product support is deliberately conservative: algebraic cancellation
    # can remove an edge but can never add one. All coefficients here are
    # nonnegative integers, so zero path count is an exact obstruction.
    pattern=S_support.tocsr()+sparse.hstack([
        sparse.csr_matrix((D,D-final_dim),dtype=np.int64),closing_support],format='csr')
    pattern.data[:]=1
    error=(T.T@T-sparse.eye(D,format='csr')).tocoo()
    close(error.data if error.nnz else [0],0.,which+' full sparse623-clock is unitary on every column')
    need(pattern[starts[-1]:,starts[-1]:].nnz==0,
         which+' exact conservative graph has zero complete final clock diagonal block','exact_integer')
    # First retention G is an actual smooth old-row companion; no new primitive.
    old_index=3
    dgate=sp.kronecker_product(sp.eye(4),J*G)
    dT=sparse.lil_matrix((D,D),dtype=float)
    dT[starts[old_index+1]:starts[old_index+1]+dims[old_index+1],
       starts[old_index]:starts[old_index]+dims[old_index]]=numeric(dgate)
    dT=dT.tocsr()
    dpattern=sparse.lil_matrix((D,D),dtype=np.int64)
    dpattern[starts[old_index+1]:starts[old_index+1]+dims[old_index+1],
             starts[old_index]:starts[old_index]+dims[old_index]]=exact_support(dgate)
    dpattern=dpattern.tocsr()
    power=sparse.eye(D,format='csr'); support_power=sparse.eye(D,dtype=np.int64,format='csr')
    traces=[]; derivatives=[]
    for age in range(1,5):
        structural=(support_power@dpattern).diagonal()
        need(np.all(structural==0),which+f' age{age} cannot return through the actual old retention variation','exact_integer')
        derivatives.append(float(age*(power@dT).diagonal().sum()))
        power=power@T; support_power=support_power@pattern
        traces.append(float(power.diagonal().sum()))
    close(derivatives,np.zeros(4),which+' all checked low-winding old-source traces vanish')
    return dict(N=N,D=D,widths=dims,instruction_count=len(events)-5,
                birth_count=5,low_winding_traces=traces,old_source_traces=derivatives,
                sparse_entries=int(T.nnz),exact_support_entries=int(pattern.nnz),
                support_origin='exact Golden stage and closure supports; conservative integer products',
                profile='q=0 diagnostic; not the q>=3 asymptotic theorem')

clocks={name:build_clock(name) for name in ('noncommuting','canonical')}
close(clocks['noncommuting']['low_winding_traces'],clocks['canonical']['low_winding_traces'],
      'actual different retained prefixes have identical checked short-winding clock traces')

# A genuinely movable rank-one SCENE feedback projector needs no fixed orientation.
zeta,f0,f1=sp.symbols('zeta f0 f1',real=True)
Q0=sp.diag(1,0); Q1=v*v.T; F=sp.diag(f0,f1)
need(equal(Q1*Q1,Q1) and red(sp.trace(Q1)-1)==0,'moved scene projector is an exact rank-one projection')
det0=(sp.eye(4)-zeta*sp.kronecker_product(Q0,F)).det()
det1=(sp.eye(4)-zeta*sp.kronecker_product(Q1,F)).det()
need(red(det1-det0)==0,'entire feedback determinant is independent of the rank-one scene orientation')

# Generic noncommuting 2x2 return and its true negative logdet derivative.
x00,x01,x10,x11,y00,y01,y10,y11,t=sp.symbols('x00 x01 x10 x11 y00 y01 y10 y11 t',real=True)
C=sp.Matrix([[x00,x01],[x10,x11]])
dC=sp.Matrix([[y00,y01],[y10,y11]])
DC=(1-zeta)*sp.eye(2)+zeta*C.T*C
dDC=zeta*(dC.T*C+C.T*dC)
ddet=sp.diff(((1-zeta)*sp.eye(2)+zeta*(C+t*dC).T*(C+t*dC)).det(),t).subs(t,0)
need(sp.expand(ddet-sp.trace(DC.adjugate()*dDC))==0,
     'full noncommuting return obeys dJ=-z Tr[D^-1(dC* C+C* dC)]','exact_symbolic')

result=dict(schema='d0.open-retention-collar/1',status='PASS',
    checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__),
    check_count=len(CHECKS),classifications={kind:sum(c['kind']==kind for c in CHECKS) for kind in sorted({c['kind'] for c in CHECKS})},
    checks=CHECKS,residuals=RESIDUALS,max_nominal_residual=max(RESIDUALS.values()),
    arithmetic='Q[a]/(a^4+a^2-1), exact rational isolating interval; nominal sparse-clock residuals labelled',
    collar=dict(n=19,cbar=str(cbar),cosine=str(cn),sine=str(sn),
                near_margin_interval=[str(x) for x in interval(near_margin)],
                actual_cold=str(actual_cold),false_product=str(fake_product)),
    clocks=clocks,
    scope=dict(helpers_reset=False,continuous_native_primitive=False,
               tiny_clock_replaces_CT_asymptotic=False,same_task_forcing=False,
               full_Cost_Info_selected=False,GR_closed=False))
print(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2))
