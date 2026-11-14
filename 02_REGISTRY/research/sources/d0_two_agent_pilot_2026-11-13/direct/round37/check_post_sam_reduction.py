#!/usr/bin/env python3
"""Exact target, all skew rows in finite fixtures, source identity and bounds."""
from pathlib import Path
import hashlib,json
import sympy as S
import post_sam_reduction as r
P=Path(__file__).resolve().parent


def zero(A):
    return all(S.simplify(x)==0 for x in A)


def main():
    M=S.diag(S.Rational(3,4),S.Rational(4,5),S.Rational(9,10))
    psi=S.Matrix([S.Rational(1,3),S.Rational(2,3),S.Rational(2,3)])
    chi=S.Matrix([S.Rational(2,3),S.Rational(1,3),S.Rational(2,3)])
    U,norm,xi,d=r.rotate_to_reference(M,psi,chi)
    assert zero(U.T*U-S.eye(3)) and S.simplify(U.det()-1)==0
    assert zero(U*M*psi-norm*chi)
    axes=0
    for a in range(3):
        for b in range(a+1,3):
            X=S.zeros(3);X[a,b]=1;X[b,a]=-1
            assert S.simplify((chi.T*X*U*M*psi)[0])==0
            assert S.simplify((chi.T*X*X*U*M*psi)[0]+norm*(X*chi).dot(X*chi))==0
            axes+=1
    # Identity limit xi=chi is regular; no division by an angle/sin occurs.
    U0,_,_,d0=r.rotate_to_reference(S.Rational(3,4)*S.eye(3),psi,psi)
    assert zero(U0-S.eye(3)) and d0==1
    # Exact source relation for arbitrary real M, arbitrary skew X.
    # M^T M replaces M^2 outside the actual symmetric A30 specialization.
    m1,m2,m3,x1,x2,x3,c,g,s=S.symbols('m1 m2 m3 x1 x2 x3 c g s',nonzero=True,real=True)
    Mt=S.diag(m1,m2,m3);v=S.Matrix([x1,x2,x3]);I=S.eye(3)
    for a in range(3):
        for b in range(a+1,3):
            X=S.zeros(3);X[a,b]=1;X[b,a]=-1
            dc=(v.T*(Mt*X-X*Mt)*v)[0]
            dq=(v.T*(Mt*Mt*X-X*Mt*Mt)*v)[0]
            B=(Mt-c*I)**2
            variance=(v.T*(B*X-X*B)*v)[0]
            assert S.expand(dq-2*c*dc-variance)==0
            assert S.simplify(-dq/(4*c*g*s)+dc/(2*g*s)+variance/(4*c*g*s))==0
    # A source-changing variance term must not be silently dropped.
    X=S.Matrix([[0,-1,0],[1,0,0],[0,0,0]])
    cfix=S.Rational(7,8)
    B=(M-cfix*S.eye(3))**2
    assert S.simplify((psi.T*(B*X-X*B)*psi)[0])!=0
    mean=(psi.T*M*psi)[0];q=(psi.T*M*M*psi)[0]
    assert S.simplify(q-mean**2)>0
    plan=r.build()
    for source,digest in plan['source_sha256'].items():
        assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==digest
    assert not plan['new_paid_native_target_word_emitted']
    assert not plan['new_full_heat_or_H_plus_J_stationarity_proved']
    pins=[Path(__file__),P/'post_sam_reduction.py',P/'POST_SAM_REDUCTION_PLAN.json']
    out={'status':'PASS_EXACT_POST_SAM_TARGET_SOURCE_IDENTITY_AND_CONDITIONAL_A30_BOUNDS',
         'all_skew_fixture_axes':axes,'identity_target_chart_checked':True,
         'second_moment_not_square_of_mean_control':True,
         'nonzero_variance_source_control':True,
         'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
         'physical_C_closed':False,'GR_closed':False}
    (P/'POST_SAM_REDUCTION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
