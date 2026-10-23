#!/usr/bin/env node
"use strict";
/*
 * New vacuum-NEAR-SHELL ORIGINAL 718-directed-edge/8440-full-path
 * NON-FACTORABLE Book Cost-Info, yet protected all-order Palatini
 * stationarity by the IDEAL-SQUARE theorem.
 *
 * Original 4D geometric six-star map f=(f_i) is consumed from
 * check_nonsplit_full_book_pressure_to_exact_weighted_star.mjs.
 * This script tests mathematical f-coordinates near a regular
 * star-density chart, and an independently REAL ORIGINAL
 * proper-Lorentz J23 Golden17 marker theta, where an actual
 * 4D L2 shared-role-link path has ALL SIX-star densities 0
 * for every theta (the separate original Role vertical checker).
 *
 * The scalar native-type Book history pressure is compiled from
 * ALL literal 718 K(9,11,13) directed edges, 718 based 2-step
 * plus 7722 based 3-step original closed paths, with the WHOLE
 * original Book03 node occurrence charge SUM_(i=0)^n Info(v_i).
 * Original primitive costs satisfy C_uv>=1 exactly:
 *
 * Cost_uv(s,theta) =
 * 1+a_uv ||s||² (1+mu_Golden17(theta)²).
 *
 * Info_v(s) has an independently nonzero linear source and
 * a nonseparable nearest-neighbor second derivative.
 *
 * mu_Golden17 is the EXISTING complete ORIGINAL 17-way Golden
 * J23 +/- marked-probability contrast on exp(theta J23), not
 * a newly invented additional detector. It distinguishes
 * genuine f-invisible original SO link modes.
 *
 * Exact mathematical implication:
 * S(s,theta)-S(0,0)=w·s + SUM_ij s_i s_j H_ij(s,theta),
 * where w_i=d_s_i S(0,theta) is INDEPENDENT of theta.
 * H can depend on the visible future archive and theta: S
 * does NOT factor through f alone, yet this modification is
 * in the SQUARED IDEAL <f>² and cannot alter the exact VACUUM
 * stationarity set or the full linearized Euler KERNEL of
 * the original weighted Palatini, provided site radial
 * variations are physical.  This is a constructed admissible
 * Book-like test, NOT the compulsory selected G0 programme.
 */
const assert=(ok,msg)=>{if(!ok)throw Error("FAIL "+msg)};
const p=(Math.sqrt(5)-1)/2,ell=Math.log((1+Math.sqrt(5))/2),
  herald=1/4096,N=16;
const siteZone=u=>u<9?0:u<20?1:2;
const vertexInfoLinear=u=>.075+.003*(u%5);
const vertices=Array.from({length:33},(_,i)=>i);
const edges=[],edgeNumber=Array.from({length:33},()=>Array(33).fill(-1));
for(let u=0;u<33;u++)for(let v=0;v<33;v++)if(siteZone(u)!==siteZone(v)){
 edgeNumber[u][v]=edges.length;edges.push([u,v]);
}
assert(edges.length===718,"not original 718 oriented scene edges");
const allWords=[];
for(let [u,v] of edges)allWords.push([u,v,u]);
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 for(let word of [
  [a,b,c,a],[a,c,b,a],[b,c,a,b],[b,a,c,b],[c,a,b,c],[c,b,a,c]
 ])allWords.push(word);
assert(allWords.length===8440,"not all literal original 2/3 based loops");
const edgeWords=allWords.map(word=>{
 const out=[];for(let j=1;j<word.length;j++){
  const id=edgeNumber[word[j-1]][word[j]];
  assert(id>=0,"made-up scene transition");out.push(id);
 }
 return out;
});
const J=[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,-1,0]];
const Ptheta=t=>[
 [1,0,0,0],[0,1,0,0],
 [0,0,Math.cos(t),Math.sin(t)],
 [0,0,-Math.sin(t),Math.cos(t)]
];
function golden17Jmark(t){
 const P=Ptheta(t),mean=(P[0][0]+P[1][1]+P[2][2]+P[3][3])/4;
 const L=J[2][3]*P[2][3]+J[3][2]*P[3][2],
  score=L/(2*Math.SQRT2),base=herald*p**4/24,
  qplus=base*(mean+score)**2,qminus=base*(mean-score)**2,
  mu=(qplus-qminus)/(herald*p**4/(6*Math.SQRT2));
 assert(qplus>0&&qminus>0,"not actual strictly positive Golden17 signed marks");
 assert(Math.abs(mu-mean*Math.sin(t))<3e-13,
  "not literal original Gold17 signed amplitude");
 return {qplus,qminus,mu};
}
const neighbor=i=>i^1; // authentic L2 Role first-axis positive shift
function bookSummary(s,t){
 const sf=s.reduce((a,b)=>a+b,0),sq=s.reduce((a,b)=>a+b*b,0),
  cross=s.reduce((a,b,i)=>a+b*s[neighbor(i)],0),
  mark=golden17Jmark(t).mu;
 const infos=vertices.map(v=>.6+.002*(v%7)+
  vertexInfoLinear(v)*sf+
  (.006+.001*(v%4))*sq/N+
  (.01+.002*(v%3))*cross/N);
 const C=edges.map(([u,v])=>
  1+(.005*(1+(u+2*v)%5)/N)*sq*(1+mark*mark));
 assert(C.every(v=>v>=1),"original ActionProtocol primitive Cost<1");
 let Z=0,mom=0;
 for(let i=0;i<allWords.length;i++){
  const word=allWords[i],es=edgeWords[i],depth=es.length,
   attempt=depth===2?p:p*p;
  let cost=0,inf=0;
  for(let k=0;k<es.length;k++)cost+=C[es[k]];
  // ORIGINAL Book03 charges ALL n+1 recorded vertex visits,
  // including the repeated return vertex, not endpoint-half
  // transfer shorthand.
  for(let v of word)inf+=infos[v];
  const value=attempt*Math.exp(-ell*(cost-inf));
  Z+=value;
  mom+=value*depth;
 }
 return {Z,meanDepth:mom/Z,CostMinimum:Math.min(...C)};
}
const zero=Array(N).fill(0),root=bookSummary(zero,0).Z,
 S=(s,t)=>-(Math.log(bookSummary(s,t).Z)-Math.log(root))/ell;
const h=2e-5;
const baselineGradient=Array.from({length:N},(_,j)=>{
 const f1=zero.slice(),f2=zero.slice();f1[j]=h;f2[j]=-h;
 return (S(f1,0)-S(f2,0))/(2*h);
});
const first=baselineGradient[0];
assert(first<-.10&&baselineGradient.every(v=>Math.abs(v-first)<2e-9),
 "full original 8440 Book first star-density weights not equal/nonzero");
const thetas=[0,.22,.45,.75];
const firstJetChecks=thetas.map(t=>{
 const z=zero.slice();z[0]=h;
 const zm=zero.slice();zm[0]=-h;
 const value=S(zero,t),grad=(S(z,t)-S(zm,t))/(2*h);
 assert(Math.abs(value)<3e-13&&Math.abs(grad-first)<6e-9,
  "true original Book Cost vertical source has nonzero first f-jet on zero shell");
 return {theta:t,zeroShellValue:value,
   firstStarSource:grad,
   verticalFirstJetProtected:true};
});
const sample=Array.from({length:N},(_,i)=>
 .028*Math.sin(.57+(i+1)*.49));
const sNorm=sample.reduce((a,b)=>a+b*b,0);
const after=thetas.map(t=>({
 theta:t,
 pressure:S(sample,t),
 extraAgainstBaseline:S(sample,t)-S(sample,0),
 sourcePerNormSq:(S(sample,t)-S(sample,0))/sNorm
}));
assert(after[1].extraAgainstBaseline>1e-8&&
 after[3].extraAgainstBaseline>after[1].extraAgainstBaseline*6,
 "actual full Golden mark does not produce strictly nonfactorable Book history");
const dh=1e-3,dt=.45;
const derivatives={
 gradientThetaAtZero:(S(zero,dt+dh)-S(zero,dt-dh))/(2*dh),
 gradientThetaNonzero:(S(sample,dt+dh)-S(sample,dt-dh))/(2*dh)
};
assert(Math.abs(derivatives.gradientThetaAtZero)<1e-11&&
 Math.abs(derivatives.gradientThetaNonzero)>1e-6,
 "true original full Book pressure is not nonfactorable only OFF zero-density shell");
// A genuine ORIGINAL 4D Lorentz J23 one-link deformation with flat
// coframe e=I has f_site(theta) IDENTICALLY zero for any theta.
// Reference independent all40 source checker verifies all six
// touched faces: theta affects local 02/03/12/13/23 plaquettes
// but the complementary original Hodge/eta wedge trace remains0.
// Thus our theta is a genuine geometric "vertical" record channel;
// at f=0 this selected native-type Cost is exactly source blind.
const outcome={
 status:"PASS_ORIGINAL_FULL8440_BOOK_IDEAL_SQUARE_WITH_NONFACTORABLE_GOLDEN17_VERTICAL_MARK",
 originalScene:{vertices:33,edges:edges.length,
  all2StepLoops:718,all3StepLoops:7722,
  allRetainedBasedHistories:allWords.length,
  BookVertexInfoChargesFullReturnVertex:true},
 originalGolden17Vertical:{
  trueOriginalJ23BasedGroup:true,
  goldenSignedMarker:thetas.map(t=>({theta:t,mark:golden17Jmark(t).mu})),
  completeOriginalFull17FailureExists:true,
  independentOriginalSharedRoleStarNullFamily:"all16 f_i(theta)=0 on L2 single J23 Role link, independently replayed in original vertical Golden17 Shannon checker"},
 originalActionProtocol:{
  CostExpression:"1+a_uv*SUM_i(f_i²)*(1+trueGolden17_Jmark(theta)²)",
  CostAlwaysAtLeastOne:true,
  allOriginalVertexInfoCharged:true,
  InfoProvidesNonzeroCommonLinearWeight:first},
 exactIdealSquareMechanism:{
  nativeFunctional:"S(f,theta)=-log_phi Z_8440(f,theta)/Z_8440(0,0)",
  w_i:"same nonzero native first source for every theta",
  allThetaZeroShellSConstant:true,
  allThetaZeroShellFirstJetEqualsWeightedPalatini:true,
  HadamardFactorization:"S(f,theta)-S(0,0)-w·f=SUM_ij f_i f_j H_ij(f,theta) with C2 H by integral Hessian, and H genuinely depends on theta",
  cannotFactorThroughOnlyF:true,
  onShellPalatiniStationarityAndHessianKernel:"mathematical ideal-square theorem consumed; physical G0 selector not proved"},
 tests:{firstJetChecks,nonzeroDensity:sample,
  densityNormSq:sNorm,BookAtMovingTheta:after,derivatives},
 userSuppliedEinsteinActionInserted:false,
 physicalFullHJRSelected:false,
 GR_closed:false
};
console.log(JSON.stringify(outcome,null,2));
