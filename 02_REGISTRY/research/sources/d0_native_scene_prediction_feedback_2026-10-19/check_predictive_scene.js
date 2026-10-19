#!/usr/bin/env node
"use strict";
// Exact 33-state/718-edge D0 scene controls. No external imports.
// Finite complete predictive-record feedback, not compulsory native Book F_N.
const p=(Math.sqrt(5)-1)/2,ell=-Math.log(p),z=2**-20,n=33;
const zone=Array.from({length:n},(_,i)=>i<9?0:i<20?1:2);
const E=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(zone[i]!==zone[j])E.push([i,j]);
const assert=(x,msg)=>{if(!x)throw Error(msg);};
const close=(x,y,eps=1e-10)=>assert(Math.abs(x-y)<eps,"number mismatch "+x+" vs "+y);
const Id=()=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const transpose=A=>A.map((row,i)=>row.map((_,j)=>A[j][i]));
function pf(K,trans=false){
 let a=new Array(n).fill(1/n);
 for(let k=0;k<1100;k++){
  const b=new Array(n).fill(0);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(trans)b[j]+=a[i]*K[i][j];else b[i]+=K[i][j]*a[j];
  const total=b.reduce((s,x)=>s+x,0);for(let i=0;i<n;i++)b[i]/=total;
  const err=Math.max(...b.map((x,i)=>Math.abs(x-a[i])));
  a=b;if(err<1e-16)break;
 }
 let lambda=0;for(let i=0;i<n;i++)for(let j=0;j<n;j++)lambda+=(trans?K[j][i]:K[i][j])*a[j];
 return {a,lambda};
}
function scene(t=0,fugacity=z,gauge=false){
 const info=Array.from({length:n},(_,i)=>.18*Math.cos((i+1)*.37));
 const K=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>{
  if(zone[i]===zone[j])return 0;
  const cost=1+(i===0&&j===9?t:0)+(gauge?.23+.07*(info[j]-info[i]):0);
  return Math.exp(-ell*cost);
 }));
 const R=pf(K),L=pf(K,true);let pi=R.a.map((v,i)=>v*L.a[i]);
 const norm=pi.reduce((s,x)=>s+x,0);pi=pi.map(x=>x/norm);
 const P=K.map((row,i)=>row.map((v,j)=>v*R.a[j]/(R.lambda*R.a[i])));
 const T=P.map((row,i)=>row.map((v,j)=>v*Math.sqrt(pi[i]/pi[j])));
 const TT=mul(transpose(T),T);
 const F=TT.map((row,i)=>row.map((v,j)=>(i===j?1:0)-v));
 const G=F.map((row,i)=>row.map((v,j)=>(i===j?1:0)-fugacity*v));
 const chol=Array.from({length:n},()=>new Array(n).fill(0));
 const pivots=[];let J=0,good=1;
 for(let i=0;i<n;i++)for(let j=0;j<=i;j++){
  let v=G[i][j];for(let k=0;k<j;k++)v-=chol[i][k]*chol[j][k];
  if(i===j){
   assert(v>=1-fugacity-1e-12&&v<1,"Cholesky pivot not positive branch");
   chol[i][j]=Math.sqrt(v);pivots.push(v);good*=v;J-=Math.log(v);
  }else chol[i][j]=v/chol[j][j];
 }
 let after=1,fail=0;for(const d of pivots){fail+=after*(1-d);after*=d;}
 close(good+fail,1,1e-12);
 for(let u=0;u<n;u++)close(P[u].reduce((s,v)=>s+v,0),1,1e-12);
 for(let v=0;v<n;v++)close(P.reduce((s,row,u)=>s+pi[u]*row[v],0),pi[v],1e-12);
 return {K,R,L,pi,P,T,F,G,pivots,J,good,fail};
}
function inverse(B){
 const A=B.map((row,i)=>[...row,...Id()[i]]);
 for(let j=0;j<n;j++){
  let r=j;for(let i=j+1;i<n;i++)if(Math.abs(A[i][j])>Math.abs(A[r][j]))r=i;
  assert(Math.abs(A[r][j])>1e-14,"singular return");
  [A[j],A[r]]=[A[r],A[j]];
  const d=A[j][j];for(let k=0;k<2*n;k++)A[j][k]/=d;
  for(let i=0;i<n;i++)if(i!==j){let v=A[i][j];for(let k=0;k<2*n;k++)A[i][k]-=v*A[j][k];}
 }
 return A.map(row=>row.slice(n));
}
function matrixSource(base,up,dn,h,q){
 const dT=up.T.map((row,i)=>row.map((x,j)=>(x-dn.T[i][j])/(2*h)));
 const X=mul(transpose(dT),base.T),Y=mul(transpose(base.T),dT);
 const dF=X.map((row,i)=>row.map((x,j)=>-x-Y[i][j]));
 const R=inverse(base.G),N=mul(R,dF);
 return q*N.reduce((s,row,i)=>s+row[i],0);
}
function run(){
 assert(E.length===718,"wrong native graph");
 const degree=Array.from({length:n},(_,i)=>E.filter(v=>v[0]===i).length);
 assert(degree.reduce((s,d)=>s+d*d,0)===15708&&degree.reduce((s,d)=>s+d-1,0)===685,"wrong real scene paths");
 const base=scene(),gauged=scene(0,z,true);
 let maxP=0,maxPi=0;
 for(let i=0;i<n;i++){maxPi=Math.max(maxPi,Math.abs(base.pi[i]-gauged.pi[i]));
  for(let j=0;j<n;j++)maxP=Math.max(maxP,Math.abs(base.P[i][j]-gauged.P[i][j]));}
 assert(maxP<1e-12&&maxPi<1e-12,"noncanonical Book endpoint gauge");
 const mu=base.R.a.map(v=>v/base.R.a.reduce((s,x)=>s+x,0));
 const cylinder=mu[0]*base.P[0][9]*base.P[9][0];
 const owned=mu[0]/Math.pow(base.R.lambda/p,2);
 close(cylinder,owned,1e-13);
 let last=mu.slice();
 for(let iter=0;iter<8;iter++)last=base.P[0].map((_,j)=>last.reduce((s,v,i)=>s+v*base.P[i][j],0));
 const mixing=Math.max(...last.map((v,i)=>Math.abs(v-base.pi[i])));
 let varianceError=0;
 for(let trial=1;trial<=4;trial++){
  const f=Array.from({length:n},(_,i)=>Math.sin((i+1)*trial*.117));
  const Pf=base.P.map(row=>row.reduce((s,v,j)=>s+v*f[j],0));
  const risk=E.reduce((s,[u,v])=>s+base.pi[u]*base.P[u][v]*(f[v]-Pf[u])**2,0);
  const quadratic=f.reduce((s,x,i)=>s+base.pi[i]*x*base.F[i].reduce((q,w,j)=>q+w*f[j],0),0);
  varianceError=Math.max(varianceError,Math.abs(risk-quadratic));
 }
 assert(varianceError<1e-12,"full recorded conditional variance identity");
 const constantKernel=Math.max(...base.F.map(row=>Math.abs(row.reduce((s,v)=>s+v,0))));
 assert(constantKernel<1e-11,"wrong constant null record");
 let lo=20,hi=25;for(let k=0;k<85;k++){const mid=(lo+hi)/2;if(mid**3-359*mid-2574>0)hi=mid;else lo=mid;}
 const rho=(lo+hi)/2,sumActive=3-718/rho**2,prodActive=3-1436/rho**2+359**2/rho**4;
 const exact=-30*Math.log1p(-z)-Math.log(1-sumActive*z+prodActive*z*z);
 close(exact,base.J,2e-11);
 const h=.001,up=scene(h),dn=scene(-h),source=(up.J-dn.J)/(2*h),actual=matrixSource(base,up,dn,h,z);
 assert(Math.abs(source)>1e-12&&Math.abs(source-actual)<1e-10,"native Cost→J first source");
 const diag=.01,bc=scene(0,diag),uc=scene(h,diag),dc=scene(-h,diag);
 const sourceTest=(uc.J-dc.J)/(2*h),analyticTest=matrixSource(bc,uc,dc,h,diag);
 assert(Math.abs(sourceTest-analyticTest)<1e-8,"nonfrozen preparation source");
 const wrongRandomWalk=-30*Math.log1p(-z)-Math.log(1-119*z/80+14001*z*z/25600);
 assert(Math.abs(wrongRandomWalk-base.J)>1e-9,"Perron history falsely identified with random walk");
 return {status:"PASS",trueScene:{vertices:n,directedEdges:718,twoStepWalks:15708,observableCostQuotientDimension:685},
  trueOwnedHistory:{nativeInitialSite0:mu[0],derivedStationarySite0:base.pi[0],
    stationaryMixingAfter8Ticks:mixing,exactRecordedCylinderError:Math.abs(cylinder-owned)},
  complete718Record:{conditionalVarianceError:varianceError,constantNullError:constantKernel},
  full34OutcomeFeedback:{z,predictedArchiveModes:30,activeModes:2,stationaryModes:1,
    originalPerronRoot:rho,fullJ:base.J,allGoodProbability:base.good,allFirstFailures:base.fail,
    outcomeTotal:base.good+base.fail,hostileWrongRandomWalkJ:wrongRandomWalk},
  originalEdgeSource:{edge:"0-to-9",derivativeActualZ:source,fullMovingPiSource:actual,
    derivativeDiagnosticZ001:sourceTest,diagnosticExactSource:analyticTest},
  costGauge:{maxKernelError:maxP,maxPiError:maxPi},
  boundary:"Explicit constructed full native-type record, not compulsory physical D0 Book F_N or GR."};
}
const output=run();
if(typeof console!=="undefined")console.log(JSON.stringify(output,null,2));
output;
