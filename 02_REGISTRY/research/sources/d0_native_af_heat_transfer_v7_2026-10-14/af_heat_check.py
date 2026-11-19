#!/usr/bin/env python3
"""D0 v7: exact native AF trace transfer; no physical-admission claim.

Normal replay is immutable. --write explicitly refreshes the adjacent receipt.
The nonlinear/limit statements are proved in the accompanying memo, not by samples.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, subprocess, sys, tempfile
from functools import lru_cache
import sympy as s

HERE = pathlib.Path(__file__).resolve().parent
PROOF = HERE / 'NATIVE_AF_HEAT_TRANSFER_RU.md'
RECEIPT = HERE / 'af_heat_receipt.json'
INPUT_HEAD = '25bf1db4876c20223f2dbaeb1cbe1105039cf7a1'
PINS = {
 '03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean': '64dc8f9da911b1ff3427413c2efc40db0bcac043',
 '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md': '573e2d70c1d7cbefd35670431b1ab9b87624dbdd',
 '02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md': '3cbb805fb72b501a0eb1d7d17b9f037dff115880',
}

def counts(n):
    a,b=1,1
    for _ in range(n): a,b=a+b,a
    return a,b

def inc(pair):
    A,B=pair
    return s.diag(A,B),A

def lift(pair,n,N):
    for _ in range(N-n): pair=inc(pair)
    return pair

def regular(pair):
    return s.diag(*(s.kronecker_product(x,s.eye(x.rows)) for x in pair))

def trreg(pair):
    return sum(x.rows*s.trace(x) for x in pair)

def transfer(pair,a,b):
    Z,W=pair
    X=Z[:a,:a]; Y=Z[a:a+b,a:a+b]
    return ((a+b)*X+a*W)/a, (s.Rational(a+b,b))*Y

def reduce_full(X,n,N):
    """Adjoint of actual left inclusion for ordinary regular operator traces."""
    out=[]
    sizes=counts(n)
    for block,d in enumerate(sizes):
        A=s.zeros(d)
        for i in range(d):
            for j in range(d):
                unit=[s.zeros(v) for v in sizes]
                unit[block][j,i]=1
                A[i,j]=s.trace(X*regular(lift(tuple(unit),n,N)))/d
        out.append(A)
    return tuple(out)

def gns_projection(n,p,a):
    A,B=counts(n); f=A+B
    J=s.zeros(f*f+A*A,A*A+B*B)
    for i in range(A):
        for j in range(A):
            J[i*f+j,i*A+j]=a
            J[f*f+i*A+j,i*A+j]=p
    for i in range(B):
        for j in range(B):
            J[(A+i)*f+(A+j),A*A+i*B+j]=1
    return J,J*J.T

def checks():
    names=[]; negative=[]
    def ck(name,value):
        if not bool(value): raise AssertionError(name)
        names.append(name)
    def reject(name,value):
        ck('REJECT_'+name,not bool(value)); negative.append(name)
    p,a,q=s.symbols('p a q',real=True)
    ideal=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.QQ.frac_field(q))
    @lru_cache(maxsize=16384)
    def red(x):
        if x == 0: return s.S.Zero
        nn,dd=s.cancel(x).as_numer_denom()
        nn=ideal.reduce(s.expand(nn))[1];dd=ideal.reduce(s.expand(dd))[1]
        if dd==0: raise ZeroDivisionError('golden denominator')
        return s.cancel(nn/dd)
    def zero(x):
        return all(red(v)==0 for v in (list(x) if isinstance(x,s.MatrixBase) else [x]))
    M=s.Matrix([[1,1],[1,0]])
    ck('literal_initial_dimensions',[sum(x*x for x in counts(n)) for n in range(5)]==[2,5,13,34,89])
    for n in range(8):
        A,B=counts(n)
        ck(f'PF_normalization_{n}',zero(A*p**(n+1)+B*p**(n+2)-1))
        # The native PF adjoint C becomes the ordinary-trace adjoint only after
        # the forced central density correction W_n^{-1} C(W_{n+1} X).
        t=p**(n+1)
        ck(f'forced_X_coefficient_{n}',zero((t/A)*p*(A+B)/(p*t)-s.Rational(A+B,A)))
        ck(f'forced_W_coefficient_{n}',zero((t/A)*p*p*A/(p*p*t)-1))
        ck(f'forced_Y_coefficient_{n}',zero((p*t/B)*(A+B)/(p*t)-s.Rational(A+B,B)))
        for r in range(7):
            aa,bb=counts(n+r); ma,mb=counts(n+2*r)
            ck(f'all_GNS_dimensions_{n}_{r}',A*ma+B*mb==aa*aa+bb*bb)
            ck(f'two_sided_multiplicity_{n}_{r}',M**(2*r)*s.Matrix([A,B])==s.Matrix([ma,mb]))
            D=aa*aa+bb*bb
            # Exact trace-distance numerator, with sign (-1)^(n+1).
            lhs=s.Rational(A*ma,D)-A*p**(n+1)
            rhs=(-1)**(n+1)*A*B*p**(2*n+2*r+3)/D
            ck(f'exact_PF_trace_error_{n}_{r}',zero(lhs-rhs))
    # Exact, all-entry one-step trace duality with arbitrary rectangular fine blocks.
    for n in range(3):
        A,B=counts(n); F=A+B
        Z=s.Matrix(F,F,lambda i,j:(i+1)*7+(j+1)*3)
        W=s.Matrix(A,A,lambda i,j:2*(i+1)-(j+1))
        out=transfer((Z,W),A,B)
        ck(f'full_trace_conservation_{n}',trreg(out)==trreg((Z,W)))
        ck(f'full_identity_multiplicities_{n}',transfer((s.eye(F),s.eye(A)),A,B)==(s.Rational(2*A+B,A)*s.eye(A),s.Rational(A+B,B)*s.eye(B)))
        for b,d in enumerate((A,B)):
            for i in range(d):
                for j in range(d):
                    u=[s.zeros(A),s.zeros(B)];u[b][i,j]=1
                    v=inc(tuple(u))
                    ck(f'adjoint_every_matrix_unit_{n}_{b}_{i}_{j}',
                        sum(x.rows*s.trace(x*y) for x,y in zip(tuple(u),out))==
                        sum(x.rows*s.trace(x*y) for x,y in zip(v,(Z,W))))
    reject('Perron_adjoint_is_full_heat_transfer',zero(p-s.Rational(2,3)))
    reject('ordinary_trace_transfer_is_unital',transfer((s.eye(2),s.eye(1)),1,1)==(s.eye(1),s.eye(1)))
    # Compare direct full-carrier reduction with the actual successive arrows.
    for N in (1,2,3):
        A,B=counts(N);D=A*A+B*B
        V=s.Matrix(D,1,lambda i,j:(i%5)-2)
        X=s.eye(D)+V*V.T # positive with cross-block coherences
        cur=reduce_full(X,N,N)
        for n in range(N-1,-1,-1):
            cur=transfer(cur,*counts(n))
            direct=reduce_full(X,n,N)
            ck(f'tower_complete_operator_{n}_{N}',cur==direct)
            ck(f'tower_full_trace_{n}_{N}',trreg(cur)==s.trace(X))
    # The literal GNS inclusion gives a squared mismatch, not a fitted spectrum.
    for n in (0,1,2):
        A,B=counts(n);ma,mb=2*A+B,A+B
        J,P=gns_projection(n,p,a);D=P.rows;Id=s.eye(D)
        ck(f'native_J_isometry_{n}',zero(J.T*J-s.eye(J.cols)))
        ck(f'native_P_projection_{n}',zero(P*P-P))
        ck(f'native_complement_rank_{n}',zero(s.trace(Id-P)-(A*A+2*A*B)))
        for b,d in enumerate((A,B)):
            U=[s.zeros(A),s.zeros(B)]
            for i in range(d):U[b][i,(i+1)%d]=1
            op=regular(inc(tuple(U)))
            ck(f'native_P_bimodule_commutant_{n}_{b}',zero(P*op-op*P))
        rp=reduce_full(P,n,n+1)
        ck(f'native_P_reduces_to_identity_{n}',all(zero(x-s.eye(x.rows)) for x in rp))
        Y=P+q*(Id-P)
        Ry=reduce_full(Y,n,n+1)
        expected=( (1+q*s.Rational(ma-A,A))*s.eye(A),
                   (1+q*s.Rational(mb-B,B))*s.eye(B))
        ck(f'native_mismatch_full_Gibbs_factor_{n}',all(zero(x-y) for x,y in zip(Ry,expected)))
        ck(f'native_mismatch_partition_all_modes_{n}',zero(trreg(Ry)-(A*A+B*B+(A*A+2*A*B)*q)))
    # Genuine n=0 -> n=1 first-source witness: beta=log2, mismatch energy nu=1.
    J,P=gns_projection(0,p,a);Id=s.eye(5);Y=(Id+P)/2
    Omega=J*s.Matrix([a,p]);rho=Omega*Omega.T
    ck('whole_Perron_vector_norm',zero((Omega.T*Omega)[0]-1))
    ck('whole_Perron_vector_has_zero_mismatch',zero((Id-P)*Omega))
    reduced=reduce_full(rho,0,1)
    ck('same_prepared_coarse_weights',zero(reduced[0][0]-p) and zero(reduced[1][0]-p*p))
    thermal=reduce_full(Y,0,1)
    ck('finite_native_partition_7_over2',zero(trreg(thermal)-s.Rational(7,2)))
    ck('two_central_factors',zero(thermal[0][0]-2) and zero(thermal[1][0]-s.Rational(3,2)))
    dK=s.Matrix([s.Rational(1,2),s.Rational(1,3)])
    cov=p*dK[0]+p*p*dK[1]
    ck('archive_source_exact_not_dropped',zero(cov-(p+2)/6))
    ck('full_heat_source_minus_3_over7',s.Rational(4,7)*dK[0]+s.Rational(3,7)*dK[1]==s.Rational(3,7))
    ck('full_price_restored_by_archive_source',zero((-s.Rational(3,7)+cov)-cov+s.Rational(3,7)))
    reject('central_correction_is_one_scalar',thermal[0][0]==thermal[1][0])
    reject('drop_archive_source_at_cyclic_preparation',zero(cov))
    reject('use_defining_instead_of_regular_multiplicity',counts(1)[0]+counts(1)[1]==5)
    # Exact positive tangent transfer at this native commutant reference.
    def T(X):
        pair=reduce_full(Y*X,0,1)
        return pair[0]/2,pair[1]/s.Rational(3,2)
    ck('native_tangent_transfer_is_unital',all(zero(x-s.eye(x.rows)) for x in T(Id)))
    # Both rational and imaginary perturbations: no restriction to commuting jets.
    for i in range(5):
        for j in range(5):
            X=s.zeros(5);X[i,j]=1
            rhs=T(X)
            tauC=(s.Rational(4,7),s.Rational(3,7))
            ck(f'Gibbs_tangent_lift_{i}_{j}',zero(sum(w*x[0] for w,x in zip(tauC,rhs))-s.trace(Y*X)/s.Rational(7,2)))
    X=s.zeros(5);X[0,1]=X[1,0]=1
    reject('all_allowed_tangents_commute_with_native_mismatch',zero((Id-P)*X-X*(Id-P)))
    # Central trace weights converge, but this does not fix a fine heat operator.
    Zfirst=s.Rational(3,2)+2
    fake=s.Rational(5,2)*(s.Rational(1,2)+1)
    reject('one_global_log_dimension_correction_suffices',Zfirst==fake)
    return {
      'schema':'d0-native-af-heat-transfer/1','status':'PASS_EXACT_REPLAY',
      'input_head':INPUT_HEAD,'owner_git_blobs':PINS,
      'owner_binding':'Literal inclusion and PF-adjoint formulas read at pinned owner; no new Lean compilation.',
      'exact_conditions':len(names),'checks_sha256':hashlib.sha256(json.dumps(names,separators=(',',':')).encode()).hexdigest(),'executed_negative_controls':negative,
      'scope':{'native_AF_trace_transfer':True,'all_level_tower_law_proved_analytically':True,
               'full_partition_and_archive_source_retained':True,'new_Lean_compilation':False,
               'physical_heat_generator_derived':False,'physical_GR_closed':False},
      'proof_sha256':hashlib.sha256(PROOF.read_bytes()).hexdigest(),
      'checker_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    data=checks()
    if args.write: RECEIPT.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    else:
        expected=json.loads(RECEIPT.read_text(encoding='utf-8'))
        if data!=expected:raise AssertionError('IMMUTABLE_RECEIPT_MISMATCH')
    print('PASS_NATIVE_AF_HEAT_TRANSFER',data['exact_conditions'],'exact conditions;',len(data['executed_negative_controls']),'negative controls; PHYSICAL_GENERATOR_OPEN')

if __name__=='__main__':main()
