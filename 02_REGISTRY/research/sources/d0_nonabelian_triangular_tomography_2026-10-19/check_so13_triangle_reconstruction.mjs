#!/usr/bin/env node
// D0 research-only nonabelian K(9,11,13) gauge tomography.
// This is a finite algebraic SO(1,3) construction, NOT a native oldLEFT
// instrument, NOT a scene-to-four-Role physical compiler, NOT GR closure.
import assert from "node:assert/strict";

const D = 4, NA = 9, NB = 11, NC = 13, N = NA+NB+NC;
const mat0 = () => Array.from({length:D},()=>Array(D).fill(0));
const id = () => Array.from({length:D},(_,i)=>Array.from({length:D},(_,j)=> +(i===j)));
const unit = (i,j) => {const a=mat0();a[i][j]=1;return a;};
const plus = (a,b) => a.map((row,i)=>row.map((x,j)=>x+b[i][j]));
const times = (a,s) => a.map(row=>row.map(x=>x*s));
const multiply = (a,b) => a.map(row=>Array.from({length:D},(_,j)=>row.reduce((s,x,k)=>s+x*b[k][j],0)));
const transpose = a => a.map((_,i)=>a.map(row=>row[i]));
const delta = (a,b) => plus(a,times(b,-1));
const maxAbs = a => Math.max(...a.flat().map(Math.abs));
const eta = mat0(); eta[0][1]=eta[1][0]=1;eta[2][2]=eta[3][3]=-1;
// For exact Lorentz samples inverse = eta U^T eta.
const inverse = a => multiply(multiply(eta,transpose(a)),eta);
const nil = (i,j) => plus(unit(1,i),unit(i,0));
const opposite = (i,j) => plus(unit(0,i),unit(i,1));
const n2=nil(2),n3=nil(3),bn2=opposite(2),bn3=opposite(3);
const expNil = (A,t)=> plus(plus(id(),times(A,t)),times(multiply(A,A),t*t/2));
const generator=(u,v,kind) => {
  const alpha=.001*((13*u+7*v+3)%17-8);
  const beta=.001*((5*u+11*v+9)%19-9);
  const bases=kind===0?[n2,bn3]:kind===1?[n3,bn2]:[n2,bn2];
  return multiply(expNil(bases[0],alpha),expNil(bases[1],beta));
};
const graph = () => Array.from({length:N},()=>Array(N).fill(null));
const set=(g,u,v,m)=> {g[u][v]=m;g[v][u]=inverse(m);};
const part = u=>u<NA?0:u<NA+NB?1:2;
const g=graph();
// Reference spanning tree: a0--ALL B, a0--ALL C, b0--(A\a0).
for(let a=0;a<NA;a++)for(let b=NA;b<NA+NB;b++)set(g,a,b,a===0||b===NA?id():generator(a,b,2));
for(let a=0;a<NA;a++)for(let c=NA+NB;c<N;c++)set(g,a,c,a===0?id():generator(a,c,1));
for(let b=NA;b<NA+NB;b++)for(let c=NA+NB;c<N;c++)set(g,b,c,generator(b,c,0));

const face=(G,a,b,c) => multiply(multiply(G[a][b],G[b][c]),G[c][a]);
const frame=Array.from({length:N},(_,u)=>multiply(expNil(n2,.001*((u*7)%9-4)),expNil(bn3,.001*((u*11)%11-5))));
const gauge=graph();
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(part(u)!==part(v))
  gauge[u][v]=multiply(multiply(inverse(frame[u]),g[u][v]),frame[v]);
// Recover original reference tree gauge using ONLY its edges, no fitted curvature.
const R=Array(N).fill(null);R[0]=id();
for(let b=NA;b<NA+NB;b++)R[b]=multiply(inverse(gauge[0][b]),R[0]);
for(let c=NA+NB;c<N;c++)R[c]=multiply(inverse(gauge[0][c]),R[0]);
for(let a=1;a<NA;a++)R[a]=multiply(inverse(gauge[NA][a]),R[NA]);
const G=graph();
let treeResidual=0;
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(part(u)!==part(v))
  G[u][v]=multiply(multiply(inverse(R[u]),gauge[u][v]),R[v]);
for(let b=NA;b<NA+NB;b++) treeResidual=Math.max(treeResidual,maxAbs(delta(G[0][b],id())));
for(let c=NA+NB;c<N;c++) treeResidual=Math.max(treeResidual,maxAbs(delta(G[0][c],id())));
for(let a=1;a<NA;a++) treeResidual=Math.max(treeResidual,maxAbs(delta(G[NA][a],id())));
assert.ok(treeResidual<1e-11);

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

let edgeError=0, lorentzError=0, faceError=0, complementError=0, omitted=0;
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(part(u)!==part(v)) {
  edgeError=Math.max(edgeError,maxAbs(delta(G[u][v],Q[u][v])));
  lorentzError=Math.max(lorentzError,maxAbs(delta(multiply(multiply(transpose(G[u][v]),eta),G[u][v]),eta)));
}
for(let a=0;a<NA;a++)for(let b=NA;b<NA+NB;b++)for(let c=NA+NB;c<N;c++) {
  faceError=Math.max(faceError,maxAbs(delta(face(G,a,b,c),face(Q,a,b,c))));
  if(a===0||b===NA||c===NA+NB)continue;
  ++omitted;
  // Ordered 7-factor NONCOMMUTATIVE version of scalar triple contrast.
  const factors=[
    face(G,a,b,NA+NB),
    inverse(face(G,a,NA,NA+NB)),
    face(G,0,NA,NA+NB),
    inverse(face(G,0,b,NA+NB)),
    face(G,0,b,c),
    inverse(face(G,0,NA,c)),
    face(G,a,NA,c)
  ];
  const predicted=factors.reduce((acc,m)=>multiply(acc,m),id());
  complementError=Math.max(complementError,maxAbs(delta(face(G,a,b,c),predicted)));
}
assert.equal(omitted,960);
assert.ok(edgeError<1e-11 && faceError<1e-11 && complementError<1e-11 && lorentzError<1e-11);
const commutator=maxAbs(delta(multiply(G[NA][NA+NB],G[NA+1][NA+NB]),multiply(G[NA+1][NA+NB],G[NA][NA+NB])));
assert.ok(commutator>1e-8);
// Hostile independent omitted face cannot obey the seven-factor identity.
const badFace=multiply(face(G,1,NA+1,NA+NB+1),expNil(n2,.05));
const predicted=face(Q,1,NA+1,NA+NB+1);
const hostileError=maxAbs(delta(badFace,predicted));
assert.ok(hostileError>.01);
assert.equal(NA*NB+NA*NC+NB*NC,359);
assert.equal(NA*NB*NC,1287);
assert.equal(NB*NC+(NA-1)*NC+(NA-1)*(NB-1),327);
console.log(JSON.stringify({
 status:"PASS_SO13_NONABELIAN_327_TRIANGLE_TOMOGRAPHY_RESEARCH_ONLY",
 scene:[NA,NB,NC], vertices:N, undirected_edges:359, directed_edges:718,
 spanning_tree_edges:32, reference_faces:327, nonlinear_matrix_compatibilities:omitted,
 Lorentz_dim_per_reference_face:6,
 max_tree_gauge_error:treeResidual,max_Lorentz_error:lorentzError,
 max_edge_recovery_error:edgeError,max_full_face_error:faceError,
 max_seven_factor_error:complementError,noncommuting_order_signal:commutator,
 hostile_nonreference_face_error:hostileError,
 original_role_lattice_identification_proved:false,
 actual_physical_book_action_proved:false,
 GR_closed:false
},null,2));
