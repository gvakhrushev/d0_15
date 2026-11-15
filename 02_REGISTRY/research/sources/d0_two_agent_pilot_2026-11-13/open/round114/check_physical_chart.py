#!/usr/bin/env python3
"""Exact finite L4 chart Jacobian, frame conventions and connection sample.

No physical V_h norm, admission, full marked transport or C/GR closure.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product,combinations
import json,sys
import sympy as s
import numpy as np
from scipy.linalg import expm,logm
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
sys.path.insert(0,str(P));import physical_chart_l4 as api
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
R=D.parents[2]
coords=O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl'
chart=O/'round21/CHART_ENVELOPE_RESULT.json'
pf=O/'round21/ORIGINAL_PF_N20_L4.jsonl'
rows=[json.loads(line) for line in coords.read_text().splitlines()]
envelope=json.loads(chart.read_text())
assert sha256(coords.read_bytes()).hexdigest()==envelope['coords_sha256']
sites=list(product(range(4),range(4),(1,2),(1,2)));expected=[]
for x in sites:
    for role in range(4):
        for component in range(4):expected.append({'site':list(x),'kind':'coframe','role':role,'component':component})
    for role in range(4):
        for i,j in combinations(range(4),2):expected.append({'site':list(x),'kind':'proper_link','role':role,'generator':[i,j]})
    for grade in (0,15):expected.append({'site':list(x),'kind':'matter','grade':grade})
assert len(rows)==len(expected)==64*42==2688
for i,(actual,want) in enumerate(zip(rows,expected)):
    assert actual==dict(want,sam_index=i)
sys.path.insert(0,str(D/'round54'));import regular_global_source as source
sam=source.namespace()['layout']['SAM']
assert len(sam)==5376
for j in range(2688):
    assert (source.physical_wire(sam[j]),source.physical_wire(sam[2688+j]))==(2+j,11893771936+j)
records=[json.loads(line) for line in pf.read_text().splitlines()]
assert len(records)==256 and min(r['N'] for r in records)==29 and max(r['N'] for r in records)==78
rho=[F(r['rho_numerator'],r['rho_denominator']) for r in records]
assert min(rho)==F(3712,5473) and max(rho)==F(768,421)
assert F(16,25)<min(rho) and max(rho)<F(9,4)
assert sum((F(r['N'],10946) for r in records),F())==1
for path,key in [(D/'round57/FULL_PLANE_FAMILY_PLAN.json','source_sha256'),
                 (O/'round113/B113_A57_AUDIT_CHECK.json','input_sha256')]:
    receipt=json.loads(path.read_text())
    for name,digest in receipt[key].items():assert sha256(Path(name).read_bytes()).hexdigest()==digest,name

# Null/rest frame conventions: T^T eta_R T = eta_N; the spatial S is
# different from T and fixes the native inverse-leg convention.
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
etaR=s.diag(1,-1,-1,-1);S=s.diag(1,1,-1,-1)
T=s.Matrix([[1,1,0,0],[1,-1,0,0],[0,0,s.sqrt(2),0],[0,0,0,-s.sqrt(2)]])/s.sqrt(2)
assert T.T*T==s.eye(4) and T.T*etaR*T==eta
assert eta.T==eta and eta*eta==s.eye(4) and S.T*S==s.eye(4) and eta*S==S*eta
nu=s.Rational(3,5);H=s.Symbol('H',real=True)
E=s.eye(4);E[1,0]=H/2
Ew=S*E/nu;u=eta*Ew.inv().T
u0=nu*s.Matrix([[0,1,0,0],[1,-H/2,0,0],[0,0,1,0],[0,0,0,1]])
assert s.simplify(u-u0)==s.zeros(4)
assert s.simplify((nu*eta*S).T*u.inv().T-E)==s.zeros(4)

# Algebraically connect writer V=s*sqrt(rho)*eta_R*(T Ew)^(-T)
# to the B21 null-frame input u, conditional on the same descriptor.
scale,rho=s.symbols('scale rho',positive=True)
V=scale*s.sqrt(rho)*etaR*(T*Ew).inv().T
assert s.simplify(T.T*V/(scale*s.sqrt(rho))-u)==s.zeros(4)
gram=s.simplify(V.T*etaR*V)
assert s.simplify(rho*gram.inv()-(Ew.T*eta*Ew)/(scale**2))==s.zeros(4)
lam=s.Symbol('lam',positive=True)
Vscaled=scale*s.sqrt(lam**2*rho)*etaR*(T*(lam*Ew)).inv().T
assert s.simplify(Vscaled-V)==s.zeros(4)

# Complete 16-component Jacobian and its inverse at symbolic H, not only
# a coframe column or the metric trace.
de=s.Matrix(4,4,s.symbols('e0:16'))
du=-u*de.T*E.inv().T
de_back=-E*du.T*u.inv().T
assert s.simplify(de_back-de)==s.zeros(4)
dU=s.Matrix(4,4,s.symbols('u0:16'))
dE=-E*dU.T*u.inv().T
assert s.simplify(-u*dE.T*E.inv().T-dU)==s.zeros(4)

# All six B21/B103 null-frame generators, their physical S conjugation,
# and their exact coordinate extraction/Frobenius Gram.
gens=[];pairs=list(combinations(range(4),2));signs=[]
for i,j in pairs:
    A=s.zeros(4);A[i,j]=1;A[j,i]=-1;G=eta*A;gens.append(G)
    assert G.T*eta+eta*G==s.zeros(4)
    signs.append(int(S[i,i]*S[j,j]));assert S*G*S==signs[-1]*G
assert signs==[1,-1,-1,-1,-1,1]
for i,G in enumerate(gens):
    for j,Hg in enumerate(gens):
        assert (G.T*Hg).trace()==(2 if i==j else 0)
    skew=eta*G
    assert [s.simplify((skew[x,y]-skew[y,x])/2) for x,y in pairs]==[int(i==j) for j in range(6)]

# Exact h-scaled physical connection sample: a genuine nilpotent B21
# central log. The integral dexp_Z is evaluated polynomially (Z^3=0),
# then projected onto the full six-dimensional Lorentz tangent basis.
N2=s.zeros(4);N2[1,2]=1;N2[2,0]=1
N3=s.zeros(4);N3[1,3]=1;N3[3,0]=1
Z=-s.Rational(1,100)*N2-s.Rational(1,150)*N3
assert Z**3==s.zeros(4) and Z.T*eta+eta*Z==s.zeros(4)
w=s.Symbol('w',real=True);expz=s.eye(4)+w*Z+w*w*Z**2/2
expminus=s.eye(4)-w*Z+w*w*Z**2/2
columns=[]
for G in gens:
    mat=(expz*G*expminus).applyfunc(lambda e:s.integrate(e,(w,0,1)))
    assert mat.T*eta+eta*mat==s.zeros(4)
    a=eta*mat
    columns.append(s.Matrix([(a[i,j]-a[j,i])/2 for i,j in pairs]))
dexp=s.Matrix.hstack(*columns)
assert dexp.det()==1
h=s.Rational(1,4);physical_to_theta=h*dexp
assert s.simplify(physical_to_theta.inv()*physical_to_theta)==s.eye(6)
assert physical_to_theta.det()==h**6
assert physical_to_theta!=dexp # an extra/missing h changes the calibration

# Uniform rational margins on the full declared L4 chart, with conservative
# Euclidean/Frobenius diagnostic bounds, not a chosen physical V_h norm.
nuF=F(3,5);old_s=F(1,1<<30);sigma=F(1,1<<80)
Rfield=F(1,1<<32);r=6*(Rfield+3*sigma)
u_upper=nuF*(1+F(3,40))+4*old_s
u_min=F(envelope['coframe_min_singular_strict_lower'])
assert u_upper<F(2,3) and u_min>F(1,2)
assert r<F(1,100) and F(2)*r/(1-2*r)<F(1,49)
assert F(1,25)+6*old_s<F(1,16)
assert F(1,25)+r<F(1,24)
# ||U-I||<1/23 implies ||log U||<1/22<1/20.
assert (F(1,24)/(1-F(1,24)))==F(1,23)
assert (F(1,23)/(1-F(1,23)))==F(1,22)<F(1,20)
cf_forward=F(2,3)*F(10,9);cf_inverse=F(6,5)*2
link_forward=F(49,48)*F(16,15);link_inverse=F(50,49)*F(16,15)*F(3,2)
assert cf_forward==F(20,27) and cf_inverse==F(12,5)
assert link_forward==F(49,45) and link_inverse==F(80,49)
omega_forward=F(49,48)*F(10,9)*F(1,4)
omega_inverse=F(9,8)*F(50,49)*4
assert omega_forward==F(245,864) and omega_inverse==F(225,49)
assert max(cf_forward,link_forward,F(1))==F(49,45)
assert max(cf_inverse,link_inverse,F(1))==F(12,5)
assert max(cf_forward,F(49,48),F(1))==F(49,48)
assert max(cf_inverse,F(50,49),F(1))==F(12,5)
assert max(cf_forward,omega_forward,F(1))==1
assert max(cf_inverse,omega_inverse,F(1))==F(225,49)

# The importable numerical evaluator is a bounded diagnostic of the exact
# formulas above. Test its complete 42x42 inverse, transposed pairing, and
# a nonlinear matrix finite difference; do not call floats a certificate.
approx={tuple(row['site']):row for row in (json.loads(line) for line in
        (O/'round21/BRINKMANN_L4_CENTRE.jsonl').read_text().splitlines())}
rng=np.random.default_rng(114);checked=0
for site in (sites[0],sites[21],sites[-1]):
    up=np.array(approx[site]['native_coframe_columns_approx'],dtype=float)
    th=rng.uniform(-1,1,(4,6))*float(F(1,1<<34))
    de0=rng.normal(size=(4,4));wj=rng.normal(size=(4,6));dp=rng.normal(size=2)
    raw=api.iota_site(up,th,de0,wj,dp)
    back=api.inverse_site(up,th,raw)
    assert np.max(np.abs(back[0]-de0))<2e-12
    assert np.max(np.abs(back[1]-wj))<2e-12 and np.max(np.abs(back[2]-dp))<2e-12
    lam0=rng.normal(size=42);cot=api.pullback_site(up,th,lam0)
    assert abs(lam0@raw-(np.sum(cot[0]*de0)+np.sum(cot[1]*wj)+cot[2]@dp))<2e-11
    _,_,Ep=api._point(up,th);eps=1e-7
    assert np.max(np.abs(api.A@np.linalg.inv(Ep).T-up))<2e-14
    uplus=api.A@np.linalg.inv(Ep+eps*de0).T
    assert np.max(np.abs((uplus-up)/eps-raw[:16].reshape(4,4).T))<1e-5
    Theta=np.tensordot(th[0],api.GEN,axes=(0,0))
    W=np.tensordot(api.SIGNS*wj[0],api.GEN,axes=(0,0))
    theta_delta=logm(expm(eps*W)@expm(Theta))
    numerical=np.array([np.sum(G*(theta_delta-Theta))/(2*eps) for G in api.GEN])
    assert np.max(np.abs(numerical-raw[16:22]))<1e-5
    checked+=1
assert checked==3
u64=np.array([approx[x]['native_coframe_columns_approx'] for x in sites],dtype=float)
th64=rng.uniform(-1,1,(64,4,6))*float(F(1,1<<34))
de64=rng.normal(size=(64,4,4));w64=rng.normal(size=(64,4,6));psi64=rng.normal(size=(64,2))
raw64=api.iota_l4(u64,th64,de64,w64,psi64)
cot64=rng.normal(size=2688);phys=api.pullback_l4(u64,th64,cot64)
expected=sum(np.sum(phys[i][0]*de64[i])+np.sum(phys[i][1]*w64[i])+phys[i][2]@psi64[i] for i in range(64))
actual=sum(float(x)*float(y) for x,y in zip(cot64,raw64))
assert raw64.shape==(2688,) and np.all(np.isfinite(raw64)) and np.isfinite(expected)
assert abs(actual-expected)<1e-9
try:api.iota_site(np.eye(4),np.zeros((4,6)),np.eye(4),np.zeros((4,6)),np.zeros(2))
except ValueError:pass
else:raise AssertionError('point outside the certified coframe bound accepted')

inputs=[Path(__file__),P/'physical_chart_l4.py',coords,chart,pf,O/'round21/H1_L4_PARTIAL_EXPORT_RU.md',
        O/'round21/BRINKMANN_L4_CENTRE.jsonl',
        O/'round25/targets.py',O/'round25/precision_name.py',
        D/'round53/regular_field_targets.py',D/'round20/coframe_targets.py',
        O/'round103/regular_link_julia.py',O/'round109/B109_FULL_CODE_SKEW_RECOVERY_RU.md',
        D/'round57/FULL_PLANE_FAMILY_PLAN.json',O/'round113/B113_A57_AUDIT_CHECK.json',
        R/'A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md',
        R/'A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md',
        R/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md',
        R/'sources/d0_retained_response_concentration_2026-10-28/SOURCE_PROOF_RU.md']
out={'status':'PASS_L4_FIXED_PF_COLLAR_TYPED_CHART_JACOBIAN_WITH_NORM_DEPENDENCIES',
     'interior_sites':64,'coordinates_per_site':42,'raw_coordinate_count':len(rows),
     'coordinate_order':'coframe[role][component], proper_link[role][01,02,03,12,13,23], matter[0,15]',
     'PF_rho_range':['3712/5473','768/421'],'physical_coframe_scale':'e_sp=nu^-1*S*E; nu=3/5; no extra h',
     'writer_density_relation':'u=T^T V/(s sqrt(rho)) when same physical descriptor is admitted',
     'full_16_coframe_jacobian_and_inverse_exact':True,
     'link_left_trivialized_map':'dtheta=G^-1 dexp_Theta^-1(dU U^-1)',
     'physical_S_generator_signs':signs,
     'exact_nilpotent_connection_dexp_6_by_6_check':True,'connection_explicit_step_h':'1/4',
     'numerical_api_inverse_pairing_and_nonlinear_diagnostic_sites':checked,
     'numerical_global_2688_component_pullback_pairing':True,
     'frobenius_dU_raw_forward_lt':'49/45','frobenius_dU_raw_inverse_lt':'12/5',
     'left_trivialized_42_block_forward_lt':'49/48','left_trivialized_42_block_inverse_lt':'12/5',
     'conditional_exponential_connection_forward_le':'1',
     'conditional_exponential_connection_inverse_le':'225/49',
     'physical_Vh_norm_or_iota_admission_supplied':False,
     'dynamic_PF_boundary_frame_or_general_connection_removed':False,
     'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in inputs}}
(P/'B114_PHYSICAL_CHART_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
