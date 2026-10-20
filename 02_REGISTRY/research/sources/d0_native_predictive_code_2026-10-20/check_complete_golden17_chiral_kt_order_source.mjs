#!/usr/bin/env node
"use strict";
/*
 * Endogenous forward-only CODING of the EXISTING complete 17-class native
 * Golden two-fresh/Bell history:
 * - learn ONLY 11 coarse class probabilities causally by fixed KT/Jeffreys
 *   half-counts (six signed pairs + five complete native complements);
 * - retain the ORIGINAL p:p² Golden conditional code inside EACH real
 *   oriented Lie pair, with no hand-set coupling/angle;
 * - the expected complete Cost−Info has an EXACT reversal-ODD component
 *   whose six coefficients reconstruct (P-P^-1)/2 nonperturbatively.
 * - all Good/Bad/GG/Bell FAILURE labels remain and are actually CODED.
 *
 * This is a FIXED MATHEMATICAL source compiler and a direct Cost−Info
 * identity on already-owned original carriers. It does NOT prove Book03,
 * G0/M1 or operational oldRIGHT/Spin cost SELECTS this source.
 */
const assert=(c,m)=>{if(!c)throw Error("FAIL "+m)};
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),h=1/4096,u=h*p**4/24;
assert(Math.abs(p+p*p-1)<2e-15,"ORIGINAL Golden exact 2-channel normalization");
const I=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const Z=()=>I().map(r=>r.map(()=>0));
const E=(i,j)=>{const A=Z();A[i][j]=1;return A};
const add=(A,B,c=1)=>A.map((row,i)=>row.map((v,j)=>v+c*B[i][j]));
const sc=(A,c)=>A.map(row=>row.map(x=>x*c));
const mm=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,x,k)=>s+x*B[k][j],0)));
const T=A=>A[0].map((_,j)=>A.map(r=>r[j]));
const dot=(A,B)=>A.reduce((s,row,i)=>s+row.reduce((v,x,j)=>v+x*B[i][j],0),0);
const tr=A=>A.reduce((s,row,i)=>s+row[i],0);
const max=A=>Math.max(...A.flat().map(x=>Math.abs(x)));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const inverse=P=>mm(mm(eta,T(P)),eta);
const G=[
 add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)
];
assert(G.every((g,i)=>G.every((g2,j)=>Math.abs(dot(g,g2)-(i===j?2:0))<1e-14),
 "all six ORIGINAL Lorentz generators Frobenius orthogonal norm²2");
function LieExp(i,t){
 const A=G[i],A2=mm(A,A);
 if(i<4)return add(add(I(),A,t),A2,t*t/2);
 if(i===4)return add(add(I(),A,Math.sin(t)),A2,1-Math.cos(t));
 return [[Math.exp(-t),0,0,0],[0,Math.exp(t),0,0],[0,0,1,0],[0,0,0,1]];
}
function originalGolden17(P){
 const m=tr(P)/4,v=dot(P,P)/4;
 let q=[];
 for(const g of G){
  const s=dot(g,P)/(2*Math.SQRT2);
  q.push(u*(m+s)**2,u*(m-s)**2);
 }
 const total=q.reduce((a,b)=>a+b,0),GG=h*p**4*v,
  GB=h*p*p*(1-p*p*v),BG=h*p**3*v;
 q.push(GG-total,GB,BG,h*(1-p**4*v-p*p*(1-p*p*v)-p**3*v),1-h);
 assert(q.length===17&&q.every(x=>x>0)&&
  Math.abs(q.reduce((a,b)=>a+b,0)-1)<4e-14,
  "ALL original Golden two-fresh/Bell17 outcomes positive and normalized");
 return q;
}
const cl=r=>r<12?Math.floor(r/2):r-6,  // class IDs 0..5,6..10
 cond=r=>r<12?(r%2===0?p:p*p):1;
function totals(q){
 const Q=Array(11).fill(0);
 for(let i=0;i<17;i++)Q[cl(i)]+=q[i];
 return Q;
}
function minimizer(q){
 const Q=totals(q);
 const m=q.map((_,r)=>Q[cl(r)]*cond(r));
 assert(Math.abs(m.reduce((s,x)=>s+x,0)-1)<3e-14,
   "learned 11 true class masses and exactly native p:p² six conditional codes normalize");
 return m;
}
function code(q,m){
 let ret=0;
 for(let i=0;i<17;i++)ret+=q[i]*Math.log(q[i]/m[i])/ell;
 return ret;
}
function pairCost(q,a){
 const z=q[2*a]+q[2*a+1],qp=q[2*a],qm=q[2*a+1];
 return (qp*Math.log(qp/(z*p))+qm*Math.log(qm/(z*p*p)))/ell;
}
function read(P){
 const q=originalGolden17(P),inv=inverse(P),v=originalGolden17(inv);
 const M=minimizer(q),Mv=minimizer(v);
 const score=code(q,M),opp=code(v,Mv);
 const cls=totals(q),clsInv=totals(v);
 assert(Math.max(...cls.map((x,i)=>Math.abs(x-clsInv[i])))<5e-13,
  "all 11 Golden code coarse class weights are EXACTLY path-reversal EVEN");
 const r=Array.from({length:6},(_,a)=>pairCost(q,a));
 const rinv=Array.from({length:6},(_,a)=>pairCost(v,a));
 const rdiff=r.map((x,a)=>x-rinv[a]);
 const mp=tr(P)/4;
 assert(mp>0,"strict positive original Golden marked root for EXACT Lie inverse");
 const readOdd=G.reduce((M,g,a)=>
    add(M,g,-Math.SQRT2*rdiff[a]/(4*u*mp)),Z());
 const idealOdd=sc(add(P,inv,-1),.5);
 const err=max(add(readOdd,idealOdd,-1));
 assert(err<1e-11,"SIGNED native Golden code reversal-source reconstructs original FULL nonlinear six-bivector Lorentz curvature");
 for(let a=0;a<6;a++){
  assert(Math.abs(rdiff[a]+q[2*a]-q[2*a+1])<2e-14,
  "actual original frozen p:p² ratio makes complete code ODD source equal negative signed mark");
 }
 const direct=Array.from({length:6},(_,a)=>dot(G[a],P)/2);
 const recovered=rdiff.map(v=>-Math.SQRT2*v/(4*u*mp));
 assert(Math.max(...direct.map((x,i)=>Math.abs(x-recovered[i])))<6e-12,
   "six ORIGINAL Lorentz signed coefficient recoveries through code PRICE agree with true half-Frobenius projections");
 return {q,score,opp,err,oddCode:score-opp,direct,recovered,mp,
  relativeNuisance:
   score-r.reduce((sum,x)=>sum+x,0)};
}
const controls=[];
for(let j=0;j<18;j++){
 const P=mm(mm(LieExp(j%6,.006*(1+j%5)),
                LieExp((j+1)%6,.007*(1+(3*j)%4))),
                LieExp((j+4)%6,.008*(1+(j%3))));
 assert(max(add(mm(mm(T(P),eta),P),eta,-1))<3e-12,
  "true original SO null metric invariance on noncommuting loop product");
 const v=read(P);
 controls.push({j,codeSourceOdd:v.oddCode,positiveRelativeCode:v.score,
    fullLorentzRecoveryMaxError:v.err,nonzeroOriginalLieMarks:v.direct.filter(x=>Math.abs(x)>1e-8).length});
}
const P0=I(),q0=originalGolden17(P0),R0=read(P0);
assert(R0.oddCode===0&&R0.score>0,
  "actual original conditional fixed chiral code pays nonzero baseline, not a free optimum");
const delta=1e-4,center=read(LieExp(4,delta)),centerm=read(LieExp(4,-delta));
const deriv=(center.score-centerm.score)/(2*delta);
const sourceExact=-Math.SQRT2*u;
assert(Math.abs(deriv-sourceExact)<3e-11,
 "REAL original J23 first COST minus INFO is exactly native Golden odd p:p² source");
const sourceOddExact=-2*4*u*((1+Math.cos(delta))/2)*(Math.sin(delta)/Math.SQRT2)/2;
assert(Math.abs(center.oddCode-sourceOddExact)<2e-12,
 "TRUE original code direction-odd expected Cost−Info is exact at finite t");

// A completely FORWARD ONLY model that learns the 11 class masses on the
// actual native Golden17 label alphabet via HALF-COUNT KT, while 6 signed
// conditional code ratios remain at the ORIGINAL p:p² values.
// No knowledge of the future field P is supplied to the decoder.
// This is NOT a freely optimal 17-symbol clairvoyant predictor.
const steps=16384,n=Array(11).fill(0),seq=[];
let logOnline=0,logConditional=0;
for(let t=0;t<steps;t++){
 const r=(t%4096===0)?(Math.floor(t/4096)===0?8:
   (Math.floor(t/4096)===1?9:
    Math.floor(t/4096)===2?0:1)):16;
 const k=cl(r),prob=(n[k]+.5)/(t+11/2)*cond(r);
 assert(prob>0&&prob<1,"actual forward-only code probability strictly positive on original complete Golden17");
 logOnline+=Math.log(prob);
 logConditional+=Math.log(cond(r));
 n[k]++;seq.push(r);
}
const lgHalf=x=>{let z=.5*Math.log(Math.PI);for(let i=0;i<x;i++)z+=Math.log(i+.5);return z};
let logMixture=lgHalf(5)-lgHalf(steps+5);
for(const count of n)logMixture+=lgHalf(count)-lgHalf(0);
logMixture+=logConditional;
assert(Math.abs(logMixture-logOnline)<5e-9,
 "complete original Golden17 11-class KT+native p:p² forward-only online code == exact fixed Bayes mixture");
assert(n.reduce((a,b)=>a+b,0)===steps&&n[10]===steps-4,
 "ALL 4095/4096 Bell fail events still count and predictive code stays complete");
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_GOLDEN17_CAUSAL_CHIRAL_CODE_EXACT_NONLINEAR_SIX_LORENTZ_CURVATURE",
 original:{golden_p:p,GoldenSuccess:1/4096,allOutcomes:17,
    learnedCoarseClasses:11,nativeFrozenSignedPairs:6,
    baselineSignedCodeValue:R0.score,originalJ23SignedFirstSource:deriv,
    originalJ23SignedFirstSourceExact:sourceExact},
 recovery:{exactLorentzSixGeneratorAlgebra:true,
    originalFull16GoldenFailureRetained:true,
    originalNoncommutingSOMatrixTests:controls.length,
    worstOddCurvatureReconstructionError:Math.max(...controls.map(x=>x.fullLorentzRecoveryMaxError)),
    controls:controls.slice(0,5)},
 causalCode:{steps,fullObservedFailureEvents:n[10],
   fixedNativePairSourceStillNonzero:true,
   complete11ClassCounts:n,
   completeGoldenCostUnits:-logOnline/ell,
   exactMixtureCodeLogResidual:logMixture-logOnline},
 mathematicalContract:"unconstrained true code optimum would erase this odd source; constrain ONLY original native Golden p:p² conditional roles, predict coarse history causally; source identity exact, not compulsory Book03/G0 selection",
 GR_closed:false
},null,2));
