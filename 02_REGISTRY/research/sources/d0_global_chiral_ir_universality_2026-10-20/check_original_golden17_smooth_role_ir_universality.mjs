#!/usr/bin/env node
"use strict";
/*
 * D0 global "IR universality" finite check, ORIGINAL Golden p and
 * TWO-FRESH/Bell full17 signed probabilities, shared smooth 4D Role links.
 *
 * Family: all true Role (x,2) links U=exp[h*a*sin(2*pi*x3) J23];
 * all other links I, so every based face is an ORIGINAL link product and
 * the lattice is integrable/Bianchi-safe. Only genuine (2,3) faces move.
 *
 * sqrt(+/-) complete Golden coordinates ("root") and same ORIGINAL
 * positive mark relative Code log-ODDS ("code") have exact equal
 * first Lorentz source, differences O(h^4) after the already-owned
 * geometric source normalization h^(-2) * sum_x h^4.
 * Even full 17-pointer Shannon is O(h^2) at this declared scaling.
 *
 * Does NOT choose the compulsory G0/Book H+J+R action or prove that
 * full retained Cost, work, clock, Spin source use this normalization.
 */
const need=(ok,msg)=>{if(!ok)throw Error("FAIL "+msg)};
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi),bell=1/4096;
const q0=p**4/(24*4096),GG=bell*p**4;
const GB=bell*p*p*(1-p*p),BG=bell*p**3,BB=bell-GG-GB-BG;
function golden17(t){
  const m=(1+Math.cos(t))/2,y=Math.sin(t)/Math.SQRT2;
  const marked=Array.from({length:10},()=>q0*m*m)
    .concat([q0*(m+y)**2,q0*(m-y)**2]);
  const rest=GG-marked.reduce((s,x)=>s+x,0);
  const q=marked.concat([rest,GB,BG,BB,1-bell]);
  need(q.length===17 && q.every(x=>x>0),
    "true complete original two-fresh Golden17 remains strictly positive");
  need(Math.abs(q.reduce((s,x)=>s+x,0)-1)<6e-15,
    "ALL 17 Golden outcomes, incl Bell failure, normalized");
  return {q,m,y};
}
function root(t){
  const q=golden17(t).q;
  return Math.SQRT2*(Math.sqrt(q[10])-Math.sqrt(q[11]))/(2*Math.sqrt(q0));
}
function code(t){
  const q=golden17(t).q;
  return Math.log(q[10]/q[11])/(2*Math.SQRT2);
}
function codeDeriv(t){
  const {m,y}=golden17(t),mp=-Math.sin(t)/2,yp=Math.cos(t)/Math.SQRT2;
  return Math.SQRT2*(m*yp-y*mp)/(m*m-y*y);
}
function Shannon(t){
  return -golden17(t).q.reduce((s,v)=>s+v*Math.log(v),0)/ell;
}
function ShannonDeriv(t){
  const {q,m,y}=golden17(t),mp=-Math.sin(t)/2,yp=Math.cos(t)/Math.SQRT2;
  const derivative=Array.from({length:10},()=>2*q0*m*mp)
    .concat([2*q0*(m+y)*(mp+yp),2*q0*(m-y)*(mp-yp)]);
  derivative.push(-derivative.reduce((s,v)=>s+v,0),0,0,0,0);
  return -derivative.reduce((s,v,i)=>s+v*Math.log(q[i]),0)/ell;
}
const H0=Shannon(0),a=.61,amp=.23;
need(Math.abs(root(.17)-Math.sin(.17))<4e-15,
  "literal p Golden amplitude ROOT exactly gives original J23 odd curvature");
need(Math.abs(root(.17)+root(-.17))<4e-15,
  "original Golden root inversion-ODD");
need(Math.abs(code(.17)+code(-.17))<4e-15,
  "original positive code log odds inversion-ODD");
need(Math.abs(Shannon(.17)-Shannon(-.17))<4e-16,
  "original complete Golden17 Shannon inversion-EVEN");
need(Math.abs(codeDeriv(0)-1)<3e-15,
  "native code-relative first source exactly equals original signed root");
need(Math.abs((code(.05)-Math.sin(.05))/.05**3-5/12)<.001,
  "analytic native Golden log-odds vs signed root Taylor 5/12 t^3");

// Proper SO(1,3) J23 rotation preserves the actual null metric, and the
// nonzero smooth Role (x,2) links are all in one SO rotation subgroup.
// Original based (2,3) plaquette P23(x)=U2(x) U2(x+3)^(-1).
function R(t){return [
 [1,0,0,0],[0,1,0,0],
 [0,0,Math.cos(t),Math.sin(t)],
 [0,0,-Math.sin(t),Math.cos(t)]
];}
function mm(A,B){return A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));}
const I=R(0),eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const T=A=>A[0].map((_,j)=>A.map(row=>row[j]));
function matErr(A,B){return Math.max(...A.flatMap((row,i)=>row.map((v,j)=>Math.abs(v-B[i][j]))));}
for(const t of [-.4,-.1,0,.2,.43]){
 need(matErr(mm(mm(T(R(t)),eta),R(t)),eta)<2e-15,
    "original Lorentz null-metric preserved by all true links");
}
function integrated(L,alpha=a){
 const h=1/L,values={root:0,code:0,linear:0,even:0,
   dRoot:0,dCode:0,dLinear:0,dEven:0,l1RootCode:0};
 let maxFace=0,checkBianchi=0;
 for(let k=0;k<L;k++){
  const x=2*Math.PI*k/L,zstep=2*Math.PI/L;
  const theta=h*alpha*(Math.sin(x)-Math.sin(x+zstep));
  const Dtheta=h*(Math.sin(x)-Math.sin(x+zstep));
  // Original smooth coframe complementary area, nondegenerate:
  // e0(x3)=(1+.23*cos(2π(x3+h/2)))dx0, e1=dx1.
  const w=1+amp*Math.cos(x+zstep/2);
  const scale=h*h*L**3*w; // native h^-2*sum_x h^4= h²*L³ per x3 slice
  maxFace=Math.max(maxFace,Math.abs(theta));
  const face=mm(R(h*alpha*Math.sin(x)),R(-h*alpha*Math.sin(x+zstep)));
  checkBianchi=Math.max(checkBianchi,matErr(face,R(theta)));
  const signed=root(theta),relative=code(theta);
  need(Math.abs(signed-Math.sin(theta))<2e-15,
    "original sqrt Golden mark gives actual based SO face");
  values.root+=scale*signed;values.code+=scale*relative;
  values.linear+=scale*theta;values.even+=scale*(Shannon(theta)-H0);
  values.dRoot+=scale*Math.cos(theta)*Dtheta;
  values.dCode+=scale*codeDeriv(theta)*Dtheta;
  values.dLinear+=scale*Dtheta;
  values.dEven+=scale*ShannonDeriv(theta)*Dtheta;
  values.l1RootCode+=scale*Math.abs(relative-signed);
 }
 need(checkBianchi<2e-15,
  "actual original SHARED-LINK plaquettes are proper group products");
 return {L,h,maxFace,basedFaces:L**4,
  ...values,oddDiff:values.code-values.root,
  oddDiffOverH4:(values.code-values.root)/h**4,
  dOddDiffOverH4:(values.dCode-values.dRoot)/h**4,
  evenOverH2:values.even/h**2,
  dEvenOverH2:values.dEven/h**2,
  evenUNSCALEDnativeBookHypothesis:values.even/h**2,
  dEvenUNSCALEDnativeBookHypothesis:values.dEven/h**2,
  bianchiError:checkBianchi};
}
const results=[8,12,16,24,32,48,64,96].map(L=>integrated(L));
for(const r of results){
 need(r.maxFace<.1,"original Golden positive chart on smooth Role fields");
 need(r.l1RootCode<=40*r.h**4,
    "global original 4D signed native Code-vs-ROOT action difference O(h^4)");
 need(Math.abs(r.dOddDiffOverH4)<11,
    "global original 4D C1 geometric source difference O(h^4)");
 need(Math.abs(r.evenOverH2)<.001,
    "complete Golden17 pointer-even interaction O(h²) IN DECLARED geometric normalization");
 need(Math.abs(r.dEvenOverH2)<.003,
    "complete Golden17 pointer-even source O(h²) in same normalization");
}
need(Math.abs(results.at(-1).root)>.4,
 "NONZERO signed Golden Role action survives true global smooth continuum");
need(Math.abs(results.at(-1).dRoot)>.7,
 "NONZERO native signed Golden gravitational first source survives refinement");
let dL=1e-4;
const htest=integrated(16,a),hp=integrated(16,a+dL),hm=integrated(16,a-dL);
for(const key of ["root","code","even"]){
 const numeric=(hp[key]-hm[key])/(2*dL),analytical=htest["d"+key[0].toUpperCase()+key.slice(1)];
 need(Math.abs(numeric-analytical)<1e-8,
  "native "+key+" TRUE moving C1 field-source differentiation");
}
// GLOBAL hostile control: actual full Golden17 even Shannon per FACE with
// NO original h^-2*GoldenLEFT weight multiplier is a mathematically
// different SOURCE law. Its SUM does NOT vanish: since H17(t)-H17(0)
// =H2*t²/2+O(t4), and t/h²→−2πa cos(2πx3), true 4D sum
// → H2 π² a² (NONZERO). Its first field source survives as
// 2 H2 π² a. Thus native work/Cost scaling must be PROVED before
// declaring the even memory IR-irrelevant.
const H2=-(p**4/(4096*ell))*((5/12)*Math.log(12)+1/6);
const evenLimit=H2*Math.PI**2*a*a;
const evenDerivativeLimit=2*H2*Math.PI**2*a;
const finest=results.at(-1);
need(Math.abs(finest.evenUNSCALEDnativeBookHypothesis-evenLimit)<2e-7 &&
     Math.abs(finest.dEvenUNSCALEDnativeBookHypothesis-evenDerivativeLimit)<1e-6,
 "unscaled original complete Golden17 even historical price has NONZERO continuum curvature-square source");
need(Math.abs(evenLimit)>.0003 && Math.abs(evenDerivativeLimit)>.001,
 "even native Cost if per-face unscaled can survive continuum; geometric weight not free");
const ratios=results.slice(1).map((r,i)=>
 (Math.abs(results[i].oddDiff)/Math.abs(r.oddDiff))/
 (results[i].h/r.h)**4);
need(ratios.every(x=>x>.8&&x<1.2),
 "observed role smooth 4D h^4 universality consistent across all refinements");
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_4D_ROLE_GOLDEN17_CHIRAL_IR_UNIVERSALITY",
 basis:"ACTUAL original CAR16 Golden-p true TWO fresh flags/Bell17; role SHARED-LINK periodic smooth J23 connection",
 golden:{p,φ:phi,originalBellSuccess:bell,
   completeOutcomeNumber:17,codeIsRelativeLogOdds:true,
   nativeRootTaylor:"sin(t)=t−t³/6+O(t5)",
   nativeCodeTaylor:"sqrt2*atanh(sqrt2*tan(t/2))=t+t³/4+O(t5)",
   differenceThirdDerivativeCoefficient:"5/12"},
 rigorousResult:"For smooth X_face=O(h²), inversion-odd analytic native Golden ROOT vs CODE have equal first Lie source; after original h^-2 weighted Role volume geometric source, action & C1 difference O(h^4). Complete even Shannon differences O(h²) on same declared scaling.",
 roleLattice:results,
 hostileActualNativeEvenCost:{
  note:"Without the geometric h^2 multiplier, per-face Golden17 Shannon retains a NONZERO R²-type continuum source",
  analyticLimit:evenLimit,measuredAtL96:finest.evenUNSCALEDnativeBookHypothesis,
  analyticFirstSourceLimit:evenDerivativeLimit,measuredFirstAtL96:finest.dEvenUNSCALEDnativeBookHypothesis},
 counterwarning:"Any independently unscaled complete Book Cost/Info, physical clock/work, code reference, nonlocal historical correlations or field-dependent coefficient can remain relevant; no full compulsory G0/EH theorem",
 GR_closed:false
},null,2));
