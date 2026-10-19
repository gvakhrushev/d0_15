#!/usr/bin/env node
// Exact rational SO(1,3) nonabelian K(9,11,13) triangle tomography.
// This is a finite algebraic construction, NOT a native oldLEFT instrument,
// NOT a scene-to-four-Role physical compiler, and NOT GR closure.
import assert from "node:assert/strict";

const D=4,NA=9,NB=11,NC=13,N=NA+NB+NC;
const abs=x=>x<0n?-x:x;
const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b){const r=a%b;a=b;b=r;}return a||1n;};
const R=(n,d=1n)=>{
  n=BigInt(n);d=BigInt(d);assert.notEqual(d,0n);
  if(d<0n){n=-n;d=-d;}
  const g=gcd(n,d);return {n:n/g,d:d/g};
};
const add=(a,b)=>R(a.n*b.d+b.n*a.d,a.d*b.d);
const neg=a=>R(-a.n,a.d);
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>R(a.n*b.n,a.d*b.d);
const div=(a,b)=>{assert.notEqual(b.n,0n);return R(a.n*b.d,a.d*b.n);};
const ZERO=R(0n),ONE=R(1n),HALF=R(1n,2n);
const mat0=()=>Array.from({length:D},()=>Array(D).fill(ZERO));
const id=()=>Array.from({length:D},(_,i)=>Array.from({length:D},(_,j)=>i===j?ONE:ZERO));
const unit=(i,j)=>{const a=mat0();a[i][j]=ONE;return a;};
const plus=(a,b)=>a.map((row,i)=>row.map((x,j)=>add(x,b[i][j])));
const times=(a,s)=>a.map(row=>row.map(x=>mul(x,s)));
const multiply=(a,b)=>a.map(row=>Array.from({length:D},(_,j)=>row.reduce((s,x,k)=>add(s,mul(x,b[k][j])),ZERO)));
const transpose=a=>a[0].map((_,j)=>a.map(row=>row[j]));
function subtractMatrices(a,b){return a.map((row,i)=>row.map((x,j)=>sub(x,b[i][j])));}
const equal=(a,b)=>a.length===b.length&&a.every((row,i)=>row.every((x,j)=>x.n===b[i][j].n&&x.d===b[i][j].d));
const isZero=a=>a.flat().every(x=>x.n===0n);
const rationalText=x=>`${x.n}/${x.d}`;
const firstNonzeroEntry=a=>{
  for(let i=0;i<a.length;i++)for(let j=0;j<a[i].length;j++)if(a[i][j].n!==0n)
    return {row:i,column:j,value:rationalText(a[i][j])};
  return null;
};
const exactRank=input=>{
  const a=input.map(row=>row.slice());
  let rank=0;
  for(let col=0;col<a[0].length&&rank<a.length;col++){
    let pivot=rank;
    while(pivot<a.length&&a[pivot][col].n===0n)pivot++;
    if(pivot===a.length)continue;
    [a[rank],a[pivot]]=[a[pivot],a[rank]];
    const p=a[rank][col];
    a[rank]=a[rank].map(x=>div(x,p));
    for(let row=0;row<a.length;row++)if(row!==rank&&a[row][col].n!==0n){
      const q=a[row][col];
      a[row]=a[row].map((x,j)=>sub(x,mul(q,a[rank][j])));
    }
    rank++;
  }
  return rank;
};
const determinant=a=>{
  let result=ZERO;
  const visit=(row,unused,permutation,sign)=>{
    if(row===D){
      const term=permutation.reduce((p,col,i)=>mul(p,a[i][col]),ONE);
      result=add(result,sign===1?term:neg(term));
      return;
    }
    for(const col of unused){
      const inversions=unused.filter(other=>other<col).length;
      visit(row+1,unused.filter(other=>other!==col),[...permutation,col],inversions%2?-sign:sign);
    }
  };
  visit(0,Array.from({length:D},(_,i)=>i),[],1);
  return result;
};
const eta=mat0();eta[0][1]=eta[1][0]=ONE;eta[2][2]=eta[3][3]=R(-1n);
// For exact Lorentz samples inverse = eta U^T eta.
const inverse=a=>multiply(multiply(eta,transpose(a)),eta);
const nil=i=>plus(unit(1,i),unit(i,0));
const opposite=i=>plus(unit(0,i),unit(i,1));
const n2=nil(2),n3=nil(3),bn2=opposite(2),bn3=opposite(3);
const commutator=(a,b)=>subtractMatrices(multiply(a,b),multiply(b,a));
const B=plus(unit(1,1),times(unit(0,0),R(-1n)));
const J=plus(unit(2,3),times(unit(3,2),R(-1n)));
assert.ok(equal(commutator(n2,bn2),B));
assert.ok(equal(commutator(n3,bn3),B));
assert.ok(equal(commutator(n2,bn3),J));
assert.ok(equal(commutator(n3,bn2),times(J,R(-1n))));
const lorentzBasis=[n2,n3,bn2,bn3,B,J];
assert.equal(exactRank(Array.from({length:16},(_,i)=>lorentzBasis.map(M=>M.flat()[i]))),6);
const expNil=(A,t)=>plus(plus(id(),times(A,t)),times(multiply(A,A),mul(mul(t,t),HALF)));
const generator=(u,v,kind)=>{
  const alpha=R(BigInt((13*u+7*v+3)%17-8),1000n);
  const beta=R(BigInt((5*u+11*v+9)%19-9),1000n);
  const bases=kind===0?[n2,bn3]:kind===1?[n3,bn2]:[n2,bn2];
  return multiply(expNil(bases[0],alpha),expNil(bases[1],beta));
};
const graph=()=>Array.from({length:N},()=>Array(N).fill(null));
const set=(g,u,v,m)=>{g[u][v]=m;g[v][u]=inverse(m);};
const part=u=>u<NA?0:u<NA+NB?1:2;
const g=graph();
// Reference spanning tree: a0--ALL B, a0--ALL C, b0--(A\a0).
for(let a=0;a<NA;a++)for(let b=NA;b<NA+NB;b++)set(g,a,b,a===0||b===NA?id():generator(a,b,2));
for(let a=0;a<NA;a++)for(let c=NA+NB;c<N;c++)set(g,a,c,a===0?id():generator(a,c,1));
for(let b=0;b<NB;b++)for(let c=NA+NB;c<N;c++)set(g,NA+b,c,generator(NA+b,c,0));
const face=(G,a,b,c)=>multiply(multiply(G[a][b],G[b][c]),G[c][a]);
const sevenFactorPrediction=(G,a,b,c)=>{
  const s=NA,t=NA+NB;
  return [
    face(G,a,b,t),
    inverse(face(G,a,s,t)),
    face(G,0,s,t),
    inverse(face(G,0,b,t)),
    face(G,0,b,c),
    inverse(face(G,0,s,c)),
    face(G,a,s,c)
  ].reduce((acc,m)=>multiply(acc,m),id());
};
const frame=Array.from({length:N},(_,u)=>multiply(expNil(n2,R(BigInt((u*7)%9-4),1000n)),expNil(bn3,R(BigInt((u*11)%11-5),1000n))));
const gauge=graph();
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(part(u)!==part(v))
  gauge[u][v]=multiply(multiply(inverse(frame[u]),g[u][v]),frame[v]);
// Recover original reference-tree gauge using ONLY its edges, no fitted curvature.
const Rtree=Array(N).fill(null);Rtree[0]=id();
for(let b=NA;b<NA+NB;b++)Rtree[b]=multiply(inverse(gauge[0][b]),Rtree[0]);
for(let c=NA+NB;c<N;c++)Rtree[c]=multiply(inverse(gauge[0][c]),Rtree[0]);
for(let a=1;a<NA;a++)Rtree[a]=multiply(inverse(gauge[NA][a]),Rtree[NA]);
const G=graph();
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(part(u)!==part(v))
  G[u][v]=multiply(multiply(inverse(Rtree[u]),gauge[u][v]),Rtree[v]);
for(let b=NA;b<NA+NB;b++)assert.ok(equal(G[0][b],id()));
for(let c=NA+NB;c<N;c++)assert.ok(equal(G[0][c],id()));
for(let a=1;a<NA;a++)assert.ok(equal(G[NA][a],id()));

const Q=graph();
// Reconstruction from THREE families of oriented triangle matrices,
// exactly 143 + 104 + 80 = 327 independent chords.
for(let b=NA;b<NA+NB;b++)set(Q,0,b,id());
for(let c=NA+NB;c<N;c++)set(Q,0,c,id());
for(let a=1;a<NA;a++)set(Q,NA,a,id());
for(let b=NA;b<NA+NB;b++)for(let c=NA+NB;c<N;c++)
  set(Q,b,c,face(G,0,b,c));
for(let a=1;a<NA;a++)for(let c=NA+NB;c<N;c++)
  set(Q,a,c,multiply(inverse(face(G,a,NA,c)),Q[NA][c]));
for(let a=1;a<NA;a++)for(let b=NA+1;b<NA+NB;b++)
  set(Q,a,b,multiply(multiply(face(G,a,b,NA+NB),Q[a][NA+NB]),inverse(Q[b][NA+NB])));

let edgeMismatches=0,lorentzViolations=0,propernessViolations=0,faceMismatches=0,complementMismatches=0,omitted=0;
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(part(u)!==part(v)){
  if(!equal(G[u][v],Q[u][v]))edgeMismatches++;
  if(!equal(multiply(multiply(transpose(G[u][v]),eta),G[u][v]),eta))lorentzViolations++;
  const det=determinant(G[u][v]);
  if(det.n!==det.d)propernessViolations++;
}
for(let a=0;a<NA;a++)for(let b=NA;b<NA+NB;b++)for(let c=NA+NB;c<N;c++){
  if(!equal(face(G,a,b,c),face(Q,a,b,c)))faceMismatches++;
  if(a===0||b===NA||c===NA+NB)continue;
  omitted++;
  // Ordered seven-factor noncommutative complement identity.
  const predicted=sevenFactorPrediction(G,a,b,c);
  if(!equal(face(G,a,b,c),predicted))complementMismatches++;
}
assert.equal(edgeMismatches,0);
assert.equal(lorentzViolations,0);
assert.equal(propernessViolations,0);
assert.equal(faceMismatches,0);
assert.equal(complementMismatches,0);
assert.equal(omitted,960);
const orderDifference=subtractMatrices(
  multiply(G[NA][NA+NB],G[NA+1][NA+NB]),
  multiply(G[NA+1][NA+NB],G[NA][NA+NB]));
assert.ok(!isZero(orderDifference));
// Hostile independent omitted face cannot obey the seven-factor identity.
const hostileTriple=[1,NA+1,NA+NB+1];
const badFace=multiply(face(G,...hostileTriple),expNil(n2,R(1n,20n)));
const predictedHostile=sevenFactorPrediction(G,...hostileTriple);
const hostileDifference=subtractMatrices(badFace,predictedHostile);
assert.ok(!isZero(hostileDifference));
assert.equal(NA*NB+NA*NC+NB*NC,359);
assert.equal(NA*NB*NC,1287);
assert.equal(NB*NC+(NA-1)*NC+(NA-1)*(NB-1),327);
console.log(JSON.stringify({
  status:"PASS_EXACT_RATIONAL_SO13_NONABELIAN_327_TRIANGLE_TOMOGRAPHY_RESEARCH_ONLY",
  arithmetic:"reduced BigInt rationals; no floating-point operations",
  scene:[NA,NB,NC],vertices:N,undirectedEdges:359,directedEdges:718,
  spanningTreeEdges:32,referenceTriangleMatrices:327,nonreferenceTriangleIdentities:omitted,
  LorentzDimensionPerReferenceFace:6,
  exactOppositeNullCommutators:true,
  exactLorentzBasisRank:6,
  exactTreeGaugeRecovery:true,exactEdgeRecovery:true,exactLorentzPreservation:true,
  exactProperLorentzDeterminants:true,exactAllFaceRecovery:true,exactSevenFactorComplement:true,
  noncommutingOrderWitness:firstNonzeroEntry(orderDifference),
  hostileIndependentFaceWitness:firstNonzeroEntry(hostileDifference),
  originalRoleLatticeIdentificationProved:false,
  actualPhysicalBookActionProved:false,
  GRclosed:false
},null,2));
