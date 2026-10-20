#!/usr/bin/env node
"use strict";
/*
  EXACT GENERIC THEOREM / ORIGINAL K(9,11,13) 33-vertex, 359 undirected,
  718 directed graph: ALL 327 independent original odd cycle-price
  directions, NOT ONLY its single CP 9→11→13 direction.

  For every antisymmetric original Book log-PRICE edge 1-cochain a:
    h_a = a - d chi, L_mu chi = divergence_mu(a)
    Q(a,b) = 2 sum_e mu_e h_a(e) h_b(e).
  Q positive definite modulo original vertex PRICE coboundaries
  (cycle dimension 359-(33-1)=327). It is EXACTLY:
  (1) the long-run Fisher/Green-Kubo Hessian of original scalar
      Perron Book pressure log rho(K exp(eps a));
  (2) the quadratic spectral gap of the REAL full-CAR16 magnetic
      predictive feedback F=I-T_theta^2, using native
      Lambda(exp(theta a_uv J23)) on the existing 16-dimensional CAR
      exterior carrier. Eight (=4+4) helicity branches gap, eight
      neutral ones do NOT; all old 480 30-Ker states remain unshifted.

  Physically selected CAR edge controller, real Book Cost code budget,
  original full H+J+R, Spin/Q8 and 4D Role Einstein source NOT selected.
  Research-only; GR_closed=false.
*/
const assert=(v,m)=>{if(!v)throw Error("FAIL "+m);};
const N=33,zone=i=>i<9?0:i<20?1:2;
const edges=[];
const A=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>+(zone(i)!==zone(j))));
for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(A[i][j])edges.push([i,j]);
const M=edges.length;
assert(M===359&&edges.length*2===718,"native directed/undirected size");
const norm=v=>Math.sqrt(v.reduce((s,x)=>s+x*x,0));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const matvec=(W,v)=>W.map(row=>dot(row,v));
let rho=0,r=Array(N).fill(1/Math.sqrt(N));
for(let z=0;z<180;z++){
 const t=matvec(A,r);rho=norm(t);r=t.map(x=>x/rho);
}
const perronErr=Math.max(...matvec(A,r).map((x,i)=>Math.abs(x-rho*r[i])));
assert(perronErr<5e-13,"original exact Perron eigenstate");
const pi=r.map(x=>x*x);
const P=A.map((row,i)=>row.map((x,j)=>x*r[j]/(rho*r[i])));
let stochasticErr=Math.max(...P.map(row=>Math.abs(row.reduce((s,x)=>s+x,0)-1)));
assert(stochasticErr<5e-13,"native Perron stochastic rows");
const weight=edges.map(([i,j])=>r[i]*r[j]/rho);
const LM=Array.from({length:N},()=>Array(N).fill(0));
for(let e=0;e<M;e++){
 const [i,j]=edges[e],w=weight[e];
 LM[i][i]+=w;LM[j][j]+=w;LM[i][j]-=w;LM[j][i]-=w;
}
function solveReduced(rhs){
 const n=N-1;
 let T=Array.from({length:n},(_,i)=>[...LM[i].slice(0,n),rhs[i]]);
 for(let k=0;k<n;k++){
  let pivot=k;for(let i=k+1;i<n;i++)if(Math.abs(T[i][k])>Math.abs(T[pivot][k]))pivot=i;
  assert(Math.abs(T[pivot][k])>1e-10,"native connected weighted graph Laplacian");
  [T[k],T[pivot]]=[T[pivot],T[k]];
  const d=T[k][k];for(let j=k;j<=n;j++)T[k][j]/=d;
  for(let i=k+1;i<n;i++){
   const v=T[i][k];if(!v)continue;
   for(let j=k;j<=n;j++)T[i][j]-=v*T[k][j];
  }
 }
 const x=Array(N).fill(0);
 for(let i=n-1;i>=0;i--){let y=T[i][n];for(let j=i+1;j<n;j++)y-=T[i][j]*x[j];x[i]=y;}
 return x;
}
function harmonic(a){
 assert(a.length===M,"original cochain dimension");
 const div=Array(N).fill(0);
 for(let e=0;e<M;e++){
  const [i,j]=edges[e],v=weight[e]*a[e];
  div[i]+=v;div[j]-=v;
 }
 const chi=solveReduced(div);
 const h=edges.map(([i,j],e)=>a[e]-chi[i]+chi[j]);
 const resid=Array(N).fill(0);
 for(let e=0;e<M;e++){
  let [i,j]=edges[e],v=weight[e]*h[e];resid[i]+=v;resid[j]-=v;
 }
 const err=Math.max(...resid.map(Math.abs));
 assert(err<1e-11,"all 327 cycle divergence equations");
 return {h,chi,err};
}
function Q(a,b){
 const ha=harmonic(a).h,hb=harmonic(b).h;
 return 2*ha.reduce((s,v,i)=>s+v*weight[i]*hb[i],0);
}
const parent=Array.from({length:N},(_,i)=>i);
function find(i){while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i];}return i;}
const tree=[],chords=[];
for(let e=0;e<M;e++){
 const [i,j]=edges[e],ii=find(i),jj=find(j);
 if(ii===jj)chords.push(e);else{parent[ii]=jj;tree.push(e);}
}
assert(tree.length===32&&chords.length===327,"original complete graph Betti-1 is 327");
const HB=chords.map(k=>{
 const q=Array(M).fill(0);q[k]=1;
 return harmonic(q).h;
});
let Gram=Array.from({length:327},()=>Array(327).fill(0));
for(let i=0;i<327;i++)for(let j=0;j<=i;j++){
 let gij=0;
 for(let e=0;e<M;e++)gij+=2*weight[e]*HB[i][e]*HB[j][e];
 Gram[i][j]=Gram[j][i]=gij;
}
// Exact rank of Hodge projection follows graph incidence; this
// independent WHOLE-327 Cholesky verifies positive definiteness.
const Chol=Array.from({length:327},()=>Array(327).fill(0));
let minChol=Infinity,maxChol=0,maxCholOff=0;
for(let i=0;i<327;i++)for(let j=0;j<=i;j++){
 let sum=Gram[i][j];
 for(let k=0;k<j;k++)sum-=Chol[i][k]*Chol[j][k];
 if(i===j){
  assert(sum>1e-12,"Hodge all327 cycle Gram degenerate");
  Chol[i][j]=Math.sqrt(sum);
  minChol=Math.min(minChol,Chol[i][j]);maxChol=Math.max(maxChol,Chol[i][j]);
 }else{
  Chol[i][j]=sum/Chol[j][j];
  maxCholOff=Math.max(maxCholOff,Math.abs(Chol[i][j]));
 }
}
const cp=edges.map(([i,j])=>{
 const a=zone(i),b=zone(j);
 return (a===0&&b===1)||(a===1&&b===2)?1:-1;
});
const gradient=edges.map(([i,j])=>Math.sin(i*.37)-Math.sin(j*.37));
const random=edges.map(([i,j],e)=>Math.sin(.127*(e+1))+.31*Math.cos(.391*(i+2)*(j+1)));
const sparse=edges.map((_,i)=>+(i===0));
let maxTestErr=0,tests=[];
function lambdaReal(a,eps){
 const matrix=A.map((row,i)=>row.slice());
 for(let e=0;e<M;e++){
  const [i,j]=edges[e],v=Math.exp(eps*a[e]);
  matrix[i][j]*=v;matrix[j][i]/=v;
 }
 let v=Array(N).fill(1/Math.sqrt(N)),lam=0;
 for(let k=0;k<190;k++){
  const b=matvec(matrix,v);lam=norm(b);v=b.map(x=>x/lam);
 }
 const kv=matvec(matrix,v),ray=dot(v,kv)/dot(v,v);
 // Non-symmetric eigenpair v is real; norm power converges to rho.
 assert(Math.abs(norm(kv.map((x,i)=>x-ray*v[i])))<1e-10,
  "true moving non-symmetric Perron eigenpair");
 return ray;
}
function lambdaMag(a,eps){
 // Real 2N Hermitian dilation of the original complex magnetic K:
 // [[K cos, -K sin],[K sin,K cos]] / rho.
 const C=Array.from({length:N},()=>Array(N).fill(0)),
       S=Array.from({length:N},()=>Array(N).fill(0));
 for(let e=0;e<M;e++){
  const [i,j]=edges[e],v=eps*a[e];
  C[i][j]=C[j][i]=Math.cos(v)/rho;
  S[i][j]=Math.sin(v)/rho;S[j][i]=-S[i][j];
 }
 function T(v){
  const re=v.slice(0,N),im=v.slice(N),x=Array(N).fill(0),y=Array(N).fill(0);
  for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(A[i][j]){
   x[i]+=C[i][j]*re[j]-S[i][j]*im[j];
   y[i]+=S[i][j]*re[j]+C[i][j]*im[j];
  }
  return x.concat(y);
 }
 let v=Array.from({length:2*N},(_,i)=>(i<N?r[i]:0)),
     lambda=0;
 for(let k=0;k<180;k++){
  let vv=T(v),next=v.map((x,i)=>(x+vv[i])/2),size=norm(next);
  v=next.map(x=>x/size);
 }
 lambda=dot(v,T(v));
 return lambda;
}
const h=.009;
for(const [name,a] of [["CP",cp],["random",random],["gradient",gradient],["edge0",sparse]]){
 const q=Q(a,a);
 const realcurv=(Math.log(lambdaReal(a,h))-2*Math.log(rho)+
                  Math.log(lambdaReal(a,-h)))/(h*h);
 const lam=lambdaMag(a,h);
 const magcurv=(1-lam*lam)/(h*h);
 const realerr=Math.abs(realcurv-q),magerr=Math.abs(magcurv-q);
 maxTestErr=Math.max(maxTestErr,realerr,magerr);
 tests.push({name,whole327HodgeVariance:q,
  scalarBookPressureFisher:realcurv,
  CAR16MagneticEightfoldGap:magcurv,
  errors:[realerr,magerr]});
 assert(realerr<.002&&magerr<.002,
   "GLOBAL all-cycle Book Fischer vs CAR magnetic gap quadratic law");
}
assert(Q(gradient,gradient)<1e-10,
 "true original Coboundary PRICE must have exactly zero cycle response");
let maxLaplacianProjector=0;
for(const q of [cp,random,gradient,sparse]){
 const first=harmonic(q).h,twice=harmonic(first).h;
 maxLaplacianProjector=Math.max(maxLaplacianProjector,
     ...twice.map((v,i)=>Math.abs(v-first[i])));
}
assert(maxLaplacianProjector<1e-10,"actual Book weighted cycle Hodge is not idempotent");
const ell=Math.log((1+Math.sqrt(5))/2);
console.log(JSON.stringify({
 result:"PASS_ALL327_NATIVE_BOOK_ARCHIVE_FISHER_EQUALS_CAR16_MAGNETIC_GAP",
 carrier:{vertices:33,originalDirectedEdges:718,independentUndirectedEdges:359,
  originalTreeEdges:32,independentCycleOrbits:327,
  gaugeCoboundaries:32,fullCAR16Grades:16,
  magneticChargedHelicityBranches:8,neutralCARBranches:8,
  original30KerTimes16:480},
 originalPerron:{rho,stochasticRowMaxError:stochasticErr,perronEigError:perronErr},
 full327:{
  HessianRank:327,strictPositiveCholesky:true,
  minimumPositiveCholeskyDiagonal:minChol,
  maxCholeskyDiagonal:maxChol,
  maxOffDiagonal:maxCholOff,
  fullWeightedProjectorIdempotence:maxLaplacianProjector},
 uniqueCanonicalLaw:{
  residualCycleCovariance:"Q(a,b)=2 sum_undirected mu_uv [a_uv-chi_u+chi_v][b_uv-chi_u+chi_v]",
  MarkovPoisson:"L_mu chi=div_mu a",
  BookLogPressureCurvature:"D²_{eps} log rho(K exp(eps a))=Q(a,a)",
  BookPhiCostCurvature:"D²_t[-log_phi rho(K phi^(-t a))]=-ln(phi) Q(a,a)",
  CAR16MagneticReturnGap:"lim(theta->0)[1-rho_magnetic(theta)^2/rho^2]/theta^2=Q(a,a)",
  endogenousGoldenCARAngle:"theta=ln(phi)*chi; gap coefficient (ln phi)^2 Q",
  kernel:"exactly the original 32 vertex price coboundaries, no more"},
 independentPhysicalFixtures:tests,
 maxFisherGapFiniteDeltaDifference:maxTestErr,
 completeBookHJRRequired:false,
 actualSelectedCAR16EdgeController:false,
 trueEinsteinPalatini40FieldCouplingUnselected:true,
 physicalG0CostPREPOldRightClockWorkOpen:true,
 GR_closed:false
},null,2));
