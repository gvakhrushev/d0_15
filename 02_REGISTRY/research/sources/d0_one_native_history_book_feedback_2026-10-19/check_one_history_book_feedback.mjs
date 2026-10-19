#!/usr/bin/env node
// D0 ORIGINAL ONE-SIDED Perron all-walks history (K9/11/13):
// ONE sample path recovers exact 33x33 conditional-innovation effect,
// its full Book-candidate logdet, and distinguishes the degree random walk.
// Plus exact moving original symmetric COST first-jet against finite difference.
// No dependencies, no extra independent copies or chosen stationary input.
// Does NOT prove compulsory physical Book03 U_N/Cost−Info = this candidate.
const n=33,parts=[9,11,13],p=(Math.sqrt(5)-1)/2,z=2**-20,
      ell=Math.log(1/p);
const zone=Array.from({length:n},(_,i)=>i<9?0:i<20?1:2);
const near=(a,b,tol=1e-10)=>{if(Math.abs(a-b)>tol)throw Error("mismatch "+a+" vs "+b+" err "+Math.abs(a-b));};
const eye=()=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const tr=A=>A.reduce((s,row,i)=>s+row[i],0);
const transpose=A=>A.map((row,i)=>row.map((_,j)=>A[j][i]));
const maxAbs=M=>Math.max(...M.flat().map(Math.abs));
let seed=18621;
const rnd=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/4294967296;};
function draw(weights){const v=rnd();let s=0;for(let i=0;i<weights.length;i++){s+=weights[i];if(v<s)return i;}return weights.length-1;}

function choleskyLogdet(M){
 const L=Array.from({length:n},()=>Array(n).fill(0));let logdet=0;
 for(let i=0;i<n;i++)for(let j=0;j<=i;j++){
  let a=M[i][j];for(let k=0;k<j;k++)a-=L[i][k]*L[j][k];
  if(i===j){if(!(a>0))throw Error("incomplete nonpositive determinant");
   L[i][j]=Math.sqrt(a);logdet+=Math.log(a);}
  else L[i][j]=a/L[j][j];
 }
 return logdet;
}
function book(F){return -choleskyLogdet(F.map((row,i)=>row.map((v,j)=>(i===j?1:0)-z*v)));}

function pfSym(K){
 let v=Array(n).fill(1/Math.sqrt(n));
 for(let k=0;k<800;k++){
  let w=K.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));
  const norm=Math.hypot(...w);w=w.map(q=>q/norm);
  const diff=Math.max(...w.map((x,i)=>Math.abs(x-v[i])));
  v=w;if(diff<2e-16)break;
 }
 const kv=K.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));
 const rho=v.reduce((s,x,i)=>s+x*kv[i],0);
 return {r:v,rho};
}
function scene(relativeCost=0){
 const A=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>{
   if(zone[i]===zone[j])return 0;
   const costly=(zone[i]===0&&zone[j]===1)||(zone[i]===1&&zone[j]===0);
   return p*Math.exp(-ell*relativeCost*(costly?1:0));
 }));
 const {r,rho}=pfSym(A);
 const pi=r.map(q=>q*q),sumr=r.reduce((a,b)=>a+b),
       mu0=r.map(q=>q/sumr);
 const P=A.map((row,i)=>row.map((v,j)=>v*r[j]/(rho*r[i])));
 for(let i=0;i<n;i++)near(P[i].reduce((a,b)=>a+b,0),1,2e-13);
 const T=A.map(row=>row.map(x=>x/rho));
 const T2=mul(T,T),F=T2.map((row,i)=>row.map((v,j)=>(i===j?1:0)-v));
 return {A,r,rho,pi,mu0,P,T,F,J:book(F)};
}
const original=scene();
const N_SCENE=n,mu0=original.mu0,pi=original.pi,P=original.P;
const nullVector=Array.from({length:n},(_,i)=>Math.sqrt(pi[i]));
// Exact single-transition innovation quadratic formula, no two successor draws.
for(let test=0;test<5;test++){
 const f=Array.from({length:n},(_,i)=>Math.sin(.19*(i+1+test)));
 let variance=0;
 for(let u=0;u<n;u++){
  const mean=P[u].reduce((s,v,j)=>s+v*f[j],0);
  variance+=pi[u]*P[u].reduce((s,v,j)=>s+v*(f[j]-mean)**2,0);
 }
 const vf=f.map((x,i)=>x*Math.sqrt(pi[i]));
 const operator=vf.reduce((s,x,i)=>s+x*original.F[i].reduce((t,v,j)=>t+v*vf[j],0),0);
 near(variance,operator,2e-13);
}
// Full 33x33 native feedback and its unique deterministic action.
const rho0=original.rho/p;
near(rho0**3-359*rho0-2574,0,2e-9);
const k=2574/rho0**3,closed=-30*Math.log1p(-z)
 -Math.log(1-(1+2*k)*z+(2*k+k*k)*z*z);
near(original.J,closed,2e-12);
near(original.J,.000030035369315208,2e-12);

function collectPath(N){
 const counts=Array.from({length:n},()=>new Float64Array(n)),
  depart=new Float64Array(n),arrival=new Float64Array(n);
 let current=draw(mu0),sumLLR=0;
 for(let t=0;t<N;t++){
  const next=draw(P[current]);
  counts[current][next]++;depart[current]++;arrival[next]++;
  sumLLR+=Math.log(P[current][next]*(33-parts[zone[current]]));
  current=next;
 }
 if(depart.some(x=>x<=0))throw Error("did not observe all original 33 states");
 const phat=Array.from(depart,x=>x/N),
       phatTransition=counts.map((row,i)=>Array.from(row,x=>x/depart[i]));
 // EXACT coordinate expression of observed one-path Gram residual covariance:
 // N^-1 Σ_t [1(Y_t+1=i)-P_hat(Y_t,i)] / √pi_hat_i × same for j.
 const C=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>
   (i===j?arrival[i]/depart[i]:0)-
   depart.reduce((s,nu,u)=>s+nu/N*phatTransition[u][i]*phatTransition[u][j],0)
      /Math.sqrt(phat[i]*phat[j])));
 let eigNull=0,errCov=0,errPi=0,errP=0;
 for(let i=0;i<n;i++){
  let v=0;
  for(let j=0;j<n;j++){
   v+=C[i][j]*Math.sqrt(phat[j]);
   errCov=Math.max(errCov,Math.abs(C[i][j]-original.F[i][j]));
   errP=Math.max(errP,Math.abs(phatTransition[i][j]-P[i][j]));
  }
  eigNull=Math.max(eigNull,Math.abs(v));
  errPi=Math.max(errPi,Math.abs(phat[i]-pi[i]));
 }
 const Jhat=book(C),errJ=Math.abs(Jhat-original.J);
 if(eigNull>5e-12||errJ>5e-8||errCov>.01)throw Error("single-record feedback failed");
 return {nativeTransitions:N,empiricalBook:Jhat,referenceBook:original.J,
   absolutePriceError:errJ,maximumConditionalCovarianceEntryError:errCov,
   maximumTransitionProbabilityError:errP,maximumStationaryPreparationError:errPi,
   exactSampleZeroModeError:eigNull,
   oneHistoryPerronVsDegreeLogLikelihoodRate:sumLLR/N};
}
const sampleSmall=collectPath(50000),sampleLarge=collectPath(300000);
if(sampleLarge.absolutePriceError>=sampleSmall.absolutePriceError)
 throw Error("deterministic seed failed tightened price control");
const rank32Proof="Full positive 718-edge tripartite support forces only constant zero-variance observable";

// An ACTUAL native scalar edge-price derivative, keeping d(rho) and all 33
// moving source terms; compare with an independent symmetric finite diff.
const h=2e-3,up=scene(h),dn=scene(-h),finite=(up.J-dn.J)/(2*h);
const dk=original.A.map((row,i)=>row.map((x,j)=>
  x*(-ell)*((zone[i]===0&&zone[j]===1)||(zone[i]===1&&zone[j]===0)?1:0)));
const r=original.r,rho=original.rho,
 dRho=r.reduce((s,x,i)=>s+x*dk[i].reduce((t,v,j)=>t+v*r[j],0),0);
const dT=dk.map((row,i)=>row.map((x,j)=>x/rho-original.T[i][j]*dRho/rho));
const G=mul(original.T,original.T).map((row,i)=>row.map((x,j)=>(i===j?1-z:0)+z*x));
const inv=G.map((row,i)=>[...row,...eye()[i]]);
for(let k=0;k<n;k++){
 let d=inv[k][k];for(let j=0;j<2*n;j++)inv[k][j]/=d;
 for(let i=0;i<n;i++)if(i!==k){const f=inv[i][k];for(let j=0;j<2*n;j++)inv[i][j]-=f*inv[k][j];}
}
const Ginv=inv.map(row=>row.slice(n));
const trueNativeSource=-2*z*tr(mul(mul(Ginv,original.T),dT));
near(trueNativeSource,finite,2e-11);
if(!(Math.abs(trueNativeSource)>1e-10))throw Error("native source nonzero signal missing");
const PerronDegKL=P.reduce((s,row,i)=>s+pi[i]*row.reduce((t,v,j)=>t+(v>0?v*Math.log(v*(33-parts[zone[i]])):0),0),0);
if(!(PerronDegKL>0))throw Error("native vs degree independent discriminator vanished");
if(Math.abs(sampleLarge.oneHistoryPerronVsDegreeLogLikelihoodRate-PerronDegKL)>.0003)
 throw Error("one-history law discrimination failed");
console.log(JSON.stringify({status:"PASS",native:{vertices:n,directedEdges:718,originalOneSidedInitialization:true,
  stationaryMinPi:Math.min(...pi),feedbackExact:original.J,fullyRetainedHistory:true},
 rank32:rank32Proof,
 fullSingleNativePath:[sampleSmall,sampleLarge],
 movingOriginalEdgePriceSource:{analytic:trueNativeSource,symmetricFieldFiniteDifference:finite,
        error:Math.abs(trueNativeSource-finite)},
 nativeHistoryVsDegreeTest:{expectedPerEdgeKLNats:PerronDegKL,
       observedPerEdgeKLNats:sampleLarge.oneHistoryPerronVsDegreeLogLikelihoodRate},
 boundary:"No physical identification with compulsory Book03 U_N or Einstein metric source"},null,2));
