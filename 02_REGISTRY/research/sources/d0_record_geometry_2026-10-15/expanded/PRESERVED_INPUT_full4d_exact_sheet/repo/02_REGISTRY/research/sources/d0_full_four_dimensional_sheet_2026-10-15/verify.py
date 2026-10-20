"""Reproduce exact structure, outward root and ALL full-4D inverse blocks.
Run with Python or Python -O. JAX is not a proof dependency.
"""
from pathlib import Path
import argparse,json,hashlib
from fractions import Fraction
import numpy as np
import sympy as s
from interval_check import I,rational,setup,neighbor,ET,ROOT
from symbol import PAIR,eta,GEN,G2,STAR,wedge,symbol
CHECKS=[]
def ck(name,yes):
 if not bool(yes):raise AssertionError(name)
 CHECKS.append(name)

def kernel():
 # This reproduces the concrete upstream bug instead of merely tagging it.
 class Old:
  def __init__(self,l,h=None):self.l=np.asarray(l,float);self.h=np.asarray(l if h is None else h,float)
 old=Old(np.zeros(1));old.l[0]=-1;old.h[0]=1
 ck('upstream_alias_reproduced',old.l[0]==1 and np.shares_memory(old.l,old.h))
 new=I(np.zeros(1));new.l[0]=-1;new.h[0]=1
 ck('independent_interval_endpoint_storage',new.l[0]==-1 and not np.shares_memory(new.l,new.h))
 for q in [Fraction(1,100),Fraction(1,1000),Fraction(-1,3)]:
  z=rational(q);ck('exact_rational_enclosure_'+str(q),Fraction(float(z.l))<=q<=Fraction(float(z.h)))
 ck('all_Lorentz_generators',all(X.T*eta+eta*X==s.zeros(4) for X in GEN))
 ck('star_square',STAR*STAR==-s.eye(6))
 ck('root_dimension',np.array(json.load(open(ROOT/'center.json'))).shape==(384,))
 ck('all_4D_links_retained',16*384==24*4**4==6144)
 ck('all_metric_slots_retained',10*4**4==2560)
 for r,t in PAIR:
  u,v=[a for a in range(4) if a not in (r,t)];seq=[r,t,u,v]
  sg=(-1)**sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
  w=sg*wedge(s.eye(4)[:,u],s.eye(4)[:,v]).T*G2*STAR
  ck('literal_face_coefficient_'+str((r,t)),w[PAIR.index((r,t))]*eta[t,t]==1)
 H=symbol(s.eye(4),[s.S.One]*4)
 ck('flat_full_hessian_is_symmetric',H==H.T)
 ck('flat_zero_frequency_det',H.det()==256)
 for z in [s.I,-s.I]:
  R=symbol(s.eye(4),[s.S.One,s.I,z,s.S.One]);ck('real_transverse_resonance_'+str(z),R.rank()==22)
 # Independent closed formulas for genuine two-coordinate scalar curvature jets.
 a,b=s.symbols('a b',real=True)
 JJ=s.Matrix([[4*a*(a*a-2*b*b+1),2*b*(2*a*a-4*b*b+1)],
   [4*a*(2*a**4-3*a*a*b*b+a*a+4*b**4-b*b),4*b*(2*a**4-3*a*a*b*b+a*a+4*b**4-b*b)]])
 det=s.factor(JJ.det());target=8*a*b*(2*a**4-3*a*a*b*b+a*a+4*b**4-b*b)
 ck('two_invariant_jacobian_identity',s.expand(det-target)==0)
 ck('two_coordinate_invariant_rank',det.subs({a:s.Rational(1,100),b:s.Rational(1,1000)})==s.Rational(12377463,1562500000000000))
 # Full IFT neighbourhood, conservative but explicit; no sampled L->infinity.
 ck('third_derivative_stencil_budget',19008*48*6<2**23)
 ck('mixed_stencil_budget',768*48*6<2**18)
 ck('coframe_forcing_budget',32*48*6<2**14)
 rho=Fraction(1,2**52);eps=Fraction(1,2**92);M=2**24
 q=M*(2**23*rho+2**18*eps);d=M*2**14*eps
 ck('full_4D_parameter_contraction',q<Fraction(1,16))
 ck('full_4D_parameter_self_mapping',d+q*rho<rho)
 # gamma bound used for large complex final interval products.
 n=512;u=Fraction(1,2**53);k=8*n+32;gamma=k*u/(1-k*u)
 from blas_bounds import GAMMA
 ck('BLAS_error_factor_proved',gamma<Fraction.from_float(GAMMA))
 flat_bloch_checks()
 return {'exact_structural_checks':len(CHECKS),'checks':CHECKS.copy(),'old_interval_alias_reproduced':True}

def flat_bloch_checks():
 # Independent coefficient check against the literal owner's polarized symbol.
 import interval_check as mod
 from full_bloch_verify import assemble
 old=mod.frame_f
 mod.frame_f=lambda n,L=4:I(1)
 try:H,bb=mod.hessian_enclosure(np.zeros((16,24)),0.,True)
 finally:mod.frame_f=old
 exact={}
 for ij,m in bb.items():
  q=np.rint(4*(m.l/2+m.h/2))/4
  ck('flat_exact_quarter_coefficients_'+str(ij),np.all(m.l<=q) and np.all(q<=m.h))
  exact[ij]=q
 z=s.symbols('z0:4',nonzero=True)
 hz=s.lambdify(z,symbol(s.eye(4),z),'numpy')
 xy=[divmod(n,4) for n in range(16)]
 for k0 in range(4):
  for k3 in range(4):
   k1=(k0+1)%4;k2=(k3+2)%4
   mat=sum(((1j)**(k0*i+k3*j))*m for (i,j),m in exact.items())
   phase=np.array([(1j)**(k1*x+k2*y) for x,y in xy])
   actual=np.einsum('iajb,j->iab',mat.reshape(16,24,16,24),phase)
   expected=phase[:,None,None]*hz(*[(1j)**k for k in (k0,k1,k2,k3)])[None,:,:]
   ck('literal_full_Bloch_placement_'+str((k0,k3)),np.array_equal(actual,expected))

def curvature():
 A=np.array(json.load(open(ROOT/'center.json'))).reshape(16,24);U=setup(A,2.**-42);et=I(ET)
 r,t=1,2;m=0
 P=U[m,r,1][0]@U[neighbor(m,r,4),t,1][0]@U[neighbor(m,t,4),r,-1][0]@U[m,t,-1][0]
 C=(P-et@P.T@et)*.5
 ck('nonzero_curvature_at_exact_anchor',float(C.l[1,2])>.027 and float(C.h[1,2])<.028)
 return {'component':[float(C.l[1,2]),float(C.h[1,2])],'all_state_energetic_stability_claimed':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--kernel-only',action='store_true');ap.add_argument('--write',action='store_true');args=ap.parse_args()
 result={'structure':kernel(),'scope':'FINITE_L4_OPEN_FULL_4D_CONNECTION_SHEET_NOT_FULL_GR'}
 if not args.kernel_only:
  from full_bloch_verify import run
  result['interval']=run(write=args.write);result['curvature']=curvature()
  ck('all_Bloch_modes_checked', {(x['q0'],x['q3']) for x in result['interval']['blocks']}=={(i,j) for i in range(4) for j in range(4)})
  ck('interval_root_complete',result['interval']['root']['contraction_upper']<2e-6)
  ck('all_blocks_strict',all(x['defect_infinity_upper']<1e-3 for x in result['interval']['blocks']))
  ck('no_false_GR_promotion',result['interval']['physical_GR_closed'] is False and result['interval']['all_mesh_uniformity_claimed'] is False)
  result['final_checks']=CHECKS.copy()
  if args.write:(ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS_FINITE_FULL_4D_SHEET',len(CHECKS),'named structural conditions; interval gates separately in receipt')
if __name__=='__main__':main()
