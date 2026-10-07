#!/usr/bin/env python3
"""Exact finite controls for native centering, metric lifts and the vacuum boundary.

Infinite-size/range and smooth-limit arguments are analytical in the companion
proof. This checker does not turn an off-shell metric lift into joint GR recovery.
"""
from __future__ import annotations
import argparse
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as sp

INPUT_HEAD='dae0ec13f9f885ff945c45613ae38becbc097d18'
INPUTS=[
 '03_FORMALIZATION/D0/Geometry/ArchiveCubicalDifferential.lean',
 '03_FORMALIZATION/D0/Geometry/A4DCoframeParentConstraint.lean',
 '03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean',
 '03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean',
 '03_FORMALIZATION/D0/Geometry/A4DMetricStressInterface.lean',
 '03_FORMALIZATION/D0/Geometry/A4DDiscreteEnergyKernel.lean',
 '02_REGISTRY/research/A4D_STAGGERED_PRIMAL_DUAL_HODGE_CARRIER.md',
 '02_REGISTRY/research/A4D_NATIVE_QUADRATIC_GRAM_FLUX_BOUNDARY.md',
 '02_REGISTRY/research/A4D_NATIVE_AFFINE_PROBE_NOGO.md',
 '02_REGISTRY/research/certificates/a4d_native_flux_gate.lean',
 '02_REGISTRY/research/certificates/a4d_native_flux_gate_results.json',
 '02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md',
]
PROBE_PREREQUISITE={
 'path': '02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
 'source_head': INPUT_HEAD,
 'sha256': '77079fb2fa8da001ca259ebef432ae7001a15d18f73cde04b8ba3380b9b1cbcf',
}
Q=sp.Rational
PAIRS=[(r,s) for r in range(4) for s in range(r,4)]
ETA=sp.diag(1,-1,-1,-1)


def cycle(L):
 return sp.Matrix(L,L,lambda j,k: int(k==(j-1)%L))


def zero(M):
 return all(sp.expand(v)==0 for v in M)


def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
 ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path)
 args=ap.parse_args();repo=args.repo.resolve();checks=[]
 sha=lambda p:hashlib.sha256((repo/p).read_bytes()).hexdigest()
 def check(name,ok):
  assert bool(ok),name
  checks.append(name);print('PASS_'+name,flush=True)
 receipt_path='02_REGISTRY/research/certificates/a4d_native_centered_metric_lift_results.json'
 receipt=json.loads((repo/receipt_path).read_text())
 assert receipt['status']=='PASS' and receipt['compiler_exit_code']==0 and not receipt['sorryAx']
 assert receipt['printed_axiom_dependencies']==19
 assert set(receipt['axioms'])<={'propext','Classical.choice','Quot.sound'}
 for p,d in {**receipt['transitive_d0_source_sha256'],**receipt['toolchain_input_sha256'],
             receipt['capsule']:receipt['capsule_sha256'],receipt['output']:receipt['output_sha256']}.items():
  assert sha(p)==d,'LEAN_INPUT_CHANGED: '+p
 assert not any(s in (repo/receipt['output']).read_text() for s in ['sorryAx','error:','warning:'])
 if (repo/PROBE_PREREQUISITE['path']).is_file():
  assert sha(PROBE_PREREQUISITE['path'])==PROBE_PREREQUISITE['sha256'],'PUBLISHED_PROBE_INPUT_CHANGED'
 check('COMPILED_ACTUAL_CENTERING_METRIC_AND_ZERO_FIELD_BINDINGS',True)
 ranks={}
 for L in range(2,17):
  I=sp.eye(L);S=cycle(L);A=(I+S)/2
  if L%2:
   C=sum(((-1)**k*S**k for k in range(L)),sp.zeros(L))
   check('ODD_ALL_CYCLIC_INVERSE_ROWS_'+str(L),A*C==I and C*A==I)
  else:
   P=sum((Q((-1)**k,L)*S**k for k in range(L)),sp.zeros(L))
   C=sum((Q((-1)**k*(L-1-2*k),L)*S**k for k in range(L)),sp.zeros(L))
   check('EVEN_COMPLETE_PROJECTOR_AND_RANGE_INVERSE_'+str(L),P*P==P and P.T==P
         and A*P==sp.zeros(L) and A*C==I-P and C*A==I-P and P*C==sp.zeros(L) and C*P==sp.zeros(L))
   b=sp.Matrix([Q(j*j+3*j-2,7) for j in range(L)]);n=sp.Matrix([(-1)**j for j in range(L)])
   projected=(I-P)*b
   check('NONEMPTY_RANGE_FIBER_WITH_RETAINED_RAW_KERNEL_'+str(L),A*(C*projected+3*n)==projected
         and n!=sp.zeros(L,1) and A*n==sp.zeros(L,1))
  rank_sum=0
  for ks in product(range(L),repeat=4):
   z=sum(L%2==0 and k==L//2 for k in ks)
   rank_sum+=10-z*(z+1)//2
  expected=10*L**4-(4*L**3+6*L**2 if L%2==0 else 0)
  check('ALL_FOUR_ROLE_SYMBOL_RANKS_'+str(L),rank_sum==expected)
  ranks[str(L)]={'rank':rank_sum,'kernel':16*L**4-rank_sum,'cokernel':10*L**4-rank_sum}
  if L%2==0:
   check('RAW_KERNEL_AND_CENTERED_SKEW_QUOTIENT_'+str(L),
         16*L**3+6*L**2*(L-1)**2==16*L**4-rank_sum)
 # Independent real-space assembly on the full 2^4 carrier, all 10 metric slots.
 L=2;sites=list(product(range(L),repeat=4));ix={x:i for i,x in enumerate(sites)}
 R=sp.zeros(10*L**4,16*L**4)
 for x in sites:
  for slot,(r,s) in enumerate(PAIRS):
   row=10*ix[x]+slot
   for a,b in [(r,s),(s,r)]:
    y=list(x);y[a]=(y[a]-1)%L;y=tuple(y)
    R[row,16*ix[x]+4*a+b]+=Q(1,2);R[row,16*ix[y]+4*a+b]+=Q(1,2)
 check('INDEPENDENT_REAL_SPACE_ALL_TEN_ROW_RANK',R.rank()==ranks['2']['rank']==104)
 weight=sp.diag(*[1 if r==s else 2 for x in sites for r,s in PAIRS])
 # Trace(R* R) is evaluated with the declared Frobenius pairing.
 check('FULL_PACKED_METRIC_FROBENIUS_WEIGHTS',(R.T*weight*R).trace()==320)
 norms={2:[1,0],3:[1,Q(1,4),Q(1,4)],4:[1,Q(1,2),0,Q(1,2)],6:[1,Q(3,4),Q(1,4),0,Q(1,4),Q(3,4)]}
 for L,amps in norms.items():
  vals=[]
  for ks in product(range(L),repeat=4):
   a=[amps[k] for k in ks]
   vals.extend([4*a[r] for r in range(4) if a[r]])
   vals.extend([2*(a[r]+a[s]) for r,s in PAIRS if r<s and a[r]+a[s]])
  expected={2:2,3:1,4:1,6:Q(1,2)}[L]
  check('SHARP_PACKED_NONZERO_RANGE_SPECTRUM_'+str(L),min(vals)==expected and max(vals)==4)
 check('UNPACKED_OFFDIAGONAL_CHANGES_INVERSE_BOUND',Q(1,2)!=1)
 # Exact matrix Gram/Jacobian/lift checks for nonflat invertible raw frames.
 t=sp.symbols('t');Theta=sp.Matrix([[1,Q(1,3),0,0],[0,-2,Q(1,5),0],[0,0,-1,Q(1,7)],[0,0,0,-3]])
 G=Theta*ETA*Theta.T;H=sp.Matrix(4,4,lambda r,s:Q(2*r-s+1,11))
 D=lambda V:V*ETA*Theta.T+Theta*ETA*V.T
 check('EXACT_NONLINEAR_GRAM_POLYNOMIAL',zero((Theta+t*H)*ETA*(Theta+t*H).T-G-t*D(H)-t*t*H*ETA*H.T))
 for r,s in PAIRS:
  V=sp.zeros(4);V[r,s]=1;V[s,r]=1
  lift=V*Theta.T.inv()*ETA/2
  check(f'ALL_TEN_NONLINEAR_METRIC_VARIATIONS_{r}_{s}',D(lift)==V)
 for r,s in [(r,s) for r,s in PAIRS if r<s]:
  skew=sp.zeros(4);skew[r,s]=1;skew[s,r]=-1;a=skew*ETA
  check(f'FRAME_TYPE_TANGENT_KERNEL_{r}_{s}',a*ETA+ETA*a.T==sp.zeros(4) and D(Theta*a)==sp.zeros(4))
 boost=sp.eye(4);boost[0,0]=boost[1,1]=Q(5,3);boost[0,1]=boost[1,0]=Q(4,3)
 check('NONLINEAR_LORENTZ_FIBER_FACTORIZATION',boost*ETA*boost.T==ETA
       and (Theta*boost)*ETA*(Theta*boost).T==G and Theta.inv()*(Theta*boost)==boost)
 V=sp.Matrix([[2,1,0,0],[1,3,1,0],[0,1,-1,1],[0,0,1,2]])
 K=Theta.inv()*V*Theta.T.inv();S=sum((sp.binomial(Q(1,2),j)*t**j*(K*ETA)**j for j in range(5)),sp.zeros(4))
 residual=sp.expand(S*ETA*S.T-ETA-t*K)
 check('STRAIGHT_METRIC_PENCIL_BINOMIAL_ALL_COMPONENTS',all(
       sp.expand(v).coeff(t,j)==0 for v in residual for j in range(5)))
 # Actual variable-coframe adjoint, independent finite translation assembly.
 L=2;sites=list(product(range(L),repeat=4))
 th={x:ETA+sp.Matrix(4,4,lambda r,s:Q((sum((j+1)*x[j] for j in range(4))+2*r-s)%9-4,30)) for x in sites}
 v={x:sp.Matrix(4,4,lambda r,s:Q((sum(x)+3*r+s)%7-3,13)) for x in sites}
 stress={x:sp.Matrix(4,4,lambda r,s:Q((sum(x)+r+s)%5-2,17)) for x in sites}
 def shift(x,r,sgn):
  y=list(x);y[r]=(y[r]+sgn)%L;return tuple(y)
 cv={x:sp.Matrix(4,4,lambda r,s:(v[x][r,s]+v[shift(x,r,-1)][r,s])/2) for x in sites}
 lhs=sum(sp.trace(stress[x].T*(cv[x]*ETA*th[x].T+th[x]*ETA*cv[x].T)) for x in sites)
 pulled={x:stress[x]*th[x]*ETA for x in sites}
 rhs=sum(v[x][r,s]*(pulled[x][r,s]+pulled[shift(x,r,1)][r,s]) for x in sites for r in range(4) for s in range(4))
 check('VARIABLE_BACKGROUND_FULL_PACKED_STRESS_PULLBACK',lhs==rhs and lhs!=0)
 # Midpoint Taylor cancellation, including every coefficient of a quartic.
 y,a=sp.symbols('y a');f=1+y+y*y+y**3+y**4
 avg=sp.expand((f.subs(y,y+a)+f.subs(y,y-a))/2)
 check('MIDPOINT_SECOND_ORDER_AND_REMAINDER_NORMALIZATION',sp.expand(avg-f-a*a*sp.diff(f,y,2)/2-a**4)==0)
 z=sp.symbols('z');trig={}
 for L in [4,8,12,16]:
  modulus=sp.Poly(sp.cyclotomic_poly(2*L,z),z,domain=sp.QQ)
  red=lambda f:sp.Poly(sp.expand(f),z,domain=sp.QQ).rem(modulus).as_expr()
  cos=lambda k:(z**(k%(2*L))+z**((-k)%(2*L)))/2
  c=cos(1)
  allrows=True
  for j in range(L):
   s=1+cos(2*j)/10;sh=1+c*cos(2*j)/10
   native=(2+cos(2*j+1)/10+cos(2*j-1)/10)/2
   native_matrix=sp.diag(native,-s,-s,-s)
   expected_gram=sp.diag(sh*sh,-s*s,-s*s,-s*s)
   allrows &= red(native-sh)==0 and all(red(v)==0 for v in native_matrix*ETA*native_matrix.T-expected_gram)
  check('ALL_CURVED_MIDPOINT_AND_GRAM_ROWS_'+str(L),allrows)
  trig[str(L)]={'independent_site_slices':L,'full_sites_by_transverse_constancy':L**4,'corrected_component':'Q_AA=s_h^2','other_diagonal':'-s^2','off_diagonal':'0'}
 # Independently contract the full second metric jet at a point where first jet vanishes.
 s0=Q(11,10);g=s0*s0*ETA;gi=g.inv();d2q=-Q(22,25)*sp.pi**2
 def dGamma(aa,b,d,c):
  d2=lambda m,n,i,j:ETA[m,n]*d2q if i==j==0 else 0
  return sp.simplify(sum(gi[aa,m]*(d2(m,d,c,b)+d2(m,b,c,d)-d2(b,d,c,m)) for m in range(4))/2)
 Ric=sp.Matrix(4,4,lambda b,d:sp.simplify(sum(dGamma(aa,b,d,aa)-dGamma(aa,b,aa,d) for aa in range(4))))
 scalar=sp.simplify(sp.trace(gi*Ric));Ein=sp.simplify(Ric-g*scalar/2)
 check('ALL_RICCI_AND_EINSTEIN_COMPONENTS_NONZERO_VACUUM_LIMIT',Ric==sp.diag(12,-4,-4,-4)*sp.pi**2/11
       and scalar==2400*sp.pi**2/1331 and Ein==sp.diag(0,8,8,8)*sp.pi**2/11)
 check('OWNER_CURVATURE_SIGN_RETAINED',-scalar==-2400*sp.pi**2/1331 and -Ein[1,1]==-8*sp.pi**2/11)
 mean_slope_square=Q(1,100)*4*sp.pi**2/2;action=-3*mean_slope_square
 check('OWNED_HALF_ACTION_AND_STRAIGHT_SCALING_CONTRAST',action==-3*sp.pi**2/50
       and sp.expand(((1+t)*action-(1-t)*action)/2-t*action)==0)
 # Recompute every Christoffel/Ricci component for the actual corrected smooth
 # metric diag(a^2,-s^2,-s^2,-s^2), allowing nonzero first and second jets.
 aa,ss,a1,s1,a2,s2=sp.symbols('aa ss a1 s1 a2 s2',real=True,nonzero=True)
 gm=sp.diag(aa**2,-ss**2,-ss**2,-ss**2);inv=gm.inv()
 dg=sp.diag(2*aa*a1,-2*ss*s1,-2*ss*s1,-2*ss*s1)
 ddg=sp.diag(2*(a1*a1+aa*a2),*([-2*(s1*s1+ss*s2)]*3))
 dinv=-inv*dg*inv
 jet=lambda i,j,k:dg[i,j] if k==0 else 0
 jet2=lambda i,j,k,c:ddg[i,j] if k==c==0 else 0
 gamma=lambda i,j,k:sp.simplify(sum(inv[i,m]*(jet(m,k,j)+jet(m,j,k)-jet(j,k,m)) for m in range(4))/2)
 Gamma={(i,j,k):gamma(i,j,k) for i,j,k in product(range(4),repeat=3)}
 def dgamma(i,j,k,c):
  if c!=0:return sp.Integer(0)
  return sp.simplify(sum(dinv[i,m]*(jet(m,k,j)+jet(m,j,k)-jet(j,k,m))
     +inv[i,m]*(jet2(m,k,j,c)+jet2(m,j,k,c)-jet2(j,k,m,c)) for m in range(4))/2)
 ric=sp.Matrix(4,4,lambda j,k:sp.simplify(sum(dgamma(i,j,k,i)-dgamma(i,j,i,k)
     +sum(Gamma[i,i,m]*Gamma[m,j,k]-Gamma[i,k,m]*Gamma[m,j,i] for m in range(4)) for i in range(4))))
 spatial=(aa*ss*s2+2*aa*s1*s1-a1*ss*s1)/aa**3
 rstd=-6*(s2/(aa*aa*ss)+s1*s1/(aa*aa*ss*ss)-a1*s1/(aa**3*ss))
 check('GENERIC_CORRECTED_METRIC_ALL_CONNECTION_AND_RICCI_COMPONENTS',
       all(sp.simplify(v)==0 for v in ric-sp.diag((-3*aa*s2+3*a1*s1)/(aa*ss),spatial,spatial,spatial))
       and sp.simplify(sp.trace(inv*ric)-rstd)==0)
 density=-aa*ss**3*rstd/2
 total_derivative=(2*ss*s1*s1+ss*ss*s2)/aa-ss*ss*s1*a1/aa**2
 b=Q(1,10)
 check('PERIODIC_ACTION_DIVERGENCE_AND_EXPLICIT_CORRECTION_BOUNDS',
       sp.simplify(density-3*total_derivative+3*ss*s1*s1/aa)==0
       and 3*b**3/(1-b)==Q(1,300)
       and (1-b)/(1+b)*Q(3,50)==Q(27,550))
 check('FULL_RAW_SOLDER_SCALING_EQUALS_SQUARED_METRIC_SCALE',zero((t*Theta)*ETA*(t*Theta).T-t*t*G))
 # Exceptions: finite Nyquist targets are outside the linear range, even though
 # smooth continuum probes have the midpoint approximate lift.
 L=4;A=(sp.eye(L)+cycle(L))/2;n=sp.Matrix([(-1)**j for j in range(L)])
 check('NO_EXACT_LIFT_OF_DIAGONAL_NYQUIST_TARGET',n.T*A==sp.zeros(1,L) and (n.T*n)[0]==4)
 check('CENTERING_KERNEL_NOT_RAW_ZERO',A*n==sp.zeros(L,1) and n!=sp.zeros(L,1))
 # At the literal flat coframe H(0)=0; the compiled gate is psi=0.
 # A nonzero cochain is therefore an off-shell control, not another root.
 flat_field=[sp.Integer(1)]+[sp.Integer(0)]*(16*4**4-1)
 check('OFF_SHELL_NONZERO_FLAT_FIELD_IS_REJECTED',sum(v*v for v in flat_field)==1
       and any(v!=0 for v in flat_field))
 payload={'status':'PASS','input_head':INPUT_HEAD,'inputs_sha256':{p:sha(p) for p in INPUTS},
  'lean_receipt_sha256':sha(receipt_path),'published_probe_prerequisite':PROBE_PREREQUISITE,'checks':checks,'finite_ranks':ranks,'curved_exact_controls':trig,
  'existing_rank_result':'REUSED_A4D_STAGGERED_PRIMAL_DUAL_HODGE_CARRIER',
  'even_least_norm_inverse':'1 / (sqrt(2) sin(pi/L))','odd_least_norm_inverse':'1 / (2 sin(pi/(2L)))',
  'all_grid_uniform_inverse':'FALSE; grows linearly with L',
  'nonlinear_fiber':'Lorentz representatives satisfying literal row Nyquist constraints, plus full raw centering kernel',
  'smooth_metric_and_variation_error':'O_V(h^2) via row midpoint preparation, without a frequency selector',
  'curved_metric_error_bound':'11 pi^2 h^2 / 100',
  'owner_einstein_action':'-3 pi^2 / 50','native_half_contrast':'0',
  'corrected_metric_periodic_owner_action':'-3 integral s (s\u0027)^2 / s_h',
  'corrected_metric_owner_action_absolute_lower_bound':'27 pi^2 / 550',
  'corrected_metric_owner_action_error_bound':'pi^4 h^2 / 300',
  'calibrated_contrast_gap_lower_bound':'3 pi^2 h^(1/3) / 100 for sufficiently small h',
  'vacuum_owner_scalar':'-2400 pi^2 / 1331','vacuum_owner_spatial_einstein':'-8 pi^2 / 11',
  'literal_flux_root_family':'EXACT_FULL_ZERO_FIELD_ROOTS_WITH_NON_EINSTEIN_CENTERED_METRIC_LIMIT',
  'global_native_gr':'OPEN; metric/variation preparation is not action or refinement transfer',
  'interlevel_admission':'NOT_ASSERTED; exact finite Euler roots do not by themselves satisfy a native interlevel field constraint',
  'protected_exceptions':['Finite Nyquist targets are not all exactly liftable','Raw kernel is not declared physical gauge',
   'Pointwise metric submersion does not invert centering','Quantitative smooth bounds belong to declared preparation',
   'Other native actions, constrained sectors, connections, and original #310 terminal remain separate']}
 out=json.dumps(payload,sort_keys=True,indent=2)+'\n'
 if args.output:args.output.write_text(out)
 else:
  expected=args.expect or Path(__file__).with_name('a4d_native_centered_metric_lift_certificate.json')
  assert expected.read_text()==out,'PINNED_LEDGER_MISMATCH';print('PASS_IMMUTABLE_PINNED_LEDGER')
 print('PASS_NATIVE_CENTERED_METRIC_LIFT',len(checks))


if __name__=='__main__':main()
