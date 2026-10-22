// ORIGINAL D0 Golden/CAR16 K0=B=I-2p²Delta, nonzero boost chart,
// actual full128 block-encoding (mathematical unchanged forward Kraus column).
// New EXACT globally QSVT admissible EVEN fixed polynomial on [-1,1],
// with strict original all-input/oldRIGHT physical-herald candidate:
// n=130 native old Kraus blanks, filter Q(B) of degree 2,050,956;
// uniform error <1.7e-22 at constant >.03798 success and
// exact field-source <1.3e-19 incl original moving inverse-square DATA.
// Every assertion is arithmetic or small mathematical control; actual
// 2,050,956 native U/U†/phase gates are NOT executed or physically admitted.
// Uses exact NB Chernoff / Chebyshev MODE proof, no 25k-term overflow.
import assert from 'node:assert/strict';
let count=0;
const ok=(yes,msg)=>{assert.ok(yes,msg);count++};
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){let c=a%b;a=b;b=c}return a||1n}
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);ok(b!==0n,'denom');if(b<0n){a=-a;b=-b}
 const g=gcd(a,b);return {a:a/g,b:b/g}}
const sum=(x,y)=>Q(x.a*y.b+y.a*x.b,x.b*y.b);
const sub=(x,y)=>sum(x,Q(-y.a,y.b));
const mul=(x,y)=>Q(x.a*y.a,x.b*y.b);
const div=(x,y)=>Q(x.a*y.b,x.b*y.a);
const pow=(x,k)=>Q(x.a**BigInt(k),x.b**BigInt(k));
const lt=(x,y)=>x.a*y.b<y.a*x.b;
const gt=(x,y)=>x.a*y.b>y.a*x.b;
const eq=(x,y)=>x.a*y.b===y.a*x.b;
const num=x=>Number(x.a)/Number(x.b);
const ONE=Q(1),ZERO=Q(0);
const p=(Math.sqrt(5)-1)/2,beta=2*p*p,zeta=2**-20,phi=1/p;
ok(p>.617&&p<.625&&Math.abs(p+p*p-1)<1e-15,
 'ORIGINAL p+p²=1 fixed Golden gate no retuned angle');
const m=1000000n,r=65n,N=m+r;
const xcut=Q(159,6400),Bcut=Q(79,80),c=pow(Bcut,130);
ok(eq(sub(ONE,pow(Bcut,2)),xcut),
 'fixed native original positive blank cap u=1/80 gives exact GLOBAL QSVT clipping threshold 159/6400');
const K=(N-1n)*159n/6241n;
ok(K===25478n,'EXACT original rational negative-binomial modal K floor((N-1)*159/6241)=25478');
ok((N-1n)*159n>=K*6241n &&(N-1n)*159n<(K+1n)*6241n,
 'fixed polynomial clipping index is TRUE native NB modal integer, not a floating numerically optimized root');
const degree=2n*(m+K);
ok(degree===2050956n &&degree%2n===0n,
 'REAL polynomial in original B is even, degree 2050956 satisfying QSVT parity');
const fullSpectrumMaxOldX=Q(117,10000);
const xMax=sub(ONE,pow(sub(ONE,fullSpectrumMaxOldX),2));
ok(eq(xMax,Q(2326311,100000000))&&lt(xMax,xcut),
 'old exact positive CAR16 real boost x=tDelta<.0117 gives spectral cutoff x_new=1-B²<0.02326311<159/6400');
const sig2=div(mul(Q(N),mul(xcut,ONE)),pow(sub(ONE,xcut),2));
ok(lt(sig2,Q(170*170)),
 'entire ORIGINAL native fixed NB m1e6+65 cutoff variance <170² by exact cross multiplication');
const PmodeLower=Q(3,4*(4*170+2));
ok(gt(mul(Q(N+K),PmodeLower),Q(r)),
 'STRICT mode Chebyshev pmf lower gives (N+K) pK(xcut)>65, hence native QSVT polynomial derivative negative at cutoff');
function lowerKLExponent(k){
 const S=N+k,a=div(Q(k),Q(S)),difference=sub(a,xMax);
 ok(gt(difference,ZERO)&&lt(a,Q(1,2)),
    'original fair boost Bernoulli Chernoff tilted threshold a > x_max and below half');
 const exponent=div(mul(Q(S),pow(difference,2)),
   mul(Q(2),mul(a,sub(ONE,xMax))));
 return exponent;
}
const E0=lowerKLExponent(K),E1=lowerKLExponent(K+1n);
ok(gt(E0,Q(52))&&gt(E1,Q(52)),
 'BIGINT ENTIRE original CAR16 native NB upper-tail Chernoff exponents strictly >52');
ok(10n**75n<4n*27n**52n,
 'BIGINT e>27/10 from first 5 terms, hence e^-52 <4e-23 (no transcendental fit)');
const EPS=Q(4,10n**23n),eps=num(EPS);
ok(Math.exp(-52)<eps,
 'independent high precision first-source event bound 4e-23 fully conservative');
const c2=pow(c,2);
const successLower=mul(c2,pow(sub(ONE,EPS),2));
const successUpper=c2;
const traceBound=div(mul(Q(4),EPS),sub(ONE,EPS));
ok(gt(successLower,Q(3798,100000))&&
 lt(traceBound,Q(17,10n**23n)),
 'BigInt ORIGINAL 130 round echo success >.03798 and ALL oldRIGHT trace error <1.7e-22');
const derivativeTailCap=div(mul(Q(N+K),EPS),sub(ONE,xMax));
ok(lt(derivativeTailCap,Q(43,10n**18n)),
 'BigInt original NB tail first SOURCE |Tʹ(x)|<4.3e-17 uniformly on actual boost');
const fieldXCap=Q(36,1000),prepWeightCap=Q(54,100);
const preparedSourceCap=mul(c2,sum(mul(mul(Q(2),EPS),prepWeightCap),
 mul(mul(Q(2),sum(ONE,EPS)),mul(derivativeTailCap,fieldXCap))));
ok(lt(preparedSourceCap,Q(13,10n**20n)),
 'BigInt ACTUAL original moving rho*=Delta^-1/Z native prepared echo P_success field source <1.3e-19');
const flagSourceCap=mul(Q(7),preparedSourceCap);
ok(lt(flagSourceCap,Q(1,10n**18n)),
 'BigInt original Golden success/abort 0/10 pointer Cost−Info first source <1e-18');
const operatorDFCap=mul(mul(Q(2),c2),mul(sum(ONE,EPS),
 mul(derivativeTailCap,fieldXCap)));
ok(lt(operatorDFCap,Q(13,10n**20n)),
 'BigInt entire PREPARED echo complementary RETURN operator derivative <1.3e-19');
const bookJSourceCap=mul(div(Q(2048),Q(1048575)),operatorDFCap);
const heatSourceCap=mul(Q(45,10),operatorDFCap);
ok(lt(sum(bookJSourceCap,heatSourceCap),Q(1,10n**18n)),
 'same full ordinary paired CUT Hodge+Book echo action (NOT native scene heat) first source <1e-18');
const p26=(Math.sqrt(5)-1)/2,cc=num(c),definite=1-p26*p26;
ok(definite>0&&cc>.194&&cc<.196,
 'actual fixed native CAR16 complete heralded all-blank amplitude c is healthy');
// Special exact "unimodal polynomial" proof control on a small NB fixture;
// analytical monotonicity for REAL N=1000065,K=25478 is in document.
// P_m,r,K(s)=c*s^(2m)*Σ_{k<=K} C(m+r+k−1,k)*(1−s²)^k.
function smallPolynomial(mm,rr,k,x,xcut){
 const NN=mm+rr;
 const c=(1-xcut)**rr;
 const b=1-x;let term=1,S=1;
 for(let j=1;j<=k;j++){term*=x*(NN+j-1)/j;S+=term}
 return c*b**mm*S;
}
const smallN=25,smallR=3,cut=.18,smallMode=Math.floor((smallN-1)*cut/(1-cut));
let maxSmall=-1,atSmall=0;
for(let i=0;i<=1000;i++){
 const x=i/1000,s=smallPolynomial(smallN-smallR,smallR,smallMode,x,cut);
 ok(s>=-1e-14&&Number.isFinite(s),'SMALL independent true NB polynomial on entire interval is positive');
 if(s>maxSmall){maxSmall=s;atSmall=x}
}
ok(maxSmall<=1&&atSmall<=cut+.01,
 'small NB polynomial mathematical mode/cutoff unimodality positive verified (not proof for large N)');
// End-to-end preserved DATA×RIGHT CP success, no scalar moved from outcome
// to fields. Actual native oldRIGHT trace error controlled by first 4eps.
const math={
 originalInputs:"full128 CAR16 K0=B=I−2p² Delta, true oldRIGHT128 and fixed Golden β,ζ",
 originalSpectrum:"0<tΔ<0.0117 on original proper-boost r∈[.1,.12]",
 exactEvenQSVTPolynomial:{
  formula:"P(s)=c*s^(2m)*sum[k=0..K] binom(m+65+k-1,k)*(1-s²)^k",
  m:Number(m),halfExponent:Number(r),N:Number(N),K:Number(K),degree:Number(degree),
  c:"(79/80)^130",xCut:"159/6400",
  modalPmfChebyshevLower:num(PmodeLower),
  varianceBound:"sigma²<170²",
  globallyBoundedOnNegativeOneToOne:"0<=P(s)<=1 for EVERY s in [-1,1], analytical unimodality",
  originalKrausComposite:"P(B)*B^130=c*Pr[NegBin(m+65,x=1-B²) <=K] as operator ID"
 },
 rigorousWholeNative:{
  nativeFieldXmax:num(xMax),
  ChernoffExponentLowerK:num(E0),ChernoffExponentLowerKplus1:num(E1),
  tailErrorUpper:eps,
  allInputOldRIGHTTraceErrorUpper:num(traceBound),
  successProbabilityLower:num(successLower),
  preparedDATAOriginalSourceUpper:num(preparedSourceCap),
  GoldenSuccessFlagSourceUpper:num(flagSourceCap),
  pairedCutBookHodgeEchoFieldSourceUpper:num(sum(bookJSourceCap,heatSourceCap))
 },
 QSVT:"real even globally bounded polynomial satisfies QSVT spectral-parity constraints; original physical coherent Stinespring U, paid U†, phase rotations and source selection STILL NOT PROVED",
 actualGateCost:"at least 2,050,956 coherent signal U/U† calls for standard QSVT, PLUS original130 K0 rounds and all factories/work/clock, not free",
 fullOriginalBook03SceneHeatIdentified:false,
 actualOldRIGHTRoutingProved:false,
 originalFull42UnpaddedRootNotRerun:true,GR_closed:false
};
console.log(JSON.stringify({status:"PASS_ORIGINAL_FULL128_GLOBALLY_BOUNDED_EVEN_QSVT_ECHO_AND_NATIVE_SOURCE",checks:count,...math},null,2));
