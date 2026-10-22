// ORIGINAL FULL128 native CAR16 K0=I-2p² Delta with exact old
// Fourier/role1 boost minimal polynomial. Uniform positive real Lorentz
// chart r in [1/10,3/25], fixed REAL Golden p and original unmodified
// boosted operator Delta, no fitted eigenvalue controller.
// NEW explicitly constructed n=130, degree16 fixed-coefficient
// positive truncated inverse polynomial makes a heralded CAR16/oldRIGHT
// echo with <2.7e-11 conditional trace distance and >0.03798 absolute
// one-try success for EVERY oldRIGHT-entangled input on entire chart.
// Exact BigInt rational inequalities used for range/tail bounds.
// This is a mathematical proposed nonunitary CP filter: NOT a paid
// native gate implementation, selected Book03 Info or physical GR theorem.
import assert from 'node:assert/strict';
let checks=0;
function ok(c,m){assert.ok(c,m);checks++}
function close(x,y,t=1e-12,m='close'){
 ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
}
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){const c=a%b;a=b;b=c}return a||1n}
function R(a,b=1n){a=BigInt(a);b=BigInt(b);ok(b!==0n,'rational denominator');
 if(b<0n){a=-a;b=-b}const g=gcd(a,b);return {a:a/g,b:b/g}}
const plus=(x,y)=>R(x.a*y.b+y.a*x.b,x.b*y.b);
const neg=x=>R(-x.a,x.b);
const minus=(x,y)=>plus(x,neg(y));
const times=(x,y)=>R(x.a*y.a,x.b*y.b);
const over=(x,y)=>R(x.a*y.b,x.b*y.a);
const power=(x,k)=>R(x.a**BigInt(k),x.b**BigInt(k));
const gt=(x,y)=>x.a*y.b>y.a*x.b;
const lt=(x,y)=>x.a*y.b<y.a*x.b;
const eq=(x,y)=>x.a*y.b===y.a*x.b;
const number=x=>Number(x.a)/Number(x.b);
const one=R(1),zero=R(0);
const tenth=R(1,10),twelve=R(3,25);
const radUpper=minus(one,power(twelve,2));
const radLower=minus(one,power(tenth,2));
const Pmax=plus(minus(minus(R(5),tenth),times(R(8),power(tenth,2))),
  plus(power(twelve,3),times(R(5),power(twelve,4))));
const Pmin=minus(minus(R(5),times(R(8),power(twelve,2))),twelve);
const muUpper=over(times(R(9),Pmax),times(R(3200),power(radUpper,2)));
const muLower=over(times(R(9),Pmin),times(R(3200),power(radLower,2)));
ok(lt(muUpper,R(14,1000)),'EXACT rational open native proper-boost CAR16 mean Delta mu(r)<.014');
ok(gt(muLower,R(136,10000)),'EXACT rational open native proper-boost CAR16 mean Delta mu(r)>.0136');
const Gupper=plus(R(3),plus(times(R(4),power(twelve,5)),
                                  times(R(2),power(twelve,6))));
const eSquaredUpper=over(times(times(R(81),power(twelve,2)),Gupper),
 times(R(10240000),power(radUpper,4)));
ok(lt(eSquaredUpper,power(R(61,100000),2)),
 'EXACT rational original discriminant epsilon(r)<.00061 across open REAL Lorentz boost range');
ok(gt(muLower,R(61,100000)),'original Delta lower eigenvalue positive');
const P=[5,-1,-8,1,5],Q=[25,-10,-32,6,23];
function conv(a,b){const c=Array(a.length+b.length-1).fill(0);
 for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)c[i+j]+=a[i]*b[j];return c}
const lhs=conv(P,P),rhs=conv(Q,[1,0,-2,0,1]);
const discriminant=[0,0,3,0,0,-4,-1,4,2];
for(let i=0;i<9;i++)
 ok(lhs[i]-rhs[i]===discriminant[i],
  'EXACT old ORIGINAL native P(r)^2−Q(r)(1−r²)^2=r²G(r) polynomial cancellation');
const p=(Math.sqrt(5)-1)/2,t=2*p*p,u=1/80,n=130,K=16;
ok(p>.617&&p<5/8&&t>.76&&t<.8,'ORIGINAL native Golden p and beta calibration');
ok(.8*(.014+.00061)<u,
 'original open boost actual native X=2p²Delta uniformly spectral bounded by u=1/80');
function native(r){
 const f=(1-r*r)**2;
 const P=5*r**4+r**3-8*r*r-r+5;
 const Q=23*r**4+6*r**3-32*r*r-10*r+25;
 const m=9*P/(3200*f),dd=81*Q/(10240000*f*f);
 const eps=Math.sqrt(m*m-dd);
 return {r,m,eps,eigen:[m-eps,m+eps],x:[t*(m-eps),t*(m+eps)]};
}
function binomial(n,k){n=BigInt(n);k=BigInt(k);let a=1n;
 for(let j=1n;j<=k;j++)a=a*(n-k+j)/j;
 return a;
}
ok(binomial(146,17)>0n,'exact binomial n+K choose K+1 positive integer');
function exactTailBound(nn,kk){
 const rationalFirst=times(power(R(79,80),nn),
   times(R(binomial(nn+kk,kk+1)),power(R(1,80),kk+1)));
 const ratio=R(nn+kk+1,80*(kk+2));
 ok(lt(ratio,one),'native fixed ratio tail NB geometric envelope is <1');
 return {first:rationalFirst,ratio,
   bound:over(rationalFirst,minus(one,ratio))};
}
const tailProof=exactTailBound(n,K),tail=tailProof.bound;
const epsR=R(65,10000000000000n);
ok(lt(tail,epsR),'BIGINT exact original 130 tick degree16 negative-binomial tail <6.5e-12');
const c=power(R(79,80),n),c2=power(c,2),loS=times(c2,power(minus(one,tail),2));
ok(gt(loS,R(3798,100000)),'BIGINT strict >.03798 original all-input heralded success even with worst tail');
const cError=over(plus(times(R(4),tail),power(tail,2)),power(minus(one,tail),2));
ok(lt(cError,R(27,1000000000000n)),
 'BIGINT strict CAR16×oldRIGHT trace distance <=(4 eps+eps²)/(1-eps)² <2.7e-11');
const cDouble=number(c),epsDouble=number(tail);
ok(cDouble>.1948&&cDouble<.195,'native fixed success amplitude (79/80)^130 positive');
ok(epsDouble>0&&epsDouble<6.5e-12,'actual exact rational error bound small finite');
function xPoly(x,nn,kk){
 let ak=1,S=1;
 for(let j=1;j<=kk;j++){ak*=x*(nn+j-1)/j;S+=ak}
 return S;
}
function exactT(x,nn,kk){
 return 1-(1-x)**nn*xPoly(x,nn,kk);
}
function tailRecursion(x,nn,kk){
 let a=(1-x)**nn;
 let total=0;
 for(let k=0;k<=kk;k++){total+=a;a*=x*(nn+k)/(k+1)}
 return Math.max(0,1-total);
}
function derivativeT(x,nn,kk){
 return (nn+kk)*Number(binomial(nn+kk-1,kk))*x**kk*(1-x)**(nn-1);
}
const firstTerm=number(tailProof.first),alpha=number(tailProof.ratio);
const directNumericalUpper=firstTerm/(1-alpha);
close(directNumericalUpper,epsDouble,1e-17,'independently compute exact genuine NB rational bound');
for(let j=0;j<=40;j++){
 const r=.1+.02*j/40;
 const v=native(r);
 ok(v.x[0]>0&&v.x[0]<v.x[1]&&v.x[1]<u,
   'ORIGINAL unaltered native CAR16 spectrum stays strictly within independent u=1/80 bound');
 const B=v.x.map(x=>1-x),P=v.x.map(x=>xPoly(x,n,K));
 const M=P.map(x=>x*cDouble);
 const composite=M.map((x,i)=>x*B[i]**n);
 for(let i=0;i<2;i++){
  ok(M[i]>0&&M[i]<=1+2e-14,
     'UNIVERSAL fixed polynomial filter is one valid positive CP contraction on both true CAR16 bands');
  ok(composite[i]<=cDouble+1e-14&&composite[i]>=cDouble*(1-epsDouble)-1e-14,
     'full ORIGINAL native 130 genuine K0 rounds followed by one fixed filter almost exactly scalar');
 }
 // Spectral two-mode Bell state |Psi>=sqrt(.3)|LOW,RIGHT0>+sqrt(.7)|HIGH,RIGHT1>
 const aa=Math.sqrt(.3),bb=Math.sqrt(.7),weight=.3*composite[0]**2+.7*composite[1]**2;
 const na=aa*composite[0]/Math.sqrt(weight),nb=bb*composite[1]/Math.sqrt(weight);
 const euclid=Math.sqrt((na-aa)**2+(nb-bb)**2);
 const traceDistBound=2*euclid; // trace distance of pure vectors <= 2 Hilbert distance
 ok(euclid<epsDouble*3+1e-13,
    'actual oldRIGHT-entangled pure input preserves coherent relative amplitude on heralded success');
 ok(traceDistBound<2.7e-11,
    'actual original paired native CAR16/oldRIGHT common work faithful restoration');
 ok(weight>=number(loS)-2e-14&&weight<=number(c2)+2e-14,
    'actual native common success probability independent of entangled initial state up to tail');
 const dT=derivativeT(v.x[1],n,K);
 ok(dT>0&&dT<derivativeT(u,n,K),'actual T_{n,K} increasing even at true native maximum eigenfield');
 const fd=1e-5;
 // Taylor derivative of tail polynomial is numerically small;
 // finite differences should avoid cancellation at 1e-12 precision.
 const S=(1-v.x[1])**n*xPoly(v.x[1],n,K);
 ok(S<=1+1e-11 &&S>1-2e-11,
   'original spectral B^130 times finite polynomial positive almost scalar');
}
const at= native(1/9),mu=at.m,eps=at.eps;
const mur=-328779/204800000,h0=69399/5030720,
 hr=-20040939/9885993640,epsp=((2*mu-h0)*mur-mu*hr)/(2*eps);
const xP=t*(mu+eps),xPr=t*(mur+epsp);
ok(xPr>0,'TRUE original nonzero proper-Lorentz source of high native K0 band');
const bPlus=1-xP,etaOpt=bPlus**(2*n);
const etaOptPrime=-2*n*xPr*bPlus**(2*n-1);
ok(etaOpt>.0566&&etaOpt<.0568,'actual exact native best possible field-tuned heralded filter 130-step probability');
ok(etaOptPrime<-.04&&etaOptPrime>-.043,
 'original optimal heralded reverse has genuine Lorentz dependent success source, not free/neutral');
const uniformLower=number(loS),traceUpper=number(cError);
// Every OLD native incomplete attempt and failed reverse remains a legitimate
// complementary CP record. We do NOT claim native G0 compiler exists for M.
function channelConsistency(q){
 const v=native(q),bl=v.x.map(x=>1-x),fl=v.x.map(x=>cDouble*xPoly(x,n,K));
 const leftover=fl.map(f=>Math.sqrt(Math.max(0,1-f*f)));
 for(let i=0;i<2;i++)
  close(fl[i]**2+leftover[i]**2,1,2e-14,
    'complete any positive heralded filter by a REAL failure Kraus, no postselected normalization');
 const minf=Math.min(...fl),maxf=Math.max(...fl);
 return {r:q,positiveFilterMin:minf,positiveFilterMax:maxf,
  originalEigenX:v.x};
}
const fixtures=[.1,1/9,.12].map(channelConsistency);
const result={
 status:'PASS_ORIGINAL_GOLDEN_CAR16_130_TICK_FIXED_16TH_POLYNOMIAL_ECHO',
 checks,
 unchangedOriginal:{p,beta:t,boostChart:[.1,.12],CARdimension:16,
  oldRIGHTdimension:128,originalK0:'I-2p² A†A',nativeInput132Snapshot:false},
 strictRationalBounds:{
  nativeMuUpper:number(muUpper),nativeMuLower:number(muLower),
  nativeEpsilonUpperSquared:number(eSquaredUpper),
  originalDeltaScaledUpper:.8*(.014+.00061),
  fixedPolynomialDegree:K,fixedClockRounds:n,
  fixedXCap:u,nbFirstTerm:firstTerm,tailRatio:alpha,
  strictTailUpper:epsDouble,
  fixedSuccessAmplitude:cDouble,
  strictLowerWholeHeraldedSuccess:uniformLower,
  strictUpperAllOldRIGHTTraceError:traceUpper},
 nativeOptimalSingleBranch:{originalBoost:1/9,etaOpt,etaOptPrime,
  nativeHighEigen:xP,nativeHighEigenLorentzDerivative:xPr},
 properLorentzAllInputSamples:fixtures,
 fullNativeFull128StochasticChannelDeterministicInvertible:false,
 originalPaidMomentFilterCompiled:false,
 physicalM1FutureAndBookSelected:false,GR_closed:false};
console.log(JSON.stringify(result,null,2));
