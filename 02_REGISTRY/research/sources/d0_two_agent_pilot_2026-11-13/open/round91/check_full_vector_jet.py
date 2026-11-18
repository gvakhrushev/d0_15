#!/usr/bin/env python3
"""Exact sampler obstruction, source amplitude witness, and typed fibres."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
import json,sys
import sympy as sp
from sympy.polys.domains import QQ
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
OWNER=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md')
sys.path.insert(0,str(D/'round46'));import independent_current_bank as a46
sys.path.insert(0,str(O/'round25'));import targets
# Exact Q(sqrt(p)), a^4+a^2=1, not floating identities.
root=sp.sqrt((sp.sqrt(5)-1)/2);K=QQ.algebraic_field(root);a=K.from_sympy(root);p=a*a;one=K.one;zero=K.zero
assert p*p+p==one and 1-2*p*p==p**3
v=[a,p];u=2*p*a
assert sum((x*x for x in v),zero)==one and u*u+p**6==one
w=[p,a];res=[w[i]-u*v[i] for i in range(2)]
assert sum((x*x for x in res),zero)==p**6
# Correct scalar derivative demands X=J/u; exact residual p^3/u.
meanfixed=[w[i]/u-v[i] for i in range(2)]
assert sum((x*x for x in meanfixed),zero)==p**6/(u*u)
# General skew on arbitrary SAM x spectator: block anti-commutation produces
# a skew matrix for (I−2Π)[Π,X], so expectation in any real input is 0.
a01,a02,a03,a12,a13,a23=sp.symbols('a01 a02 a03 a12 a13 a23',real=True)
X=sp.Matrix([[0,a01,a02,a03],[-a01,0,a12,a13],[-a02,-a12,0,a23],[-a03,-a13,-a23,0]])
Pi=sp.diag(0,0,1,1);Z=sp.eye(4)-2*Pi;H=Pi*X-X*Pi
assert H.T==H and (Z*H).T==-Z*H and Z*H+H*Z==sp.zeros(4)
# Exact owned two-bit MG2/MG3, all entries in the Golden field.
phi=[p,p*a,p*a,p*p];pi=[q*q for q in phi];hs=[one/(one-2*q) for q in pi]
S=sum((pi[i]*hs[i] for i in range(4)),zero);V=[-3*p*p,one-3*p*p,2*one-3*p*p,3*one-3*p*p]
H2=[[zero if i==j else phi[i]*phi[j]*(hs[i]+hs[j])/(one+S) for j in range(4)] for i in range(4)]
X2=[[zero if i==j else H2[i][j]/(i-j) for j in range(4)] for i in range(4)]
assert sum(pi,zero)==one and sum((pi[i]*V[i] for i in range(4)),zero)==zero
assert all(X2[i][j]==-X2[j][i] for i in range(4) for j in range(4))
assert all((V[i]-V[j])*X2[i][j]==H2[i][j] for i in range(4) for j in range(4))
assert all(sum((H2[i][j]*phi[j] for j in range(4)),zero)==phi[i] for i in range(4))
# Frobenius norm and sum of the six positive plane coefficients in exact field.
norm2=sum((X2[i][j]*X2[i][j] for i in range(4) for j in range(4)),zero)
expected_norm=K.from_sympy(F(391,363)-F(491,4356)*sp.sqrt(5))
assert norm2==expected_norm and F(391,363)-F(491,4356)*2<1
planes=sum((-X2[i][j] for i in range(4) for j in range(i+1,4)),zero)
expected_planes=K.from_sympy(F(13,33)-sp.sqrt(5)/66+root*(21+3*sp.sqrt(5))/22)
assert planes==expected_planes
assert F(12,33)+F(4,5)*(21+3*F(9,4))/22<F(3,2)
# Bind the real original source leaf, one fresh Choi, and all copy totals.
plan=a46.namespace();fresh=plan['reports'][7];slots=plan['source_slots']
assert len(plan['layout']['SAM'])==2688
assert Counter(z['kind'] for z in slots)=={'Choi':1440,'CAR':128}
sel=[i for i in fresh['source_slots'] if slots[i]['kind']=='Choi' and slots[i]['walk']=='S1' and slots[i]['copy']==0]
assert sel==[1372]
binding=json.loads((D/'round11/PERIODIC_SOURCE_BINDING.json').read_text())
assert binding['site_bindings'][5]['site']==[0,0,1,1] and binding['leaf_templates'][2]['name']=='u/0/2'
assert binding['site_bindings'][5]['leaf_addresses_in_template_order'][2]==21
assert int(targets.CREATORS[2][4,0])==1 and all(int(targets.CREATORS[i][4,0])==int(i==2) for i in range(4))
assert targets.ADDR[21]['kind']=='inverse_coframe_column' and targets.ADDR[21]['site']==[0,0,1,1]
assert targets.chi_ref((0,0,0,0),0)==1/128
assert a46.inventory()['eta_common_new']<F(1,2**3232)
# Ideal SOURCE amplitude: anchor r=(0,0,0) yields c; query t=(21,0,4)
# yields c*u_j for any label. CAR(z=0,grade=1,r=0) yields d=a/128.
# An environment functional choosing those amplitudes in all source copies
# has Ksrc=c^1440*d^128>0 and returns Ksrc*u_j for every label b.
assert 2**16<65568<2**18 and F(1,2)<F(3,5) # 2^-9<c<2^-8, 2^-8<d<2^-7
assert 1440*9+128*8==13984 and 1440*8+128*7==12416
# Arbitrary real 2x2 P demonstrates that contraction commutes with the
# matched frame and yields exact Ksrc P^T diag(u_0,u_1) P; no output trace.
p00,p01,p10,p11,z0,z1=sp.symbols('p00 p01 p10 p11 z0 z1',real=True)
P=sp.Matrix([[p00,p01],[p10,p11]]);E=sp.diag(z0,z1)
raw=sp.Matrix(2,2,lambda i,j:sum(P[b,i]*[z0,z1][b]*P[b,j] for b in range(2)))
assert raw==P.T*E*P
# A47's 2-bit code and proposed sigma remain inside the old asymmetric cube.
s=F(1,2**30);sigma=F(1,2**80)
assert 3*sigma<F(1,3)*s and 3*sigma<F(3,5)*s
assert sigma/s==F(1,2**50)
assert F(1,2**3231)/F(1,2**3208)==F(1,2**23)
# Independent full DATA-column target derivative bounds, valid on the same
# continuous chart and canonical SOURCE-private embedding, not dirty private.
slack=json.loads((O/'round21/CHART_ENVELOPE_RESULT.json').read_text())
cf=F(slack['coframe_creator_norm_strict_upper']);L=F(slack['material_slack_strict_lower'])
assert 1-cf*cf>F(1,16) and L>F(1,3)
# ||dTheta|| <= sqrt(6)||h||. For the old cube ||Theta||<=6s.
link_factor=F(17,16)/(1-6*s)
assert 6*link_factor**2<9 and 6*link_factor<7
link1=F(1,2)*4*F(17,16)**3*3
link2=F(1,2)*(4*F(17,16)**3*7+12*F(17,16)**2*9)
assert link1<8 and link2<80
assert 40**2<2049 and 4752**2<112**2*2049
assert F(108,25)<F(441,100) # (6/5 sqrt(3))² < (21/10)²
assert 3*F(21,10)+2*F(11,10)**2<12
M1=540*3+32*4;M2=M1*M1-(540*3**2+32*4**2)+540*338+32*12
assert M1==1748 and M1<2**11 and M2==3233036 and M2<2**22
assert sigma*104**2*M2<F(1,2**44)
# General source approximation budget is many orders larger than Ksrc;
# it cannot establish the same strict lower bound for the compiled word.
assert 12416>3200 and 2*F(1,2**3232)*2/s==F(1,2**3200)
files=[Path(__file__),OWNER,D/'round46/independent_current_bank.py',D/'round46/INDEPENDENT_CURRENT_BANK_PLAN.json',
 D/'round46/INDEPENDENT_CURRENT_BANK_RU.md',D/'round31/ACTUAL_MEAN_GEOMETRY_LIFT_RU.md',
 D/'round22/FULL_RAW_CHOI_RU.md',D/'round24/FULL_CAR_SOURCE_RU.md',D/'round23/CAR_VACUUM_FOURIER_RU.md',
 D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',D/'round11/PERIODIC_SOURCE_BINDING.json',
 O/'round21/CHART_ENVELOPE_RESULT.json',O/'round25/targets.py',O/'round35/BANK_PREPARATION_REDUCTION_RU.md',O/'round45/SITE_NATIVE_RU.md',
 O/'round90/B90_FRESH_CURRENT_ARENA_AUDIT_RU.md']
out={'status':'EXACT_ONE_BIT_FULL_VECTOR_OBSTRUCTION_AND_OWNED_TWO_BIT_REPAIR_MAP',
 'one_bit_global_skew_gap':'p^3 for unrestricted real skew; p^3/(2 p sqrt(p)) if scalar mean normalized',
 'source_functional_leaf':'fresh Choi slot 1372, site 5, Julia address 21, input 0, output 4',
 'ideal_source_witness_factor':'(1/sqrt(65568))^1440*(sqrt(p)/128)^128',
 'ideal_witness_factor_strict_between':['2^-13984','2^-12416'],
 'actual_native_nonzero_jet_proved_from_current_error':False,
 'MG2_two_bit_exact_identity_Qsqrtp':True,'MG2_Frobenius_norm_squared':'391/363-491*sqrt(5)/4356','full_columns_fibre':'all SOURCE DATA and SITE columns with each SOURCE private at declared RAW input, arbitrary SAM/old/reference',
 'all_dirty_source_private_or_original_CAR_vacuum_extension_identified':False,
 'full_DATA_target_M1_upper':M1,'full_DATA_target_M2_upper':M2,
 'two_bit_sigma':'2^-80','new_sampler_table_or_paid_family_built':False,
 'physical_C_closed':False,'GR_closed':False,
 'source_sha256':{str(f.resolve()):sha256(f.read_bytes()).hexdigest() for f in files}}
Path(__file__).with_name('B91_FULL_VECTOR_JET_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
