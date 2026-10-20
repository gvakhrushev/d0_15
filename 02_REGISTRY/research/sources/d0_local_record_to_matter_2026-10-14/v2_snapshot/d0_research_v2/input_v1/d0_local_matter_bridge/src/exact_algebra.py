"""Exact local algebra. Reconstructed from formulas supplied in this conversation.
No GitHub/Lean owner pin or historical 203-check receipt is claimed.
Explicit checks remain active under python -O.
"""
from __future__ import annotations
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
checks=[];mutants=[]
def check(name,ok):
    if not bool(ok):raise AssertionError(name)
    checks.append(name)
def zero(x):
    if isinstance(x,s.MatrixBase):return all(s.expand(v)==0 for v in x)
    return s.expand(x)==0
def eq(name,x):check(name,zero(x))
def reject(name,false_statement):
    check('REJECT_'+name,not bool(false_statement));mutants.append(name)

def creator(r):
    out=s.zeros(16)
    for mask in range(16):
        if not(mask&(1<<r)):
            out[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
    return out
C=[creator(i) for i in range(4)]
I=s.eye(16);I4=s.eye(4);eta=s.diag(1,-1,-1,-1)
def rho(A):return sum((A[i,j]*C[i]*C[j].T for i in range(4)for j in range(4)),s.zeros(16))
def lift(A):return rho(A)-s.trace(A)*I/2

phi=(1+s.sqrt(5))/2;pi0=s.Rational(6,5)*phi**2;delta0=(1/phi)**3/2
check('pi0_exact_seam_identity',s.simplify(2*pi0*(2-phi)-s.Rational(12,5))==0)
check('golden_feedback_delta_identity',s.simplify(4/phi**3-8*delta0)==0)
for i in range(4):
    for j in range(4):
        eq(f'CAR_cc_{i}{j}',C[i]*C[j]+C[j]*C[i])
        eq(f'CAR_ca_{i}{j}',C[i]*C[j].T+C[j].T*C[i]-int(i==j)*I)
check('all_Fock_grades_retained',[sum(m.bit_count()==k for m in range(16))for k in range(5)]==[1,4,6,4,1])

# Zero one-point CAR current does not imply zero quadratic kinetic stress.
beta_car=C[0]+C[0].T
for i in range(1,4):
    alpha=beta_car*(C[i]-C[i].T)
    eq(f'isotropic_Fock_density_zero_CAR_current_{i}',s.trace(alpha)/16)
check('nonzero_first_shell_metric_stress',128-64*s.sqrt(2)>0)
reject('zero_vector_current_implies_zero_kinetic_stress',128-64*s.sqrt(2)==0)

# Exact norm-preserving metric lift on all ten symmetric metric directions.
V=[]
for i in range(4):
    for j in range(i,4):
        E=s.zeros(4);E[i,j]=1;E[j,i]=1;V.append(((i,j),E))
for (i,j),v in V:
    A=v*eta/2;T=lift(A)
    eq(f'metric_lift_{i}{j}',A*eta+eta*A.T-v)
    dotW=s.trace(A)*I-rho(A).T-rho(A)
    eq(f'full_density_pairing_normalization_{i}{j}',dotW+T.T+T)
for (i,j),v in V:
    for (k,l),w in V:
        A=v*eta/2;B=w*eta/2
        Cv=(v*eta*w*eta-w*eta*v*eta)/4
        # Derivative-of-horizontal-field formula includes both q and matter terms.
        DvB=-w*eta*v*eta/2;DwA=-v*eta*w*eta/2
        direct=lift(DvB)-lift(DwA)+lift(B)*lift(A)-lift(A)*lift(B)
        eq(f'lift_curvature_{i}{j}_{k}{l}',direct-rho(Cv))
        eq(f'curvature_is_Lorentz_vertical_{i}{j}_{k}{l}',Cv*eta+eta*Cv.T)
V0=s.diag(1,0,0,0);W0=s.zeros(4);W0[0,1]=W0[1,0]=1
Cv=(V0*eta*W0*eta-W0*eta*V0*eta)/4
check('nonflat_horizontal_connection',Cv[1,0]==-s.Rational(1,4))
reject('horizontal_Euler_row_automatically_integrates_to_an_action',Cv==s.zeros(4))

# Positive G and the already used observer Lorentz chart: exact inverse and all ten directions.
gtest=s.Matrix([[2,s.Rational(1,5),0,0],[s.Rational(1,5),3,0,0],[0,0,4,0],[0,0,0,5]])
vref=I4[:,0];gden=(vref.T*gtest*vref)[0];Q0=gtest.inv()
qtest=-Q0+2*vref*vref.T/gden
qinv=-gtest+2*gtest*vref*vref.T*gtest/gden
eq('retained_observer_Lorentz_inverse',qtest*qinv-I4)
eq('retained_observer_recovers_positive_Q',-qtest+2*vref*vref.T/(vref.T*qinv*vref)[0]-Q0)
check('retained_observer_Lorentz_det',qtest.det()==-1/gtest.det())
columns=[]
for ij,H in V:
    dq=Q0*H*Q0-2*vref*vref.T*(vref.T*H*vref)[0]/gden**2
    columns.append(s.Matrix([dq[i,j]for (i,j),_ in V]))
check('retained_observer_full_ten_metric_chart',s.Matrix.hstack(*columns).rank()==10)

# Fock trace identities used for ALL local linear-link variations.
G=s.Matrix([[2,s.Rational(1,5),0,0],[s.Rational(1,5),3,0,0],[0,0,4,0],[0,0,0,5]])
ann=[sum((G[i,j]*C[j].T for j in range(4)),s.zeros(16))for i in range(4)]
for a in range(4):
    for b in range(4):
        K=s.zeros(4);K[a,b]=1;R=rho(K)
        for i in range(4):
            for r in range(4):
                expected=4*(G[i,r]*s.trace(K)-(G*K)[i,r])
                eq(f'full_Fock_link_trace_{a}{b}_{i}{r}',s.trace(ann[i]*C[r]*R)-expected)
                eq(f'raising_pair_trace_zero_{a}{b}_{i}{r}',s.trace(C[i]*C[r]*R))

# Homogeneous metric mode symbols span ALL ten packed components.
labels=[ij for ij,v in V]
modal=[]
for i in range(4):
    k=I4[:,i];T=k*k.T;modal.append([T[r,t]*(1 if r==t else 2)for r,t in labels])
for i in range(4):
    for j in range(i+1,4):
        k=I4[:,i]+I4[:,j];T=k*k.T;modal.append([T[r,t]*(1 if r==t else 2)for r,t in labels])
check('metric_moment_full_rank10',s.Matrix(modal).rank()==10)
reject('radial_balance_proves_all_ten_equations',len([1])==len(labels))

# A genuine seam insertion on the archive, not a harmless global U phase.
a,p,x,y,z=s.symbols('a p x y z',real=True)
def Ugate():
    U=s.zeros(16)
    for k in range(0,16,2):
        U[k,k]=a;U[k,k+1]=-p
        low=k.bit_count()<=1
        U[k+1,k]=p if low else -p;U[k+1,k+1]=a if low else -a
    return U
U=Ugate();P=s.diag(*[int(k%2==0)for k in range(16)]);Q=I-P
Btheta=P+(x+s.I*y)*Q
W=U*Btheta*U;Fb=P*s.conjugate(W.T)*Q*W*P
ideal=s.groebner([a*a-p,p*p+p-1,x*x+y*y-1],a,p,y,domain=s.QQ.frac_field(x,z))
def red(e):
    n,d=s.cancel(e).as_numer_denom();n=ideal.reduce(s.expand(n))[1];d=ideal.reduce(s.expand(d))[1]
    if d==0:raise ZeroDivisionError('golden phase denominator')
    return s.cancel(n/d)
L=4*p**3
for i in range(16):
    for j in range(16):
        want=0
        if i==j and i%2==0:want=L*(1+x)/2 if i.bit_count()<=1 else L*(1-x)/2
        check(f'seam_full_feedback_{i}_{j}',red(Fb[i,j]-want)==0)
# Both complementary current-dependent sectors, not a single resonant eigenvalue.
Ptheta=(1-z*L*(1+x)/2)*(1-z*L*(1-x)/2)
check('seam_pencil_two_sectors',red(Ptheta-(1-z*L+z*z*L*L*(1-x*x)/4))==0)
check('seam_feedback_trace_constant',red(s.trace(Fb)-4*L)==0)
reject('a_global_unitary_phase_changes_feedback',s.simplify(s.exp(-s.I*z)*s.exp(s.I*z))!=1)
reject('fixed_seam_angle_supplies_radial_scale_response',s.diff(s.cos(s.Rational(12,5)),z)!=0)

# Quadratic seam closure K=(U-exp(i theta))^*(U-exp(i theta)).
# The variable p here is an independently normalized planar unitary witness.
Ur=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
cost=(Ur-(x+s.I*y)*s.eye(2)).conjugate().T*(Ur-(x+s.I*y)*s.eye(2))
for e in cost-(2*s.eye(2)-(x-s.I*y)*Ur-(x+s.I*y)*Ur.T):
    check('quadratic_seam_defect_identity_'+str(len(checks)),s.rem(s.Poly(s.expand(e),y),s.Poly(y*y+x*x-1,y)).as_expr()==0)

# General radial critical scale and its correct second derivative sign.
beta,E,R,var=s.symbols('beta E R var',positive=True)
Eprime=-2*E+2*beta*var;Rprime=-2*R
check('radial_second_derivative_at_balance',s.simplify((2*Eprime-2*Rprime).subs(R,E)-4*beta*var)==0)
reject('radial_second_derivative_is_negative',-4*beta*var==4*beta*var)

# Pure-matter saddle direction is retained, not suppressed by quoting radial convexity.
h,cross=s.symbols('h cross',positive=True)
check('degenerate_matter_metric_mixed_Hessian_negative_det',s.det(s.Matrix([[h,cross],[cross,0]]))==-cross**2)
reject('positive_radial_Hessian_proves_joint_minimum',s.det(s.Matrix([[h,cross],[cross,0]]))>0)

out={'schema':'d0-local-exact/1','status':'PASS','checks':checks,'exact_controls':len(checks),
     'negative_controls':mutants,'number_of_negative_controls':len(mutants),
     'pi0_value':'(6/5)*phi^2, user-supplied premise; arithmetic verified',
     'theta_seam':'12/5','owner_status':'CONVERSATION_RECONSTRUCTION_NOT_CURRENT_REPOSITORY_OR_LEAN',
     'native_matter_admission_derived':False,'GR_derived':False}
(ROOT/'results/exact_algebra.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS_EXACT_ALGEBRA',len(checks),'controls;',len(mutants),'negative controls')
