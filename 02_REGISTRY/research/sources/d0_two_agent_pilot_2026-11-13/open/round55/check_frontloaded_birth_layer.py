#!/usr/bin/env python3
"""Exact ST4 obstruction for any front-loaded A25/A28 birth order.

All canonical births precede A and no gates occur between them. Selectors are
fresh RAW v and the active port is among these births. Does not address other
interleaved histories or prove that the actual full heat derivative is nonzero.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
import importlib.util,itertools,json,sys
import sympy as s
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13');domain=root/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py';files=[D/'round25/GLOBAL_H1_PLAN.json',D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/global_h1.py',O/'round49/SC6_ACTIVE_PORT_OWNER_CHECK.json',O/'round53/READY_GAIN_INTEGER_INDEPENDENT_CHECK.json',O/'round52/SCALAR_CORNER_PREMISE_CHECK.json',domain];h=lambda x:sha256(x.read_bytes()).hexdigest();pins={str(f):h(f) for f in files};globalp=json.loads(files[0].read_text());ns=json.loads(files[1].read_text());sc6=json.loads(files[3].read_text());ready=json.loads(files[4].read_text());schedule=globalp['forward_stage_schedule'];assert [z['kind'] for z in schedule][-2:]==['PORT_ZERO','SC6'] and globalp['port_G_inverse_after_all_R_load'];assert sc6['status']=='PASS_SC6_EXACT_ACTUAL_PORT_CONTROL_AND_OWNER_EMBEDDING' and ready['status']=='PASS_INDEPENDENT_INTEGER_READY_AND_GAIN_FLOOR';assert ns['SC6_local_to_global'][19]==ns['layout']['port']
terms=[(z['selector'],z['sign'],*z['call_indices']) for z in sc6['term_normal_forms']];assert len(terms)==8 and len({z[0] for z in terms})==8 and all(z[0].count('1')==2 for z in terms)
count=Counter()
for e in itertools.product((0,1),repeat=7):
 n=sum(e[i]*e[j] if sign>0 else 1-e[i]*e[j] for _,sign,i,j in terms);count[n]+=1
assert min(count)==2 and max(count)==6 and sum(count.values())==128
# R^T Z R and off-diagonal between port |0> and |1>. This remains exact for
# the true φ=512 θ with c²+s²=1; κ=s².
c,t=s.symbols('c t',real=True);R=s.Matrix([[c,-t],[t,c]]);Z=s.diag(1,-1);P0=s.diag(1,0);M=R.T*Z*R;comm=M*P0-P0*M;assert M[0,1]==-2*c*t and comm.T*comm==4*c*c*t*t*s.eye(2)
# j_v=G|0>, j_vperp=G|1>; G is orthogonal for p+p²=1.
spec=importlib.util.spec_from_file_location('b55_native',domain);nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt);G=s.Matrix(nt.G_LOCAL);assert nt.exact_matrix_equal(G.T*G,s.eye(2));v=G*s.Matrix([1,0]);vp=G*s.Matrix([0,1]);assert nt.exact_matrix_equal(v.T*vp,s.zeros(1,1)) and nt.exact_matrix_equal(v.T*v,s.ones(1,1)) and nt.exact_matrix_equal(vp.T*vp,s.ones(1,1))
# Birth-layer membership for arbitrary placement: the only special factor is
# (I−|v><v|)_port; every subsequently born wire is v in both witnesses.
Pv=v*v.T;Dv=s.eye(2)-Pv;assert nt.exact_matrix_equal(Dv*v,s.zeros(2,1)) and nt.exact_matrix_equal(Dv*vp,vp)
kl=F(93793197770933667,10**17);ku=F(93793197770933668,10**17);assert 4*kl*(1-ku)>F(12,25)**2
pl=F(309,500);bound=F(12,25)*2*pl**7;assert bound>F(3,100)
# In the real code domain an aux deliberately addressed by G cannot also be
# declared immutable old_right, though an active arbitrary input is legal.
Gaux=nt.Gate('G',(3,));legal=nt.Execution(5,(),(4,),(Gaux,),nt.G_CX_SOURCE_I,0,(1,2));nt.validate_execution(legal,max_qubits=5,max_expanded_stages=1)
sealed=nt.Execution(5,(),(3,4),(Gaux,),nt.G_CX_SOURCE_I,0,(1,2))
try:nt.validate_execution(sealed,max_qubits=5,max_expanded_stages=1)
except nt.DomainError as error:assert 'immutable old_right' in str(error)
else:raise AssertionError('addressed aux accepted as sealed old RIGHT')
# Minimal diagnostic growing clock with one birth and a reflection. Its
# Tr(T) depends on reflection angle, so W²=I does not imply ST6/ST4.
u,w=s.symbols('u w',real=True);T=s.Matrix([[0,u,w],[1,0,0],[0,w,-u]]);assert s.trace(T)==-u and s.expand(T.T*T-s.eye(3))==(u*u+w*w-1)*s.diag(0,1,1)
for path,pin in pins.items():assert h(Path(path))==pin,path
out={'status':'PASS_FRONTLOADED_PORT_BIRTH_LAYER_ST4_OBSTRUCTION','input_sha256':pins,'SC6_report_event_pattern_counts':{str(k):v for k,v in sorted(count.items())},'every_selector_word_weight':'p^7','accept_projector_expectation_lower':'2*p^7 for any report state when the untouched five selectors start product v^5','port_offdiagonal_absolute_lower':'> (12/25)*2*(309/500)^7 > 3/100','birth_layer_witness':'u=all canonical v; z=u with port v_perp. For any port birth position k among front-loaded births, Π_k z=z and Π_k u=0. Exact matrix element <u|W|z>=-sin(1024θ)*t, t>=2p^7, under completed R_load tensor I_port and untouched selector registers.','ST4_commutation_fails_for_every_frontloaded_birth_order':True,'all_births_before_A_no_intervening_gates_required':True,'not_a_proof_actual_full_heat_derivative_nonzero':True,'not_a_claim_about_interleaved_births_or_other_programs':True,'aux_addressed_cannot_be_declared_immutable_oldRIGHT':True,'tiny_clock_witness':'one-birth reflection clock has Tr(T)=-cos(2φ), not generically constant','physical_admission_or_C_proved':False,'GR_closed':False}
(P/'FRONTLOADED_PORT_ST4_OBSTRUCTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'count_distribution':out['SC6_report_event_pattern_counts'],'commutator_lower':'>3/100'}))
