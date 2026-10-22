// EXACT rational native A^2 quadratic spectrum and native full128 blank K00.
// Proves nonzero two-round record dependence from ACTUAL invariant inverse-square
// rho; strict lower wall for predictive KL via Pinsker, and nonzero proper-link
// boost derivative of blank covariance. No full128 tensor census or Book Info assumption.
import assert from 'node:assert/strict';
let checks=0;const ok=(x,m)=>{assert.ok(x,m);checks++};
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){let v=a%b;a=b;b=v}return a||1n}
function R(a,b=1n){a=BigInt(a);b=BigInt(b);ok(b!==0n,'denom');
 if(b<0n){a=-a;b=-b}const g=gcd(a,b);return {a:a/g,b:b/g}
}
const plus=(x,y)=>R(x.a*y.b+y.a*x.b,x.b*y.b);
const neg=x=>R(-x.a,x.b);
const minus=(x,y)=>plus(x,neg(y));
const mul=(x,y)=>R(x.a*y.a,x.b*y.b);
const div=(x,y)=>R(x.a*y.b,x.b*y.a);
const square=x=>mul(x,x);
const power=(x,n)=>{let y=R(1);while(n--)y=mul(y,x);return y};
const gt=(x,y)=>x.a*y.b>y.a*x.b;
const lt=(x,y)=>x.a*y.b<y.a*x.b;
const eq=(x,y)=>x.a*y.b===y.a*x.b;
const num=x=>Number(x.a)/Number(x.b);
const s=x=>x.a.toString()+"/"+x.b.toString();
const Z=R(0),O=R(1),N9=R(9),r=R(1,9);
const P=plus(plus(plus(plus(mul(R(5),power(r,4)),power(r,3)),
                mul(R(-8),square(r))),neg(r)),R(5));
const Pd=plus(plus(plus(mul(R(20),power(r,3)),mul(R(3),square(r))),
                  mul(R(-16),r)),R(-1));
const Q=plus(plus(plus(plus(mul(R(23),power(r,4)),mul(R(6),power(r,3))),
                  mul(R(-32),square(r))),mul(R(-10),r)),R(25));
const Qd=plus(plus(plus(mul(R(92),power(r,3)),mul(R(18),square(r))),
                  mul(R(-64),r)),R(-10));
const oneMinusR2=minus(O,square(r)),F=square(oneMinusR2);
const originalMu=div(mul(R(9),P),mul(R(3200),F));
const originalD=div(mul(R(81),Q),mul(R(10240000),F));
const slopePoly=(poly,dpoly)=>plus(dpoly,div(mul(mul(R(4),r),poly),oneMinusR2));
const muP=div(mul(R(9),slopePoly(P,Pd)),mul(R(3200),F));
const dP=div(mul(R(81),slopePoly(Q,Qd)),mul(R(10240000),F));
const h=div(originalD,originalMu);
const hP=div(minus(mul(dP,originalMu),mul(originalD,muP)),square(originalMu));
const G=minus(originalMu,h),GP=minus(muP,hP),HG=mul(h,G);
const HGp=plus(mul(hP,G),mul(h,GP));
ok(eq(originalMu,R(141489,10240000)),'SAME original CAR16 mean Delta at boost1/9');
ok(eq(h,R(69399,5030720)),'SAME original CAR16 invariant harmonic Delta at boost1/9');
ok(lt(muP,Z),'native proper boost source muP negative');
ok(gt(G,Z),'native CAR16 spectral nonscalarity exactly');
ok(gt(h,Z),'native faithful inverse-square');
ok(gt(HGp,Z),'NATIVE field derivative of h(mu-h) strictly positive');
const fpoly=x=>minus(plus(square(x),x),O);
ok(lt(fpoly(R(617,1000)),Z)&&gt(fpoly(R(620,1000)),Z),
  'exact polynomial bracket 0.617<p<0.620');
const lowerT=R(76,100),upperT=R(7688,10000);
ok(gt(mul(R(2),square(R(617,1000))),lowerT),'native t=2p² > 0.76 exactly');
ok(lt(mul(R(2),square(R(620,1000))),upperT),'native t=2p² < 0.7688 exactly');
ok(gt(h,R(13795,1000000)),'native harmonic h>0.013795 exact');
ok(gt(G,R(2224,100000000)),'native Delta mean-h gap >0.00002224 exact');
ok(lt(originalMu,R(14,1000)),'native mu <0.014 exact');
const ALower=R(989,1000),AUpper=minus(O,mul(upperT,R(14,1000)));
ok(gt(AUpper,ALower),'native blank survival 1-t mu>0.989 exact');
const deltaLower=mul(mul(mul(mul(R(4),square(lowerT)),
 R(13795,1000000)),R(2224,100000000)),square(ALower));
ok(gt(deltaLower,R(69,100000000)),'native full128 q00-q0² >6.9e-7 strict algebraic bound');
const miLower=mul(R(8),square(R(69,100000000)));
ok(gt(miLower,R(38,10000000000000n)),'native full128 first-two-letters mutual information >3.8e-12 nat');
const p=(Math.sqrt(5)-1)/2,t=2*p*p,mu=num(originalMu),hv=num(h);
const eps=Math.sqrt(mu*(mu-hv)),lamLo=mu-eps,lamHi=mu+eps;
const aLo=(1-t*lamLo),aHi=(1-t*lamHi);
const wLo=(mu+eps)/(2*mu),wHi=(mu-eps)/(2*mu);
const qBlank=wLo*aLo*aLo+wHi*aHi*aHi;
const q00=wLo*aLo**4+wHi*aHi**4;
const corrDirect=q00-qBlank**2;
const covariance=4*t*t*hv*(mu-hv)*(1-t*mu)**2;
ok(Math.abs(corrDirect-covariance)<1e-14,
   'literal K00=B=I-2p²Delta: native stationary blank covariance formula');
ok(corrDirect>num(deltaLower),'actual CAR16 source positive beyond rigorous rational bound');
const source=4*t*t*((1-t*mu)**2*num(HGp)-2*t*(1-t*mu)*num(HG)*num(muP));
ok(source>0.000013,'original proper Lorentz boost native two-round covariance SOURCE positive');
const binJoint=[
 [q00,qBlank-q00],
 [qBlank-q00,1-2*qBlank+q00]];
const qb=[qBlank,1-qBlank];
let binaryMI=0;
for(let i=0;i<2;i++)for(let j=0;j<2;j++){
 const v=binJoint[i][j];
 ok(v>0,'native binary coarse two-round POSITIVE event');
 binaryMI+=v*Math.log(v/(qb[i]*qb[j]));
}
ok(binaryMI>num(miLower),'native actual blank/nonblank two-round MI beats Pinsker lower bound');
const tv=.5*binJoint.flatMap((r,i)=>r.map((x,j)=>Math.abs(x-qb[i]*qb[j]))).reduce((s,x)=>s+x,0);
ok(Math.abs(tv-2*covariance)<1e-13,'binary coarsening TV=2 native blank covariance');
ok(binaryMI>=2*tv*tv-1e-13,'KL Pinsker 2TV² lower bound native');
console.log(JSON.stringify({status:"PASS_EXACT_NATIVE_FULL128_TWO_STEP_INFO_WALL",checks,
 originalNativeOwner:"d0_native_preparation_closure_2026-10-21/PROOF.md §7",
 originalK00:"B=I-2p² A²; complete native full128 oldRIGHT remains spectator",
 exactMu:s(originalMu),exactHarmonic:s(h),muDerivative:s(muP),
 HGapDerivative:s(HGp),
 full128StationaryBlankProbability:qBlank,
 full128StationaryTwoBlankProbability:q00,
 rigorousBlankCovarianceLower:num(deltaLower),
 actualBlankCovariance:covariance,actualPositiveLorentzBoostDerivative:source,
 rigorousFull128PairMutualInfoLower:num(miLower),
 coarseFull128TwoRoundBinaryMutualInfo:binaryMI,
 predictiveInfoLower:"I_pred≥I(Y0;Y1)≥8(q00-q0²)^2",
 actualFull128OtherLabelCensusNotRerun:true,
 fullOriginalBook03InfoNotDerived:true,
 GR_closed:false},null,2));
