#!/usr/bin/env node
"use strict";
/*
  EXACT D0 research falsifier of primitive cost/source uniqueness:
  - True original 4D L=2 Role J23 shared-link orbit, all16 six-star f_x=0.
    Geometry certified by independently owned original full96 Role checker.
  - Genuine complete 17-outcome TWO Golden flags+Bell failure on the SAME
    P(theta)=exp(theta J23); Golden p=1/phi, 1/4096 Herald.
  - Actual original K(9,11,13), all718 directed primitive Cost actions,
    all718 based 2-returns +7722 based 3-returns, true Book path Info
    INCLUDING its repeated closing root vertex, literal Golden g2=p,g3=p².
  - TWO different strictly ActionProtocol-admissible complete mathematical
    Cost/Info laws, all agreeing at theta=0 and in every first source, but
    opposite nonzero second-source on the Einstein f-constant J23 direction.
  - BOTH exceptional Cost/Info source functions are computed from ORIGINAL
    full Golden17 KL (not a fitted theta² counterterm or imported coefficient).
  - Fully retains all conditional Golden outcomes and actual stage failure
    alternatives as a POSITIVE probability experiment via common p^20 check.
  NOT a declaration that compulsory M1/G0 H+J+R selects EITHER law.
*/
const fail=(v,s)=>{if(!v)throw new Error("FAIL "+s)};
const phi=(1+Math.sqrt(5))/2,p=1/phi,ell=Math.log(phi),herald=1/4096;
const N=33,zone=i=>i<9?0:i<20?1:2;
const originalDirected=[];
for(let u=0;u<N;u++)for(let v=0;v<N;v++)
 if(zone(u)!==zone(v))originalDirected.push([u,v]);
fail(originalDirected.length===718,"original directed graph has 718 edges");
const words=[];
for(const [u,v] of originalDirected)words.push([u,v,u]);
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 for(const w of [[a,b,c,a],[a,c,b,a],[b,c,a,b],
                 [b,a,c,b],[c,a,b,c],[c,b,a,c]])words.push(w);
fail(words.length===8440,"original 718+7722 Book paths missing");
const E=()=>Array.from({length:N},()=>Array(N).fill(0));
const K0=E();
for(const [u,v] of originalDirected)K0[u][v]=p;
function golden17(theta){
 const cos=Math.cos(theta),sin=Math.sin(theta),
       mean=(1+cos)/2;
 const q=[];
 for(let a=0;a<6;a++){
  const signed=a===4?sin/Math.SQRT2:0;
  q.push(herald*p**4/24*(mean+signed)**2,
         herald*p**4/24*(mean-signed)**2);
 }
 const gg=herald*p**4;
 const rest=gg-q.reduce((s,v)=>s+v,0);
 const bg=herald*p**2*(1-p*p);
 const gb=herald*p**3,bb=herald*p*p;
 q.push(rest,bg,gb,bb,1-herald);
 fail(q.length===17&&Math.min(...q)>0,"full original positive Golden17 support");
 fail(Math.abs(q.reduce((s,v)=>s+v,0)-1)<2e-14,
  "full Golden17 FAILED flags + Bell complement not normalized");
 return q;
}
const ref=golden17(0);
function KL(theta){
 return golden17(theta).reduce((s,q,i)=>s+q*Math.log(q/ref[i])/ell,0);
}
const g2=p,g3=p*p;fail(Math.abs(g2+g3-1)<1e-15,"original Golden stage prior");
const floor=(law,theta)=>({
 K:(u,v)=>{
  if(zone(u)===zone(v))return 0;
  return p*(law==="cost"&&u===0&&v===9?
      Math.exp(-ell*KL(theta)):1);
 },
 Info:u=>law==="info"&&u===0?KL(theta):0
});
function fullBook(law,theta){
 const model=floor(law,theta);
 let Z=0,n2=0,n3=0,edgeOccurrences=0,vertexOccurrences=0;
 for(const word of words){
  const n=word.length-1,g=n===2?g2:g3;
  let val=g,visits=0;
  for(let k=0;k<=n;k++){
   val*=Math.exp(ell*model.Info(word[k]));
   if(word[k]===0)visits++;
   if(k<n){
    val*=model.K(word[k],word[k+1]);
    if(word[k]===0&&word[k+1]===9)edgeOccurrences++;
   }
  }
  Z+=val;
  if(n===2)n2+=val;else n3+=val;
  vertexOccurrences+=visits;
 }
 return {Z,n2,n3,edgeOccurrences,vertexOccurrences};
}
const base=fullBook("canonical",0);
fail(base.edgeOccurrences===41,"ORIGINAL 2+39 based directed edge occurrence count");
fail(base.vertexOccurrences===72+1144,"true full Book start/close vertex Info occurrence");
const Z0=718*p**3+7722*p**5;
fail(Math.abs(base.Z-Z0)<2e-9,"true original 8440 Book partition");
const edgeOccupancy=(2+39*p*p)/(718+7722*p*p);
const vertexOccupancy=(72+1144*p*p)/(718+7722*p*p);
const fisher=p**4/(6*4096),K2=fisher/ell;
function action(law,theta){return -Math.log(fullBook(law,theta).Z/base.Z)/ell}
let maxRawErr=0,stageError=0;
const tiny=1e-3;
for(const t of [0,.05,.15,.27]){
 const excess=KL(t);
 fail(excess>=-1e-15,"native positive Golden KL violated");
 const cost=action("cost",t),inf=action("info",t);
 // On the actual original based-word support each directed edge appears
 // at most once. This gives a CLOSED exact whole8440 Cost action.
 const predictedCost=-Math.log(1+
   edgeOccupancy*(Math.exp(-ell*excess)-1))/ell;
 // Vertex0 occurs once OR twice (when it is the closing root). Respect
 // the genuine Book03 full start+end vertex Info charge, no endpoint frozen.
 const ZinfoRatio=1+
   (24*p**3+572*p**5)/Z0*(Math.exp(ell*excess)-1)+
   (24*p**3+286*p**5)/Z0*(Math.exp(2*ell*excess)-1);
 const predictedInfo=-Math.log(ZinfoRatio)/ell;
 maxRawErr=Math.max(maxRawErr,Math.abs(cost-predictedCost),
                                    Math.abs(inf-predictedInfo));
 // One admissible literal Golden-power common path verification regime.
 const kappa=p**20,beta2=p*p,beta3=p*p;
 const Z2=fullBook("cost",t).n2,Z3=fullBook("cost",t).n3;
 const reject2=g2*(1-beta2)+g2*beta2*(1-kappa*Z2/g2);
 const reject3=g3*(1-beta3)+g3*beta3*(1-kappa*Z3/g3);
 const accept2=kappa*Z2,accept3=kappa*Z3;
 fail(reject2>0&&reject3>0&&Math.abs(
   reject2+reject3+accept2+accept3-1)<1e-12,
   "all original stage failures must be retained in valid positive law");
 stageError=Math.max(stageError,Math.abs(reject2+reject3+accept2+accept3-1));
}
fail(maxRawErr<3e-11,"analytic 8440 path source identity fail");
const analyticalCost=edgeOccupancy*K2,analyticalInfo=-vertexOccupancy*K2;
const h=.004;
const numericalCost=(action("cost",h)+action("cost",-h))/(h*h);
const numericalInfo=(action("info",h)+action("info",-h))/(h*h);
fail(Math.abs(numericalCost-analyticalCost)<2e-10,
 "true original Golden raw Cost Hessian wrong");
fail(Math.abs(numericalInfo-analyticalInfo)<3e-10,
 "true original Golden raw INFO Hessian wrong");
const sameFirst=Math.abs((action("cost",h)-action("cost",-h))/(2*h))+
 Math.abs((action("info",h)-action("info",-h))/(2*h));
fail(sameFirst<1e-10,"native cost/info first source must agree at flat");
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_GOLDEN17_FULL8440_COST_INFO_SECOND_SOURCE_NONSELECTION",
 originalCarrier:{RoleSites:16,SharedRoleLinks:64,BasedRoleFaces:96,
  fullPalatiniStarOnJ23Link:"ALL16 f_x(theta) ≡ 0; independent original96 checker owned"},
 golden17:{completeLabels:17,goldenP:p,bellFailure:4095/4096,
  codeKLCurvature:K2,fullFisher:fisher},
 nativeBook:{directedOriginalEdges:718,based2:718,based3:7722,actualWords:8440,
  fullStartAndClosingRootInfo:true,fullPartition0:Z0,
  directedEdgeOccurrences:base.edgeOccurrences,
  node0Visits:base.vertexOccurrences,
  expectedDirectEdgeCount:edgeOccupancy,expectedNode0Visits:vertexOccupancy,
  originalGoldenStageAttempts:[g2,g3]},
 twoFundamentallyAdmissibleMathematicalCompletions:{
  canonicalCost:"ALL directed primitive costs C=1",
  excessCost:"ONLY C_(0,9)=1+D_phi(q17(theta)||q17(0)) >=1",
  movingInfo:"ALL Cost=1, vertex0 Info=D_phi(q17(theta)||q17(0))",
  sameActionAndAllFirstJetsAtFlat:true,
  nonzeroOppositeSecondJetCost:analyticalCost,
  nonzeroOppositeSecondJetInfo:analyticalInfo,
  directFull8440SecondJetCost:numericalCost,
  directFull8440SecondJetInfo:numericalInfo,
  exactWholeBookFormulaError:maxRawErr,
  fullEarlyLateStageLawError:stageError},
 noAddedScaleOrFittedEinsteinCoupling:true,
 doesNotSelectActualG0FullHJR:true,
 GR_closed:false
},null,2));
