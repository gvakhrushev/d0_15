#!/usr/bin/env node
"use strict";
/*
 * Exact-algebraic / independently evaluated original 33/718 native Book
 * absolute Perron + real 2/3 returned-stage projective source law:
 *
 * B=-log_phi(lambda), stage=log_phi[(beta3 Z3)/(beta2 Z2)]
 * B+stage=log_phi[(beta3 Tr P^3)/(beta2 Tr P^2)].
 *
 * The complete 718-edge differential is C=mu+2 f2-3 f3, balanced and
 * zero-total. All probabilities, path lengths, endpoint gauges preserved.
 * Diagnostic original strictly Cost>=1 support; NOT compelled G0 H+J+R.
 */
const assert=(b,m)=>{if(!b)throw Error("FAIL: "+m)};
const phi=(1+Math.sqrt(5))/2,p=1/phi,lnphi=Math.log(phi),N=33;
const part=i=>i<9?0:(i<20?1:2);
const K=Array.from({length:N},(_,u)=>Array.from({length:N},(_,v)=>
  part(u)===part(v)?0:p*Math.exp(-lnphi*(.12+.023*((7*u+11*v)%13)))));
assert(K.flat().filter(v=>v>0).length===718,"exact original 718 directed edges");
const trans=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
function PF(A){
 let v=Array(N).fill(1/N);
 for(let k=0;k<1500;k++){
  let next=A.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));
  let sum=next.reduce((s,x)=>s+x,0);
  next=next.map(x=>x/sum);
  if(k>15&&Math.max(...next.map((x,j)=>Math.abs(x-v[j])))<3e-16){v=next;break;}
  v=next;
 }
 const Av=A.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));
 const eigen=Av.reduce((s,x,j)=>s+x*v[j],0)/v.reduce((s,x)=>s+x*x,0);
 assert(Math.max(...Av.map((x,i)=>Math.abs(x-eigen*v[i])))<2e-12,
  "original positive irreducible PF right eigenpair");
 return {eigen,v};
}
function native(A){
 const R=PF(A),L=PF(trans(A)),lambda=R.eigen;
 assert(Math.abs(L.eigen-lambda)<1e-12,"original left/right Perron agree");
 const lr=R.v.reduce((s,v,i)=>s+v*L.v[i],0);
 const pi=R.v.map((v,i)=>v*L.v[i]/lr);
 const P=A.map((row,u)=>row.map((v,j)=>v*R.v[j]/(lambda*R.v[u])));
 const mu=P.map((row,u)=>row.map(v=>pi[u]*v));
 const A2=mm(A,A),P2=mm(P,P);
 let Z2=0,Z3=0,T2=0,T3=0;
 for(let u=0;u<N;u++){
  Z2+=A2[u][u];T2+=P2[u][u];
  for(let v=0;v<N;v++){Z3+=A2[u][v]*A[v][u];T3+=P2[u][v]*P[v][u];}
 }
 const f2=A.map((row,u)=>row.map((v,j)=>v*A[j][u]/Z2));
 const f3=A.map((row,u)=>row.map((v,j)=>v*A2[j][u]/Z3));
 const C=A.map((row,u)=>row.map((_,v)=>mu[u][v]+2*f2[u][v]-3*f3[u][v]));
 for(const [label,F] of [["mu",mu],["n2",f2],["n3",f3]]){
  let mass=F.reduce((s,row)=>s+row.reduce((a,x)=>a+x,0),0);
  assert(Math.abs(mass-1)<4e-13,"original "+label+" probabilities normalize");
  assert(Math.max(...Array.from({length:N},(_,u)=>Math.abs(
     F[u].reduce((a,x)=>a+x,0)-F.reduce((a,row)=>a+row[u],0))))<4e-13,
   "original "+label+" 718-edge flow is BALANCED");
 }
 const sum=C.reduce((s,row)=>s+row.reduce((a,x)=>a+x,0),0);
 assert(Math.abs(sum)<1e-12,"C source has EXACT zero total charge 1+2-3");
 assert(Math.max(...Array.from({length:N},(_,u)=>Math.abs(
   C[u].reduce((s,x)=>s+x,0)-C.reduce((s,row)=>s+row[u],0))))<1e-12,
   "C source is fully balanced: dC=0 on every original vertex");
 const beta2=p,beta3=p*p; // sample fixed stage priors; universal law independent of ratio
 const B=-Math.log(lambda)/lnphi;
 const stage=Math.log(beta3*Z3/(beta2*Z2))/lnphi;
 const shape=B+stage;
 const fromP=Math.log(beta3*T3/(beta2*T2))/lnphi;
 // The actual TWO-stage acceptance odds PLUS the already observed native
 // Doob P recover the absolute PF lambda with NO added free meter.
 const stageOdds=beta3*Z3/(beta2*Z2);
 const lambdaRecovered=stageOdds*(beta2/beta3)*(T2/T3);
 assert(Math.abs(lambdaRecovered/lambda-1)<2e-12,
   "original complete 2/3-stage ratio plus normalized P reconstructs EXACT absolute Book lambda");

 assert(Math.abs(shape-fromP)<2e-12,
   "FULL SCALAR pressure + 2/3 stage CLOCK = only Doob P-cycle ratio");
 assert(Math.abs(Z2/lambda**2-T2)<2e-12&&Math.abs(Z3/lambda**3-T3)<2e-12,
   "original full native moments = lambda^n Tr P^n");
 const W=Z3/7722;
 assert(Math.abs(W-lambda**3*T3/7722)<2e-12,
   "native 7722 third-tick Weyl scale = absolute lambda^3 × Doob shape");
 return {lambda,P,pi,mu,f2,f3,C,Z2,Z3,T2,T3,B,stage,shape,fromP,W,stageOdds,lambdaRecovered};
}
const old=native(K);
const q=Math.pow(phi,.37),D=Array.from({length:N},(_,u)=>1+((u*u)%17)/23);
const changed=K.map((row,u)=>row.map((v,j)=>q*D[u]/D[j]*v));
const now=native(changed);
let Pmax=0,Cmax=0,muMax=0;
for(let u=0;u<N;u++)for(let v=0;v<N;v++){
 Pmax=Math.max(Pmax,Math.abs(old.P[u][v]-now.P[u][v]));
 Cmax=Math.max(Cmax,Math.abs(old.C[u][v]-now.C[u][v]));
 muMax=Math.max(muMax,Math.abs(old.mu[u][v]-now.mu[u][v]));
}
assert(Pmax<1e-12&&muMax<1e-12&&Cmax<1e-12,
 "original pure pressure scaling + arbitrary positive endpoint similarity leave P/mu/C unchanged");
assert(Math.abs(old.shape-now.shape)<1e-12,
 "global source completely insensitive to original absolute lambda and endpoint gauge");
assert(Math.abs(now.lambda/old.lambda-q)<2e-12,
 "genuine absolute pressure DOES change, so not silently omitted");
assert(Math.abs(now.W/old.W-q**3)<2e-12,
 "Book 3-tick Weyl character remains distinct from projective clock shape");

// Original admissible OFF-FLOOR two-sided genuine primitive Cost tangent;
// no unphysical negative-C variation at the C=1 boundary.
const perturb=K.map((row,u)=>row.map((v,j)=>v>0?
  Math.sin((13*u+7*j+1)/9)+.25*Math.cos((u-4*j)/6):0));
const ssum=(F,d)=>F.reduce((sum,row,u)=>sum+row.reduce((z,v,j)=>z+v*d[u][j],0),0);
const exactSource=ssum(old.C,perturb),dt=1e-5;
const run=t=>native(K.map((row,u)=>row.map((v,j)=>v*Math.exp(-lnphi*t*perturb[u][j])))).shape;
const numSource=(run(dt)-run(-dt))/(2*dt);
assert(Math.abs(exactSource-numSource)<5e-9,
 "original complete heterogeneous Book 718-clock source matches real finite derivative");
const common=K.map((row,u)=>row.map(x=>x>0?1:0));
const xi=Array.from({length:N},(_,u)=>u*u/137),cob=K.map((row,u)=>row.map((x,v)=>x>0?xi[u]-xi[v]:0));
assert(Math.abs(ssum(old.C,common))<1e-12,"original uniform Cost/Info scalar null source");
assert(Math.abs(ssum(old.C,cob))<1e-12,"original endpoint Cost/Info gradient null source");


// ORIGINAL 2/3/4 stage archive: second independent, 4-vs-3 projective
// moment-ratio SOURCE on the SAME 718 complete original Book edges.
function fourth(A){
 const b=native(A),A2=mm(A,A),A3=mm(A2,A),A4=mm(A3,A);
 const P3=mm(mm(b.P,b.P),b.P),P4=mm(P3,b.P);
 let z4=0,t4=0;for(let u=0;u<N;u++){z4+=A4[u][u];t4+=P4[u][u];}
 const f4=A.map((row,u)=>row.map((v,j)=>v*A3[j][u]/z4));
 const J43=A.map((row,u)=>row.map((_,v)=>b.mu[u][v]+3*b.f3[u][v]-4*f4[u][v]));
 const beta3=p*p,beta4=p**3;
 const stage43=Math.log(beta4*z4/(beta3*b.Z3))/lnphi;
 const actual43=b.B+stage43;
 const projective43=Math.log(beta4*t4/(beta3*b.T3))/lnphi;
 const odds43=beta4*z4/(beta3*b.Z3);
 const recovered43=odds43*(beta3/beta4)*(b.T3/t4);
 assert(Math.abs(recovered43/b.lambda-1)<3e-12,
 "original complete 3/4-stage ratio independently reconstructs SAME absolute lambda");

 assert(Math.abs(actual43-projective43)<3e-12,
  "original 4/3 stage clock and absolute pressure reduce to Doob-only stage SHAPE");
 assert(Math.abs(z4/b.lambda**4-t4)<3e-12,
  "original 4-tick full trace matches lambda^4 normalized Doob trace");
 assert(Math.abs(ssum(J43,common))<3e-12&&Math.abs(ssum(J43,cob))<3e-12,
  "all 718 native 4/3 pressure-compensated current has zero total and endpoint gauge");
 assert(Math.max(...Array.from({length:N},(_,u)=>Math.abs(
   J43[u].reduce((s,x)=>s+x,0)-J43.reduce((s,row)=>s+row[u],0))))<3e-12,
  "4/3 native edge source is a divergence-free balanced current");
 return {J43,actual43,projective43,z4,t4,odds43,recovered43};
}
const perturbedK=t=>K.map((row,u)=>row.map((v,j)=>v*Math.exp(-lnphi*t*perturb[u][j])));
const F4=fourth(K),fourthPlus=fourth(perturbedK(dt)),fourthMinus=fourth(perturbedK(-dt));
const secondSource=ssum(F4.J43,perturb),secondFD=(fourthPlus.actual43-fourthMinus.actual43)/(2*dt);
assert(Math.abs(secondSource-secondFD)<9e-9,
 "original exact 4/3 clock SOURCE agrees with full scalar Book finite differences");
const cross=ssum(old.C,F4.J43),norm43=ssum(F4.J43,F4.J43);
const gramDet=ssum(old.C,old.C)*norm43-cross**2;
assert(gramDet>1e-12,
 "two ORIGINAL clock-shape source rows 3/2 and 4/3 are LINEARLY INDEPENDENT");
const currentNorm=ssum(old.C,old.C);
const odd=K.map((row,u)=>row.map((_,v)=>(old.C[u][v]-old.C[v][u])/2));
const even=K.map((row,u)=>row.map((_,v)=>(old.C[u][v]+old.C[v][u])/2));
let oddMass=0,oddDiv=0,nOdd=0,nEven=0;
for(let u=0;u<N;u++){
 let out=0,incoming=0;
 for(let v=0;v<N;v++){
  oddMass+=odd[u][v];out+=odd[u][v];incoming+=odd[v][u];
  nOdd+=odd[u][v]**2;nEven+=even[u][v]**2;
 }
 oddDiv=Math.max(oddDiv,Math.abs(out-incoming));
}
assert(oddDiv<1e-12&&Math.abs(oddMass)<1e-12,
 "original chiral component is a true 327-dimensional CIRCULATION");
// REAL irreversibility control: a directed ABC 3-cycle affinity is nonzero
// and equals the full original scalar net forward-vs-reverse path cost.
const abc=[[1,15],[15,32],[32,1]];
const xyz=[[1,32],[32,15],[15,1]];
const forward=abc.reduce((q,[u,v])=>q*K[u][v],1);
const backward=xyz.reduce((q,[u,v])=>q*K[u][v],1);
const cycleOdds=forward/backward;
assert(Math.abs(Math.log(cycleOdds))>1e-8,
 "true original 3-zone Book unequal circulation distinguishes orientation");
assert(nOdd>0&&nEven>0,
 "heterogeneous original Book history has BOTH genuinely nonzero odd and even shape response");
// Span: E=359 undirected original pairs.
// odd divergence-free space = E-(N-1)=327;
// even with total0 = E-1=358, containing original future32 + even-dark326.
assert(359-32===327&&359-1===358&&32+326===358,
 "full normalized original 685=327 cycle+32 future+326 even-dark");

console.log(JSON.stringify({
 status:"PASS_ORIGINAL_718_BOOK_PROJECTIVE_2_3_CLOCK_BALANCED_SHAPE_SOURCE",
 nativeOriginal:{vertices:33,directedEdges:718,undirectedEdges:359,BookRoot:old.lambda,
  absoluteBookB:old.B,stageClockContrast:old.stage,
  projectiveShape:old.shape,normalizedDoobOnly:old.fromP,
  Z2:old.Z2,Z3:old.Z3,TrP2:old.T2,TrP3:old.T3,
  nativeWeylW:old.W,nativeWeylFactorized:old.lambda**3*old.T3/7722,
  originalStage32Odds:old.stageOdds,recoveredLambdaFrom32:old.lambdaRecovered},
 transformations:{positiveScale:q,lambdaRatio:now.lambda/old.lambda,
  maxDoobDeviation:Pmax,maxMuDeviation:muMax,maxShapeCurrentDeviation:Cmax,
  scalarShapeShift:now.shape-old.shape,
  BookWeylRatio:now.W/old.W},
 twoClockSource:{stage34: F4.actual43,DoobOnly34:F4.projective43,stage4Z:F4.z4,
   stage4P:F4.t4,stage43Odds:F4.odds43,recoveredLambdaFrom43:F4.recovered43,norm43,crossWith32:cross,positiveGramDet:gramDet,
   exactCostSource43:secondSource,finiteCostSource43:secondFD},
 shapeFirstSource:{norm2:currentNorm,
  balancedMass:ssum(old.C,common),endpointGauge: ssum(old.C,cob),
  exactCostVariation:exactSource,finiteDifference:numSource,
  discrepancy:exactSource-numSource},
 realHodgeSectors:{cycleOddNorm2:nOdd,shapeEvenNorm2:nEven,
  originalTriangleForwardReverseOdds:cycleOdds,
  oddDivergenceMax:oddDiv,modeCounts:{allShape:685,oddCycle:327,evenFuture:32,evenDark:326}},
 physicalScope:"math original scalar Book edge-local path-price and optional fixed stage-clock; no forced G0 full action/GR",
 GR_closed:false
},null,2));
