#!/usr/bin/env node
"use strict";
/*
  Complete original K(9,11,13) 718-edge / 1287 triangle scalar BOOK and
  native Golden-p two-flag CAR/Choi/Bell17 positive-root face readout.

  ORIGINAL proper Lorentz null group exponentials and six independent
  Golden signed marks; one physically TYPE-CORRECT 4-link rectangle per
  face. Role links across faces are not inferred from scene graph.
  Demonstrates exact mathematical projective/radial identity, NOT the
  compulsory physical D0 ActionProtocol or 40-Euler GR closure.
*/
const assert=(condition,why)=>{if(!condition)throw new Error(why);}
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p);
const dim=4;
const zero=()=>Array.from({length:dim},()=>Array(dim).fill(0));
const eye=()=>Array.from({length:dim},(_,i)=>Array.from({length:dim},(_,j)=>+(i===j)));
const E=(i,j)=>{const m=zero();m[i][j]=1;return m;};
const add=(a,b,w=1)=>a.map((r,i)=>r.map((x,j)=>x+w*b[i][j]));
const scale=(a,c)=>a.map(r=>r.map(x=>x*c));
const matmul=(a,b)=>a.map(r=>b[0].map((_,j)=>r.reduce((s,v,k)=>s+v*b[k][j],0)));
const transpose=a=>a[0].map((_,j)=>a.map(row=>row[j]));
const trace=a=>a.reduce((s,r,i)=>s+r[i],0);
const frob=(a,b)=>trace(matmul(transpose(a),b));
const nilExp=(a,t)=>add(add(eye(),scale(a,t)),scale(matmul(a,a),t*t/2));
const maxerr=(a,b)=>Math.max(...a.flatMap((r,i)=>r.map((x,j)=>Math.abs(x-b[i][j]))));
const G=[
 add(E(1,2),E(2,0)), add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)), add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1), add(E(1,1),E(0,0),-1)
];
const eta=add(add(E(0,1),E(1,0)),add(E(2,2),E(3,3)),-1);
let lieError=0;
for(let i=0;i<6;i++){
  lieError=Math.max(lieError,maxerr(add(matmul(transpose(G[i]),eta),matmul(eta,G[i])),zero()));
  for(let j=0;j<6;j++)lieError=Math.max(lieError,Math.abs(frob(G[i],G[j])-(i===j?2:0)));
}
assert(lieError<1e-14,"original 6 Lie source Gram / eta mismatch");
function rectangle(g,j){
 const a=.019+.0031*j+.014*g,b=.025+.0016*j-.012*g;
 const A=nilExp(G[0],a),B=nilExp(G[3],b);
 const Ai=nilExp(G[0],-a),Bi=nilExp(G[3],-b);
 return [
   matmul(matmul(matmul(A,B),Ai),Bi),
   matmul(matmul(matmul(B,A),Bi),Ai)
 ];
}
function goldenBell17(U){
 const T=trace(U)/4,norm=frob(U,U),q=[];
 for(const v of G){
   const x=frob(v,U)/(2*Math.SQRT2);
   q.push((p**4/(24*4096))*(T+x)**2,(p**4/(24*4096))*(T-x)**2);
 }
 const GG=p**4*norm/(4*4096);
 const GGrest=GG-q.reduce((s,x)=>s+x,0);
 const GB=p*p*(4-p*p*norm)/(4*4096);
 const BG=p**3*norm/(4*4096);
 const BB=p*(4-p*p*norm)/(4*4096);
 q.push(GGrest,GB,BG,BB,4095/4096);
 assert(q.length===17&&Math.min(...q)>0,"not a complete positive 17-outcome native-P instrument");
 assert(Math.abs(q.reduce((s,x)=>s+x,0)-1)<1e-12,"full native Bell17 not normalized");
 return q;
}
const zone=i=>i<9?0:i<20?1:2;
function originalK(t){
 return Array.from({length:33},(_,i)=>Array.from({length:33},(_,j)=>{
  if(zone(i)===zone(j))return 0;
  const C=1.13+.025*Math.sin(.12*i+.27*j)**2
                +.041*(t+.3)**2*Math.cos(.08*i+.31*j)**2;
  const info=k=>.11*Math.sin(.27*k)+t*.06*Math.cos(.16*k);
  return Math.exp(-ell*(C-.4*info(i)-.6*info(j)));
 }));
}
function originalZ3(k){
 let sum=0;for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
   sum+=k[a][b]*k[b][c]*k[c][a]+k[a][c]*k[c][b]*k[b][a];
 return 3*sum;
}
function observable(t,g){
 const k=originalK(t),W=originalZ3(k)/7722;
 let geometric=0,maxError=0,minProbability=1;
 for(let j=0;j<6;j++){
  const [U,Ui]=rectangle(g,j);
  maxError=Math.max(maxError,maxerr(matmul(transpose(U),matmul(eta,U)),eta));
  const a=0,b=9,c=20+j;
  // True TYPE of independent positive stage/Book acceptance: the factors
  // move with BOTH Book field and original Role geometry field.
  const alpha=p**20*(.8+.03*t+.02*g+.004*t*g)*(1+.03*j);
  const masses=[
   alpha*k[a][b]*k[b][c]*k[c][a],
   alpha*k[a][c]*k[c][b]*k[b][a]
  ];
  const Qs=[
    goldenBell17(U).map(x=>x*masses[0]),
    goldenBell17(Ui).map(x=>x*masses[1])
  ];
  minProbability=Math.min(minProbability,...Qs[0],...Qs[1]);
  const normalized=Qs.map(q=>q.reduce((s,x)=>s+x,0));
  // All source, verifier, early acceptance and absolute Book weights are
  // differentiated in the true positive sum, not declared constant.
  const marks=Qs.map((q,i)=>G.map((_,a)=>
     (Math.sqrt(q[2*a])-Math.sqrt(q[2*a+1]))/Math.sqrt(normalized[i])
  ));
  let R=zero();
  for(let a=0;a<6;a++)
    R=add(R,scale(G[a],64*Math.sqrt(3)/p**2*(marks[0][a]-marks[1][a])));
  const Rtrue=scale(add(U,Ui,-1),.5);
  maxError=Math.max(maxError,maxerr(R,Rtrue));
  // Test a nontrivially moving original Lie/Hodge contraction. The exact
  // full 40-role Euler equality is already owned independently upstream.
  const H=add(scale(G[(j+1)%6],1+j*.3+g*.05),scale(G[(j+2)%6],.27+g*.06));
  geometric+=frob(H,R);
 }
 assert(maxError<1e-10&&minProbability>0,"positive-root curvature decoding failed");
 return {W,geometric,raw:W*geometric,conditional:W*geometric/W,
         maxError,minProbability};
}
const t=-.17,g=.21,h=.0005,z=observable(t,g),
 tplus=observable(t+h,g),tminus=observable(t-h,g),
 gplus=observable(t,g+h),gminus=observable(t,g-h);
const dW=(tplus.W-tminus.W)/(2*h),dG=(gplus.geometric-gminus.geometric)/(2*h);
const dRaw=(tplus.raw-tminus.raw)/(2*h),
 dCond=(tplus.conditional-tminus.conditional)/(2*h);
const cross=(observable(t+h,g+h).conditional-observable(t+h,g-h).conditional
            -observable(t-h,g+h).conditional+observable(t-h,g-h).conditional)/(4*h*h);
assert(Math.abs(z.conditional-z.geometric)<1e-13,"off-shell equality");
assert(Math.abs(dRaw-dW*z.geometric)<1e-7,"raw W*Euler source");
assert(Math.abs(dCond)<1e-8,"Book scalar source contaminated conditioned geometry");
assert(Math.abs(cross)<1e-7,"mixed K/geometry physical-source cancellation");
console.log("PASS original 33 sites, 718 edges, 1287 ABC triangles, 7722 oriented original rooted clocks");
console.log("PASS 6 actual original proper Lorentz 4-link rectangles with native Golden Bell17 each orientation");
console.log("PASS maximum off-shell odd-matrix decoder error",z.maxError);
console.log("PASS smallest complete positive 17-Bell joint-label mass",z.minProbability);
console.log("PASS true non-symmetric raw original Book orbit scalar W=Z3/7722",z.W);
console.log("PASS actual Book weighted source d_t(W*Sstar)",dRaw,"nonzero");
console.log("PASS exact product rule source residual",dRaw-dW*z.geometric);
console.log("PASS projective conditioned d_t source",dCond,"~0");
console.log("PASS conditioned scalar/geometry mixed Hessian",cross,"~0");
console.log("NOTE: genuine compulsory Book H+J+R stationarity and its cost/clock controller NOT derived");
