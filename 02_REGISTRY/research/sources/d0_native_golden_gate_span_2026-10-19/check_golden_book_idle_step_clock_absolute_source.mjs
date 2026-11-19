#!/usr/bin/env node
"use strict";
/**
 * Literal original GoldenCoherentMemory.fullStep with blank system/record:
 *   fullStep*[1,0,0,0]^T = [sqrt(p),0,0,p]^T.
 * EXACT Book odds matching of the TRUE two outcomes under primitive
 * identity Cost=0 and nonidentity Cost=1, with zero relative vertex Info:
 *   w_idle=1, w_transition=p, (q_idle,q_transition)=(p,p²).
 *
 * New decisive original ActionProtocol-fiber discriminator:
 * if the COMPLETE same-normalizer Book/Born pair binds these ACTUAL
 * pointer outcomes for all field points, its NET relative Cost−Info
 * is forced to exactly 1 on that open chart. It is NOT a theorem that
 * original G0/Book03 makes that physical binding or prices the full
 * clock/prep/work equally.
 *
 * C(t)=1+t²: its relative Book full flag is q(t)=p^(1+t²)/
 * (1+p^(1+t²)), with q''(0)=−2 log(phi)*p³, but the FIXED
 * literal Golden gate has constant q_G=p² and q_G''=0.
 * Thus equality only at a vacuum point and its FIRST jet is not enough.
 *
 * The original SAME full K(9,11,13) Perron trace has a length-defect
 * blind mode ONLY if each depth is normalized separately. Any
 * physically SAME-CLOCK positive two-length mixture with known
 * field-independent depth preparation sees a common excess Cost c(t):
 *   log_phi Odds_(n+1)/Odds_n changes by exactly -c(t).
 * The data of such a two-length experiment are mathematical here.
 * No compulsory multi-depth G0 readout/clock law is asserted.
 */
const require=(ok,message)=>{if(!ok)throw Error(message)};
const phi=(1+Math.sqrt(5))/2,p=1/phi,a=Math.sqrt(p),ell=Math.log(phi);
require(Math.abs(p+p*p-1)<1e-15,"wrong primitive Golden p");
const full=[
  [a,0,-p,0],
  [0,a,0,-p],
  [0,p,0,a],
  [p,0,a,0]
];
const amp=full.map(row=>row[0]),probs=amp.map(x=>x*x);
require(Math.abs(probs[0]-p)<1e-15&&Math.abs(probs[3]-p*p)<1e-15,
  "literal fullStep blank law not p,p²");
require(probs[1]===0&&probs[2]===0,"literal old record not a correlated two-branch state");
const oddsGate=probs[3]/probs[0];
require(Math.abs(oddsGate-p)<1e-15,
  "literal Golden two-event relative odds is not primitive p");

const qBornChange=p*p;
const qBookChange=c=>{
  const r=Math.exp(-ell*(1+c));
  return r/(1+r);
};
const netCostFromFullFlag=(qIdle,qChange)=>
  -Math.log(qChange/qIdle)/ell;
require(Math.abs(qBookChange(0)-qBornChange)<1e-15,
  "canonical identity/step Book/Born equality failed");
require(Math.abs(netCostFromFullFlag(probs[0],probs[3])-1)<2e-15,
  "true Golden pointer does not fix one relative Book quantum");

const q0=qBookChange(0),secondExact=-2*ell*p**3;
const tlist=[.2,.1,.05,.025,.0125];
const derivatives=tlist.map(t=>({
  t,
  bornMean:qBornChange,
  bookMean:qBookChange(t*t),
  difference:qBookChange(t*t)-qBornChange,
  bookSecondCentral:(qBookChange(t*t)+qBookChange(t*t)-2*q0)/(t*t),
  expectedSecond:secondExact
}));
for(let e of derivatives)require(e.difference<0,"extra true native Cost did not suppress success probability");
require(Math.abs(derivatives.at(-1).bookSecondCentral-secondExact)<1e-5,
  "false second-jet calculation for original Golden book success probability");

const N=33,part=i=>i<9?0:i<20?1:2,neighbors=Array.from({length:N},(_,i)=>
  Array.from({length:N},(_,j)=>part(i)!==part(j)?j:-1).filter(j=>j>=0));
require(neighbors.reduce((s,r)=>s+r.length,0)===718,"not actual 718-edge original scene");
let counts=Array(N).fill(0n);counts[0]=1n;
const rawPathCounts=[1n];
for(let m=1;m<=9;m++){
  const next=Array(N).fill(0n);
  for(let i=0;i<N;i++)if(counts[i])for(let j of neighbors[i])next[j]+=counts[i];
  counts=next;
  rawPathCounts.push(counts.reduce((s,x)=>s+x,0n));
}
const depth=4,alpha=p,beta=p*p; // existing primitive Golden branch weights, optional mathematical two-depth clock.
function clockOdds(costExcess){
  const z0=Number(rawPathCounts[depth])*p**depth,
        z1=Number(rawPathCounts[depth+1])*p**(depth+1);
  const val0=alpha*z0*Math.exp(-ell*depth*costExcess),
        val1=beta*z1*Math.exp(-ell*(depth+1)*costExcess);
  const total=val0+val1;
  return {q0:val0/total,q1:val1/total,odds:val1/val0,
          allPathsRetained:rawPathCounts[depth].toString()+"/"+rawPathCounts[depth+1].toString()};
}
const clock0=clockOdds(0);
const clockSamples=tlist.map(t=>{
  const c=t*t,C=clockOdds(c);
  const recovered=-Math.log(C.odds/clock0.odds)/ell;
  require(Math.abs(recovered-c)<2e-14,"clock failed to recover uniform primitive excess");
  return {t,relativeUniformExtra:c,clockShortProbability:C.q0,
    clockLongProbability:C.q1,relativeLogOddsShift:-c,recovered};
});

const varLength=clock0.q0*clock0.q1; // n and n+1 only
require(varLength>0,"multi-depth length Fisher must be positive");
const costFisher=ell*ell*varLength;
const primitiveGoldenLengthFisher=ell*ell*p**3;
require(Math.abs(probs[0]*probs[3]-p**3)<1e-14,"true literal primitive Golden length variance mismatch");
// ALL ORIGINAL vertices of each native path are charged in the BOOK03
// vertex sum. A uniform edge Cost excess c and a uniform vertex-Info
// increase i change every full path of length m by:
//       Delta S = m*c − (m+1)*i = m*(c−i)−i.
// Thus full normalized ANY-depth laws sense only c−i. The extra
// global i is an absolute unnormalised partition factor, invisible even
// to complete positive clock flags.
const prior0=alpha*Number(rawPathCounts[depth])*p**depth;
const prior1=beta*Number(rawPathCounts[depth+1])*p**(depth+1);
function costInfoJoint(c,i){
  const z0=prior0*Math.exp(-ell*(depth*c-(depth+1)*i)),
        z1=prior1*Math.exp(-ell*((depth+1)*c-(depth+2)*i)),
        z=z0+z1;
  return {q0:z0/z,q1:z1/z,relativeAbsolutePartitionAction: -Math.log(z/(prior0+prior1))/ell};
}
const jointControls=[0.01,0.04,0.11].map(c=>{
  const gain=costInfoJoint(c,c),costOnly=costInfoJoint(c,0);
  require(Math.abs(gain.q0-clock0.q0)<4e-15&&
    Math.abs(gain.q1-clock0.q1)<4e-15,
    "uniform Cost+Info gauge affected true recorded clock law");
  require(Math.abs(gain.relativeAbsolutePartitionAction+c)<4e-14,
    "finite whole-path Book partition did not retain endpoint Info absolute scale");
  require(Math.abs(costOnly.q1-clock0.q1)>1e-5,
    "clock failed to reveal unpaired real Cost excess");
  return {c,normalizedClockUnchangedWhenInfoAlsoMoves:true,
    sameCostInfoWholeBookActionShift:-c,
    recordedUnpairedCostFlagChange:costOnly.q1-clock0.q1};
});
const fisherCostInfo=[
  [costFisher,-costFisher],
  [-costFisher,costFisher]
];


// Exact original full K9/11/13 path-count Perron growth: at each n
// Z_n = 1_(start a0)^T (p A)^n 1. Since K=p A is primitive
// (both 2- and 3-return cycles), Z_(n+1)/Z_n -> lambda=p*rho.
// If a PHYSICAL common-clock complete law compares consecutive n
// with field-INDEPENDENT known priors alpha_n, the ratio of their
// absolute depth marginals estimates lambda without a NEW meter:
//    lambda = lim (alpha_n/alpha_(n+1)) q(n+1)/q(n).
// Existing Golden/GNS mathematical levels do NOT prove native scene
// G0 actually retains such a compulsory clock mixture.
const countsAll=[1n];
let tails=Array(N).fill(0n);tails[0]=1n;
for(let n=1;n<=24;n++){
  const next=Array(N).fill(0n);
  for(let u=0;u<N;u++)if(tails[u])for(let v of neighbors[u])next[v]+=tails[u];
  tails=next;
  countsAll.push(tails.reduce((s,x)=>s+x,0n));
}
const originalRho=(function(){
  let lo=20,hi=24;
  for(let j=0;j<90;j++){
    const m=(lo+hi)/2;
    if(m**3-359*m-2574>0)hi=m;else lo=m;
  }
  return (lo+hi)/2;
})();
const nativeLambda=p*originalRho;
const perronRatios=[4,8,12,16,20,23].map(n=>({
  depth:n,
  exactTotalPaths:String(countsAll[n]),
  ratioRawBookDepths:p*Number(countsAll[n+1])/Number(countsAll[n]),
  nativeAbsolutePerronLambda:nativeLambda
}));
require(Math.abs(perronRatios.at(-1).ratioRawBookDepths-nativeLambda)<1e-4,
  "absolute original pressure not recovered from true all-path depth ratio");

const kthFlatControls=[];
for(let m of [2,3,4,5]){
  const c=t=>t**(2*m), h=.2;
  const change=clockOdds(c(h));
  kthFlatControls.push({m,firstDifferentDerivativeOrder:2*m,
    sameAllFieldJetsThrough:2*m-1,
    normalizedFixedDepthInvariance:true,
    genuineMixedDepthDifference:change.odds-clock0.odds});
}
function flatExcess(t){return t===0?0:Math.exp(-1/(t*t))}
const smooth=[.2,.3,.4].map(t=>({
  t,flatExcess:flatExcess(t),
  clockOddsDifferent:clockOdds(flatExcess(t)).odds!==clock0.odds
}));
require(smooth.every(e=>e.clockOddsDifferent),
  "smooth flat nonlinear ambiguity not picked up by off-shell clock");
const result={
  status:"PASS_ORIGINAL_GOLDEN_BOOK_IDENTITY_STEP_CLOCK_ABSOLUTE_SOURCE",
  originalBlankFullStepAmplitudes:amp,
  originalCompleteGoldenFlags:{idle:probs[0],nonidentity:probs[3],odds:oddsGate},
  bookSameNormalizerPair:{
    costs:[0,1],unnormalizedWeights:[1,p],
    normalizedFlagProbabilities:[1/(1+p),p/(1+p)],
    exactSymbolicConsequence:"p+p²=1 ⇒ (1/(1+p),p/(1+p))=(p,p²)",
    netRelativeCostFromRealGoldenPointer:1,
    logicalGate:"physical SAME-history Book/Born idle-vs-transition identification with all prep/clock/work/Info correctly priced is OPEN"
  },
  primitiveMathematicalExtraCost:{
    c:"t²",sameFlagAtOrigin:true,sameFirstDerivativeAtOrigin:true,
    distinctSecondNativeBookPointer:true,
    bookSuccessSecondDerivative:secondExact,
    literalFixedGoldenSuccessSecondDerivative:0,
    tControls:derivatives
  },
  sceneFullClockConditional:{
    originalGraph:"K(9,11,13)",edges:718,
    startingVertex:0,
    shortDepth:depth,longDepth:depth+1,
    exactNumberOfAllOriginalPaths:[String(rawPathCounts[depth]),String(rawPathCounts[depth+1])],
    clockPrior:"mathematical fixed α=p, β=p²; native physical clock mix is NOT selected",
    canonicalClockLongProbability:clock0.q1,
    extraCostIdentity:"log_phi(odds(c)/odds(0))=-c for adjacent depths",
    trueNormalizedAllOutcomes:true,
    samples:clockSamples,
    PerronDepthRatios:perronRatios,
    nativeAbsoluteLambda:nativeLambda,
    PerronRecoveryAssumptions:"true shared clock-depth marginal + known relative preparation; original K positive primitive; physical G0 clock law not proved",
    exactLengthVariance:varLength,
    exactUniformCostFisher:costFisher,
    primitiveGoldenOneTickCostFisher:primitiveGoldenLengthFisher,
    FisherCostInfoMatrix:fisherCostInfo,
    exactFisherRankWithCostAndInfo:1,
    fullBook03UniformShiftIdentity:"Delta S_gamma=m*(c-i)-i for m edges, m+1 visited vertices",
    jointCostInfoGaugeControls:jointControls
  },
  deepJetWarning:{
    admissibleAnalyticExcessFamilies:kthFlatControls,
    smoothFlatExcessCInfinity:"c(t)=exp(-1/t²) for t≠0, c(0)=0 has ALL derivatives 0 at origin but nonzero off-shell",
    smoothOffShellCheck:smooth,
    conclusion:"No finite jet order, or all C∞ jets at a single point without analyticity, select compulsory absolute Book Cost; need open-chart binding or actual clock."
  },
  GR_closed:false
};
console.log(JSON.stringify(result,null,2));
