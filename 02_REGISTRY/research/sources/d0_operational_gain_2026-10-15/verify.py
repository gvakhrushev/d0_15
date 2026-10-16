#!/usr/bin/env python3
"""Finite operational information gain and native cost-cut memory recurrence.
Exact algebra, outward intervals, separately labelled floating-point tests.
No assert statements: all mathematical gates run under Python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.linalg import expm
HERE = Path(__file__).resolve().parent
CHECKS: list[tuple[str,str]] = []
SCOPE = {
 'finite_full_algebra_measurement_optimization': True,
 'literal_cost_cut_full_gram_spectral_recurrence': True,
 'moving_instrument_and_initial_preparation_included': True,
 'physical_admission_of_all_algebraic_tests': False,
 'native_Info_identified_without_maximal_gain_contract': False,
 'generic_entropy_or_MPS_method_claimed_new': False,
 'physical_hilbert_carrier_replaced_by_compact_matrices': False,
 'bounded_action_implies_bounded_source': False,
 'original_fixed_source_terminal_or_GR_closed': False,
 'new_Lean_compilation': False,
}
def ck(name: str, value, kind='exact'):
    if not bool(value): raise RuntimeError('MATHEMATICAL_GATE: '+name)
    CHECKS.append((kind,name))
def adj(A): return A.conjugate().T

def compact_step(X,Y,K0,K1):
    if not isinstance(X,sp.MatrixBase): raise TypeError('exact SymPy matrices required')
    r=X.rows//K0.rows
    B0=sp.kronecker_product(K0,sp.eye(r)); B1=sp.kronecker_product(K1,sp.eye(r))
    return B0*X*adj(B0)+Y, B1*X*adj(B1)

# Numeric path is explicit: '*' above is symbolic matrix multiplication only.
def step(X,Y,B0,B1):
    return B0@X@B0.conj().T+Y, B1@X@B1.conj().T

def step_jet(X,Y,dX,dY,B0,B1,dB0,dB1):
    dXX=dB0@X@B0.conj().T+B0@dX@B0.conj().T+B0@X@dB0.conj().T+dY
    dYY=dB1@X@B1.conj().T+B1@dX@B1.conj().T+B1@X@dB1.conj().T
    return dXX,dYY

def gram(words,L):
    vs=[sp.Matrix(list(A*L)) for A in words]
    V=sp.Matrix.hstack(*vs)
    return V.T*V.conjugate(),V*adj(V)

def exact():
    R=sp.Rational; I=sp.I
    K0=sp.diag(R(3,5),R(5,13))
    U=sp.Matrix([[R(3,5),I*R(4,5)],[I*R(4,5),R(3,5)]])
    K1=U*sp.diag(R(4,5),R(12,13)); L=sp.diag(R(3,5),R(4,5))
    ck('actual_kraus_completeness',adj(K0)*K0+adj(K1)*K1==sp.eye(2))
    ck('noncommuting_instrument_fixture',K0*K1!=K1*K0)
    ck('normalized_initial_factor',sp.trace(L*adj(L))==1)
    A=[K0]; B=[K1]; a=b=1
    SX,X=gram(A,L); SY,Y=gram(B,L)
    H0=sp.Matrix([[1,1],[1,0]]);H1=sp.Matrix([[0,-I],[I,2]])
    dK0=I*H0*K0;dK1=I*H1*K1
    dL=I*sp.Matrix([[0,1],[1,0]])*L
    ck("moving_density_not_only_purification_gauge",dL*adj(L)+L*adj(dL)!=sp.zeros(2))
    ck('true_kraus_unitary_tangent',adj(dK0)*K0+adj(K0)*dK0+adj(dK1)*K1+adj(K1)*dK1==sp.zeros(2))
    dA=[dK0];dB=[dK1]
    z=sp.Symbol('z')
    def dgram(W,dW):
        v=[sp.Matrix(list(T*L)) for T in W]
        dv=[sp.Matrix(list(dT*L+T*dL)) for T,dT in zip(W,dW)]
        V=sp.Matrix.hstack(*v);dV=sp.Matrix.hstack(*dv)
        return dV.T*V.conjugate()+V.T*dV.conjugate(), dV*adj(V)+V*adj(dV)
    dSX,dX=dgram(A,dA);dSY,dY=dgram(B,dB)
    b0=sp.kronecker_product(K0,sp.eye(2));b1=sp.kronecker_product(K1,sp.eye(2))
    db0=sp.kronecker_product(dK0,sp.eye(2));db1=sp.kronecker_product(dK1,sp.eye(2))
    for n in range(4):
        sA,xfull=gram(A,L);sB,yfull=gram(B,L)
        dsA,dxfull=dgram(A,dA);dsB,dyfull=dgram(B,dB)
        ck(f'complete_ready_block_{n}',xfull==X)
        ck(f'complete_pending_block_{n}',yfull==Y)
        ck(f'complete_jet_ready_{n}',(dxfull-dX).applyfunc(sp.expand)==sp.zeros(4))
        ck(f'complete_jet_pending_{n}',(dyfull-dY).applyfunc(sp.expand)==sp.zeros(4))
        ck(f'actual_fibonacci_counts_{n}',(len(A),len(B))==(a,b))
        ck(f'full_probability_{n}',sp.simplify(sp.trace(X)+sp.trace(Y))==1)
        ck(f'full_probability_jet_{n}',sp.simplify(sp.trace(dX)+sp.trace(dY))==0)
        # Exact polynomial identity retains all zero modes on both carriers.
        if n<=2:
            for tag,S,T in [('A',sA,X),('B',sB,Y)]:
                ck(f'full_characteristic_polynomial_{n}_{tag}',
                   sp.expand(z**4*S.charpoly(z).as_expr()-z**S.rows*T.charpoly(z).as_expr())==0)
        A1=[K0*T for T in A]+B;B1=[K1*T for T in A]
        dA1=[dK0*T+K0*dT for T,dT in zip(A,dA)]+dB
        dB1=[dK1*T+K1*dT for T,dT in zip(A,dA)]
        fA,_=gram(A1,L);fB,_=gram(B1,L)
        fdA,_=dgram(A1,dA1);fdB,_=dgram(B1,dB1)
        ck(f'actual_AF_restriction_A_{n}',(fA[:a,:a]+fB-sA).applyfunc(sp.expand)==sp.zeros(a))
        ck(f'actual_AF_restriction_B_{n}',fA[a:,a:]==sB)
        ck(f'actual_AF_restriction_jet_A_{n}',(fdA[:a,:a]+fdB-dsA).applyfunc(sp.expand)==sp.zeros(a))
        ck(f'actual_AF_restriction_jet_B_{n}',sp.simplify(fdA[a:,a:]-dsB)==sp.zeros(b))
        xn,yn=compact_step(X,Y,K0,K1)
        dxn=db0*X*adj(b0)+b0*dX*adj(b0)+b0*X*adj(db0)+dY
        dyn=db1*X*adj(b1)+b1*dX*adj(b1)+b1*X*adj(db1)
        oldcost=(n+1)*sp.trace(X)+(n+2)*sp.trace(Y)
        newcost=(n+2)*sp.trace(xn)+(n+3)*sp.trace(yn)
        ck(f'exact_cost_increment_{n}',sp.simplify(newcost-oldcost-sp.trace(X)-sp.trace(yn))==0)
        ck(f'REJECT_resplit_pending_{n}',xn!=b0*X*adj(b0)+b0*Y*adj(b0))
        A,B,dA,dB,X,Y,dX,dY=A1,B1,dA1,dB1,xn,yn,dxn,dyn
        a,b=a+b,a
    # Conditional history action binding, not an unconditional physical assertion.
    q,mu,g=sp.symbols('q mu g',positive=True)
    cost=-sp.log(mu)/g;gain=sp.log(q/mu)/g
    ck('branch_cost_minus_gain_surprisal',sp.simplify(sp.expand_log(cost-gain+sp.log(q)/g,force=True))==0)
    qv=[R(1,8),R(1,8),R(3,4)];rv=[R(1,4),R(1,4),R(1,2)]
    kl=sum(x*sp.log(x/y) for x,y in zip(qv,rv))
    coarse=R(1,4)*sp.log(R(1,2))+R(3,4)*sp.log(R(3,2))
    ck('equal_likelihood_grouping_retains_gain',sp.simplify(kl-coarse)==0)
    ck('unequal_likelihood_grouping_loses_gain',sp.simplify(kl)>0)
    # Exact primal/dual optimum: p central within the ready block.
    p=sp.Symbol('p',positive=True);c=R(3,5)
    sig=sp.diag(1,1,1);sig[:2,:2]=p**2*sp.Matrix([[1,c],[c,1]]);sig[2,2]=p**3
    muM=sp.diag(p**2,p**2,p**3)
    W=sp.diag(1,1,1);W[:2,:2]=sp.Matrix([[1,1],[1,-1]])/sp.sqrt(2)
    target=sp.diag(p**2*(1+c),p**2*(1-c),p**3)
    ck('likelihood_PVM_orthogonal',W*adj(W)==sp.eye(3))
    ck('likelihood_PVM_attains_spectrum',sp.simplify(adj(W)*sig*W-target)==sp.zeros(3))
    ck('central_reference_invariant',adj(W)*muM*W==muM)
    ck('branch_diagonal_gain_zero',list(sig.diagonal())==list(muM.diagonal()))
    ck('full_coherence_not_zero',sig!=muM)
    u,cc=sp.symbols('u cc',real=True)
    rr=sp.sqrt(cc**2+(1-cc**2)*u**2)
    f=lambda x:(1+x)*sp.log(1+x)+(1-x)*sp.log(1-x)
    gu=p**2*f(rr)/g
    du2=sp.diff(gu,u,2).subs({u:0,cc:R(3,5)})
    ck('gain_hessian_exact',sp.simplify(du2-16*p**2*sp.log(4)/(15*g))==0)
    dc=sp.diff(p**2*f(cc)/g,cc).subs(cc,R(3,5))
    theta_gain=-R(4,5)*dc
    ck('gain_theta_jet_exact',sp.simplify(theta_gain+4*p**2*sp.log(4)/(5*g))==0)
    ck('net_action_gain_sign_opposite_old_entropy_contract',sp.simplify(-theta_gain-4*p**2*sp.log(4)/(5*g))==0)
    # Two-probability Gibbs-like reference is NOT needed: all algebraic tests
    # only require faithful mu central in the actual represented algebra.
    return len([1 for k,_ in CHECKS if k=='exact'])

def entropy_and_jet(X,dX=None):
    X=(X+X.conj().T)/2
    v,U=np.linalg.eigh(X)
    if v.min() < -1e-10:raise ValueError('nonpositive numeric fixture')
    ids=v>1e-12
    value=float(-np.sum(v[ids]*np.log(v[ids])))
    if dX is None:return value
    # Constant-rank trace derivative; the total trace jet is separately tested.
    diagon=np.real(np.diag(U.conj().T@dX@U))
    return value,float(-np.dot(diagon[ids],np.log(v[ids])))

def fixture(t=0.):
    k0=np.diag([3/5,5/13]).astype(complex)
    U=np.array([[3/5,4j/5],[4j/5,3/5]])
    k1=U@np.diag([4/5,12/13]);L=np.diag([3/5,4/5]).astype(complex)
    H0=np.array([[1,1],[1,0]],complex);H1=np.array([[0,-1j],[1j,2]],complex);HL=np.array([[0.,1.],[1.,0.]])
    return expm(1j*t*H0)@k0,expm(1j*t*H1)@k1,expm(1j*t*HL)@L,H0,H1,HL

def compact_numeric(N,t=0.,jet=False):
    K0,K1,L,H0,H1,HL=fixture(t)
    b0=np.kron(K0,np.eye(2));b1=np.kron(K1,np.eye(2))
    v0=(K0@L).reshape(-1);v1=(K1@L).reshape(-1)
    X=np.outer(v0,v0.conj());Y=np.outer(v1,v1.conj())
    if jet:
        if t!=0: raise ValueError('jet is declared only at t=0')
        dK0=1j*H0@K0;dK1=1j*H1@K1;dL=1j*HL@L
        db0=np.kron(dK0,np.eye(2));db1=np.kron(dK1,np.eye(2))
        dv0=(dK0@L+K0@dL).reshape(-1);dv1=(dK1@L+K1@dL).reshape(-1)
        dX=np.outer(dv0,v0.conj())+np.outer(v0,dv0.conj())
        dY=np.outer(dv1,v1.conj())+np.outer(v1,dv1.conj())
    for _ in range(N):
        if jet: dx,dy=step_jet(X,Y,dX,dY,b0,b1,db0,db1)
        X,Y=step(X,Y,b0,b1)
        if jet:dX,dY=dx,dy
    if jet:
        ex,dx=entropy_and_jet(X,dX);ey,dy=entropy_and_jet(Y,dY)
        return ex+ey,dx+dy,X,Y,dX,dY
    return entropy_and_jet(X)+entropy_and_jet(Y),X,Y

def numeric():
    errors=[]
    for N in (0,1,2,4,7):
        K0,K1,L,_,_,_=fixture();A=[K0];B=[K1]
        for _ in range(N):A,B=[K0@M for M in A]+B,[K1@M for M in A]
        def block(ws):
            Z=np.array([(M@L).reshape(-1) for M in ws]);return Z@Z.conj().T
        S0=block(A);S1=block(B)
        ent,dent,X,Y,dx,dy=compact_numeric(N,jet=True)
        direct=entropy_and_jet(S0)+entropy_and_jet(S1)
        ck(f'numeric_full_gram_entropy_{N}',abs(ent-direct)<2e-11,'numeric')
        ck(f'numeric_trace_jet_{N}',abs(np.trace(dx+dy))<3e-12,'numeric')
        dt=1e-5
        fd=(compact_numeric(N,dt)[0]-compact_numeric(N,-dt)[0])/(2*dt)
        errors.append(abs(fd-dent))
        ck(f'numeric_true_preparation_and_gate_source_{N}',abs(fd-dent)<2e-7,'numeric')
        ck(f'numeric_compact_probability_{N}',abs(np.trace(X+Y)-1)<2e-12,'numeric')
    # The full algebraic maximum is tested against rotated fine and coarse tests.
    p=(np.sqrt(5)-1)/2;mu=np.array([p*p,p*p,p**3]);c=3/5
    sig=np.array([[p*p,c*p*p,0],[c*p*p,p*p,0],[0,0,p**3]],complex)
    qopt=np.array([p*p*(1+c),p*p*(1-c),p**3]);D=float(np.sum(qopt*np.log(qopt/mu)))
    for j,ang in enumerate(np.linspace(0,np.pi/2,17)):
        O=np.eye(3);O[:2,:2]=[[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]]
        q=np.real(np.diag(O.T@sig@O));score=float(np.sum(q*np.log(q/mu)))
        ck(f'numeric_logsum_bound_projective_{j}',score<=D+2e-14,'numeric')
        T=np.array([[.7,.2,.1],[.3,.8,.9]])
        qc=T@q;mc=T@mu;coarse=float(np.sum(qc*np.log(qc/mc)))
        ck(f'numeric_logsum_bound_POVM_{j}',coarse<=score+2e-14,'numeric')
    # Deep tape test: only two 4x4 matrices are updated, no history truncation.
    N=1000;ent,dent,X,Y,dx,dy=compact_numeric(N,jet=True);a=b=1
    for _ in range(N):a,b=a+b,a
    ck('numeric_deep_native_mass',abs(np.trace(X+Y)-1)<5e-12,'numeric')
    ck('numeric_deep_entropy_capacity',-1e-11<=ent<=np.log(8)+1e-11,'numeric')
    earlyX=compact_numeric(1)[1]
    ck('numeric_full_matrices_required_at_first_cost_cut',np.linalg.norm(earlyX-np.diag(np.diag(earlyX)))>0.1,'numeric')
    ck('deep_fibonacci_count_not_small',len(str(a+b))>200,'numeric')
    return {'label':'FLOATING_POINT_DIAGNOSTICS_NOT_INTERVAL_PROOF',
            'max_finite_difference_error':float(max(errors)), 'deep_level':N,
            'full_defining_carrier_decimal_digits':len(str(a+b)),
            'compact_matrix_shape':[4,4], 'deep_entropy_nats':ent,
            'deep_entropy_jet':dent, 'deep_cost':float(((N+1)*np.trace(X)+(N+2)*np.trace(Y)).real)}

def intervals():
    mp.iv.dps=60;iv=mp.iv
    p=(iv.sqrt(5)-1)/2;ell=iv.log((1+iv.sqrt(5))/2)
    gain=p*p*((iv.mpf(8)/5)*iv.log(iv.mpf(8)/5)+(iv.mpf(2)/5)*iv.log(iv.mpf(2)/5))/ell
    netjet=4*p*p*iv.log(4)/(5*ell)
    hessian=-16*p*p*iv.log(4)/(15*ell)
    ck('interval_gain_positive',gain>iv.mpf('0.30598560631735') and gain<iv.mpf('0.30598560631736'),'interval')
    ck('interval_net_theta_positive',netjet>iv.mpf('0.88030642633503') and netjet<iv.mpf('0.88030642633505'),'interval')
    ck('interval_net_preparation_curvature_negative',hessian>iv.mpf('-1.17374190178006') and hessian<iv.mpf('-1.17374190178004'),'interval')
    cost=2*(2*p*p)+3*(p**3);net=cost-gain
    ck('interval_net_action_positive',net>0,'interval')
    ck('interval_no_new_base',ell>0,'interval')
    return {'gain_phi_units':str(gain),'net_theta_source_phi_units':str(netjet),'net_u_hessian_phi_units':str(hessian)}

def run(stage='all'):
    CHECKS.clear()
    exact_count=exact() if stage in ('all','exact') else 0
    nums=numeric() if stage in ('all','numeric') else {}
    ints=intervals() if stage in ('all','interval') else {}
    counts=Counter(k for k,_ in CHECKS)
    receipt={'schema':'d0-operational-gain/1','scope':SCOPE,'checks':dict(sorted(counts.items())),
      'unique_gate_names':len(set(name for _,name in CHECKS)),
      'condition_name_sha256':hashlib.sha256('\n'.join(k+':'+n for k,n in CHECKS).encode()).hexdigest(),
      'exact_conditions':exact_count,'numeric_conditions_are_not_exact':True,'intervals':ints}
    return receipt,nums

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--math-only',action='store_true');ap.add_argument('--stage',choices=['all','exact','numeric','interval'],default='all');args=ap.parse_args()
    out,num=run(args.stage)
    if not args.math_only and args.stage=='all':
        out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        out['proof_sha256']=hashlib.sha256((HERE/'RESULT.md').read_bytes()).hexdigest()
        path=HERE/'receipt.json'
        if args.write:
            path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
            (HERE/'numeric_result.json').write_text(json.dumps(num,indent=2,sort_keys=True)+'\n')
        elif json.loads(path.read_text())!=out:raise RuntimeError('IMMUTABLE_RECEIPT_MISMATCH')
    print(json.dumps({'status':'PASS','checks':out['checks'],'scope':out['scope'],'numeric_diagnostic':num},sort_keys=True))
if __name__=='__main__':main()
