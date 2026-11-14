#!/usr/bin/env python3
"""Exact fixed-point recurrence, coherent b-sectors and realification checks."""
from pathlib import Path
from fractions import Fraction as F
import json,math
import sympy as s
I=s.I;root=s.sqrt(3);t=(1+I*root)/2;assert s.simplify((t-1)**2+t)==0
c=s.Rational(3,5);v=s.Rational(4,5);eps=(1-c)/2;gamma=(1+c)/2;g=s.simplify(t*t+t*eps)
H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);id3=s.eye(3);Hb=s.kronecker_product(H,id3);j=s.Matrix([1,0,0,0,0,0]);P=j*j.T;Q=s.diag(1,1,1,0,0,0);Rstart=s.eye(6)+(t-1)*P;Rgood=s.eye(6)+(t-1)*Q
V0=s.Matrix([[c,-v,0],[v,c,0],[0,0,1]]);V1=s.Matrix([[c,0,-v],[0,1,0],[v,0,c]]);matches=0
for V in (V0,V1):
 assert V.T*V==id3 and V[0,0]==c
 CV=s.diag(id3,V);A0=Hb*CV*Hb;out=A0*j
 A1=A0*Rstart*A0.conjugate().T*Rgood*A0;new=A1*j
 assert all(s.simplify(x)==0 for x in Q*new-g*Q*out)
 assert all(s.simplify(x)==0 for x in (s.eye(6)-Q)*new-t*eps*(s.eye(6)-Q)*out)
 assert s.simplify((out.conjugate().T*Q*out)[0]-gamma)==0
 assert s.simplify((new.conjugate().T*(s.eye(6)-Q)*new)[0]-eps**3)==0
 matches+=1
# Shared scalar g is independent of the two b branches, so coherent SAM and
# arbitrary untouched external spectators extend by direct sum/tensor I.
# Exact scalar recurrence in Q(i sqrt(3)) for 8 levels, rational gamma.
def cmul(x,y):return (x[0]*y[0]-3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
e=F(1,5);e0=e;prod=(F(1),F(0))
for _ in range(8):
 factor=((e-1)/2,(1+e)/2);prod=cmul(prod,factor);e=e**3
 assert (1-e0)*(prod[0]**2+3*prod[1]**2)==1-e
assert e==F(1,5**6561)
# With high success after one level, failing to remove the common phase can
# leave a large rebit-1 component; probability-only amplification is not U.
uncorrected_imag=s.simplify(s.sqrt(gamma)*s.im(g));assert uncorrected_imag>s.Rational(9,10)
correction=s.conjugate(g)/s.sqrt(s.expand_complex(g*s.conjugate(g)));assert s.simplify(s.im(correction*g))==0 and s.simplify(s.re(correction*g))>0
# Physical realification: predicate acts as identity on rebit and phase is the
# complete real 2×2 rotation; both rebit columns are affected under P.
J=s.Matrix([[0,-1],[1,0]]);rot=s.eye(2)/2+root*J/2;assert rot.T*rot==s.eye(2)
control=s.diag(1,0);Qre=s.kronecker_product(control,rot)+s.kronecker_product(s.eye(2)-control,s.eye(2))
assert Qre[1,0]!=0 and Qre[0,1]!=0 and Qre[2:4,2:4]==s.eye(2)
out={'status':'PASS_EXACT_FIXED_POINT_AND_REALIFICATION','coherent_controlled_V_example_sectors':matches,'one_step_bad_amplitude_factor':'t epsilon','epsilon_recurrence':'epsilon_next=epsilon^3','exact_eight_step_rational_example':True,'good_amplitude_factor':'g=t^2+t epsilon','success_phase_same_across_SAM_if_c_constant':True,'rebit_correction_is_necessary':True,'uncorrected_rebit_one_component_gt':'9/10 in exact one-step example','phase_predicate_excludes_rebit':True,'scope':'exact fixed-point mathematics, not physical controlled Omega loader','GR_closed':False}
Path(__file__).with_name('FIXED_POINT_MATH_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
