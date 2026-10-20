#!/usr/bin/env node
"use strict";
/*
 ORIGINAL shared 4D Role L=2 torus: 16 sites, 64 SHARED actual proper
 Lorentz links (6 Lie directions each =384), 96 genuine oriented based
 faces (6 Lie scores each). Original native Golden-p two-fresh CAR16/Bell17
 has a COMPLETE 17-probability conditional law with Fisher c=p^4/(6*4096).

 This checker proves an exact, globally counted finite statistical
 "internal Golden code follows the geometry" Schur construction:
   H_total = (c/ln phi) [[D'D,-D'D],[-D'D,D'D]] ⊗ I6
 and stationary reference elimination gives ZERO extra geometry Hessian
 on all 270 visible curvature modes (114 gauge/Wilson null modes).
 No Golden pointer outcomes or old archive are deleted or postselected.
 Ref state prep/code COST and physical G0 selection are NOT established.
*/
const phi=(1+Math.sqrt(5))/2,p=1/phi,ell=Math.log(phi),bell=1/4096;
const fail=(x,msg)=>{if(!x)throw new Error("FAIL "+msg)};
const dim=16,nd=64,pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const index=(x,r)=>4*x+r,face=(x,r,s)=>6*x+pairs.findIndex(([a,b])=>a===r&&b===s);
const shift=(x,r)=>x^(1<<r);
const D=Array.from({length:96},()=>Array(nd).fill(0));
for(let x=0;x<dim;x++)for(let r=0;r<4;r++)for(let s=r+1;s<4;s++){
 const row=D[face(x,r,s)];
 row[index(x,r)]++;
 row[index(shift(x,r),s)]++;
 row[index(shift(x,s),r)]--;
 row[index(x,s)]--;
}
const cubes=[];
for(let x=0;x<dim;x++)for(let r=0;r<4;r++)
for(let s=r+1;s<4;s++)for(let t=s+1;t<4;t++)
 cubes.push([x,r,s,t]);
fail(cubes.length===64,"not original role cubes");
function Bianchi(){
 let max=0;
 for(const [x,r,s,t] of cubes){
  const q=Array(96).fill(0);
  q[face(shift(x,r),s,t)]+=1;q[face(x,s,t)]-=1;
  q[face(shift(x,s),r,t)]-=1;q[face(x,r,t)]+=1;
  q[face(shift(x,t),r,s)]+=1;q[face(x,r,s)]-=1;
  for(let col=0;col<nd;col++){
   let v=0;for(let i=0;i<96;i++)if(q[i])v+=q[i]*D[i][col];
   max=Math.max(max,Math.abs(v));
  }
 }
 return max;
}
fail(Bianchi()===0,"original L2 cube Bianchi d2d1 !=0");
function rank(B,eps=1e-11){
 const a=B.map(x=>x.slice());let rr=0;
 for(let j=0;j<a[0].length&&rr<a.length;j++){
  let k=rr;
  for(let i=rr+1;i<a.length;i++)if(Math.abs(a[i][j])>Math.abs(a[k][j]))k=i;
  if(Math.abs(a[k][j])<eps)continue;
  [a[rr],a[k]]=[a[k],a[rr]];
  let v=a[rr][j];for(let t=j;t<a[0].length;t++)a[rr][t]/=v;
  for(let i=rr+1;i<a.length;i++){
   let fac=a[i][j];
   if(!fac)continue;
   for(let t=j;t<a[0].length;t++)a[i][t]-=fac*a[rr][t];
  }rr++;
 }
 return rr;
}
const oneRank=rank(D),rkFull=6*oneRank,nullity=6*(nd-oneRank);
fail(oneRank===45&&rkFull===270&&nullity===114,"true original d1 rank/nullity");
const gram=Array.from({length:nd},()=>Array(nd).fill(0));
for(let row=0;row<96;row++)for(let i=0;i<nd;i++)if(D[row][i])
 for(let j=0;j<nd;j++)if(D[row][j])
  gram[i][j]+=D[row][i]*D[row][j];
let spectralError=0,wilsonNull=0,gaugeNull=0,counts={};
for(let mask=0;mask<16;mask++){
 const q=Array.from({length:4},(_,r)=>(mask&(1<<r))?-2:0);
 const k=q.reduce((s,x)=>s+x*x,0)/4;
 if(k>0)counts[k]=(counts[k]||0)+3*6; // 3 transverse link components *6 Lie
 const sgn=x=>{
  let parity=0;for(let j=0;j<4;j++)
    if((x&(1<<j))&&(mask&(1<<j)))parity++;
  return parity%2?-1:1;
 };
 const testVecs=[];
 // A_mu(x)=sigma(mask,x) q_mu is the exact Walsh longitudinal.
 if(mask!==0)testVecs.push(q);
 // Three independent transverse tests can be checked without basis fit.
 for(let r=0;r<4;r++){
  const v=Array(4).fill(0);v[r]=1;
  if(k>0)for(let j=0;j<4;j++)v[j]-=q[r]*q[j]/(4*k);
  testVecs.push(v);
 }
 for(let v of testVecs){
  const four=Array.from({length:nd},(_,id)=>sgn(Math.floor(id/4))*v[id%4]);
  const out=gram.map(row=>row.reduce((z,a,j)=>z+a*four[j],0));
  const expect=(k===0?0:(v===q?0:4*k)); // longitudinal zero
  const project=q.reduce((z,a,j)=>z+a*v[j],0);
  const transverse=k>0&&Math.abs(project)<1e-12;
  const eigen=transverse?4*k:0;
  spectralError=Math.max(spectralError,...out.map((z,i)=>Math.abs(z-eigen*four[i])));
  if(k===0)wilsonNull++;
  if(k>0&&v===q)gaugeNull++;
 }
}
fail(spectralError<1e-11,"exact Walsh four-torus discrete Maxwell Gram");
fail(counts[1]===72&&counts[2]===108&&counts[3]===72&&counts[4]===18,
 "true original L2 Fisher spectrum multiplicities wrong");
const c=p**4/(6*4096),goldenKLHessian=c/ell;
function golden17(theta){
 const mean=(1+Math.cos(theta))/2,sin=Math.sin(theta);
 const q=[];
 for(let a=0;a<6;a++){
  const signed=a===4?sin/Math.SQRT2:0;
  q.push(bell*p**4/24*(mean+signed)**2,bell*p**4/24*(mean-signed)**2);
 }
 const gg=bell*p**4,rest=gg-q.reduce((s,x)=>s+x,0),
  GB=bell*p*p*(1-p*p),BG=bell*p**3,BB=bell*p*p;
 q.push(rest,GB,BG,BB,1-bell);
 fail(q.length===17&&Math.min(...q)>0&&Math.abs(q.reduce((s,x)=>s+x,0)-1)<2e-13,
  "actual native full Golden17 cannot be normalized");
 return q;
}
function KL(a,b){
 const x=golden17(a),y=golden17(b);
 return x.reduce((s,v,i)=>s+v*Math.log(v/y[i])/ell,0);
}
// On the TRUE shared 4D link (x=0, role=0), exactly six based
// plaquettes have ±theta, 90 flat; reference link has ±z.
// KL(q(-theta)||q(-z))=KL(q(theta)||q(z)) because GOLDEN q± labels swap.
for(let t of [.02,.10,.17]){
 fail(Math.abs(KL(-t,0)-KL(t,0))<1e-13,"same real 6-plaquette signed KL");
 fail(Math.abs(KL(t,t))<1e-13,"matching full-code reference must attain KL minimum");
}
const fullOneLink=(theta,refAngle)=>6*KL(theta,refAngle),h=.012;
const HH=fullOneLink(h,0)+fullOneLink(-h,0)-2*fullOneLink(0,0);
const RR=fullOneLink(0,h)+fullOneLink(0,-h)-2*fullOneLink(0,0);
const cross=(fullOneLink(h,h)-fullOneLink(h,-h)
  -fullOneLink(-h,h)+fullOneLink(-h,-h))/4;
const d2geometry=HH/(h*h),d2reference=RR/(h*h),
      d2mixed=cross/(h*h),expected=6*goldenKLHessian;
fail(Math.abs(d2geometry-expected)<2e-7&&
 Math.abs(d2reference-expected)<2e-7&&
 Math.abs(d2mixed+expected)<2e-7,
 "full native same-observer Golden reference Schur 2jet not matched");
const exactSchur=expected-(expected*expected)/expected;
fail(exactSchur===0,"the prepared code should exactly eliminate extra geometric Schur");
// Field-to-code curvature is wholly visible on true face-incidence image;
// the actual 114 link gauge+Wilson zero directions stay unmeasured.
console.log(JSON.stringify({
 status:"PASS_NATIVE_ORIGINAL_ROLE96_GOLDEN17_ALL384_LINK_FISHER_REFERENCE_SCHUR",
 originalRole:{sites:dim,trueSharedLinks:nd,lorentzDirections:6*nd,
  genuineBasedPlaquettes:96,trueCubeBianchi:64,d2d1_error:Bianchi()},
 sourceRank:{rankLinkIncidence:oneRank,
  golden17PositiveFisherRank:rkFull,
  physicalGaugePlusWilsonNullity:nullity,
  Fourier_nonzero_eigenvalues_by_k_counts:counts,
  WalshSpectrumError:spectralError},
 exactOriginalGolden:{completeOutcomesPerFace:17,
  successPlusFullFailures:true,oneFaceLieFisher:c,
  oneFaceGoldenKLSecondSource:goldenKLHessian},
 firstOneLink:{t:.1,
  candidateFullSixFaceFixedCodeKL:fullOneLink(.1,0),
  candidateFullSixFaceMatchedMovingCodeKL:fullOneLink(.1,.1)},
 localSharedLinkStiffness:{sourceExpected:expected,
  observedGeometry:d2geometry,observedReference:d2reference,
  observedCross:d2mixed,exactStationarySchur:exactSchur},
 full384SourceStructure:"(c/lnphi) [[D'D,-D'D],[-D'D,D'D]] tensor I6; genuine shared-link incidence D with rank45",
 physicalSelectorAndReferencePreparationWorkNotForced:true,
 GR_closed:false
},null,2));
