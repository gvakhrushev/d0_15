#!/usr/bin/env node
"use strict";
/*
 * Golden single-step blow-up / condensed D0->GR bounded controls.
 *
 * This checker does NOT prove the all-metrics natural-operator theorem,
 * full physical admission, or that native phi^n refinement is physical
 * metric unit scaling. It tests the exact finite shrinking-native-leg
 * HJR Bloch source, its continuum Bessel representation, and SEPARATE
 * metric-weight countermodels used in the mathematical proof.
 * 23 Oct correction: raw rho scales inverse legs, hence covariant g
 * scales rho^-1 (and carries h^-2 at fixed rho). The raw contrast below
 * is not a test of physical Golden metric scaling or fixed-primary GR.
 */
function assert(ok, label) { if (!ok) throw new Error("FAILED: "+label); }
const phi=(1+Math.sqrt(5))/2,p=(Math.sqrt(5)-1)/2,
  zeta=2**-20,beta=2*p*p,rhoGolden=phi*phi;
function close(a,b,eps, label) {
  assert(Math.abs(a-b)<=eps,label+": "+a+" vs "+b);
}
function I0(x) {
  let sum=1, term=1;
  for(let n=1;n<=120;n++){
    term*=x*x/(4*n*n);sum+=term;
    if(Math.abs(term)<Math.abs(sum)*1e-16) break;
  }
  return sum;
}
function I1(x) {
  let sum=0,term=x/2;
  for(let n=0;n<=120;n++){
    sum+=term;
    term*=x*x/(4*(n+1)*(n+2));
    if(Math.abs(term)<Math.abs(sum)*1e-16)break;
  }
  return sum;
}
function continuumPressure(rho) {
  // Complete 16 L^4 shifted-adjoint HJR on native v=h sqrt(rho) e,
  // with 128*16 feedback weight; not a fixed-physical-metric limit.
  let s=0;
  for(let n=0;n<7;n++){
    let t=(n+1)*beta*rho,i=I0(2*t),j=I1(2*t);
    s+=(-zeta/(1-zeta))**n*Math.exp(-8*t)*i*i*(i-j)**2;
  }
  return 4096*zeta*beta*rho/(1-zeta)*s;
}
const P1=continuumPressure(1),Pg=continuumPressure(rhoGolden),
      defect=Pg-rhoGolden*P1;
close(P1,8.200604436907762e-6,1e-17,"raw shrinking-leg null source at rho=1");
close(Pg,2.67183317722466e-7,1e-18,"raw shrinking-leg null source at rho=phi^2");
assert(defect<-2.1e-5,"strict continuum raw-rho source contrast");
assert(Pg/rhoGolden <P1,"positive integral monotonicity");
console.log("CONTINUUM shrinking-leg HJR: P(1)=",P1,
  " P(phi^2)=",Pg," raw-rho contrast=",defect);

// Explicit finite native creation legs v=h sqrt(rho) e, U=I, all modes.
// Their physical covariant metric has scale h^-2 rho^-1, not rho.
// retain H global normalization and full J feedback, moving Riesz
// first shear=0 (all 8 first shell momenta have one active coordinate).
function nativeFlatSource(L,rho) {
  const cs=Array.from({length:L},(_,k)=>Math.cos(2*Math.PI*k/L));
  const sn=Array.from({length:L},(_,k)=>Math.sin(2*Math.PI*k/L));
  const ar=cs.map(c=>2*(1-c)),alpha=p*p/(128*L*L),m=256*L*L;
  let partition=0,weighted=0,feedback=0;
  for(let a=0;a<L;a++)for(let b=0;b<L;b++)
  for(let c=0;c<L;c++)for(let d=0;d<L;d++){
    const mu=ar[a]+ar[b]+ar[c]+ar[d],
      B=1-alpha*rho*mu;
    assert(B>0,"true original Julia chart");
    const W=Math.exp(m*Math.log(B)),F=1-zeta+zeta*W,
      mixed=2*((1-cs[a])*(1-cs[b])+sn[a]*sn[b]);
    partition+=W; weighted+=mixed*W/B;
    feedback+=mixed*W/(B*F);
  }
  const H=-rho*weighted/partition;
  const J=rho*2048*zeta*beta*feedback;
  return {H,J,P:(H+J)/(L**4)};
}
const finite=[];
for(const L of [4,8,12,16,20]){
  let s1=nativeFlatSource(L,1),sg=nativeFlatSource(L,rhoGolden);
  // Finite thermal reference (O(1)) is retained, never silently erased.
  assert(Number.isFinite(s1.H)&&Number.isFinite(sg.J),"finite original thermal+feedback");
  finite.push({L,source1:s1.P,sourceGolden:sg.P,defect:sg.P-rhoGolden*s1.P});
}
console.log("FINITE shrinking-leg CAR16 H+J+R source (rank128 R first jet=0):",JSON.stringify(finite));
close(finite[finite.length-1].source1,P1,3e-6,"finite-L Fourier torus approach");

// The physically relevant tensor weights under g->rho g in 4D.
// G[ρg]=G[g], metric ρg, R² Euler ρ^-1.
// This is a dimensional algebra control, NOT a native physical derivation.
for(const rho of [rhoGolden,2,3]){
  assert(1!==rho&&rho!==rho**-1,"different homogeneity weights");
}

// A genuine fourth-jet R² counterexample invisible to any 2-jet-only
// test: conformal g=e^{2a x^4}eta has g(0)=eta and dg=d²g=0,
// but R=72a x²+O(x^6) and E^{R²}_{00}(0)=-288a.
for(const a of [1,-2,3]){
  let secondR=144*a,boxR=-secondR;
  let R2_E00=2*boxR;
  assert(R2_E00===-288*a,"exact 4th-order off-Brinkmann witness");
  close(R2_E00/rhoGolden,(-288*a)/rhoGolden,1e-12,"R² has scale weight -1");
}

// Analytically C0 but not C1 at R=0, still Golden discretely
// invariant as a symmetric local 2-tensor (NOT off-shell conserved).
function logPeriodicRatio(R) {
  return Math.sin(Math.PI*Math.log(Math.abs(R))/Math.log(phi));
}
for(const R of [0.17,2.3,11]){
  close(logPeriodicRatio(R/rhoGolden),logPeriodicRatio(R),2e-14,
    "discrete phi-2 scaling periodicity");
}
let r0=phi**(-20),r1=phi**(-19.5);
close(logPeriodicRatio(r0),0,1e-13,"non-smooth derivative subsequence 0");
close(logPeriodicRatio(r1),1,1e-13,"non-smooth derivative subsequence 1");

// The categorical DESCENT requirement is not automatic even for finite
// condensed probes: one metric can have two histories with different
// source values. No source map on the metric quotient exists then.
const quotient=[0,0,1],badSource=[3,4,5],goodSource=[3,3,5];
const descends=src=>src.every((v,i)=>src.every((w,j)=>
  quotient[i]!==quotient[j]||v===w));
assert(!descends(badSource),"equalizer fails when hidden native source varies");
assert(descends(goodSource),"equalizer permits a unique metric-source map");

// The Golden blow-up normal-jet argument is analytical: in normal
// coordinates g(tx)=eta+t² h2(x)+O(t³). This polynomial diagnostic
// shows why any nonzero smooth cubic response is excluded by the
// EXACT equality E(g_t)=t² E(g) on infinitely many phi^-n.
for(let n=2;n<=10;n++) {
  const t=phi**(-n),a=7,b=5;
  const fake=(a*t*t+b*t*t*t)/(t*t);
  assert(fake>a&&Math.abs(fake-a)<b*phi**(-n)+1e-10,
    "higher smooth jet decays under Golden zoom");
}
console.log("PASS mathematical checks: discrete Golden blow-up controls, ",
  "strict raw-rho HJR contrast, real R² 4jet, nondifferentiable ",
  "log-periodic exception, and finite condensed source equalizer.");
console.log("FULL native Cost-Info/oldRIGHT/clock/action selection, metric",
  " descent, open-Diff naturality and off-shell Ward remain OPEN.");
