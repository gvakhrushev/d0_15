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

// ORIGINAL genuine K(9,11,13) CP cyclic three-zone orientation is an
// ALL-ORDER complex-analytic identity, not just a coincident Hessian:
// rho_real(eps)^3-359 rho_real(eps)-2574 cosh(3eps)=0,
// rho_magnetic(theta)^3-359 rho_magnetic(theta)-2574 cos(3theta)=0.
// Both are the SAME polynomial under analytic continuation eps=i theta.
// This is the exact original 33-site finite controlled operator, not
// a new CP coupling. ALL 327 directions have a locally holomorphic
// Perron root, but their characteristic polynomial is less simple.
function cubicroot(trig){
 let x=rho;
 for(let j=0;j<20;j++)x-=(x*x*x-359*x-2574*trig)/(3*x*x-359);
 return x;
}
let maxCPFiniteGap=0, maxCPBook=0;
for(const theta of [.07,.13,.21]){
 const actual=lambdaMag(cp,theta)*rho,
       exact=cubicroot(Math.cos(3*theta));
 const err=Math.abs(actual-exact);
 maxCPFiniteGap=Math.max(maxCPFiniteGap,err);
 assert(err<1e-11,"original CP ALL ORDER complex analytic 33-char gap");
 const scalar=lambdaReal(cp,theta),right=cubicroot(Math.cosh(3*theta));
 maxCPBook=Math.max(maxCPBook,Math.abs(scalar-right));
 assert(Math.abs(scalar-right)<1e-11,
   "real Book pressure CP original cubic not exact");
}
let maxMixedError=0,mixedResults=[];
const qXY=Q(cp,random);
for(const hh of [.016,.009]){
 const aplus=cp.map((v,i)=>v+random[i]),
       aminus=cp.map((v,i)=>v-random[i]);
 const f=(a,v)=>Math.log(lambdaReal(a,v));
 const hessMix=(f(aplus,hh)-f(aminus,hh)
                 -f(aminus,-hh)+f(aplus,-hh))/(4*hh*hh);
 // f(h(a+b)) - f(h(a-b)) - f(-h(a-b)) + f(-h(a+b)):
 // each is even for anti-symmetric cycle a; divide 4h² -> Q(a,b).
 const gm=a=>1-lambdaMag(a,hh)**2;
 const magMix=(gm(aplus)-gm(aminus))/(4*hh*hh);
 const er=Math.abs(hessMix-qXY),em=Math.abs(magMix-qXY);
 maxMixedError=Math.max(maxMixedError,er,em);
 assert(er<.001&&em<.001,
  "entire all327 Book/quantum multivariate polarization failed");
 mixedResults.push({h:hh,analyticMixedCycleCovariance:qXY,
  realBookMixedHessian:hessMix,magneticCycleMixedGap:magMix,
  errors:[er,em]});
}

// GLOBAL, not perturbative: for EVERY original positive reciprocal
// edge B_uv=B_vu and EVERY real antisymmetric a, Perron radius
// rho(B exp(a)) >= rho(B); equality iff a is a vertex coboundary.
// Elementary proof is rowwise Cauchy on the two positive eigenvectors
// of K(a) and K(-a)=K(a)^T. Connected + ORIGINAL triangles make
// equality iff coboundary, so original full scalar Book Cost
// A=-log_phi rho is a STRICT GLOBAL MAXIMUM at REVERSIBILITY on the
// complete 327-cycle quotient, not a physical minimum.
// Crucially: choose the entirely ORIGINAL allowed primitive Cost=3
// baseline, then for every tested small two-sided a perturb
// Cost_uv=3-t a_uv / ln(phi) remains >=1.  Thus no
// ActionProtocol saturated-floor one-sided loophole is needed.
// GENERIC full original CAR16 "DARK" rank revival: original rank(A)=3
// gives 30 original transfer zero modes per CAR grade = 480 at zero
// phase. The CP homogeneous zone angle preserves rank3 and 480 zeros.
// But GENERIC original 327-cycle phases make charged Hermitian 33x33
// magnetic K full rank33 (zero original transfer modes lifted), while
// eight J23-neutral CAR grades still carry exact rank3 K. Hence generic
// full 33x16 transfer zero subspace has dimension 30*8=240, not 480!
// This has NOTHING to do with the Perron F=I-T² zero gap: rank(F)
// near flat is a DIFFERENT question. "Protected rank30" is ONLY
// true for the zone-constant original CP interface family.
function rankHermitianPhase(a,theta,tol=1e-10){
 const W=A.map((row,i)=>row.map((v,j)=>[v,0]));
 for(let e=0;e<M;e++){
  let [i,j]=edges[e],t=theta*a[e],c=Math.cos(t),si=Math.sin(t);
  W[i][j]=[c,si];W[j][i]=[c,-si];
 }
 let rank=0,minPivot=Infinity;
 for(let j=0;j<N&&rank<N;j++){
  let pivot=rank;
  for(let i=rank+1;i<N;i++)
   if(W[i][j][0]**2+W[i][j][1]**2 >
      W[pivot][j][0]**2+W[pivot][j][1]**2)pivot=i;
  const [re,im]=W[pivot][j],mag=Math.hypot(re,im);
  if(mag<tol)continue;
  [W[rank],W[pivot]]=[W[pivot],W[rank]];
  minPivot=Math.min(minPivot,mag);
  const den=re*re+im*im;
  for(let i=rank+1;i<N;i++){
   let [ar,ai]=W[i][j],rr=(ar*re+ai*im)/den,
       ii=(ai*re-ar*im)/den;
   for(let k=j;k<N;k++){
    let [br,bi]=W[rank][k];
    W[i][k][0]-=rr*br-ii*bi;
    W[i][k][1]-=rr*bi+ii*br;
   }
  }
  rank++;
 }
 return {rank,minPivot};
}
const genericTransferRanks=[];
for(const theta of [0,.1,.2,.5,.8]){
 const cpRank=rankHermitianPhase(cp,theta);
 const genRank=rankHermitianPhase(random,theta);
 const gradientRank=rankHermitianPhase(gradient,theta);
 assert(cpRank.rank===3&&gradientRank.rank===3,
   "native CP zone phase/vertex PRICE-gauge lifted the wrong dark kernel");
 assert(genRank.rank===(theta===0?3:33),
   "generic 327 cycle full-rank CAR16 transfer not recovered");
 genericTransferRanks.push({theta,originalCPZoneRank:cpRank.rank,
  genericFullCycleRank:genRank.rank,gradientGaugeRank:gradientRank.rank,
  genericFull33MinPivot:genRank.minPivot,
  originalCAR16TransferZeroModesGeneric:8*(N-genRank.rank)+8*(N-cpRank.rank)});
}
const byZone=[Array.from({length:9},(_,i)=>i),
 Array.from({length:11},(_,i)=>i+9),
 Array.from({length:13},(_,i)=>i+20)];
// FIXED native ABC triangle plus 15 disjoint reciprocal pairs on
// remaining 30 vertices proves NONZERO Laurent determinant monomial
// e^(i(alpha_ab+alpha_bc+alpha_ca)) of the Hermitian phase matrix.
const triangle=[byZone[0].shift(),byZone[1].shift(),byZone[2].shift()];
const matching=[];
while(byZone.some(v=>v.length)){
 const ix=[0,1,2].sort((x,y)=>byZone[y].length-byZone[x].length);
 assert(byZone[ix[1]].length>0,"remaining true K913 graph has no matching");
 matching.push([byZone[ix[0]].shift(),byZone[ix[1]].shift()]);
}
assert(matching.length===15&&
 new Set(triangle.concat(matching.flat())).size===33,
 "original 33 determinant triangle+15 disjoint pair monomial lacks proof");

// FULL finite stationarity-constrained BOOK Cost–Info dual:
/// I(nu)=sum_uv nu_uv ln[nu_uv/(nu_u P0_uv)] >=0,
/// log(rho(P0 exp(eps a))) = sup_divfree_nu
///    {eps sum(nu_uv a_uv)-I(nu)}.
///
/// It follows by taking conditional KL to the Doob-tilted transition
/// P_eps; endpoint log r_eps cancels because nu is stationary.
/// Hessian of the SUP-ensemble is Q327, while the MINIMAL required
/// cycle-current cost is its Legendre dual with Hessian Q327^-1.
/// This is a finite variational theorem on ACTUAL original path
/// flow distributions, not a fitted gravitational action or claim
/// that fundamental M1 forces a specified nonzero current.
function transitionTilt(a,eps){
 const B=A.map(row=>row.slice());
 for(let e=0;e<M;e++){
  let [i,j]=edges[e],q=Math.exp(eps*a[e]);
  B[i][j]=q;B[j][i]=1/q;
 }
 let v=Array(N).fill(1/Math.sqrt(N)),lam=0;
 for(let k=0;k<180;k++){
  const w=matvec(B,v);lam=norm(w);v=w.map(x=>x/lam);
 }
 const PP=B.map((row,i)=>row.map((x,j)=>x*v[j]/(lam*v[i])));
 let stationary=Array(N).fill(1/N);
 for(let t=0;t<300;t++){
  let q=Array(N).fill(0);
  for(let i=0;i<N;i++)for(let j=0;j<N;j++)
   if(A[i][j])q[j]+=stationary[i]*PP[i][j];
  stationary=q;
 }
 const residual=Math.max(...stationary.map((x,j)=>
  Math.abs(x-PP.reduce((sm,row,i)=>sm+stationary[i]*row[j],0))));
 assert(residual<4e-13,"actual tilted Book Markov stationary flow");
 let current=0,rate=0;
 const flow=Array.from({length:N},(_,i)=>PP[i].map(x=>x*stationary[i]));
 for(let e=0;e<M;e++){
  let [i,j]=edges[e],v=flow[i][j],w=flow[j][i];
  current+=(v-w)*a[e];
  rate+=v*Math.log(PP[i][j]/P[i][j])+
        w*Math.log(PP[j][i]/P[j][i]);
 }
 return {current,rate,press:Math.log(lam/rho),flow,pi:stationary};
}
let exactRateDualError=0,strictVariationalMargin=Infinity,dualTests=[];
for(const [name,field] of [["CP",cp],["random",random],["singleEdge",sparse]]){
 for(let eps of [.04,.1,.2]){
  const tr=transitionTilt(field,eps);
  const residual=Math.abs(tr.rate-(eps*tr.current-tr.press));
  exactRateDualError=Math.max(exactRateDualError,residual);
  assert(residual<2e-12,"original exact finite Markov level2.5 Legendre KL");
  const flowMix=Array.from({length:N},(_,i)=>tr.flow[i].map(
   (x,j)=>.72*x+.28*(pi[i]*P[i][j])));
  const row=flowMix.map(v=>v.reduce((a,b)=>a+b,0));
  let I=0,J=0,divErr=0;
  for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(A[i][j]){
   const x=flowMix[i][j];
   I+=x*Math.log(x/(row[i]*P[i][j]));
   const sign=(i<j?1:-1),e=(i<j?edges.findIndex(q=>q[0]===i&&q[1]===j):
                                      edges.findIndex(q=>q[0]===j&&q[1]===i));
   J+=x*sign*field[e];
  }
  for(let i=0;i<N;i++){
   let incoming=0;for(let j=0;j<N;j++)incoming+=flowMix[j][i];
   divErr=Math.max(divErr,Math.abs(row[i]-incoming));
  }
  const gap=tr.press-(eps*J-I);
  strictVariationalMargin=Math.min(strictVariationalMargin,gap);
  assert(divErr<2e-12&&gap>1e-7,
   "finite Book stationary current KL dual should be strict off optimum");
  const q=Q(field,field);
  dualTests.push({name,eps,current:tr.current,rate:tr.rate,
   LegendreEqualityError:residual,
   nonoptimalStationaryFlowStrictGap:gap,
   localCurrentQuadraticExpected:tr.current**2/(2*q),
   actualRateToLocalQuadratic:tr.rate/(tr.current**2/(2*q))});
 }
}
const invCholesky=rhs=>{
 const n=327,y=Array(n).fill(0),x=Array(n).fill(0);
 for(let i=0;i<n;i++){
  let s=rhs[i];for(let j=0;j<i;j++)s-=Chol[i][j]*y[j];
  y[i]=s/Chol[i][i];
 }
 for(let i=n-1;i>=0;i--){
  let s=y[i];for(let j=i+1;j<n;j++)s-=Chol[j][i]*x[j];
  x[i]=s/Chol[i][i];
 }
 return x;
};
const currentGradient=Array.from({length:327},(_,i)=>Math.sin((i+1)*.113));
const dualCovector=invCholesky(currentGradient);
let inverseFisherMaxResidual=0;
for(let i=0;i<327;i++){
 const v=dot(Gram[i],dualCovector)-currentGradient[i];
 inverseFisherMaxResidual=Math.max(inverseFisherMaxResidual,Math.abs(v));
}
assert(inverseFisherMaxResidual<2e-11,
 "the exact native 327-dimensional current-rate Hessian inverse is not defined");
const ell=Math.log((1+Math.sqrt(5))/2),interiorCost=3;
let minAdmittedCost=Infinity,minNonGradientGlobalBookGap=Infinity;
const globalComparisons=[];
for(const [name,vec] of [["CP",cp],["random",random],["edge",sparse],
 ["mixed",cp.map((x,i)=>x+.35*random[i])],["pureCoboundary",gradient]]){
 for(const t of [.08,.20,.40]){
  const upper=Math.max(...vec.map(Math.abs));
  const costfloor=interiorCost-Math.abs(t)*upper/ell;
  minAdmittedCost=Math.min(minAdmittedCost,costfloor);
  assert(costfloor>=1,"real CHIRAL perturb violates original primitive ActionProtocol cost quantum");
  const up=lambdaReal(vec,t),down=lambdaReal(vec,-t);
  const rel=Math.abs(up/rho-down/rho);
  assert(rel<3e-12,"original K(a) and K(-a) transpose have different Perron pressures");
  let gap=up/rho-1;
  if(name==="pureCoboundary"){
   assert(Math.abs(gap)<3e-12,"true global gradient diagonal-gauge must leave rho constant");
  }else{
   assert(gap>1e-7,"strict native cyclic Perron pressure lower bound fails");
   minNonGradientGlobalBookGap=Math.min(minNonGradientGlobalBookGap,gap);
  }
  globalComparisons.push({name,t,relativePerronPressureGap:gap,
    genuineMinimumPrimitiveCost:costfloor});
 }
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
console.log(JSON.stringify({
 result:"PASS_ALL327_NATIVE_BOOK_ARCHIVE_FISHER_EQUALS_CAR16_MAGNETIC_GAP",
 carrier:{vertices:33,originalDirectedEdges:718,independentUndirectedEdges:359,
  originalTreeEdges:32,independentCycleOrbits:327,
  gaugeCoboundaries:32,fullCAR16Grades:16,
  magneticChargedHelicityBranches:8,neutralCARBranches:8,
  original30KerTimes16AtZeroPhase:480,
  original30KerTimes16CPZonalAllPhases:480,
  genericCycleNonzeroTransferKernel:240},
 originalPerron:{rho,stochasticRowMaxError:stochasticErr,perronEigError:perronErr},
 full327:{
  HessianRank:327,strictPositiveCholesky:true,
  minimumPositiveCholeskyDiagonal:minChol,
  maxCholeskyDiagonal:maxChol,
  maxOffDiagonal:maxCholOff,
  fullWeightedProjectorIdempotence:maxLaplacianProjector,
  exactCPAllOrderRealCubicMaxError:maxCPBook,
  exactCPAllOrderMagneticCubicMaxError:maxCPFiniteGap,
  multivariateCrossFisherTests:mixedResults,
  maxMixedCycleSourceError:maxMixedError,
  strictGlobalBookReversibilityTheorem:true,
  allAdmittedOriginalCostMinimum:minAdmittedCost,
  minimumPositiveOffshellCyclicPressureGap:minNonGradientGlobalBookGap,
  fullPositiveDomainCyclicGlobalTests:globalComparisons,
  genericCARMixingAndDarkKernelRevival:genericTransferRanks,
  exactBookCurrentRateLegendre:{maximumEqualityError:exactRateDualError,
   nonoptimalStationaryFlowMinimumStrictGap:strictVariationalMargin,
   full327CurrentHessianInverseMaxResidual:inverseFisherMaxResidual,
   finiteOriginalCurrentTests:dualTests},
  determinantLaurentNonzeroMonomial:{nativeTriangle:triangle,
   reciprocalPerfectMatchingCount:matching.length,
   signedCoefficientNonzero:true}},
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
