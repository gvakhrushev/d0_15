#!/usr/bin/env node
// Original fixed K9 root, actual 33-vertex K(9,11,13) finite suffix counts.
// All probabilities are exact integer ratios; angles are only displayed
// numerical illustrations of the proved square-root/Fisher identity.
const parts=[9n,11n,13n], n=33;
const zone=i=>i<9?0:i<20?1:2;
const edges=[];
for(let u=0;u<n;u++)for(let v=0;v<n;v++)
  if(zone(u)!==zone(v))edges.push([u,v]);
const assert=(ok,msg)=>{if(!ok)throw Error(msg);};
assert(edges.length===718,"actual original edges");
const gcd=(a,b)=>b===0n?a:gcd(b,a%b);
const frac=(a,b)=>{const g=gcd(a,b);return `${a/g}/${b/g}`;};
const rows=[];
let counts=[1n,1n,1n];
for(let horizon=1;horizon<=32;horizon++){
  const mass11=parts[1]*counts[1],mass13=parts[2]*counts[2];
  const total=mass11+mass13;
  const b=Number(mass11)/Number(total);
  const theta=Math.atan2(Math.sqrt(1-b),Math.sqrt(b));
  rows.push({horizon,mass11,total,b,theta,
    probabilityZone11:frac(mass11,total)});
  counts=parts.map((_,i)=>parts.reduce((s,size,j)=>
    s+(i===j?0n:size*counts[j]),0n));
}
let all=0,via11=0,via13=0;
const firstVertexCounts=Array(n).fill(0);
for(let v=0;v<n;v++)if(zone(v)!==zone(0))
for(let w=0;w<n;w++)if(zone(w)!==zone(v)){
  all++;firstVertexCounts[v]++;
  if(zone(v)===1)via11++;else via13++;
}
assert(all===502&&via11===242&&via13===260,"literal depth2 enumeration");
assert(firstVertexCounts.slice(9,20).every(x=>x===22),"K11 per-vertex");
assert(firstVertexCounts.slice(20).every(x=>x===20),"K13 per-vertex");
const [r1,r2,r3]=rows;
const less=(x,y)=>x.mass11*y.total<y.mass11*x.total;
assert(less(r1,r3)&&less(r3,r2),"exact horizon reversal");
assert(r2.theta<r3.theta&&r3.theta<r1.theta,"angle reversal");
// e11,e13 are fixed orthonormal normalized zone-indicator vectors.
// sqrt(Q_n)=sqrt(b_n)e11+sqrt(1-b_n)e13, exactly.
let planeResidual=0,normResidual=0;
for(const r of rows){
  const x=Array.from({length:24},(_,i)=>
    i<11?Math.sqrt(r.b/11):Math.sqrt((1-r.b)/13));
  const norm=x.reduce((s,v)=>s+v*v,0);
  normResidual=Math.max(normResidual,Math.abs(norm-1));
  for(let i=0;i<24;i++){
    const predicted=i<11?Math.cos(r.theta)/Math.sqrt(11):
      Math.sin(r.theta)/Math.sqrt(13);
    planeResidual=Math.max(planeResidual,Math.abs(x[i]-predicted));
  }
}
const sequentialLength=2*(Math.abs(r2.theta-r1.theta)+Math.abs(r3.theta-r2.theta));
const endpointDistance=2*Math.abs(r3.theta-r1.theta);
assert(sequentialLength>endpointDistance,"chronological horizon path is not minimizing");
assert(planeResidual<1e-14&&normResidual<1e-14,"square-root embedding");
console.log(JSON.stringify({
  status:"PASS",originalVertices:33,originalDirectedEdges:718,
  completeDepth2Paths:all,equalPathCost:2,equalPathProbability:"1/502",
  nextZoneMass:{K11:"242/502",K13:"260/502"},
  eachNextVertexMass:{K11:"22/502",K13:"20/502"},
  exactFirstThreeZone11Probabilities:rows.slice(0,3).map(r=>r.probabilityZone11),
  exactInequality:"11/24 < 2618/5595 < 121/251",
  progression:rows.filter(r=>[1,2,3,4,5,6,8,16,32].includes(r.horizon))
    .map(({horizon,probabilityZone11,b,theta})=>({horizon,probabilityZone11,b,theta})),
  squareRootPlaneResidual:planeResidual,squareRootNormResidual:normResidual,
  fisherLengthHorizon1to2to3:sequentialLength,
  fisherDistanceHorizon1to3:endpointDistance,
  excess:sequentialLength-endpointDistance,
  scope:"Image lies in a Fisher great circle by two-zone symmetry; ordered horizon progression reverses and is not a minimizing geodesic. Neither fact selects an individual history."
},null,2));
