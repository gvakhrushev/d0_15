#!/usr/bin/env python3
"""Check the original Cartesian reference under its null-frame transport.
Uses A11's scalar DAG only; no native bank or factory execution.
"""
from pathlib import Path
from fractions import Fraction
import importlib.util,sys,json,math
import numpy as np
import sympy as sp
P=Path(__file__).resolve().parent; B=P.parent/'round21'
src=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round11')
spc=importlib.util.spec_from_file_location('a11_dag_review',src/'source_operator_dag.py');mod=importlib.util.module_from_spec(spc);sys.modules[spc.name]=mod;spc.loader.exec_module(mod)
dag=json.loads((src/'SOURCE_TENSOR_DAG.json').read_text());r2=sp.sqrt(2)/2
T=sp.Matrix([[r2,r2,0,0],[r2,-r2,0,0],[0,0,1,0],[0,0,0,-1]])
cart=sp.diag(1,-1,-1,-1);null=sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
assert T.T*T==sp.eye(4) and T.det()==1 and T*cart*T.T==null
h=Fraction(1,4);t=h/2;v=h/20;ca=(1+t*t)/(1-t*t);sa=2*t/(1-t*t);cb=(1-v*v)/(1+v*v);sb=2*v/(1+v*v)
q=lambda x:sp.Rational(x.numerator,x.denominator)
A=sp.eye(4);A[0,0]=A[2,2]=q(ca);A[0,2]=A[2,0]=q(sa)
Bmat=sp.eye(4);Bmat[1,1]=Bmat[2,2]=q(cb);Bmat[1,2]=q(sb);Bmat[2,1]=-q(sb)
An=sp.simplify(T*A*T.T);Bn=sp.simplify(T*Bmat*T.T)
assert sp.simplify(An.T*null*An-null)==sp.zeros(4) and sp.simplify(Bn.T*null*Bn-null)==sp.zeros(4)
assert An.det()==1 and Bn.det()==1
# u_ref=nu sqrt(rho)/s_ref T eta_cart; its Role metric is diagonal Cartesian.
nu=sp.Rational(3,5);sref=sp.Integer(6);rho=sp.Rational(1)
u=nu*sp.sqrt(rho)/sref*T*cart
assert sp.simplify(u.T*null*u/nu**2-rho/sref**2*cart)==sp.zeros(4)
# Evaluate complete 16-CAR/R2 scalar DAG on the true transported reference fields.
meta=json.loads((B/'REFERENCE_METADATA.json').read_text());k0=float(meta['k0_original']);Fh=float(Fraction(meta['F_h_rational']));dh=Fh/(36*k0)
p=(math.sqrt(5)-1)/2; amp=.25*6*math.sqrt(dh)/2
U=np.array(u,dtype=float); I=np.eye(4); AA=np.array(An,dtype=float); BB=np.array(Bn,dtype=float)
def calc(l1,matter_axis=None):
 matrices=[AA,l1,I,I] if l1 is not None else [I,I,I,I]
 v={}
 for r in range(4):
  for i in range(4):v[f'u/{r}/{i}']=U[i,r]
 for key in dag['link_nodes']:
  loc,r=key.split('/');r=int(r)
  for i in range(4):
   for j in range(4):v[f'M/{loc}/{r}/{i}/{j}']=matrices[r][i,j]
 for loc in ['base']+[f'plus{r}' for r in range(4)]:
  for grade in (0,15):
   psi=0. if grade==15 or matter_axis is None else (-amp if loc==f'plus{matter_axis}' else amp)
   v[f'X/{loc}/{grade}']=2*math.sqrt(p)*psi/256
 return {k:value['value'] for k,value in mod.evaluate(dag,v,p).items()}
plus=calc(BB);minus=calc(BB.T);time=calc(None,0);space=calc(None,1)
fp=plus['H_f_before_inverse_PF'];fm=minus['H_f_before_inverse_PF'];qt=time['H_q_before_inverse_PF'];qs=space['H_q_before_inverse_PF']
assert abs(fp-Fh/36)<1e-12 and abs(fm+Fh/36)<1e-12,(fp,fm,Fh/36)
assert abs(qt-dh)<1e-12 and abs(qs+dh)<1e-12,(qt,qs,dh)
res={'status':'PASS_EXACT_FRAME_TRANSPORT_AND_NUMERIC_A11_REFERENCE','det_T':str(T.det()),'T_eta_cart_Tt_equals_eta_null':True,
 'role_metric':'rho/s_ref² diag(1,-1,-1,-1)','boost_rotation_transported_to_null_proper_lorentz':True,
 'F_h':str(Fraction(meta['F_h_rational'])),'f_plus_float':fp,'f_minus_float':fm,'expected_f_plus_float':Fh/36,
 'q_time_float':qt,'q_space_float':qs,'expected_q_time_float':dh,
 'dag':'A11 source_operator_dag; concrete reference scalar diagnostic, not native writer', 'GR_closed':False}
(P/'REFERENCE_FRAME_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
