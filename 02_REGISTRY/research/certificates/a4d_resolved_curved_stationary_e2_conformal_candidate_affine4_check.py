#!/usr/bin/env python3
"""Actual affine-order-four no-go for the low-order conformal candidate.

Allows all solder-compatible second amplitudes, arbitrary next translations,
and the two free action coefficients p,q (q!=0) left by the leading balance.
The leading Fourier translation is b0=e0/(256*q), b2=b3=e0, parity 1100.
Two necessary affine rows cannot vanish simultaneously. No new channel,
coefficient selector, finite witness, or whole-support no-go is asserted.
"""
from __future__ import annotations
import ast,contextlib,importlib.util,io,types
from pathlib import Path
from itertools import permutations
import sympy as sp

def check(name,c):
 if not c:raise AssertionError(name)
 print('PASS_'+name,flush=True)
here=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('candidate',here/'a4d_resolved_curved_stationary_e2_conformal_candidate_jet_check.py');owner=importlib.util.module_from_spec(s)
with contextlib.redirect_stdout(io.StringIO()):s.loader.exec_module(owner)
o=owner.o;I=sp.eye(4);Z=sp.zeros(4);v=owner.v;signs=owner.signs
# Reuse the owned third-jet function definitions directly; their unrelated
# old-Newton-line certificate does not need to execute a second time.
tree=ast.parse((here/'a4d_resolved_curved_stationary_e2_support7_affine_order3_check.py').read_text())
order=next(node.value.value for node in tree.body if isinstance(node,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='ORDER'for t in node.targets))
check('OWNED_THIRD_JET_ORDER_FOUR',order==4)
ns={'sp':sp,'Matrix':sp.Matrix,'zeros':sp.zeros,'eye':sp.eye,'I4':I,'Z4':Z,'ORDER':order,'permutations':permutations}
funcs=[node for node in tree.body if isinstance(node,ast.FunctionDef)and node.name in ('jet_add','jet_neg','jet_mul','jet_inv','scalar_jet_mul','det_jet','adj_jet','scalar_matrix_jet_mul','cayley_jet')]
exec(compile(ast.Module(body=funcs,type_ignores=[]),'<owned-third-jet-functions>','exec'),ns)
j=types.SimpleNamespace(**{node.name:ns[node.name]for node in funcs})
check('THIRD_JET_SPECIALIZES_TO_OWNED_SECOND_JET',all(j.cayley_jet(a,h)[:3]==owner.j.cayley_jet(a,h)for a,h in zip(o.generators0,v)))
B=[]
for r in range(4):
 b=sp.zeros(4,16);b[:,4*r:4*r+4]=sp.eye(4);B.append(b)
def jc(m):return [m,sp.zeros(*m.shape),sp.zeros(*m.shape),sp.zeros(*m.shape)]
def residual_maps(X):
 U=[j.jet_mul([I+a/2,h/2,x/2,Z],j.jet_inv([I-a/2,-h/2,-x/2,Z]))for a,h,x in zip(o.generators0,v,X)];Ui=[j.jet_inv(u)for u in U];F={};tr={}
 for r,s in o.PAIRS:
  P=j.jet_mul(j.jet_mul(j.jet_mul(U[r],U[s]),Ui[r]),Ui[s]);M=j.jet_add(jc(I),j.jet_neg(P))
  F[r,s]=(P,M,j.det_jet(M),j.adj_jet(M))
  aa=j.jet_add(jc(B[r]),j.jet_mul(U[r],jc(signs[r]*B[s])));bb=j.jet_add(jc(B[s]),j.jet_mul(U[s],jc(signs[s]*B[r])))
  tr[r,s]=j.jet_add(aa,j.jet_neg(j.jet_mul(P,bb)))
 R={}
 for ff in o.PAIRS:
  _,M,D,A=F[ff]
  for gg in o.PAIRS:
   if ff==gg:continue
   R[ff,gg]=j.jet_add(j.scalar_matrix_jet_mul(D,tr[gg]),j.jet_neg(j.jet_mul(j.jet_mul(F[gg][1],A),tr[ff])))
   assert R[ff,gg][0]==sp.zeros(4,16)
 return R
p,q=sp.symbols('p q');Gamma=-sp.Rational(1,1024)
coef=(Gamma/2+p,Gamma/2-p,q,-q);beta=sp.zeros(16,1);beta[0]=1/(256*q);beta[8]=beta[12]=1
R0=residual_maps([Z]*4)
Q2=sp.zeros(16);Q3=sp.zeros(16)
for fg,R in R0.items():
 ff,gg=fg;cls=0 if len(set(ff)&set(gg))==1 else 1
 for kind,metric in enumerate((o.ETA,I)):
  c=coef[2*kind+cls];Q2+=16*c*R[1].T*metric*R[1];Q3+=16*c*(R[1].T*metric*R[2]+R[2].T*metric*R[1])
check('ALL_PARAMETER_MODE_AFFINE_LOWER_FORMS_ZERO',Q2.applyfunc(sp.cancel)==Q3.applyfunc(sp.cancel)==sp.zeros(16))
# Recheck all leading link rows for this full coefficient family, rather
# than treating the fixed coefficient point as a selector.
bvec=[sp.eye(4)[:,0]/(256*q),sp.zeros(4,1),sp.eye(4)[:,0],sp.eye(4)[:,0]]
Rv=owner.residuals(owner.kin(v),bvec)
for row,(role,g)in enumerate(owner.f.TESTS):
 w=[g if i==role else Z for i in range(4)];Rw=owner.residuals(owner.kin(w),bvec);Rm=owner.residuals(owner.kin(owner.add(v,w)),bvec);ch=0
 for fg,R in Rv.items():
  ff,gg=fg;cls=0 if len(set(ff)&set(gg))==1 else 1;r1,r2=R[1:];mix=Rm[fg][2]-r2-Rw[fg][2]
  for kind,metric in enumerate((o.ETA,I)):
   ch+=32*coef[2*kind+cls]*((r2.T*metric*Rw[fg][1])[0]+(r1.T*metric*mix)[0])
 check(f'PARAMETRIC_LEADING_LINK_ROW_{row}',sp.cancel(owner.estar[row]+ch)==0)

def affine4(R):
 H=[sp.zeros(16)for _ in range(4)]
 for fg,V in R.items():
  ff,gg=fg;cls=0 if len(set(ff)&set(gg))==1 else 1
  for kind,metric in enumerate((o.ETA,I)):
   H[2*kind+cls]+=16*sum((V[i].T*metric*V[4-i]for i in (1,2,3)),sp.zeros(16))
 return (2*sum((c*M for c,M in zip(coef,H)),sp.zeros(16))*beta).applyfunc(sp.cancel)
E0=affine4(R0);cols=[]
for k,(_,role,g)in enumerate(o.SELECTED_SPECS):
 X=[g if i==role else Z for i in range(4)];cols.append(affine4(residual_maps(X))-E0)
 print('SECOND_AMPLITUDE_COLUMN_CHECKED',k,flush=True)
A=sp.Matrix.hstack(*cols).applyfunc(sp.cancel)
# EL4 is linear in the second amplitudes: possible quadratic terms are
# the identically zero combined channel Q2 at this seed (owned joint gate).
# Next translations in parity 1100 act through Q3=0; other Fourier modes
# cannot repair this mode of a translation-invariant affine operator.
Na=owner.kernel[10:,:];Ka=sp.Matrix.hstack(*Na.columnspace());xa=owner.part[10:,:]
check('SECOND_AMPLITUDE_PROJECTION_DIMENSION_FOUR',Ka.shape==(7,4))
check('EVERY_SOLDER_COMPATIBLE_SECOND_AMPLITUDE_DROPS_OUT_OF_AFFINE4', (A*Ka).applyfunc(sp.cancel)==sp.zeros(16,4))
source=(q*(E0+A*xa)).applyfunc(sp.cancel)
check('AFFINE4_COMPONENT_TWO_EXACT',sp.expand(source[2]-32*q*(1024*q-1))==0)
check('AFFINE4_COMPONENT_THREE_EXACT',sp.expand(source[3]+32*q*(25600*q-1)/5)==0)
check('EXACT_POLYNOMIAL_COKERNEL_OBSTRUCTION_768_Q',sp.expand(-5*source[3]-25*source[2]-768*q)==0)
print('EXACT_RESULT: q!=0 is required by the leading translation balance; two actual affine EL4 rows require 1024*q=1 and 25600*q=1. Their polynomial combination is 768*q!=0.',flush=True)
print('VERDICT: declared conformal candidate and its full two-coefficient family blocked at necessary affine order four, for every second correction and next translation.',flush=True)
print('SCOPE: this reconstruction only; the general conformal critical-solder locus and finite seven-amplitude configurations remain open. No finite vacuum or hostile L3 result.',flush=True)
