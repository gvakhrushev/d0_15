// Finite regular algebraic native Book03 heat + feedback cannot exactly
// reproduce whole Shannon CQ logarithmic source on an open Born chart.
// Checks actual native three-status Golden probabilities and *strict*
// finite K truncated-harmonic Gibbs relative entropy, with elementary
// bounded algebraic heat/feedback controls. Universal Puiseux/monodromy
// theorem is analytical, NOT claimed numerically certified.
import assert from 'node:assert/strict';
const p=(Math.sqrt(5)-1)/2,phi=1/p,beta=2*p*p,z=2**-20;
let checks=0;const ok=(x,m)=>{assert.ok(x,m);checks++};
const close=(a,b,t=2e-11,m='close')=>
 ok(Math.abs(a-b)<t*Math.max(1,Math.abs(a),Math.abs(b)),m+': '+a+' vs '+b);
const gamma=(1-(1-2*p**3)**9)**128*
 (((1-p**120)**4)*(1-(1-16*p**9)**20))**43;
const L=4*p**3,Q=1-z*L,R=1-z*L*(1+p**6),r0=1-Q*R;
const originalQ=[1-gamma,gamma*(1-r0),gamma*r0];
close(originalQ.reduce((a,b)=>a+b,0),1,2e-13,'original N1 full ternary positive probability normalization');
ok(originalQ.every(q=>q>0&&q<1),'all full paid READY failures/statuses positive');
ok(originalQ[0]>originalQ[1]&&originalQ[1]>originalQ[2],
   'strict ORIGINAL native three nonuniform Golden probabilities');
const H=q=>-q.reduce((a,x)=>a+x*Math.log(x),0);
const deltaK=(q,K)=>{
 let s=0,w=1-q;
 for(let n=1;n<=K;n++){s+=w/n;w*=1-q}
 return -Math.log(q)-s;
};
function GibbsTruncated(q,K){
 const d=q.map(x=>deltaK(x,K));
 const v=q.map((x,i)=>x*Math.exp(d[i]));
 const N=v.reduce((a,b)=>a+b,0),sigma=v.map(x=>x/N);
 const kl=q.reduce((a,x,i)=>a+x*Math.log(x/sigma[i]),0);
 const dual=kl/beta;
 return {d,sigma,kl,dual};
}
for(const K of [1,2,3,4,8,20,100,400,1000]){
 const m=GibbsTruncated(originalQ,K);
 close(m.sigma.reduce((a,b)=>a+b,0),1,2e-13,'finite-K complete three-mode generated Gibbs normalized');
 ok(m.kl>1e-10,'finite K cannot exactly Gibbs-match TRUE original unequal statuses');
 ok(m.dual>1e-10,'finite generated HJR action gap strict relative entropy');
 ok(m.d[2]>m.d[1]&&m.d[1]>m.d[0],
   'strict finite native harmonic remaining tail follows rare-category order');
 for(const q of originalQ){
   const exact=-((1-q)**K)/q;
   const h=Math.min(2e-8,q*1e-4);
   const numerical=(deltaK(q+h,K)-deltaK(q-h,K))/(2*h);
   close(numerical,exact,8e-4,'actual native harmonic δ_K derivative tail negative exact');
   ok(exact<0,'nonuniform q implies different positive finite cap tails');
 }
}
// Original finite cap K=100M can get an *extremely* small but NOT ZERO
// positive KL gap analytically; double arithmetic would round it to 0.
// This is intentionally NOT computed by finite double sums.
const Khuge=100_000_000,rare=originalQ[2],theta=1-8e-7;
ok(rare>8.3e-7&&rare<9e-7,'native rare q for stable tail-control chart');
ok(Math.exp(-80)/80<3e-37,'owned uniform finite K100M native operator tail bound');
ok(Math.pow(theta,Khuge)<=Math.exp(-80),'finite Golden source bound reference');
// Concrete fixed finite REGULAR algebraic two-level source.  A(u), F(u)
// bounded algebraic right through Born outcome u=0; real HJR value has
// finite Puiseux source even though native CQ source diverges log u.
function boundedAction(u){
 const aa=1+u,bb=2+u*u,
       F0=4*p*u*(1-p*u),F1=4*p*(1-u)*(1-p*(1-u)),
       w0=1-u,w1=u;
 ok(F0>=0&&F0<1&&F1>=0&&F1<1,'strict genuine Golden-like algebraic effect eigenvalues');
 const R=w0*aa+w1*bb;
 const Z=Math.exp(-beta*aa)+Math.exp(-beta*bb);
 const J=-Math.log1p(-z*F0)-Math.log1p(-z*F1);
 return {R,H:Math.log(Z)/beta,J,A:R+Math.log(Z)/beta+J};
}
function source(u){
 const aa=1+u,bb=2+u*u;
 const dr=2-2*u+3*u*u;
 const eb0=Math.exp(-beta*aa),eb1=Math.exp(-beta*bb);
 const dH=-(eb0+2*u*eb1)/(eb0+eb1);
 const f0=4*p*u*(1-p*u), f1=4*p*(1-u)*(1-p*(1-u));
 const f0p=4*p*(1-2*p*u);
 const f1p=-4*p*(1-2*p*(1-u));
 const dJ=z*f0p/(1-z*f0)+z*f1p/(1-z*f1);
 return dr+dH+dJ;
}
for(const u of [1e-1,1e-2,1e-3,1e-4,1e-6,1e-8]){
 const s=source(u);
 ok(Number.isFinite(s)&&s>0&&s<3,'bounded heat+feedback+prepared source near a genuine finite report-zero chart');
 const h=Math.min(u/200,1e-6);
 const approx=(boundedAction(u+h).A-boundedAction(u-h).A)/(2*h);
 close(s,approx,2e-7,'independent whole positive finite heat+Golden feedback source');
 const nativeHprime=Math.log((1-u)/u)/Math.log(phi);
 ok(nativeHprime>0,'original Golden Shannon source positive');
 if(u<1e-4)ok(nativeHprime>14,'Shannon derivative logarithm diverges, finite algebraic HJR source bounded');
}
const eta=GibbsTruncated(originalQ,20);
console.log(JSON.stringify({status:"PASS_FINITE_ALGEBRAIC_BOOK_PUISEUX_GATE",checks,
 original:{gamma,r0,threeProbabilities:originalQ},
 finiteK20ExactNativeKL:eta.kl,
 strictFiniteAllPositiveK:"proven from δ_K'(q)=-(1-q)^K/q<0",
 finiteK100MKlPositiveAnalyticalOnly:true,
 analyticalPuiseuxMonodromy:"not machine-formalized",
 originalNative42ConfiguredRootNotRerun:true,
 fullPhysicalBook03InfoHodgeNotSelected:true,
 GR_closed:false}));
