#!/usr/bin/env node
// D0 actual K(9,11,13) ORIGINAL one-sided Perron trace -> ONE complete
// 718-edge conditional-expectation instrument -> rank32 true feedback.
// Pure JS; no dependencies. This is a mathematical native-scene device,
// NOT the literal v8/full Book03 physically admitted programme.
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),z=2**-20,n=33;
const zone=Array.from({length:n},(_,i)=>i<9?0:i<20?1:2);
const edges=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(zone[u]!==zone[v])edges.push([u,v]);
if(edges.length!==718)throw Error("not actual 718 original directed edges");
const nearly=(a,b,tol=1e-10)=>{if(Math.abs(a-b)>tol)throw Error("not equal "+a+" "+b+" tol "+tol)};
const rho=(()=>{let r=22;for(let k=0;k<35;k++)r-=(r*r*r-359*r-2574)/(3*r*r-359);return r})();
nearly(rho**3-359*rho-2574,0,1e-9);
const r0=Array.from({length:n},(_,i)=>1/(rho+[9,11,13][zone[i]])),sumR=r0.reduce((a,b)=>a+b);
const r=r0.map(x=>x/sumR),norm2=r.reduce((a,v)=>a+v*v,0);
const pi=r.map(v=>v*v/norm2);
const P=Array.from({length:n},()=>new Float64Array(n));
for(const[u,v]of edges)P[u][v]=r[v]/(rho*r[u]);
for(let u=0;u<n;u++)nearly(P[u].reduce((a,b)=>a+b),1,1e-13);
for(let v=0;v<n;v++)nearly(P.reduce((s,row,u)=>s+pi[u]*row[v],0),pi[v],1e-13);
let mu0=Float64Array.from(r),maxDiff0=0;
for(let i=0;i<n;i++)maxDiff0=Math.max(maxDiff0,Math.abs(mu0[i]-pi[i]));
if(maxDiff0<1e-3)throw Error("one-sided must not be falsely stationary");
const d= Math.sqrt(rho*rho-10296/rho);
const eigOther=[(-rho+d)/2,(-rho-d)/2],q=Math.max(...eigOther.map(x=>Math.abs(x/rho)));
function chiNorm(mu){return Math.sqrt(mu.reduce((s,v,i)=>s+(v-pi[i])**2/pi[i],0))}
const normStart=chiNorm(mu0),mixing=[];
for(const k of [0,1,2,4,8,12,20]){
 if(k){const prev=mixing.at(-1);}// cosmetic; stage recomputed below
 let state=Float64Array.from(mu0);
 for(let step=0;step<k;step++){
   const nxt=new Float64Array(n);
   for(const[u,v]of edges)nxt[v]+=state[u]*P[u][v];
   state=nxt;
 }
 const delta=chiNorm(state);
 if(delta>normStart*q**k+3e-13)throw Error("original native Perron mixing failed");
 mixing.push({k,chi2Distance:delta,spectralUpper:normStart*q**k});
}
const T=Array.from({length:n},()=>new Float64Array(n));
let margPast=new Float64Array(n),margFuture=new Float64Array(n);
for(const[u,v]of edges){
 const mu=pi[u]*P[u][v];
 const past=Math.sqrt(mu/pi[u]),future=Math.sqrt(mu/pi[v]);
 margPast[u]+=past*past;margFuture[v]+=future*future;
 T[u][v]+=past*future;
}
for(let i=0;i<n;i++){
 nearly(margPast[i],1,1e-13);nearly(margFuture[i],1,1e-13);
 for(let j=0;j<n;j++)nearly(T[i][j],zone[i]!==zone[j]?1/rho:0,1e-13);
}
const identity=()=>Array.from({length:n},(_,i)=>Float64Array.from({length:n},(_,j)=>+(i===j)));
const F=identity();
for(let i=0;i<n;i++)for(let j=0;j<n;j++)for(let k=0;k<n;k++)F[i][j]-=T[k][i]*T[k][j];
// Literal ONE complete registered past/future edge probability: conditional
// variance equals the full positive quadratic form on 718 real transitions.
let varianceErr=0;
for(let trial=0;trial<8;trial++){
 const v=Array.from({length:n},(_,i)=>Math.sin((trial+1)*(.2+i*.13)));
 const Pf=Array.from({length:n},(_,u)=>P[u].reduce((s,x,j)=>s+x*v[j],0));
 const conditional=edges.reduce((s,[u,j])=>s+pi[u]*P[u][j]*(v[j]-Pf[u])**2,0);
 const e=F.reduce((s,row,i)=>s+Math.sqrt(pi[i])*v[i]*row.reduce((a,x,j)=>a+x*Math.sqrt(pi[j])*v[j],0),0);
 varianceErr=Math.max(varianceErr,Math.abs(e-conditional));
}
if(varianceErr>1e-12)throw Error("not real completed future-past variance");
// All original 30 ARCHIVE + active2 + stationary1 are present, with proper
// Perron-Doob (not degree-random-walk) active normalization.
const feig=eigOther.map(x=>1-(x/rho)**2),Jexact=-30*Math.log1p(-z)-Math.log(
  1-z*(1+5148/rho**3)+z*z*(5148/rho**3+(2574/rho**3)**2));
function choleskyLogdet(A){
 const L=Array.from({length:n},()=>new Float64Array(n));
 let log=0;
 for(let i=0;i<n;i++)for(let j=0;j<=i;j++){
  let v=A[i][j];for(let k=0;k<j;k++)v-=L[i][k]*L[j][k];
  if(i===j){if(v<=0)throw Error("not positive F event");L[i][j]=Math.sqrt(v);log+=Math.log(v);}
  else L[i][j]=v/L[j][j];
 }
 return log;
}
const good=F.map((row,i)=>Float64Array.from(row,(v,j)=>(i===j?1:0)-z*v));
const Jmatrix=-choleskyLogdet(good);
nearly(Jmatrix,Jexact,1e-12);
const nullVector=pi.map(Math.sqrt),Fnull=F.map(row=>row.reduce((s,x,j)=>s+x*nullVector[j],0));
if(Math.max(...Fnull.map(Math.abs))>1e-12)throw Error("stationary null mode is not preserved");
function initialEffect(theta,t,commonShift=0){
 const K=Array.from({length:n},()=>new Float64Array(n));
 const info=Array.from({length:n},(_,v)=>.23*(v%5)+.07*Math.sin((v+1)*t*.34));
 for(const[u,v]of edges){
  const extra=(u===0&&v===9)?t:0;
  const cost=2+commonShift+extra;
  K[u][v]=Math.exp(-ell*(cost-theta*info[u]-(1-theta)*info[v]));
 }
 function pf(trans){
  let v=new Float64Array(n).fill(1/n);
  for(let k=0;k<1000;k++){
   const w=new Float64Array(n);
   for(const[u,j]of edges){if(trans)w[j]+=K[u][j]*v[u];else w[u]+=K[u][j]*v[j];}
   const S=w.reduce((a,b)=>a+b);for(let i=0;i<n;i++)w[i]/=S;
   const err=Math.max(...w.map((x,i)=>Math.abs(x-v[i])));v=w;if(err<1e-16)break;
  }
  const AV=new Float64Array(n);
  for(const[u,j]of edges){if(trans)AV[j]+=K[u][j]*v[u];else AV[u]+=K[u][j]*v[j];}
  return{v,lambda:AV.reduce((a,b)=>a+b)};
 }
 const rv=pf(false),lv=pf(true),alpha=rv.v,beta=lv.v;
 let stat=Float64Array.from(alpha,(v,i)=>v*beta[i]);
 const sum=stat.reduce((a,b)=>a+b);stat=stat.map(x=>x/sum);
 const Pnow=K.map((row,i)=>Float64Array.from(row,(x,j)=>x*alpha[j]/(rv.lambda*alpha[i])));
 const Tnow=Pnow.map((row,i)=>Float64Array.from(row,(x,j)=>x*Math.sqrt(stat[i]/stat[j])));
 const Fnow=identity();
 for(let i=0;i<n;i++)for(let j=0;j<n;j++)for(let k=0;k<n;k++)Fnow[i][j]-=Tnow[k][i]*Tnow[k][j];
 const goodNow=Fnow.map((row,i)=>Float64Array.from(row,(v,j)=>(i===j?1:0)-z*v));
 return{J:-choleskyLogdet(goodNow),stat,P:Pnow,F:Fnow,lambda:rv.lambda};
}
const thetaList=[-.6,.25,1.3],sceneTheta=thetaList.map(theta=>initialEffect(theta,.15));
const commonShift=.17,unshifted=initialEffect(.25,.15),shifted=initialEffect(.25,.15,commonShift);
nearly(shifted.lambda/unshifted.lambda,Math.exp(-ell*commonShift),1e-13);
nearly(shifted.J,unshifted.J,1e-12);
for(let i=0;i<n;i++){
 nearly(shifted.stat[i],unshifted.stat[i],1e-12);
 for(let j=0;j<n;j++){
  nearly(shifted.P[i][j],unshifted.P[i][j],1e-12);
  nearly(shifted.F[i][j],unshifted.F[i][j],1e-12);
 }
}
for(let i=1;i<sceneTheta.length;i++){
 nearly(sceneTheta[i].J,sceneTheta[0].J,1e-11);
 for(let u=0;u<n;u++){
   nearly(sceneTheta[i].stat[u],sceneTheta[0].stat[u],1e-12);
   for(let v=0;v<n;v++)nearly(sceneTheta[i].P[u][v],sceneTheta[0].P[u][v],1e-12);
 }
}
const h=1e-3,derivative=(initialEffect(.25,.15+h).J-initialEffect(.25,.15-h).J)/(2*h);
if(Math.abs(derivative)<1e-12)throw Error("candidate return feedback lacks genuine Cost source");
console.log(JSON.stringify({
 status:"PASS",scene:{vertices:33,originalDirectedEdges:edges.length,nativeOneSidedStartNotStationary:maxDiff0},
 nativePerron:{rho,otherEigenvalues:eigOther,bulkMixingRatio:q,mixing},
 complete718EdgeReadings:{pastMarginalUnit:true,futureMarginalUnit:true,overlap:"exact original Perron Doob transfer",
    conditionalVarianceMaxError:varianceErr,innovationEdgeDimension:718-33},
 feedback:{rank:32,archiveMultiplicity30:true,stationaryKernel:1,activeEigenvalues:feig,
    Jclosed:Jexact,Jmatrix,goodProbability:Math.exp(-Jexact)},
 genuineCostPerturbation:{t:.15,costBase:2,oneEdgePerturbationDerivative:derivative,
    thetaConventionValues:thetaList,thetaFeedbackInvariant:true,uniformCostShift:commonShift,
    pressureChange:Math.log(shifted.lambda/unshifted.lambda)/ell,
    feedbackCostShiftChange:shifted.J-unshifted.J},
 boundary:"F_var is canonical for a specified Perron edge-record experiment; not yet identified with Book03 selected F_N, original 128 Kraus, CAR16 or physical GR."
},null,2));
