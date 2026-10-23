// ORIGINAL CAR16/full128 spectrum: proven literal Golden/Kraus
// K0=I-2p² Delta, true Fourier/role1 proper boost, true oldRIGHT128.
// NEW fixed RATIONAL degree8 polynomial: recentered negative-binomial
// filter for n=130 actual paid Kraus ALLBLANK events.
// Uniform any DATA×RIGHT fidelity error<8e-14, success>.03798,
// all-field moving actual inverse-square DATA preparation source<2.6e-13.
// NO gate implementation or Book03 physical Info selected.
// Independent arithmetic Galois certificate native Golden angle irrational,
// and literal naive LCU B^j 1-norm >5e14, meaning *that algorithm*
// has herald success <4e-30 vs quantum filter's mathematical 3.8%.
// No physical QSVT compiler or 42-field root rerun is claimed.
import assert from 'node:assert/strict';
let checks=0;const ck=(x,m)=>{assert.ok(x,m);checks++};
const almost=(x,y,t=2e-12,m='close')=>ck(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
const ab=x=>x<0n?-x:x;
function gcd(a,b){a=ab(a);b=ab(b);while(b){const t=a%b;a=b;b=t}return a||1n}
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);ck(b!==0n,'rational nonzero denominator');
 if(b<0n){a=-a;b=-b}const g=gcd(a,b);return {a:a/g,b:b/g}}
const plus=(x,y)=>Q(x.a*y.b+y.a*x.b,x.b*y.b);
const minus=(x,y)=>plus(x,Q(-y.a,y.b));
const mul=(x,y)=>Q(x.a*y.a,x.b*y.b);
const div=(x,y)=>Q(x.a*y.b,x.b*y.a);
const pow=(x,n)=>Q(x.a**BigInt(n),x.b**BigInt(n));
const lt=(x,y)=>x.a*y.b<y.a*x.b;
const gt=(x,y)=>x.a*y.b>y.a*x.b;
const eq=(x,y)=>x.a*y.b===y.a*x.b;
// Convert BIGINT rational to diagnostic double without Infinity/Infinity;
// strict inequalities above always use cross-multiplied ORIGINAL integers.
function num(x){if(x.a===0n)return 0;
 const neg=x.a<0n,na=(neg?-x.a:x.a).toString(),nb=x.b.toString();
 const va=na.slice(0,16),vb=nb.slice(0,16);
 const v=Number(va)/Number(vb) *10**((na.length-va.length)-(nb.length-vb.length));
 return neg?-v:v;
}
function choose(n,k){n=BigInt(n);k=BigInt(k);let a=1n;for(let j=1n;j<=k;j++)a=a*(n-k+j)/j;return a}
const ONE=Q(1),TENTH=Q(1,10),TWELVE=Q(3,25),p=(Math.sqrt(5)-1)/2,phi=1/p,t=2*p*p;
const ra=minus(ONE,pow(TWELVE,2)),rb=minus(ONE,pow(TENTH,2));
const pUpper=plus(minus(minus(Q(5),TENTH),mul(Q(8),pow(TENTH,2))),plus(pow(TWELVE,3),mul(Q(5),pow(TWELVE,4))));
const pLower=minus(minus(Q(5),mul(Q(8),pow(TWELVE,2))),TWELVE);
const muUpper=div(mul(Q(9),pUpper),mul(Q(3200),pow(ra,2)));
const muLower=div(mul(Q(9),pLower),mul(Q(3200),pow(rb,2)));
const epsPolyUpper=plus(Q(3),plus(mul(Q(4),pow(TWELVE,5)),mul(Q(2),pow(TWELVE,6))));
const epsSquared=div(mul(mul(Q(81),pow(TWELVE,2)),epsPolyUpper),mul(Q(10240000),pow(ra,4)));
ck(gt(muLower,Q(1367,100000))&&lt(muUpper,Q(14,1000)),
 'old original native exact μ(r) enclosed in (0.01367,0.014) on WHOLE real boost interval');
ck(lt(epsSquared,pow(Q(61,100000),2)),
 'original exact CAR16 discriminant bound eps<0.00061 across whole proper boost interval');
ck(t>.76&&t<.8,
 'native p fixed, beta=2p² no temperature fit');
const xlo=mul(Q(76,100),minus(Q(1367,100000),Q(61,100000)));
const xhi=mul(Q(8,10),plus(Q(14,1000),Q(61,100000)));
ck(gt(xlo,Q(99,10000))&&lt(xhi,Q(117,10000)),
 'STRICT rational ORIGINAL entire band x=2p²lambda in (.0099,.0117)');
const x0=Q(27,2500),rad=Q(9,10000),b0=minus(ONE,x0),a=div(rad,b0),c=pow(Q(79,80),130);
ck(eq(a,Q(9,9892))&&eq(div(c,pow(b0,130)),pow(Q(9875,9892),130)),
 'exact rational native original source center yields positive field-INDEPENDENT coefficients');
ck(gt(minus(x0,rad),Q(0))&&lt(plus(x0,rad),Q(1,80)),
 'whole true original native spectrum sits in small rational centered chart');
const n=130,K=8,beta=2*p*p;
const b=div(c,pow(b0,n)),first=mul(pow(a,K+1),Q(choose(n+K,K+1)));
const Rratio=mul(a,Q(n+K+1,K+2));
const geom=div(first,minus(ONE,Rratio));
const eta=mul(pow(plus(ONE,a),n),geom);
ck(eq(Rratio,Q(1251,98920)),'exact first ignored NB ratio r9→r10');
ck(lt(eta,Q(19,1000000000000000n)),
 'BigInt EXACT entire centered inverse-recovery operator multiplicative error <1.9e-14');
const c2=pow(c,2);
const successL=mul(c2,pow(minus(ONE,eta),2));
const successU=mul(c2,pow(plus(ONE,eta),2));
const pureTrace=div(mul(Q(4),eta),minus(ONE,eta));
ck(gt(successL,Q(3798,100000))&&lt(successU,Q(381,10000)),
 'BigInt TRUE all oldRIGHT input success chance >.03798 and <.0381');
ck(lt(pureTrace,Q(8,100000000000000n)),
 'BigInt ORIGINAL CAR16×oldRIGHT all-state postselected trace distance <8e-14');
const derivativeTail=mul(mul(Q(n+K),Q(choose(n+K-1,K))),
 mul(pow(a,K),pow(plus(ONE,a),n-1)));
ck(lt(derivativeTail,Q(183,1000000000000n)),
 'BigInt exact centered NB tail |dT/dy|<1.83e-10 uniformly');
const preparedBound=mul(c2,
 plus(mul(mul(Q(2),eta),Q(54,100)),mul(mul(Q(2),div(derivativeTail,b0)),Q(18,1000))));
ck(lt(preparedBound,Q(26,100000000000000n)),
 'BigInt ORIGINAL moving rho*=Delta^-1/TrDelta^-1 native field success first source <2.6e-13');
const flagBound=mul(Q(7),preparedBound);
ck(lt(flagBound,Q(19,10000000000000n)),
 'BigInt ORIGINAL Golden 0/10 success-flag reported Price−Info source <1.9e-12');
ck(lt(mul(Q(n),a),ONE),
 'alternating Y<0 series in recentered polynomial has DECREASING terms, so M is POSITIVE contraction');
const betaOld=2*p*p;
function native(r){
 const R=(1-r*r)**2,P=5*r**4+r**3-8*r*r-r+5,
 Qv=23*r**4+6*r**3-32*r*r-10*r+25;
 const m=9*P/(3200*R),d=81*Qv/(10240000*R),
 e=Math.sqrt(m*m-d),G=3-4*r**3-r**4+4*r**5+2*r**6,
 Gp=-12*r*r-4*r**3+20*r**4+12*r**5,
 Pp=20*r**3+3*r*r-16*r-1,
 mr=9/(3200*R)*(Pp+4*r*P/(1-r*r)),
 er=e*(1/r+4*r/(1-r*r)+Gp/(2*G));
 return {r,m,e,mr,er,x:[t*(m-e),t*(m+e)],xp:[t*(mr-er),t*(mr+er)]};
}
function poly(y){
 let C=1,v=1;
 for(let j=1;j<=K;j++){C*=y*(n+j-1)/j;v+=C}
 return v;
}
function tailSigned(y){
 // Explicit convergent unnormalized tail after degree K, including negative y,
 // no subtraction of two near-one numbers.
 let term=1;
 for(let j=1;j<=K+1;j++)term*=y*(n+j-1)/j;
 let ans=0;
 for(let j=K+1;j<K+90;j++){ans+=term;term*=y*(n+j)/(j+1)}
 return Math.pow(1-y,n)*ans;
}
const derivC=(n+K)*Number(choose(n+K-1,K));
function tailPrime(y){return derivC*y**K*(1-y)**(n-1)}
const cm=num(c),bm=num(b),maxError=num(eta),sourcestandard=num(preparedBound);
function prepared(r){
 const x=native(r),s=x.e/x.m,sp=x.er/x.m-x.e*x.mr/x.m**2;
 const w=[(1+s)/2,(1-s)/2],wp=[sp/2,-sp/2];
 const y=x.x.map(v=>(v-num(x0))/num(b0));
 const M=y.map(v=>bm*poly(v));
 const T=y.map(tailSigned);
 const C=y.map(v=>cm*(1-tailSigned(v)));
 const P=cm*cm*w.reduce((a,v,i)=>a+v*(1-T[i])**2,0);
 const source=cm*cm*(wp[0]*((1-T[0])**2-(1-T[1])**2)
     -2*w.reduce((a,v,i)=>a+v*(1-T[i])*tailPrime(y[i])*x.xp[i]/num(b0),0));
 const corr=w.reduce((sum,wi,i)=>sum+wi*(-2*T[i]+T[i]**2),0);
 return {r,x,w,wp,y,M,T,C,P,source,corr};
}
const sample=[.1,.105,1/9,.115,.12].map(prepared);
for(let k=0;k<=80;k++){
 const r=.1+.02*k/80,v=prepared(r);
 ck(v.x.x.every(x=>x>.0099&&x<.0117),
  'full actual 16 CAR native spectrum satisfies strict centered source envelope without fitted eigenvalues');
 ck(v.M.every(x=>x>0&&x<1),'fixed DEGREE8 native centered polynomial is CP-positive/Kraus contraction on real entire original chart');
 ck(v.T.every(x=>Math.abs(x)<maxError)&&v.C.every(x=>Math.abs(x-cm)<=cm*maxError+2e-14),
  'native K0^130 and positive polynom almost exactly restores ANY unknown input amplitude');
 ck(v.P>num(successL)-2e-15&&v.P<num(successU)+2e-15,
  'native full original inverse-square moving prep herald chance inside exact source bound');
 ck(Math.abs(v.wp[0])+Math.abs(v.wp[1])<.54&&
    v.x.xp.every(v=>Math.abs(v)<.018),
  'whole original native moving reference and Lorentz field first jet enclosed');
 ck(Math.abs(v.source)<sourcestandard,
  'original unaltered moving DATA prep source |dPsuccess/dr|<2.6e-13, not frozen');
 const flag=1-Math.log((1-v.P)/v.P)/Math.log(phi);
 ck(Math.abs(flag)<7&&Math.abs(flag*v.source)<num(flagBound),
  'original additional Golden report 0/10 Price−Info source <1.9e-12');
 const h=2e-4,l=prepared(r-h),u=prepared(r+h);
 const fd=cm*cm*(u.corr-l.corr)/(2*h);
 ck(Math.abs(fd-v.source)<2e-14,
  'INDEPENDENT finite difference of stable small correction including moving rho* source');
}
// EXACT failure of the NAIVE finite LCU compiler, despite high ideal filter
// success. P8(1-B/b0) has alternating and HUGE coefficients in B powers.
// Their absolute norm is EXACTLY b Σ_k binom(n+k-1,k) (1+1/b0)^k,
// not the O(1) spectral norm on the narrow actual native band.
let naiveLCUnorm=Q(0);
for(let k=0;k<=K;k++)
 naiveLCUnorm=plus(naiveLCUnorm,mul(Q(choose(n+k-1,k)),
             pow(Q(4973,2473),k)));
naiveLCUnorm=mul(naiveLCUnorm,b);
ck(gt(naiveLCUnorm,Q(500000000000000n)),
 'BigInt literal unamplified coherent native B^j LCU coefficient 1-norm>5e14');
const lcuProbabilityUpper=1/(num(naiveLCUnorm)**2);
ck(lcuProbabilityUpper<4e-30&&lcuProbabilityUpper>0,
 'specific naive LCU unamplified success cannot compete with mathematically valid physical CP filter; not a universal compiler no-go');
// Original Golden angle θ satisfies cosθ=sqrt(p), sinθ=p:
// t_φ=2cos(2θ)=4p−2=2√5−4, exact monic polynomial t²+8t−4=0;
// conjugate =−2sqrt5−4<-2, impossible for any root-of-unity angle.
const angle=Math.atan2(p,Math.sqrt(p)),ratio=angle/Math.PI;
const omega=4*p-2,conj=-4-2*Math.sqrt(5);
almost(omega**2+8*omega-4,0,1e-13,
 'Galois exact native original 2cos2θ algebraic-integer polynomial X²+8X−4');
ck(conj < -2 && omega> -2&&omega<2,
 'non-unit-circle REAL algebraic conjugate certifies original Golden θ/π IRRATIONAL');
ck(Math.abs(Math.cos(angle)-Math.sqrt(p))<1e-14&&Math.abs(Math.sin(angle)-p)<1e-14,
 'original native Golden gate rotation angle exactly constructed');
const o={
 status:"PASS_ORIGINAL_NATIVE_CAR16_DEGREE8_CENTERED_ECHO_AND_GALOIS_PHASE",
 checks,
 source:"old original full128 Fourier CAR16 K0=I-2p²Delta, true r∈[1/10,3/25]",
 exactRational:{
  x0:"27/2500",xHalfWidth:"9/10000",yHalfWidth:"9/9892",
  fixedScalar:"(79/80)^130",centeredPrefactor:"(9875/9892)^130",
  binomialOrder:n,degree:K,
  uniformMultiplicativeRecoveryErrorUpper:num(eta),
  uniformAnyEntangledOldRIGHTTraceDistanceUpper:num(pureTrace),
  successLower:num(successL),successUpper:num(successU),
  movingStationaryDATAFieldSourceUpper:num(preparedBound),
  nativeGoldenSuccessFlagSourceUpper:num(flagBound)
 },
 sourceSamples:sample,
 naiveLCU:{coeffNorm:num(naiveLCUnorm),specificUnamplifiedSuccessUpper:lcuProbabilityUpper,
  highEfficiencyCPFilterStillExistsMathematically:true},
 nativeGalois:{angleRadians:angle,ratioThetaPi:ratio,
  twoCosTwoTheta:omega,conjugate:conj,minimalPoly:"X²+8X−4",
  irrationalThetaPi:true,
  ifQ8QuarterTurnRoutedOnSameActivePort:"{G,S=diag(1,i)} closure SU(2) dense",
  nativePhysicalPhaseAndJuliaControlledUnitaryCompilationProved:false},
 fullOriginalFull128Book03PhysicalHodgeSelected:false,
 nativeFilterPhysicallyCompiled:false,
 originalH4Unpadded42SourceRecomputed:false,GR_closed:false
};
console.log(JSON.stringify(o,null,2));
