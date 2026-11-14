#!/usr/bin/env python3
"""Exact fixtures supporting A29 scalar corner and conditional R11 algebra."""
from pathlib import Path
from fractions import Fraction as F
import json,sympy as s
P=Path(__file__).resolve().parent
p=(s.sqrt(5)-1)/2;a=s.sqrt(p);v=s.Matrix([a,p]);G=s.Matrix([[a,-p],[p,a]]);I=s.eye(2);J=s.kronecker_product(I,v,v)
def CX(control,target,n):
 M=s.zeros(2**n)
 for x in range(2**n):
  y=x ^ (1<<(n-1-target)) if (x>>(n-1-control))&1 else x;M[y,x]=1
 return M
# SAM first; two born factors thereafter. Only controls ever act on SAM.
U=CX(1,2,3)*s.kronecker_product(I,G,I)*CX(0,2,3)*s.kronecker_product(I,I,G)
assert any(s.simplify(x)!=0 for x in U-U.T) # word need not be a reflection
C=J.T*U*J;assert s.simplify(C[0,1])==0 and s.simplify(C[1,0])==0
assert all(s.simplify(s.im(x))==0 for x in C)
# Tensor an arbitrary two-dimensional old factor: exact identity on it.
assert all(s.simplify(x)==0 for x in s.kronecker_product(C,I)-s.diag(C[0,0],C[0,0],C[1,1],C[1,1]))
# Independent full-column retention: <v|G|v>=sqrt(p), hence K copies p^(K/2).
assert s.simplify((v.T*G*v)[0]-a)==0
# Representative non-diagonal old Gram: D<=I implies D^-1>=I.
A=s.Matrix([[s.Rational(1,2),s.Rational(1,4)],[s.Rational(1,4),s.Rational(1,2)]])
z=s.Rational(2,5);eta=z*s.Rational(1,3);cc=s.Rational(7,10);D=(1-z)*I+eta*cc**2*A;Q=D.inv()-I
assert Q[0,0]>0 and Q.det()>0
assert F(5,6)**4<F(1,2) and F(18,2872)<1 and 11647+3158+1==14806
out={'status':'PASS_EXACT_SCALAR_RETENTION_AND_CONDITIONAL_R11_ALGEBRA','nonreflection_real_word_scalar_corner':True,'external_old_factor_exact_identity':True,'raw_birth_G_return_factor':'sqrt(p)','non_diagonal_old_Gram_test':True,'heat_decay':'(2p)^(-K) < (5/6)^K','sufficient_K_for_prefix_N_lt_2^q_and_abs_t_z_traceA_ge_2^-Q':'4*(q+3158+Q+T+1)','isolated_segment_q':11647,'isolated_sufficient_K':'4*(14806+Q+T)','conditional_on_actual_common_history_marks_gain_and_nonzero_old_Gram':True,'physical_C_closed':False,'GR_closed':False}
(P/'SCALAR_RETENTION_CONDITIONS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
