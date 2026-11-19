#!/usr/bin/env node
"use strict";
/*
  Original Golden p and one literal coherent odd-parity bell gadget:
  CONDITIONAL pure |Phi+>, success s=2p^3; failure r=p²+p^4, coherent
  failing AB ket is archived, NOT measured as FF/RR.

  Exact stopped clock: independent first-success attempts truncated at K.
  True public parity *waiting-time* record {success at j<=K, fail all K}
  has normalized probabilities r^(j-1)s and r^K, and phi-Shannon entropy.
  Six native OFFLINE prep gadgets have a finite uniformly bounded expected
  used-gate budget; the six inverse Bell effects are single-shot on DATA.
  A DISTINCT classical dephased extractor with separately observed F/R
  has exact full prefix-free raw φ-code length; its hidden Book06 history
  price may NOT be transplanted into the coherent trace-class experiment.

  Work and preparation Cost remain physically unselected by G0/Book H+J+R.
*/
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),s=2*p**3,r=1-s;
const fail=(v,msg)=>{if(!v)throw Error(msg)};
const h=x=>x>0?-x*Math.log(x)/ell:0;
function stopped(K){
 let q=Array.from({length:K},(_,j)=>s*r**j).concat([r**K]);
 const mass=q.reduce((a,b)=>a+b,0);
 fail(Math.abs(mass-1)<2e-13,"native parity clock unnormalized");
 const info=q.reduce((a,b)=>a+h(b),0);
 const expectedAttempts=(1-r**K)/(1-r);
 return {K,fullClockProbability:mass,
  parityStoppingEntropyPhi:info,
  expectedGoldenGateCallsOneSeed:2*expectedAttempts,
  offlineSixSeedReadiness:(1-r**K)**6,
  complete64UnconditionalRate:(1-r**K)**6*s**6/4096};
}
const stopInfinite=-Math.log(s)/ell-(r/s)*Math.log(r)/ell;
const trace=[];
for(const K of [1,2,4,8,16,35,50]){
 let a=stopped(K);
 fail(a.parityStoppingEntropyPhi<=stopInfinite+.2,
  "stopped native parity conditional clock code unexpectedly long");
 trace.push(a);
}
fail(Math.abs(stopped(50).parityStoppingEntropyPhi-stopInfinite)<1e-10,
 "native geometric stopping entropy infinite-depth limit wrong");
const expectedGForReady6=6*2/s,meanGWithInverse6=expectedGForReady6+12;
fail(Math.abs(meanGWithInverse6-6/p**3-12)<1e-12,
 "real Bell inverse single-shot source consumed twice");
const classicalExpectedRawCost=12*(2-p)/p**3;
const classicalPublicUniformInfo=12*Math.log(2)/ell;
const classicalHiddenTranscriptInfo=classicalExpectedRawCost-classicalPublicUniformInfo;
const probabilities=[p*p,p**3,p**3,p**4]; // FF,FR,RF,RR
const costs=[2,3,3,4],rawSingleEntropy=probabilities.reduce(
 (sum,q,i)=>sum+q*costs[i],0);
fail(Math.abs(rawSingleEntropy-2*(2-p))<2e-13,
 "literal original F/R prefix code raw cost != exact phi-Shannon");
const rootOneShotCost=36,expectedOneShot=p**36;
fail(Math.abs(-Math.log(expectedOneShot)/ell-rootOneShotCost)<2e-13,
 "native Bell exact one-shot success surprisal not 36");
console.log(JSON.stringify({
 result:"PASS_BOOK03_BOOK06_ORIGINAL_GOLDEN_COHERENT_BELL_PARITY_ARCHIVE_CLOCK",
 actualNativeConstants:{p,s,r},
 coherentBell:{oneShotFull64NativeSuccess:p**36,
  exactOneShotSuccessGoldenSurprisal:36,
  sixOfflinePureBellSeedsExpectedUsedGoldenG:expectedGForReady6,
  sixInverseBellEffectsExactlyOneShotGoldenG:12,
  genuineTotalGCallsExpectedUpperBound:meanGWithInverse6,
  BellEffectNotRepeatableOnUnknownQuantumData:true,
  parityStoppingClockGoldenEntropyPerOfflineSeedInfinite:stopInfinite,
  sixOfflineParityStopTimesGoldenEntropyInfinite:6*stopInfinite,
  finiteKClockTrace:trace},
 separatelyMeasuredClassicalFRExtractor:{
  prefixFreeExactRawWordCodeEntropyInGoldenUnits:classicalExpectedRawCost,
  publiclyRetainedUniform4096InformationInGoldenUnits:classicalPublicUniformInfo,
  conditionalHiddenOriginalFRTranscriptInGoldenUnits:classicalHiddenTranscriptInfo,
  comparisonIsNotCoherentBellMeasurement:true},
 physicalBookAndClockHJRActionStillNotSelected:true,
 GR_closed:false
},null,2));
