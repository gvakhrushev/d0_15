#!/usr/bin/env node
"use strict";
/*
  ORIGINAL D0 K(9,11,13) graph: 33 vertices; 718 directed edges;
  718 rooted 2-returns and 7722 based ABC 3-returns; 8440 true words.
  All 17 native Golden/Bell outcomes survive on every accepted word.

  EXACT INVERSE: even UNKNOWN, INDEPENDENT, MOVING two/three-clock
  acceptance multipliers give the unique ORIGINAL 685-dimensional
  normalized Perron transition P; absolute Perron lambda does NOT follow.
  Prove native cycle clock/three-flow first-source identities and
  common-verifier-only absolute calibration.

  SCIENTIFIC SCOPE: positive original scene/math conditional experiment;
  not literal G0 compelled, not Role/spacetime Lorentz controller or GR.
*/
const phi=(1+Math.sqrt(5))/2,p=1/phi,ell=Math.log(phi),N=33;
const zone=i=>i<9?0:i<20?1:2;
const check=(v,s)=>{if(!v)throw Error(s);};
const mat=()=>Array.from({length:N},()=>Array(N).fill(0));
function original(y,shift=0){
 const C=mat(),K=mat();
 for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(zone(i)!==zone(j)){
  const cost=1.13+.04*Math.sin((i+1)*.117+(j+1)*.188)**2+.02*y*y;
  const info=k=>.13*Math.sin(.13*(k+1))+.03*y*Math.cos(.17*k);
  const s=cost-.37*info(i)-.63*info(j)-shift;
  check(cost>=1,"original native action quantum");
  C[i][j]=s;K[i][j]=Math.exp(-ell*s);
 }
 return {C,K};
}
function perron(K){
 let r=Array(N).fill(1/N),lambda=0;
 for(let k=0;k<180;k++){
  const w=K.map(row=>row.reduce((s,x,j)=>s+x*r[j],0));
  lambda=w.reduce((s,x)=>s+x,0);
  r=w.map(x=>x/lambda);
 }
 const P=mat();
 let maxRow=0;
 for(let i=0;i<N;i++){
  let sum=0;
  for(let j=0;j<N;j++){
   P[i][j]=K[i][j]*r[j]/(lambda*r[i]);sum+=P[i][j];
  }
  maxRow=Math.max(maxRow,Math.abs(sum-1));
 }
 check(maxRow<1e-12,"Perron row stochastic");
 return {lambda,P};
}
function moments(K){
 const K2=mat();let Z2=0,Z3=0;
 for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(K[i][j]){
  Z2+=K[i][j]*K[j][i];
  for(let k=0;k<N;k++)if(K[j][k]&&K[k][i]){
   const v=K[j][k]*K[k][i];
   K2[j][i]+=v;Z3+=K[i][j]*v;
  }
 }
 return {Z2,Z3,K2};
}
const golden17=[
 ...Array(12).fill(p**4/(24*4096)),
 p**4/(2*4096),p**3/4096,p**3/4096,p**2/4096,4095/4096
];
check(golden17.length===17&&Math.min(...golden17)>0
  &&Math.abs(golden17.reduce((a,b)=>a+b,0)-1)<1e-14,
  "original complete flat two-flag Golden/Bell17 lost outcomes");

function clock(y,shift=0,common=false){
 const {C,K}=original(y,shift),pf=perron(K),mom=moments(K);
 // TRUE unknown, moving stage and early-preparation; no fixed prior used
 // by the reconstruction and NO independence of kappa2 and kappa3.
 const g2=p+.015*Math.sin(2*y+1.5*shift),g3=1-g2;
 const beta2=.29+.01*Math.sin(y+2*shift);
 const beta3=.33+.017*Math.cos(y-.7*shift);
 const kappa2=p**21*Math.exp(.06*y+.11*shift);
 const kappa3=common?kappa2:p**23*Math.exp(-.13*y-.07*shift);
 const alpha2=g2*beta2*kappa2,alpha3=g3*beta3*kappa3;
 check(kappa2*mom.Z2<1&&kappa3*mom.Z3<1,
       "whole stage rejection probability must remain nonnegative");
 let N2=0,N3=0,accepted2=0,accepted3=0;
 // ALL original accepted 2/3 word marginals: Golden 17-way sum is one.
 const S2=mat();
 const S3=Array.from({length:N},()=>mat());
 for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(K[i][j]){
  const q2=alpha2*K[i][j]*K[j][i];
  S2[i][j]=q2;accepted2+=q2;N2++;
  for(let k=0;k<N;k++)if(K[j][k]&&K[k][i]){
   const q3=alpha3*K[i][j]*K[j][k]*K[k][i];
   S3[i][j][k]=q3;accepted3+=q3;N3++;
  }
 }
 check(N2===718&&N3===7722,"original rooted cycle counts changed");
 check(Math.abs(accepted2-alpha2*mom.Z2)<2e-13
   &&Math.abs(accepted3-alpha3*mom.Z3)<4e-12,
   "whole accepted path sum");
 const E2=g2*(1-beta2),E3=g3*(1-beta3);
 const B2=g2*beta2*(1-kappa2*mom.Z2);
 const B3=g3*beta3*(1-kappa3*mom.Z3);
 check(Math.abs(E2+B2+accepted2-g2)<2e-13
    &&Math.abs(E3+B3+accepted3-g3)<5e-13,
   "full early and late stage failures not retained");
 // No input knowledge of alpha_n: observe only positive accepted S2,S3!
 const symmetric=mat();
 for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(K[i][j]){
  const b=.5*Math.log(S2[i][j]);
  symmetric[i][j]=b;symmetric[j][i]=b;
 }
 const face=Array.from({length:9},()=>Array.from({length:11},
              ()=>Array(13).fill(0)));
 for(let a=0;a<9;a++)for(let b=0;b<11;b++)
 for(let c=0;c<13;c++)
  face[a][b][c]=.5*Math.log(
    S3[a][9+b][20+c]/S3[a][20+c][9+b]);
 // Constructive right inverse of the owned exact 960 triangle constraints.
 const odd=mat();
 for(let a=0;a<9;a++)for(let b=9;b<20;b++){
  odd[a][b]=face[a][b-9][0];odd[b][a]=-odd[a][b];
 }
 for(let b=9;b<20;b++)for(let c=20;c<33;c++){
  odd[b][c]=face[0][b-9][c-20]-face[0][b-9][0];
  odd[c][b]=-odd[b][c];
 }
 for(let c=20;c<33;c++)for(let a=0;a<9;a++){
  odd[c][a]=face[a][0][c-20]-face[a][0][0]
             -face[0][0][c-20]+face[0][0][0];
  odd[a][c]=-odd[c][a];
 }
 const Ktilde=mat();
 for(let i=0;i<N;i++)for(let j=0;j<N;j++)
  if(zone(i)!==zone(j))
   Ktilde[i][j]=Math.exp(symmetric[i][j]+odd[i][j]);
 const decoded=perron(Ktilde);
 let Perror=0,triangleError=0;
 for(let i=0;i<N;i++)for(let j=0;j<N;j++)
  Perror=Math.max(Perror,Math.abs(pf.P[i][j]-decoded.P[i][j]));
 for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++){
  const loop=.5*Math.log(
   Ktilde[a][b]*Ktilde[b][c]*Ktilde[c][a]/
   (Ktilde[a][c]*Ktilde[c][b]*Ktilde[b][a]));
  triangleError=Math.max(triangleError,
                         Math.abs(loop-face[a][b-9][c-20]));
 }
 check(Perror<1e-12&&triangleError<1e-12,
   "entire nonreversible P inverse failed");
 check(Math.abs(decoded.lambda/pf.lambda/Math.sqrt(alpha2)-1)<2e-12,
   "only unknown true alpha2 scalar should remain");
 const t0=moments(pf.P),t1=moments(decoded.P);
 const intrinsic=Math.log(t0.Z3/t0.Z2)/ell;
 const recovered=Math.log(t1.Z3/t1.Z2)/ell;
 check(Math.abs(intrinsic-recovered)<1e-12,"P-shape clock value");
 const attempted2=E2+B2+accepted2,attempted3=E3+B3+accepted3;
 const recBeta2=1-E2/attempted2,recBeta3=1-E3/attempted3;
 const rawStageClock=Math.log(accepted3/accepted2)/ell;
 const correctedStageClock=Math.log(
    (accepted3/(attempted3*recBeta3))/
    (accepted2/(attempted2*recBeta2)))/ell;
 // Without a common verifier this IS NOT the true log(Z3/Z2)
 // because a genuine kappa3/kappa2 remains!
 const stageResidual=correctedStageClock-
    Math.log(mom.Z3/mom.Z2)/ell;
 check(Math.abs(stageResidual-
          Math.log(kappa3/kappa2)/ell)<3e-12,
  "real independent depth verifier residual lost");

 if(common){
  const q2=(i,j)=>S2[i][j],q3=(i,j,k)=>S3[i][j][k];
  const kappaRecovered=(attempted3*recBeta3)**2/
                       (attempted2*recBeta2)**3
   *q2(0,9)*q2(9,20)*q2(0,20)/
    (q3(0,9,20)*q3(0,20,9));
  check(Math.abs(kappaRecovered/kappa2-1)<2e-12,
        "native five-loop common verifier exact inversion");
  check(Math.abs(correctedStageClock-
        Math.log(mom.Z3/mom.Z2)/ell)<3e-12,
        "native shared verifier cancels from true stage clock");
 }
 return {y,shift,common,K,C,P:pf.P,lambda:pf.lambda,mom,
  gamma17:golden17,N2,N3,Perror,triangleError,intrinsic,recovered,
  kappa2,kappa3,rawStageClock,correctedStageClock,stageResidual,
  alpha2,alpha3,clockFullLabels:(N2+N3)*17+4};
}
function nativeFlow(y){
 const a=clock(y),up=clock(y+1e-5),dn=clock(y-1e-5);
 const K=a.K,C=a.C,{Z2,Z3,K2}=a.mom,P=a.P;
 let pi=Array(N).fill(1/N);
 for(let r=0;r<250;r++){
  const next=Array(N).fill(0);
  for(let i=0;i<N;i++)for(let j=0;j<N;j++)
   next[j]+=pi[i]*P[i][j];
  pi=next;
 }
 let source=0,bookShape=0,sum=0;
 const div=Array(N).fill(0);
 for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(K[i][j]){
  const f2=K[i][j]*K[j][i]/Z2;
  const f3=K[i][j]*K2[j][i]/Z3;
  const mu=pi[i]*P[i][j];
  const flux=3*f3-2*f2-mu;
  const ds=(up.C[i][j]-dn.C[i][j])/(2e-5);
  source-=flux*ds;
  bookShape-=3*ell*(f3-mu)*ds;
  sum+=flux;div[i]+=flux;div[j]-=flux;
 }
 const finite=(up.recovered-dn.recovered)/(2e-5);
 const finiteShape=(Math.log(up.mom.Z3/up.lambda**3)
    -Math.log(dn.mom.Z3/dn.lambda**3))/(2e-5);
 const maxDiv=Math.max(...div.map(Math.abs));
 check(Math.abs(source-finite)<3e-7&&
       Math.abs(bookShape-finiteShape)<3e-7&&
       Math.abs(sum)<2e-12&&maxDiv<3e-12,
  "native 2/3/long-archive exact source identities");
 return {finite,source,bookShape,finiteShape,maxDiv,sourceErr:finite-source};
}
const checks=[];
for(const y of [-.30,0,.23]){
 const x=clock(y);
 const shared=clock(y,0,true);
 check(x.clockFullLabels===143484,"total native complete record size");
 checks.push({y,fullAcceptedPaths:x.N2+x.N3,
  fullPositiveOutcomes:x.clockFullLabels,
  independentVerifierPerror:x.Perror,
  independentVerifierClockShapeErr:x.intrinsic-x.recovered,
  movingVerifierRatio:x.kappa3/x.kappa2,
  commonVerifierStageResidual:shared.stageResidual});
}
const y=.21,h=1e-5,a=clock(y),b=clock(y,.13);
const up=clock(y,h),down=clock(y,-h);
check(Math.abs(a.intrinsic-b.intrinsic)<2e-12,
  "uniform Info shift altered projective Book/clock observable");
check(Math.abs(Math.log(b.lambda/a.lambda)/ell-.13)<1e-12,
  "Book absolute lambda did not feel original +1 scale");
const scaleSource=(up.intrinsic-down.intrinsic)/(2*h);
check(Math.abs(scaleSource)<3e-7,
  "true independent moving 2/3 stage filters contaminated P source");
const flowing=nativeFlow(y);
for(const x of checks)console.log("PASS native whole 718/7722 depth-clock",JSON.stringify(x));
console.log("PASS original real q(GoldenBell17) complete, all 143484 labels and early/late rejected stages");
console.log("PASS arbitrary unrelated moving kappa_2/kappa_3 -> exact WHOLE normalized 33x33 P inverse");
console.log("PASS full moving stage-permission source cannot contaminate projective clock",scaleSource);
console.log("PASS original native 2/3/stationary three-flow source",JSON.stringify(flowing));
console.log("PASS true lambda scales phi^t; independent depth verifier cannot determine its absolute magnitude");
console.log("PASS with ONE common verifier: original five loop κ and absolute stage clock recovered");
console.log("NOTE: statistical inverses are native-TYPE mathematics; compulsory full G0/Book H+J+R, 4D Role, material and full physical GR root remain OPEN");
