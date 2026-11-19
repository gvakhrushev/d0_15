from pathlib import Path
import ast, hashlib, json
from functools import lru_cache
import sympy as s

base=Path(__file__).with_name('GRAM_RESULTS.json')
base_bytes=base.read_bytes()
base_sha='a737b0c285cca3f0fea6d5d78c9a6e5d48fcaad3b5d2fc47c8cc557c643d3e2e'
if hashlib.sha256(base_bytes).hexdigest()!=base_sha:raise ArithmeticError('immutable_first_Gram')
previous=json.loads(base_bytes)
coords=[tuple(x) for x in previous['coordinates']]
G=s.Matrix([[s.Rational(x) for x in row] for row in previous['Gram']])
repo=Path(__file__).resolve().parents[4]
source=repo/'02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
data=source.read_bytes()
expected='bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da'
if hashlib.sha256(data).hexdigest()!=expected:raise ArithmeticError('actual_creator_pin')
tree=ast.parse(data)
nodes=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name=='creator') or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXTERIOR_ORDER' for t in n.targets))]
namespace={'s':s,'lru_cache':lru_cache}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),namespace)
C=[namespace['creator'](i) for i in range(4)]
A=[c.T for c in C]
gamma=[C[i]-A[i] for i in range(4)]
hat=[C[i]+A[i] for i in range(4)]
checks=[]
def eq(actual,expected,label):
    if isinstance(actual,s.MatrixBase):
        if actual.shape!=expected.shape or any(x!=0 for x in actual-expected):raise ArithmeticError(label)
    elif s.expand(actual-expected)!=0:raise ArithmeticError(label)
    checks.append(label)
def T(row,a,b,c):
    if b==c:return s.Integer(0)
    return row[coords.index((a,b,c))] if b<c else -row[coords.index((a,c,b))]
I=s.eye(24)
V=s.Matrix(4,24,lambda c,k:sum(T(I[:,k],a,a,c) for a in range(4)))
triples=[(a,b,c) for a in range(4) for b in range(a+1,4) for c in range(b+1,4)]
H=s.Matrix(4,24,lambda i,k:T(I[:,k],*triples[i])+T(I[:,k],*triples[i][1:],triples[i][0])+T(I[:,k],triples[i][2],*triples[i][:2]))
eq(G,2*H.T*H-4*V.T*V,'full24_exact_q_equals_2h_squared_minus_4v_squared')
Zbasis=[]
for a,b,c in coords:
    Q=C[b]*C[c]*A[a]
    Zbasis.append(Q+Q.T)
image=s.Matrix.hstack(*[z.reshape(256,1) for z in Zbasis])
kernel=s.Matrix.hstack(*G.nullspace())
if (image*kernel).rank()!=16:raise ArithmeticError('kernel_contains_16_independent_NONZERO_operator_directions')
checks.append('kernel_contains_16_independent_NONZERO_operator_directions')
w=s.zeros(24,1)
w[coords.index((0,1,2))]=1
w[coords.index((1,0,2))]=1
Zw=sum((w[k]*Zbasis[k] for k in range(24)),s.zeros(16))
eq(V*w,s.zeros(4,1),'named_tensor_witness_zero_v')
eq(H*w,s.zeros(4,1),'named_tensor_witness_zero_h')
eq(G*w,s.zeros(24,1),'named_tensor_witness_full_bilinear_kernel_not_merely_isotropic')
eq(s.trace(Zw*Zw),8,'named_tensor_witness_operator_nonzero_HS_squared_8')
B=[-(gamma[i]*Zw+Zw*gamma[i])/2 for i in range(4)]
eq(Zw,-(gamma[0]*hat[1]*hat[2]+gamma[1]*hat[0]*hat[2])/2,'actual_exact_right_Clifford_decomposition')
eq(B[0],-hat[1]*hat[2]/2,'B0_actual')
eq(B[1],-hat[0]*hat[2]/2,'B1_actual')
eq(B[2],s.zeros(16),'B2_zero')
eq(B[3],s.zeros(16),'B3_zero')
for i in range(4):
    eq(B[i].T,-B[i],'flavour_connection_antiHermitian_%d'%i)
    for j in range(4):eq(B[i]*gamma[j],gamma[j]*B[i],'flavour_connection_commutes_left_Clifford_%d_%d'%(i,j))
eq(sum((gamma[i]*B[i] for i in range(4)),s.zeros(16)),Zw,'exact_connection_type_Z')
curvature=B[0]*B[1]-B[1]*B[0]
eq(curvature,hat[0]*hat[1]/2,'named_constant_connection_curvature_NONZERO')
eq(s.trace(curvature.T*curvature),4,'constant_curvature_HS_squared_4')
eq(-s.trace(Zw*Zw)-sum(s.trace((g*Zw+Zw*g)**2) for g in gamma)/4,0,'named_witness_q_zero')
eq(s.trace((Zw-gamma[2]*hat[0]*hat[1]).T*(Zw-gamma[2]*hat[0]*hat[1])),24,'single_gamma2_flavour_proposal_rejected_HS_squared_24')
# For every actual kernel direction, Z is an unmodified left-Clifford
# connection perturbation sum gamma_i B_i with antiHermitian right B_i.
for a in range(kernel.cols):
    zz=s.Matrix(image*kernel[:,a]).reshape(16,16)
    bb=[-(g*zz+zz*g)/2 for g in gamma]
    eq(sum((gamma[i]*bb[i] for i in range(4)),s.zeros(16)),zz,'generic_tensor_kernel_connection_type_%d'%a)
    for i in range(4):
        for j in range(4):eq(bb[i]*gamma[j],gamma[j]*bb[i],'generic_tensor_right_commutant_%d_%d_%d'%(a,i,j))
# NEW consumer: a2-blind tensor direction is visible at the next heat
# coefficient.  This is the actual constant Clifford-connection family
# D_lam=sum gamma_i(partial_i+lam B_i), with its complete16 carrier.
lam=s.Symbol('lambda',real=True)
conn=[lam*x for x in B]
F={(i,j):conn[i]*conn[j]-conn[j]*conn[i] for i in range(4) for j in range(4)}
eq(F[0,1],lam**2*hat[0]*hat[1]/2,'a4_actual_constant_curvature_F01')
for i in range(4):
    for j in range(i+1,4):
        if (i,j)!=(0,1):eq(F[i,j],s.zeros(16),'a4_other_curvature_zero_%d_%d'%(i,j))
EE=-sum((gamma[i]*gamma[j]*F[i,j] for i in range(4) for j in range(i+1,4)),s.zeros(16))
eq(EE.T,EE,'a4_endomorphism_Hermitian')
eq(s.trace(EE),0,'a2_trace_zero_for_every_lambda')
eq(s.trace(EE*EE),4*lam**4,'a4_full16_trace_E_squared')
Ftrace=sum((s.trace(F[i,j]*F[i,j]) for i in range(4) for j in range(4)),s.Integer(0))
eq(Ftrace,-8*lam**4,'a4_full_ordered_ij_curvature_trace')
eq(s.trace(F[0,1]*F[0,1]),-4*lam**4,'a4_F01_squared_sign')
# Covariant derivative of a constant E need not vanish; only its trace
# Laplacian vanishes by cyclicity.  Do not silently freeze the connection.
cov_laplacian=sum((conn[i]*(conn[i]*EE-EE*conn[i])-(conn[i]*EE-EE*conn[i])*conn[i]
                   for i in range(4)),s.zeros(16))
eq(s.trace(cov_laplacian),0,'a4_covariant_laplacian_trace_zero_not_frozen')
a4=s.expand(s.trace(EE*EE)/2+Ftrace/12+s.trace(cov_laplacian)/6)
eq(a4,s.Rational(4,3)*lam**4,'a4_named_family_nonzero_exact')
eq(s.diff(a4,lam),s.Rational(16,3)*lam**3,'a4_named_family_Euler_selects_lambda_zero')
eq(a4,-Ftrace/6,'a4_trace_identity_minus_one_sixth_ordered_curvature')

# NEW consumer: a genuine scalar density w, b=dlog(w).  For the actual
# convention d_native=d_dR-Q_T, conjugation by sqrt(w) gives
# Z_eff=-Z_Q-hatgamma(b)/2.  Its exact q is tested by all96 mixed traces.
cross=s.zeros(24,4)
for i in range(24):
    for j in range(4):
        value=s.trace(Zbasis[i]*hat[j])
        eq(value,-8*V[j,i],'density_all96_TrZ_hat_%d_%d'%(i,j))
        cross[i,j]=value
for i in range(4):
    for j in range(4):
        eq(s.trace(hat[i]*hat[j]),16*int(i==j),'density_hat_Gram_%d_%d'%(i,j))
        eq(gamma[i]*hat[j]+hat[j]*gamma[i],s.zeros(16),'density_hat_anticommutes_gamma_%d_%d'%(i,j))
# Pullback under [T,b] -> -Z(T)-hat(b)/2.  The sign here matters.
effective=G.row_join(-cross/2).col_join((-cross.T/2).row_join(-4*s.eye(4)))
hh=H.row_join(s.zeros(4))
vv=V.row_join(-s.eye(4))
eq(effective,2*hh.T*hh-4*vv.T*vv,'density_full28_q_eff_equals_2h_squared_minus_4_v_minus_b_squared')
if effective.rank()!=8:raise ArithmeticError('density_form_rank_8_kernel20')
checks.append('density_form_rank_8_kernel20')
print(json.dumps({'schema':'d0-torsion-a2-kernel-consumer/2','status':'PASS_EXACT','prior_Gram_sha256':base_sha,'prior_kernel_result_sha256':'09a4aa6dd94ef9646a68a09335ab118e070b51c6e5d6ff07a0554616fa2df4df','quadratic_identity':'q(T)=2 sum_(a<b<c) (T^a_bc+T^b_ca+T^c_ab)^2 -4 sum_c(sum_a T^a_ac)^2','generic_quadratic_rank':8,'generic_quadratic_inertia':{'positive':4,'negative':4,'zero':16},'kernel_is_exact_tracefree_cycliczero_tensor16':True,'kernel_operator_image_rank':16,'tensor_witness':{'nonzero_coordinates':{'T0_12':1,'T1_02':1},'Z_HS_squared':8,'Z_rank':Zw.rank(),'q':0,'flavour_B0':'-hatgamma1*hatgamma2/2','flavour_B1':'-hatgamma0*hatgamma2/2','flavour_B2_B3_zero':True,'constant_curvature_F01':'hatgamma0*hatgamma1/2','curvature_HS_squared':4,'single_gamma2_B2_is_actual_witness':False,'flat_flavour_holonomy_claim':False},'a4_named_family':{'family':'D_lambda=sum gamma_i(partial_i+lambda B_i)','a2_trace':'0 for all lambda','F01':'lambda^2 hatgamma0 hatgamma1/2','Tr_F01_squared':'-4 lambda^4','ordered_ij_sum_Tr_Fij_squared':'-8 lambda^4','Tr_E_squared':'4 lambda^4','Tr_covariant_laplacian_E':'0','traced_a4_without_common_4pi_factor':'4/3 lambda^4','lambda_derivative':'16/3 lambda^3','only_named_family_Euler_classified':True,'full_tensor16_a4_Euler_classified':False},'density_shift':{'convention':'d_native=d_deRham-Q_T','unitary':'multiplication by sqrt(w), b=dlog(w)','Z_effective':'-Z_Q-hatgamma(b)/2','Tr_ZQ_hatgamma_b':'-8 v dot b','Tr_hatgamma_b_squared':'16 |b|^2','q_effective':'2 |h|^2-4 |v-b|^2','all96_cross_traces_checked':True,'effective_28_variable_rank':8,'effective_kernel_dimension':20,'arbitrary_global_density_gradient_admission_claim':False},'all_kernel_Z_are_right_Clifford_connection_type':True,'checks':len(checks),'checks_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest(),'creator_source_sha256':expected,'scope':'conditional actual deRhamHodge baseline/same measure/Clifford-compatible connection; named a4 family and scalar-density conjugation only; no new action/physical admission/fullprice stationarity claim'},sort_keys=True))
