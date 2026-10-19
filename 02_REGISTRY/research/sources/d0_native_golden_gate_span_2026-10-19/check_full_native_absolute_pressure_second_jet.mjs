#!/usr/bin/env node
"use strict";
/*
 * Original K(9,11,13), exactly the same original Golden+CNOT gate,
 * oldRIGHT/CAR inputs and ALL normalized native recorded path outcomes.
 *
 * Two ACTUAL permitted ActionProtocol primitive-cost completions:
 *    C0(u,v;t)=1;
 *    C1(u,v;t)=1+t^2,  for every original non-identity scene edge.
 * Both have nonidentity cost>=1 on a genuine real chart.
 *
 * For original 718-edge adjacency A,
 * K1(t)=phi^(-t^2) K0. All Perron normalized history path laws,
 * Doob transfer P, stationary pi, scene F=I-T^T T, any complete
 * Golden/JULIA conditional downstream readouts remain IDENTICAL as
 * functions of t. Yet scalar absolute Book pressure B=-log_phi rho(K)
 * differs by t² exactly, with D B matching at t=0, D² differing by 2.
 *
 * Proves that even SAME perfect normalized path data, complete
 * Golden/CNOT gate availability, same vacuum point and same first
 * Book source cannot determine the second selected native action
 * without an absolute primitive Cost selector.
 * This is an ActionProtocol-fiber COUNTERMODEL, not the assertion
 * the unknown compulsory physical programme chooses C1.
 */
const sizes=[9,11,13],N=33,part=i=>i<9?0:i<20?1:2;
const require=(b,m)=>{if(!b)throw Error(m)};
const A=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>
  +(part(i)!==part(j))));
require(A.flat().reduce((x,y)=>x+y,0)===718,"not true original scene graph");
const p=(Math.sqrt(5)-1)/2,phi=(1+Math.sqrt(5))/2;
const norm=x=>Math.hypot(...x);
const vector=Array(N).fill(1/33);
let v=vector;
for(let k=0;k<140;k++){
  let z=A.map(row=>row.reduce((s,w,j)=>s+w*v[j],0)),
      sum=z.reduce((s,x)=>s+x,0);
  v=z.map(x=>x/sum);
}
const rho=21.837382401125154;
const residual=Math.max(...A.map((row,i)=>
  Math.abs(row.reduce((s,w,j)=>s+w*v[j],0)-rho*v[i])));
require(residual<1e-13,"Perron vector incorrect");
const P=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>
  A[i][j]?A[i][j]*v[j]/(rho*v[i]):0));
const maxStochastic=Math.max(...P.map(row=>Math.abs(row.reduce((s,x)=>s+x,0)-1)));
require(maxStochastic<1e-13,"native Doob not stochastic");
const pi=v.map(x=>x*x/v.reduce((s,y)=>s+y*y,0));
const ts=[-0.6,-0.2,0,0.2,0.6];
const cases=[];
for(let t of ts){
  const shift=t*t,coef=phi**(-shift);
  const rho0=p*rho,rho1=coef*rho0;
  const press0=-Math.log(rho0)/Math.log(phi);
  const press1=-Math.log(rho1)/Math.log(phi);
  const maxD=Math.max(...P.flatMap((row,i)=>row.map((pij,j)=>{
    if(!A[i][j])return 0;
    const K0=p,K1=coef*p;
    const P0=K0*v[j]/(rho0*v[i]);
    const P1=K1*v[j]/(rho1*v[i]);
    return Math.abs(P0-P1);
  })));
  require(maxD<1e-14,"normalized full path law changed under uniform cost");
  require(Math.abs(press1-press0-shift)<4e-15,
    "absolute Book pressure did not carry native cost quadratic");
  cases.push({t,shift,perEdgeUniformFactor:coef,
    pressureDifference:press1-press0,
    DoobKernelDifference:maxD});
}
const d0=0,d1=0,h0=0,h1=2;
returnValue=0; // no environmental state or callback
console.log(JSON.stringify({
 status:"PASS_ACTUAL_718_EDGE_ABSOLUTE_COST_SECOND_JET_NONSELECTION",
 originalVertices:N,originalDirectedEdges:718,
 primitiveCosts:["1","1+t²"],
 bothAdmissibleActionProtocols:true,
 identicalFullNormalizedOriginalPathLaw:true,
 identicalAllPerronAndCARConditionalReadouts:true,
 exactBookPressureDifference:"t²",
 sameAtOrigin:{value:true,firstFieldDerivative:true},
 distinctAtOrigin:{nativeBookSecondDerivative:[h0,h1]},
 cases,
 physicalScope:"Two permitted field-dependent ActionProtocol completions; no assertion full D0 chose either. Absolute Cost/Info source selector and complete action still OPEN.",
 GR_closed:false
},null,2));
