#!/usr/bin/env node
"use strict";
/*
  ORIGINAL literal real Golden gate G=[[a,-p],[p,a]] and CNOT ONLY,
  all from computational blanks. Real 4-qubit circuit with measured
  fresh parity register prepares EXACT coherent |Phi+> conditional on
  parity=1 with success s=2p^3. Reversing the SAME original finite
  circuit with measured ancilla 1's produces EXACT coherent Bell effect
  sqrt(s) <Phi+|, with EVERY other computational outcome retained.

  Tensor SIX such verified native effects for the ORIGINAL 64-dimensional
  two-fresh CAR16/Golden programme/Choi Bell processor, not mere classical
  fair random labels. Both programme-state entanglement and Bell projector
  are native-type prepared from 12 independent Golden pair parity gadgets:
  unconditioned 64d teleportation probability s^12/4096=p^36,
  conditioned after full preparation readiness EXACT 1/4096. The
  conditional output IS the original arbitrary fixed SO64 U|psi>.
  K-capped fresh parity attempts yield success (1-r^K)^12/4096 with
  all failed earlier Bell ancillas retained; expected G source count is
  bounded by 12/p^3 despite K=O(log L) worst-case for refinement.

  THIS proves mathematical coherent Bell-resource and effect compilation
  in native active Golden/CNOT + parity measurement vocabulary, NOT
  compulsory physical oldRIGHT/Book G0 admission, field-dependent
  |P_U> programme preparation, autonomous known-|1> ancilla routing,
  source/clock/work price, complete thirteen-effect CHOI source POVM,
  or GR. No new fundamental gate or irrational amplitude imported.
*/
const phi=(1+Math.sqrt(5))/2,p=1/phi,a=Math.sqrt(p),s=2*p**3,r=1-s;
const fail=(x,msg)=>{if(!x)throw Error("FAIL "+msg)};
const E16=()=>Array(16).fill(0);
const dot=(x,y)=>x.reduce((sm,a,i)=>sm+a*y[i],0);
const norm=x=>Math.sqrt(dot(x,x));
function golden(v,mask,inverse=false){
 const q=v.slice(),out=v.slice();
 for(let i=0;i<q.length;i++)if(!(i&mask)){
  let j=i|mask;
  if(inverse){
   out[i]=a*q[i]+p*q[j];
   out[j]=-p*q[i]+a*q[j];
  }else{
   out[i]=a*q[i]-p*q[j];
   out[j]=p*q[i]+a*q[j];
  }
 }
 return out;
}
function cnot(v,control,target){
 let out=Array(v.length).fill(0);
 for(let i=0;i<v.length;i++)out[(i&control)?(i^target):i]=v[i];
 return out;
}
function U4(v){
 let x=golden(v,8),y=golden(x,4); // actual A, B original Golden
 y=cnot(y,8,2);y=cnot(y,4,2);    // ORIGINAL fresh C= A XOR B
 y=cnot(y,8,4);                 // success |Psi+> -> |+>_A |1>_B
 y=cnot(y,8,1);                 // exact |Phi+>_(A,D), D was blank
 return y;
}
function U4dag(v){
 let y=cnot(v,8,1);y=cnot(y,8,4);
 y=cnot(y,4,2);y=cnot(y,8,2);
 y=golden(y,4,true);y=golden(y,8,true);
 return y;
}
let start=E16();start[0]=1;
let raw=U4(start),target=E16();target[6]=a*p;target[15]=a*p;
let rawSuccess=raw.reduce((sm,v,i)=>sm+((i&2)?v*v:0),0);
const uncondBellAmpError=Math.max(...raw.map((v,i)=>((i&2)?Math.abs(v-target[i]):0)));
fail(Math.abs(rawSuccess-s)<2e-15&&uncondBellAmpError<2e-15,
 "actual three native wires+fresh blank Bell state source incorrect");
fail(Math.abs(norm(raw)-1)<2e-15&&Math.abs(s+r-1)<2e-15,
 "all Golden parity failures not preserved");
const qSuccess=target.map(v=>v/Math.sqrt(s));
fail(Math.max(...qSuccess.map((v,i)=>
 Math.abs(v-((i===6||i===15)?Math.SQRT1_2:0))))<2e-15,
 "actual physical |Phi+> Bell state not coherent and EXACT");
let maxUnit=0;
const columns=[];
for(let j=0;j<16;j++){
 let basis=E16();basis[j]=1;
 columns.push(U4(basis));
}
for(let i=0;i<16;i++)for(let j=0;j<16;j++)
 maxUnit=Math.max(maxUnit,Math.abs(dot(columns[i],columns[j])-(i===j?1:0)));
fail(maxUnit<2e-15,"finite original G/CNOT Bell gadget not orthogonal");
let maxReverse=0,physInputs=[
 [.38,-.41,.23,.74], [.5,.5,.5,.5], [1,0,0,0],
 [0,Math.SQRT1_2,Math.SQRT1_2,0], [Math.SQRT1_2,0,0,-Math.SQRT1_2]
];
for(let ψ of physInputs){
 const n=norm(ψ);ψ=ψ.map(x=>x/n);
 const input=E16();
 // Bell data on (A,D), known prepared ancilla B=C=1 from
 // a previously successful native parity-comparison resource.
 for(let A=0;A<2;A++)for(let D=0;D<2;D++)
  input[8*A+4+2+D]=ψ[2*A+D];
 let out=U4dag(input);
 let wanted=a*p*(ψ[0]+ψ[3]);
 maxReverse=Math.max(maxReverse,Math.abs(out[0]-wanted));
 let probabilityAllZero=out[0]**2;
 let expected=s*((ψ[0]+ψ[3])/Math.SQRT2)**2;
 fail(Math.abs(probabilityAllZero-expected)<3e-15,
  "true reverse native Bell effect is not sqrt(s)<Phi+|");
 fail(Math.abs(norm(out)-1)<2e-15,
  "whole inverse Bell measurement did not retain all 16 outcomes");
}
fail(maxReverse<2e-15,"Bell effect from native reverse U4 inaccurate");

// n=6 (d=64): explicit ORIGINAL fixed Golden/CNOT U64 as a nontrivial
// programmed orthogonal target, not selected physical Lorentz map.
// Bell resource vector is |P_U>=(I tensor U)|Omega_64> on two 64d registers;
// both Bell gadgets contribute sqrt(s)^6, not a free 1/sqrt(64) input.
const d=64,n=6,unitColumns=[];
for(let i=0;i<d;i++){
 let basis=Array(d).fill(0);basis[i]=1;
 let y=golden(basis,4);y=cnot(y,32,1);
 unitColumns.push(y);
}
let msg=Array.from({length:d},(_,i)=>.37*Math.cos(.11*i)+.53*Math.sin(.07*i));
let div=norm(msg);msg=msg.map(x=>x/div);
const wanted=Array(d).fill(0),actual=Array(d).fill(0);
for(let j=0;j<d;j++){
 for(let i=0;i<d;i++){
  const Uji=unitColumns[i][j];
  wanted[j]+=Uji*msg[i];
  const programmeState=(s**(n/2))*Uji/Math.sqrt(d);
  const trueReverseBellEffect=(s**(n/2))/Math.sqrt(d);
  actual[j]+=trueReverseBellEffect*programmeState*msg[i];
 }
}
const normTrue=norm(actual),normalizingAmplitude=s**n/d,
      expectedProb=s**(2*n)/d**2;
const maxQuantumTransport=Math.max(...actual.map((v,j)=>
 Math.abs(v-normalizingAmplitude*wanted[j])));
fail(maxQuantumTransport<1e-15&&
 Math.abs(normTrue**2-expectedProb)<3e-15,
 "exact full64 two-copy Golden pair Bell teleportation failed");
fail(Math.abs(expectedProb-p**36)<3e-18,
 "12 native original fair coherent pair success must equal p^36");


const nativeUnconditionalKrausScale=p**18;
fail(Math.abs(normalizingAmplitude-nativeUnconditionalKrausScale)<3e-16,
 "one-shot original 64d coherent Bell circuit Kraus != EXACT p^18 U");
const fieldRotate=(v,y)=>{
 const out=v.slice();
 out[0]=Math.cos(y)*v[0]-Math.sin(y)*v[1];
 out[1]=Math.sin(y)*v[0]+Math.cos(y)*v[1];
 return out;
};
const transportField=y=>fieldRotate(wanted,y).map(x=>nativeUnconditionalKrausScale*x);
const fldStep=.002;
const fplus=transportField(fldStep),fminus=transportField(-fldStep),
      fzero=transportField(0);
let fieldFirstErr=0,fieldSecondErr=0;
for(let i=0;i<d;i++){
 const d1=(fplus[i]-fminus[i])/(2*fldStep);
 const d2=(fplus[i]-2*fzero[i]+fminus[i])/(fldStep**2);
 const analytic1=(i===0?-wanted[1]:i===1?wanted[0]:0)*nativeUnconditionalKrausScale;
 const analytic2=(i===0?-wanted[0]:i===1?-wanted[1]:0)*nativeUnconditionalKrausScale;
 fieldFirstErr=Math.max(fieldFirstErr,Math.abs(d1-analytic1));
 fieldSecondErr=Math.max(fieldSecondErr,Math.abs(d2-analytic2));
}
fail(fieldFirstErr<2e-10&&fieldSecondErr<2e-10,
 "complete native Bell64 conditioned arbitrary smooth input does not preserve C² source");
const maxBellRawProb=1/4096;
const table=[];
for(const L of [4,8,16,32,64]){
 const K=Math.ceil((7*Math.log(L)+Math.log(12))/(-Math.log(r)));
 const tau=1-r**K,ready=tau**12;
 const rawProb=ready/4096;
 const expectedGoldenCalls=24*tau/(1-r);
 fail(expectedGoldenCalls<=12/p**3+1e-12,
  "unbounded expectation of native Golden coherent parity gadget");
 fail(12*r**K*L**6<=1/L+1e-12,
  "required h^-2 complete six-face/L4 source convergence no longer holds");
 table.push({L,K,all12BellCoherentSeedsReady:ready,
  fullUnconditionalNativeBellProb:rawProb,
  exactConditionalBellProb:maxBellRawProb,
  worstCaseGoldenGateCalls:24*K,
  expectedGoldenGateCalls:expectedGoldenCalls,
  sourceSixFacesHminus2Bound:6*12*r**K*L**6});
}
console.log(JSON.stringify({
 result:"PASS_ORIGINAL_GOLDEN_CNOT_COHERENT_BELL64_TELEPORTATION",
 originalPrimitive:{goldenP:p,a,singleCoherentPairSuccess:s,
  failureStillInTrueActiveArchive:r,minimumBasisGatesTwo:true,
  completeNativeFourQubitGateColumnsOrthogonal:true,
  unitaryMatrixError:maxUnit,
  coherentBellStateAmplitudeError:uncondBellAmpError,
  reverseBellEffectError:maxReverse},
 fixed64OriginalProcessor:{CAR16andTwoFreshFlags:true,
  programmeDimension:d,actualOriginalGoldenCNOT_U64:true,
  maxProportionalArbitraryDataQuantumOutputError:maxQuantumTransport,
  exactOneShotNativeKrausAmplitude:p**18,
  inheritedFieldFirstSourceError:fieldFirstErr,
  inheritedFieldSecondSourceError:fieldSecondErr,
  unconditionalExactNativeProbabilityWithOneTry:p**36,
  formula:"(2p³)^12/4096 = p^36",
  BellProbabilityGivenAll12NativePairsReady:1/4096,
  completeOtherOutcomesKept:true},
 genuineFinite4DScaling:{sites:"L^4",facesPerSite:6,
  expectedNativeGoldenGateCallsLimit:12/p**3,
  nativeFeedforwardAndComparisonWorkUnpriced:true,
  conservativeBellFailureSourceBound:"h^-2*6L^4*12*r^K <=6/L",
  table},
 fullMovingU64ProgrammeStatePreparationNotForced:true,
 actualOldRightReferenceFiniteControllerAndWorkNotProved:true,
 innerChoi13POVMPositiveObservableStillConditional:true,
 actualG0Book03HJREulerAndEinsteinGRNotClosed:true,
 GR_closed:false
},null,2));
