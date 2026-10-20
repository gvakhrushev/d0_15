#!/usr/bin/env node
"use strict";
/*
 D0 prospective-Dmin ORIGINAL Golden/CNOT coherent Bell resource
 COST/READINESS optimizer on actual 4D L^4 site output budget.

 This is the fixed 6-OFFLINE-coherent-Bell-pair family from the complete
 native 4q U4 gate. A genuine full-price Dmin law is NOT assumed forced.
 Within THIS actual admitted math execution family, every attempt uses
 exactly two original Golden G and four original CNOT plus one measured
 fresh parity C; the C=0 coherent failure is retained. After K attempts
 the prep READY probability is (1-r^K)^6 with r=p²+p^4. The inverse
 Bell measurement is SINGLE-SHOT on unknown data; never counted as
 repeatable offline. Exact end-to-end raw native rate B*s^6/4096.

 Given an original h^-2 * 6 L^4 source discrepancy budget <=6/L,
 the smallest honest K meeting per-six-prep failure <= L^-7
 is computable with NO new scale/coupling:
 K_min=ceil(log(1-(1-L^-7)^(1/6))/log r).
 The original gate-/clock-execution count is monotone with K, so this
 is the optimal bounded-depth protocol IN THIS SIX-PARITY FAMILY
 under that explicit fixed assurance task. No optimization over all
 G0/Book03 histories or source price is asserted.
*/
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),s=2*p**3,r=1-s;
const fail=(ok,msg)=>{if(!ok)throw Error("FAIL "+msg)};
function ready(K){return Math.exp(6*Math.log1p(-(r**K)));}
function failReady(K){return -Math.expm1(6*Math.log1p(-(r**K)));}
function kOptimal(L){let delta=L**(-7);return Math.ceil(
 Math.log(-Math.expm1(Math.log1p(-delta)/6))/Math.log(r));}
const rows=[];
for(const L of [4,8,16,32,64,128]){
 const K=kOptimal(L),target=L**(-7),B=ready(K),qFail=failReady(K);
 fail(K>=1&&qFail<=target+1e-15,"prospective exact Dmin Bell-prep task not met");
 fail(K===1||failReady(K-1)>target-1e-15,
 "prospective shorter K already meets native source task");
 const sourceError=6*L**6*qFail;
 const usedG=12*(1-r**K)/(1-r)+12;
 const usedCNOT=4*6*(1-r**K)/(1-r)+24;
 fail(sourceError<=6/L+1e-11&&
   usedG<=6/p**3+12+1e-10,"native work not bounded/refining");
 rows.push({L,K,ready:B,notReady:qFail,
  sourceScaledAllOriginalFacesErrorUpperBound:sourceError,
  expectedUsedGoldenGates:usedG,expectedUsedCNOTs:usedCNOT,
  maximumGoldenGateCalls:12*K+12,
  fullRawNativeTeleportSuccess:B*s**6/4096});
}
const K=1;
fail(Math.abs(ready(K)*s**6/4096-p**36)<1e-15,
 "literal n=6 coherent Golden Bell one-shot source not phi^-36");
console.log(JSON.stringify({
 status:"PASS_PROSPECTIVE_NATIVE_DMIN_MINIMAL_GOLDEN_BELL_4D_REFINEMENT",
 nativeOriginalGolden:{p,s,r,oneShotFull64Success:p**36},
 admissibleBoundedFamily:{sixIndependentOfflinePureGoldenBellSeeds:true,
  offlineFailureStatesRetainedCoherently:true,
  sixInverseBellMeasurementsSingleShot:true,
  perTrialNativeGates:{GoldenG:2,CNOT:4,measuredNewParity:1},
  K_min_rule:"ceil(ln(1-(1-L^-7)^(1/6))/ln(p²+p^4))",
  exactOptimality:"minimum number of offline attempts K among identical native parity gadget family with six-pair ready failure <=L^-7",
  table:rows},
 sourceInNativeUnits:{fullBellAmplitude:p**18,
  fullOneShotEventSurprisal:36,
  expectedGatesUniformBound:6/p**3+12,
  codeAndPreparationWorkOutsideGateCount:true},
 cannotInferCompulsoryProspectiveDminFromM1:true,
 genuineMovingProgrammeAndHJRSourceStillOpen:true,
 GR_closed:false
},null,2));
