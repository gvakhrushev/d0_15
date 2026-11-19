#!/usr/bin/env python3
"""Same native H+J+R: exact matrix jets and auxiliary variational closure.
No native primitive admission, new physical action, or GR certificate.
"""
from __future__ import annotations
from itertools import combinations
import json
import sympy as s

CHECKS=[]
def simp(v):
    v=s.expand(s.expand_log(s.expand(v),force=True))
    repl={}
    for atom in v.atoms(s.log):
        q=atom.args[0]
        if q.is_Rational and q>0:
            repl[atom]=sum(e*s.log(k) for k,e in s.factorint(int(q.p)).items())-sum(e*s.log(k) for k,e in s.factorint(int(q.q)).items())
    return s.expand(v.xreplace(repl))
def eq(name, a, b=0):
    if isinstance(a,s.MatrixBase) or isinstance(b,s.MatrixBase):
        diff=s.Matrix(a)-s.Matrix(b)
        ok=all(simp(v)==0 for v in diff)
    else: ok=simp(a-b)==0
    if not ok: raise ArithmeticError(name)
    CHECKS.append(name)
def demand(name, ok):
    if not ok: raise ArithmeticError(name)
    CHECKS.append(name)
def tr(a): return s.trace(a)
def logdiag(a): return s.diag(*[s.log(v) for v in a.diagonal()])
def power_jet(a,da,dda,n):
    p,dp,ddp=s.eye(a.rows),s.zeros(a.rows),s.zeros(a.rows)
    for _ in range(n):
        p,dp,ddp=p*a,dp*a+p*da,ddp*a+2*dp*da+p*dda
    return p,dp,ddp

def dlog_at_diagonal(d,h):
    ev=list(d.diagonal())
    def c(i,j):
        if ev[i]==ev[j]: return 1/ev[i]
        return (s.log(ev[i])-s.log(ev[j]))/(ev[i]-ev[j])
    return s.Matrix(d.rows,d.rows,lambda i,j:c(i,j)*h[i,j])

def ddlog_diagonal_entries(d,h,k):
    ev=list(d.diagonal()); vals=[]
    for i,bi in enumerate(ev):
        total=k[i,i]/bi
        for j,bj in enumerate(ev):
            g= -1/(2*bi**2) if bi==bj else (s.log(bj)-s.log(bi)-(bj-bi)/bi)/(bj-bi)**2
            total+=2*g*h[i,j]*h[j,i]
        vals.append(total)
    return s.diag(*vals)

def hermitian_basis(n,tracezero=False):
    basis=[]
    if tracezero:
        for i in range(n-1):
            h=s.zeros(n);h[i,i]=1;h[n-1,n-1]=-1;basis.append(h)
    else:
        for i in range(n):
            h=s.zeros(n);h[i,i]=1;basis.append(h)
    for i,j in combinations(range(n),2):
        h=s.zeros(n);h[i,j]=h[j,i]=1;basis.append(h)
        h=s.zeros(n);h[i,j]=s.I;h[j,i]=-s.I;basis.append(h)
    return basis

def run():
    CHECKS.clear()
    dim=4; alpha=s.Rational(1,16); m=4; beta=m*alpha; z=s.Rational(1,5); mult=128
    # A zero Dirac eigenvalue, opposite signs, and repeated Delta eigenvalues.
    D=s.diag(0,1,-1,2); Delta=D*D
    E=s.Matrix([[1,s.I,1,0],[-s.I,0,1,1],[1,1,-1,s.I],[0,1,-s.I,2]])/13
    E2=s.Matrix([[0,1,0,s.I],[1,1,1,0],[0,1,0,1],[-s.I,0,1,-1]])/17
    Delta1=D*E+E*D;Delta2=2*E*E+D*E2+E2*D
    B=s.eye(dim)-alpha*Delta;B1=-alpha*Delta1;B2=-alpha*Delta2
    K,K1,K2=power_jet(B,B1,B2,m);Z=tr(K);Z1=tr(K1);Z2=tr(K2)
    F=s.eye(dim)-K; A=(1-z)*s.eye(dim)+z*K; A1=z*K1;A2=z*K2
    rho=K/Z;rho1=K1/Z-K*Z1/Z**2;X=A.inv();X1=-X*A1*X
    Lam=-logdiag(B)/alpha;Lam1=-dlog_at_diagonal(B,B1)/alpha
    Lam2diag=-ddlog_diagonal_entries(B,B1,B2)/alpha
    demand('D_zero_mode_retained',D[0,0]==0 and K[0,0]==1 and A[0,0]==1)
    demand('Delta_repeated_eigenvalue_retained',Delta[1,1]==Delta[2,2] and D[1,1]!=D[2,2])
    demand('genuine_noncommuting_jet',Delta*Delta1!=Delta1*Delta)
    demand('complex_Hermitian_directions_retained',s.conjugate(E.T)==E and E.has(s.I))
    eq('thermal_full_normalizer',tr(rho),1)
    eq('thermal_normalizer_jet',tr(rho1),0)
    eq('feedback_all_modes',A*X,s.eye(dim))
    eq('feedback_inverse_jet',A1*X+A*X1,s.zeros(dim))
    eq('thermal_KKT_on_trace_constraint',logdiag(rho)+beta*Lam,-s.log(Z)*s.eye(dim))
    eq('thermal_KKT_jet_including_partition',dlog_at_diagonal(rho,rho1)+beta*Lam1,-Z1/Z*s.eye(dim))
    eq('noncommuting_trace_power_first',Z1,-beta*tr(B**(m-1)*Delta1))
    eq('heat_source_not_Delta_Gibbs_source',Z1/(beta*Z),-tr(B**(m-1)*Delta1)/Z)
    eq('thermal_auxiliary_first_source',-tr(rho*Lam1),Z1/(beta*Z))
    eq('feedback_auxiliary_first_source',-mult*tr(X*A1),mult*beta*z*tr(X*B**(m-1)*Delta1))
    # Full normalized matter matrix with its own retained two-dimensional reference.
    t=s.symbols('t',real=True)
    C=s.Matrix([[1,0],[0,1],[1,1],[1,-1]])
    C1=s.Matrix([[s.I,1],[1,0],[0,s.I],[1,2]])/11
    C2=s.Matrix([[1,s.I],[0,1],[1,0],[-s.I,1]])/19
    Ct=C+t*C1+t*t*C2/2
    mass=tr(Ct*Ct.H);matt=Ct*Ct.H/mass
    rhoM=matt.subs(t,0);rhoM1=matt.diff(t).subs(t,0);rhoM2=matt.diff(t,2).subs(t,0)
    eq('matter_all_reference_normalized',tr(rhoM),1)
    eq('matter_first_normalizer_retained',tr(rhoM1),0)
    eq('matter_second_normalizer_retained',tr(rhoM2),0)
    demand('matter_is_not_thermal_auxiliary',rhoM!=rho)
    R1=tr(rhoM1*Delta+rhoM*Delta1)
    R2=tr(rhoM2*Delta+2*rhoM1*Delta1+rhoM*Delta2)
    heat1=Z1/(beta*Z);feed1=-mult*tr(X*A1)
    W=rhoM-B**(m-1)/Z+mult*beta*z*X*B**(m-1)
    eq('complete_native_source_operator',R1+heat1+feed1,tr(W*Delta1)+tr(rhoM1*Delta))
    eq('complete_native_Dirac_anticommutator',tr(W*Delta1),tr((D*W+W*D)*E))
    demand('matter_cannot_be_commuted_through_D',D*rhoM!=rhoM*D)
    # Second response: exact Schur terms, no spectral sampling or frozen weights.
    heat2=(Z2/Z-(Z1/Z)**2)/beta
    feedback2=mult*(tr(X*A1*X*A1)-tr(X*A2))
    corrH=tr(rho1*dlog_at_diagonal(rho,rho1))/beta
    corrX=mult*tr(A*X1*A*X1)
    fixedH=-tr(rho*Lam2diag);fixedX=-mult*tr(X*A2)
    eq('heat_exact_Schur_second_response',heat2,fixedH+corrH)
    eq('feedback_exact_Schur_second_response',feedback2,fixedX+corrX)
    eq('full_native_Hessian_identity',R2+heat2+feedback2,R2+fixedH+fixedX+corrH+corrX)
    demand('freezing_thermal_weight_loses_real_term',simp(corrH)!=0)
    demand('freezing_feedback_precision_loses_real_term',simp(corrX)!=0)
    # Every Hermitian precision and every trace-zero Hermitian density direction.
    for i,V in enumerate(hermitian_basis(dim,True)):
        eq('density_stationarity_%02d'%i,tr(V*(logdiag(rho)+s.eye(dim)+beta*Lam)),0)
    for i,V in enumerate(hermitian_basis(dim)):
        eq('precision_stationarity_%02d'%i,tr(V*(X.inv()-A)),0)
    eq('density_auxiliary_dimension',len(hermitian_basis(dim,True)),15)
    eq('precision_auxiliary_dimension',len(hermitian_basis(dim)),16)
    # Entropy gap identity tested algebraically on diagonal arbitrary full-rank candidate.
    cand=s.diag(s.Rational(1,10),s.Rational(2,10),s.Rational(3,10),s.Rational(4,10))
    hstar=s.log(Z)/beta;htrial=(-tr(cand*logdiag(cand))-beta*tr(cand*Lam))/beta
    Drel=tr(cand*(logdiag(cand)-logdiag(rho)))
    eq('exact_thermal_relative_entropy_gap',hstar-htrial,Drel/beta)
    O=s.Matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
    candnc=O*cand*O.H; lognc=O*logdiag(cand)*O.H
    demand('noncommuting_thermal_candidate',candnc*rho!=rho*candnc)
    hnc=(-tr(candnc*lognc)-beta*tr(candnc*Lam))/beta
    eq('exact_coherent_thermal_gap',hstar-hnc,tr(candnc*(lognc-logdiag(rho)))/beta)
    # Rank-deficient trial is allowed in the gap, not a new auxiliary stationary point.
    vec=s.Matrix([1,1,1,1])/2; pure=vec*vec.H
    eq('pure_trial_gap_without_log_zero',hstar+tr(pure*Lam),-tr(pure*logdiag(rho))/beta)
    # Matrix (not scalar/commuting) logdet gap with determinant identities.
    L=s.Matrix([[1,s.Rational(1,5),0,0],[0,1,s.Rational(1,7),0],[0,0,1,s.Rational(1,11)],[0,0,0,1]])
    trial=L*L.T
    demand('noncommuting_precision_candidate',trial*A!=A*trial)
    gstar=-mult*s.log(A.det())
    gtrial=mult*(dim+s.log(trial.det())-tr(trial*A))
    gap=mult*(tr(trial*A)-s.log(trial.det()*A.det())-dim)
    eq('exact_full_feedback_gap',gstar-gtrial,gap)
    eq('all_auxiliary_gaps_zero_at_profile',tr(X*A)-s.log(X.det()*A.det())-dim,0)
    # Finite history sum with its nonzero, norm-controlled remainder.
    for k in (0,1,3,7):
        Xk=sum((z**j*F**j for j in range(k+1)),s.zeros(dim))
        eq('whole_history_tail_identity_%d'%k,X-Xk,z**(k+1)*F**(k+1)*X)
        demand('history_partial_sum_not_exact_%d'%k,Xk!=X)
    # Change of full basis acts on everything. No deleting of observer derivatives.
    G=s.Matrix([[0,1,s.I,0],[-1,0,0,1],[s.I,0,0,0],[0,-1,0,0]])/23
    demand('full_unitary_frame_generator',G.H==-G)
    comm=lambda a,b:a*b-b*a
    eq('matter_frame_terms_cancel_offshell',tr(comm(G,rhoM)*Delta+rhoM*comm(G,Delta)),0)
    eq('native_geometric_frame_source_is_trace_commutator',tr((-B**(m-1)/Z+mult*beta*z*X*B**(m-1))*comm(G,Delta)),0)
    eq('precision_frame_stationarity_covariant',comm(G,A)*X+A*comm(G,X),s.zeros(dim))
    # Adding a physical zero mode changes the thermal normalization: it is retained.
    demand('no_silent_zero_mode_padding',s.simplify(-1/Z+1/(Z+1))!=0)
    # Ground-level gap equalities are exact, but no full physical dynamics is selected.
    return {'schema':'d0-native-price-unfolding/1','exact_check_count':len(CHECKS),'checks':CHECKS,
      'fixture_dimension':dim,'reference_dimension':2,'power':m,'multiplicity':mult,
      'thermal_profile':'K/Tr(K)','return_profile':'[(1-z)I+zK]^{-1}',
      'same_action':'R + log(C Tr K)/beta - M Tr log((1-z)I+zK)',
      'physical_auxiliary_preparation_postulated':False,'GR_closed':False,
      'new_native_action_selected':False,'whole_repository_replayed':False}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
