#!/usr/bin/env python3
"""Exact controlled-kernel identities and joint-source negative controls."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
import sympy as S
import joint_source_reduction as p
P=Path(__file__).resolve().parent;R=S.Rational


def controlled(columns):
    d=len(columns);work=columns[0].rows;v=S.zeros(d*work,d)
    for j,u in enumerate(columns):v[j*work:(j+1)*work,j]=u
    assert v.T*v==S.eye(d)
    return v


def skew_basis(d):
    for a in range(d):
        for b in range(a+1,d):
            y=S.zeros(d);y[b,a]=1;y[a,b]=-1;yield a,b,y


def exact_identities():
    us=[S.Matrix([R(12,13),0,R(5,13)]),S.Matrix([R(4,5),R(3,5),0]),
        S.Matrix([0,R(12,13),R(5,13)])]
    V=controlled(us);Swork=S.diag(1,1,-1);d=3
    J=controlled([us[0]]*d);Delta=V-J
    def phi(y):return V.T*S.kronecker_product(y,Swork)*V
    D=phi(S.eye(d));A=Delta.T*S.kronecker_product(S.eye(d),Swork)*Delta
    assert D.is_diagonal() and A.is_diagonal()
    ideal_planes=0
    for a,b,y in skew_basis(d):
        E=phi(y)-(D*y+y*D)/2
        direct=Delta.T*S.kronecker_product(y,Swork)*Delta-(A*y+y*A)/2
        assert E==direct and E.T==-E
        ideal_planes+=1
    # Actual-like nonsymmetric cross-kernel: distinct normalized backward
    # columns. This fixture validates algebra, not the production error size.
    vs=[us[0],S.Matrix([R(12,13),R(5,13),0]),us[2]]
    W=controlled(vs)
    L=S.Matrix(d,d,lambda c,b:(vs[c].T*Swork*us[b])[0])
    M=S.diag(*[L[j,j] for j in range(d)])
    assert L!=L.T and all(M[j,j]>R(2,3) for j in range(d))
    chi=S.Matrix([R(2,3),R(2,3),R(1,3)])
    assert (chi.T*chi)[0]==1
    cref=R(9,10);gs=R(1,2000)
    checked=0
    for a,b,y in skew_basis(d):
        Ph=W.T*S.kronecker_product(y,Swork)*V
        assert Ph==L.multiply_elementwise(y)
        anti=(Ph-Ph.T)/2;symmetric=(Ph+Ph.T)/2
        E=anti-(M*y+y*M)/2
        assert E.T==-E and symmetric.T==symmetric
        dp=-(chi.T*M*M*y*chi)[0]/(2*cref*gs)
        dq=-(chi.T*M*Ph*chi)[0]/(2*cref*gs)
        residual=-(chi.T*M*(E+symmetric)*chi)[0]/(2*cref*gs)
        assert S.simplify(dq-dp/2-residual)==0
        # Subtracting any scalar from M in the skew-E term is exact.
        mu=R(7,10)
        assert (chi.T*M*E*chi)[0]==(chi.T*(M-mu*S.eye(d))*E*chi)[0]
        checked+=1
    # The full nonlinear relative-inner operator is the Hadamard kernel.
    rel=S.Matrix([[R(3,5),-R(4,5),0],[R(4,5),R(3,5),0],[0,0,1]])
    K=L.multiply_elementwise(rel)
    assert K==W.T*S.kronecker_product(rel,Swork)*V
    x=S.Matrix([R(1,3),R(2,3),R(2,3)]);y=chi
    c=(x.T*K*y)[0];AA=S.diag(*x)*L*S.diag(*y)
    assert c==S.trace(AA.T*rel)
    for a,b,Z in skew_basis(d):
        assert (x.T*L.multiply_elementwise(rel*Z)*y)[0]==S.trace((rel.T*AA).T*Z)
        assert (x.T*L.multiply_elementwise(Z*rel)*y)[0]==S.trace((AA*rel.T).T*Z)
        assert ((Z*x).T*K*y)[0]==((Z*x).T*(K*y-c*x))[0]
        assert (x.T*K*Z*y)[0]==((K.T*x-c*y).T*Z*y)[0]
    # A supported basis vector solves all four feedback rows at R=I even
    # for the nonsymmetric kernel; it destroys the old mean first jet.
    for b in range(d):
        e=S.eye(d)[:,b];c=M[b,b]
        assert M*e==c*e and M.T*e==c*e
        mean=S.diag(0,1,2)
        for a,k,Z in skew_basis(d):
            assert (e.T*L.multiply_elementwise(Z)*e)[0]==0
            comm=mean*Z-Z*mean
            assert (e.T*comm*e)[0]==0 and (comm*e)[b]==0
    # Outer stationarity in a degenerate M eigenspace is not sufficient:
    # the actual antisymmetric L part has an independent inner equation.
    L2=S.Matrix([[R(3,4),R(1,4)],[R(1,8),R(3,4)]])
    y2=S.Matrix([R(3,5),R(4,5)]);X2=S.Matrix([[0,-1],[1,0]])
    M2=R(3,4)*S.eye(2)
    assert M2*y2==R(3,4)*y2
    assert (y2.T*L2.multiply_elementwise(X2)*y2)[0]!=0
    return {'ideal_operator_identity_planes':ideal_planes,'actual_nonsymmetric_residual_planes':checked,
      'relative_inner_Hadamard_map_and_left_right_derivatives':True,
      'basis_feedback_stationary_but_mean_first_jet_zero':True,
      'degenerate_outer_equations_not_sufficient_for_inner_negative_control':True}


def main():
    result=exact_identities();plan=p.build()
    assert plan==json.loads((P/'JOINT_SOURCE_REDUCTION_PLAN.json').read_text())
    for f,h in plan['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
    result.update({'status':'PASS_EXACT_JOINT_KERNEL_REDUCTION_AND_SOURCE_BOUNDS',
      'production_kernel_or_full_heat_computed':False,'all_skew_physical_admission_proved':False,
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in
        (Path(__file__),P/'joint_source_reduction.py',P/'JOINT_SOURCE_REDUCTION_PLAN.json')}})
    (P/'JOINT_SOURCE_REDUCTION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':main()
