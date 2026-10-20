#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL D0 K(9,11,13) based 718 2-tick + 7722 3-tick histories,
 * original Golden p=phi^-1, ALL native 17 positive two-fresh/Bell outputs.
 * Full 8440*17 joint weights (NO discarded failure or unsupported path).
 *
 * Exact algebraic results:
 *   sum_{gamma,r} w_gamma q_{r|gamma}(U) = sum_gamma w_gamma;
 *   conditional information Cost-Info is a KL with unique ν=q optimum;
 *   stationary elimination cancels ALL q geometry first/second/ALL jets,
 *   despite STRICT positive full17 conditional Fisher/Petz loss;
 *   original per-path signed sqrt Golden J23 readout stays orientation-odd.
 *
 * Research only. Mathematical conditional Golden17 apparatus on original
 * scene histories; true M1/G0 implementation, paid controller/oldRIGHT,
 * full128 coherent/coded port, signed 4D action selection not established.
 */
const check=(p,s)=>{if(!p)throw Error("FAIL "+s);};
const phi=(1+Math.sqrt(5))/2,p=1/phi,ell=Math.log(phi),bell=1/4096;
const V=33,zone=u=>u<9?0:(u<20?1:2),verts=Array.from({length:V},(_,i)=>i);
const edges=[],edgeidx=Array.from({length:V},()=>Array(V).fill(-1));
for(let u=0;u<V;u++)for(let v=0;v<V;v++)if(zone(u)!==zone(v)){
  edgeidx[u][v]=edges.length;edges.push([u,v]);
}
check(edges.length===718,"original K(9,11,13) 718 directed edges");
const histories=[];
for(const [u,v] of edges)histories.push({verts:[u,v,u],orient:0});
const parity3=z=>(z[0]===0&&z[1]===1&&z[2]===2)||
                   (z[0]===1&&z[1]===2&&z[2]===0)||
                   (z[0]===2&&z[1]===0&&z[2]===1)?1:-1;
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++){
  const six=[[a,b,c,a],[a,c,b,a],[b,c,a,b],
    [b,a,c,b],[c,a,b,c],[c,b,a,c]];
  for(const vertices of six)histories.push({
    verts:vertices,orient:parity3(vertices.slice(0,3).map(zone))});
}
check(histories.length===8440&&histories.filter(h=>h.orient>0).length===3861&&
      histories.filter(h=>h.orient<0).length===3861,
 "whole original 718+7722 true based paths with reversed orientation");

const cost=(u,v,y,t)=>1.22+.013*((u+7*v)%9)+
   .018*y*(((3*u+5*v)%11)-5)/6+
   .008*t*(((11*u+7*v)%13)-6)/6;
const info=(u,y)=>.44+.009*(u%7)+.021*y*(u%5-2)/2;
const priors={2:p,3:p*p}; // stated original-type fixed stage profile; not compulsory clock
function weight(hist,y,t){
  const vs=hist.verts,depth=vs.length-1;
  let c=0,ii=0;
  for(let j=0;j<depth;j++){
    check(edgeidx[vs[j]][vs[j+1]]>=0,"full original supported edge");
    const cc=cost(vs[j],vs[j+1],y,t);
    check(cc>=1,"true original ActionProtocol primitive Cost floor");
    c+=cc;
  }
  // Exact BOOK_03 full vertex Info (including the final return root).
  for(const u of vs)ii+=info(u,y);
  return priors[depth]*Math.exp(-ell*(c-ii));
}
const c=p**4*bell/24,flat=()=>{
  const GG=bell*p**4,GB=bell*p*p*(1-p*p),BG=bell*p**3;
  return {GG,GB,BG,BB:bell-GG-GB-BG};
};
function golden17(theta){
  const m=(1+Math.cos(theta))/2,s=Math.sin(theta)/Math.SQRT2;
  const q=[];for(let k=0;k<6;k++){
    const x=(k===4?s:0);
    q.push(c*(m+x)**2,c*(m-x)**2);
  }
  const norm=flat();
  q.push(norm.GG-q.reduce((x,v)=>x+v,0),
    norm.GB,norm.BG,norm.BB,1-bell);
  check(q.length===17&&q.every(v=>v>0),"full original 17-way GOOD/BAD including 4095/4096 fail");
  const z=q.reduce((a,b)=>a+b,0);
  check(Math.abs(z-1)<5e-16,"Golden17 all outcomes normalized");
  return q;
}
const H=q=>-q.reduce((s,v)=>s+v*Math.log(v),0)/ell;
const KL=(v,q)=>v.reduce((s,x,i)=>s+x*Math.log(x/q[i])/ell,0);
function nativeRun(y,t,perturb=false){
 const book=histories.map(h=>weight(h,y,t)),Z=book.reduce((a,b)=>a+b,0);
 const obs=new Map([[0,golden17(0)],[1,golden17(t)],[-1,golden17(-t)]]);
 let fineZ=0,fullEntropy=0,pointerMoving=0,pretrace=0,probOrient=0,flagFisher=0;
 const groups=[];
 for(let i=0;i<histories.length;i++){
   const w=book[i],sigma=histories[i].orient,q=obs.get(sigma),pr=w/Z;
   const wsum=w*q.reduce((s,a)=>s+a,0);fineZ+=wsum;
   // Extract original signed Golden J23 mark root, with positive complete q.
   const signed=256*Math.sqrt(3)/(p*p)*(Math.sqrt(q[8])-Math.sqrt(q[9]));
   check(Math.abs(signed-2*Math.sin(sigma*t))<1e-13,
     "native conditional positive-root signed geometry is 2sin(orientation*t)");
   pretrace+=pr*signed;
   probOrient+=pr*sigma;
   pointerMoving+=pr*H(q);
   fullEntropy+=pr*(-Math.log(pr)/ell+H(q));
   // NONCONST true historical label probabilities all positive.
   if(i===0||i===718||i===histories.length-1)groups.push({
    idx:i,depth:histories[i].verts.length-1,orient:sigma,
    BookProbability:pr,Golden17FailureProb:q[16]});
 }
 check(Math.abs(fineZ/Z-1)<8e-13,"ENTIRE full8440*17 partition exactly equals original scalar Book Z");
 check(Math.abs(pretrace-2*Math.sin(t)*probOrient)<4e-13,
 "full pretrace signed Book cycle expectation retains odd Golden source");
 return {Z,book,fineZ,pointerMoving,fullEntropy,pretrace,
  probOrient,goldenByOrient:obs,groups};
}
// ACTUAL all8440 ×17 history, moving native Cost+Info and moving CAR readout.
const y=.14,t=.19,R=nativeRun(y,t),R0=nativeRun(y,0);
check(Math.abs(R.pointerMoving-R0.pointerMoving)>1e-9,
 "complete native Golden17 pointer entropy genuinely moves, even though Book fine Z does not");
check(Math.abs(R.pretrace)>1e-8,"true Book orientation memory has NONZERO native signed Golden geometric mark");
const h=2e-4;
const Zprice=(yy,tt)=>-Math.log(nativeRun(yy,tt).Z)/ell;
const Fprice=(yy,tt)=>-Math.log(nativeRun(yy,tt).fineZ)/ell;
const vBook=(Zprice(y,t+h)-Zprice(y,t-h))/(2*h),
      vFine=(Fprice(y,t+h)-Fprice(y,t-h))/(2*h);
check(Math.abs(vBook-vFine)<5e-9,"first true moving scene source exact cancellation of conditional q_score");
const secF=(Fprice(y,t+h)-2*Fprice(y,t)+Fprice(y,t-h))/h**2;
const secB=(Zprice(y,t+h)-2*Zprice(y,t)+Zprice(y,t-h))/h**2;
check(Math.abs(secF-secB)<7e-7,"second native Book source unaffected by complete normalized Golden measurements");

const q0=golden17(0),qt=golden17(.19),Hdiff=H(qt)-H(q0);
check(Math.abs(Hdiff)>1e-7,"full Golden pointer Shannon has a real moving source on original J23");
const oneFisher=bell*p**4/6;
const dp=golden17(h).map((x,i)=>(x-golden17(-h)[i])/(2*h));
const finiteFI=dp.reduce((s,x,i)=>s+x*x/q0[i],0);
// STRICT Fisher/Petz loss alongside the ZERO scalar action source loss.
// At t=0 the complete Book history score may move; every 3-tick
// path has native Golden J23 score ±, two-tick paths have no angle.
// Conditional score mean=0, so the cross-history Fisher term vanishes.
const FIbase=nativeRun(y,0),bookPrice=FIbase.book,ZFI=FIbase.Z;
let dLogRaw=[],meanLogRaw=0,threeStageMass=0;
for(let i=0;i<histories.length;i++){
 const vs=histories[i].verts,dep=vs.length-1;
 let dc=0;
 for(let j=0;j<dep;j++)
   dc+=.008*(((11*vs[j]+7*vs[j+1])%13)-6)/6;
 const dl=-ell*dc;
 dLogRaw.push(dl);meanLogRaw+=(bookPrice[i]/ZFI)*dl;
 if(histories[i].orient!==0)threeStageMass+=bookPrice[i]/ZFI;
}
let fisherBook=0,fisherJoint=0;
for(let i=0;i<histories.length;i++){
 const pr=bookPrice[i]/ZFI,scoreBook=dLogRaw[i]-meanLogRaw;
 const sign=histories[i].orient,q=FIbase.goldenByOrient.get(sign);
 let fiCond=0;
 for(let j=0;j<17;j++){
  const dq=(sign===0?0:sign*dp[j]);
  const score=scoreBook+dq/q[j];
  fisherJoint+=pr*q[j]*score*score;
  fiCond+=dq*dq/q[j];
 }
 fisherBook+=pr*scoreBook*scoreBook;
 if(sign!==0)check(Math.abs(fiCond-oneFisher)<2e-10,
  "both original triangle orientations carry same complete native Golden17 Fisher");
}
const predictedFisherLost=threeStageMass*oneFisher;
check(predictedFisherLost>0&&Math.abs(fisherJoint-fisherBook-predictedFisherLost)<2e-11,
 "true all143480 positive labels have strictly more Fisher than Book alone, yet exact identical scalar log partition");

check(Math.abs(finiteFI-oneFisher)<2e-10,
 "TRUE ALL17 conditional Fisher = Bell*p^4/6, only two native signed marks moving");

// COMPLETE conditional-record Gibbs principle exact, no arbitrary record penalty.
// q(U) is the same true native positive law used in the code length
// L_r=-log_phi q_r and distinguishability gain H_phi(ν).
// C(ν;U)=E_ν L_r(U)−H_phi(ν)=D_phi(ν||q(U)).
const codeMinusInfo=(nu,q)=>{
  const cost=nu.reduce((s,v,i)=>s-v*Math.log(q[i])/ell,0);
  return cost-H(nu);
};
check(Math.abs(codeMinusInfo(qt,qt))<2e-13&&
 Math.abs(KL(qt,qt))<2e-13,
 "true moving q record stationary Cost−Info ZERO, no fitted subtraction");
const kfixed=codeMinusInfo(q0,qt);
check(kfixed>0,"if record law incorrectly FROZEN, real relative information source appears");
check(Math.abs(kfixed-KL(q0,qt))<2e-13,"entire Cost−Info equals KL to actual moving Golden law");
// At t=0: fixed-record Hessian has positive Fisher; allowing true moving
// ν=q(t) cancels it exactly by Schur / Gibbs envelope.
const kPlus=codeMinusInfo(q0,golden17(h)),
      kMinus=codeMinusInfo(q0,golden17(-h));
const finiteFixedH=(kPlus+kMinus-2*codeMinusInfo(q0,q0))/h**2;
const predictedFixedH=oneFisher/ell;
check(Math.abs(finiteFixedH-predictedFixedH)<1e-8,
 "positive raw fixed-record Fisher Hessian from ALL 17 real outcomes");
const relaxedPlus=codeMinusInfo(golden17(h),golden17(h));
const relaxedMinus=codeMinusInfo(golden17(-h),golden17(-h));
const relaxedH=(relaxedPlus+relaxedMinus-2*codeMinusInfo(q0,q0))/h**2;
check(Math.abs(relaxedH)<8e-8,
 "full actual normalized record internally relaxed Schur Hessian is EXACT ZERO");

// FULL 143480-outcome Gibbs variational identity and conditional KL chain,
// by sampling actual posterior and a genuinely nonoptimal conditional tape.
const N=histories.length,posterior=R.book.map(w=>w/R.Z);
let exactObjective=0,splitPath=0,conditionalGap=0,perturbedObjective=0;
const mix=.11,other=golden17(.31);
for(let i=0;i<N;i++){
  const pr=posterior[i],q=R.goldenByOrient.get(histories[i].orient);
  const Lg=-Math.log(R.book[i])/ell;
  const baselineRef=1/N;
  for(let j=0;j<17;j++){
    const nu=pr*q[j],mu=baselineRef*q[j];
    exactObjective+=nu*(Lg+Math.log(nu/mu)/ell);
    const altered=(1-mix)*q[j]+mix*other[j],
      nuPert=pr*altered;
    perturbedObjective+=nuPert*(Lg+Math.log(nuPert/mu)/ell);
  }
  splitPath+=pr*(Lg+Math.log(pr*N)/ell);
  conditionalGap+=pr*KL(q,q);
}
const targetObjective=Math.log(N)/ell-Math.log(R.Z)/ell;
check(Math.abs(exactObjective-targetObjective)<8e-11,
 "whole 143480 strict-positive joint Gibbs optimum is actual Book Z plus fixed counting constant");
check(Math.abs(splitPath-targetObjective)<8e-11&&Math.abs(conditionalGap)<8e-13,
 "EXACT KL chain: history cost+path KL plus unique conditional Golden record KL");
check(perturbedObjective>targetObjective+1e-9,
 "nonoptimal moving full Golden conditional record pays STRICT positive relative-code gap");

// The fixed-pointer *true native original GOLDEN CODE REFERENCE* may not
// match measured q. This is an independent physical source NOT cancelled.
// Original genuine nonblank full128: measured k=(p²,p), code=(p,p²),
// divergence in phi units is p-p²=p³ > 0.
const portCode=KL([p*p,p],[p,p*p]);
check(Math.abs(portCode-p**3)<3e-15,
 "REAL full128 native mismatch retained: self-information cancellation not a complete Book no-go");

// STRONGER M1/MDL no-go: NO probability-only optimal full Golden17 code
// can supply an ORIENTATION-ODD first source. This holds for ANY admissible
// codebook set invariant under permitted relabeling, not only Shannon.
// Verify with 17 actual native F/R prefix leaves (F Cost1, R Cost2).
const wordCost=w=>[...w].reduce((z,x)=>z+(x==="F"?1:2),0);
let leaves=["F","R"];
while(leaves.length<17){
 const candidates=leaves.map((w,i)=>({w,i,depth:wordCost(w)}))
    .filter(o=>o.w!=="F").sort((a,b)=>a.depth-b.depth||a.i-b.i);
 const picked=candidates[0];leaves.splice(picked.i,1,picked.w+"F",picked.w+"R");
}
check(leaves.length===17&&new Set(leaves).size===17&&
 leaves.every((w,i)=>leaves.every((v,j)=>i===j||!v.startsWith(w))),
 "17 true prefix-free original F/R codewords, no extra letter primitive");
const costs=leaves.map(wordCost).sort((a,b)=>a-b);
const optimalCodeValue=q=>q.slice().sort((a,b)=>b-a)
  .reduce((total,v,i)=>total+v*costs[i],0);
const codeFixed=q=>q.reduce((total,v,i)=>total+v*wordCost(leaves[i]),0);
const pplus=golden17(.19),pminus=golden17(-.19);
const optimalPos=optimalCodeValue(pplus),optimalNeg=optimalCodeValue(pminus);
check(Math.abs(optimalPos-optimalNeg)<1e-13,
 "ANY label-reassignable original F/R code optimal COST is REVERSAL EVEN");
const distinctPairs=golden17(.19);
check(distinctPairs[8]!==distinctPairs[9],"orientation reversal really swaps two unequal native J23 outcomes");
// EXACT finite Golden/F/R CODE OPTIMUM CUSP at a native positive record.
// The 12 signed Golden marker outcomes are equal at t=0; one original
// marked pair splits linearly. Within this true 17-word admissible prefix
// codebook, the label-reassignable optimal code gives the growing J+
// native cost 7 and shrinking J- cost9 (reversed for t<0). Therefore
// optimalCodeValue(q(t))=V0−2sqrt(2)c |t|+O(t²), c=Bell p^4/24.
// This is a real nondifferentiable native F/R EXPECTED CODE statistic,
// not a proof that global fundamental M1 Dmin chooses this codebook.
const assignCosts=theta=>{
 const q=golden17(theta),ids=Array.from({length:17},(_,i)=>i)
  .sort((a,b)=>q[b]-q[a]);
 return {positive:costs[ids.indexOf(8)],negative:costs[ids.indexOf(9)]};
};
const mapPlus=assignCosts(1e-5),mapMinus=assignCosts(-1e-5);
check(mapPlus.positive===7&&mapPlus.negative===9&&
 mapMinus.positive===9&&mapMinus.negative===7,
 "TRUE Golden17 mark labels swap 7/9 original F/R code lengths under reversal");
const theoreticalCusp=-2*Math.SQRT2*c,codeAtZero=optimalCodeValue(golden17(0));
const left=(codeAtZero-optimalCodeValue(golden17(-1e-5)))/(1e-5);
const right=(optimalCodeValue(golden17(1e-5))-codeAtZero)/(1e-5);
check(left>0&&right<0&&Math.abs(right-theoreticalCusp)<1e-10&&
 Math.abs(left+right)<1e-10,
 "actual native F/R optimally assigned code has strict even |t| cusp and no ordinary Euler derivative at flat geometry");

// A fixed asymmetric labelled code CAN produce an odd cost; that is an
// INDEPENDENT semantic/orientation rule, not a probability-only Dmin law.
// Label costs 1 vs 2 using original F/R (other native outcomes share baseline).
const labelledOdd=(q)=>q[8]*1+q[9]*2;
const oddActual=labelledOdd(pplus)-labelledOdd(pminus);
check(Math.abs(oddActual)>1e-8,
 "orientation-labelled original Golden code can have odd source ONLY after semantic label choice");

const source={bookZ:R.Z,fineZ:R.fineZ,pointerMoving:R.pointerMoving,
 pointerAtZero:R0.pointerMoving,pretraceSigned:R.pretrace,
 cycleOrientationWeight:R.probOrient,BookGradient:vBook,
 fineGradient:vFine,BookHessian:secB,fineHessian:secF,
 conditionalFisher:finiteFI,conditionalFisherPredicted:oneFisher,
 conditionalFixedReferenceHessian:finiteFixedH,
 conditionalFixedReferenceHessianPredicted:predictedFixedH,
 conditionalStationaryEnvelopeHessian:relaxedH,
 fullJointOptimalObjective:exactObjective,
 trueBookObjective:targetObjective,strictAlternateCost:perturbedObjective,
 all8440ThreeCycleProbability:threeStageMass,
 pathOnlyFisher:fisherBook,full143480Fisher:fisherJoint,
 strictlyPositiveLostFisher:fisherJoint-fisherBook,
 exactPredictedLostFisher:predictedFisherLost,
 nativeFRCode:{codewords:leaves,sortedCosts:costs,
 optimalCostAtPlus:optimalPos,optimalCostAtMinus:optimalNeg,
 probabilityOnlyOptimalParityResidual:optimalPos-optimalNeg,
 orientationLabelledSemanticCostContrast:oddActual,
 truePrefixCodeCusp:{codeValueAtFlat:codeAtZero,theoreticalSlopeRight:theoreticalCusp,
  measuredSlopeRight:right,measuredSlopeLeft:left,
  assignedAtPlus:mapPlus,assignedAtMinus:mapMinus}},
 actualFull128PortMismatch:p**3,actualFull128PortMismatchChecked:portCode};
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_FULL143480_BOOK_GOLDEN_CONDITIONAL_COST_INFO_AND_SIGNED_SOURCE",
 originalCarrier:{K:"K(9,11,13)",vertices:33,edges:718,
 genuineBased2:718,genuineBased3:7722,BookPaths:8440,
 trueFullGolden17Flags:17,allJointPositiveLabels:8440*17,
 completeBellFailureProbability:1-bell,
 originalGolden:p,stagePriors:"test fixed p,p², not compulsory stage selection"},
 sources:source,selectedGroups:R.groups,
 interpretation:"Exact conditional self-code Cost−Info cancels after genuine law relaxation; Book absolute partition source remains; signed pretrace Golden record retains nonzero orientation. Physical full Book/G0 H+J+R selection not proved.",
 notClaimed:["full native compulsory selected action","original scene-to-Role map","native code matches full measured q","native clock or preparation cost","coherent full128 stress","sourced Einstein/refinement"],
 GR_closed:false
},null,2));
