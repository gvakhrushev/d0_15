#!/usr/bin/env python3
"""Rational bound for a local raw-u/log-link/Psi mean decoder at B25 cube.

Uses A30 operator-norm mark bounds and the pinned B21 chart envelope; does
not measure the mean, construct a physical reader, or assert source closure.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
from hashlib import sha256
import itertools,json,sympy as S
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');coordfile=O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl';envfile=O/'round21/CHART_ENVELOPE_RESULT.json';registryfile=D/'round30/SOURCE_RAW_MARK_REGISTRY.json';planfile=D/'round30/COMMON_SOURCE_MARKED_PLAN.json'
coords=[json.loads(line) for line in coordfile.read_text().splitlines()];env=json.loads(envfile.read_text());registry=json.loads(registryfile.read_text());assert len(coords)==2688 and [c['sam_index'] for c in coords]==list(range(2688)) and sha256(coordfile.read_bytes()).hexdigest()==env['coords_sha256']
counts=Counter(c['kind'] for c in coords);assert counts=={'coframe':1024,'proper_link':1536,'matter':128}
sites=defaultdict(Counter);links=defaultdict(set)
for c in coords:
 site=tuple(c['site']);sites[site][c['kind']]+=1
 if c['kind']=='proper_link':links[(site,c['role'])].add(tuple(c['generator']))
assert len(sites)==64 and all(v=={'coframe':16,'proper_link':24,'matter':2} for v in sites.values())
assert len(links)==256 and all(x==set(itertools.combinations(range(4),2)) for x in links.values())
# Null eta is an orthogonal involution. K_ab=eta(Eab-Eba) has norm 1;
# taking (eta K_cd)_ab reads coefficient delta_(ab,cd).
eta=S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]]);assert eta.T*eta==S.eye(4)
pairs=list(itertools.combinations(range(4),2));K=[]
for i,j in pairs:
 A=S.zeros(4);A[i,j]=1;A[j,i]=-1;Q=eta*A;K.append(Q);assert Q.T*Q==S.diag(*[int(t in (i,j)) for t in range(4)])
for row,(i,j) in enumerate(pairs):
 for col,Q in enumerate(K):assert (eta*Q)[i,j]==int(row==col)
# Rigorous rational majorants for exp and log series, using mean X=0.
s=F(1,2**30);e=F(1,2**3214);m=len(coords);x=6*s
assert 0<x<F(1,2)
mean_error=x*x/(1-x)+8*e # ||E exp(X)-I|| plus actual U-entry marks and ||U0^-1||<2
assert mean_error<s and mean_error/(1-mean_error)<2*s
assert x/(1-x)<7*s and 1/(1-x)<2
# ideal derivative Dexp-I <7s; Dlog-I <2s, Dexp<2:
# six coordinates per link -> each block row/column sum <6*(7s+4s).
geom=66*s
# Per U entry ||pullback difference||<e; commutator derivative ≤2e;
# 4x4 matrix spectral ≤4 max-entry, base inverse <2, Dlog<2,
# and 1/u<10/9 -> coefficient <40 e/s. Add m entries per row/column.
assert F(2)*F(309,500)*F(39,50)>F(9,10)
mark=m*40*e/s;delta=geom+mark;assert mark<F(1,2**3166) and delta<F(1,2**23)
assert F(52,1)/(2*F(309,500)*F(39,50)*(1-F(1,2**23)))<55
# Owner prefix mark bounds are actually stronger than assumed entry bound.
assert registry['original_mark_error_bounds']=={'inverse_coframe_u':'2^-3215','proper_link_U':'2^-3214','material_Psi':'2^-3223'}
# Exact one-coordinate rotation illustrates the mean decoder's nonlinearity.
# r²=1-2p³(1-cos s), Jnorm=sin(s)/(s*r²); its s² coefficient
# p³-1/6 is strictly positive, so even the ideal link Jacobian is not I.
assert F(309,500)**3 > F(1,6)
# Positive e=nu eta u^-T: creator columns <1, hence ||u||_F<2;
# ||D u / D e|| <= ||u||²/nu <20/3, in Frobenius matrix norm.
assert F(3,5)>0 and F(4,1)/F(3,5)==F(20,3)
paths=[coordfile,envfile,registryfile,planfile,O/'round25/targets.py']
out={'status':'PASS_CONDITIONAL_EXPLICIT_MEAN_DECODER_BOUND','chart_m':m,'interior_sites':64,'coordinate_counts':dict(counts),'link_blocks':len(links),'sampling_s':'2^-30','decoder':'u and Psi direct; theta_ab=(eta log(mean(U) U0^-1))_ab, a<b','pure_vertex_chart_exact_on_local_log_branch':True,'ideal_additive_u_Psi_Jacobian_exact_identity':True,'ideal_link_Jacobian_error_row_and_column_lt':'66*2^-30','single_rotation_exact_normalized_J':'sin(s)/(s*(1-2p^3*(1-cos(s))))','single_rotation_not_exact_identity':True,'entry_error_assumption':'each actual source U mark <2^-3214 in full SAM/old pullback operator norm','actual_joint_Jacobian_spectral_error_lt':'2^-23','Neumann_inverse_norm_l2_lt':'1/(1-2^-23)','normalized_SAM_lift_norm_lt':'55','physical_raw_coordinate_lift_norm_lt':'55*2^30','raw_u_from_physical_e_Frobenius_derivative_lt':'20/3','mean_link_log_at_reference_norm_lt':'2*((6s)^2/(1-6s)+8e)','actual_numeric_J_or_reader_executed':False,'original_mark_history_or_physical_comparison_admission_proved':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'GR_closed':False}
(P/'MEAN_DECODER_BOUND.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'m':m,'geom_bound_float':float(geom),'total_bound_float':float(delta),'inverse_norm':'<1/(1-2^-23)'}))
