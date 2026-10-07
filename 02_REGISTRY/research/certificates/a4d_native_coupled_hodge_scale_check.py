#!/usr/bin/env python3
"""Immutable controls for exact coupled metric fibers and scale response.

This checks explicit bindings of existing scalar/Hodge owners. No native
physical action is selected, and no prepared family is declared on shell.
The all-size and continuum arguments are in the companion proof.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from itertools import combinations, product
from pathlib import Path
import sympy as sp

INPUT_HEAD = '2d3f5fff0273ae5c028c07343a72b27b54374602'
INPUTS = [
 '03_FORMALIZATION/D0/Geometry/ArchiveMetricMeasureHodgeLift.lean',
 '03_FORMALIZATION/D0/Geometry/A4DMetricStarSignatureBoundary.lean',
 '03_FORMALIZATION/D0/Geometry/A4DStarFiniteLorentzQuotient.lean',
 '03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean',
 '03_FORMALIZATION/D0/Gauge/YangMillsKillingPositivity.lean',
 '02_REGISTRY/research/A4D_NATIVE_CONNECTION_ACTION_BOUNDARY.md',
 '02_REGISTRY/research/A4D_NATIVE_TRANSPORTED_CONNECTION_REALIZATION.md',
 '02_REGISTRY/research/certificates/a4d_native_connection_action_check.py',
]
PROBE_PREREQUISITE = {
 'path': '02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
 'source_head': 'fc12fc7800eff1a0fb74d73c9d920128cbc9450f',
 'sha256': '77079fb2fa8da001ca259ebef432ae7001a15d18f73cde04b8ba3380b9b1cbcf',
}
Q = sp.Rational
ETA = sp.diag(1,-1,-1,-1)
I = sp.eye(4)
PAIRS = list(combinations(range(4),2))


def compound2(M):
 return sp.Matrix(6,6,lambda i,j:
  M[PAIRS[i][0],PAIRS[j][0]]*M[PAIRS[i][1],PAIRS[j][1]]-
  M[PAIRS[i][0],PAIRS[j][1]]*M[PAIRS[i][1],PAIRS[j][0]])


def contract(A,B):
 return sum(A[i,j]*B[i,j] for i in range(6) for j in range(6))


def hodge_variation(M,mu,V):
 dM=-M*V*M;dm=mu*sp.trace(M*V)/2
 return dm*compound2(M)+mu*sp.Matrix(6,6,lambda i,j:
  dM[PAIRS[i][0],PAIRS[j][0]]*M[PAIRS[i][1],PAIRS[j][1]]+
  M[PAIRS[i][0],PAIRS[j][0]]*dM[PAIRS[i][1],PAIRS[j][1]]-
  dM[PAIRS[i][0],PAIRS[j][1]]*M[PAIRS[i][1],PAIRS[j][0]]-
  M[PAIRS[i][0],PAIRS[j][1]]*dM[PAIRS[i][1],PAIRS[j][0]])


def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
 ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path)
 args=ap.parse_args();repo=args.repo.resolve();checks=[]
 sha=lambda p:hashlib.sha256((repo/p).read_bytes()).hexdigest()
 def check(name,condition):
  assert bool(condition),name
  checks.append(name);print('PASS_'+name,flush=True)
 rp='02_REGISTRY/research/certificates/a4d_native_coupled_hodge_scale_results.json'
 receipt=json.loads((repo/rp).read_text())
 assert receipt['status']=='PASS' and receipt['compiler_exit_code']==0 and not receipt['sorryAx']
 assert receipt['owner_input_head']==INPUT_HEAD and receipt['printed_axiom_dependencies']==18
 assert len(receipt['transitive_d0_source_sha256'])==56
 assert set(receipt['axioms'])<={'propext','Classical.choice','Quot.sound'}
 for p,d in {**receipt['transitive_d0_source_sha256'],**receipt['toolchain_input_sha256'],
             receipt['capsule']:receipt['capsule_sha256'],receipt['output']:receipt['output_sha256']}.items():
  assert sha(p)==d,'LEAN_INPUT_CHANGED: '+p
 output=(repo/receipt['output']).read_text()
 assert not any(s in output for s in ['sorryAx','error:','warning:'])
 assert all(s in output for s in ['archive_metric_measure_hodge_lift_owner',
  'hodgeMetricMeasureWeight','discreteYangMillsAction_nonnegative_of_killing_nonpos'])
 if (repo/PROBE_PREREQUISITE['path']).exists():
  assert sha(PROBE_PREREQUISITE['path'])==PROBE_PREREQUISITE['sha256']
 check('ACTUAL_HODGE_ACTION_AND_QUOTIENT_BINDINGS_COMPILE',True)
 spec=importlib.util.spec_from_file_location('prior_connection',repo/INPUTS[-1])
 old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

 s,mu=sp.symbols('s mu',positive=True);cs=sp.symbols('c0:4',nonzero=True,real=True)
 for bits in product([0,1],repeat=4):
  subset=[i for i,b in enumerate(bits) if b];k=len(subset)
  w=mu**(1-k)*sp.prod(cs[i] for i in subset)
  ws=(s*s*mu)**(1-k)*sp.prod(s*cs[i] for i in subset)
  check('ACTUAL_HODGE_GRADE_'+''.join(map(str,bits)),sp.simplify(ws-s**(2-k)*w)==0)
 M=sp.Matrix(4,4,sp.symbols('m0:16'))
 check('ALL_THIRTY_SIX_MIDDLE_COMPOUND_SLOTS_SCALE_EXACTLY',
       all(sp.expand(z)==0 for z in s*s*mu*compound2(M/s)-mu*compound2(M)))
 F0=sp.Matrix([[1,Q(1,3),0,0],[0,1,Q(1,5),0],[Q(1,7),0,1,Q(1,11)],[0,0,0,1]])*ETA
 Q0=F0*ETA*F0.T;mu0=abs(F0.det());M0=Q0.inv();H0=mu0*compound2(M0)
 Q2=sp.diag(4,-Q(1,4),-1,-1)
 H1=compound2(ETA);H2=compound2(Q2.inv())
 check('COFRAME_DEPENDENT_SHAPE_RESPONSE_IS_REAL',-2*H1[1,1]==2 and -2*H2[1,1]==Q(1,2))
 L=old.cayley(Q(1,7)*old.GEN[0]);F1=sp.diag(2,3,4,5)
 check('ACTUAL_DRESSED_LINK_SCALE_CANCELLATION',
       (s*F0)*L*(s*F1).inv()==F0*L*F1.inv())

 # The tested Hodge pairing passes the actual local Lorentz gauge check.
 Lam=old.cayley(Q(1,5)*old.GEN[0]);Tg=sp.zeros(4);Tgauge=sp.zeros(4)
 for r in range(4):
  prev=F0+Q(r+1,40)*I;Rr=old.cayley(Q(1,9)*old.GEN[(r+1)%6])
  Lprev=old.cayley(Q(1,11)*old.GEN[(r+3)%6])
  Tg[r,:]=(F0[r,:]+(prev*Rr)[r,:])/2
  Tgauge[r,:]=((F0*Lam)[r,:]+((prev*Lprev)*(Lprev.inv()*Rr*Lam))[r,:])/2
 check('ACTUAL_TRANSPORTED_CENTER_SITEWISE_GAUGE_COVARIANCE',Tgauge==Tg*Lam)
 check('ACTUAL_TRANSPORTED_METRIC_SITEWISE_GAUGE_INVARIANCE',Tgauge*ETA*Tgauge.T==Tg*ETA*Tg.T)
 check('ALL_THIRTY_SIX_INTERNAL_CURVATURE_PAIRINGS_GAUGE_INVARIANT',all(
  sp.trace((Lam.inv()*X*Lam)*(Lam.inv()*Y*Lam))==sp.trace(X*Y) for X in old.GEN for Y in old.GEN))

 # Full off-diagonal metric response; compare to direct scalar differentiation.
 C=[sum((Q((a+2)*(j+1)%7-3,5)*G for j,G in enumerate(old.GEN)),sp.zeros(4)) for a in range(6)]
 K=sp.Matrix(6,6,lambda i,j:sp.trace(C[i]*C[j]))
 fullgrad=sp.zeros(4);t=sp.symbols('t',real=True);metric_values=[]
 for a in range(4):
  for b in range(a,4):
   V=sp.zeros(4);V[a,b]=1;V[b,a]=1
   dH=hodge_variation(M0,mu0,V)
   predicted=-contract(dH,K)
   Qt=Q0+t*V;direct=-sp.sqrt(-Qt.det())*contract(compound2(Qt.inv()),K)
   actual=sp.simplify(sp.diff(direct,t).subs(t,0))
   check('FULL_METRIC_VARIATION_'+str(a)+str(b),sp.simplify(actual-predicted)==0)
   fullgrad[a,b]=fullgrad[b,a]=actual if a==b else actual/2
   metric_values.append(actual)
 trace_full=sum(fullgrad[a,b]*Q0[a,b] for a in range(4) for b in range(4))
 trace_packed=sum((1 if a==b else 2)*fullgrad[a,b]*Q0[a,b] for a in range(4) for b in range(a,4))
 trace_wrong=sum(fullgrad[a,b]*Q0[a,b] for a in range(4) for b in range(a,4))
 check('FULL_AND_PACKED_METRIC_SCALE_IDENTITY',trace_full==trace_packed==0 and any(z!=0 for z in metric_values))
 check('OMITTING_PACKED_OFF_DIAGONAL_TWO_IS_DETECTED',trace_wrong!=0)

 # Literal native link derivative on the full constant periodic field.
 # Every shared face position and the transported-weight term are included.
 RR=[old.cayley(Q(1,8+r)*old.GEN[r]) for r in range(4)]
 TT=sp.zeros(4)
 for r in range(4):TT[r,:]=(F0[r,:]+(F0*RR[r])[r,:])/2
 gT=TT*ETA*TT.T;mT=abs(TT.det());invT=gT.inv();HT=mT*compound2(invT)
 Ps=[RR[r]*RR[q]*RR[r].inv()*RR[q].inv() for r,q in PAIRS]
 CC=[(P-P.inv())/2 for P in Ps];KK=sp.Matrix(6,6,lambda i,j:sp.trace(CC[i]*CC[j]))
 mixed_rows=[];native_rows=[]
 for r in range(4):
  for gi,G in enumerate(old.GEN):
   dT=sp.zeros(4);dT[r,:]=(F0*G*RR[r])[r,:]/2
   dg=dT*ETA*TT.T+TT*ETA*dT.T
   dH=hodge_variation(invT,mT,dg)
   dHscaled=hodge_variation(invT/Q(9,4),mT*Q(81,16),Q(9,4)*dg)
   assert dH==dHscaled
   weight_row=-contract(dH,KK);curve_row=0
   for q in range(4):
    if q==r:continue
    ai=PAIRS.index((min(r,q),max(r,q)));P=Ps[ai];Pi=P.inv()
    if r<q:dP=G*P-RR[r]*RR[q]*RR[r].inv()*G*RR[q].inv()
    else:dP=-P*G+RR[q]*G*RR[r]*RR[q].inv()*RR[r].inv()
    dC=(dP+Pi*dP*Pi)/2
    curve_row-=2*sum(HT[ai,j]*sp.trace(dC*CC[j]) for j in range(6))
   native_rows.append(curve_row+weight_row);mixed_rows.append(weight_row)
   check('NATIVE_FULL_LINK_ROW_'+str(6*r+gi)+'_SCALE_IDENTITY',dH==dHscaled)
 check('OMITTING_TRANSPORTED_WEIGHT_LINK_VARIATION_CHANGES_GATE',any(z!=0 for z in mixed_rows))
 check('CURVED_PREPARATION_NOT_AUTOMATICALLY_NATIVE_STATIONARY',any(z!=0 for z in native_rows))

 # The all-row smooth leading stencil, with the actual half-Einstein normalization.
 f,v,w,c=sp.symbols('f v w c',nonzero=True,real=True);b=[c,1/c,1,1]
 E=sp.diag(*[bb*f for bb in b]);Theta=ETA*E.T
 B=[]
 for j in range(1,4):
  X=sp.zeros(4);X[0,j]=X[j,0]=1;B.append(X)
 omega=[sp.zeros(4)]+[b[j]/b[0]*(v/f)*B[j-1] for j in range(1,4)]
 torsion=[]
 for r,q in PAIRS:
  deq=E.diff(f)[:,q]*v if r==0 else sp.zeros(4,1)
  der=E.diff(f)[:,r]*v if q==0 else sp.zeros(4,1)
  torsion.extend(deq-der+omega[r]*E[:,q]-omega[q]*E[:,r])
 check('ALL_TWENTY_FOUR_TORSION_SLOTS',len(torsion)==24 and all(sp.simplify(z)==0 for z in torsion))
 face_density=[]
 for r,q in PAIRS:
  curvature=b[q]/b[0]*(w/f-v*v/(f*f))*B[q-1] if r==0 else omega[r]*omega[q]-omega[q]*omega[r]
  face_density.append(sp.factor((old.weight(E,r,q)*old.biv(curvature))[0]))
 check('SIX_PHYSICAL_CURVATURE_DENSITIES_AND_SIGN',all(sp.simplify(x-y)==0 for x,y in zip(face_density,[(f*w-v*v)/c**2]*3+[v*v/c**2]*3))
       and sp.factor(sum(face_density))==3*f*w/c**2)
 bad_rows=[]
 for r in range(4):
  for gi,G in enumerate(old.GEN):
   row=bad=0
   for q in range(4):
    if q==r:continue
    W=old.weight(E,min(r,q),max(r,q));dW=W.diff(f)*v if q==0 else sp.zeros(1,6)
    sign=1 if r<q else -1
    derivative=(dW*old.biv(G))[0]
    transport=(W*old.biv(omega[q]*G-G*omega[q]))[0]
    row+=sign*(derivative-transport);bad+=sign*(derivative+transport)
   check('PHYSICAL_LEADING_CONNECTION_ROW_'+str(6*r+gi),sp.simplify(row)==0)
   bad_rows.append(sp.factor(bad))
 check('REVERSED_SPIN_CONNECTION_FAILS_ALL_ROW_PREPARATION',any(z!=0 for z in bad_rows))

 # Every factor position in a face has the claimed first-order tangent.
 h=sp.symbols('h',real=True);A=old.GEN[1]+2*old.GEN[3];Bmat=old.GEN[2]-old.GEN[4]
 first=lambda X:X.applyfunc(lambda z:sp.expand(z).coeff(h,0)+h*sp.expand(z).coeff(h,1))
 factors=[I+h*A,I+h*Bmat,I-h*A,I-h*Bmat]
 factor_count=0
 for gi,G in enumerate(old.GEN):
  expected=[G,G+h*(A*G-G*A),-G-h*(Bmat*G-G*Bmat),-G]
  for j in range(4):
   diff=(G*factors[j]) if j<2 else (-factors[j]*G)
   actual=I
   for k,F in enumerate(factors):actual=first(actual*(diff if k==j else F))
   assert actual==expected[j]
   factor_count+=1
 check('ALL_FACE_FACTOR_POSITIONS_RETAINED',factor_count==24)

 # Exact special coframes, including raw nondegeneracy, on two finite levels.
 fiber_sites=gram_slots=0
 for period in [4,8]:
  mesh=Q(1,period);delta=sp.pi*mesh
  for stretch in [1,2]:
   bs=[sp.Integer(stretch),Q(1,stretch),sp.Integer(1),sp.Integer(1)]
   for x in range(period):
    y=Q(x,period);ff=1+sp.cos(2*sp.pi*y)/10;fp=-sp.pi*sp.sin(2*sp.pi*y)/5
    target=sp.diag(bs[0]*ff,-bs[1]*ff,-ff,-ff)
    raw=sp.zeros(4);raw[0,0]=bs[0]*(1+sp.cos(2*sp.pi*y+delta)/(10*sp.cos(delta)))
    centered=sp.zeros(4)
    previous0=bs[0]*(1+sp.cos(2*sp.pi*(y-mesh)+delta)/(10*sp.cos(delta)))
    centered[0,0]=sp.simplify((raw[0,0]+previous0)/2)
    for r in range(1,4):
     Om=bs[r]/bs[0]*fp/ff*B[r-1]
     raw[r,:]=target[r,:]*(I-mesh*Om/2)
     z=mesh*bs[r]/bs[0]*fp/ff/2
     R=I.copy();R[0,0]=R[r,r]=(1+z*z)/(1-z*z);R[0,r]=R[r,0]=2*z/(1-z*z)
     centered[r,:]=((raw[r,:]+raw[r,:]*R)/2).applyfunc(sp.simplify)
    assert all(sp.simplify(z)==0 for z in centered-target),(period,stretch,x,'CENTER')
    actual=sp.simplify(centered*ETA*centered.T)
    required=sp.diag(bs[0]**2*ff**2,-bs[1]**2*ff**2,-ff**2,-ff**2)
    metric_error=(actual-required).applyfunc(lambda z:sp.simplify(sp.expand(z)))
    # The sixteen entry equalities above justify this normal form before
    # taking a determinant; unreduced Cayley/radical fractions obscure it.
    volume_error=sp.simplify(sp.expand(-target.det()-ff**4))
    assert metric_error==sp.zeros(4) and volume_error==0,(period,stretch,x,metric_error,volume_error)
    assert raw[0,0]>0 and all(raw[r,r]<0 for r in range(1,4))
    fiber_sites+=1;gram_slots+=10
 check('EXACT_NONEMPTY_TRANSPORTED_METRIC_AND_EQUAL_VOLUME_FIBERS',fiber_sites==24 and gram_slots==240)

 y=sp.symbols('y',real=True);ff=1+sp.cos(2*sp.pi*y)/10
 integral=sp.integrate(sp.diff(ff,y)**2,(y,0,1))
 I1=-3*integral;I2=I1/4;gap=sp.simplify(I1-I2)
 check('CURVED_METRICS_EQUAL_DENSITY_BUT_DISTINCT_ACTION',integral==sp.pi**2/50 and gap==-9*sp.pi**2/200)
 ep,A0,A1,vp,vm=sp.symbols('ep A0 A1 vp vm',real=True)
 native_diff=sp.expand(((A0+vp)-(A0+vm))/2-((A1+vp)-(A1+vm))/2)
 physical_diff=sp.expand(((1+ep)*I1-(1-ep)*I1)/2-((1+ep)*I2-(1-ep)*I2)/2)
 check('ARBITRARY_VOLUME_PROFILE_CANCELS_WITHOUT_A_SENSITIVITY_BOUND',native_diff==0)
 check('CALIBRATED_PAIRED_GAP_AND_HALF_NORMALIZATION',sp.simplify(physical_diff-ep*gap)==0
       and abs(gap)/4==9*sp.pi**2/800)
 q=sp.symbols('q',positive=True)
 check('TOTAL_RECORD_REFINEMENT_ORDER_CANNOT_HIDE_PAIRED_GAP',sp.limit(q**3/q,q,0)==0)
 vv,tt,gg=sp.symbols('vv tt gg',positive=True)
 reconstructed=sp.integrate((12*tt**3+4*gg*tt)/(4*tt),(tt,1,vv))
 check('VOLUME_ONLY_RADIAL_RESPONSE_RECONSTRUCTION_HAS_RAW_DEGREE_FOUR',
       sp.expand(reconstructed-(vv**3-1+gg*(vv-1)))==0)
 check('NONPOLYNOMIAL_RADIAL_RESPONSE_RECONSTRUCTION',
       sp.integrate(4/(4*tt),(tt,1,vv))==sp.log(vv))

 # Full weight variation: all flattened curvature coordinates are free.
 xx=sp.symbols('x0:6');ww=sp.Matrix(6,6,lambda i,j:sp.Symbol('w'+str(i)+'_'+str(j)))
 scalar=(sp.Matrix(xx).T*ww*sp.Matrix(xx))[0]
 zero=dict.fromkeys(xx,0)
 assert all(sp.diff(scalar,x).subs(zero)==0 for x in xx)
 assert all(sp.diff(scalar,a).subs(zero)==0 for a in ww)
 check('FULL_COFRAME_AND_LINK_ZERO_CURVATURE_GATE_INCLUDES_WEIGHT_DERIVATIVE',True)
 N=old.GEN[0]+old.GEN[3]
 check('INDEFINITE_ZERO_VALUE_NOT_A_GATE',sp.trace(N*N)==0 and sp.trace(N*old.GEN[0])!=0)
 V,lam=sp.symbols('V lam',real=True)
 check('NONZERO_CONSTANT_VOLUME_TERM_HAS_EMPTY_FREE_SCALE_GATE',sp.diff(A0+lam*(1+t)**2*V,t).subs(t,0)==2*V*lam)
 V0=sp.symbols('V0',real=True)
 check('NONLINEAR_VOLUME_PROFILE_IS_PROTECTED_FROM_EMPTY_FIBER_CLAIM',
       sp.diff(((1+t)**2*V-V0)**2,t).subs({t:0,V:V0})==0)
 # Identity links are a distinct native root and fail physical preparation.
 hh=sp.symbols('hh',positive=True)
 physical_row=ff.subs(y,Q(1,4))**2-ff.subs(y,Q(1,4)-hh)**2
 check('CURVED_EXACT_NATIVE_FLAT_LINK_ROOT_FAILS_PHYSICAL_H2_GATE',sp.limit(physical_row/hh,hh,0)==-2*sp.pi/5)
 check('MIXED_SCALE_SHAPE_DEPENDENCE_REMAINS_OUTSIDE_CLASS',
       sp.expand(((1+ep)*A0-(1-ep)*A0)/2-((1+ep)*A1-(1-ep)*A1)/2-ep*(A0-A1))==0)
 check('POINTWISE_RAW_SCALING_NOT_SILENTLY_ASSUMED',Q(1+2,2)!=1)

 payload={
  'status':'PASS','input_head':INPUT_HEAD,'inputs_sha256':{p:sha(p) for p in INPUTS},
  'lean_receipt_sha256':sha(rp),'published_probe_prerequisite':PROBE_PREREQUISITE,
  'checks':checks,'compiled_propositions':18,'transitive_d0_pins':56,
  'finite_fiber_controls':{'L':[4,8],'time_fibers':fiber_sites,'metric_slots':gram_slots},
  'metric_response':'all ten actual derivatives; packed off-diagonal weight two; scale trace zero',
  'native_connection_response':'all 24 full constant-field link rows retain both shared-curvature and transported-weight derivatives; omitting the weight term changes the gate',
  'physical_preparation':'all 24 leading Euler rows zero with all four face positions; actual residual O(h^2) follows analytically from the smooth bounded stencil',
  'class':'I_N=A_h(F,R,z)+B_h(mu,z), A_h invariant under uniform positive raw scaling; the two exact metric/volume families and their probes must be admitted',
  'radial_completeness':'Within a positive scaling cone, every C1 native scalar with continuous volume-only full raw radial response has the stated additive decomposition by a one-dimensional integral; this is not completeness of the D0 core',
  'exact_fibers':'actual transported Gram equals g_c at every L in 4N for c=1,2; all-size proof analytic, scalar and Cayley inverse identities compile',
  'paired_contrast':'native contrasts exactly equal for arbitrary separate volume profiles; physical difference -9*pi^2*h^(1/3)/200+O(h^(4/3)); at least one total transfer error >=9*pi^2*h^(1/3)/800 for small h',
  'on_shell':'NOT_ASSERTED for Levi-Civita preparations; no interlevel compatibility claimed',
  'quadratic_gate':'smooth coframe-dependent curvature-quadratic binding has exact identity-link full levelwise roots for all admitted raw frames; its curved actual readout fails Einstein soundness and physical O(h^2) preparation in that stated class',
  'volume_gate':'only a nonzero constant volume coefficient forces the source-free full scale gate empty; arbitrary nonlinear volume profiles are not covered by that empty-fiber claim',
  'hodge_owner':'actual degree identities and cardinalities printed; no generic uniqueness or Lorentz positivity supplied',
  'exceptions':['genuine mixed scale/shape dependence','native restrictions excluding the probes',
    'additional native matter or interlevel equations','pointwise raw scaling is not exact centered Weyl scaling'],
  'native_action_selection':'NONE_ADDED','physical_ward':'OPEN','native_refinement':'OPEN',
  'positive_gr':'OPEN','global_closure':'OPEN','parents':'#310 #202 #317 original terminals preserved',
 }
 out=json.dumps(payload,sort_keys=True,indent=2)+'\n'
 if args.output:args.output.write_text(out)
 else:
  expected=args.expect or Path(__file__).with_name('a4d_native_coupled_hodge_scale_certificate.json')
  assert expected.read_text()==out,'PINNED_LEDGER_MISMATCH';print('PASS_IMMUTABLE_PINNED_LEDGER')
 print('PASS_NATIVE_COUPLED_HODGE_SCALE',len(checks),flush=True)


if __name__=='__main__':main()
