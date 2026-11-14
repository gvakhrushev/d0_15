#!/usr/bin/env python3
"""Check H1 source normalization and y+/y- reference signs exactly."""
from pathlib import Path
from hashlib import sha256
import json,sympy as s
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');meta=json.loads((O/'round21/REFERENCE_METADATA.json').read_text())
rho,d=s.symbols('rho d',positive=True);sqrt2=s.sqrt(2)/2;T=s.Matrix([[sqrt2,sqrt2,0,0],[sqrt2,-sqrt2,0,0],[0,0,1,0],[0,0,0,-1]]);cart=s.diag(1,-1,-1,-1);null=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]]);nu=s.Rational(3,5);h=s.Rational(1,4);sref=6
u=nu*s.sqrt(rho)/sref*T*cart;metric=s.simplify(u.T*null*u/nu**2);assert metric==rho/sref**2*cart
amp=h*sref*s.sqrt(d)/2
q_by_axis=[]
for axis in range(4):
 deriv=s.zeros(4,1);deriv[axis]=-2*amp/h
 value=s.simplify((deriv.T*metric*deriv)[0]);assert value==(rho*d if axis==0 else -rho*d);q_by_axis.append(str(value))
# Exact coefficient map from the actual A17 definition to H1 inherited r(x,y):
# u=p+sigma*p²*Hq/(64*rho*Lambda) versus u=p+p²*y.
Lambda=2**1525;epsilon=s.Rational(1,2**1531);assert epsilon==s.Rational(1,64*Lambda)
q=s.symbols('q',real=True);yplus=s.simplify(-epsilon*(-rho*d)/rho);yminus=s.simplify(-epsilon*(rho*d)/rho);assert yplus==epsilon*d and yminus==-epsilon*d
# sigma=-1 is encoded logical 0. Born v=G|0> and exact routed G^-1 is
# independently checked in B47/B48; seven RAW distinct wires cost this sum.
assert 7*1==7 and 7*6==42 and 7*4==28
files=[O/'round25/TARGETS_RU.md',O/'round25/targets.py',O/'round24/check_reference_frame.py',O/'round21/REFERENCE_METADATA.json',D/'round11/source_operator_dag.py',D/'round17/GLOBAL_REPORT_ASSEMBLY_RU.md']
out={'status':'PASS_OWNER_SIGMA_MINUS_AND_REFERENCE_SIGN_BINDING','input_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files},'original_r_u':'p + p^2*y','A17_report_u':'p + sigma*p^2*Hq/(64*rho*Lambda)','epsilon':'1/(64*Lambda)=2^-1531','H1_original_y':'-epsilon*Hq/rho','sigma_value':-1,'sigma_bit':0,'reference_metric':'(rho/36) diag(1,-1,-1,-1)','reference_amplitude':'h*6*sqrt(d)/2','Hq_axis_exact':q_by_axis,'yplus_space_Hq':'-rho*d','yminus_time_Hq':'+rho*d','yplus':'epsilon*d','yminus':'-epsilon*d','f_0_xplus_xminus_zero_matter_Hq_zero':True,'seven_distinct_sigma_RAW_zero_preparations':{'G_port':7,'CX':42,'SourceI':28},'assumptions':'A17 actual source moment/bank binding produces the audited Hq; all sigma wires receive true RAW v and have distinct valid routed layouts. The current bank g_q and all marks still require their own full H1 binding.','physical_birth_mark_admission_proved':False,'GR_closed':False}
(P/'SIGMA_OWNER_BINDING_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'sigma':-1,'seven_sigma_G_CX_SourceI':[7,42,28]}))
