#!/usr/bin/env python3
"""Exact all-column NPS invalid guard and both conditional placements."""
import contextlib, io, json, runpy
from pathlib import Path
import sympy as s
root=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()): base=runpy.run_path(str(root/'round6/check_backward.py'))
nt=base['nt'];p=nt.P;a=nt.A;G=nt.G_LOCAL; F=nt.GOLDEN_FIELD
I=s.eye(2);Z=s.zeros(2);v=s.Matrix([a,p]);Pr0=s.diag(1,0);Pr1=s.diag(0,1);Pt0=Pr0;Pt1=Pr1
k=s.kronecker_product; B=G**2
E=k(Pr0,G,I)+k(Pr1,G.T,I)
Ra=k(Pr0,I,I)+k(Pr1,I,B)
Rs=k(Pr0,I,I)+k(Pr1,Pt0,B)+k(Pr1,Pt1,I)
J=k(I,v,I);P0=k(Pr0,I,I);P1=k(Pr1,Pt0,I);Pbad=k(Pr1,Pt1,I)
checks=[]
def need(c,n):
 if not bool(c):raise AssertionError(n)
 checks.append(n)
def eq(A,B):
 A=s.Matrix(A);B=s.Matrix(B)
 return A.shape==B.shape and all(F.from_sympy(s.expand(x))==F.zero for x in A-B)
need(eq(E.T*E,s.eye(8)),'actual E0 is unitary')
need(eq(Ra.T*Ra,s.eye(8)) and eq(Rs.T*Rs,s.eye(8)),'both recoveries all-column unitary')
need(eq(E*Ra,Ra*E),'r-only recovery commutes with E0 on all columns')
need(not eq(Pbad*Ra*Pbad,Pbad),'r-only recovery acts nontrivially on invalid columns')
need(eq(Pbad*E*J,s.zeros(8,4)),'original initialized invalid branch vanishes')
need(eq(Pbad*E*Ra*J,s.zeros(8,4)),'r-only recovery before encoder preserves exact no-11')
need(eq(Pbad*Rs,Pbad),'LC10-style supported recovery is identity on invalid')
need(not eq(E*Rs,Rs*E),'identity-invalid recovery does not commute with E0 in general')
expected=s.zeros(8,4);expected[6:8,2:4]=a*p*(I-B)
need(eq(Pbad*E*Rs*J,expected),'premature supported recovery creates exact ap(I-R1) invalid amplitude')
need(not eq(expected,s.zeros(8,4)),'premature insertion is a strict hostile control')
need(eq(Pbad*Rs*E*J,s.zeros(8,4)),'supported recovery after E0 preserves no-11')
for label,P in [('zero',P0),('one',P1),('invalid',Pbad)]:
 need(eq(J.T*E.T*Rs.T*P*Rs*E*J,J.T*E.T*P*E*J),'after-encoder supported recovery preserves '+label+' effect')
L0=s.eye(8);L1=k(Pr0,G**2,I)+k(Pr1,I,I)
need(eq(Rs*L0,L0*Rs) and eq(Rs*L1,L1*Rs),'selected supported recovery commutes with L0,L1 endpoints')
# A later t rotation can mix r1t0/r1t1; do not infer all-column commutation.
T=k(I,G.T**2,I)
need(not eq(T*Rs,Rs*T),'later t rotation does not commute on all dirty columns')
# A branch-zero-only bank recovery is the particularly useful overlap case:
# it is BOTH r-only and identity on the entire invalid r1,t1 sector.
Rzero=k(Pr0,I,B)+k(Pr1,I,I)
need(eq(Rzero.T*Rzero,s.eye(8)),'branch-zero recovery unitary')
need(eq(E*Rzero,Rzero*E),'branch-zero recovery commutes with E0 all columns')
need(eq(Pbad*Rzero,Pbad),'branch-zero recovery fixes invalid exactly')
need(eq(Pbad*E*Rzero*J,s.zeros(8,4)),'branch-zero recovery preserves original initialized invalid guard')
# Analytic local-row control for normalized V0,V1 with 0<xi<1.
# Equal positive weights and xi=3/5 have an explicit top eigenvector.
V0=s.Matrix([1,0]);V1=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
chi=(V0+V1)/s.sqrt(s.Rational(16,5))
x0=(chi.T*V0)[0]; zeta=(chi-x0*V0)/s.sqrt(1-x0*x0)
need(s.simplify((chi.T*chi)[0]-1)==0,'common eigenframe normalized')
need(s.simplify(x0*x0-s.Rational(4,5))==0,'common eigenframe strictly overlaps V0')
need(s.simplify(2*x0*(chi.T*zeta)[0]-s.Rational(4,5))==0,'branch-zero local dh is strictly positive')
print(json.dumps({'status':'PASS','checks':len(checks),'exact_field':'Q(sqrt(p))',
'actual_r_only_macro_nontrivial_invalid':True,'selected_LC10_invalid_identity':True,
'bad_placement_invalid_amplitude':'a*p*(I-R1)',
'branch_zero_recovers_and_fixes_invalid':True,
'common_eigenframe_local_dh_fixture':'4/5',
'full_H1_recovery_word_emitted':False,'physical_cost_info_binding_proved':False,
'GR_closed':False},indent=2,sort_keys=True))
