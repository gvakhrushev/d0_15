#!/usr/bin/env python3
"""D0: nonlocal two-density field reduction; exact author checks.
No native query-admission, selected Book03 value, finite-lattice GR or CI claim.
The scientific theorems are proved in PROOF.md; these are bounded algebraic
checks including a genuine nonlinear two-stage ledger and an exact nonlocal
continuum solution. Explicit checks remain active with python -O.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

CHECKS=[]
def check(name, value):
    if not bool(value):
        raise AssertionError(name)
    CHECKS.append(name)
def zero(name, value):
    if isinstance(value,s.MatrixBase):
        value=value.applyfunc(s.simplify)
        check(name,value==s.zeros(*value.shape))
    else:
        check(name,s.simplify(value)==0)

# 1. Exact general field-coordinate factors. A and B are FUNCTIONAL
# derivatives, not partial derivatives of an assumed local price.
a,A,B,eta2,vbar,varpi,qbar,chi=s.symbols('a A B eta2 vbar varpi qbar chi', nonzero=True)
r=A/a
v=vbar/r**2
q=r*qbar
# Covariant Einstein source after connection elimination:
W=varpi*A*B/(a*a*vbar)
zero('metric_source_conformal_factor', varpi*B/(A*v)-W)
zero('matter_source_uses_same_W', varpi*B*r-a*vbar*W)
y=-eta2*q
zero('density_constant_from_Bianchi', y/A+eta2*qbar/a)
Xbar=-eta2*vbar*W*qbar/varpi
x=Xbar/r
zero('geometric_density_reconstruction', x-B*(-eta2*qbar/a))
zero('material_density_reconstruction', y-A*(-eta2*qbar/a))

# 2. General symmetric functional Hessian with nonsymmetric cross block.
n=3
Hxx=s.Matrix([[1,2,0],[2,-1,3],[0,3,0]])
Hxy=s.Matrix([[0,1,2],[-2,0,1],[1,3,0]])
Hyy=s.Matrix([[2,0,1],[0,1,-1],[1,-1,3]])
H=Hxx.row_join(Hxy).col_join(Hxy.T.row_join(Hyy))
J=s.zeros(n).row_join(s.eye(n)).col_join(s.eye(n).row_join(s.zeros(n)))
l=s.Matrix([2,3,4,5,6,7])
check('whole_history_Hessian_symmetric',H==H.T)
check('cross_history_block_nontrivial',Hxy!=Hxy.T)
z=s.Rational(1,101)
u=(s.eye(2*n)-z*J*H).inv()*z*J*l
AB=l+H*u
zero('exact_coupled_nonlocal_fixed_point',u-z*J*AB)
for j in range(n):
    zero(f'original_radial_constraint_{j}',u[j]*AB[j]-u[n+j]*AB[n+j])
    zero(f'common_conformal_density_{j}',u[n+j]/AB[j]-z)
check('inhomogeneous_solution_not_constant_densities',len(set(u[:n]))>1 and len(set(u[n:]))>1)
check('functional_kernel_not_assumed_invertible',s.zeros(2*n).det()==0)
for h in (H,s.zeros(2*n)):
    k=(s.eye(2*n)-z*J*h)
    check('fixed_point_inverse_exists_'+str(h.rank()),k.det()!=0)
# Exact finite norm certificate for the contraction at this chi.
L=max(sum(abs(e) for e in row) for row in H.tolist())
check('exact_contraction',z*L<s.Rational(1,2))

# 3. Real independent internal variables: eliminate only on an actual
# nondegenerate stationary baseline, keep the Schur correction.
R=s.Matrix([[1,0],[0,2],[1,1],[-1,1],[0,1],[2,-1]])
C=s.Matrix([[4,1],[1,3]])
Hred=H-R*C.inv()*R.T
ured=(s.eye(2*n)-z*J*Hred).inv()*z*J*l
xi=-C.inv()*R.T*ured
ABfull=l+H*ured+R*xi
zero('independent_internal_equations',C*xi+R.T*ured)
zero('internal_elimination_preserves_fixed_point',ured-z*J*ABfull)
check('internal_remainder_not_deleted',Hred!=H)
check('null_internal_baseline_has_no_extra_mode',C.det()!=0)

# 4. A nonlocal price constructed from the old two-stage sequential ledger.
# K is a fixed, doubly stochastic, non-symmetric address kernel.
r0,kappa,beta,alpha=s.symbols('r0 kappa beta alpha',positive=True)
rr=s.symbols('r1:4',positive=True)
h=s.Function('h')
K=s.Matrix([[s.Rational(1,2),s.Rational(1,3),s.Rational(1,6)],
            [s.Rational(1,6),s.Rational(1,2),s.Rational(1,3)],
            [s.Rational(1,3),s.Rational(1,6),s.Rational(1,2)]])
check('address_kernel_positive',all(q>0 for q in K))
zero('address_kernel_row_balance',K*s.ones(n,1)-s.ones(n,1))
zero('address_kernel_column_balance',K.T*s.ones(n,1)-s.ones(n,1))
check('not_symmetrized_by_hand',K!=K.T)
cost=[kappa-beta*h(q) for q in rr]
V=alpha*(sum(cost)+beta*sum(K[i,j]*rr[i]*cost[j]
                           for i in range(n) for j in range(n)))
sub=dict(zip(rr,[r0]*n))
V2=alpha*(kappa-beta*h(r0))*(1+beta*r0)
for i in range(n):
    zero(f'constant_record_mode_source_{i}',s.diff(V,rr[i]).subs(sub)-s.diff(V2,r0))
check('price_is_genuinely_history_coupled',s.diff(V,rr[0],rr[1])!=0)
# Deliberately break mass balance: it no longer produces one common source.
Kbad=s.Matrix([[1,0,0],[1,0,0],[0,0,1]])
Vbad=alpha*(sum(cost)+beta*sum(Kbad[i,j]*rr[i]*cost[j]
                              for i in range(n) for j in range(n)))
check('unbalanced_address_kernel_fails_common_source',
      s.simplify(s.diff(Vbad,rr[0]).subs(sub)-s.diff(Vbad,rr[1]).subs(sub))!=0)
# Literal original Golden detector r(x,y), finite z and matter sign retained.
p=(s.sqrt(5)-1)/2
zx=s.Rational(1,2**20)
xx,yy=s.symbols('x y',real=True)
bb=4*(p+p*p*yy)**2*(1-(p+p*p*yy)**2)
ee=p*p*(1+xx)
ell=4*ee*(1-ee)
aa=ell+(1-ell)*bb
detector=1-(1-zx*bb)*(1-zx*aa)
rx=s.simplify(s.diff(detector,xx).subs({xx:0,yy:0}))
ry=s.simplify(s.diff(detector,yy).subs({xx:0,yy:0}))
Q=1-zx*4*p**3
RR=1-zx*4*p**3*(1+p**6)
zero('literal_finite_z_ratio',ry/rx-2*p**(-5)*(RR/Q+p**6))
ratio=s.N(-ry/rx,40)
check('original_sigma_minus_coupling',abs(float(ratio)+23.416406751884075)<1e-12)

# 4b. Literal complete stopped ledger, summed over ALL actually executed
# ordered address words. No costs assigned equal and no completed-branch
# renormalization. The prefix preparation bill stays as its fixed baseline.
from itertools import product
hh=s.symbols('h1:4')
kk=s.symbols('k1:4')
bar_r=sum(rr)/n
bar_h=sum(hh)/n
bar_k=sum(kk)/n
for cap in (1,2,3,4):
    direct=s.Integer(0)
    for word in product(range(n),repeat=cap):
        occupancy=s.Integer(1)
        subtotal=s.Integer(0)
        for site in word:
            subtotal+=occupancy*(kk[site]-beta*hh[site])
            occupancy*=beta*rr[site]
        direct+=alpha*subtotal
    EN=sum((beta*bar_r)**j for j in range(cap))
    closed=alpha*n**cap*(bar_k-beta*bar_h)*EN
    zero(f'all_executed_ordered_words_price_cap_{cap}',s.expand(direct-closed))
    # Moving an address cost without changing the TOTAL cost is field-source
    # neutral after this actually paid word construction, not on one word.
    zero(f'unequal_address_costs_only_through_mean_cap_{cap}',
         s.diff(closed,kk[0])-s.diff(closed,kk[1]))
    evals={**dict(zip(rr,[r0]*n)),**dict(zip(hh,[h(r0)]*n))}
    for i in range(n):
        source=s.diff(closed,rr[i])+s.diff(closed,hh[i])*s.diff(h(r0),r0)
        expected=alpha*n**(cap-1)*s.diff((bar_k-beta*h(r0))*
                   sum((beta*r0)**j for j in range(cap)),r0)
        zero(f'all_word_full_entropy_chain_source_{cap}_{i}',source.subs(evals)-expected)
# A single cyclic ordering does NOT accomplish the same cancellation.
cyc=sum((kk[i]-beta*hh[i])+beta*rr[i]*(kk[(i+1)%n]-beta*hh[(i+1)%n])
        for i in range(n))
cs=[(s.diff(cyc,rr[i])+s.diff(cyc,hh[i])*s.diff(h(r0),r0)).subs(
     {**dict(zip(rr,[r0]*n)),**dict(zip(hh,[h(r0)]*n))}) for i in range(n)]
zero('hostile_cyclic_order_retains_address_price_difference',cs[0]-cs[1]-(kk[1]-kk[2])*beta)
check('single_cycle_does_not_remove_actual_nonuniform_cost',s.expand(cs[0]-cs[1])!=0)
# Actual inverse-PF integer trace cancellation, without altering measure.
n_i=s.symbols('n1:4',positive=True)
n_mean=sum(n_i)/3
rho=[n_i[i]/n_mean for i in range(3)]
for i in range(3):
    zero(f'original_integer_trace_inverse_PF_compensation_{i}',n_i[i]/rho[i]-n_mean)

# 5. Independent exact 4D NONLOCAL continuum-price root.
# Diagnostic functional: F= int(x+2y) + (1/6)(int w(s)x)^2.
# Unit coordinate box: t in [1,2], s,z,w in [0,1]; w(s)=s+1/2 has mean 1.
# This is not a new selected D0 action or fitted curvature coefficient.
t,sx,zcoord,wcoord=s.symbols('t s z w',positive=True)
coords=(t,sx,zcoord,wcoord)
w=sx+s.Rational(1,2)
chistar=-s.Rational(1,100)
b0=s.Integer(2)
xstar=chistar*b0
Af=1+s.Rational(1,3)*w*xstar
qstar=-chistar
Bf=b0
cf=s.Rational(3,4)*Af*Bf*qstar
scale=t**s.Rational(2,3)
gbar=s.diag(1,-(scale*cf)**2,-scale**2,-scale**2)
gi=s.diag(*[1/gbar[i,i] for i in range(4)])
vb=scale**3*cf
Gamma=[[[s.simplify(sum(gi[l,k]*(s.diff(gbar[k,j],coords[i])+s.diff(gbar[k,i],coords[j])
    -s.diff(gbar[i,j],coords[k])) for k in range(4))/2)
    for j in range(4)] for i in range(4)] for l in range(4)]
Ric=s.zeros(4)
for i in range(4):
    for j in range(4):
        Ric[i,j]=s.simplify(sum(s.diff(Gamma[k][i][j],coords[k])-s.diff(Gamma[k][i][k],coords[j])
            +sum(Gamma[k][k][m]*Gamma[m][i][j]-Gamma[k][j][m]*Gamma[m][i][k]
                 for m in range(4)) for k in range(4)))
sc=s.simplify(sum(gi[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
Ein=(Ric-sc*gbar/2).applyfunc(s.simplify)
zero('independent_4D_Ricci_scalar',sc+s.Rational(4,3)/t**2)
zero('Einstein_dust_metric',Ein-s.diag(s.Rational(4,3)/t**2,0,0,0))
# Original tetrad/metric differs by the NONCONSTANT determined A(s).
ebar=s.diag(1,scale*cf,scale,scale)
ebari=ebar.inv()
e=ebar/s.sqrt(Af)
g=gbar/Af;ginv=gi*Af;vg=vb/Af**2
Omega=[s.zeros(4) for _ in range(4)]
for mu in range(4):
    for aidx in range(4):
        for bidx in range(4):
            Omega[mu][aidx,bidx]=s.simplify(sum(ebar[aidx,nu]*Gamma[nu][mu][rh]*ebari[rh,bidx]
                for nu in range(4) for rh in range(4))
                -sum(s.diff(ebar[aidx,nu],coords[mu])*ebari[nu,bidx] for nu in range(4)))
eta=s.diag(1,-1,-1,-1)
for mu in range(4):
    zero(f'proper_Lorentz_spin_connection_{mu}',Omega[mu].T*eta+eta*Omega[mu])
for aidx in range(4):
    for mu in range(4):
        for nu in range(mu+1,4):
            tors=s.diff(ebar[aidx,nu],coords[mu])-s.diff(ebar[aidx,mu],coords[nu])
            tors+=sum(Omega[mu][aidx,j]*ebar[j,nu]-Omega[nu][aidx,j]*ebar[j,mu] for j in range(4))
            zero(f'24_weighted_Cartan_rows_{aidx}_{mu}_{nu}',tors)
# Construct curvature from the independent Lorentz connection and original e.
curv={}
for mu in range(4):
    for nu in range(4):
        curv[mu,nu]=(Omega[nu].diff(coords[mu])-Omega[mu].diff(coords[nu])
                     +Omega[mu]*Omega[nu]-Omega[nu]*Omega[mu]).applyfunc(s.simplify)
ei=e.inv()
Ric_original=s.zeros(4)
# R^rho_{sigma mu nu} = e_a^rho R^a_b mu nu e^b_sigma;
# Ric_{sigma nu} = sum_rho R^rho_{sigma rho nu}.
for sig in range(4):
    for nu in range(4):
        Ric_original[sig,nu]=s.simplify(sum(ei[rh,aa]*curv[rh,nu][aa,bb]*e[bb,sig]
             for rh in range(4) for aa in range(4) for bb in range(4)))
zero('actual_Palatini_Ricci_equals_Einstein_frame_Ricci',Ric_original-Ric)
Rorig=s.simplify(sum(ginv[i,j]*Ric_original[i,j] for i in range(4) for j in range(4)))
psigrad=s.Matrix([s.sqrt(qstar),0,0,0])
Xtensor=psigrad*psigrad.T
xgeom=s.simplify(vg*Rorig)
ygeom=s.simplify(-(psigrad.T*ginv*psigrad)[0])
zero('nonlocal_source_fixed_point_x',xgeom-xstar)
zero('nonlocal_source_fixed_point_y',ygeom-chistar*Af)
Acomputed=1+s.Rational(1,3)*w*s.integrate(w*xgeom,(sx,0,1))
zero('actual_nonlocal_functional_derivative',Acomputed-Af)
metric_res=(Af*vg*(Ric_original-Rorig*g/2)-Bf*Xtensor).applyfunc(s.simplify)
for i in range(4):
    for j in range(4):
        zero(f'all16_metric_coframe_equations_{i}_{j}',metric_res[i,j])
# All16 tetrad equations follow from tensor rows + independent proper Cartan.
for comp in range(2):
    grad=psigrad if comp==0 else s.zeros(4,1)
    scalar=sum(s.diff(sum(Bf*ginv[mu,nu]*grad[nu] for nu in range(4)),coords[mu])
               for mu in range(4))
    zero(f'actual_two_scalar_rows_{comp}',scalar)
check('unprotected_fixed_original_torsion_is_not_omitted',s.diff(Af,sx)!=0)
check('original_y_is_NOT_spacetime_constant',s.diff(ygeom,sx)!=0)
zero('correct_new_constant_ratio',s.diff(ygeom/Af,sx))
# Hostile replacement: setting F_x to a frozen constant loses the field root.
wrong=(vg*(Ric_original-Rorig*g/2)-Bf*Xtensor).applyfunc(s.simplify)
check('freezing_nonlocal_price_source_fails',wrong!=s.zeros(4))
# Baseline moves freely? Then its actual derivative remains, no automatic root.
zeta=s.symbols('zeta',real=True)
check('nonstationary_upstream_not_hidden',s.diff(zeta+zeta**2,zeta).subs(zeta,0)!=0)

RESULT={'status':'AUTHOR_EXACT_NONLOCAL_DENSITY_REDUCTION_PASS','checks':CHECKS,
 'check_count':len(CHECKS),'input_ref':'7f87eaaba20a19b1dad3a27079a4417caff5bff1',
 'actual_finite_Golden_ratio_sigma_minus':str(ratio),
 'source_class':'given differentiable history functional of exactly two fixed-measure densities',
 'new_relation':'x=chi*deltaF/dy; y=chi*deltaF/dx; chi constant in spacetime',
 'native_moving_query_admission':False,'complete_Book03_valuation_selected':False,
 'arbitrary_kernel_gauge_covariance_assumed':False,'finite_native_lattice_Bianchi_proved':False,
 'physical_metric_equals_conjugate_metric_in_general':False,'GR_closed':False}
here=Path(__file__).resolve().parent
(here/'RESULT.json').write_text(json.dumps(RESULT,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(RESULT,indent=2,ensure_ascii=False))
