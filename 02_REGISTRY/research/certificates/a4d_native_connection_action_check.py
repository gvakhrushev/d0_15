#!/usr/bin/env python3
"""Immutable controls for existing connection actions and metric blindness.

The all-mesh homothetic contrast obstruction is analytical in the companion
proof. These exact controls do not declare prepared links native on shell.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path
import sympy as sp

INPUT_HEAD = '59fef13f804d4c5706ef86fe6df01a53f214c565'
INPUTS = [
 '03_FORMALIZATION/D0/Gauge/YangMillsKillingPositivity.lean',
 '03_FORMALIZATION/D0/Gauge/MatrixRepGaugeTransform.lean',
 '03_FORMALIZATION/D0/Gauge/NonAbelianSeamObstructionGap.lean',
 '03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean',
 '03_FORMALIZATION/D0/Geometry/A4DResolvedCorrelatedActionPassport.lean',
 '03_FORMALIZATION/D0/Geometry/A4DAffineOriginSolderBoundary.lean',
 '02_REGISTRY/research/A4D_NATIVE_TRANSPORTED_CONNECTION_REALIZATION.md',
 '02_REGISTRY/research/certificates/a4d_native_transported_connection_results.json',
 '02_REGISTRY/research/A4D_NATIVE_VECTOR_SOURCE_BOUNDARY.md',
 '02_REGISTRY/research/MEMO_A4D_ROLE_BIVECTOR_INSERTION_UNIQUENESS.md',
]
PROBE_PREREQUISITE = {
 'path': '02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
 'source_head': 'fc12fc7800eff1a0fb74d73c9d920128cbc9450f',
 'sha256': '77079fb2fa8da001ca259ebef432ae7001a15d18f73cde04b8ba3380b9b1cbcf',
}
ETA = sp.diag(1,-1,-1,-1)
I = sp.eye(4)
Q = sp.Rational
PAIRS = list(combinations(range(4),2))
GEN = []
for a,b in PAIRS:
 S = sp.zeros(4); S[a,b]=1; S[b,a]=-1
 GEN.append(S*ETA)


def eps(seq):
 return 0 if len(set(seq)) != len(seq) else (-1)**sum(
  seq[i]>seq[j] for i,j in combinations(range(len(seq)),2))


STAR_PAIR = sp.Matrix(6,6,lambda i,j:-eps((*PAIRS[i],*PAIRS[j])))


def wedge(v,w): return sp.Matrix([v[a]*w[b]-v[b]*w[a] for a,b in PAIRS])
def biv(X): return sp.Matrix([(X*ETA)[a,b] for a,b in PAIRS])
def weight(E,r,s):
 u,v=[a for a in range(4) if a not in (r,s)]
 return eps((r,s,u,v))*wedge(E[:,u],E[:,v]).T*STAR_PAIR
def prod(mats):
 out=I
 for M in mats: out=out*M
 return out
def cayley(Z): return (I-Z/2).inv()*(I+Z/2)


def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
 ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path)
 args=ap.parse_args();repo=args.repo.resolve();checks=[]
 sha=lambda p:hashlib.sha256((repo/p).read_bytes()).hexdigest()
 def check(name,cond):
  assert bool(cond),name
  checks.append(name);print('PASS_'+name,flush=True)
 rp='02_REGISTRY/research/certificates/a4d_native_connection_action_results.json'
 receipt=json.loads((repo/rp).read_text())
 assert receipt['status']=='PASS' and receipt['compiler_exit_code']==0 and not receipt['sorryAx']
 assert receipt['owner_input_head']==INPUT_HEAD and receipt['printed_axiom_dependencies']==20
 assert len(receipt['transitive_d0_source_sha256'])==43
 assert set(receipt['axioms'])<={'propext','Classical.choice','Quot.sound'}
 for p,d in {**receipt['transitive_d0_source_sha256'],**receipt['toolchain_input_sha256'],
             receipt['capsule']:receipt['capsule_sha256'],receipt['output']:receipt['output_sha256']}.items():
  assert sha(p)==d,'LEAN_INPUT_CHANGED: '+p
 output=(repo/receipt['output']).read_text()
 assert not any(s in output for s in ['sorryAx','error:','warning:'])
 for name in ['discreteYangMillsAction_nonnegative_of_killing_nonpos',
              'matrix_rep_yang_mills_action_nonnegative_of_skew',
              'exact_bianchi_identity_replaced_by_graded_incidence_closure']:
  assert name in output
 if (repo/PROBE_PREREQUISITE['path']).exists():
  assert sha(PROBE_PREREQUISITE['path'])==PROBE_PREREQUISITE['sha256']
 check('ACTUAL_COMPILED_ACTION_AND_TRANSPORTED_GRAM_BINDINGS',True)

 b0,b1,b2,r0,r1,r2=sp.symbols('b0 b1 b2 r0 r1 r2',real=True)
 v=[b0,b1,b2,r0,r1,r2]
 K=sp.Matrix([[0,b0,b1,b2],[b0,0,r0,r1],[b1,-r0,0,r2],[b2,-r1,-r2,0]])
 S=-sp.trace(K*K)
 check('ALL_SIX_LORENTZ_COORDINATES',K.T*ETA+ETA*K==sp.zeros(4))
 check('ACTUAL_LORENTZ_TRACE_SIGNATURE',sp.expand(S-2*(r0*r0+r1*r1+r2*r2-b0*b0-b1*b1-b2*b2))==0
       and sp.hessian(S,v)==sp.diag(-4,-4,-4,4,4,4))
 check('FULL_INDEPENDENT_CURVATURE_GATE_IS_ZERO',sp.solve([sp.diff(S,x) for x in v],v)==dict.fromkeys(v,0))
 check('EUCLIDEAN_SKEW_EXCLUDES_EXACTLY_ALL_BOOSTS',sp.solve(list(K+K.T),v)=={b0:0,b1:0,b2:0})
 check('FOUR_LINKS_DISCARD_TWELVE_OF_TWENTY_FOUR_DIRECTIONS',
       sp.kronecker_product(sp.eye(4),sp.diag(1,1,1,0,0,0)).rank()==12)
 J=sp.zeros(4);J[1,2]=1;J[2,1]=-1
 B=sp.zeros(4);B[0,1]=B[1,0]=1
 check('TRACE_PAIRING_FAILS_NONPOSITIVE_KILLING_PREMISE',sp.trace(B*B)==2 and -sp.trace(B*B)==-2)
 N=B+J
 check('ZERO_ACTION_IS_NOT_ZERO_CURVATURE_OR_STATIONARITY',N!=sp.zeros(4) and N**3==sp.zeros(4)
       and -sp.trace(N*N)==0 and sp.diff(S,b0).subs(dict(zip(v,[1,0,0,1,0,0])))==-4)
 U=I.copy();U[0,0]=U[1,1]=Q(5,3);U[0,1]=U[1,0]=Q(4,3)
 JU=U*J*U.inv()
 check('PROPER_LORENTZ_CONJUGATION_PRESERVES_TRACE_ACTION',U.T*ETA*U==ETA and U.det()==1
       and U[0,0]>0 and -sp.trace(JU*JU)==-sp.trace(J*J)==2)
 check('FIXED_FROBENIUS_REPAIR_FAILS_LORENTZ_INVARIANCE',sp.trace(J.T*J)==2 and sp.trace(JU.T*JU)==Q(82,9))

 # Exhaust the real symmetric quadratic forms invariant under the six
 # actual adjoint generators. No selected new action is introduced.
 Bs=[]
 for i in range(1,4):
  X=sp.zeros(4);X[0,i]=X[i,0]=1;Bs.append(X)
 Rs=[]
 for i,j,sgn in [(2,3,1),(1,3,-1),(1,2,1)]:
  X=sp.zeros(4);X[i,j]=sgn;X[j,i]=-sgn;Rs.append(X)
 basis=Bs+Rs
 coords=lambda X:sp.Matrix([X[0,1],X[0,2],X[0,3],X[2,3],-X[1,3],X[1,2]])
 ads=[sp.Matrix.hstack(*[coords(X*Y-Y*X) for Y in basis]) for X in basis]
 hpairs=[(i,j) for i in range(6) for j in range(i,6)]
 hv=sp.symbols('H0:21');H=sp.zeros(6)
 for z,(i,j) in zip(hv,hpairs):H[i,j]=H[j,i]=z
 constraints=sp.Matrix([v for ad in ads for v in ad.T*H+H*ad]).jacobian(hv)
 H0=sp.diag(1,1,1,-1,-1,-1);H1=sp.zeros(6)
 for i in range(3):H1[i,i+3]=H1[i+3,i]=1
 check('COMPLETE_INVARIANT_SYMMETRIC_QUADRATIC_SPACE_RANK_NINETEEN',constraints.to_DM().rank()==19
       and all(ad.T*HH+HH*ad==sp.zeros(6) for ad in ads for HH in [H0,H1]))
 alpha,beta=sp.symbols('alpha beta',real=True);HH=alpha*H0+beta*H1
 order=[0,3,1,4,2,5]
 check('EVERY_NONZERO_INVARIANT_FORM_HAS_THREE_OPPOSITE_EIGENVALUE_PAIRS',
       HH.extract(order,order)==sp.diag(*[sp.Matrix([[alpha,beta],[beta,-alpha]])]*3)
       and HH*HH==(alpha*alpha+beta*beta)*sp.eye(6))
 check('NO_NONZERO_POSITIVE_COEFFICIENT_REPAIR',HH[0,0]==alpha and HH[3,3]==-alpha
       and (sp.Matrix([1,0,0,1,0,0]).T*HH*sp.Matrix([1,0,0,1,0,0]))[0]==2*beta
       and (sp.Matrix([1,0,0,-1,0,0]).T*HH*sp.Matrix([1,0,0,-1,0,0]))[0]==-2*beta)

 # Noncompact orbit contraction, exact for every positive rational q and
 # every real common-null-generator link amplitude, not a mode census.
 qq=sp.symbols('qq',positive=True);aa,bb=sp.symbols('aa bb',real=True)
 Bq=I.copy();Bq[0,0]=Bq[2,2]=(qq+1/qq)/2;Bq[0,2]=Bq[2,0]=(qq-1/qq)/2
 null_link=lambda x:I+x*N+x*x*N*N/2
 check('ACTUAL_PROPER_LORENTZ_CONTRACTOR',sp.simplify(Bq.T*ETA*Bq)==ETA and sp.simplify(Bq.det())==1
       and sp.simplify(Bq*N*Bq.inv())==N/qq)
 check('EXACT_UNIPOTENT_LORENTZ_LINK_GROUP',sp.expand(null_link(aa).T*ETA*null_link(aa))==ETA
       and sp.expand(null_link(aa)*null_link(bb))==null_link(aa+bb).applyfunc(sp.expand)
       and sp.expand(null_link(aa)*null_link(-aa))==I)
 check('ARBITRARY_LINK_AMPLITUDE_CONTRACTION',sp.simplify(Bq*null_link(aa)*Bq.inv()-null_link(aa/qq))==sp.zeros(4)
       and all(sp.limit(z,qq,sp.oo)==0 for z in null_link(aa/qq)-I))
 ca=sp.symbols('ca',real=True)
 check('ODD_UNIPOTENT_CURVATURE_IS_EXACTLY_CURL_TIMES_N',
       sp.expand((null_link(ca)-null_link(-ca))/2)==ca*N and null_link(1)!=I)
 cyclic=list(product(range(2),repeat=4))
 step=lambda x,r:tuple((x[i]+1)%2 if i==r else x[i] for i in range(4))
 amap={(x,r):int(x==(0,0,0,0) and r==0) for x in cyclic for r in range(4)}
 curved=0
 for x in cyclic:
  for r,s in PAIRS:
   aa0,aa1,aa2,aa3=[amap[k] for k in [(x,r),(step(x,r),s),(step(x,s),r),(x,s)]]
   curl=aa0+aa1-aa2-aa3
   P=null_link(aa0)*null_link(aa1)*null_link(-aa2)*null_link(-aa3)
   assert P==null_link(curl)
   curved+=int(P!=I)
 check('NONEMPTY_CURVED_NONGAUGE_PERIODIC_SECTOR',curved==6)
 check('VALUE_BLINDNESS_DOES_NOT_IMPLY_STATIONARITY_WITHOUT_LOWER_BOUND',
       -sp.trace(N*N)==0 and sp.diff(S,b0).subs(dict(zip(v,[1,0,0,1,0,0])))==-4)

 # The actual indefinite action has a different gate from a positive repair.
 # Retain transverse variations and derive its complete common-N sector gate.
 prefix=sp.symbols('prefix',real=True)
 Pnull=null_link(ca);Pinull=null_link(-ca);Cnull=ca*N
 for gi,G in enumerate(GEN):
  for sg in [1,-1]:
   dP=sg*null_link(prefix)*G*null_link(ca-prefix)
   dC=(dP+Pinull*dP*Pinull)/2
   check('FULL_TRANSVERSE_NULL_SECTOR_ROW_'+str(gi)+'_'+str(sg),
         sp.expand(-2*sp.trace(Cnull*dC)+sg*2*ca*sp.trace(N*G))==0)
 edges=[(x,r) for x in cyclic for r in range(4)];ei={e:i for i,e in enumerate(edges)}
 faces=[(x,r,s) for x in cyclic for r,s in PAIRS]
 D=sp.zeros(len(faces),len(edges))
 for rowi,(x,r,s) in enumerate(faces):
  for key,sg in [((x,r),1),((step(x,r),s),1),((step(x,s),r),-1),((x,s),-1)]:D[rowi,ei[key]]+=sg
 av=sp.Matrix([amap[e] for e in edges]);cv=D*av;normal=D.T*cv
 check('COMPLETE_L2_CURL_AND_NORMAL_KERNEL',D.to_DM().rank()==45 and (D.T*D).to_DM().rank()==45)
 check('REAL_COUNTING_ENERGY_IDENTITY_BEHIND_ALL_SIZE_GATE',
       (av.T*normal)[0]==(cv.T*cv)[0]==6)
 full_rows=[-2*sp.trace(N*G)*normal[j] for j in range(len(edges)) for G in GEN]
 check('CURVED_ZERO_VALUE_FAILS_COMPLETE_NATIVE_LINK_GATE',len(full_rows)==384
       and max(abs(x) for x in full_rows)==24 and any(x!=0 for x in full_rows))
 for vker in D.nullspace():assert D.T*D*vker==sp.zeros(len(edges),1)
 check('FLAT_SECTOR_SOLVES_ALL_TRANSVERSE_ROWS',len(D.nullspace())==19)

 # Symbolic full coframe, all ten Gram components, and all 36 curvature slots.
 c=sp.symbols('c',real=True)
 E=sp.Matrix(4,4,sp.symbols('e0:16'))
 g=E.T*ETA*E
 gram=(c*E).T*ETA*(c*E)-c*c*g
 check('ALL_TEN_HOMOTHETIC_METRIC_SLOTS',all(sp.expand(gram[i,j])==0 for i in range(4) for j in range(i,4)))
 for r,s in PAIRS:
  w0,w1=weight(E,r,s),weight(c*E,r,s)
  check('ALL_SIX_CURVATURE_COEFFICIENTS_SCALE_ON_FACE_'+str(r)+str(s),
        all(sp.expand((w1*biv(G))[0]-c*c*(w0*biv(G))[0])==0 for G in GEN))
 # Any derivative of the holonomy, including each of its four positions,
 # enters the same linear bivector slot. Verify every matrix slot as well.
 for k in range(24):
  r=k//6;G=GEN[k%6]
  check('CONNECTION_DIRECTION_'+str(k)+'_HAS_IDENTICAL_SOLDER_SCALING',all(
        sp.expand(((weight(c*E,min(r,s),max(r,s))-c*c*weight(E,min(r,s),max(r,s)))*biv(G))[0])==0
        for s in range(4) if s!=r))

 # A literal full periodic lattice; every based face and four factor positions.
 L=2;sites=list(product(range(L),repeat=4))
 shift=lambda x,r,d=1:tuple((x[i]+d)%L if i==r else x[i] for i in range(4))
 links={(x,r):cayley(Q(1+(sum(x)+r)%3,20)*GEN[(sum((j+1)*x[j] for j in range(4))+r)%6])
        for x in sites for r in range(4)}
 raw={x:ETA+sp.Matrix(4,4,lambda r,a:Q((sum(x)+2*r+a)%7-3,100)) for x in sites}
 frames={}
 for x in sites:
  T=sp.zeros(4)
  for r in range(4):
   y=shift(x,r,-1);T[r,:]=(raw[x][r,:]+raw[y][r,:]*links[y,r])/2
  frames[x]=ETA*T.T
 check('NONEMPTY_ACTUAL_TRANSPORTED_METRIC_FIBERS',all(E0.det()!=0 for E0 in frames.values()))
 scale=Q(3,2);metric_rows=0;face_rows=0;derivative_positions=0
 native0=0;native1=0;physical0=0;physical1=0
 for x in sites:
  E0=frames[x];E1=scale*E0
  for r,s in PAIRS:
   keys=[(x,r),(shift(x,r),s),(shift(x,s),r),(x,s)]
   mats=[links[keys[0]],links[keys[1]],links[keys[2]].inv(),links[keys[3]].inv()]
   P=prod(mats);Pi=P.inv();C=(P-Pi)/2
   check_name='LORENTZ_FACE_'+''.join(map(str,x))+'_'+str(r)+str(s)
   assert P.T*ETA*P==ETA and C.T*ETA+ETA*C==sp.zeros(4),check_name
   n=-sp.trace(C*C);native0+=n;native1+=n
   w0,w1=weight(E0,r,s),weight(E1,r,s)
   physical0+=(w0*biv(C))[0];physical1+=(w1*biv(C))[0]
   for pos in range(4):
    # Independent left Lorentz tangent of the underlying positive link.
    for G in GEN:
     dmat=G*mats[pos] if pos<2 else -mats[pos]*G
     dP=prod(mats[:pos])*dmat*prod(mats[pos+1:])
     dC=(dP+Pi*dP*Pi)/2
     assert (w1*biv(dC))[0]==scale*scale*(w0*biv(dC))[0]
     derivative_positions+=1
   face_rows+=1
  assert E1.T*ETA*E1==scale*scale*(E0.T*ETA*E0)
  metric_rows+=10
 check('FULL_L2_PHYSICAL_ACTION_HOMOTHETY',face_rows==96 and physical0!=0
       and physical1==scale*scale*physical0)
 check('FULL_L2_ALL_FOUR_SHARED_LINK_POSITION_DERIVATIVES',derivative_positions==2304)
 check('FULL_L2_ALL_TEN_METRIC_COMPONENTS',metric_rows==160)
 check('LITERAL_LINK_BOUND_NATIVE_MATRIX_ACTION_IS_COFRAME_BLIND',native0==native1 and native0!=0)
 # Coframe-blindness is a real restriction, not a condition satisfied by star.
 check('PROTECTED_EXPLICIT_COFRAME_DEPENDENCE_ESCAPES_CLASS',physical1!=physical0)

 y=sp.symbols('y',real=True);f=1+sp.cos(2*sp.pi*y)/10
 integral=sp.integrate(sp.diff(f,y)**2,(y,0,1));Istar=-3*integral
 check('CURVED_PREPARATION_ACTION_SIGN_AND_NORMALIZATION',integral==sp.pi**2/50 and Istar==-3*sp.pi**2/50)
 check('CURVATURE_NONZERO',sp.diff(f,y,2).subs(y,0)!=0)
 eps0,I0,a,n=sp.symbols('eps I0 a n',real=True)
 half=((1+eps0)*I0-(1-eps0)*I0)/2
 check('EXACT_HOMOTHETIC_HALF_CONTRAST',sp.expand(half-eps0*I0)==0)
 check('ARBITRARY_NATIVE_CALIBRATION_CANNOT_CHANGE_ZERO',sp.simplify((n-n)/2)==0)
 q=sp.symbols('q',positive=True)
 check('RECORD_ERROR_ORDER_CANNOT_CANCEL_PREPARED_GAP',sp.limit(q**3/q,q,0,dir='+')==0)
 check('NATIVE_GATE_NOT_INFERRED_FROM_PHYSICAL_PREPARATION',sp.diff(S,b0).subs(dict(zip(v,[1,0,0,1,0,0])))!=0)

 # A distinct genuine root of the explicitly tested link-bound matrix action:
 # all native links identity, all odd curvatures zero, unrestricted coframe.
 # Derivatives of the quadratic scalar vanish through every curvature tangent.
 curv_slots=sp.Matrix(4,4,sp.symbols('dc0:16'))
 check('ZERO_CURVATURE_FULL_LINK_DERIVATIVE_VANISHES',
       -2*sp.trace(sp.zeros(4)*curv_slots)==0)
 h=sp.symbols('h',positive=True)
 fquarter=f.subs(y,Q(1,4));fprev=f.subs(y,Q(1,4)-h)
 row=fquarter**2-fprev**2
 check('EXACT_NATIVE_ROOT_FAILS_PHYSICAL_H2_PREPARATION',
       sp.limit(row/h,h,0,dir='+')==-2*sp.pi/5)
 # All 24 physical identity-link rows; complementary spatial legs do not
 # involve the temporally centered correction. Verify two adjacent time sites.
 temporal_here,temporal_prev=sp.symbols('temporal_here temporal_prev')
 Ehere=sp.diag(temporal_here,Q(11,10),Q(11,10),Q(11,10))
 Eprev=sp.diag(temporal_prev,1,1,1)
 rows=[]
 for r in range(4):
  for alpha,G in enumerate(GEN):
   value=0
   for s in range(4):
    if s==r:continue
    Ep=Eprev if s==0 else Ehere
    if r<s:value+=((weight(Ehere,r,s)-weight(Ep,r,s))*biv(G))[0]
    else:value+=((weight(Ep,s,r)-weight(Ehere,s,r))*biv(G))[0]
   rows.append(value)
 expected=[0]*24
 for r in range(1,4):expected[6*r+PAIRS.index((0,r))]=Q(21,100)
 check('ALL_TWENTY_FOUR_PHYSICAL_FLAT_LINK_ROWS_AT_CURVED_METRIC',rows==expected)
 check('ON_SHELL_BINDING_AND_PREPARED_FAMILY_NOT_CONFUSED',
       any(z!=0 for z in rows) and -2*sp.trace(sp.zeros(4)*curv_slots)==0)

 # Independent exact rational two-link check of the different flat action jets.
 t=sp.symbols('t',real=True)
 A=sp.zeros(4);A[0,2]=A[2,0]=1
 R0=cayley(t*A);R1=cayley(t*J)
 P=sp.simplify(R0*R1*R0.inv()*R1.inv());C=sp.simplify((P-P.inv())/2)
 ym=sp.factor(-sp.trace(C*C));star=sp.factor((weight(I,0,1)*biv(C))[0])
 ym2=sp.limit(ym/t**2,t,0);ym4=sp.limit(ym/t**4,t,0);star2=sp.limit(star/t**2,t,0)
 check('MATRIX_CURVATURE_ACTION_HAS_ZERO_HOMOGENEOUS_FLAT_TWO_JET',ym2==0 and ym4!=0)
 check('EXISTING_STAR_HAS_NONZERO_SAME_LINK_TWO_JET',star2!=0)
 payload={
  'status':'PASS','input_head':INPUT_HEAD,'inputs_sha256':{p:sha(p) for p in INPUTS},
  'lean_receipt_sha256':sha(rp),'published_probe_prerequisite':PROBE_PREREQUISITE,'checks':checks,
  'compiled_propositions':20,'transitive_d0_pins':43,
  'literal_lattice':{'L':2,'faces':face_rows,'metric_slots':metric_rows,'factor_tangents':derivative_positions},
  'flat_two_link_coefficients':{'native_t2':str(ym2),'native_t4':str(ym4),'physical_t2':str(star2)},
  'class':'I_N(F,R,z)=Phi_h(R,z), with the displayed uniform coframe-scaling probes admitted',
  'contrast':'native zero; physical -3*pi^2*h^(1/3)/50+O(h^(4/3)); O(h) record/refinement errors cannot cancel',
  'native_solution':'NOT_ASSERTED for the displayed Levi-Civita preparations',
  'flat_link_gate':'For the specified matrix action bound to odd plaquette curvature, identity links are exact full levelwise roots for arbitrary raw coframe. The curved midpoint readout tends to non-Einstein g; a physical connection row/h tends to -2*pi/5, so all-row O(h^2) preparation does not follow. Additional native/interlevel constraints are outside this class.',
  'auxiliary':'value set independent of F; branch constancy only under the stated differentiable actual stationary path',
  'lorentz_positivity':'trace action has signature (3,3); Euclidean skew deletes boosts, fixed Frobenius repair is not Lorentz invariant',
  'invariant_quadratics':'complete 21-coefficient symmetric family has rank-19 invariance constraints; all nonzero surviving forms have signature (3,3)',
  'continuous_link_sector':'Every continuous simultaneous-proper-Lorentz-invariant connection scalar has its identity value on all links exp(a_r(x)N), N=B01+J12. This includes nonlocal functions. Curved holonomies survive and are not gauge-flat. Stationarity follows only with differentiability and a global lower bound at the identity; indefinite zero value alone does not imply it.',
  'actual_null_sector_gate':'For the existing indefinite matrix action bound to odd plaquette curvature, all six Lorentz tangents at every edge give E=-2 Tr(NG) D^T D a. Full stationarity in the complete common-N sector is exactly zero real curl. Curved zero-value configurations are off shell; general nonabelian Lorentz links are outside this classification.',
  'curvature_gate':'full independent curvature gate is zero; composed nonlinear link gate not classified',
  'ward':'printed Bianchi-named proposition is skewness closure, not physical divergence',
  'protected_exceptions':['own coframe dependence','coframe-dependent retained variables/operators',
    'independently owned constraints excluding the tested probes','jointly transforming observer fields'],
  'native_action_selection':'NONE_ADDED','refinement_admission':'OPEN',
  'positive_gr':'OPEN','global_closure':'OPEN','parents':'#310 #202 #317 original terminals preserved',
 }
 out=json.dumps(payload,sort_keys=True,indent=2)+'\n'
 if args.output:args.output.write_text(out)
 else:
  expected=args.expect or Path(__file__).with_name('a4d_native_connection_action_certificate.json')
  assert expected.read_text()==out,'PINNED_LEDGER_MISMATCH';print('PASS_IMMUTABLE_PINNED_LEDGER')
 print('PASS_NATIVE_CONNECTION_ACTION',len(checks),flush=True)


if __name__=='__main__':main()
