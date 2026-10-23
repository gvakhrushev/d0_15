#!/usr/bin/env node
"use strict";
// Original Golden full128 conditional nonblank port:
// exact score sufficiency but nonzero Cost-Info source, same actual instrument.
const p=(Math.sqrt(5)-1)/2,logphi=Math.log(1/p);
const assert=(x,name)=>{if(!x)throw Error("FAILED "+name);console.log("PASS",name)};
const near=(a,b,t=1e-12)=>Math.abs(a-b)<=t;
assert(near(p*p+p,1)&&near(p**3,2*p-1),"golden primitive normalization/code identity");
const r=[p*p,p],ref=[p,p*p];
const H=-r.reduce((s,x)=>s+x*Math.log(x)/logphi,0);
const C=r[0]+2*r[1];
const KL=r.reduce((s,x,i)=>s+x*Math.log(x/ref[i])/logphi,0);
assert(near(H,2-p)&&near(C,1+p)&&near(KL,p**3)&&near(C-H,KL),
"exact port conditional Shannon / primitive Cost / Info=p^3");
const q=[.65,.1,.15,.1],dq=[.007,-.013,.023,-.017];
assert(near(q.reduce((a,b)=>a+b,0),1)&&near(dq.reduce((a,b)=>a+b,0),0),
"actual tested reduced probability and source normalized");
const Q=[],dQ=[],Qrest=[];
for(let i=0;i<q.length;i++){
 if(i<2){Q.push(q[i]);dQ.push(dq[i]);Qrest.push(i);}
 else for(const w of r){Q.push(q[i]*w);dQ.push(dq[i]*w);Qrest.push(i);}
}
for(let i=0;i<Q.length;i++)assert(near(dQ[i]/Q[i],dq[Qrest[i]]/q[Qrest[i]]),
"full history score equals port-forgotten label score "+i);
const Ifull=Q.reduce((s,x,i)=>s+dQ[i]*dQ[i]/x,0);
const Ired=q.reduce((s,x,i)=>s+dq[i]*dq[i]/x,0);
assert(near(Ifull,Ired),"Fisher info exactly conserved by original port forgetting");
const dpnz=(-42957+14319*Math.sqrt(5))/5120000;
const codeJ23=p**3*dpnz;
const shannonJ23=(2-p)*dpnz;
assert(near(codeJ23,-0.0005043529002143444,1e-14),
"actual original J23 hidden-code source exact");
assert(near(shannonJ23,-0.0029525333048285245,1e-14),
"actual original J23 hidden-Shannon source exact");
const q0=(5034167+28557*Math.sqrt(5))/5120000, n=1024;
const e=1-q0;
const fisherRatio=n*e*q0**(n-1)/(1-q0**n);
assert(near(fisherRatio,0.05459555094710281,1e-13) && fisherRatio>0&&fisherRatio<1,
"OR count-Fisher strictly loses native field information on scalar shell");
console.log(JSON.stringify({type:"original full128 port/label, not k-Golden Slater",
portKL:KL,portFisherLoss:Ifull-Ired,
J23hiddenCodeSource:codeJ23,J23hiddenShannonSource:shannonJ23,
fisher_OR_over_EXIT_COUNT:fisherRatio,gr_closed:false},null,2));
