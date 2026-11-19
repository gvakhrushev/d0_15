#!/usr/bin/env node
// Research-only: exact structural theorem is proved in the paired memo.
// This bounded numeric check is NOT a native physical detector or GR closure.
import assert from "node:assert/strict";

const N = 33, NA = 9, NB = 11, NC = 13;
const part = i => i < NA ? 0 : i < NA + NB ? 1 : 2;
const edges = [];
const triangles = [];
for (let u=0; u<N; u++) for (let v=u+1; v<N; v++)
  if (part(u)!==part(v)) edges.push([u,v]);
for (let a=0; a<NA; a++) for (let b=NA; b<NA+NB; b++)
  for (let c=NA+NB; c<N; c++) triangles.push([a,b,c]);
assert.equal(edges.length,359);
assert.equal(triangles.length,1287);
assert.equal(edges.length-N+1,327);
assert.equal((NA-1)*(NB-1)*(NC-1),960);
assert.equal(2*edges.length-N,685);

const zeros=()=>Array.from({length:N},()=>Array(N).fill(0));
const P=zeros();
for (let u=0;u<N;u++) {
  for(let v=0;v<N;v++)
    if(part(u)!==part(v)) P[u][v]=1+((7*u+11*v+13)%19)/37;
  const norm=P[u].reduce((a,b)=>a+b,0);
  for(let v=0;v<N;v++) P[u][v]/=norm;
}
const d=Array.from({length:N},(_,i)=>Math.exp(.2*Math.sin(i*.37)));
const K=P.map((row,u)=>row.map((x,v)=>x*d[v]/d[u]));
const scale=2.75;
const Ks=K.map(row=>row.map(x=>scale*x));

function perron(M) {
  let r=Array(N).fill(1),lambda=1;
  for (let iter=0;iter<500;iter++) {
    const nr=M.map(row=>row.reduce((s,x,j)=>s+x*r[j],0));
    lambda=nr.reduce((s,x)=>s+x,0)/r.reduce((s,x)=>s+x,0);
    r=nr.map(x=>x/lambda);
  }
  return {lambda,r};
}
function doob(M) {
  const {lambda,r}=perron(M);
  return {lambda,P:M.map((row,u)=>row.map((x,v)=>x*r[v]/(lambda*r[u])))};
}
const a=doob(K),b=doob(Ks);
const mxerr=(Q)=>Math.max(...Q.flatMap((row,u)=>row.map((x,v)=>Math.abs(x-P[u][v]))));
assert.ok(Math.abs(a.lambda-1)<1e-12);
assert.ok(Math.abs(b.lambda-scale)<1e-12);
assert.ok(mxerr(a.P)<1e-12 && mxerr(b.P)<1e-12);

const face=(M,[a,b,c])=>Math.log(M[a][b]*M[b][c]*M[c][a]/(M[a][c]*M[c][b]*M[b][a]));
const return2=(M,[u,v])=>M[u][v]*M[v][u];
let errB=0,errA=0;
for (const e of edges) errB=Math.max(errB,Math.abs(return2(K,e)-return2(P,e)));
for (const t of triangles) errA=Math.max(errA,Math.abs(face(K,t)-face(P,t)));
assert.ok(errB<1e-12 && errA<1e-12);

// Native additive directed-edge scalar price implies 960 mixed contrasts vanish.
function F(a,b,c) {
  return Math.log(K[a][b]/K[b][a])
       + Math.log(K[b][c]/K[c][b])
       + Math.log(K[c][a]/K[a][c]);
}
const aa=0,bb=NA,cc=NA+NB;
function triple(a,b,c, fn) {
  return fn(a,b,c)-fn(aa,b,c)-fn(a,bb,c)-fn(a,b,cc)
       +fn(aa,bb,c)+fn(aa,b,cc)+fn(a,bb,cc)-fn(aa,bb,cc);
}
let errT=0;
for (let i=1;i<NA;i++) for(let j=NA+1;j<NA+NB;j++)
  for(let k=NA+NB+1;k<N;k++) errT=Math.max(errT,Math.abs(triple(i,j,k,F)));
assert.ok(errT<1e-12);
function Fbroken(a,b,c) {return F(a,b,c)+(a===1&&b===NA+1&&c===NA+NB+1?1/7:0);}
assert.ok(Math.abs(triple(1,NA+1,NA+NB+1,Fbroken)-1/7)<1e-12);

// One absolute 2-edge BOOK weight recovers the global unobservable Perron scale.
const [u,v]=edges[0];
const lambdaFromOneAbsoluteReturn=Math.sqrt(return2(Ks,[u,v])/return2(P,[u,v]));
assert.ok(Math.abs(lambdaFromOneAbsoluteReturn-scale)<1e-12);
const hostile=P.map(row=>row.slice());
hostile[u][v]*=1.1;
const hn=hostile[u].reduce((x,y)=>x+y,0);
hostile[u]=hostile[u].map(x=>x/hn);
assert.ok(Math.abs(return2(hostile,[u,v])-return2(P,[u,v]))>1e-7);

console.log(JSON.stringify({
  status:"PASS_FINITE_MATHEMATICAL_TOMOGRAPHY_ONLY",
  nodes:N,undirected_edges:edges.length,directed_edges:edges.length*2,
  triangles:triangles.length,oriented_cycle_rank:edges.length-N+1,
  triple_contrast_compatibilities:(NA-1)*(NB-1)*(NC-1),
  stochastic_dimension:2*edges.length-N,
  two_cycle_plus_orientation:edges.length+(edges.length-N+1),
  one_nonlinear_pressure_compatibility:true,
  max_two_cycle_similarity_error:errB,
  max_triangle_similarity_error:errA,
  max_triple_compatibility_error:errT,
  max_recovered_probability_error:Math.max(mxerr(a.P),mxerr(b.P)),
  pressure_from_single_absolute_return:lambdaFromOneAbsoluteReturn,
  branch_selection_proved:false,
  native_Book_Born_identification_proved:false,
  GR_closed:false
},null,2));
