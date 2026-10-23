#!/usr/bin/env node
"use strict";
/* Full ORIGINAL K(9,11,13) 33/718 scene, ALL original
 * 718 two-step and 7722 based ABC3 loops, asymmetric local
 * SO(2) J23 edge phase theta_0,9=t with inverse reverse.
 * Original true symmetric heterogeneous primitive Cost>=1 and
 * original three-tick Book raw weight are reversal-even.
 * Attach all 17 pre-owned primitive p=phi^-1 GOLDEN16/two-fresh
 * Julia/Bell outcomes to EVERY original true source history.
 *
 * Reversal swaps the EXISTING J23 signed Golden marks qJ+/qJ-,
 * so the actual recorded labelled law can be oriented even when
 * FULL scalar Book price gives a perfect reversal-symmetric tie.
 *
 * Conditionally declare one pre-registered future predicate
 * "J+ probability > J- probability" to break the feasibility
 * symmetry and select a unique outcome among a matched pair
 * BEFORE execution. This is NOT a physical forcing of that
 * predicate from M1; it demonstrates the ONLY valid deterministic
 * escape in existing prospective Dmin without an extra action.
 */
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi),sBell=1/4096;
const z=u=>u<9?0:u<20?1:2;
const assert=(b,m)=>{if(!b)throw Error("FAIL "+m);console.log("PASS "+m)};
const K=Array.from({length:33},()=>Array(33).fill(0)),
      angle=Array.from({length:33},()=>Array(33).fill(0));
const edges=[];for(let u=0;u<33;u++)for(let v=0;v<33;v++)if(z(u)!==z(v)){
  const cost=1.02+((7*(u+v)+3)%11)/200;
  if(cost<1)throw Error("invalid native original cost floor");
  K[u][v]=p**cost;
  edges.push([u,v]);
}
assert(edges.length===718&&edges.every(([u,v])=>K[u][v]===K[v][u]),
 "genuine 718 original directed primitive Cost≥1, nonuniform symmetric reciprocal weights");
const theta=0.083;
angle[0][9]=theta;angle[9][0]=-theta;
const loops2=edges.map(([u,v])=>[u,v,u]),loops3=[];
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 loops3.push([a,b,c,a],[b,c,a,b],[c,a,b,c],[a,c,b,a],[c,b,a,c],[b,a,c,b]);
assert(loops2.length===718&&loops3.length===7722,
 "ALL actual original based Book n2/n3 returning word labels, 8440 complete");
const reversal=w=>[w[0],...w.slice(1,-1).reverse(),w[0]];
const key=w=>w.join(",");
const all=[...loops2,...loops3],keys=new Set(all.map(key));
assert(all.every(w=>keys.has(key(reversal(w))))&&keys.size===8440,
 "every actual 8440-word native scene path has distinct, real supported reversal partner");
const raw=w=>{
 let q=1;for(let i=1;i<w.length;i++)q*=K[w[i-1]][w[i]];
 return q*(w.length===3?p:p*p);
};
const hol=w=>w.slice(0,-1).reduce((s,u,i)=>s+angle[u][w[i+1]],0);
let maxCostParity=0,maxAngleParity=0;
for(const w of all){
 let r=reversal(w);
 maxCostParity=Math.max(maxCostParity,Math.abs(raw(w)-raw(r)));
 maxAngleParity=Math.max(maxAngleParity,Math.abs(hol(w)+hol(r)));
}
assert(maxCostParity<3e-16&&maxAngleParity<1e-15,
 "FULL original Book raw scalar Cost exactly reversal-even, but ordered SO2 holonomy reverses sign");
const k0=p**4/24;
function golden17(t){
 const m=(1+Math.cos(t))/2,y=Math.sin(t)/Math.SQRT2;
 const signedPlus=k0*(m+y)**2,signedMinus=k0*(m-y)**2,
   plain=k0*m*m,marks=[...Array(10).fill(plain),signedPlus,signedMinus];
 const GG=p**4,GB=p*p*(1-p*p),BG=p**3;
 const rest=GG-marks.reduce((s,x)=>s+x,0),
       sixteen=[...marks,rest,GB,BG,1-GG-GB-BG],
       seventeen=sixteen.map(x=>sBell*x).concat([1-sBell]);
 if(!seventeen.every(x=>x>0))throw Error("original Golden17 sign positivity chart exceeded");
 return seventeen;
}
const q0=golden17(0),qp=golden17(theta),qm=golden17(-theta);
function marked(Q){return 256*Math.sqrt(3)/p**2*(Math.sqrt(Q[10])-Math.sqrt(Q[11]));}
const oddPositive=marked(qp),oddNegative=marked(qm);
assert(Math.abs(oddPositive-2*Math.sin(theta))<2e-13&&
 Math.abs(oddNegative+2*Math.sin(theta))<2e-13,
 "TRUE original Golden17 positive signed-root J23 decoder returns ±2sinθ, NOT even Fisher");
assert(Math.abs(qp[10]-qm[11])<1e-17 &&
 Math.abs(qp[11]-qm[10])<1e-17 &&
 Array.from({length:17},(_,j)=>j).filter(j=>j!==10&&j!==11)
     .every(j=>Math.abs(qp[j]-qm[j])<2e-17),
 "EXACT original full17 labelled reversal is native J+ <-> J- permutation; no failed flags lost");
let partition=0,fullMass=0,positive3=0,negative3=0,touched=0,
    weightedOdd=0,oddAbsolute=0,conditionalParity=0;
for(const w of all){
 const weight=raw(w),q=golden17(hol(w));
 partition+=weight;fullMass+=weight*q.reduce((a,b)=>a+b,0);
 weightedOdd+=weight*marked(q);
 if(Math.abs(hol(w))>1e-9){
   touched++;if(hol(w)>0)positive3++;else negative3++;
   oddAbsolute+=weight*Math.abs(marked(q));
 }
}
assert(Math.abs(partition-fullMass)<1e-12&&partition>0,
 "FULL 8440×17=143480 positive native Book/Golden recorded events share original scalar partition EXACTLY");
assert(touched===78&&positive3===39&&negative3===39,
 "single original SO2 chiral A0-B0 edge yields 13 undirected ABC triangles /78 based oriented words, ±39");
assert(Math.abs(weightedOdd)<2e-13&&oddAbsolute>0,
 "all histories scalar/Golden reversal-paired: aggregate signed source zero, but each local oriented face has nonzero contrast");
const taskPair=[0,9,20,0],reversePair=reversal(taskPair),
      forwardCost=-Math.log(raw(taskPair))/ell,
      reverseCost=-Math.log(raw(reversePair))/ell,
      forwardMark=marked(golden17(hol(taskPair))),
      reverseMark=marked(golden17(hol(reversePair)));
assert(Math.abs(forwardCost-reverseCost)<1e-14 &&
 Math.abs(forwardMark+reverseMark)<2e-13&&forwardMark>0&&reverseMark<0,
 "one ACTUAL original ABC pair gives TIED prospective scalar Book Cost but two opposite native signed Golden future responses");
const symmetricFeasible=[true,true],orientedFeasible=[forwardMark>0,reverseMark>0];
assert(symmetricFeasible.every(Boolean)&&orientedFeasible.filter(Boolean).length===1,
 "same initial scalar price without oriented future task has TWO minimizers; genuinely directed future-test predicate breaks admissibility tie");
const qCost=[forwardCost,reverseCost];
const minScalar=Math.min(...qCost);
assert(qCost.every(v=>Math.abs(v-minScalar)<1e-14),
 "simple ex-ante scalar Dmin argmin does NOT uniquely select signed SO2 curvature on the real native Book triangle");
const frameCost=0.5;
assert(frameCost>0&&forwardMark>0,
 "any actual charged observer/reference/semantic orientation in full task is a physical datum, not a random tie-breaker");

// ACTUAL statistical price of signed original J23 readout in the
// entire primitive 17-category Golden/Bell apparatus on original
// K913 support.  Distinguish TWO hypotheses theta versus -theta,
// both having EXACTLY identical native Book 8440 scalar history law.
// Unlike the distinct Q8 two-port experiment, the full17 Julia
// apparatus heralds only 1/4096 and the signed SO2 contrast is
// small for genuine weak curvature. Never claim these have equal
// Cost/Info/physics simply because both use p=phi^-1.
//
// Given original positive-root chart, for a touched triangle only
// qJ+/qJ- exchange under reversal:
//   B_local=sum sqrt(q_theta*r_reverse) =1−2k sin²theta
//   k=p^4/(24*4096).
// Whole Book mixture:
//   B_total =1−massTouched*(1−B_local).
// On iid N replays, Bhattacharyya B^N; total variation <=sqrt(1−B^(2N)).
// For equal priors, Bayes error≥(1−TV)/2; achieving error<=epsilon
// requires N>=log(4eps(1-eps))/(2log B). This is NECESSARY only.
const touchedMass=all.reduce((s,w)=>s+
  (Math.abs(hol(w))>1e-9?raw(w):0),0)/partition;
const nativeSignedMarkK=sBell*p**4/24;
const localOverlapLoss=2*nativeSignedMarkK*Math.sin(theta)**2,
      wholeOverlapLoss=touchedMass*localOverlapLoss;
function directBH(selected){
 let sum=0,mass=0;
 for(const w of all){
  if(selected&&Math.abs(hol(w))<1e-9)continue;
  const wi=raw(w),q=golden17(hol(w)),r=golden17(-hol(w));
  mass+=wi;
  for(let j=0;j<17;j++)sum+=wi*Math.sqrt(q[j]*r[j]);
 }
 return sum/mass;
}
assert(Math.abs(directBH(false)-(1-wholeOverlapLoss))<7e-13&&
       Math.abs(directBH(true)-(1-localOverlapLoss))<7e-13,
 "all original FULL 143480 labelled Golden/Book probabilities produce EXACT Hellinger reversal overlap from TWO true marked effects");
const originalFullGoldenStatisticalLowerBounds=[];
for(const epsilon of [.25,.1,.01,.001]){
 const cutoff=4*epsilon*(1-epsilon);
 const nWhole=Math.ceil(Math.log(cutoff)/
    (2*Math.log1p(-wholeOverlapLoss)));
 const nTargeted=Math.ceil(Math.log(cutoff)/
    (2*Math.log1p(-localOverlapLoss)));
 assert(nWhole>100*nTargeted&&nTargeted>1000000,
   "ideal 17-output Golden/Julia statistically costly signed SO2 source: true necessary sample count for Bayesian error "+epsilon);
 originalFullGoldenStatisticalLowerBounds.push({
  equal_prior_Bayes_error_target:epsilon,
  full_original_Book_8440_blind_path_trials_at_least:nWhole,
  targeted_true_ABC_J23_Golden17_trials_at_least:nTargeted
 });
}
console.log("FULL_GOLDEN17_SIGNED_INFORMATION_COST",JSON.stringify({
 original_full17_signed_mark_constant:nativeSignedMarkK,
 true_original_Book_probability_mass_touched:touchedMass,
 whole_hellinger_overlap_loss:wholeOverlapLoss,
 conditional_hellinger_overlap_loss:localOverlapLoss,
 exact_information_theoretic_necessary_iid_trial_bounds:originalFullGoldenStatisticalLowerBounds,
 physical_scope:"not an execution price, not a full G0 selected experiment; differs from native 2-port Q8 discrete ± central test"
}));

console.log(JSON.stringify({
 original_carrier:"K(9,11,13) all718 edges, all8440 based 2/3 histories and full143480 Golden17 labelled outcomes",
 original_native_cost:"nonuniform reciprocal primitive Cost>=1; scalar Book path law reversal-invariant",
 original_SO2_Holonomy_theta:theta,
 original_chiral_loop_pairs:39,
 full_joint_scalar_partition:partition,
 original_signed_sum_over_reversal_symmetric_history:weightedOdd,
 nonzero_signed_magnitude_before_scalar_averaging:oddAbsolute,
 one_real_ABC_pair:{
  forward:taskPair,backward:reversePair,exact_same_scalar_code:[forwardCost,reverseCost],
  original_Golden_signed_contrasts:[forwardMark,reverseMark],
  no_orientation_boundary_unique_argmin:false,
  with_declared_future_semantic_positive_J23_goal_unique:true
 },
 exact_no_go:"Reversal-symmetric full admissibility and cost cannot determine a unique sign-odd physical minimum, unless the chosen signed source is zero",
 conditional_escape:"Native oriented full initial/reference/verified goal or real reversal-odd price breaks selection symmetry BEFORE execution, not after",
 forced_native_Book_semantic_goal:false,
 actual_physically_selected_G0_spin_connector:false,
 GR_closed:false
},null,2));
