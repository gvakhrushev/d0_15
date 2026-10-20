#!/usr/bin/env node
"use strict";
/*
  ORIGINAL D0 full-17 Golden two-fresh/Bell and literal ORIGINAL 8440
  rooted 2/3 book paths, with TRUE repeated closing-root vertex INFO.
  Test a candidate native BOOK-TYPE expected cross-code Cost minus full
  Shannon Info on each visit, and audit the INTEGER number m=0,1,2 of
  separately PAID ROOT PREPARATION code recordings per based path.

  At a field-stationary FULL matched Golden reference mu=q(theta),
  per 17-way observation: C_code=H_phi(q), so
  S_gamma=n[1+C_code]+m C_code-(n+1)H_phi(q)
         =n+(m-1)H_phi(q).
  Exactly m=1 gives S_gamma=n, across ALL 8440 true words and ALL theta.
  This is conditional PREPARATION-COST AUDIT, NOT a claim G0/Book03
  physically includes m root registers, has the moving codebook or
  chooses this expected Cost vs full Info; entire Spin/Q8/clock/work OPEN.
*/
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),bell=1/4096;
const fail=(ok,why)=>{if(!ok)throw new Error("FAIL "+why)};
const zone=i=>i<9?0:i<20?1:2;
const wordLengths=[];
for(let i=0;i<33;i++)for(let j=0;j<33;j++)
 if(zone(i)!==zone(j))wordLengths.push(2);
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 for(let rep=0;rep<6;rep++)wordLengths.push(3);
fail(wordLengths.length===8440&&wordLengths.filter(n=>n===2).length===718
 &&wordLengths.filter(n=>n===3).length===7722,
 "actual original 718/7722 rooted Book histories are not complete");
const qflat=()=>{
 const qq=Array(12).fill(bell*p**4/24);
 qq.push(bell*p**4/2,bell*p*p*(1-p*p),bell*p**3,bell*p*p,1-bell);
 return qq;
};
function q17(theta){
 const m=(1+Math.cos(theta))/2,x=Math.sin(theta)/Math.SQRT2;
 const qq=[];
 for(let i=0;i<6;i++){
  const v=i===4?x:0;
  qq.push(bell*p**4/24*(m+v)**2,bell*p**4/24*(m-v)**2);
 }
 const gg=bell*p**4;
 qq.push(gg-qq.reduce((s,x)=>s+x,0),
       bell*p*p*(1-p*p),bell*p**3,bell*p*p,1-bell);
 fail(qq.length===17&&Math.min(...qq)>0&&
   Math.abs(qq.reduce((s,x)=>s+x,0)-1)<2e-13,
   "positive complete original Golden/Bell17 lost branch");
 return qq;
}
const H=qq=>qq.reduce((s,v)=>s-v*Math.log(v)/ell,0);
const Cross=(qq,ref)=>qq.reduce((s,v,i)=>s-v*Math.log(ref[i])/ell,0);
const KL=(qq,ref)=>qq.reduce((s,v,i)=>s+v*Math.log(v/ref[i])/ell,0);
function full96(theta,zeta){
 // True shared original 4D Role link (0,0)=exp(theta J23):
 // exactly THREE +theta and THREE -theta face holonomies, 90 flat.
 const qp=q17(theta),qm=q17(-theta),rp=q17(zeta),rm=q17(-zeta),q0=q17(0);
 const ent=90*H(q0)+3*H(qp)+3*H(qm);
 const cross=90*Cross(q0,q0)+3*Cross(qp,rp)+3*Cross(qm,rm);
 const diff=3*KL(qp,rp)+3*KL(qm,rm);
 fail(Math.abs(cross-ent-diff)<2e-11,"full96 true code Cost−Info mismatch");
 fail(diff>=-3e-13,"negative original full Golden KL");
 return {H:ent,C:cross,D:diff};
}
const Z2=718*p**3,Z3=7722*p**5,Z0=Z2+Z3;
function partitionByFullOriginalWord(m,theta,zeta){
 const {H:info,C:code,D}=full96(theta,zeta);
 let Z=0;
 for(const n of wordLengths){
  const primitiveC=1+code;
  fail(primitiveC>=1,"original ActionProtocol primitive quantum violated");
  // Actual Book03 sums n transition Costs and (n+1) vertex Info,
  // including the LAST copy of the original based-loop root.
  // The separate m*C is the independently typed boundary/OLD prep
  // cost to be CHECKED, not pretended part of Book03 primitive edges.
  const net=n*primitiveC+m*code-(n+1)*info;
  Z+=(n===2?p:p*p)*Math.exp(-ell*net);
 }
 const analytical=Math.exp(-ell*(m-1)*info)*
  (Z2*Math.exp(-ell*(2+m)*D)+Z3*Math.exp(-ell*(3+m)*D));
 fail(Math.abs(Z-analytical)<5e-9,"all8440 original full code/Info exact path law");
 return {Z,H:info,C:code,D,absoluteCost:1+code,
  normalizedAction:-Math.log(Z/Z0)/ell,
  exactClosedAction:-Math.log(analytical/Z0)/ell};
}
let maxRootExact=0,matchingStatus=[];
for(const theta of [-.21,-.1,0,.14,.28]){
 const q=full96(theta,theta);
 fail(Math.abs(q.C-q.H)<2e-12&&Math.abs(q.D)<2e-12,
 "moving prepared native Golden code is not its own optimum");
 let row={theta,info:q.H};
 for(let m=0;m<=2;m++){
  const n=partitionByFullOriginalWord(m,theta,theta);
  const expected=(m-1)*q.H;
  maxRootExact=Math.max(maxRootExact,
        Math.abs(n.normalizedAction-expected));
  fail(Math.abs(n.normalizedAction-expected)<3e-11,
   "expected root/prep Cost count does not fix source");
  row["bookAction_m"+m]=n.normalizedAction;
 }
 matchingStatus.push(row);
}
const h=.06,zero=full96(0,0);
const dh=(full96(h,h).H+full96(-h,-h).H-2*zero.H)/(h*h);
const exactHpp=-(6*p**4/(4096*ell))*
 ((5/12)*Math.log(12)+1/6);
fail(Math.abs(dh-exactHpp)<1e-6,"true six Golden face full Shannon Hessian wrong");
let HessAtMatched=[];
for(let m=0;m<=2;m++){
 const a=partitionByFullOriginalWord(m,h,h).normalizedAction,
       b=partitionByFullOriginalWord(m,-h,-h).normalizedAction,
       c=partitionByFullOriginalWord(m,0,0).normalizedAction;
 const dd=(a+b-2*c)/(h*h);
 fail(Math.abs(dd-(m-1)*exactHpp)<2e-6,
  "genuine original prep-count Book Hessian mismatch");
 HessAtMatched.push(dd);
}
// The reference-moving full-code source has a POSITIVE relative
// Fisher but EXACTLY ZERO after stationary elimination if m=1.
const qh=full96(.1,0),qmatched=full96(.1,.1);
fail(qh.D>0&&Math.abs(qmatched.D)<1e-13&&
 Math.abs(partitionByFullOriginalWord(1,.1,.1).normalizedAction)<2e-11,
 "internal Golden reference stationary envelope did not remove full-source");
const weightedVisits=(3*Z2+4*Z3)/Z0;
const klpp=(p**4/(4096*ell));
const frozenReferenceHessian=weightedVisits*klpp;
const kTest=.06;
const dynCodePhi=x=>partitionByFullOriginalWord(1,x,0).normalizedAction,
       dynH=(dynCodePhi(kTest)+dynCodePhi(-kTest)-
                   2*dynCodePhi(0))/(kTest*kTest);
fail(Math.abs(dynH-frozenReferenceHessian)<3e-6,
 "matched reference vs fixed old memory real Book code source");

console.log(JSON.stringify({
 status:"PASS_ORIGINAL_8440_BOOK_VISITS_ROOT_CODE_CHARGE_SOURCE",
 originalScene:{vertices:33,directedEdges:718,rootedPathCount:8440,
  stage2:718,stage3:7722,goldenStageAttempts:[p,p*p],
  initialAndFinalRootVisit:true},
 originalGeometry:{RoleSites:16,trueSharedLinks:64,actualBasedFaces:96,
  changingFacesOnTrueJ23Role0:6,all16PalatiniStarDensityValuesOnOrbit:0},
 fullGolden:{full17OutcomesKept:true,BellFailure:4095/4096,
  infoEntropyAtFlat:zero.H,codeMatchedAtFlat:zero.C,
  trueEntropySecondSource:exactHpp},
 matchedReferenceAllOrder:matchingStatus,
 rootPreparationCount:{m0_NoRootCode:"Book residual=-H96",
   m1_SingleChargedRootCode:"Book residual=0 identically",
   m2_DoubleChargedRootCode:"Book residual=+H96",
   exact8440SourceMaxError:maxRootExact,
   secondBookEulerForM0: -exactHpp,
   secondBookEulerForM1:0,
   secondBookEulerForM2:exactHpp,
   finiteSecondSourceForEachM:HessAtMatched},
 fixedReferenceExtra:{trueMeanVisitedVertices:weightedVisits,
   positiveGoldenCodeHessianOneLink:klpp,
   BookFixedCodeHessian:frozenReferenceHessian,
   finiteFull8440Hessian:dynH,
   fullCodeKLAtTheta01:qh.D,matchedReferenceKLAtTheta01:qmatched.D},
 physicalRootOldRightClockWorkSourceStillUnselected:true,
 noAdHocEinsteinCoefficient:true,
 GR_closed:false
},null,2));
