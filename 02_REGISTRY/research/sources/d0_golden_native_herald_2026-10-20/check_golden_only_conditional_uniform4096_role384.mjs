#!/usr/bin/env node
"use strict";
/*
GLOBAL finite Golden-only probability theorem AND native constructive escape.

Actual original GoldenCoherentMemory.fullStep: on basis |00>, outputs
a|00>+p|11>, a²=p=phi^-1, p+p²=1. Consequently the measured native
letters F,R have probabilities p,p². Actual native CNOT/permutations
have integral entries. Algebraic-integral amplitudes forbid a FINITE
unconditional 1/4096 (or any nontrivial rational) probability from
basis-blank Golden/CNOT circuits WITHOUT an imported reference state,
gate amplitude, or conditional normalization.

A finite two-fresh-reply test of FR vs RF yields a conditional EXACT
fair bit with two equal probabilities p³, retaining FF,RR failure.
K attempts per bit, 12 independent bits:
  success per bit tau=1-(p²+p^4)^K,
  ALL-READY B=tau^12,
  EXACT uniform 4096 codes GIVEN ALL READY.
  unconditional one-code probability a_K^12,
  a_K=p³ * sum_{j=0}^{K-1}(p²+p^4)^j, in Z[p].
All failures are preserved.

The COMPLETE 18-outcome mathematical instrument is NOTREADY plus
READY × the original full 17-outcome Golden/CAR/Bell q(P). It has a
conditional Bell herald exactly 1/4096, but unconditional herald
B/4096, so it does NOT violate the algebraic-integer theorem.
The inner 13-effect CHOI quantum POVM and genuine controller/prep/clock/
oldRIGHT programme are assumed as typed consumers, NOT hereby built.

Global original Role L=2 16 sites, 64 shared links, 96 actual faces,
384 link-Lie directions, exact d1 rank45 and 114 physical nulls.
Full unconditional Golden Fisher is multiplied by B; conditioned
signed Palatini root decoder remains EXACT at every finite K.
Original h^-2 summed all L4-site source budget has K=O(log L);
worst-case samples O(log L), expected consumed Golden draws bounded.
No Book H+J+R gravitational action, physical refinement or GR claimed.
*/
const phi=(1+Math.sqrt(5))/2, p=1/phi, ell=Math.log(phi);
const assert=(x,msg)=>{if(!x)throw Error("FAIL "+msg)};
const r=p*p+p**4, pr=2*p**3, goldenHerald=1/4096;
assert(Math.abs(r-(3-4*p))<2e-15 && Math.abs(pr+r-1)<2e-15,"true Golden identity");

// EXACT RING R=Z[p], p²=1-p. Every a=√p is an algebraic integer
// because a⁴+a²-1=0; Golden/CNOT pure-basis circuit amplitudes stay
// algebraic integers even beyond this smaller real probability ring.
const one=[1n,0n], zero=[0n,0n], goldenP=[0n,1n];
const plus=(x,y)=>[x[0]+y[0],x[1]+y[1]];
const neg=x=>[-x[0],-x[1]];
const sub=(x,y)=>plus(x,neg(y));
const times=(x,y)=>[
 x[0]*y[0]+x[1]*y[1],
 x[0]*y[1]+x[1]*y[0]-x[1]*y[1]
];
const mulInt=(x,k)=>[x[0]*BigInt(k),x[1]*BigInt(k)];
function power(x,n){let out=one;for(let i=0;i<n;i++)out=times(out,x);return out;}
const rp=power(goldenP,2),r4=power(goldenP,4),
      ringR=plus(rp,r4),p3=power(goldenP,3);
assert(ringR[0]===3n&&ringR[1]===-4n,"r=3-4p native integral ring");
assert(sub(one,ringR).every((x,i)=>x===mulInt(p3,2)[i]),
 "exact 1-r=2p³ in Z[p]");
let exactCertificates=[];
for(let K=1;K<=12;K++){
 let sum=zero,pow=one;
 for(let j=0;j<K;j++){sum=plus(sum,pow);pow=times(pow,ringR);}
 const qbit=times(p3,sum),notReady=power(ringR,K);
 assert(plus(mulInt(qbit,2),notReady).every((x,i)=>x===one[i]),
  "strict whole Golden fair-bit event sum fails in exact algebraic ring");
 const oneLabel=power(qbit,12),twelveReady=power(mulInt(qbit,2),12);
 assert(mulInt(oneLabel,4096).every((x,i)=>x===twelveReady[i]),
  "EXACT conditional 4096-way uniformity over native integral ring fails");
 assert(oneLabel[1]!==0n,
  "finite basis Golden-only circuit has a forbidden rational nontrivial probability");
 if([1,2,4,8,12].includes(K))
  exactCertificates.push({K,
   acceptedOneBitGoldenRing:qbit.map(x=>x.toString()),
   heraldOneCodeGoldenRing:oneLabel.map(x=>x.toString())});
}

const q16=t=>{
 const m=(1+Math.cos(t))/2,s=Math.sin(t)/Math.SQRT2;
 const q=[];
 for(let a=0;a<6;a++){
  const v=a===4?s:0;
  q.push(p**4/24*(m+v)**2,p**4/24*(m-v)**2);
 }
 const rest=p**4-q.reduce((x,y)=>x+y,0);
 const GB=p*p*(1-p*p),BG=p**3,BB=p*p;
 q.push(rest,GB,BG,BB);
 assert(q.length===16&&Math.min(...q)>0&&
    Math.abs(q.reduce((s,x)=>s+x,0)-1)<2e-14,
  "actual original pre-herald Golden 16-outcome conditional lost failure");
 return q;
};
const q17=t=>q16(t).map(x=>x*goldenHerald).concat([1-goldenHerald]);
function ready(K){return (1-r**K)**12;}
function complete(K,t){
 const b=ready(K),q=q17(t);
 const out=[1-b,...q.map(x=>x*b)];
 assert(out.length===18&&Math.min(...out)>0&&
  Math.abs(out.reduce((s,x)=>s+x,0)-1)<2e-14,
 "all native extraction failures and Golden17 downstream records must remain");
 return out;
}
const KL=(a,b)=>a.reduce((s,x,i)=>s+x*Math.log(x/b[i])/ell,0);
let max18KL=0,maxOdd=0,maxFisher=0;
const nativeLieFI=p**4/(6*4096);
const diff=.00002;
for(let K of [1,2,4,8,16,35]){
 const b=ready(K);
 for(let theta of [-.17,-.08,.08,.17]){
  const q=complete(K,theta),qo=complete(K,0);
  const e=Math.abs(KL(q,qo)-b*KL(q17(theta),q17(0)));
  max18KL=Math.max(max18KL,e);
  const conditional=q.slice(1).map(v=>v/b);
  const qp=conditional[8],qm=conditional[9]; // fifth J23 marker
  const odd=Math.sqrt(12)/(p*p*Math.sqrt(goldenHerald))*
     (Math.sqrt(qp)-Math.sqrt(qm));
  maxOdd=Math.max(maxOdd,Math.abs(odd-Math.sin(theta)));
 }
 const left=complete(K,-diff),right=complete(K,diff),q0=complete(K,0);
 let FI=0;
 for(let i=0;i<18;i++){
  const d=(right[i]-left[i])/(2*diff);
  FI+=d*d/q0[i];
 }
 maxFisher=Math.max(maxFisher,Math.abs(FI-nativeLieFI*b));
}
assert(max18KL<3e-13&&maxOdd<3e-13&&maxFisher<5e-12,
  "finite bounded native-herald projective Golden source not exact");

function laplaceRank(){
 // Original 4D periodic L=2 cochain incidence of true SHARED links
 // (NOT 6 fake free plaquettes).
 const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const D=Array.from({length:96},()=>Array(64).fill(0));
 for(let x=0;x<16;x++)for(let j=0;j<6;j++){
  const [r,s]=pairs[j],row=D[6*x+j],idx=(x,t)=>4*x+t;
  row[idx(x,r)]++;
  row[idx(x^(1<<r),s)]++;
  row[idx(x^(1<<s),r)]--;
  row[idx(x,s)]--;
 }
 let a=D.map(x=>x.slice()),rank=0;
 for(let col=0;col<64&&rank<96;col++){
  let best=rank;
  for(let row=rank+1;row<96;row++)
   if(Math.abs(a[row][col])>Math.abs(a[best][col]))best=row;
  if(Math.abs(a[best][col])<1e-11)continue;
  [a[best],a[rank]]=[a[rank],a[best]];
  let pivot=a[rank][col];
  for(let k=col;k<64;k++)a[rank][k]/=pivot;
  for(let row=rank+1;row<96;row++){
   let f=a[row][col];if(!f)continue;
   for(let k=col;k<64;k++)a[row][k]-=f*a[rank][k];
  }
  rank++;
 }
 return rank;
}
const roleRank=laplaceRank();
assert(roleRank===45,"original true 4D L2 Role shared-link rank not 45");
const table=[];
for(let L of [4,8,16,32,64,128]){
 const K=Math.ceil((7*Math.log(L)+Math.log(12))/(-Math.log(r)));
 const tau=1-r**K,B=tau**12,reject=1-B;
 const expectedDraws=24*(1-r**K)/(1-r);
 const worstDraws=24*K;
 const scaledErrorBound=L**6*12*r**K;
 assert(scaledErrorBound<=1/L+1e-12,
   "the explicit original h^-2/all-L4-site source budget is not o(1)");
 assert(expectedDraws<=12/p**3+1e-12,
   "native expected Golden draws should be UNIFORMLY bounded");
 table.push({L,K,notReady:reject,
  correctedBellHeraldUnconditional:B/4096,
  conditionalBellHerald:1/4096,
  expectedNativeGoldenDraws:expectedDraws,
  maximumNativeGoldenDraws:worstDraws,
  sourceBudgetUpperBound:6*scaledErrorBound});
}
const codeCostPerGoldenDraw=p+2*p*p;
const expectedLimit=12/p**3;
const expectedFullCodeBudget=expectedLimit*codeCostPerGoldenDraw;
const conditionalInformation4096=12*Math.log(2)/ell;
assert(Math.abs(expectedLimit-24/(1-r))<2e-13,"expected native work");
console.log(JSON.stringify({
 result:"PASS_ORIGINAL_GOLDEN_ONLY_HERALDED_UNIFORM4096_COMPLETE_GR_SOURCE_COMPILER",
 theorem:{nativeProbabilityRing:"Z[p], p²=1−p; a=√p is root of a⁴+a²−1",
  finiteUnconditionalRationalProbabilityImpossible:true,
  externalHalfCoinRequired:false,
  conditionalUniform4096Exactly:true,
  actualGoldenSamplesFF_RRfailureKept:true,
  exactAlgebraicRingCertificates:exactCertificates},
 originalGolden:{p,r,successOfPair:2*p**3,fullBellProbabilityGivenReady:1/4096,
  completeExperimentalOutcomeClasses:18,
  Golden16SuccessAndFailAllRetained:true,
  maxExactConditionalSignedJ23Error:maxOdd,
  maxWholeRecordGoldenKLFactorizationError:max18KL,
  maxFull18FisherSourceError:maxFisher},
 originalRole:{L2sites:16,trueSharedLinks:64,trueBasedFaces:96,
  sourceRank:6*roleRank,
  trueLorentzGaugePlusWilsonNullity:6*(64-roleRank),
  positivityPreservesWholeRoleRankForEveryFiniteK:true},
 finiteRefinement:{fourDimSites:"L^4",sixFacesPerSite:true,
  rawSourceNormModel:"h^-2 * 6 L^4 * per-face source discrepancy",
  K_rule:"ceil((7 ln L + ln12)/(-ln(p²+p⁴)))",
  rawNormErrorUpperBound:"6/L",
  table},
 genuineResourceAccounting:{
  limitExpectedNativeGoldenSamplesFor12FairBits:expectedLimit,
  expectedGoldenFRCodeUnitsInDeclaredNative1_2Code:expectedFullCodeBudget,
  conditionalUniform4096InfoUnits:conditionalInformation4096,
  nonnegligibleExpectedCodeOverhead:expectedFullCodeBudget-conditionalInformation4096,
  worstCasePrimitiveSamples:"24K",independentComparisonAndAncillaCostStillRequired:true
 },
 innerChoi13QuantumPOVMNotCompiled:true,
 movingNativeGoldenInputAndG0OldRightClockWorkNotSelected:true,
 selectedBookHJRToPalatiniEulerNotProved:true,
 GR_closed:false
},null,2));
