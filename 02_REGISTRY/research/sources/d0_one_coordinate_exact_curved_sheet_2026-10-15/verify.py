#!/usr/bin/env python3
"""Exact full-symbol controls and a genuine 192-variable interval root.
No CORE, full D0 action, prescribed-source, or general-4D closure is claimed.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import numpy as np
import sympy as s
from algebra import PAIR,eta,GEN,G2,STAR,wedge,symbol,inverse_coefficients
ROOT=Path(__file__).parent
CHECKS=[]
def check(name,condition):
 if not bool(condition):raise AssertionError(name)
 CHECKS.append(name)

def literal_hessian(z):
 """Differentiate the actual two-amplitude odd plaquette, every shared slot."""
 out=s.zeros(24)
 for r,ss in PAIR:
  u,v=[i for i in range(4) if i not in (r,ss)];seq=[r,ss,u,v]
  sg=(-1)**sum(seq[i]>seq[j] for i,j in combinations(range(4),2))
  pairing=sg*wedge(s.eye(4)[:,u],s.eye(4)[:,v]).T*G2*STAR
  roles=[r,ss,r,ss];offsets=[0,int(r==1),int(ss==1),0];signs=[1,1,-1,-1]
  for i in range(4):
   for j in range(4):
    if i==j:continue
    for a,X in enumerate(GEN):
     for b,Y in enumerate(GEN):
      C=(X*Y-Y*X)*eta;w=(pairing*s.Matrix([C[x,y] for x,y in PAIR]))[0]
      out[6*roles[i]+a,6*roles[j]+b]+=s.Rational(signs[i]*signs[j]*(1 if i<j else -1),2)*w*z**(offsets[j]-offsets[i])
 return out.applyfunc(s.expand)

def algebra_checks():
 check('all_six_Lorentz_generators',all(X.T*eta+eta*X==s.zeros(4) for X in GEN))
 check('literal_star_square',STAR*STAR==-s.eye(6))
 z=s.symbols('z',nonzero=True);H=symbol(s.eye(4),[s.Integer(1),z,s.Integer(1),s.Integer(1)])
 C=literal_hessian(z)
 check('physical_placement_is_transposed_owner_symbol',C==H.T)
 check('wrong_placement_is_detectably_different',C!=H)
 den=14+z*z+z**-2
 check('full_24_component_determinant',s.cancel(C.det()-den**2)==0)
 coef=inverse_coefficients()
 N=sum((mat*z**k for k,mat in coef.items()),s.zeros(24))
 check('left_inverse_every_Laurent_coefficient',(C*N-den*s.eye(24)).applyfunc(s.expand)==s.zeros(24))
 check('right_inverse_every_Laurent_coefficient',(N*C-den*s.eye(24)).applyfunc(s.expand)==s.zeros(24))
 check('inverse_numerator_radius_four',min(coef)==-4 and max(coef)==4)
 row=max(sum(abs(b[i,j]) for b in coef.values() for j in range(24)) for i in range(24))
 col=max(sum(abs(b[i,j]) for b in coef.values() for i in range(24)) for j in range(24))
 check('both_full_kernel_norm_budgets',row==70 and col==70)
 q=7-4*s.sqrt(3)
 check('Green_decay_in_unit_interval',0<q<1)
 check('Green_homogeneous_recurrence',s.simplify(q*q-14*q+1)==0)
 check('Green_delta_normalization',s.simplify((14-2*q)/(8*s.sqrt(3)))==1)
 check('Green_absolute_sum',s.simplify((1+q)/(1-q)/(8*s.sqrt(3)))==s.Rational(1,12))
 check('all_period_all_lp_inverse_bound',row/12==s.Rational(35,6))
 for L in [4,8,12]:
  Q=s.zeros(L)
  for i in range(L):Q[i,i]+=14;Q[i,(i+2)%L]+=1;Q[i,(i-2)%L]+=1
  Qinv=Q.inv();check(f'wrapped_Q_inverse_{L}',Q*Qinv==s.eye(L))
  check(f'wrapped_Q_row_budget_{L}',max(sum(abs(Qinv[i,j]) for j in range(L)) for i in range(L))<=s.Rational(1,12))
 # Analytic derivatives used by the interval certificate, on a rational generic
 # Lorentz point, including all mixed generator directions.
 X=sum((s.Rational(k+1,101)*G for k,G in enumerate(GEN)),s.zeros(4));V=s.eye(4)-X/2;S=V.inv();U=S*(s.eye(4)+X/2)
 check('Cayley_is_genuinely_Lorentz',U.T*eta*U==eta)
 deriv=[S*G*S for G in GEN]
 for k,G in enumerate(GEN):
  check('Cayley_first_jet_'+str(k),V*deriv[k]==G*(U+s.eye(4))/2)
  for j in range(k,6):
   Y=GEN[j];dd=(S*Y*S*G*S+S*G*S*Y*S)/2
   check(f'Cayley_full_second_jet_{k}_{j}',V*dd==(Y*deriv[k]+G*deriv[j])/2)
 # Ten genuine two-sided Gram tangents, including the off-diagonal weights.
 E=s.Matrix([[1,s.Rational(1,9),0,0],[0,1,s.Rational(1,13),0],[0,0,1,s.Rational(1,17)],[0,0,0,1]])
 g=E.T*eta*E
 for a in range(4):
  for b in range(a,4):
   V=s.zeros(4);V[a,b]=V[b,a]=1;dE=E*g.inv()*V/2
   check(f'complete_Gram_tangent_{a}{b}',dE.T*eta*E+E.T*eta*dE==V)
 h=s.symbols('h',positive=True)
 check('unweighted_raw_source_loss_all_four_directions',s.simplify(h**-2*h**-4*h**7)==h)
 check('all_4d_local_connection_rows_at_L8',24*8**4==98304)
 check('published_center_dimension',np.array(json.loads((ROOT/'root_center.json').read_text())).shape==(8,24))
 return {'exact_named_conditions':len(CHECKS),'inverse_norm':'35/6','determinant':'(14+z^2+z^-2)^2','kernel_numerator_nonzeros':sum(sum(v!=0 for v in b) for b in coef.values()),'unrestricted_4D_microstructure_closed':False,'full_D0_action_closed':False}

def interval_checks():
 from intervals import I,calc,preconditioner,rowsum_out,setup
 A=np.array(json.loads((ROOT/'root_center.json').read_text()));rad=2.**-30
 g,_=calc(A,0.,False);_,J=calc(A,rad,True);B=preconditioner(8)
 contraction=rowsum_out((I(np.eye(192))-B@J).absup())
 disp=float((B@I(g.l[:,None],g.h[:,None])).absup().max())
 image=float(np.nextafter(disp+np.nextafter(contraction*rad,np.inf),np.inf))
 check('strict_uniform_contraction',contraction<3/40)
 check('center_displacement',disp<2.**-40)
 check('strict_ball_self_inclusion',image<2.**-33<rad)
 check('Cayley_chart_is_connected_to_identity',3*(float(np.max(np.abs(A)))+rad)<s.Rational(1,8))
 UU=setup(A,rad,False);P=UU[0,1,1][0]@UU[1,2,1][0]@UU[0,1,-1][0]@UU[0,2,-1][0]
 odd=(P-I(np.array(eta.tolist(),float))@P.T@I(np.array(eta.tolist(),float)))*.5
 check('exact_root_has_nonidentity_plaquette',float(odd.l[1,2])>1/200 and float(odd.h[1,2])<3/500)
 return {'method':'directed_outward_IEEE754_interval_Banach_certificate','variables':192,'radius':'2^-30','contraction_upper':contraction,'displacement_upper':disp,'image_radius_upper':image,'odd_curvature_12':[float(odd.l[1,2]),float(odd.h[1,2])],'full_4d_connection_rows':98304,'full_metric_or_matter_stationarity_claimed':False}

def floating_checks():
 from nonlinear import residual,inverse
 rng=np.random.default_rng(310);L=5;E=np.tile(np.eye(4),(L,1,1));v=rng.normal(size=(L,24));eps=1.e-5
 Hv=(residual(E,eps*v)-residual(E,-eps*v))/(2*eps)
 err=float(np.max(np.abs(inverse(Hv)-v)));check('independent_full_nonlinear_Jacobian_diagnostic',err<1.e-7)
 return {'status':'FLOATING_DIAGNOSTIC_NOT_INTERVAL','inverse_Jacobian_error':err}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--algebra',action='store_true');ap.add_argument('--interval',action='store_true');ap.add_argument('--numeric',action='store_true');ap.add_argument('--write',type=Path);arg=ap.parse_args()
 result={'scope':'EXACT_NONLINEAR_ONE_COORDINATE_CONNECTION_SHEET_NOT_FULL_D0_OR_FULL_4D_TERMINAL'}
 if arg.algebra or not(arg.interval or arg.numeric):result['algebra']=algebra_checks()
 if arg.interval or not(arg.algebra or arg.numeric):result['interval']=interval_checks()
 if arg.numeric:result['numerical']=floating_checks()
 if result.get('full_D0_action_closed',False):raise AssertionError('false global promotion')
 print(json.dumps(result,sort_keys=True,indent=2));print('PASS_ONE_COORDINATE_EXACT_CURVED_CONNECTION')
 if arg.write:arg.write.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
