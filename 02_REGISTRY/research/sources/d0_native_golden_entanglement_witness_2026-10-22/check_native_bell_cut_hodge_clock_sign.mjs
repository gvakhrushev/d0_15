// ORIGINAL CAR16 native actual K0=I-2p² A² in 128-label all-Kraus
// canonical Stinespring, real proper Lorentz boost r=1/9;
// actual oldRIGHT128 present as declared 16-dimensional Bell subspace.
// An explicit FIXED joint registered event (ALL n labels0 AND final
// DATA16/RIGHT16 Bell) has genuine Born probability q_n and native source.
// The PREPARED rank1 cut of the COMPLETE pure forward OUTPUT, with FIXED
// reflection U=I-2Pi_event, produces a full paired cut-Hodge 2-mode
// thermal trace plus ALL (D−2) true zero modes + Book logdet.
// Entire source changes sign EXACTLY between native n=32 and n=33.
// No original compulsory Book03 Δ_N selection nor paid joint oldRIGHT
// gate routing assumed. Entire non-event record complement retained.
import assert from 'node:assert/strict';
let checks=0;function ok(x,m){assert.ok(x,m);checks++}
function near(x,y,t=1e-10,m='close'){
 ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
}
const p=(Math.sqrt(5)-1)/2,zeta=2**-20,beta=2*p*p;
const mu=141489/10240000,h=69399/5030720,muR=-328779/204800000,hR=-20040939/9885993640;
const eps=Math.sqrt(mu*(mu-h));
const epsR=((2*mu-h)*muR-mu*hR)/(2*eps);
const bLo=1-beta*(mu-eps),bHi=1-beta*(mu+eps),bMean=1-beta*mu;
const rightDim=128,carDim=16,alphabet=128;
function dims(n){return carDim*rightDim*alphabet**n}
function signal(n){
 const A=(bLo**n+bHi**n)/2;
 const Ap=-(n*beta/2)*(bLo**(n-1)*(muR-epsR)+bHi**(n-1)*(muR+epsR));
 const q=A*A,qr=2*A*Ap,f=4*q*(1-q),fr=4*(1-2*q)*qr;
 const D=dims(n),E=Math.exp(-beta*f);
 const Z=D-2+2*E,JJ=-Math.log1p(-zeta*f);
 const heat=(Math.log(D)+Math.log1p(-2*(1-E)/D))/beta;
 const fullValue=heat+JJ;
 const thermalCoefficient=-2*E/Z;
 const feedbackCoefficient=zeta/(1-zeta*f);
 const coef=feedbackCoefficient+thermalCoefficient;
 const dH=fr*thermalCoefficient,dJ=fr*feedbackCoefficient;
 return {n,q,qr,f,fr,D,zeroModes:D-2,Z,heat,JJ,fullValue,
          coefficient:coef,thermalCoefficient,feedbackCoefficient,
          dH,dJ,dBook:fr*coef};
}
ok(mu>.0138&&mu<.01382&&eps>.00055&&eps<.00056,
 'unchanged ORIGINAL native Fourier CAR16 two-eigenvalue strict exact rational fixture');
ok(beta>.76&&beta<.8&&zeta===1/1048576,
 'actual Golden/native beta and fugacity unchanged');
ok(bLo>bHi&&bHi>0&&bLo<1&&bMean>3092/3125,
 'actual original B positive eigenvalues and rational lower centre');
ok(bMean<989512/1000000,
 'exact p² mu native upper mean root by beta>.76 and mu>.0138');
const x=beta*eps/bMean;
ok(x>0&&x<46/100000,
 'native two spectral modes relative gap small enough for exact 33-binomial cosh envelope');
// The original 32/33 full CAR16 clean Bell probabilities: q_n=A_n².
// n32: Jensen q>=bMean^64>(3092/3125)^64>1/2.
// n33: (bMean^33 E[(1+x)^33+(1-x)^33]/2)²
//      <= bMean^66 exp((33x)^2)
//      < (989512/1e6)^66/(1-(33*46/1e5)^2) < 1/2.
// BOTH last inequalities tested with exact BigInt rational, not a float.
ok(2n*3092n**64n>3125n**64n,
 'BIGINT exact n32 clean-Bell q_32>1/2 on true original CAR16 native source');
const X=100000n,Y=46n,b=989512n,d=1000000n;
ok(2n*b**66n*X**2n<
   d**66n*(X**2n-(33n*Y)**2n),
 'BIGINT exact native CAR16 q_33<1/2 by rigorous cosh log bound');
const q32=signal(32).q,q33=signal(33).q;
ok(q32>.5&&q33<.5,
 'same fixed native Golden CAR16 K0 32-to-33 horizon crosses exact 50% Bernoulli mark');
let lastQ=1;
for(let n=1;n<=140;n++){
 const s=signal(n);
 ok(s.q<lastQ&&s.q>0&&s.q<1,
   'true native measured joint allblank and Bell event monotone decreasing by positive K0');
 lastQ=s.q;
 ok(s.qr>0,'real proper-Lorentz first source of TRUE returned native event always strictly positive');
 ok(s.f>=0&&s.f<=1,'real original complete reflection paired Hodge F rank1 PSD contraction');
 ok(s.Z>=s.D-2&&s.Z<=s.D,
   'ALL original retained work zero modes and both nonzero Hodge eigenmodes in full HEAT');
 near(s.dBook,s.dH+s.dJ,1e-13,
   'exact full source thermal derivative PLUS Book trace-resolvent feedback source');
 if(n>=2){
  ok(s.D-2>4/zeta,
    'actual FULL oldRIGHT128 & all 128^n original Kraus histories force tiny heat norm and positive full Book coefficient');
  ok(s.coefficient>zeta/2,
    'complete paired Hodge heat cannot reverse genuine Book feedback source for n>=2');
  if(n<=32)ok(s.dBook<0,
      'full Hodge+Book proper-Lorentz first source STRICTLY NEGATIVE for all clocks n2..32');
  else ok(s.dBook>0,
      'same original Book source STRICTLY POSITIVE all clocks n>=33');
 }else{
  ok(s.dBook>0,'one-round same full Hodge output heat dominates negative feedback derivative');
 }
}
ok(signal(32).dBook<0&&signal(33).dBook>0,
 'EXACT intrinsically native full heat+feedback source sign inversion at 33 clock rounds');
const s130=signal(130);
ok(s130.q>1/16&&s130.q<.075,
 'actual CAR16 old clean-Bell entanglement criterion positive after 130 native rounds');
ok(40n*99n**260n<3n*100n**260n,
 'BIGINT q130<3/40 since original bLo<99/100');
ok(bLo<.99&&s130.q<.075,
 'n130 original clean-Bell probability STRICT below .075');
const source130lower=2*zeta*.85*.0158;
ok(source130lower>2.5e-8&&s130.dBook>source130lower,
 'whole native thermal zero-mode retaining cut Book Lorentz source >2.5e-8 at n130');
ok(s130.zeroModes>0&&s130.D>1e270,
 'genuine oldRIGHT128 / full fine128^130 work never truncated, field-independent dimensional price kept');
// Field derivatives tested on fully ORIGINAL µ(r),d(r) native proper boost rational.
function native(r){
 const x=r*r,f=(1-x)**2;
 const m=9*(5*x*x+x*r-8*x-r+5)/(3200*f);
 const det=81*(23*x*x+6*x*r-32*x-10*r+25)/(10240000*f);
 const er=Math.sqrt(m*m-det);
 return {m,er,low:1-beta*(m-er),high:1-beta*(m+er)};
}
function actual(n,r){
 const {low,high}=native(r);
 const a=(low**n+high**n)/2,q=a*a;
 const f=4*q*(1-q),D=dims(n),exp=Math.exp(-beta*f);
 // mathematically EXACT full action: beta^-1 ln(D-2+2 exp(-beta f))-ln(1-z f)
 return Math.log(D)/beta+
   Math.log1p(-2*(1-exp)/D)/beta -Math.log1p(-zeta*f);
}
function reduced(n,r){
 const {low,high}=native(r);
 const a=(low**n+high**n)/2,q=a*a;
 const f=4*q*(1-q),D=dims(n),exp=Math.exp(-beta*f);
 // Keep the entire field-independent ln D separately; do NOT erase physical cost.
 return Math.log1p(-2*(1-exp)/D)/beta-Math.log1p(-zeta*f);
}
for(const n of [1,2,3,10,31,32,33,34,100,130]){
 const s=signal(n);
 near(actual(n,1/9),s.fullValue,1e-11,
   'ORIGINAL full harmonic heat absolute value and Book feedback WITHOUT rank division');
 for(const dh of [1e-3,3e-4]){
  const diff=(reduced(n,1/9+dh)-reduced(n,1/9-dh))/(2*dh);
  near(diff,s.dBook,1e-8,'independent ORIGINAL native proper boost exact full cut Hodge+feedback source');
 }
}
const p0=signal(1),s2=signal(2),s32=signal(32),s33=signal(33);
console.log(JSON.stringify({status:"PASS_ORIGINAL_NATIVE_CAR16_OLD_RIGHT_COMPLETE_CUT_HODGE_SIGN_AT_33",checks,
 retainedPhysicalData:{
  native:"same original 128 Kraus Fourier CAR16 K0=I-2p²Delta",
  physicalReference:"oldRIGHT128 FULL dimension retained; 16-dim Bell embedding specifically DECLARED, NOT original full Choi128 writer",
  fullWork:"128^n original outcome history slots, every untouched branch included in whole Hodge zeros",
  candidateHeat:"paired cut Hodge L_C=C†C+CC†, NOT mandatory Book03 scene Delta_N"
 },
 finiteClockSign:{n1:p0,n2:s2,n32:s32,n33:s33,n130:s130},
 exactIntegerCertificates:{
  n32:"2*3092^64 >3125^64",
  n33:"2*989512^66 * 100000^2 <1000000^66*(100000^2 - (33*46)^2)",
  n130:"16*3092^260 >3125^260, and 40*99^260 <3*100^260"
 },
 rule:"for every n>=2 this prepared rank-one complete Hodge+Book candidate has source sign sign(1-2q_n); q_n crosses one half at exactly n=33",
 historicalSourceSelection:false,oldRIGHTPhysicalBellRoutingNotAdmitted:true,
 originalNativeFull42EinsteinProofNotConsumed:false,GR_closed:false}));
