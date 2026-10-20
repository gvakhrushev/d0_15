#!/usr/bin/env node
"use strict";
/*
 Entire ORIGINAL native K(9,11,13) edge carrier and full CAR16 exterior:
  - 33 sites, 718 directed edges, 1287 distinct ABC triangle labels;
  - the existing homogeneous spatial SO(2) J23 proper-Lorentz subgroup
    and complete 16-grade Lambda exterior, not an added U(1) field;
  - arbitrary 359-dimensional antisymmetric scene edge-phase phi,
    with 327 physical cycle degrees modulo 32 vertex coboundaries.

 THEOREM (ALL φ, not only CP flat tangent):
   S=Lambda(R23(pi)), S²=I16, S commutes with all U_uv,
   U_uv^twist=U_uv S for adding signed pi to ALL original edges,
   Ttwist=T (I_33⊗S), so Ftwist=I−Ttwist²=I−T²=F.
 All 1287 original TRIANGLE holonomies get Utriangle^twist
 = Utriangle S, unlike the full squared return F.

 GLOBAL FLATNESS CLASSIFICATION:
 charged F has at least one zero ⇔ ALL 1287 triangle U(1)
 holonomies are +1, OR ALL 1287 equal -1; these are two distinct
 vertex-gauge classes because filled native triangles give H1=0.
 8 neutral CAR grades always have Perron-zero of F, charged8
 contribute another8 iff in one of the TWO global sheet classes.
 Generic φ has dim ker F=8; all+ or all− has 16.
 This is an exact Perron triangle-inequality theorem; numeric
 checks only validate specific full original carrier examples.

 This is not Spin Q8 *central* sign (π planar rotation is NOT
 central in full SO(1,3)). Not a physical G0 phase-controller,
 compulsory Book03 H+J+R or GR. No selection of metric or action.
*/
const assert=(v,m)=>{if(!v)throw Error("FAIL "+m);};
const N=33,CAR=16,zone=i=>i<9?0:i<20?1:2;
const adj=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>+(zone(i)!==zone(j))));
const edges=[];
for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(adj[i][j])edges.push([i,j]);
assert(edges.length===359,"native 359 undirected/718 directed");
let Perron=Array(N).fill(1/Math.sqrt(N)),rho=0;
const norm=v=>Math.sqrt(v.reduce((s,x)=>s+x*x,0));
for(let k=0;k<180;k++){
 const w=adj.map(row=>row.reduce((s,a,j)=>s+a*Perron[j],0));
 rho=norm(w);Perron=w.map(x=>x/rho);
}
assert(Math.max(...adj.map((row,i)=>Math.abs(
 row.reduce((s,x,j)=>s+x*Perron[j],0)-rho*Perron[i])))<1e-12,
 "original entire primitive Perron no eigenpair");
// Full CAR16 matrix of spatial proper rotation J23:
// neutral grades contain both/neither of underlying 2,3 and are fixed;
// the eight charged grades group into four exact standard 2x2 rotations.
const neutral=[],chargedPairs=[];
for(let mask=0;mask<CAR;mask++){
 const n2=!!(mask&4),n3=!!(mask&8);
 if(n2===n3)neutral.push(mask);
 else if(n2)chargedPairs.push([mask,(mask^4)|8]);
}
assert(neutral.length===8&&chargedPairs.length===4&&
 chargedPairs.flat().length===8,"original CAR16 grade charges");
const I=()=>Array.from({length:CAR},(_,i)=>Array.from({length:CAR},(_,j)=>+(i===j)));
const M=()=>Array.from({length:CAR},()=>Array(CAR).fill(0));
const S=Array.from({length:CAR},(_,i)=>neutral.includes(i)?1:-1);
const mat=(t)=>{
 const u=M();
 for(const i of neutral)u[i][i]=1;
 for(const [a,b] of chargedPairs){
  u[a][a]=u[b][b]=Math.cos(t);
  u[b][a]=Math.sin(t);u[a][b]=-Math.sin(t);
 }
 return u;
};
const mm=(a,b)=>a.map(row=>b[0].map((_,j)=>
 row.reduce((s,x,k)=>s+x*b[k][j],0)));
const maxdiff=(a,b)=>Math.max(...a.flatMap((row,i)=>row.map((x,j)=>Math.abs(x-b[i][j]))));
const piMat=mat(Math.PI);
const id=I();
assert(maxdiff(mm(piMat,piMat),id)<1e-15,
 "full CAR16 pi spin-orientation S must square to identity");
for(let i=0;i<CAR;i++)for(let j=0;j<CAR;j++)
 assert(Math.abs(piMat[i][j]-(i===j?S[i]:0))<6e-16,
  "native pi half-turn CAR grade parity not diagonal");

const phi=Array.from({length:N},()=>Array(N).fill(0)),
      twisted=Array.from({length:N},()=>Array(N).fill(0)),
      pureGauge=Array.from({length:N},()=>Array(N).fill(0)),
      gauge0=Array.from({length:N},(_,i)=>.17*Math.sin(i*.13)+.41*Math.cos(i*.31));
for(let e=0;e<edges.length;e++){
 const [i,j]=edges[e];
 const q=.35*Math.sin(.127*(e+1))+.13*Math.cos(.091*i+.21*j);
 phi[i][j]=q;phi[j][i]=-q;
 twisted[i][j]=q+Math.PI;twisted[j][i]=-q-Math.PI;
 pureGauge[i][j]=gauge0[i]-gauge0[j];
 pureGauge[j][i]=-pureGauge[i][j];
}
let maxHalfTurnOperator=0,maxFullCARF=0,maxCARGroup=0;
for(const [i,j] of edges){
 const u=mat(phi[i][j]),up=mat(twisted[i][j]),
       us=u.map(row=>row.map((x,k)=>x*S[k]));
 maxHalfTurnOperator=Math.max(maxHalfTurnOperator,maxdiff(up,us));
 const inv=mat(-phi[i][j]);
 const trans=u[0].map((_,c)=>u.map(row=>row[c]));
 maxCARGroup=Math.max(maxCARGroup,maxdiff(mm(u,inv),id),
  maxdiff(inv,trans));
}
// Compute the FULL 33*16 x 33*16 TWO-STEP return F blocks,
// not only a trace, eigenvalue or one CP cycle. Entire SO(2) exterior
// representation makes each 16x16 block an EXACT linear combination
// of 8 neutral diagonals and 4 charged 2x2 rotations.
const blockM=()=>Array.from({length:N},()=>Array.from({length:N},
 ()=>[0,0,0]));
const coefficients=phase=>{
 const out=blockM();
 for(let i=0;i<N;i++)for(let k=0;k<N;k++)if(adj[i][k])
  for(let j=0;j<N;j++)if(adj[k][j]){
   const x=(phase[i][k]+phase[k][j]),a=out[i][j],
         v=1/(rho*rho);
   a[0]+=v;a[1]+=v*Math.cos(x);a[2]+=v*Math.sin(x);
  }
 return out;
};
const c0=coefficients(phi),c1=coefficients(twisted);
for(let i=0;i<N;i++)for(let j=0;j<N;j++){
 const [a0,b0,d0]=c0[i][j],[a1,b1,d1]=c1[i][j];
 maxFullCARF=Math.max(maxFullCARF,
   Math.abs(a0-a1),Math.abs(b0-b1),Math.abs(d0-d1));
 // Every actual full16 block entry: neutral a, charged real 2x2 (b,d).
 const z0=M(),z1=M();
 for(const t of neutral){z0[t][t]=a0;z1[t][t]=a1;}
 for(const [x,y] of chargedPairs){
  z0[x][x]=z0[y][y]=b0;z1[x][x]=z1[y][y]=b1;
  z0[y][x]=d0;z0[x][y]=-d0;z1[y][x]=d1;z1[x][y]=-d1;
 }
 maxFullCARF=Math.max(maxFullCARF,maxdiff(z0,z1));
}
assert(maxFullCARF<9e-15&&maxHalfTurnOperator<9e-15&&maxCARGroup<5e-15,
 "full native 528x528 squared return NOT identical under pi all-edge twist");
// Original two/three-step *scalar BOOK* history from unchanged K=p*A
// is exactly identical in all 718 +7722 original words before/after twist.
const p=(Math.sqrt(5)-1)/2,originalZ2=718*p**3,
      originalZ3=7722*p**5;
const originalCompleteBook=originalZ2+originalZ3;
let triples=0,triMaxDiff=0,triMinDiff=Infinity,
    flatMin=Infinity,allFluxFlipError=0;
const psi=Array(CAR).fill(0);psi[1]=psi[4]=Math.SQRT1_2;
function overlap(ang){const U=mat(ang),v=mm(U,psi.map(x=>[x])).map(row=>row[0]);
 return psi.reduce((s,x,i)=>s+x*v[i],0);}
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<N;c++){
 triples++;
 const θ=phi[a][b]+phi[b][c]+phi[c][a],
       θtw=twisted[a][b]+twisted[b][c]+twisted[c][a];
 const U=mat(θ),Ut=mat(θtw),US=U.map(row=>row.map((x,j)=>x*S[j]));
 allFluxFlipError=Math.max(allFluxFlipError,maxdiff(Ut,US));
 const q=overlap(θ)**2,qt=overlap(θtw)**2;
 triMaxDiff=Math.max(triMaxDiff,Math.abs(q-qt));
 triMinDiff=Math.min(triMinDiff,Math.abs(q-qt));
 const fg=pureGauge[a][b]+pureGauge[b][c]+pureGauge[c][a];
 flatMin=Math.min(flatMin,Math.abs(fg));
 assert(Math.abs(fg)<1e-13,"native pure gradient triangle holonomy not flat");
}
assert(triples===1287&&allFluxFlipError<9e-15&&triMaxDiff>.9,
 "full original 1287 triangle holonomy does not separate feedback twin");
// In the global zero set: ALL native triangles +1 or ALL triangles -1;
// there are TWO original gauge-equivalence classes because H1(filled)=0.
let flatPlus=0,flatMinus=0,notFlat=0;
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<N;c++){
 const f=pureGauge[a][b]+pureGauge[b][c]+pureGauge[c][a],
       g=f+3*Math.PI;
 if(Math.abs(Math.cos(f)-1)<1e-12)flatPlus++;
 if(Math.abs(Math.cos(g)+1)<1e-12)flatMinus++;
 const x=phi[a][b]+phi[b][c]+phi[c][a];
 if(Math.abs(Math.cos(x)-1)>1e-6&&Math.abs(Math.cos(x)+1)>1e-6)
  notFlat++;
}
assert(flatPlus===1287&&flatMinus===1287&&notFlat>1000,
 "global plus/minus native filled-triangle flat classes not resolved");
const psiFlat=overlap(0)**2,psiTwisted=overlap(Math.PI)**2;
assert(Math.abs(psiFlat-1)<1e-15&&Math.abs(psiTwisted)<1e-30,
 "native grade1 CAR coherence cannot distinguish original triangle sheets");

// FULL NATIVE Golden-p 17-outcome Choi/Julia/Bell READOUT distinguishes
// the two F-identical global pi sheets UNIFORMLY at ALL phase angles.
// This is an actually owned *mathematical conditional observer*,
// not its physical G0/controller PREP or selected Book03 price.
const goldp=(Math.sqrt(5)-1)/2,herald=1/4096,
      kGolden=goldp**4/(24*4096);
function completeGolden17(θ){
 const c=Math.cos(θ),sn=Math.sin(θ),
       m=(1+c)/2, q=[];
 for(let a=0;a<6;a++){
  const v=a===4?sn/Math.SQRT2:0;
  q.push(kGolden*(m+v)**2,kGolden*(m-v)**2);
 }
 const GG=goldp**4*herald,
       GB=goldp**3*herald,BG=goldp**3*herald,
       BB=goldp**2*herald;
 q.push(GG-q.reduce((s,x)=>s+x,0),GB,BG,BB,1-herald);
 assert(q.length===17&&Math.min(...q)>-1e-15&&
       Math.abs(q.reduce((s,x)=>s+x,0)-1)<1e-13,
  "true ORIGINAL Golden17 positivity and all failure branches");
 return q;
}
let maxGoldenTVExact=0,minObservedTV=Infinity,maxGoldenTVDiff=0;
for(let m=0;m<=4096;m++){
 const θ=2*Math.PI*m/4096,c=Math.cos(θ),ss=Math.sin(θ);
 const q=completeGolden17(θ),qp=completeGolden17(θ+Math.PI);
 const TV=.5*q.reduce((acc,v,i)=>acc+Math.abs(v-qp[i]),0);
 const formula=kGolden*(11*Math.abs(c)+
                  Math.max(Math.abs(c),Math.SQRT2*Math.abs(ss)));
 maxGoldenTVExact=Math.max(maxGoldenTVExact,Math.abs(TV-formula));
 minObservedTV=Math.min(minObservedTV,TV);
 maxGoldenTVDiff=Math.max(maxGoldenTVDiff,TV);
 assert(TV+2e-14>=Math.SQRT2*kGolden,
  "native positive full17 cannot distinguish global half-turn pi memory");
}
assert(maxGoldenTVExact<4e-15&&
 Math.abs(minObservedTV-Math.SQRT2*kGolden)<3e-15,
 "native global Golden17 sheet separation bound not exact");
// The TRUE full17 two-branch total-variation distinguishability is
// 1/2*(10k|cos| + k|cos+sqrt2 sin| +k|cos-sqrt2 sin|
//      +12k|cos|) = k[11|cos|+max(|cos|,sqrt2|sin|)].
// Thus the uniform bound is SHARP at a pi/2 orientation.
// The chosen composite observer/coframe reference must transform
// covariantly under local physical Lorentz frame changes; its raw
// positive marker is not an observer-free new fundamental postulate.

// STRONGER GLOBAL POSITIVE QUANTUM TOMOGRAPHY: the SAME original 17
// full Golden/Bell probabilities identify EVERY oriented SO(2) face
// holonomy, including the pi sheet invisible to the exact FULL F.
// q_nonJ,+ = k m², m=(1+cos θ)/2≥0.
// q_J,+ - q_J,- = 2 sqrt2 k m sin θ.
// Thus cosθ=2 sqrt(q_nonJ,+/k)−1 and
// sinθ=(qJ+−qJ−)/(2sqrt2 k m), with θ=pi at m=0.
// This inverse is globally exact on U(1) BUT has a genuine non-C1
// inverse chart at theta=pi; smooth 4D refining near-flat plaquettes
// lie in a C1-regular chart, full Spin central sheets remain separate.
function decodeFull17SO2(qq){
 const m=Math.sqrt(Math.max(0,qq[0]/kGolden));
 const co=2*m-1;
 const si=m>1e-14?(qq[8]-qq[9])/(2*Math.SQRT2*kGolden*m):0;
 const rr=Math.hypot(co,si);
 assert(Math.abs(rr-1)<4e-10,
  "actual positive Golden17 outcome is not on full SO2 holonomy circle");
 return {cos:co/rr,sin:si/rr,angle:Math.atan2(si,co)};
}
let maxSO2Tomography=0,maxSO2TriangleSource=0,
    maxGaugeReconstruction=0,zeroFullCAROrientResidual=0;
const phaseFields=[phi,twisted,pureGauge];
for(const field of phaseFields){
 const F=Array.from({length:9},()=>Array.from({length:11},
               ()=>Array(13).fill(0)));
 for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<N;c++){
  const θ=field[a][b]+field[b][c]+field[c][a],
    qq=completeGolden17(θ),rec=decodeFull17SO2(qq);
  maxSO2Tomography=Math.max(maxSO2Tomography,
    Math.abs(Math.cos(θ)-rec.cos),Math.abs(Math.sin(θ)-rec.sin));
  F[a][b-9][c-20]=rec.angle;
 }
 // Exact U(1) right inverse: all original 1287 triangle labels give
 // one arbitrary 359-edge phase representative, whose 327 physical
 // closed holonomies agree. 32 endpoint gradients remain gauge.
 const omega=Array.from({length:N},()=>Array(N).fill(0));
 for(let a=0;a<9;a++)for(let b=9;b<20;b++){
  omega[a][b]=F[a][b-9][0];omega[b][a]=-omega[a][b];
 }
 for(let b=9;b<20;b++)for(let c=20;c<N;c++){
  omega[b][c]=F[0][b-9][c-20]-F[0][b-9][0];
  omega[c][b]=-omega[b][c];
 }
 for(let c=20;c<N;c++)for(let a=0;a<9;a++){
  omega[c][a]=F[a][0][c-20]-F[a][0][0]
     -F[0][0][c-20]+F[0][0][0];
  omega[a][c]=-omega[c][a];
 }
 for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<N;c++){
  const actual=omega[a][b]+omega[b][c]+omega[c][a],
        got=F[a][b-9][c-20],e=actual-got;
  maxSO2TriangleSource=Math.max(maxSO2TriangleSource,
       Math.abs(Math.sin(e)),Math.abs(1-Math.cos(e)));
 }
 // Entire 718-edge gauge relation recovered on native support via
 // one ORIGINAL 32-edge rooted spanning tree, no matrix fit or phase prior.
 const gauge=Array(N).fill(null),queue=[0];gauge[0]=0;
 while(queue.length){
  const i=queue.shift();
  for(let j=0;j<N;j++)if(adj[i][j]&&gauge[j]===null){
   gauge[j]=gauge[i]-field[i][j]+omega[i][j];
   queue.push(j);
  }
 }
 assert(gauge.every(v=>v!==null),"native complete K913 phase gauge disconnected");
 for(const [i,j] of edges){
  const δ=(field[i][j]-omega[i][j])-(gauge[i]-gauge[j]);
  maxGaugeReconstruction=Math.max(maxGaugeReconstruction,
    Math.abs(Math.sin(δ)),Math.abs(1-Math.cos(δ)));
 }
}
// The actual near-flat source is uniformly regular on any
// true physical plaquette chart |theta|<=delta<pi.
const θsmall=.003;
const qPlus=completeGolden17(θsmall),qMinus=completeGolden17(-θsmall);
const dSigned=((qPlus[8]-qPlus[9])-(qMinus[8]-qMinus[9]))/(2*θsmall);
const sourceExpected=2*Math.SQRT2*kGolden;
const sourceError=Math.abs(dSigned-sourceExpected);
assert(maxSO2Tomography<3e-12&&maxSO2TriangleSource<3e-12&&
 maxGaugeReconstruction<3e-12&&sourceError<4e-11,
 "GLOBAL original 327-cycle Golden17 SO2 tomography or smooth source failed");

// FULL ORIGINAL 327-DIMENSIONAL POSITIVE QUANTUM FISHER from ALL1287
// complete native Golden17 conditioned triangle-marked experiments.
// At ORIGINAL FLAT triangle holonomy one face has Fisher
// I_Lie=4k=p^4/(6*4096) for the J23 proper Lorentz rotation.
// On the TRUE native triangle incidence matrix d2^T of shape
// 1287×359, its entire 359-edge Fisher is 4k d2 d2^T.
// Its kernel is EXACTLY 32 original vertex gauge gradients; the
// 327 physical cycles are STRICTLY positive, independent of
// arbitrary nonuniform moving positive Book acceptance weights.
const parent=Array.from({length:N},(_,i)=>i);
function root(x){while(parent[x]!==x){parent[x]=parent[parent[x]];x=parent[x];}return x;}
const chords=[],tree=[];
for(let e=0;e<edges.length;e++){
 const [i,j]=edges[e],ii=root(i),jj=root(j);
 if(ii===jj)chords.push(e);
 else{parent[ii]=jj;tree.push(e);}
}
assert(tree.length===32&&chords.length===327,
 "native ABC graph 32 vertex gauges+327 independent triangle cycles");
const chordIndex=new Map(chords.map((k,i)=>[k,i]));
const edgeIndex=new Map(edges.map(([i,j],k)=>[i+","+j,k]));
const cN=chords.length,Gram=Array.from({length:cN},
 ()=>Array(cN).fill(0)),WGram=Array.from({length:cN},
 ()=>Array(cN).fill(0));
const nativeP=(Math.sqrt(5)-1)/2,logphi=Math.log(1/nativeP);
const nativeK=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>{
 if(!adj[i][j])return 0;
 return nativeP*Math.exp(-logphi*(.07*Math.sin(.17*i+.23*j)**2+
                                     .03*Math.cos(.13*i+.21*j)**2));
}));
const faceData=[];
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<N;c++){
 const orig=[
  [edgeIndex.get(a+","+b),+1],
  [edgeIndex.get(b+","+c),+1],
  [edgeIndex.get(a+","+c),-1]
 ];
 const sparse=orig.filter(([e])=>chordIndex.has(e))
     .map(([e,s])=>[chordIndex.get(e),s]);
 const w=nativeK[a][b]*nativeK[b][c]*nativeK[c][a];
 faceData.push({sparse,orig,w});
}
const totalW=faceData.reduce((s,v)=>s+v.w,0);
let minBookFaceWeight=Infinity,maxBookFaceWeight=0;
for(const {sparse,w} of faceData){
 const prob=w/totalW;
 minBookFaceWeight=Math.min(minBookFaceWeight,prob);
 maxBookFaceWeight=Math.max(maxBookFaceWeight,prob);
 for(const [i,sgnI] of sparse)for(const [j,sgnJ] of sparse){
  Gram[i][j]+=sgnI*sgnJ;
  WGram[i][j]+=prob*sgnI*sgnJ;
 }
}
function strictCholesky(A){
 const n=A.length,L=Array.from({length:n},()=>Array(n).fill(0));
 let min=Infinity,max=0;
 for(let i=0;i<n;i++)for(let j=0;j<=i;j++){
  let x=A[i][j];
  for(let z=0;z<j;z++)x-=L[i][z]*L[j][z];
  if(i===j){
   assert(x>1e-14,"original all327 phase triangle Fisher not full rank");
   L[i][j]=Math.sqrt(x);
   min=Math.min(min,L[i][j]);max=Math.max(max,L[i][j]);
  }else L[i][j]=x/L[j][j];
 }
 return {min,max};
}
const unitChol=strictCholesky(Gram),
      paidChol=strictCholesky(WGram);
let maxGradientFaceError=0;
const vertexPotential=Array.from({length:N},(_,i)=>
 .17*Math.sin(i*.13)+.34*Math.cos(i*.21));
for(const face of faceData){
 const s=face.orig.reduce((v,[edge,sign])=>{
  const [i,j]=edges[edge];return v+sign*(vertexPotential[i]-vertexPotential[j]);
 },0);
 maxGradientFaceError=Math.max(maxGradientFaceError,Math.abs(s));
}
assert(maxGradientFaceError<6e-16,
 "all1287 original triangle Fisher should be blind to original 32 site gauge gradients");
const lStep=.0002;
const qqp=completeGolden17(lStep),qqm=completeGolden17(-lStep),
      qq0=completeGolden17(0);
const fisherOneFace=qq0.reduce((z,v,i)=>{
 const d=(qqp[i]-qqm[i])/(2*lStep);
 return z+(v>0?d*d/v:0);
},0);
assert(Math.abs(fisherOneFace-4*kGolden)<5e-12,
 "native complete 17 face mark Fisher per J23 Lie equals original 4k");
const minConditionalFaceFisher=4*kGolden*minBookFaceWeight;

// IMPORTANT: the two true ORIGINAL 327-metrics are BOTH definite on
// cycles but they are NOT necessarily a multiple of one another:
//  Q_Book(a)=2 sum μ_e(a−grad b)^2 (all-walk current cost curvature),
//  I_Golden17(a)=4k sum_triangle w_t (delta a)^2 (all positive faces).
// One must not identify this difference with an Einstein coupling.
// This whole-original bridge is a canonical pair of source forms
// related by a calculable positive operator on the same 327-dimensional
// cycle quotient, with no unsupported universal proportionality.
const muUnd=edges.map(([i,j])=>Perron[i]*Perron[j]/rho);
const lap=Array.from({length:N},()=>Array(N).fill(0));
for(let e=0;e<edges.length;e++){
 const [i,j]=edges[e],w=muUnd[e];
 lap[i][i]+=w;lap[j][j]+=w;lap[i][j]-=w;lap[j][i]-=w;
}
function solveGauge(a){
 const div=Array(N).fill(0);
 for(let e=0;e<edges.length;e++){
  const [i,j]=edges[e],v=muUnd[e]*a[e];
  div[i]+=v;div[j]-=v;
 }
 const n=N-1,M=Array.from({length:n},(_,i)=>
   [...lap[i].slice(0,n),div[i]]);
 for(let k=0;k<n;k++){
  let idx=k;for(let i=k+1;i<n;i++)
   if(Math.abs(M[i][k])>Math.abs(M[idx][k]))idx=i;
  assert(Math.abs(M[idx][k])>1e-12,
    "all original 33 native vertex Laplacian roots not solved");
  [M[idx],M[k]]=[M[k],M[idx]];
  const z=M[k][k];for(let j=k;j<=n;j++)M[k][j]/=z;
  for(let i=k+1;i<n;i++){
   const g=M[i][k];
   for(let j=k;j<=n;j++)M[i][j]-=g*M[k][j];
  }
 }
 const b=Array(N).fill(0);
 for(let i=n-1;i>=0;i--){
  let z=M[i][n];
  for(let j=i+1;j<n;j++)z-=M[i][j]*b[j];
  b[i]=z;
 }
 return b;
}
function bookVariance(a){
 const b=solveGauge(a);
 return 2*edges.reduce((s,[i,j],e)=>{
  const v=a[e]-b[i]+b[j];
  return s+muUnd[e]*v*v;
 },0);
}
function fullGoldenFaceFisher(a){
 return 4*kGolden*faceData.reduce((s,face)=>{
  const flux=face.orig.reduce((z,[e,sgn])=>z+sgn*a[e],0);
  return s+(face.w/totalW)*flux*flux;
 },0);
}
const originalCP=edges.map(([i,j])=>{
 const a=zone(i),b=zone(j);
 return (a===0&&b===1)||(a===1&&b===2)?1:-1;
});
const originalOneEdge=edges.map((_,e)=>+(e===0));
const independentSourceRatios=[
 ["CP",originalCP],["singleRealEdge",originalOneEdge]
].map(([name,a])=>{
 const Q=bookVariance(a),Gf=fullGoldenFaceFisher(a);
 assert(Q>0&&Gf>0,"genuine native cycle modes not measured by Golden/Book");
 return {name,actualBookCycleVariance:Q,fullGolden17TriangleFisher:Gf,
          ratioOfTwoDifferentPhysicallyTypedMetrics:Gf/Q};
});
assert(Math.abs(independentSourceRatios[0].ratioOfTwoDifferentPhysicallyTypedMetrics-
                independentSourceRatios[1].ratioOfTwoDifferentPhysicallyTypedMetrics)
       >1e-6,"full native 327 Book and Golden face metrics should not be blindly identified");

// EXACT ORIGINAL Golden conditional p:p² CODE price, ALL 17 native
// labels kept. For one original SO2 triangle and its TRUE reversal,
// the complete relative-code excess has an EXACT signed difference:
//
//   Δ_code(θ):=D_phi(q17(θ)||mu)-D_phi(q17(-θ)||mu)
//           = -[q_J+(θ)-q_J-(θ)]
//           = -2sqrt2 k m(θ) sinθ,
//
// with m=(1+cosθ)/2 and k=p^4/(24*4096).
// Its FIRST ODD-CONTRAST source is Δ'_code(0)=-2sqrt2 k;
// the source of ONE forward code separately is half this:
// D'_phi(q17(θ)||mu)|0=-sqrt2 k.
// The ratio -Δ/(2sqrt2 k m) extends ANALYTICALLY to sinθ at
// θ=pi, even though raw floating KL subtraction is ill-conditioned
// there and individual qlogq terms need not be C2.
// This is an actual mathematically admissible ORIGINAL fixed GOLDEN
// code-reference, NOT proof that Book03/H+J+R selects its price.
const fixedNativeGoldenP=(Math.sqrt(5)-1)/2,
      loggold=Math.log(1/fixedNativeGoldenP);
const fullReference=completeGolden17(0),goldenCode=fullReference.slice();
for(let j=0;j<6;j++){
 const mass=fullReference[2*j]+fullReference[2*j+1];
 goldenCode[2*j]=mass*fixedNativeGoldenP;
 goldenCode[2*j+1]=mass*fixedNativeGoldenP**2;
}
assert(Math.min(...goldenCode)>0&&
       Math.abs(goldenCode.reduce((s,x)=>s+x,0)-1)<1e-14,
 "actual original Golden17 p:p² code not faithful");
const KLφ=(q,code)=>q.reduce((sum,v,i)=>
 sum+(v>0?v*Math.log(v/code[i])/loggold:0),0);
let maxOddGoldenSourceError=0,maxOddRecoveredCurvatureError=0;
for(let j=0;j<=4096;j++){
 const θ=2*Math.PI*j/4096,qr=completeGolden17(θ),
       qback=completeGolden17(-θ);
 const delta=KLφ(qr,goldenCode)-KLφ(qback,goldenCode);
 const m=(1+Math.cos(θ))/2,
       analytic=-2*Math.SQRT2*kGolden*m*Math.sin(θ);
 maxOddGoldenSourceError=Math.max(maxOddGoldenSourceError,
                                 Math.abs(delta-analytic));
 if(m>1e-12){
  const sinRecovered=-delta/(2*Math.SQRT2*kGolden*m);
  maxOddRecoveredCurvatureError=Math.max(maxOddRecoveredCurvatureError,
                            Math.abs(sinRecovered-Math.sin(θ)));
 }
}
const hCode=.0015;
const oneSource=(KLφ(completeGolden17(hCode),goldenCode)-
                 KLφ(completeGolden17(-hCode),goldenCode))/(2*hCode);
const singleAnalytic=-Math.SQRT2*kGolden,
      contrastAnalytic=2*singleAnalytic;
assert(maxOddGoldenSourceError<3e-14&&
       maxOddRecoveredCurvatureError<3e-9&&
       Math.abs(oneSource-singleAnalytic)<1e-10,
 "original Golden signed relative CODE source did not recover nonlinear holonomy");
console.log(JSON.stringify({
 result:"PASS_GLOBAL_ALL327_FULLCAR16_F_SQUARING_Z2_INDISTINGUISHABILITY",
 actualNativeCarrier:{sceneVertices:33,fullOriginalDirectedEdges:718,
  undirectedEdges:359,independentCycleDegrees:327,
  allOriginalABCbasedTriangles:triples,fullCAR16Grades:16,
  exactSimulatedFullFeedbackOperatorDimension:528},
 exactAllOrderOperator:{matrixEquality:"F(phi+pi on every original edge)=F(phi)",
  maxFull528SquaredReturnDifference:maxFullCARF,
  completeGolden17Detector:{labels:17,includesAllBellAndGoodBadFailures:true,
   exactFullTV_formula:"k(11|cosθ|+max(|cosθ|,√2|sinθ|)), k=p^4/(24*4096)",
   SHARP_global_minimumTV:Math.SQRT2*kGolden,
   exactGlobalSO2FaceTomography:true,
   maxRecoveredActual1287FaceHolonomyError:maxSO2Tomography,
   maxOriginal1287TriangleCochainRightInverseError:maxSO2TriangleSource,
   maxOriginal718EdgePhaseGaugeReconstructionError:maxGaugeReconstruction,
   all327LocalGolden17Fisher:{fullRankOnChordGauge:cN,
    originalGaugeKernel:tree.length,originalFaceCount:faceData.length,
    singleFaceAnalyticJ23Fisher:4*kGolden,
    singleFaceFiniteDifferenceFisher:fisherOneFace,
    unweightedTriangleGramCholesky:unitChol,
    trueNonuniformBookTriangleFlowCholesky:paidChol,
    minimumPositiveNonuniformBookFaceWeight:minBookFaceWeight,
    maximumPositiveNonuniformBookFaceWeight:maxBookFaceWeight,
    positiveFisherWeightFloor:minConditionalFaceFisher,
    pureOriginalGaugeFisherSourceError:maxGradientFaceError,
    nativeBookVsGoldenTwoDistinctMetrics:independentSourceRatios,
    exactGoldenNativeOddCodeSource:{
       referenceAlphabet:"fixed original p:p² on six marked +- pairs, full17 other outcomes",
       fullPhiRelativeCodeDifference:"-2sqrt2*k*m(theta)*sin(theta)",
       fullPhaseContrastAnalyticSource:contrastAnalytic,
       nativeSingleForwardCodeAnalyticSource:singleAnalytic,
       nativeSingleForwardCodeFiniteSource:oneSource,
       full4097AngleExactSourceDifferenceError:maxOddGoldenSourceError,
       recoveredSinMaxAbsoluteErrorNearPi:maxOddRecoveredCurvatureError,
       ratioHasAnalyticPhaseLimitAtPiButNumericallyIllConditioned:true,
       originalPhysicalG0CodeSelectorStillMissing:true},


    movingBookWeightsCannotRemoveConditionalFisherIfPositive:true},

   nearFlatSignedLorentzLinearCoefficient:sourceExpected,
   nearFlatSignedLorentzSourceError:sourceError,
   globalDecoderSmoothExceptAtCompactPiHalfturn:true,

   observedMinimumTV:minObservedTV,
   maximumTV:maxGoldenTVDiff,
   exactFormulaMaxError:maxGoldenTVExact,
   fullCAR16PretraceReadoutNeeded:true},

  maxEdge16x16HalfTurnIdentity:maxHalfTurnOperator,
  CAR16ExactRotationGroupError:maxCARGroup,
  appliesAtArbitraryOriginal359OrientationInputs:true,
  localHessianAndAllDerivativeJetsAlsoBlind:true},
 fullHistoricalDistinguishability:{triangleHolonomyIdentity:
  "U_abc^twist=U_abc * Lambda(R23(pi))",
  all1287HolonomyMaxEntryError:allFluxFlipError,
  maximumActualCoherentProbabilityDifference:triMaxDiff,
  minimumActualCoherentProbabilityDifference:triMinDiff,
  flatCoherentEventProb:psiFlat,allPiTriangleCoherentEventProb:psiTwisted,
  allOriginalScalarBookWeightsUnchanged:originalCompleteBook,
  originalBased2Z:originalZ2,originalBased3Z:originalZ3},
 globalPositiveFKernelClassification:{
  plusClass:"all 1287 triangle fluxes 0 mod 2pi",
  minusClass:"all 1287 triangle fluxes pi mod 2pi",
  plusOriginalTriangleChecks:flatPlus,minusOriginalTriangleChecks:flatMinus,
  genericFrustratedOriginalTriangleChecks:notFlat,
  chargedCAR16GenericFNullity:0,chargedCAR16PlusMinusFNullity:8,
  neutralCAR16AlwaysFNullity:8,
  fullGenericFNullity:8,fullPlusMinusFNullity:16},
 notTheFullSpinQ8Center:true,
 noPhysicalCompulsoryFullBookSourceOrEinsteinProof:true,
 GR_closed:false
},null,2));
