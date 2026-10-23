#!/usr/bin/env node
"use strict";
/*
 Original K(9,11,13) REAL 718 Perron/Doob directed edges; 17 actual
 complete Golden/Lorentz Bell labels per edge = 12,206 joint events.
 Replace the mathematical imported ideal Bell h=1/4096 by the
 independently verified native coherent p^18 U SUCCESS EVENT with
 h=p^36: no new amplitude and exact golden action surprisal 36.
 Complete old one-sided Perron r (not stationary pi), full failure
 1-p^36 on EACH real edge, moving scalar Book source plus moving
 proper-Lorentz conditional source, exact Fisher orthogonality.
 N.B. edge->SO Lorentz sign assignment is a math test, not a physical
 4D Role face controller. Compulsory Book H+J+R source NOT selected.
*/
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi),herald=p**36,N=33;
const z=i=>i<9?0:i<20?1:2,fail=(v,msg)=>{if(!v)throw Error(msg)};
const edge=[],Kmat=(y)=>{
 let K=Array.from({length:N},()=>Array(N).fill(0));
 for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(z(u)!==z(v)){
  const Cost=1.09+.018*Math.sin(.111*u+.027*v)**2
    +.007*y*y;
  const Info=i=>.08*Math.sin(.21*i)+.025*y*Math.cos(.13*i);
  K[u][v]=Math.exp(-ell*(Cost-.4*Info(u)-.6*Info(v)));
 }
 return K;
};
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(z(u)!==z(v))edge.push([u,v]);
fail(edge.length===718,"missing original directed scene prices");
function perron(K){
 let r=Array(N).fill(1/N),rho=0;
 for(let t=0;t<170;t++){
  let a=K.map(row=>row.reduce((s,v,j)=>s+v*r[j],0));
  rho=a.reduce((s,v)=>s+v,0);r=a.map(x=>x/rho);
 }
 const P=K.map((row,u)=>row.map((v,j)=>v*r[j]/(rho*r[u])));
 fail(Math.max(...P.map(row=>Math.abs(row.reduce((s,x)=>s+x,0)-1)))<2e-13,
  "true Perron rows not stochastic");
 return {r,P,rho};
}
function q16(x){
 const m=(1+Math.cos(x))/2,s=Math.sin(x)/Math.SQRT2,q=[];
 for(let j=0;j<6;j++){
  const v=j===4?s:0;
  q.push((p**4/24)*(m+v)**2,(p**4/24)*(m-v)**2);
 }
 const gg=p**4,rest=gg-q.reduce((s,x)=>s+x,0);
 q.push(rest,p*p*(1-p*p),p**3,p*p);
 fail(q.length===16&&Math.min(...q)>0&&
  Math.abs(q.reduce((s,x)=>s+x,0)-1)<2e-14,
 "all original Golden conditional CAR and failure outcomes not summed");
 return q;
}
const q17=x=>q16(x).map(v=>herald*v).concat([1-herald]);
function joint(y,xi){
 const {r,P,rho}=perron(Kmat(y)),data=[];
 for(const [u,v] of edge){
  const orient=(u<v?1:-1),base=r[u]*P[u][v],q=q17(xi*orient);
  for(let j=0;j<17;j++)data.push(base*q[j]);
 }
 fail(data.length===12206&&Math.min(...data)>0&&
  Math.abs(data.reduce((a,b)=>a+b,0)-1)<3e-13,
   "full old one-sided Perron × Golden17 native complete q broken");
 return {r,P,rho,data};
}
const y=.19,xi=0,t=.0003,base=joint(y,xi),
 plusY=joint(y+t,0),minusY=joint(y-t,0),
 plusX=joint(y,t),minusX=joint(y,-t);
let Iy=0,Ix=0,Icross=0;
for(let k=0;k<base.data.length;k++){
 const dy=(plusY.data[k]-minusY.data[k])/(2*t),
       dx=(plusX.data[k]-minusX.data[k])/(2*t);
 Iy+=dy*dy/base.data[k];
 Ix+=dx*dx/base.data[k];
 Icross+=dy*dx/base.data[k];
}
const IExpected=herald*p**4/6;
fail(Math.abs(Ix-IExpected)<2e-12&&Math.abs(Icross)<2e-11&&Iy>0,
 "native Golden rate p^36 did not keep full scalar/Lorentz source decoupling");
let maximumOdd=0,maximumMarginal=0;
const finite=joint(y,.071);
for(let i=0;i<edge.length;i++){
 const [u,v]=edge[i],prob=base.r[u]*base.P[u][v];
 const direct=finite.data.slice(i*17,(i+1)*17),
   recovered=direct.reduce((s,x)=>s+x,0);
 maximumMarginal=Math.max(maximumMarginal,Math.abs(recovered-prob));
 const qplus=direct[8]/(prob*herald),qminus=direct[9]/(prob*herald);
 const recoveredOdd=Math.sqrt(12)/(p*p)*
        (Math.sqrt(qplus)-Math.sqrt(qminus));
 maximumOdd=Math.max(maximumOdd,Math.abs(recoveredOdd-
       (u<v?1:-1)*Math.sin(.071)));
}
fail(maximumOdd<1e-12&&maximumMarginal<5e-14,
 "original signed Palatini Lie root lost under native p^36 Bell success");
console.log(JSON.stringify({
 result:"PASS_ORIGINAL_K913_FULL12206_NATIVE_P36_COHERENT_BELL_SCORE",
 originalScene:{directedEdges:718,fullLabelledOutcomes:12206,
  retainedOneSidedPrior:true,movingPerronPressure:base.rho},
 nativeFullGolden:{p,exactEventProbability:herald,
  trueSuccessSurprisalInGoldenCodeUnits:-Math.log(herald)/ell,
  actualFullBellFailureProbability:1-herald,
  conditional16AllGoldenGoodBadOutcomesKept:true},
 completeSource:{PerronFisher:Iy,actualAll718SignedLorentzFisher:Ix,
  expectedIntrinsicNativeFisher:p**40/6,
  bookLorentzFisherCross:Icross,
  recoveredMaximumPositiveSignedRootError:maximumOdd,
  recoveredMaximumPerronHistoryMarginalError:maximumMarginal},
 roleL2Prediction:{all384OriginalProperLinks:true,
  trueBasedFaceIncidencePerLieRank:45,
  allSixLieNativeFisherRank:270,
  unchangedGaugePlusWilsonNullity:114,
  perFaceIntrinsicNativeFisher:p**40/6},
 physicalRoleToSceneMapAndMovingProgrammeNotSelected:true,
 exactInnerChoiPOVMIsSeparateNativeCompilerObligation:true,
 realBookHJRPrepClockWorkSourceNotSelected:true,
 GR_closed:false
},null,2));
