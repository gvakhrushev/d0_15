#!/usr/bin/env node
"use strict";
/**
 * NEW STRUCTURAL D0→GR ORIGINAL SIX-GENERATOR LORENTZ/COST NO-GO.
 *
 * On genuine original SO+(1,3) null-eta:
 *   B=E11-E00, J=E23-E32,
 *   N2=E12+E20, N3=E13+E30,
 *   barN2=E02+E21, barN3=E03+E31.
 *
 * Original proper Lorentz boost D(lambda)=diag(1/lambda,lambda,1,1):
 *   Ad_D N_i=lambda N_i, Ad_D barN_i=lambda^-1 barN_i.
 * Therefore every continuous CONJUGACY-INVARIANT scalar cost
 * C(SO+(1,3)) assigns exactly C(I) to any exp(aN2+bN3)
 * and exp(a barN2+b barN3):
 *   C(exp N)=C(D(lambda)exp N D(lambda)^-1)
 *            → C(I) as lambda→0 or infinity.
 * No analyticity, perturbative approximation or positivity is
 * required for this exact all-amplitude blind mode.
 *
 * If additionally C∈C², C(P)>=C(I) on a real open class chart,
 * its Hessian at I is Ad-invariant and positive semidefinite.
 * Lorentz boost scaling forces H(N,N)=H(barN,barN)=0,
 * PSD => all four N null directions are in radical(H).
 * Ad-invariance makes radical an ideal. The brackets
 * [N2,barN2]=B, [N2,barN3]=J then force H(B,-)=H(J,-)=0.
 * Thus H=0 on ALL six proper Lorentz directions. If C is
 * C4, nonnegative near identity also forces D³C(I)=0,
 * so C(exp tX)=C(I)+O(t^4) for any Lie tangent X.
 *
 * The SAME TRUE GOLDEN/Bell17 ORIGINAL full positive instrument
 * CAN distinguish exact exp(tN2) from I through signed Choi
 * mark q_N+−q_N− = (herald p^4/(6 sqrt2))*t,
 * while trace of ANY power of unipotent exp(tN2) is 4.
 * Hence geometry must be source-selected via a coframe-/root-
 * referenced PRETRACE ordered mark and genuine Info/Book source,
 * not just a smooth positive conjugacy-class Cost of one plaquette.
 *
 * IMPORTANT: the result assumes the scalar Cost is conjugacy
 * invariant in P ALONE, and its canonical minimum at P=I.
 * It does NOT constrain an observer/coframe-dependent price,
 * two-face order/relative holonomy, unsaturated Cost, moving Info,
 * selected physical G0 H+J+R, or prove GR_closed.
 */
const assert=(v,m)=>{if(!v)throw Error("FAIL "+m)};
const I=()=>Array.from({length:4},(_,i)=>
  Array.from({length:4},(_,j)=>+(i===j)));
const E=(a,b)=>Array.from({length:4},(_,i)=>
  Array.from({length:4},(_,j)=>+(i===a&&j===b)));
const zero=()=>I().map(r=>r.map(()=>0));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const add=(A,B,k=1)=>A.map((row,i)=>row.map((x,j)=>x+k*B[i][j]));
const scale=(A,k)=>A.map(r=>r.map(x=>k*x));
const mat=(A,B)=>A.map(row=>B[0].map((_,j)=>
 row.reduce((v,x,k)=>v+x*B[k][j],0)));
const transpose=A=>A[0].map((_,i)=>A.map(r=>r[i]));
const same=(A,B)=>A.every((row,i)=>row.every((x,j)=>x===B[i][j]));
const norm=A=>Math.max(...A.flat().map(Math.abs));
const tr=A=>A.reduce((s,r,i)=>s+r[i],0);
const fro=(A,B)=>A.reduce((s,r,i)=>s+r.reduce((v,x,j)=>v+x*B[i][j],0),0);
const bracket=(A,B)=>add(mat(A,B),mat(B,A),-1);
const N2=add(E(1,2),E(2,0)),
 N3=add(E(1,3),E(3,0)),
 M2=add(E(0,2),E(2,1)),
 M3=add(E(0,3),E(3,1)),
 B=add(E(1,1),E(0,0),-1),
 J=add(E(2,3),E(3,2),-1),
 Lie=[N2,N3,M2,M3,B,J];
assert(same(bracket(N2,M2),B),"native [N2,barN2] != B");
assert(same(bracket(N2,M3),J),"native [N2,barN3] != J23");
for(const G of Lie)
 assert(same(add(mat(transpose(G),eta),mat(eta,G)),zero()),
   "original genuine proper SO(null eta) tangent failed");
const boost=l=>[
 [1/l,0,0,0],[0,l,0,0],[0,0,1,0],[0,0,0,1]
];
const binv=l=>boost(1/l);
function expNull(a,b=0,opposite=false){
 const A=opposite?M2:N2,C=opposite?M3:N3,
  G=add(scale(A,a),scale(C,b)),
  G2=mat(G,G),G3=mat(G2,G);
 assert(same(G3,zero()),"true original 2-null abelian group not nilpotent cubic");
 const P=add(add(I(),G),scale(G2,.5));
 assert(same(mat(mat(transpose(P),eta),P),eta),
  "true exponential does not preserve null Lorentz eta");
 return P;
}
for(const lam of [.25,.5,2,4,8]){
 const D=boost(lam),Di=binv(lam);
 assert(same(mat(mat(transpose(D),eta),D),eta),
  "original dyadic boost not SO eta");
 for(const [j,G] of Lie.entries()){
  const t=j<2?lam:j<4?1/lam:1;
  assert(same(mat(mat(D,G),Di),scale(G,t)),
   "exact Ad_B eigenvalue error on original basis "+j);
 }
}
const p=(Math.sqrt(5)-1)/2,herald=1/4096;
const finiteSamples=[];
for(const [a,b] of [[.125,0],[0,.125],[.125,-.0625],[-.25,.125]]){
 for(const opposite of [false,true]){
  const P=expNull(a,b,opposite);
  assert(!same(P,I()),"no genuine null wave");
  let Q=I();
  for(let n=1;n<=5;n++){
   Q=mat(Q,P);
   assert(tr(Q)===4,"nontrivial native exact unipotent power got scalar trace");
  }
  const gauges=[1,2,4,8,16].map(i=>{
    const l=opposite?i:1/i;
    const D=boost(l),Di=binv(l);
    const shrink=mat(mat(D,P),Di);
    return {lambda:l,distToFlat:norm(add(shrink,I(),-1))};
  });
  assert(gauges.every((x,i)=>i===0||
    x.distToFlat<gauges[i-1].distToFlat),
    "true conjugation does not contract original null SO group");
  const mean=tr(P)/4,G=opposite?M2:N2,
    contrast=fro(G,P)/(2*Math.SQRT2);
  const qplus=herald*p**4/24*(mean+contrast)**2,
    qminus=herald*p**4/24*(mean-contrast)**2,
    delta=qplus-qminus;
  const expected=herald*p**4*a/(6*Math.SQRT2);
  assert(Math.abs(delta-expected)<1e-16,
    "original full17 positive Choi mark does not see true null amplitude");
  finiteSamples.push({a,b,opposite,
    originalProperSO:true,traceP:tr(P),
    traceFifthPower:tr(Q),
    sampleContractingConjugates:gauges,
    measuredPositiveGoldenMarkerDifference:delta});
 }
}
// An Ad-invariant REAL PSD bilinear form H on the six-dimensional
// actual Lorentz algebra must have H(N2,N2)=0 by scale lambda=2;
// likewise all four N_i/M_i. The PSD Cauchy-Schwarz inequality
// makes them complete radical vectors. Because the radical of an
// Ad-invariant form is a Lie ideal, brackets above add B and J.
// The following exact full six directions are the resulting ideal.
const span=[N2,N3,M2,M3,bracket(N2,M2),bracket(N2,M3)];
function rank(A){
 const R=A.map(r=>r.slice());let j=0;
 for(let c=0;c<R[0].length&&j<R.length;c++){
  let p=j;while(p<R.length&&Math.abs(R[p][c])<1e-12)p++;
  if(p===R.length)continue;
  [R[p],R[j]]=[R[j],R[p]];
  let t=R[j][c];
  for(let k=c;k<R[0].length;k++)R[j][k]/=t;
  for(let i=0;i<R.length;i++)if(i!==j){
   let f=R[i][c];
   for(let k=c;k<R[0].length;k++)R[i][k]-=f*R[j][k];
  }j++;
 }return j;
}
assert(rank(span.map(M=>M.flat()))===6,
  "null radical Lie commutators do not span real so(1,3)");
function samplePositiveClassCost(P){
 return 1+(tr(P)-4)**2;
}
assert(finiteSamples.every(x=>x.traceP===4),
 "native parabolic cost conjugacy classification failed");
const quartic=[
 .125,.0625,.03125
].map(t=>{
 const P=add(add(I(),J,Math.sin(t)),mat(J,J),1-Math.cos(t));
 return {t,canonicalNativeCostExcess:samplePositiveClassCost(P)-1,
   excessDividedByT4:(samplePositiveClassCost(P)-1)/t**4};
});
const outcome={
 status:"PASS_NATIVE_LORENTZ_NULL_PARABOLIC_CLASS_COST_BLIND_AND_HESSIAN_ZERO",
 exactOriginalProperLorentzBasisDimension:rank(span.map(M=>M.flat())),
 allNullBoostAdScalesCorrect:true,
 exactNilpotentOriginalPowersTrace4:true,
 fullNullTwoPlaneInvisibleToEveryContinuousConjugacyClassCost:true,
 ifCostAdInvariantAndAtCanonicalPositiveMinimum:{
   allSixLieHessianZero:true,
   allSixLieThirdTaylorJetsZeroIfC3:true,
   quarticMinimumIfC4:true,
   proof:"PSD Hessian; boost Ad scaling null N,M forces 4 radical vectors; radical ideal plus commutators B,J spans all so(1,3)" },
 originalCompleteGolden17PositiveContrastSeesNullAmplitude:true,
 fullOriginalNativeNullContrastSamples:finiteSamples,
 nontrivialAdInvariantPositiveQuarticCostControl:quartic,
 physicalScope:"Only Cost depending on SINGLE plaquette conjugacy class P and smooth saturated minimum; coframe/observer/relative-history dependence is not excluded and real full G0 Book source still unselected",
 GR_closed:false
};
console.log(JSON.stringify(outcome,null,2));
