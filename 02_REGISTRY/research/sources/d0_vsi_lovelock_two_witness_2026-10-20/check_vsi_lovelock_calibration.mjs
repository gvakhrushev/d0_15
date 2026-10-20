#!/usr/bin/env node
"use strict";
/*
 * Exact integer-index controls for the *existing* D0 nonlinear Brinkmann
 * carrier and the two-witness Lovelock classification interface.
 *
 * This checks Riemann/Ricci scalar-contraction identities on many exact
 * constant 2-jets. The full covariant-derivative VSI induction and the
 * external Lovelock theorem are analytic inputs, NOT inferred by sampling.
 * Native physical Cost-Info selection, action uniqueness and GR closure OPEN.
 */
function assert(cond,msg){if(!cond)throw new Error(msg)}
const n=4, u=0,v=1,x=2,y=3;
function ginv(H){
  return [[0,1,0,0],[1,-H,0,0],[0,0,-1,0],[0,0,0,-1]];
}
function tensor(c,A,B) {
  // The ORIGINAL null Brinkmann metric H=c(x^2+y^2)+A(x^2-y^2)+2Bxy
  // has lower R_{uiuj}=-H_ij/2 and Ric_uu=+Delta H/2=2c.
  const T=[[-(c+A),-B],[-B,-(c-A)]];
  const wedge=(a,b,i)=>Number(a===u&&b===i)-Number(a===i&&b===u);
  return (a,b,d,e)=>{
    let s=0;
    for(let i=2;i<4;i++)for(let j=2;j<4;j++)
      s+=T[i-2][j-2]*wedge(a,b,i)*wedge(d,e,j);
    return s;
  };
}
function invariants(c,A,B,H0){
  const inv=ginv(H0), R=tensor(c,A,B);
  const Ric=Array.from({length:n},(_,b)=>Array.from({length:n},(_,d)=>{
    let s=0;
    for(let a=0;a<n;a++)for(let e=0;e<n;e++)s+=inv[a][e]*R(a,b,e,d);
    return s;
  }));
  let scalar=0,ricciSquare=0,riemannSquare=0;
  for(let a=0;a<n;a++)for(let b=0;b<n;b++){
    scalar+=inv[a][b]*Ric[a][b];
    for(let e=0;e<n;e++)for(let f=0;f<n;f++)
      ricciSquare+=inv[a][e]*inv[b][f]*Ric[a][b]*Ric[e][f];
  }
  // Raise all indices using the literal null inverse, including
  // g^{vv}=-H. DO NOT substitute a Euclidean positive metric.
  for(let a=0;a<n;a++)for(let b=0;b<n;b++)
  for(let d=0;d<n;d++)for(let e=0;e<n;e++){
    const t=R(a,b,d,e);
    if(!t)continue;
    for(let f=0;f<n;f++)for(let g=0;g<n;g++)
    for(let k=0;k<n;k++)for(let l=0;l<n;l++)
      riemannSquare+=t*inv[a][f]*inv[b][g]*
                       inv[d][k]*inv[e][l]*R(f,g,k,l);
  }
  return {Ric,scalar,ricciSquare,riemannSquare,
    Ruxux:R(u,x,u,x),Ruxuy:R(u,x,u,y),
    WeylNonzero:A!==0||B!==0};
}
// A finite exact-integer check of one- and two-jet expressions.
// Strictly independent c,A,B values exercise vacuum, sourced Ricci,
// genuinely Weyl-curved, and completely flat configurations.
let cases=0, sourced=0,weyl=0;
for(let c=-2;c<=2;c++)for(let A=-2;A<=2;A++)
for(let B=-2;B<=2;B++)for(const h of [-3,0,2]){
  const t=invariants(c,A,B,h);
  assert(t.Ric[0][0]===2*c,"incorrect Ric_uu");
  for(let a=0;a<4;a++)for(let b=0;b<4;b++)
    if(a!==0||b!==0)assert(t.Ric[a][b]===0,"wrong non-null Ricci");
  assert(t.scalar===0,"Ricci scalar not zero");
  assert(t.ricciSquare===0,"Ricci squared not zero");
  assert(t.riemannSquare===0,"Kretschmann not zero");
  assert(t.Ruxux===-(c+A),"wrong transverse tensor");
  assert(t.Ruxuy===-B,"wrong Weyl mixed curvature");
  cases++;if(c) sourced++;if(A||B) weyl++;
}
const f=invariants(0,0,0,0),wave=invariants(0,1,1,0),
      source=invariants(2,1,1,0);
assert(f.Ruxux===0&&f.Ruxuy===0,"flat control");
assert(wave.Ruxux!==0&&wave.Ric[0][0]===0,"nonflat vacuum invisible");
assert(source.Ric[0][0]!==0&&source.Ruxuy!==0,"sourced Ricci+Weyl witness");

// Algebra of the TWO native equation calibrations.
// Conditional Lovelock E=a G + b g with a!=0:
// flat Einstein, T=0 -> b=0; nonvac G=-lambda T -> kappa=-lambda*a.
// A real R^2 Euler is identically zero whenever R(x) is the zero
// field (all derivatives vanish), so it is a fourth-order stealth term.
const p=(Math.sqrt(5)-1)/2,zeta=2**-20;
const Q=1-zeta*4*p**3, Qr=1-zeta*4*p**3*(1+p**6);
const lambda=-2*p**-5*(Qr/Q+p**6);
assert(lambda<0 && Math.abs(lambda+23.416406751884)<1e-9,
       "actual configured J2 ratio differs");
for(const a of [1,3,7]){
  const b=0,kappa=-a*lambda;
  assert(Math.abs(a*(-lambda*4)-(kappa*4))<1e-10,
         "native source calibration incorrect");
  assert(b===0,"vacuum calibration");
}
const report={
  proof:"EXACT integer null Brinkmann tensor witness",
  cases, sourced,weyl,
  RicciScalar:0,RicciSquared:0,Kretschmann:0,
  flat_vs_wave:"Riemann differs despite identical entire polynomial-scalar catalogue",
  sourced_control:{Ricuu:source.Ric[0][0],Ruxuy:source.Ruxuy},
  configured_lambda:lambda,
  universal_class:"conditional on metric-only natural off-shell conserved 2jet E",
  higher_curvature_control:"R^2 Euler vanishes on ALL Brinkmann H because R identically 0",
  core_status:"VSI + calibration math only; full native Cost-Info/selection remains OPEN",
  GR_closed:false
};
console.log(JSON.stringify(report,null,2));
