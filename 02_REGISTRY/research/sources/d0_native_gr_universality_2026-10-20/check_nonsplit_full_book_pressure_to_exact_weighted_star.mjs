#!/usr/bin/env node
"use strict";
/*
 * STRATEGIC D0→GR UNIVERSALITY / NO BOOK ACTION FIT.
 *
 * The mathematical theorem is proved in RESULT.md:
 * for actual six-based Palatini site densities f_i(e,U) homogeneous
 * degree 2 in site i's ORIGINAL coframe e_i and unchanged at j!=i;
 * and for ANY C^2 smooth, perhaps completely NONSEPARABLE field
 * history cost F(f_0,...,f_{N-1}) with w_i=dF/df_i(0)!=0,
 * define a_i(f)=int_0^1 dF/df_i(t f) dt;
 *    e_tilde_i = sqrt(a_i(f)/w_i) e_i;
 * then EXACTLY F(f(e,U))-F(0) = SUM_i w_i f_i(e_tilde,U).
 * f→f*a_i(f)/w_i is a local diffeo at zero (derivative I);
 * the full coframe map is invertible by its determinant identity in
 * RESULT.md, with the SAME physical links U.
 * Independently radially varying EACH site forces f_i=0 at
 * ANY vacuum stationary point for either action, and then ALL
 * 16+24 original equations have identical zero sets.
 * More strongly, the site-radial Euler identities prove equality of
 * the full linearized kernels in original coordinates: contracting
 * either Hessian with Z_i=e_i gives 2*w_i*df_i[V]. The checker is a
 * numerical witness for one fixture, not the proof of this theorem.
 *
 * This fixture is NOT physically selected D0 action. It is a
 * hostile ORIGINAL 718-edge 8440-history native Book clock
 * mathematical completion whose primitive C_uv>=1 exactly,
 * moving vertex Info_v(f) supplies the linear curvature source,
 * and nontrivial mixed f_i f_j couplings really occur. We vary
 * the REAL original 16-site 4D L2 proper SO six-based field.
 *
 * A compulsory D0 G0 proof needs much less than EXACT matching
 * the complete original H+J+R to Palatini. It suffices that its
 * geometric dependence, after internal Euler, factors through
 * f_i, with ALL w_i nonzero and correctly signed. This
 * factorization is OPEN and cannot be inferred from this fixture.
 */
const check=(ok,msg)=>{if(!ok)throw Error("FAIL "+msg)};
const golden=(Math.sqrt(5)-1)/2,phi=(1+Math.sqrt(5))/2,lnphi=Math.log(phi);
const N=16,L=2,sites=Array.from({length:N},(_,i)=>i),
  prs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const E=(a,b)=>Array.from({length:4},(_,i)=>
 Array.from({length:4},(_,j)=>+(i===a&&j===b)));
const I=()=>Array.from({length:4},(_,i)=>
 Array.from({length:4},(_,j)=>+(i===j)));
const add=(A,B,c=1)=>A.map((r,i)=>r.map((v,j)=>v+c*B[i][j])),
  sc=(A,t)=>A.map(r=>r.map(v=>v*t)),
  matmul=(A,B)=>A.map(row=>B[0].map((_,j)=>
    row.reduce((s,v,k)=>s+v*B[k][j],0))),
  tr=A=>A[0].map((_,j)=>A.map(r=>r[j])),
  max=A=>Math.max(...A.flat(Infinity).map(x=>Math.abs(x)));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const invSO=U=>matmul(matmul(eta,tr(U)),eta);
const same=(A,B,tol=1e-12)=>max(add(A,B,-1))<tol;
const shift=(x,r)=>x^(1<<r);
const gen=[add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
  add(E(0,2),E(2,1)),add(E(0,3),E(3,1))];
function expNull(j,t){
  const G=gen[j],G2=matmul(G,G);
  return add(add(I(),sc(G,t)),sc(G2,t*t/2));
}
const links=sites.map(x=>Array.from({length:4},(_,r)=>{
  const A=expNull((x+2*r)%4,.004*(1+(x+r)%3)),
    B=expNull((3*x+r+1)%4,.003*(1+(2*x+r)%2)),
    U=matmul(A,B);
  check(same(matmul(matmul(tr(U),eta),U),eta,3e-14),
    "not real ORIGINAL proper SO four-link connection");
  return U;
}));
const coframes=sites.map(x=>Array.from({length:4},(_,a)=>
 Array.from({length:4},(_,mu)=>
  +(a===mu)+.003*((7*x+3*a+5*mu+mu*a)%9-4))));
const eps=(a,b,c,d)=>{
 const seq=[a,b,c,d];if(new Set(seq).size!==4)return 0;
 let sign=1;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)
  if(seq[i]>seq[j])sign=-sign;
 return sign;
};
function pairing(e,u,v,R){
  const C=matmul(R,eta);let z=0;
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
    const [c,d]=[0,1,2,3].filter(i=>i!==a&&i!==b);
    z+=eps(a,b,c,d)*(e[a][u]*e[b][v]-e[b][u]*e[a][v])*C[c][d];
  }
  return z;
}
function originalStarSite(x,e=coframes[x]){
  let sum=0;
  for(let [r,s] of prs){
    const [u,v]=[0,1,2,3].filter(i=>i!==r&&i!==s);
    const P=matmul(matmul(matmul(links[x][r],
      links[shift(x,r)][s]),
      invSO(links[shift(x,s)][r])),invSO(links[x][s])),
      R=sc(add(P,invSO(P),-1),.5);
    sum+=eps(r,s,u,v)*pairing(e,u,v,R);
  }
  return sum;
}
const f=sites.map(x=>originalStarSite(x));
check(f.every(Number.isFinite)&&f.some(x=>Math.abs(x)>1e-4),
  "not actual nonflat original six-based Role star densities");
for(let i=0;i<N;i++){
 const t=1.061,scaled=sc(coframes[i],t);
 check(Math.abs(originalStarSite(i,scaled)-t*t*f[i])<1e-11,
  "original Palatini site quadratic source property failed");
}
// ORIGINAL all718 directed Book transitions and all 8440 BASED
// closed 2- and 3-step scene paths. Absolutely NO new graph.
const zone=x=>x<9?0:x<20?1:2;
const allowed=(u,v)=>zone(u)!==zone(v);
const edges=[],hist=[];
for(let u=0;u<33;u++)for(let v=0;v<33;v++)if(allowed(u,v)){
 edges.push([u,v]);hist.push([u,v,u]);
}
for(let a=0;a<9;a++)for(let b=9;b<20;b++)
 for(let c=20;c<33;c++){
  const perms=[[a,b,c],[a,c,b],[b,c,a],[b,a,c],[c,a,b],[c,b,a]];
  for(let q of perms)hist.push([...q,q[0]]);
}
check(edges.length===718&&hist.length===8440,
  "not complete ORIGINAL K(9,11,13) scene closed loops");
const Kinds=2,attempt={2:golden,3:golden*golden};
// Actual primitive Cost=C_uv(f)>=1 for EVERY REAL f, no
// incompatible first derivative at the canonical minimum.
// Original vertex Info_v(f) is a positive native-TYPE recorded
// gain, smooth with unknown actual selector. Its first gradient
// generates the (negative) source; nonlinear cross terms give
// a NONSEPARABLE Book pressure.
function features(z){
 let sum=0,squares=0,neighbor=0;
 for(let i=0;i<N;i++){
   sum+=z[i];squares+=z[i]*z[i];
   neighbor+=z[i]*z[shift(i,0)];
 }
 return {sum,squares,neighbor};
}
function edgeCost(u,v,z,ff){
 const d=.005*(1+(u+2*v)%5)/N;
 return 1+d*ff.squares;
}
function info(v,z,ff){
 const b=.075+.003*(v%5),g=.012*(1+v%3)/N,
   d=.01*(1+v%4)/N;
 return .6+.002*(v%7)+b*ff.sum+g*ff.squares+d*ff.neighbor;
}
function desc(z){
 const ff=features(z),out=[];
 for(let [u,v] of edges){
  const cu=edgeCost(u,v,z,ff),Su=info(u,z,ff),Sv=info(v,z,ff);
  check(cu>=1-1e-14,"Cost<1 violates original ActionProtocol");
  out.push(Math.exp(-lnphi*(cu-(Su+Sv)/2)));
 }
 return out;
}
const graphIndex=Array.from({length:33},()=>Array(33).fill(-1));
edges.forEach(([u,v],i)=>graphIndex[u][v]=i);
const pathEdges=hist.map(w=>{
 const ids=[];
 for(let i=1;i<w.length;i++)ids.push(graphIndex[w[i-1]][w[i]]);
 check(ids.every(i=>i>=0),"nonexistent original native scene edge");
 return ids;
});
function originalBookLogZ(z){
 const W=desc(z);let sum=0;
 for(let i=0;i<hist.length;i++){
  const ids=pathEdges[i],time=ids.length;
  let val=attempt[time];for(let id of ids)val*=W[id];
  sum+=val;
 }
 return Math.log(sum);
}
const z0=Array(N).fill(0),baseLogZ=originalBookLogZ(z0);
function F(z){return -(originalBookLogZ(z)-baseLogZ)/lnphi}
function gradient(z){
 const ff=features(z),Cost=Array.from({length:33},()=>null),
   i0=Array.from({length:33},()=>Array(N).fill(0)),
   edgeS=Array(edges.length).fill(0),
   W=Array(edges.length).fill(0),
   edgeDerivative=Array.from({length:edges.length},()=>Array(N).fill(0));
 const dff=Array.from({length:N},(_,i)=>({
   sum:1,squares:2*z[i],
   neighbor:z[shift(i,0)]+z[shift(i,0)] // shift back=shift forward for L=2
 }));
 for(let v=0;v<33;v++){
  for(let i=0;i<N;i++){
   i0[v][i]=(.075+.003*(v%5))*dff[i].sum
      +.012*(1+v%3)/N*dff[i].squares
      +.01*(1+v%4)/N*dff[i].neighbor;
  }
 }
 for(let e=0;e<edges.length;e++){
  const [u,v]=edges[e],
    Cu=edgeCost(u,v,z,ff),Su=info(u,z,ff),Sv=info(v,z,ff),
    s=Cu-(Su+Sv)/2;
  edgeS[e]=s;W[e]=Math.exp(-lnphi*s);
  for(let i=0;i<N;i++)
    edgeDerivative[e][i]=.005*(1+(u+2*v)%5)/N*dff[i].squares
        -(i0[u][i]+i0[v][i])/2;
 }
 let Z=0,A=Array(N).fill(0);
 for(const ids of pathEdges){
  let weight=attempt[ids.length],s=Array(N).fill(0);
  for(const e of ids){
   weight*=W[e];
   for(let j=0;j<N;j++)s[j]+=edgeDerivative[e][j];
  }
  Z+=weight;
  for(let j=0;j<N;j++)A[j]+=weight*s[j];
 }
 return A.map(x=>x/Z);
}
const w=gradient(z0);
check(w.every(v=>v<-.02)&&Math.max(...w)-Math.min(...w)<1e-12,
  "flat original Book source has nonuniform/zero first star coefficient");
const wFlat=w[0];
// Explicit nonseparable original Book Hessian: nearest-neighbor versus
// distant site fields produce DIFFERENT exact mixed second-jet values.
function second(i,j,h=.0003){
 const z=Array(N).fill(0);
 z[i]=h;z[j]=h;const pp=F(z);
 z[j]=-h;const pm=F(z);
 z[i]=-h;z[j]=h;const mp=F(z);
 z[j]=-h;const mm=F(z);
 return (pp-pm-mp+mm)/(4*h*h);
}
const near=second(0,1),far=second(0,7);
check(Number.isFinite(near)&&Number.isFinite(far)&&
 Math.abs(near-far)>1e-4,"original full Book cannot demonstrate true nonseparability");
// 8-point Gaussian quadrature of mathematically exact line-homotopy,
// f0=0 has w_i, using all8440 historical events at every node.
const xgauss=[-.9602898564975363,-.7966664774136267,
 -.5255324099163290,-.1834346424956498,
 .1834346424956498,.5255324099163290,
 .7966664774136267,.9602898564975363],
 gaussw=[.1012285362903763,.2223810344533745,
 .3137066458778873,.3626837833783620,
 .3626837833783620,.3137066458778873,
 .2223810344533745,.1012285362903763];
function integratedWeights(z){
 let A=Array(N).fill(0);
 for(let k=0;k<8;k++){
  const t=(xgauss[k]+1)/2,gt=gradient(z.map(v=>v*t));
  for(let j=0;j<N;j++)A[j]+=gt[j]*gaussw[k]/2;
 }
 return A;
}
const A=integratedWeights(f),sigma=A.map((v,i)=>Math.sqrt(v/w[i]));
check(sigma.every(v=>v>0&&Number.isFinite(v)),
 "non-positive global Book coframe dressing on curved chart");
const eTilde=coframes.map((e,i)=>sc(e,sigma[i]));
const fTilde=sites.map(i=>originalStarSite(i,eTilde[i]));
const star=sites.reduce((s,i)=>s+w[i]*fTilde[i],0),book=F(f);
check(Math.abs(book-star)<2e-8,
 "nonseparable ORIGINAL full718 Book pressure not coframe-equivalent");
check(Math.max(...fTilde.map((v,i)=>Math.abs(v-(A[i]/w[i])*f[i])))<1e-12,
 "original 16 coframes did not retain exact site-square homogeneity");
// Test the finite-dimensional diffeomorphism on f coordinates.
// g_i=(a_i(f)/w_i) f_i. This map has Dh(0)=I analytically.
// Simple Newton-like iteration recovers the original f from g.
let invF=fTilde.slice(),iterations=0;
for(;iterations<12;iterations++){
 const Ai=integratedWeights(invF);
 const next=invF.map((_,i)=>fTilde[i]*w[i]/Ai[i]);
 if(Math.max(...next.map((v,i)=>Math.abs(v-invF[i])))<1e-14){
   invF=next;break;
 }
 invF=next;
}
const maxInverse=Math.max(...invF.map((v,i)=>Math.abs(v-f[i])));
check(maxInverse<1e-10,"nonseparable global radial diffeomorphism has no inverse");
const result={
 status:"PASS_CONSTRUCTED_ORIGINAL_718_BOOK_NATIVE_TYPE_CONTROL",
 trueOriginalRoleStar:{sites:N,links:4*N,
  genuineSixFaceTypes:prs.length,
  maxOriginalSiteDensity:Math.max(...f.map(Math.abs)),
  nonzeroSites:f.filter(v=>Math.abs(v)>1e-7).length,
  independentOriginalLocalCoframeQuadratic:true},
 originalBookNativeTypeControl:{
  originalVertices:33,originalDirectedEdges:edges.length,
  allRetainedTwoThreeClosedHistories:hist.length,
  primitiveCostAtOriginOne:true,
  primitiveCostNeverBelowOne:true,
  fieldSourceCarriedByOriginalMovingVertexInfo:true,
  minFirstGradient:wFlat,
  siteWeightsAllEqualAtOrigin:true,
  nearbyCrossSecondDerivative:near,
  distantCrossSecondDerivative:far,
  trulyNonseparableHistoryAction:true,
  wholeBookNativeSelectorProved:false,
  fieldMapIsConstructedControl:true},
 exactMathematicalTheorem:{
  statement:"For any C2 F(f) with all w_i=dF/df_i(0)!=0, the local vacuum stationary sets agree pointwise with the weighted original six-face star. The full actions are exactly related by a local coframe diffeomorphism; stationary Hessians are congruent and the site-radial Euler identities prove equality of their kernels in the original coordinates.",
  canonicalHomotopy:"a_i(f)=int_0^1 dF/d f_i(t f) dt",
  coframe:"e_i_tilde=sqrt(a_i(f)/w_i)*e_i",
  scalarDiffeomorphism:"g_i(f)=f_i*a_i(f)/w_i; Dg(0)=I",
  onVacuumCoframeIdentity:true,
  nativeMetricMatterSourceSelectionStillOpen:true},
 numericalNonseparableOriginalBook:{
  BookF:book,weightedStarFromQuadrature:star,
  difference:book-star,
  comparisonMethod:"floating point; 8-point Gauss-Legendre homotopy; not an exact-arithmetic replay",
  minimumDressing:Math.min(...sigma),maximumDressing:Math.max(...sigma),
  gradientLineQuadratureNodes:8,
  scalarInverseIterations:iterations+1,
  scalarInverseError:maxInverse,
  interpretedAsPhysicalNativeGR:false},
 GR_closed:false
};
console.log(JSON.stringify(result,null,2));
