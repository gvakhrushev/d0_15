#!/usr/bin/env python3
"""Exact counterexamples requiring half-vector, SAM-uniform and spectator domains."""
from fractions import Fraction as F
from pathlib import Path
import json,math
import sympy as s
I=s.eye(3);r=s.Matrix([1,0,0]);b=s.Matrix([s.Rational(3,5),s.Rational(4,5),0]);c=(r.T*b)[0];u=(r+b)/s.sqrt(2*(1+c))
R=lambda x:I-2*x*x.T
K=b*r.T-r*b.T;O=I+K+K*K/(1+c)
assert s.simplify(R(u)*R(r)-O)==s.zeros(3)
wrong=R(b)*R(r)*r-b; assert s.simplify((wrong.T*wrong)[0])==s.Rational(4,5)
# Private scratch counterexample and correct joint-anchor construction.
# Basis is (bank,work)=(00,01,10,11). U prepares u on |00>, but
# its action on |01> is arbitrary. Reflecting all work columns is wrong.
E=s.eye(4);e0=E[:,0];rotation=s.Matrix([[s.Rational(3,5),0,-s.Rational(4,5),0],[0,1,0,0],[s.Rational(4,5),0,s.Rational(3,5),0],[0,0,0,1]])
Pswap=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
Us=rotation*Pswap;embed=s.Matrix([[1,0],[0,0],[0,1],[0,0]])
r2=s.Matrix([1,0]);b2=s.Matrix([s.Rational(3,5),s.Rational(4,5)]);u2=(r2+b2)/s.sqrt(2*(1+b2[0]))
# Replace rotation angle to prepare the half vector, not the final b.
cs=u2[0];sn=u2[1];rotation=s.Matrix([[cs,0,-sn,0],[0,1,0,0],[sn,0,cs,0],[0,0,0,1]]);Us=rotation*Pswap
assert s.simplify(Us*e0-embed*u2)==s.zeros(4,1)
Rjoint=E-2*e0*e0.T;Rfull=E-2*s.diag(1,1,0,0)
R2=lambda x:s.eye(2)-2*x*x.T
trueO=R2(u2)*R2(r2)
assert s.simplify(Us*Rjoint*Us.T*Rjoint*embed-embed*trueO)==s.zeros(4,2)
assert s.simplify(Us*Rfull*Us.T*Rfull*embed-embed*trueO)!=s.zeros(4,2)
# One innocent external oldRIGHT=0 test is insufficient. Controlled U has
# correct anchor vector for F=0 and different anchor vector for F=1.
# Desired b=r => O=I; choose U_0=I, U_1=swap(0,1).
U0=I;U1=s.Matrix([[0,1,0],[1,0,0],[0,0,1]])
assert U0*r==r and U1*r!=r
W0=U0*R(r)*U0.T*R(r);W1=U1*R(r)*U1.T*R(r)
assert W0==I and W1!=I and W1[0,0]==-1
# All-but-one SAM branches can pass an average check while failing worst-case.
# Uniform 2^2688 vertices with only one bad branch have squared average 2^-2688;
# the control-block operator norm still equals one (bad block difference I).
assert F(1,2**2688)<F(1,2**2600)
actual_c=1/math.sqrt(32*2049);wrong_norm=math.sqrt(2*(1-actual_c));assert wrong_norm>1
out={'status':'PASS_EXACT_REDUCTION_HOSTILE_EXAMPLES','half_vector_identity_exact':True,'using_omega_itself_instead_of_half_vector_squared_error_exact':'4/5 for c=3/5','actual_choi_wrong_omega_instead_of_u_error_norm':wrong_norm,'joint_private_clean_anchor_gives_correct_all_data_columns':True,'naive_anchor_tensor_I_private_work_fails_on_clean_data_column':True,'one_oldRIGHT_column_passes_but_other_fails':True,'sam_average_one_bad_vertex_squared_error':'2^-2688 with worst_case_block_error=1','scope':'explicit finite counterexamples; no claim that A16 or a future U exhibits these failures','GR_closed':False}
Path(__file__).with_name('REDUCTION_HOSTILES_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
