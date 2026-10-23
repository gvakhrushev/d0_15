#!/usr/bin/env node
// Exact analytic finite-source theorem, bounded independent numerical controls.
// Original transition Cost−Info split theta remains a CONVENTION, not a newly
// selected physical law. No new Kraus/GR action; all failures/endpoints retained.
// Tests full alternative paths, conditional first jets, and NONCOMMUTING loop.
const phi=(1+Math.sqrt(5))/2, ell=Math.log(phi);
const close=(a,b,eps=1e-9)=>{if(Math.abs(a-b)>eps)throw Error("mismatch "+a+" vs "+b)};
const info=(v,t)=>.29*(v+1)+.07*v*t*t+Math.sin(t*(v+1)*.34);
const cost=(u,v,t)=>2+.09*u+.03*v+.021*(u+1)*(v+1)*t+.006*u*v*t*t;
function action(path,theta,t){
 let s=0;
 for(let i=0;i<path.length-1;i++){
  const u=path[i],v=path[i+1];
  s+=cost(u,v,t)-theta*info(u,t)-(1-theta)*info(v,t);
 }
 return s;
}
const raw=(path,theta,t)=>Math.exp(-ell*action(path,theta,t));
const firstPair=[[0,1,3],[0,2,3],[0,4,3]];
const secondPair=[[1,2,3],[1,4,3]];
const allPaths=[...firstPair,...secondPair];
const thetaValues=[-.3,.15,.5,1.2],tt=.37;
for(const theta of thetaValues){
 for(const eta of thetaValues){
  for(const path of allPaths){
   close(action(path,theta,tt)-action(path,eta,tt),
     (theta-eta)*(info(path.at(-1),tt)-info(path[0],tt)),1e-13);
  }
 }
}
function conditional(theta,t,arr=firstPair){
 const w=arr.map(path=>raw(path,theta,t)),total=w.reduce((a,b)=>a+b);
 return w.map(x=>x/total);
}
function endMarginal(theta,t){
 const a=firstPair.reduce((x,y)=>x+raw(y,theta,t),0),
       b=secondPair.reduce((x,y)=>x+raw(y,theta,t),0);
 return a/(a+b);
}
let maxCond=0,maxSource=0;
for(const theta of thetaValues){
 for(let i=0;i<firstPair.length;i++){
  const h=1e-5;
  maxCond=Math.max(maxCond,Math.abs(conditional(theta,tt)[i]-
     conditional(.5,tt)[i]));
  const deriv=(conditional(theta,tt+h)[i]-conditional(theta,tt-h)[i])/(2*h);
  const derivOther=(conditional(.5,tt+h)[i]-conditional(.5,tt-h)[i])/(2*h);
  maxSource=Math.max(maxSource,Math.abs(deriv-derivOther));
 }
}
if(!(maxCond<1e-13&&maxSource<1e-8))throw Error("conditional physics depends on theta");
// HOSTILE: the original complete unconditional endpoint distribution
// is generally different and MUST NOT be silently erased as 'gauge'.
if(Math.abs(endMarginal(-.3,tt)-endMarginal(1.2,tt))<.05)
 throw Error("hostile real endpoint marginal test failed");

const matMul=(A,B)=>[
 [A[0][0]*B[0][0]+A[0][1]*B[1][0],A[0][0]*B[0][1]+A[0][1]*B[1][1]],
 [A[1][0]*B[0][0]+A[1][1]*B[1][0],A[1][0]*B[0][1]+A[1][1]*B[1][1]]
];
const scale=(A,c)=>A.map(row=>row.map(x=>x*c));
const maxDiff=(A,B)=>Math.max(...A.flatMap((row,i)=>row.map((x,j)=>Math.abs(x-B[i][j]))));
const cycle=[
 [0,1,[[1,1.1],[0,1]]],
 [1,3,[[1,0],[-.4,1]]],
 [3,2,[[1,.5],[0,1]]],
 [2,0,[[1,0],[.8,1]]]
];
function holonomy(theta,t){
 let U=[[1,0],[0,1]];
 for(const [a,b,M] of cycle){
  const edge=cost(a,b,t)-theta*info(a,t)-(1-theta)*info(b,t);
  U=matMul(U,scale(M,Math.exp(-ell*edge/2)));
 }
 return U;
}
let maxLoop=0,maxLoopJet=0;
for(const theta of thetaValues){
 maxLoop=Math.max(maxLoop,maxDiff(holonomy(theta,tt),holonomy(.5,tt)));
 const h=1e-5;
 const derivative=t=>holonomy(theta,t);
 const d1=holonomy(theta,tt+h).map((row,i)=>row.map((x,j)=>
  (x-holonomy(theta,tt-h)[i][j])/(2*h)));
 const d0=holonomy(.5,tt+h).map((row,i)=>row.map((x,j)=>
  (x-holonomy(.5,tt-h)[i][j])/(2*h)));
 maxLoopJet=Math.max(maxLoopJet,maxDiff(d1,d0));
}
if(!(maxLoop<1e-13&&maxLoopJet<1e-8))throw Error("closed native-face transport depends on allocation");

const CI=(u,v)=>2+.4*u*v+.07*u*u*v+.13*u*v*v;
const I=q=>q*q+.3*q*q*q+Math.sin(q);
const Ip=q=>2*q+.9*q*q+Math.cos(q);
const interior=(u,q,v,theta)=>{
 const h=1e-6;
 const action=t=>CI(u,t)+CI(t,v)-theta*I(u)-I(t)-(1-theta)*I(v);
 return (action(q+h)-action(q-h))/(2*h);
};
const expected=(u,q,v)=>.4*u+.07*u*u+.26*u*q+
 .4*v+.14*q*v+.13*v*v-Ip(q);
let maxEuler=0;
for(const theta of thetaValues){
 maxEuler=Math.max(maxEuler,Math.abs(interior(-.2,.3,.5,theta)
             -expected(-.2,.3,.5)));
}
if(maxEuler>1e-8)throw Error("bulk internal Euler fails");
// Endpoint canonical p_θ - p_η = (θ−η)dI(q) on BOTH discrete sides.
const q=.3, theta1=1.2,theta2=-.3;
const pMinus=t=>-.4*.5-.14*q*.5-.13*.5*.5+t*Ip(q);
const pPlus=t=>.4*(-.2)+.07*(-.2)**2+.26*(-.2)*q-(1-t)*Ip(q);
close(pMinus(theta1)-pMinus(theta2),(theta1-theta2)*Ip(q));
close(pPlus(theta1)-pPlus(theta2),(theta1-theta2)*Ip(q));
// A 2D exact boundary gradient has zero curl, so (q,p)->(q,p+c dI)
// is a genuine symplectomorphism, not just a 1D triviality.
const gradI2=(x,y)=>[2*x+.6*y,.6*x+Math.exp(y)];
const h=1e-5;
const curl=(gradI2(.21,.36+h)[0]-gradI2(.21,.36-h)[0])/(2*h)
 -(gradI2(.21+h,.36)[1]-gradI2(.21-h,.36)[1])/(2*h);
close(curl,0,1e-9);
// Exact full ORIGINAL endpoint-variance criterion, without dropping failures.
// Full Z(θ) changes with θ; first two accounting derivatives are mean/variance.
function endpointStats(theta,t){
 const W0=firstPair.reduce((s,p)=>s+raw(p,theta,t),0),
       W1=secondPair.reduce((s,p)=>s+raw(p,theta,t),0);
 const P=W0/(W0+W1),i0=info(3,t)-info(0,t),
       i1=info(3,t)-info(1,t),mean=P*i0+(1-P)*i1;
 return {Z:W0+W1,P,mean,var:P*(i0-mean)**2+(1-P)*(i1-mean)**2};
}
const e=.37,hTheta=1e-4,stats=endpointStats(.5,tt);
const lnZ=t=>Math.log(endpointStats(t,tt).Z);
const thetaSource=(lnZ(.5+hTheta)-lnZ(.5-hTheta))/(2*hTheta);
const thetaHessian=(lnZ(.5+hTheta)-2*lnZ(.5)+lnZ(.5-hTheta))/(hTheta*hTheta);
close(thetaSource,-ell*stats.mean,1e-8);
close(thetaHessian,ell*ell*stats.var,1e-6);
if(!(stats.var>0))throw Error("genuine complete endpoint susceptibility unexpectedly zero");
// ORIGINAL real 4×4 Lorentz two-null crossing, genuinely NONCOMMUTATIVE.
const id4=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const zero4=()=>Array.from({length:4},()=>Array(4).fill(0));
const mul4=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const add4=(A,B,c=1)=>A.map((row,i)=>row.map((v,j)=>v+c*B[i][j]));
const scale4=(A,c)=>A.map(row=>row.map(v=>v*c));
const diff4=(A,B)=>Math.max(...A.flatMap((row,i)=>row.map((v,j)=>Math.abs(v-B[i][j]))));
const N2=zero4(),oppositeN3=zero4(),rotation=zero4();
N2[1][2]=N2[2][0]=1;
oppositeN3[0][3]=oppositeN3[3][1]=1;
rotation[2][3]=1;rotation[3][2]=-1;
close(diff4(add4(mul4(N2,oppositeN3),mul4(oppositeN3,N2),-1),rotation),0,1e-14);
const expNull=(N,a)=>add4(add4(id4(),N,a),mul4(N,N),a*a/2); // N^3=0 exactly
const fourNull=[
 [0,1,expNull(N2,.13)],
 [1,2,expNull(oppositeN3,.17)],
 [2,3,expNull(N2,-.13)],
 [3,0,expNull(oppositeN3,-.17)]
];
function fullNullLoop(theta,t){
 let P=id4();
 for(const [u,v,U] of fourNull){
  const edge=cost(u,v,t)-theta*info(u,t)-(1-theta)*info(v,t);
  P=mul4(P,scale4(U,Math.exp(-ell*edge/2)));
 }
 return P;
}
let maxNoncommutingNull=0;
for(const theta of thetaValues){
 maxNoncommutingNull=Math.max(maxNoncommutingNull,
    diff4(fullNullLoop(theta,tt),fullNullLoop(.5,tt)));
}
if(!(maxNoncommutingNull<1e-12))throw Error("4x4 native double-null crossed Weyl changed under theta");
// Baseline matrix is CURVED, not a trivial identity disguised by a scalar.
const originalUnweighted=fourNull.map(x=>x[2]).reduce((A,B)=>mul4(A,B),id4());
if(!(diff4(originalUnweighted,id4())>.02))throw Error("crossed nonflat Lorentz loop absent");
console.log(JSON.stringify({
 status:"PASS",
 actualNativeBookPhi:phi,
 testedEndpointPathCount:allPaths.length,
 testedAllocations:thetaValues,
 conditionalValueMaxDifference:maxCond,
 conditionalFieldSourceMaxDifference:maxSource,
 unconditionedEndpointMarginalThetaMinus03:endMarginal(-.3,tt),
 unconditionedEndpointMarginalTheta12:endMarginal(1.2,tt),
 noncommutingClosedHolonomyMaxDifference:maxLoop,
 true4x4DoubleNullCrossedWeylThetaDifference:maxNoncommutingNull,
 closedHolonomyMovingInfoJetMaxDifference:maxLoopJet,
 discreteInteriorEulerMaxError:maxEuler,
 canonicalMomentumShiftAndSymplecticCurl:"PASS",
 trueUnconditionedEndpointInfoVariance:stats.var,
 dThetaLogPartition:thetaSource,
 dTheta2LogPartition:thetaHessian,
 scope:"Original Book edge allocation convention and declared path/weighted-loop carriers. NOT compulsory native whole Cost−Info/GR."
},null,2));
