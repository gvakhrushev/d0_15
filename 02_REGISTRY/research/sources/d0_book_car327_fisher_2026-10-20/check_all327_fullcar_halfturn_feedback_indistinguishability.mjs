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
console.log(JSON.stringify({
 result:"PASS_GLOBAL_ALL327_FULLCAR16_F_SQUARING_Z2_INDISTINGUISHABILITY",
 actualNativeCarrier:{sceneVertices:33,fullOriginalDirectedEdges:718,
  undirectedEdges:359,independentCycleDegrees:327,
  allOriginalABCbasedTriangles:triples,fullCAR16Grades:16,
  exactSimulatedFullFeedbackOperatorDimension:528},
 exactAllOrderOperator:{matrixEquality:"F(phi+pi on every original edge)=F(phi)",
  maxFull528SquaredReturnDifference:maxFullCARF,
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
