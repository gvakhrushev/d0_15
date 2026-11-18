#!/usr/bin/env python3
"""Independent A37 algebra and exact numerical budget; not native U* execution."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sympy as s
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
# Different physical denominators and gains: independent symbolic derivation.
et,d0,c0,gs,c,q,dc,dq=s.symbols('eta d0 c0 gs c q dc dq',positive=True)
Dold=d0+et*c*c;Dred=d0+et*q
G_old=4*et*c*gs/Dold;G_red=4*et*c0*gs/Dred
old=(-2*et*c*dc/Dold)/G_old
red=(-et*dq/Dred)/G_red
assert s.simplify(red-old+(dq-2*c0*dc)/(4*c0*gs))==0
# Validate the variance identity for an arbitrary real symmetric 3x3 M and
# arbitrary skew-generator X, not only a numerically diagonal fixture.
a,b,d,e,f,h=s.symbols('a b d e f h',real=True)
M=s.Matrix([[a,b,d],[b,e,f],[d,f,h]])
x,y,z=s.symbols('x y z',real=True);v=s.Matrix([x,y,z])
u1,u2,u3=s.symbols('u1 u2 u3',real=True)
X=s.Matrix([[0,u1,u2],[-u1,0,u3],[-u2,-u3,0]])
dM=2*(v.T*M*X*v)[0];dM2=2*(v.T*M*M*X*v)[0]
V=(M-c0*s.eye(3))**2
assert s.expand(2*(v.T*V*X*v)[0]-(dM2-2*c0*dM))==0
# U*=I+K+K²/(1+d): local rotation taking xi to chi.  In a 2-plane
# chi=(1,0), xi=(d,r), impose d²+r²=1 exactly.
dd,rr=s.symbols('dd rr',real=True);xi=s.Matrix([dd,rr]);chi=s.Matrix([1,0]);K=chi*xi.T-xi*chi.T
U=s.eye(2)+K+K*K/(1+dd)
def reduce_circle(e):
    num,_=s.fraction(s.cancel(e));return s.rem(s.expand(num),rr**2+dd**2-1,rr).expand()
assert all(reduce_circle(v)==0 for v in U*xi-chi)
assert all(reduce_circle(v)==0 for v in U.T*U-s.eye(2))
assert reduce_circle(U.det()-1)==0
# Counterexample to d>0 for arbitrary normalized psi and singular antipode.
assert (s.Matrix([1,0]).T*s.Matrix([-1,0]))[0]==-1
# ||psi-chi||<1/6, chi^T M chi>2/3, ||M||<=1 imply d>1/2.
assert F(2,3)-F(1,6)==F(1,2)
# Source and contrast bounds, exact rationals.  Preconditions are the
# original fixed B25/B65/A33 source results, not auto-admission of a task.
assert 2**13+24*16+F(1,2**1457)<2**14
p,x,y,z=s.symbols('p x y z');E=p**2*(1+x);ell=4*E*(1-E);u=p+p**2*y;b=4*u*u*(1-u*u);A=ell+(1-ell)*b;r=s.expand(1-(1-z*b)*(1-z*A))
for dr in (s.diff(r,x),s.diff(r,y)):
    assert sum(abs(t) for t in s.Poly(dr,p,x,y,z).coeffs())<2**21
ref_delta=F(1,2**1543);eps=F(1,2**1531)
g_upper=2*ref_delta*eps*2**42
assert g_upper==F(1,2**3031) and g_upper<F(1,2**3030)
native=F(1,2**3231); sigma=2*g_upper*2**14+native
assert sigma<F(1,2**3014)
# p²+p=1 => p^7=13p−8; actual visibility λ=κ p^7, 0<κ<=1.
lo,hi=F(618033,10**6),F(618034,10**6)
assert lo*lo+lo<1<hi*hi+hi
assert s.rem(p**7-(13*p-8),p*p+p-1,p)==0
p7upper=13*hi-8
assert 1-8*p7upper>F(2,3)
# For ||X||<=1, derivative of <(M-c_ref I)^2> has norm <=2 sigma².
# c_ref>2/3 and gs>2^-3158 imply the row bound below.
row=sigma*sigma*F(3,4)*2**3158
assert row<F(1,2**2870) and 55*row<F(1,2**2864)
# A34/B67 finite H+J vector relative to A32 analytic determinant at the
# same input has a separate <=2^-67 finite-price/heat budget. A33/B66's
# lower bound is used only after this subtraction; no new native U* source.
lifted=55*row; finite=F(1,2**67)
assert F(1,2**45)-finite-lifted>F(1,2**46)
assert F(1,2**17)+finite+lifted<F(1,2**16)
assert F(1,2**16)+finite+lifted<F(1,2**15)
# Optional analytic-only q(theta) finite-difference truncation: ||M||<=1
# implies ||ad_X^k M²||<=2^k.  This does NOT include a native U* word,
# angle synthesis, changed output, clock or heat.
z0=F(1,2**20);t=F(1,2**1618)
bracket=8/(1-z0)+24*z0/(1-z0)**2+16*z0*z0/(1-z0)**3
bracket_old=64/(1-z0)+192*z0/(1-z0)**2+128*z0*z0/(1-z0)**3
assert 8*bracket==bracket_old
fd=t*t*2**3158*bracket/16
assert fd<F(1,2**78)
# Actual second moment is not the square of the matched mean: exact
# normalized two-level positive, nonconstant diagonal counterexample.
psi=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
mat=s.diag(s.Rational(7,10),s.Rational(4,5))
mean=(psi.T*mat*psi)[0];second=(psi.T*mat*mat*psi)[0]
assert s.simplify(second-mean**2)>0
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
aplan=json.loads((D/'round37/POST_SAM_REDUCTION_PLAN.json').read_text())
acheck=json.loads((D/'round37/POST_SAM_REDUCTION_CHECK.json').read_text())
assert aplan['status']=='ACTUAL_A30_ANALYTIC_POST_SAM_FEEDBACK_STATIONARY_SECTION'
assert acheck['status']=='PASS_EXACT_POST_SAM_TARGET_SOURCE_IDENTITY_AND_CONDITIONAL_A30_BOUNDS'
assert not aplan['new_paid_native_target_word_emitted'] and not aplan['new_full_heat_or_H_plus_J_stationarity_proved']
for source in (aplan,acheck):
    for f,digest in source['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==digest,f
files=[Path(__file__),D/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md',D/'round37/post_sam_reduction.py',D/'round37/check_post_sam_reduction.py',D/'round37/POST_SAM_REDUCTION_PLAN.json',D/'round37/POST_SAM_REDUCTION_CHECK.json',D/'round2/SAM_BACKWARD_RU.md',D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',D/'round30/COMMON_RAW_SOURCE_MARKS_RU.md',D/'round31/ACTUAL_MEAN_GEOMETRY_LIFT_RU.md',O/'round54/B54_PRODUCT_SOURCE_EXACT_RU.md',O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',O/'round65/SCALAR_HESSIAN_ENVELOPE.json',O/'round65/FINITE_REFERENCE_SECANT_DEFECT.json',O/'round71/A36_INDEPENDENT_AUDIT.json',O/'round72/B72_BACKWARD_MARKED_OUTPUT_SUBSYSTEM_RU.md']
out={'status':'PASS_CONDITIONAL_REDUCED_FEEDBACK_ALGEBRA_AND_BOUNDS','I_tau_uniform_abs_lt':'2^14','original_gain_g_lt':'2^-3030','reference_c_ref_gt':'2/3','sigma_lt':'2^-3014','single_row_source_change_lt':'2^-2870','A31_forward_corrected_vector_norm_lt':'2^-2864','reduced_analytic_feedback_norm_between':['2^-46','2^-16'],'reduced_feedback_minus_Egeom_at_decoded_mean_lt':'2^-15','source_identity':'d_red-d_old=-D_psi <(M-c_ref I)^2>/(4 c_ref g s)','real_SO_rank_two_rotation_formula_locally_verified':True,'global_positive_d_or_global_single_chart':False,'analytic_only_reduced_feedback_fd_truncation_lt':'2^-78 conditional','paid_native_Ustar_or_its_circuit_error_constructed':False,'full_heat_plus_J_or_Cost_Info_stationarity_proved':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files}}
(P/'REDUCED_FEEDBACK_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'row_lt':out['single_row_source_change_lt'],'corrected_lt':out['A31_forward_corrected_vector_norm_lt']}))
