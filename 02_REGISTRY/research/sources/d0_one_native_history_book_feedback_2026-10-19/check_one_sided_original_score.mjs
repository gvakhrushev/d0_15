#!/usr/bin/env node
// Direct ORIGINAL D0 K(9,11,13) ONE-SIDED Perron history Cost−Info first-source.
// Exhaustive ALL 15,708 original length-2 recorded paths, no artificial
// independent copies, no stationary reset, no dropped failure/endpoints.
// This is a genuine finite path-likelihood-score theorem, NOT the theorem
// that compulsory physical D0 Book03 action equals this statistical readout.
const n=33,parts=[9,11,13],phi=(1+Math.sqrt(5))/2,p=1/phi,
      ell=Math.log(phi),zone=Array.from({length:n},(_,i)=>i<9?0:i<20?1:2);
const near=(a,b,tol=1e-9)=>{if(Math.abs(a-b)>tol)throw Error(a+" versus "+b)};
function scene(t){
 const K=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>
   zone[i]===zone[j]?0:p*Math.exp(-ell*t*
   (+((zone[i]===0&&zone[j]===1)||(zone[i]===1&&zone[j]===0))))));
 let r=Array(n).fill(1/n),rho=0;
 for(let step=0;step<1000;step++){
  const next=K.map(row=>row.reduce((v,a,j)=>v+a*r[j],0)),mass=next.reduce((a,b)=>a+b);
  const normalized=next.map(x=>x/mass);
  const gap=Math.max(...normalized.map((v,j)=>Math.abs(v-r[j])));
  r=normalized;rho=mass;if(gap<1e-16)break;
 }
 near(r.reduce((a,b)=>a+b),1,1e-12);
 const P=K.map((row,i)=>row.map((a,j)=>a*r[j]/(rho*r[i])));
 return {K,r,rho,P};
}
const h=1e-4,base=scene(0),up=scene(h),down=scene(-h);
const f=Array.from({length:n},(_,i)=>Math.sin(.3*i)+.2*Math.cos(.17*i));
const forecast=base.P.map(row=>row.reduce((s,a,j)=>s+a*f[j],0));
const dLogRho=(Math.log(up.rho)-Math.log(down.rho))/(2*h);
const dLogTerminal=base.r.map((_,i)=>(Math.log(up.r[i])-Math.log(down.r[i]))/(2*h));
const W=(s,u,v,w)=>s.K[u][v]*s.K[v][w]*s.r[w]/(s.rho*s.rho);
let count=0,normal=0,scoreTotal=0,mean=0,scoreSource=0,plus=0,minus=0;
for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(zone[u]!==zone[v])
for(let w=0;w<n;w++)if(zone[v]!==zone[w]){
 const n9_11=+((zone[u]===0&&zone[v]===1)||(zone[u]===1&&zone[v]===0))
             + +((zone[v]===0&&zone[w]===1)||(zone[v]===1&&zone[w]===0));
 const score=-ell*n9_11-2*dLogRho+dLogTerminal[w];
 const observable=(f[w]-forecast[v])**2;
 const prob=W(base,u,v,w);
 count++;normal+=prob;scoreTotal+=prob*score;mean+=prob*observable;
 scoreSource+=prob*observable*score;
 plus+=W(up,u,v,w)*observable;minus+=W(down,u,v,w)*observable;
}
near(count,15708,0);near(normal,1,2e-9);
if(Math.abs(scoreTotal)>2e-9)throw Error("full history score mean nonzero");
const derivative=(plus-minus)/(2*h);
near(scoreSource,derivative,2e-8);
if(Math.abs(scoreSource)<.01)throw Error("genuine Book price source vanished");
// A complete native Book Cost price with true terminal Perron trace is
// normalized at EVERY field value, not just at the base.
const normalization=s=>{let mass=0;for(let u=0;u<n;u++)for(let v=0;v<n;v++)
 if(zone[u]!==zone[v])for(let w=0;w<n;w++)
 if(zone[v]!==zone[w])mass+=W(s,u,v,w);return mass;};
near(normalization(up),1,1e-9);near(normalization(down),1,1e-9);
console.log(JSON.stringify({
 status:"PASS",realOriginalVertices:n,originalDirectedEdges:718,
 completeOriginalDepth2Histories:count,
 trueNativeOneSidedNormalization:normal,
 genuineBaselineDistinctionLossMean:mean,
 firstSourceByFullRecordedCostInfoScore:scoreSource,
 firstSourceByIndependentWholeHistoryFieldPerturbation:derivative,
 sourceAbsoluteDifference:Math.abs(scoreSource-derivative),
 totalHistoryScoreMean:scoreTotal,
 scope:"Original one-sided Perron full-path first source, not selected Book03 physical Einstein action"
},null,2));
