#!/usr/bin/env python3
"""Exact controls for native links, complete transported-center fibers and jets.

All-size determinants/range bounds and smooth remainders are analytical in the
companion proof. Neither a finite jet nor a small physical residual is a native
joint stationary solution. The immutable ledger preserves those boundaries.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from itertools import combinations, product
import sympy as sp

INPUT_HEAD='fc12fc7800eff1a0fb74d73c9d920128cbc9450f'
INPUTS=[
 '03_FORMALIZATION/D0/Geometry/ArchiveChainConnection.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveChainCurvature.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean',
 '03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean',
 '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
 '03_FORMALIZATION/D0/Geometry/A4DMetricStressInterface.lean',
 '03_FORMALIZATION/D0/Geometry/A4DDiscreteEnergyKernel.lean',
 '02_REGISTRY/research/A4D_CARTAN_CHAIN_CONNECTION_REALIZATION.md',
 '02_REGISTRY/research/A4D_NATIVE_CENTERED_METRIC_LIFT.md',
 '02_REGISTRY/research/certificates/a4d_native_centered_metric_lift.lean',
 '02_REGISTRY/research/certificates/a4d_native_centered_metric_lift_results.json',
]
PROBE_PREREQUISITE={
 'path':'02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
 'source_head':INPUT_HEAD,
 'sha256':'77079fb2fa8da001ca259ebef432ae7001a15d18f73cde04b8ba3380b9b1cbcf',
}
ETA=sp.diag(1,-1,-1,-1)
I=sp.eye(4)
Q=sp.Rational
PAIRS=list(combinations(range(4),2))
SYM=[(r,s) for r in range(4) for s in range(r,4)]
GEN=[]
for a,b in PAIRS:
 S=sp.zeros(4);S[a,b]=1;S[b,a]=-1
 GEN.append(S*ETA)


def prod(mats):
 ans=I
 for mat in mats:ans=ans*mat
 return ans


def block_center(links):
 """Independent full operator assembly; stacked row covectors are columns."""
 L=len(links);A=sp.eye(4*L)
 for j in range(L):
  k=(j-1)%L
  for a in range(4):
   for b in range(4):A[4*j+a,4*k+b]+=links[k][b,a]
 return A/2


def rhs(links,targets):
 L=len(links)
 return 2*sum(((-1)**k*targets[-k%L]*prod(
   [links[j%L] for j in range(-k,0)]) for k in range(L)),sp.zeros(1,4))


def flat_rows(rows):
 return sp.Matrix([v for row in rows for v in row])


def cayley(Z):return (I-Z/2).inv()*(I+Z/2)


def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
 ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path)
 args=ap.parse_args();repo=args.repo.resolve();checks=[]
 sha=lambda p:hashlib.sha256((repo/p).read_bytes()).hexdigest()
 def check(name,ok):
  assert bool(ok),name
  checks.append(name);print('PASS_'+name,flush=True)
 rp='02_REGISTRY/research/certificates/a4d_native_transported_connection_results.json'
 receipt=json.loads((repo/rp).read_text())
 assert receipt['status']=='PASS' and receipt['compiler_exit_code']==0 and not receipt['sorryAx']
 assert receipt['owner_input_head']==INPUT_HEAD and receipt['printed_axiom_dependencies']==20
 assert set(receipt['axioms'])<={'propext','Classical.choice','Quot.sound'}
 for p,d in {**receipt['transitive_d0_source_sha256'],**receipt['toolchain_input_sha256'],
             receipt['capsule']:receipt['capsule_sha256'],receipt['output']:receipt['output_sha256']}.items():
  assert sha(p)==d,'LEAN_INPUT_CHANGED: '+p
 assert not any(s in (repo/receipt['output']).read_text() for s in ['sorryAx','error:','warning:'])
 if (repo/PROBE_PREREQUISITE['path']).is_file():
  assert sha(PROBE_PREREQUISITE['path'])==PROBE_PREREQUISITE['sha256'],'PUBLISHED_PROBE_INPUT_CHANGED'
 check('ACTUAL_NATIVE_AND_GENERIC_FIBER_PROPOSITIONS_COMPILED',True)
 boost=I.copy();boost[0,0]=boost[1,1]=Q(5,3);boost[0,1]=boost[1,0]=Q(4,3)
 rot=I.copy();rot[2,2]=rot[3,3]=Q(3,5);rot[2,3]=Q(4,5);rot[3,2]=-Q(4,5)
 turn=I.copy();turn[1,1]=turn[2,2]=Q(3,5);turn[1,2]=Q(4,5);turn[2,1]=-Q(4,5)
 check('LORENTZ_AND_NATIVE_INVERSE_ORIENTATION',all(U*ETA*U.T==ETA for U in [boost,rot,turn])
       and boost.inv()!=boost and boost*boost.inv()==I)
 ranks={}
 for L in range(2,7):
  families={'flat':[I]*L,'boost':[boost]+[I]*(L-1),
            'loxodromic':[boost*rot]+[I]*(L-1),
            'noncommuting':[([boost,turn,rot][j] if j<3 else I) for j in range(L)]}
  for name,R in families.items():
   tag=name+'_'+str(L);A=block_center(R);W=prod(R);G=I-(-1)**L*W
   nullity=4-G.rank();ranks[tag]={'kernel':nullity,'rank':4*L-nullity,'det_twice_center':str(G.det())}
   check('FULL_OPERATOR_RANK_AND_DETERMINANT_'+tag,
         A.rank()==4*L-nullity and (2*A).det()==G.det())
   raw=[sp.Matrix(1,4,lambda a,b:Q((j+1)*(b+2)-b*b,7)) for j in range(L)]
   target=[(raw[j]+raw[(j-1)%L]*R[(j-1)%L])/2 for j in range(L)]
   B=rhs(R,target)
   check('COMPATIBILITY_AND_ACTUAL_FULL_ROWS_'+tag,
         raw[0]*G==B and A*flat_rows(raw)==flat_rows(target))
   # A different compatible initial row reconstructs every kernel direction.
   kernel=G.T.nullspace()
   for z in kernel:
    rows=[z.T]
    for j in range(1,L):rows.append(-rows[-1]*R[j-1])
    assert A*flat_rows(rows)==sp.zeros(4*L,1) and rows[-1]*R[-1]+rows[0]==sp.zeros(1,4)
   check('FULL_KERNEL_AND_NONEMPTY_FIBERS_'+tag,len(kernel)==nullity)
   if nullity:
    v=G.nullspace()[0];t=[sp.zeros(1,4) for _ in range(L)];t[0]=v.T
    # Bv = 2||v||^2 is an explicit incompatible fiber.
    check('EMPTY_FIBER_WITNESS_'+tag,rhs(R,t)*v==sp.Matrix([[2*(v.T*v)[0]]])
          and (v.T*v)[0]>0 and A.row_join(flat_rows(t)).rank()>A.rank())
   else:
    t=[sp.Matrix(1,4,lambda a,b:Q(j*j+2*b-3,11)) for j in range(L)]
    rows=[rhs(R,t)*G.inv()]
    for j in range(1,L):rows.append(2*t[j]-rows[-1]*R[j-1])
    check('ARBITRARY_TARGET_RECONSTRUCTION_'+tag,A*flat_rows(rows)==flat_rows(t))
 check('EVEN_HOLONOMY_CHANGES_THE_RAW_KERNEL',
       [ranks[name+'_4']['kernel'] for name in ['flat','boost','loxodromic']]==[4,2,0])
 R=[boost,turn,rot,I];W=prod(R);raw=[sp.Matrix([[j+1,2-j,3+j*j,4]]) for j in range(4)]
 t=[(raw[j]+raw[j-1]*R[j-1])/2 for j in range(4)]
 check('REVERSED_NONCOMMUTING_PRODUCT_REJECTED',W!=prod(list(reversed(R)))
       and raw[0]*(I-prod(list(reversed(R))))!=rhs(R,t))
 # Gauge covariance of the complete line readout and compatibility equation.
 gauge=[turn,boost,rot,boost*turn]
 Rt=[gauge[j].inv()*R[j]*gauge[(j+1)%4] for j in range(4)]
 ft=[raw[j]*gauge[j] for j in range(4)]
 tt=[(ft[j]+ft[j-1]*Rt[j-1])/2 for j in range(4)]
 check('COMPLETE_LINE_GAUGE_AND_MONODROMY_COVARIANCE',
       all(tt[j]==t[j]*gauge[j] for j in range(4))
       and prod(Rt)==gauge[0].inv()*W*gauge[0]
       and rhs(Rt,tt)==rhs(R,t)*gauge[0])
 check('OMITTED_LINK_GAUGE_FAILS',any(
       (ft[j]+ft[j-1]*R[j-1])/2!=t[j]*gauge[j] for j in range(4)))
 z=sp.symbols('z')
 H=[sp.Matrix([[2-j,j+1,j*j,-3]]) for j in range(4)]
 K=[R[j]*GEN[j] for j in range(4)]
 for j in range(4):
  actual=((raw[j]+z*H[j])+(raw[j-1]+z*H[j-1])*(R[j-1]+z*K[j-1]))/2
  derivative=(H[j]+H[j-1]*R[j-1]+raw[j-1]*K[j-1])/2
  check('ACTUAL_JOINT_RAW_LINK_VARIATION_POLYNOMIAL_'+str(j),
        (actual-t[j]-z*derivative-z*z*H[j-1]*K[j-1]/2).applyfunc(sp.expand)==sp.zeros(1,4))
 for L in [4,8,12]:
  h=Q(1,L);U=cayley(h*(GEN[0]+GEN[5]/3));R=[U]*L
  f=[(-1)**j*sp.Matrix([[1,2,-1,3]]) for j in range(L)]
  actual=[(f[j]+f[j-1]*R[j-1])/2 for j in range(L)]
  check('EVEN_NEAR_IDENTITY_ALTERNATING_DEFECT_'+str(L),all(
        actual[j]==(-1)**j*sp.Matrix([[1,2,-1,3]])*(I-R[j-1])/2 for j in range(L)))
  check('NEAR_IDENTITY_INJECTIVE_HOLONOMY_'+str(L),(I-U**L).det()!=0)
 # Every finite link tangent direction; explicit inverse, right trivialization.
 for r in range(4):
  Om=sum((Q((r+1)*(j+2)-3,31)*J for j,J in enumerate(GEN)),sp.zeros(4))
  h=Q(1,8);P=I-h*Om/2;U=cayley(h*Om);columns=[]
  for a,J in enumerate(GEN):
   DU=h*P.inv()*J*P.inv();X=U.inv()*DU/h
   check('ALL_24_NATIVE_CONNECTION_TANGENTS_'+str(r)+'_'+str(a),
         DU*ETA*U.T+U*ETA*DU.T==sp.zeros(4)
         and X*ETA+ETA*X.T==sp.zeros(4) and P*(DU/h)*P==J)
   columns.append(sp.Matrix(list(DU)))
  check('FULL_SIX_DIMENSIONAL_TANGENT_RANK_'+str(r),sp.Matrix.hstack(*columns).rank()==6
        and U*ETA*U.T==ETA and cayley(-h*Om)==U.inv())
 Theta=sp.Matrix([[1,Q(1,3),0,0],[0,-2,Q(1,5),0],[0,0,-1,Q(1,7)],[0,0,0,-3]])
 stress=sp.Matrix(4,4,lambda r,s:Q(r+s+1,13))
 for r,s in SYM:
  V=sp.zeros(4);V[r,s]=1;V[s,r]=1;H=V*Theta.T.inv()*ETA/2
  check('ALL_TEN_METRIC_AND_PACKED_VARIATIONS_'+str(r)+'_'+str(s),
        H*ETA*Theta.T+Theta*ETA*H.T==V
        and sp.trace(stress.T*V)==stress[r,s]*(1 if r==s else 2))
 # Full noncommuting jets, independently multiplied as polynomials.
 h=sp.symbols('h')
 def trunc(M,n=3):return M.applyfunc(lambda a:sum(sp.expand(a).coeff(h,j)*h**j for j in range(n)))
 def Cjet(Z):return I+Z+Z*Z/2
 wrong=[]
 for r in range(4):
  row=Theta[r,:];D=sp.Matrix(1,4,lambda a,b:Q(2*r-b+1,19));D2=sp.Matrix(1,4,lambda a,b:Q(r+2*b-3,23))
  Om=sum((Q(r+j+1,17)*J for j,J in enumerate(GEN)),sp.zeros(4))
  Dom=sum((Q(2*r-j+3,29)*J for j,J in enumerate(GEN)),sp.zeros(4))
  current=(row+h*D/2+h*h*D2/8)*Cjet(-h*Om/2)
  prev=(row-h*D/2+h*h*D2/8)*Cjet(-h*(Om-h*Dom)/2)
  result=trunc((current+prev*Cjet(h*(Om-h*Dom)))/2)
  expected=row+h*h*(D2/8-D*Om/4-row*Dom/4+row*Om*Om/8)
  check('ACTUAL_TRANSPORTED_MIDPOINT_ALL_ROW_JETS_'+str(r),trunc(result-expected)==sp.zeros(1,4))
  wrong.append(trunc((current+prev*Cjet(-h*(Om-h*Dom)))/2,2)!=row)
 check('INVERSE_PULL_BREAKS_FIRST_ORDER_CANCELLATION',all(wrong))
 # Six plaquettes and affine torsion: all matrix/vector slots, shifted jets.
 omega=[sum((Q((r+1)*(j+1)-2,17)*J for j,J in enumerate(GEN)),sp.zeros(4)) for r in range(4)]
 dw=[[sum((Q(3*r-2*s+j,23)*J for j,J in enumerate(GEN)),sp.zeros(4)) for s in range(4)] for r in range(4)]
 E=ETA*Theta.T
 de=[sp.Matrix(4,4,lambda a,b:Q(r+2*a-3*b,31)) for r in range(4)]
 order_control=False;torsion_control=False
 for r,s in PAIRS:
  Ur=Cjet(h*omega[r]);Us=Cjet(h*omega[s])
  Urs=Cjet(h*(omega[s]+h*dw[r][s]));Usr=Cjet(h*(omega[r]+h*dw[s][r]))
  A=trunc(Ur*Urs);B=trunc(Us*Usr)
  # Inverses are obtained by C(-Z), preserving the actual path orientation.
  P=trunc(Ur*Urs*Cjet(-h*(omega[r]+h*dw[s][r]))*Cjet(-h*omega[s]))
  F=dw[r][s]-dw[s][r]+omega[r]*omega[s]-omega[s]*omega[r]
  check('ALL_FACE_CURVATURE_MATRIX_SLOTS_'+str(r)+'_'+str(s),
        P==I+h*h*F and trunc(A-B)==h*h*F and trunc((P-I)*B)==h*h*F)
  ba=h*E[:,r]+Ur*(h*E[:,s]+h*h*de[r][:,s])
  bb=h*E[:,s]+Us*(h*E[:,r]+h*h*de[s][:,r])
  tor=de[r][:,s]-de[s][:,r]+omega[r]*E[:,s]-omega[s]*E[:,r]
  check('ALL_AFFINE_TORSION_VECTOR_SLOTS_'+str(r)+'_'+str(s),trunc(ba-bb)==h*h*tor)
  order_control |= omega[r]*omega[s]!=omega[s]*omega[r]
  torsion_control |= F*(E[:,r]+E[:,s])!=sp.zeros(4,1)
 check('NONCOMMUTING_ORDER_AND_BASED_TORSION_REMAINDER_RETAINED',order_control and torsion_control)
 A=boost*turn;B=rot*boost;P=A*B.inv()
 check('EXACT_FINITE_BASED_VERSUS_OPEN_ORDER',A-B==(P-I)*B and (B.inv()*A-I)*B!=A-B)
 ba=sp.Matrix([1,2,3,4]);bb=sp.Matrix([2,-1,1,3])
 check('EXACT_BASED_TORSION_IS_NOT_OPEN_TORSION',ba-P*bb==ba-bb+(I-P)*bb and (I-P)*bb!=sp.zeros(4,1))
 y=sp.symbols('y',real=True);scale=1+sp.cos(2*sp.pi*y)/10
 value=-3*sp.integrate(sp.diff(scale,y)**2,(y,0,1))
 check('TRANSPORTED_SPECTATOR_GATE_CURVED_PHYSICAL_HALF_ACTION',value==-3*sp.pi**2/50)
 c=sp.symbols('c',real=True)
 # Rebuild the four-link test; raw/t name the noncommuting four-cycle.
 links=[boost,turn,rot,I]
 scaled_target=[(c*raw[j]+c*raw[j-1]*links[j-1])/2 for j in range(4)]
 check('ACTUAL_FIXED_LINK_CENTER_SCALE_HOMOGENEITY',all(
       (scaled_target[j]-c*t[j]).applyfunc(sp.expand)==sp.zeros(1,4) for j in range(4)))
 # Literal four-torus row shifts, global counting L2 and transported defect.
 # A Frobenius bound on each link defect dominates its Euclidean operator norm.
 L=4;sites=list(product(range(L),repeat=4))
 fields={x:sp.Matrix(4,4,lambda r,a:Q((sum((j+1)*x[j] for j in range(4))+3*r-2*a)%11-5,13)) for x in sites}
 choices=[cayley(Q(1,8)*GEN[0]),cayley(Q(1,8)*GEN[3]),cayley(Q(1,8)*(GEN[0]+GEN[5]/3))]
 radius2=max(sp.trace((U-I).T*(U-I)) for U in choices)
 raw2=0;center2=0;defect2=0;bulk_checks=0
 for x in sites:
  center=sp.zeros(4);transported=sp.zeros(4)
  for r in range(4):
   y=list(x);y[r]=(y[r]-1)%L;y=tuple(y)
   U=choices[(sum(y)+r)%len(choices)]
   center[r,:]=(fields[x][r,:]+fields[y][r,:])/2
   transported[r,:]=(fields[x][r,:]+fields[y][r,:]*U)/2
   assert transported[r,:]-center[r,:]==fields[y][r,:]*(U-I)/2
  raw2+=sp.trace(fields[x].T*fields[x]);center2+=sp.trace(center.T*center)
  defect=transported-center;defect2+=sp.trace(defect.T*defect)
 check('FULL_FOUR_TORUS_GLOBAL_CENTER_AND_TRANSPORT_DEFECT_BOUND',center2<=raw2 and defect2<=radius2*raw2/4)
 # Fixed coarse bulk matrices remain equal after every row shift; full graded
 # solder vanishes there while the perturbation convention has raw solder eta.
 for U in choices:
  bulk=(Theta+Theta*U)/2
  assert bulk-Theta==Theta*(U-I)/2
  zero_bulk=(sp.zeros(4)+sp.zeros(4)*U)/2
  eta_bulk=(ETA+ETA*U)/2
  assert zero_bulk==sp.zeros(4) and eta_bulk-ETA==ETA*(U-I)/2
  bulk_checks+=1
 check('ACTUAL_SCALAR_AND_GRADED_TRANSPORTED_BULK_IDENTITIES',bulk_checks==3)
 z=sp.symbols('z',nonnegative=True)
 check('GLOBAL_GRAM_L1_ERROR_CONSTANT',sp.expand((1+z/2+1)*(z/2)-(z+z*z/4))==0)
 # Entire flat native differential: metric-only and independently prescribed
 # metric/link outputs have different exact ranges.
 L=2;sites=list(product(range(L),repeat=4));ix={x:i for i,x in enumerate(sites)}
 DF=sp.zeros(10*L**4,16*L**4);DR=sp.zeros(10*L**4,24*L**4)
 for x in sites:
  for slot,(r,s) in enumerate(SYM):
   row=10*ix[x]+slot
   for a,b in [(r,s),(s,r)]:
    y=list(x);y[a]=(y[a]-1)%L;y=tuple(y)
    DF[row,16*ix[x]+4*a+b]+=Q(1,2);DF[row,16*ix[y]+4*a+b]+=Q(1,2)
    for j,J in enumerate(GEN):DR[row,24*ix[y]+6*a+j]+=Q(1,2)*ETA[a,a]*J[a,b]
 joint=DF.row_join(DR).col_join(sp.zeros(24*L**4,16*L**4).row_join(sp.eye(24*L**4)))
 check('FULL_FLAT_RAW_METRIC_RANK_REUSED_WITH_ACTUAL_MATRIX',DF.to_DM().rank()==104)
 check('FULL_FLAT_JOINT_METRIC_ONLY_RANK',DF.row_join(DR).to_DM().rank()==128
       and all(DR[10*ix[x]+SYM.index((r,r)),j]==0 for x in sites for r in range(4) for j in range(DR.cols)))
 check('FULL_FLAT_INDEPENDENT_METRIC_LINK_RANK_AND_COKERNEL',joint.to_DM().rank()==488
       and joint.rows-488==56 and joint.cols-488==152)
 payload={'status':'PASS','input_head':INPUT_HEAD,'inputs_sha256':{p:sha(p) for p in INPUTS},
  'lean_receipt_sha256':sha(rp),'published_probe_prerequisite':PROBE_PREREQUISITE,
  'checks':checks,'finite_cycle_ranks':ranks,
  'matrix_readout':'nativeLink linear part acts by U, not U^-1; all affine shifts retained',
  'complete_fiber':'B(t) in row-range(I-(-1)^L W); all fibers are translated propagated row kernels',
  'determinant':'det A_R = 2^(-4L) det(I-(-1)^L W)',
  'range_bound':'2 L C0 (1+C0 kappa), conditional on segment-product and actual range-inverse bounds',
  'near_identity_full_inverse':'at least 2/(C h) for even L when injective; no least-positive singular bound in the singular case',
  'smooth_actual_metric':'g+O_Ck(h^2); full row midpoint with half Cayley transport',
  'independent_variations':'all 10 symmetric metric and all 24 connection directions',
  'physical_preparation':'all 24 connection residuals O(h^2), conditional on the published finite-probe theorem, on corrected readout',
  'native_action_transfer':'OPEN; physical observable evaluation is not a native action identity',
  'native_stationarity':'OPEN; no on-shell equation is replaced by an auxiliary preparation residual',
  'native_refinement':'OPEN; no physical interlevel arrow selected',
  'affine_and_raw_kernel':'RETAINED; no identification with physical gauge',
  'centered_cartan_ward':'OPEN; ordinary node gauge is not the centered-Cartan connection law',
  'global_native_gr':'OPEN',
  'spectator_flux_gate':'SCOPED_NO_GO: free standalone flux plus unconstrained native links has exact levelwise zero-field roots; physical half-contrast -3*pi^2*h^(1/3)/50+O(h) versus native zero; additional native connection/interlevel gates are not asserted',
  'specified_refinement_limits':'Under R_h=I+O(h), exact componentwise scalar pullback still has exactly constant smooth Lorentz metric limits; bounded-raw/composed-error extension preserved with extra finite error (Ch+C^2h^2/4)B^2. Exact graded full/perturbation limits remain zero/eta in measure; no general approximate graded or concentration claim.',
  'flat_joint_readout':'Even L metric-only rank 10L^4-4L^3; independently prescribed metric/link rank 34L^4-4L^3-6L^2 and cokernel 4L^3+6L^2. Odd grids are onto. Smooth approximate simultaneous preparation is not finite arbitrary-target surjectivity.',
  'protected_exceptions':['Holonomy can remove the even flat Nyquist kernel',
   'Singular finite metric fibers retain their explicit Lorentz-representative compatibility conditions',
   'Raw nondegeneracy is an additional condition outside the smooth prepared class',
   'The previous ordinary-center and specified-refinement obstructions retain their original scopes']}
 out=json.dumps(payload,sort_keys=True,indent=2)+'\n'
 if args.output:args.output.write_text(out)
 else:
  expected=args.expect or Path(__file__).with_name('a4d_native_transported_connection_certificate.json')
  assert expected.read_text()==out,'PINNED_LEDGER_MISMATCH';print('PASS_IMMUTABLE_PINNED_LEDGER')
 print('PASS_NATIVE_TRANSPORTED_CONNECTION',len(checks))


if __name__=='__main__':main()
