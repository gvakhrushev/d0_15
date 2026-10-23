#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL D0 K(9,11,13), 33 vertices, 718 directed primitive edges.
 * STRICT POSITIVE actual Perron / Doob P, pi, mu from a permitted
 * heterogeneous native unit-floor primitive Cost>=1.
 *
 * Exact ALL-STEP Markov statistical theorem:
 * I_complete_path(n edges) = I_stationary_pi + n I_conditional_transition
 * (initial score + Markov martingale increments are orthogonal).
 * I_stationary_edge_mu = I_pi + I_transition.
 *
 * Canonical 685D Markov Jeffreys Fisher volume:
 * sqrt(det I_transition) = PROD_u pi_u^((d_u-1)/2)
 *                           PROD_(uv edge) P_uv^(-1/2).
 * A naive rowwise-independent KT prior omits pi factors and can retain
 * a nonzero vertex-source even after long natural coding.
 *
 * EXACT analytic determinant/score identities + numerical ORIGINAL
 * complete 15,708 positive two-edge full-path replays.
 * NO compulsory G0/Book03/M1 history action/coding prior/GR promotion.
 */
const assert=(ok,msg)=>{if(!ok)throw Error("FAIL: "+msg)};
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),N=33;
const zone=u=>u<9?0:u<20?1:2;
const K=Array.from({length:N},(_,u)=>Array.from({length:N},(_,v)=>
 zone(u)===zone(v)?0:
 Math.exp(-ell*(1.12+.023*((7*u+11*v)%13)))));
const neighbors=Array.from({length:N},(_,u)=>Array.from({length:N},(_,v)=>K[u][v]>0?v:-1).filter(v=>v>=0));
const degrees=neighbors.map(r=>r.length);
assert(K.flat().filter(x=>x>0).length===718,"true original 718 strict positive edges");
assert(degrees.slice(0,9).every(x=>x===24)&&degrees.slice(9,20).every(x=>x===22)
 &&degrees.slice(20).every(x=>x===20),"true original zone degrees 24/22/20");
const dimension=degrees.reduce((s,d)=>s+d-1,0);
assert(dimension===9*23+11*21+13*19&&dimension===685,"exact original Markov shape/source dimension 685");
const transpose=A=>A[0].map((_,i)=>A.map(row=>row[i]));
function Perron(A){
 let ray=Array(N).fill(1/N),lambda=0;
 for(let step=0;step<900;step++){
  const v=A.map(row=>row.reduce((s,x,j)=>s+x*ray[j],0)),
    sum=v.reduce((s,x)=>s+x,0);
  ray=v.map(x=>x/sum);
 }
 const ar=A.map(row=>row.reduce((s,x,j)=>s+x*ray[j],0));
 lambda=ar.reduce((s,x,i)=>s+x*ray[i],0)/ray.reduce((s,x)=>s+x*x,0);
 assert(Math.max(...ar.map((x,i)=>Math.abs(x-lambda*ray[i])))<2e-12,
   "real native PF convergence");
 return {lambda,ray};
}
function native(A){
 const R=Perron(A),L=Perron(transpose(A));
 assert(Math.abs(R.lambda-L.lambda)<2e-12,"actual left/right Perron agree");
 const product=R.ray.reduce((s,x,i)=>s+x*L.ray[i],0);
 const pi=R.ray.map((x,i)=>x*L.ray[i]/product);
 const P=A.map((row,u)=>row.map((x,v)=>x*R.ray[v]/(R.lambda*R.ray[u])));
 const mu=P.map((row,u)=>row.map(x=>pi[u]*x));
 assert(Math.max(...P.map(row=>Math.abs(row.reduce((s,x)=>s+x,0)-1)))<2e-12,
  "original Doob row normalization");
 assert(Math.max(...pi.map((x,j)=>Math.abs(P.reduce((s,row,i)=>s+pi[i]*row[j],0)-x)))<2e-12,
  "native stationary true preparation");
 return {lambda:R.lambda,pi,P,mu};
}
const native0=native(K);
const tangent=K.map((row,u)=>row.map((x,v)=>x>0?
 Math.sin((13*u+7*v+1)/9)+.25*Math.cos((u-4*v)/6):0));
const dt=1e-5;
const perturb=t=>K.map((row,u)=>row.map((x,v)=>x*Math.exp(-ell*t*tangent[u][v])));
const plus=native(perturb(dt)),minus=native(perturb(-dt));
const dpi=native0.pi.map((v,i)=>(plus.pi[i]-minus.pi[i])/(2*dt));
const dP=native0.P.map((row,u)=>row.map((x,v)=>(plus.P[u][v]-minus.P[u][v])/(2*dt)));
const dmu=native0.mu.map((row,u)=>row.map((x,v)=>(plus.mu[u][v]-minus.mu[u][v])/(2*dt)));
assert(Math.abs(dpi.reduce((s,x)=>s+x,0))<2e-10,
 "original moving pi score sums exactly to zero");
assert(Math.max(...dP.map(row=>Math.abs(row.reduce((s,x)=>s+x,0))))<2e-10,
 "real moving original P scores zero in each one of 33 native rows");
let Ipi=0,Icond=0,Iedge=0;
for(let u=0;u<N;u++){
 Ipi+=dpi[u]**2/native0.pi[u];
 for(let v of neighbors[u]){
  Icond+=native0.pi[u]*dP[u][v]**2/native0.P[u][v];
  Iedge+=dmu[u][v]**2/native0.mu[u][v];
 }
}
assert(Ipi>1e-7&&Icond>1e-4,"original heterogeneous two-sided field changes both stationary and conditional source");
assert(Math.abs(Iedge-Ipi-Icond)<2e-8,
 "WHOLE original 718-edge Fisher = vertex32 + conditional Markov685 EXACT");

let npaths=0,FI2=0,FI0=0,positiveMass=0;
for(let u=0;u<N;u++){
 const sp=dpi[u]/native0.pi[u];
 FI0+=native0.pi[u]*sp**2;
 for(let v of neighbors[u]){
  const su=dP[u][v]/native0.P[u][v];
  for(let w of neighbors[v]){
   const sw=dP[v][w]/native0.P[v][w];
   const prob=native0.pi[u]*native0.P[u][v]*native0.P[v][w];
   FI2+=prob*(sp+su+sw)**2;
   positiveMass+=prob;npaths++;
  }
 }
}
assert(npaths===15708&&Math.abs(positiveMass-1)<1e-12,
 "ALL 15,708 original complete two-step Markov histories retained and normalized");
assert(Math.abs(FI0-Ipi)<2e-12&&Math.abs(FI2-Ipi-2*Icond)<3e-8,
 "EXACT original 15,708 native full-path Fisher = I_pi + 2 I_cond");

function rowBlockLogdet(row,u){
 const d=neighbors[u].length,m=d-1;
 const Irow=Array.from({length:m},(_,i)=>Array.from({length:m},(_,j)=>
  native0.pi[u]*((i===j?1/native0.P[u][neighbors[u][i]]:0)
               +1/native0.P[u][neighbors[u][d-1]])));
 // Direct all-positive finite Gaussian determinant of original true
 // (d-1)x(d-1) multinomial Fisher, independent of matrix determinant lemma.
 let val=0;
 for(let i=0;i<m;i++){
  let k=i;for(let j=i+1;j<m;j++)if(Math.abs(Irow[j][i])>Math.abs(Irow[k][i]))k=j;
  if(i!==k){[Irow[i],Irow[k]]=[Irow[k],Irow[i]];}
  const a=Irow[i][i];
  assert(a>0,"each original row Fisher is positive definite");
  val+=Math.log(a);
  for(let j=i+1;j<m;j++){
   const frac=Irow[j][i]/a;
   for(let h=i+1;h<m;h++)Irow[j][h]-=frac*Irow[i][h];
  }
 }
 const formula=m*Math.log(native0.pi[u])-
  neighbors[u].reduce((s,v)=>s+Math.log(native0.P[u][v]),0);
 assert(Math.abs(val-formula)<2e-9,
  "direct literal original row Fisher determinant equals Markov Jeffreys closed formula");
 return formula;
}
const rowLogdet=degrees.map((_,u)=>rowBlockLogdet(native0.P[u],u));
const logDet=rowLogdet.reduce((s,x)=>s+x,0);
function logJeffreys(data){
 let vertex=0,edge=0;
 for(let u=0;u<N;u++){
  vertex+=(degrees[u]-1)*Math.log(data.pi[u]);
  for(let v of neighbors[u])edge-=Math.log(data.P[u][v]);
 }
 return {logPriorHalf:(vertex+edge)/2, vertexHalf:vertex/2,rowHalf:edge/2};
}
const J=logJeffreys(native0),Jp=logJeffreys(plus),Jm=logJeffreys(minus);
assert(Math.abs(logDet-2*J.logPriorHalf)<2e-9,
 "full REAL 685-dimensional original Markov Fisher volume is exactly native Jeffreys measure");
const dVertex=(Jp.vertexHalf-Jm.vertexHalf)/(2*dt);
const dRow=(Jp.rowHalf-Jm.rowHalf)/(2*dt);
const dFull=(Jp.logPriorHalf-Jm.logPriorHalf)/(2*dt);
assert(Math.abs(dVertex)>1e-5&&Math.abs(dFull-dRow-dVertex)<2e-8,
 "rowwise independent KT MISSES a genuinely nonzero native stationary-vertex first source");

// Original positive endpoint gauge AND global absolute Perron shift
// leave the entire native 685-dimensional P, pi and canonical J unchanged.
const q=Math.pow(1/p,.23);
const D=Array.from({length:N},(_,u)=>1+((u*u)%17)/23);
const Kgauge=K.map((row,u)=>row.map((x,v)=>x*q*D[u]/D[v]));
const Ng=native(Kgauge),Jg=logJeffreys(Ng);
const maxP=Math.max(...native0.P.flatMap((row,u)=>row.map((x,v)=>Math.abs(x-Ng.P[u][v]))));
assert(maxP<2e-12&&Math.abs(Jg.logPriorHalf-J.logPriorHalf)<1e-10,
 "complete Markov Jeffreys code prior is intrinsic to Doob history, not absolute Book pressure");
const expectedGammaDim=dimension/2;
assert(expectedGammaDim===342.5&&
 Math.abs(J.logPriorHalf-(J.vertexHalf+J.rowHalf))<1e-12,
 "native 685/2 logarithmic Fisher volume and 32-vertex preparation factor");



// Strongest ORIGINAL source constructive step: stationary pi is recovered
// from 33 TRUE directed spanning-tree cofactors of I−P^T, with NO
// separately postulated vertex source. This recovers the missing 32
// Jeffreys preparation coordinates as explicit native transition
// polynomials (the Markov-chain tree theorem, not an Einstein postulate).
function stationaryFromRootedTrees(P){
 const Lap=Array.from({length:N},(_,u)=>Array.from({length:N},(_,v)=>
   (u===v?1:0)-P[v][u]));
 const logWeights=[];
 for(let root=0;root<N;root++){
  const S=Lap.filter((_,u)=>u!==root).map(row=>row.filter((_,v)=>v!==root));
  const m=N-1;let lg=0,sgn=1;
  for(let k=0;k<m;k++){
   let r=k;for(let i=k+1;i<m;i++)if(Math.abs(S[i][k])>Math.abs(S[r][k]))r=i;
   assert(Math.abs(S[r][k])>1e-15,
    "TRUE original directed tree minor is nonsingular at every vertex");
   if(r!==k){[S[r],S[k]]=[S[k],S[r]];sgn=-sgn;}
   const piv=S[k][k];sgn*=Math.sign(piv);lg+=Math.log(Math.abs(piv));
   for(let i=k+1;i<m;i++){
    const scale=S[i][k]/piv;
    for(let j=k+1;j<m;j++)S[i][j]-=scale*S[k][j];
   }
  }
  assert(sgn>0,"original irreducible Markov rooted arborescence cofactor POSITIVE");
  logWeights.push(lg);
 }
 const m=Math.max(...logWeights),tau=logWeights.map(x=>Math.exp(x-m)),
   total=tau.reduce((a,b)=>a+b,0);
 return tau.map(x=>x/total);
}
const piTrees=stationaryFromRootedTrees(native0.P),
      piTreesPlus=stationaryFromRootedTrees(plus.P),
      piTreesMinus=stationaryFromRootedTrees(minus.P);
const treePiErr=Math.max(...piTrees.map((x,u)=>Math.abs(x-native0.pi[u])));
const treeScoreErr=Math.max(...dpi.map((x,u)=>
 Math.abs(x-(piTreesPlus[u]-piTreesMinus[u])/(2*dt))));
assert(treePiErr<3e-12&&treeScoreErr<5e-9,
 "all 33 original stationary probabilities and their MOVING source recovered from original rooted spanning tree sums");
const treeVertexSource=native0.pi.reduce((acc,_,u)=>acc+
 .5*(degrees[u]-1)*
  (Math.log(piTreesPlus[u])-Math.log(piTreesMinus[u]))/(2*dt),0);
assert(Math.abs(treeVertexSource-dVertex)<2e-7,
 "the TRUE native 32-mode vertex Jeffreys first source is a finite original transition TREE current, no separate pi oracle");

// FULL FORWARD-ONLY original supported Markov KT prediction: a fixed,
// integer-count online decoder for genuine 718 native allowed transitions.
// This ROW independent online baseline is a valid complete Markov code
// but is NOT the proper Markov Jeffreys joint prior: latter has extra
// moving rooted-tree factor pi^((degree−1)/2), certified above.
const liveCount=Array.from({length:N},()=>Array(N).fill(0));
const rowTotal=Array(N).fill(0),testEdges=512;let place=0,onlineMarkovLog=0;
for(let step=0;step<testEdges;step++){
 const next=neighbors[place][(step*7+place)%degrees[place]];
 const prob=(liveCount[place][next]+.5)/
            (rowTotal[place]+degrees[place]/2);
 assert(prob>0&&prob<1,"real original Book supported edge KT prediction strictly positive");
 onlineMarkovLog+=Math.log(prob);
 liveCount[place][next]++;rowTotal[place]++;place=next;
}
const LF=[0],LH=[.5*Math.log(Math.PI)];
for(let k=1;k<testEdges+15;k++){
 LF[k]=LF[k-1]+Math.log(k);
 LH[k]=LH[k-1]+Math.log(k-.5);
}
let markovMixtureLog=0;
for(let u=0;u<N;u++){
 const a=degrees[u]/2; // native d_u=24/22/20, so a=12/11/10 INTEGER
 markovMixtureLog+=LF[a-1]-LF[a+rowTotal[u]-1];
 for(const v of neighbors[u])markovMixtureLog+=LH[liveCount[u][v]]-LH[0];
}
assert(Math.abs(onlineMarkovLog-markovMixtureLog)<2e-9,
 "TRUE all718 supported Book Markov forward KT path code EXACT equals fixed independent-row Dirichlet half-mixture");
const onlineOriginalBook={
 steps:testEdges,initialOriginalVertex:0,finalOriginalVertex:place,
 fullyRetainedOriginalRowCounts:rowTotal,
 completeForwardGoldenUnitCode:-onlineMarkovLog/Math.log(1/p),
 onlineMixtureResidual:onlineMarkovLog-markovMixtureLog};
// THE TRUE 718×17 = 12,206 full mathematical single-transition native
// BOOK+GOLDEN complete event labels. Here one scalar geometric source moves
// BOTH genuine original Book Cost and ORIGINAL native Golden J23 mark.
// Conditional Born law retains ALL Bell failures and signed +/- metadata.
// Fisher splits exactly into vertex-π + transition-P + Golden-CAR channels;
// this does NOT pick a compulsory G0 Book H+J+R action or erase Q8 spin.
const golden=(t)=>{
 const p=(Math.sqrt(5)-1)/2,h=1/4096;
 const avg=(1+Math.cos(t))/2,ss=Math.sin(t)/Math.SQRT2;
 const marks=[];
 for(let axis=0;axis<6;axis++){
  const s=axis===4?ss:0;
  marks.push(h*p**4/24*(avg+s)**2,h*p**4/24*(avg-s)**2);
 }
 const norm=p**4,gb=p*p*(1-p*p),bg=p**3;
 marks.push(h*(norm-marks.reduce((a,b)=>a+b,0)/h),h*gb,h*bg,
            h*(1-norm-gb-bg),1-h);
 assert(marks.length===17&&marks.every(x=>x>0)&&
    Math.abs(marks.reduce((a,b)=>a+b,0)-1)<1e-13,
    "full original native Golden17 records include every Bell FAILURE category");
 return marks;
};
const gold0=golden(0),goldP=golden(dt),goldM=golden(-dt),
 dGolden=gold0.map((q,i)=>(goldP[i]-goldM[i])/(2*dt));
const IGolden=gold0.reduce((sum,q,i)=>sum+dGolden[i]**2/q,0);
const exactGoldenOne=p**4/(4096*6);
assert(Math.abs(IGolden-exactGoldenOne)<1e-11,
 "original complete two-fresh Golden17 finite score Fisher equals true p^4/(6*4096)");
let full12206Fisher=0,full12206Mass=0,full12206MeanScore=0,positiveFull=0;
for(let u=0;u<N;u++)for(let v of neighbors[u]){
 const history=native0.pi[u]*native0.P[u][v];
 const sHistory=dpi[u]/native0.pi[u]+dP[u][v]/native0.P[u][v];
 for(let k=0;k<17;k++){
  const Q=history*gold0[k],source=sHistory+dGolden[k]/gold0[k];
  full12206Fisher+=Q*source**2;
  full12206Mass+=Q;
  full12206MeanScore+=Q*source;
  positiveFull++;
 }
}
assert(positiveFull===12206&&Math.abs(full12206Mass-1)<2e-12&&
 Math.abs(full12206MeanScore)<2e-10,
 "ALL original 718x17 native-type joint positive labels have unit total mass and zero score mean");
assert(Math.abs(full12206Fisher-(Ipi+Icond+IGolden))<3e-8,
 "TRIPLE ORIGINAL 12206-source FISHER CHAIN: vertex32 + Doob685 + Golden17 exactly");
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_718_MARKOV_FISHER_JEFFREYS_SOURCE_GEOMETRY",
 native:{vertices:33,directedEdges:718,parameterDimension:dimension,
  siteDegrees:{A:24,B:22,C:20},exactOriginalCompleteTwoStepPaths:npaths,
  normalizedTwoStepPathMass:positiveMass,absolutePerronLambda:native0.lambda},
 exactFisher:{movingStationaryVertex32:Ipi,conditionalTransition685:Icond,
  wholeStationaryEdge685:Iedge,originalCompleteTwoStepHistory:FI2,
  exactPathDifference:FI2-(Ipi+2*Icond),exactOneStepDifference:Iedge-Ipi-Icond,
  completeOriginalBookGoldenLabels:positiveFull,
  fullBookGoldenJointFisher:full12206Fisher,
  trueGolden17ConditionalFisher:IGolden,
  fullTripleSourceDefect:full12206Fisher-Ipi-Icond-IGolden},
 Jeffreys:{halfLogDetNative685:J.logPriorHalf,explicitRowDetSumHalf:logDet/2,
  stationaryVertexFisherLogPrior:J.vertexHalf,
  naiveIndependentKTrowLogPrior:J.rowHalf,
  missingRowwiseMovingVertexFirstSource:dVertex,
  naiveRowwiseMovingFirstSource:dRow,correctMovingFirstSource:dFull,
  gaugeCovariantLogPriorDifference:Jg.logPriorHalf-J.logPriorHalf,
  all33RootedTreeStationaryProbabilityError:treePiErr,
  all33RootedTreeDerivativeError:treeScoreErr,
  rootedTreeVertexJeffreysFirstSource:treeVertexSource,
  realOriginalBookOnlineKTPredictor:onlineOriginalBook,
  universalCodingLogNSlope:expectedGammaDim},
 note:"per-step Fisher exact. Markov Jeffreys prior canonical volume, asymptotic coding source C2 requires independently controlled uniform Markov mixture approximation; not compulsory native G0/Book selected action",
 GR_closed:false
},null,2));
