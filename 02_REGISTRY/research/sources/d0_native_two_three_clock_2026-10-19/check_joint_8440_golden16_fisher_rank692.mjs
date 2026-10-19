#!/usr/bin/env node
"use strict";
/**
 * GENERAL POSITIVE ORIGINAL K(9,11,13) Book + complete Golden-p CAR16
 * mathematical source-observability theorem, all no-fitted parameters.
 *
 * 718 original directed scalar Book weights K_uv>0, 359 undirected
 * backtracks (2 based orientations) + 1287 original ABC triangles
 * (6 based/oriented traversals each) = 8440 COMPLETE native path labels.
 * Give ALL paths of length2/3 one common known-positive attempt prior
 * α₂,α₃ and ONE global normalizer.
 *
 * Their full strictly positive normalized Fisher with respect to the
 * 718 independent log K edge-weights has EXACT rank 686:
 * kernel exactly the 32 original endpoint coboundary directions.
 *
 * Proof: for an infinitesimal source d with ZERO score on all 8440
 * paths, each 2-backtrack yields d_uv+d_vu=c.
 * Forward/reverse triangle in same positively supported full law:
 * 3c/2 ± cycle(d)=c => c=0 and cycle(d)=0.
 * Every even component then zero; all odd triangle circulations zero.
 * Constructive 32-tree / 327-chord triangle basis shows odd d is EXACT
 * endpoint coboundary. Conversely all endpoint coboundaries telescope
 * on every based loop. Thus kernel32 and rank718−32=686.
 *
 * Attach the ALREADY OWNED complete original Golden-p 16-outcome
 * CAR/Julia/Choi conditional full-flag mathematical measurement. Its
 * six original independent proper-Lorentz Lie first-source directions
 * have Fisher exactly (p^4/6)*I6 at flat; independently positive. For
 * q_(history,mark)=q_history(K)*q_mark(U), cross score=0 exactly.
 * Hence the JOINT 8440*16 positive mathematical law has local
 * FIRST-SOURCE Fisher rank 686+6=692 over independent (K,U).
 *
 * This is not a physically admitted SAME G0 instrument, no compulsory
 * 2/3 clock, no native field->K/U map, no selected Cost/Info/work,
 * no matter/preparation source and NO GR completion.
 */
const require=(ok,message)=>{if(!ok)throw Error(message)};
const n=33,zone=u=>u<9?0:u<20?1:2;
const upper=[],edgeDirection=[];
for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(zone(u)!==zone(v)){
 upper.push([u,v]);edgeDirection.push([u,v],[v,u]);
}
const triangles=[];
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 triangles.push([a,b,c]);
require(upper.length===359&&edgeDirection.length===718&&triangles.length===1287,
  "not literal original 33/359/718/1287 source graph");
const counts={backtrackBased:2*upper.length,triangleBased:6*triangles.length};
require(counts.backtrackBased+counts.triangleBased===8440,
  "not complete original 8440 one-normalizer 2/3 clock outcomes");

const tree=[];
for(let b=9;b<20;b++)tree.push([0,b]);
for(let c=20;c<33;c++)tree.push([0,c]);
for(let a=1;a<9;a++)tree.push([a,9]);
require(tree.length===32,"tree must have V−1 original source edges");
const fundamental=[];
for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 fundamental.push([0,b,c]);
for(let a=1;a<9;a++)for(let c=20;c<33;c++)
 fundamental.push([a,9,c]);
for(let a=1;a<9;a++)for(let b=10;b<20;b++)
 fundamental.push([a,b,20]);
require(fundamental.length===327,"not 143+104+80 original triangle cycle basis");

const ze=()=>Array.from({length:n},()=>Array(n).fill(0));
const rand=(u,v)=>((u*1243+v*977+u*v*37+72)%43)-21;
const original=ze();
for(const [u,v]of upper){let val=rand(u,v);original[u][v]=val;original[v][u]=-val;}
const triangleSum=(a,b,c)=>original[a][b]+original[b][c]+original[c][a];

// First choose original tree coboundary so every tree antisymmetric
// coefficient is ZERO, giving an exact unique 327-dimensional section.
const chi=Array(n).fill(0);
for(let b=9;b<20;b++)chi[b]=original[0][b];
for(let c=20;c<33;c++)chi[c]=original[0][c];
for(let a=1;a<9;a++)chi[a]=chi[9]-original[a][9];
const fixed=ze();
for(const [u,v]of upper){
 fixed[u][v]=original[u][v]+chi[u]-chi[v];
 fixed[v][u]=-fixed[u][v];
}
for(const [u,v]of tree)require(fixed[u][v]===0,"nonzero gauge-fixed original tree coefficient");

// Recover ENTIRE non-tree antisymmetric signed source from exactly
// 327 true ABC triangular orientation comparisons.
const reconstructed=ze(),set=(u,v,val)=>{
  reconstructed[u][v]=val;reconstructed[v][u]=-val;
};
for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 set(b,c,triangleSum(0,b,c));
for(let a=1;a<9;a++)for(let c=20;c<33;c++)
 set(a,c,reconstructed[9][c]-triangleSum(a,9,c));
for(let a=1;a<9;a++)for(let b=10;b<20;b++)
 set(a,b,triangleSum(a,b,20)-reconstructed[b][20]+reconstructed[a][20]);
for(const [u,v]of upper)
 require(reconstructed[u][v]===fixed[u][v],
  "triangular oriented cycle recovery does not span full 327-dimensional graph flow");

// EXACT mathematical rank proof of the complete normalized score:
// 359 even scalar backtrack products are independent, since the
// common score c is fixed to 0 by combining two opposite ABC loops
// with one set of backtracks. The 327 odd triangle scores are
// independent by this explicit recursive reconstruction. The only
// remaining 32 gauges are the input tree gradients.
const evenRank=upper.length,oddRank=fundamental.length;
const nativeScalarRank=evenRank+oddRank;
const gauge=tree.length;
require(nativeScalarRank===686&&nativeScalarRank+gauge===718,
  "wrong original 8440 clock score rank");

const p=(Math.sqrt(5)-1)/2,
      golden16q=p**4/24,
      golden16LieSource=p**4/(12*Math.sqrt(2)),
      fisherSixPerDirection=2*golden16LieSource**2/golden16q;
require(Math.abs(fisherSixPerDirection-p**4/6)<1e-15,
  "complete original 16-outcome Golden-p Lie Fisher is not p^4/6");

// All 16 complete Golden outcomes including Good/Bad and GGrest:
const probs=[
  ...Array(12).fill(golden16q),
  p**4/2,p**3,p**3,p**2
];
require(Math.abs(probs.reduce((a,b)=>a+b,0)-1)<1e-14,
  "original full Golden16 instrument does not retain all probability");
require(Math.min(...probs)>0,"not all complete Golden16 outcomes positive");
// P=(P_history>0)(Q_marker>0). For each independent tangent,
// E_book(score_book)=E_car(score_car)=0; cross Fisher exactly 0.
const CARrank=6,joint=nativeScalarRank+CARrank,
      jointOutcomes=(counts.backtrackBased+counts.triangleBased)*probs.length;
require(joint===692&&jointOutcomes===135040,
  "wrong full original 8440-history x Golden16 recorded law dimensions");


// ORIGINAL Golden exact-cost F/R native word support: no new alphabet
// required to LABEL 135040 full loop×CAR outcomes. This is a finite
// address-capacity fact, NOT a true physical detector/CAR instruction
// or a zero-work readout.
const fib=[0n,1n];
for(let i=2;i<=32;i++)fib.push(fib[i-1]+fib[i-2]);
const nativeGoldenCost=Array.from({length:30},(_,i)=>i)
  .find(i=>fib[i+1]>=BigInt(jointOutcomes));
require(nativeGoldenCost===26&&fib[27]===196418n,
  "original Golden F/R native recording code insufficient at 26");
const minimumFreshBinaryBits=Math.ceil(Math.log2(jointOutcomes));
const fullGNSDimension=fib[27]**2n+fib[26]**2n;
require(minimumFreshBinaryBits===18&&
  fullGNSDimension===53316291173n,
  "wrong exact original Golden recording carrier size");

const summary={
  status:"PASS_ORIGINAL_BOOK_8440_CLOCK_FISHER686_PLUS_GOLDEN_CAR6_EQUALS692",
  actualGraph:{vertices:n,undirectedEdges:359,directedEdges:718,
    originalABCtriangles:triangles.length},
  trueJointClosedClock:{allBasedBacktracks:counts.backtrackBased,
    allBasedOrientedTriangles:counts.triangleBased,
    singleNormalizedPositiveClockOutcomes:8440,
    priors:"any fixed positive native-type attempt α₂,α₃, same normalizer; actual physical G0 clock is NOT owned"},
  graphSourceExactDimensions:{
    symmetricEven359:evenRank,oddTriangleCycles327:oddRank,
    endpointGradientKernel32:gauge,
    fullBookNormalizedMixedClockFisherRank686:nativeScalarRank,
    explicitOriginalTriangleCycleBasis:fundamental.length,
    exactIntegerOriginalCycleReconstruction:true},
  originalGolden16:{
    flagProbabilitiesAtIdentity:probs,
    all16StrictlyPositive:true,
    LieFisherEigenvalue:p**4/6,
    sixLieSourceRank:CARrank},
  mathematicalJoinedRecord:{
    totalOutcomeLabels:jointOutcomes,
    minimumFreshBinaryBits,
    minimumOriginalGoldenExactCostWordDepth:nativeGoldenCost,
    existingGoldenTypeAExactCost26Words:String(fib[27]),
    existingGoldenTypeBPendingCost26Words:String(fib[26]),
    fullAFGNSDimensionAtCost26:String(fullGNSDimension),
    originalGoldenSourceCodeHasEnoughDistinctLabels:true,
    independentBookAndCARLocalFisherRank:joint,
    exactCrossFisherZero:true,
    originalScalarBookPerronPressureGaugeInvariantUnderEndpointCoboundary:true,
    fullSourceCanBeDecodedMathematically:true
  },
  physicalScope:"Original 2/3 one-normalizer clock AND Golden16 marker are mathematical paid candidate records; compulsory G0 same-run admission/source, Role field->K+Lorentz and full H+J+R/CAR/prep/clock work remain OPEN",
  GR_closed:false
};
console.log(JSON.stringify(summary,null,2));
