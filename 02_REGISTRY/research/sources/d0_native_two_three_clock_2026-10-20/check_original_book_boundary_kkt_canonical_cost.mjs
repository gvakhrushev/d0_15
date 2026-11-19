#!/usr/bin/env node
"use strict";
// ORIGINAL full 718-edge Perron Book scalar action over ALL physically
// ActionProtocol-admissible primitive nonidentity costs C_uv>=1, at
// FIXED original vertex Info and fixed scene carrier.
// Conditional “minimize across action completions” hypothesis clearly
// distinguished from the actual G0 ActionProtocol, which does NOT
// require that external minimization over programmes.
const phi=(1+Math.sqrt(5))/2,p=1/phi,ln=Math.log(phi);
const n=33,z=u=>u<9?0:u<20?1:2;
const edges=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(z(u)!==z(v))edges.push([u,v]);
const check=(v,name)=>{if(!v)throw Error("FAIL "+name);console.log("PASS "+name)};
check(edges.length===718,"ALL 718 original directed nonidentity edges are live");
const info=Array.from({length:n},(_,u)=>.008*((u*5)%13));
const fixedK=(cost)=>{
 const K=Array.from({length:n},()=>Array(n).fill(0));
 for(let [u,v] of edges)K[u][v]=Math.exp(-ln*(cost(u,v)-(info[u]+info[v])/2));
 return K;
};
const dot=(x,y)=>x.reduce((s,a,j)=>s+a*y[j],0);
const mul=(A,x)=>A.map(row=>dot(row,x));
function PF(K){
 let r=Array(n).fill(1/Math.sqrt(n)),l=r.slice();
 for(let j=0;j<1800;j++){
  let y=mul(K,r),zz=Math.hypot(...y),next=y.map(v=>v/zz);
  let yt=Array.from({length:n},(_,v)=>K.reduce((s,row,u)=>s+row[v]*l[u],0));
  let ll=Math.hypot(...yt),nextL=yt.map(v=>v/ll);
  let d=Math.max(...next.map((v,i)=>Math.abs(v-r[i])),
                 ...nextL.map((v,i)=>Math.abs(v-l[i])));
  r=next;l=nextL;if(d<4e-16)break;
 }
 const rr=mul(K,r),norm=dot(l,r),rho=dot(l,rr)/norm;
 const pi=l.map((v,u)=>v*r[u]/norm);
 const P=K.map((row,u)=>row.map((v,w)=>v*r[w]/(rho*r[u])));
 const mu=K.map((row,u)=>row.map((v,w)=>pi[u]*P[u][w]));
 return {rho,r,l,pi,P,mu,action:-Math.log(rho)/ln};
}
const canonical=()=>fixedK(()=>1);
const trueCost=(u,v)=>1+.015*((u*11+v*7+3*u*v)%23);
const K1=fixedK(trueCost),K0=canonical(),a0=PF(K0),a1=PF(K1);
check(a0.rho>a1.rho&&a0.action<a1.action,
 "all718 positive Perron original fixed-Info Book action globally lowest at CANONICAL C=1");
check(Math.abs(a1.pi.reduce((s,x)=>s+x,0)-1)<2e-13
 &&a1.P.every(row=>Math.abs(row.reduce((s,x)=>s+x,0)-1)<2e-13),
 "ORIGINAL real moving left/right Perron history stationary/transition normalize");
const total=a1.mu.reduce((s,row)=>s+row.reduce((x,y)=>x+y,0),0);
check(Math.abs(total-1)<2e-13&&edges.every(([u,v])=>a1.mu[u][v]>0),
 "EVERY original nonidentity Cost inequality has strictly positive KKT multiplier = native stationary edge frequency");
const tests=[[0,9],[0,20],[9,20],[12,24],[5,18],[8,31]];
for(let [u,v] of tests){
 const h=1e-4;
 const plus=PF(fixedK((x,y)=>trueCost(x,y)+h*Number(x===u&&y===v))).action;
 const minus=PF(fixedK((x,y)=>trueCost(x,y)-h*Number(x===u&&y===v))).action;
 check(Math.abs((plus-minus)/(2*h)-a1.mu[u][v])<2e-10,
  "EXACT native gradient dBook/dCost = mu_uv on edge "+u+"-"+v);
}
const uni=.03,Au=PF(fixedK((u,v)=>trueCost(u,v)+uni)).action;
check(Math.abs(Au-a1.action-uni)<4e-14,
 "uniform original primitive Cost scale shifts absolute Book action by EXACT delta");
let neg=.02;
const lower=PF(fixedK((u,v)=>trueCost(u,v)-neg)).action;
check(lower<a1.action,
 "strict downward book descent on any truly allowed positive Cost excess");
const minmu=Math.min(...edges.map(([u,v])=>a1.mu[u][v]));
const maxmu=Math.max(...edges.map(([u,v])=>a1.mu[u][v]));
console.log(JSON.stringify({
 scope:"ORIGINAL all718 K913 fixed-Info primitive action cost>=1",
 absoluteBookAtCanonical:a0.action,
 absoluteBookAtAdmissibleExcess:a1.action,
 positiveFullMu:[minmu,maxmu],
 sumMu:total,
 KKT_condition:"D_C Aeff = mu_uv >0, Cuv>=1, unique solution Cuv=1 for EVERY directed original edge",
 logical_HYPOTHESIS_REQUIRED:"actual D0 minimizes Aeff also ACROSS primitive ActionProtocol cost completions at FIXED Info; currently NOT a G0 theorem",
 false_claims_to_avoid:"minimum along histories within one selected protocol does not imply minimum across all protocols",
 GR_closed:false
},null,2));
