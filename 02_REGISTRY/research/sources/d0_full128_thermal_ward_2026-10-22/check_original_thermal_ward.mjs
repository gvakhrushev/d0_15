// Native ORIGINAL full128, exact CAR16 Fourier/role-1 boost rational
// two-band source, genuine two-round K00=B=I-2p^2 Delta / J2=-128 Tr log((1-z)I+zB^4).
// Tests naive raw Delta vs original log-survival effective heat + exact
// inverse-square stationary input. Claims only those mathematical candidates.
// Node builtin assert; no physical Book03 Hodge or full 42-root selection.
import assert from 'node:assert/strict';
let checks=0;
const ok=(x,m)=>{assert.ok(x,m);checks++};
const close=(x,y,t=5e-9,m='close')=>ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){let t=a%b;a=b;b=t}return a||1n}
function R(a,b=1n){a=BigInt(a);b=BigInt(b);ok(b!==0n,'nonzero rational denominator');
 if(b<0n){a=-a;b=-b}const g=gcd(a,b);return {a:a/g,b:b/g}}
const plus=(a,b)=>R(a.a*b.b+b.a*a.b,a.b*b.b);
const neg=a=>R(-a.a,a.b);
const minus=(a,b)=>plus(a,neg(b));
const mult=(a,b)=>R(a.a*b.a,a.b*b.b);
const divide=(a,b)=>R(a.a*b.b,a.b*b.a);
const square=a=>mult(a,a);
const pow=(a,n)=>{let v=R(1);while(n--)v=mult(v,a);return v};
const gt=(a,b)=>a.a*b.b>b.a*a.b;
const lt=(a,b)=>a.a*b.b<b.a*a.b;
const eq=(a,b)=>a.a*b.b===b.a*a.b;
const value=a=>Number(a.a)/Number(a.b);
const format=a=>a.a+'/'+a.b;
const one=R(1),zero=R(0),r0=R(1,9);
function nativeExact(r){
 const r2=square(r),r3=mult(r2,r),r4=square(r2);
 const a=plus(plus(plus(plus(mult(R(5),r4),r3),mult(R(-8),r2)),neg(r)),R(5));
 const da=plus(plus(plus(mult(R(20),r3),mult(R(3),r2)),mult(R(-16),r)),R(-1));
 const b=plus(plus(plus(plus(mult(R(23),r4),mult(R(6),r3)),mult(R(-32),r2)),mult(R(-10),r)),R(25));
 const db=plus(plus(plus(mult(R(92),r3),mult(R(18),r2)),mult(R(-64),r)),R(-10));
 const f=oneMinusR2(r),den=square(f);
 const mu=divide(mult(R(9),a),mult(R(3200),den));
 const d=divide(mult(R(81),b),mult(R(10240000),den));
 const der=(m,dm,scale,n)=>divide(mult(scale,plus(dm,divide(mult(mult(R(4),r),m),f))),mult(n,den));
 const mup=der(a,da,R(9),R(3200));
 const dp=der(b,db,R(81),R(10240000));
 const h=divide(d,mu);
 const hp=divide(minus(mult(dp,mu),mult(d,mup)),square(mu));
 const W=minus(mult(minus(mult(R(2),mu),h),mup),mult(mu,hp));
 const B=minus(mult(h,mup),mult(mu,hp));
 return {mu,d,h,mup,dp,hp,W,B};
}
function oneMinusR2(r){return minus(one,square(r))}
const x=nativeExact(r0);
ok(eq(x.mu,R(141489,10240000)),"exact original native mu fixture");
ok(eq(x.h,R(69399,5030720)),"exact original invariant inverse-square h fixture");
ok(eq(x.mup,R(-328779,204800000)),"exact original proper-Lorentz mu source");
ok(eq(x.hp,R(-20040939,9885993640)),"exact original moving preparation R source");
ok(eq(x.B,R(6042018339,1030291456000000)),"exact prior original rank-two port source B*");
ok(gt(x.W,zero)&&lt(x.W,R(6,1000000)),"true original CAR16 epsilon^2 source W positive <6e-6");
ok(gt(x.mu,R(138,10000))&&lt(x.mu,R(14,1000)),"native rational mean bracket");
ok(gt(x.h,R(13795,1000000))&&lt(x.h,R(138,10000)),"native rational harmonic bracket");
ok(gt(minus(x.mu,x.h),R(22,1000000)),"native two-eigenmode strict split");
ok(lt(x.mup,R(-160,100000))&&gt(x.mup,R(-161,100000)),"native mu_r rational bounds");
ok(lt(x.hp,R(-202,100000))&&gt(x.hp,R(-203,100000)),"native h_r rational bounds");
ok(lt(minus(x.hp,x.mup),R(-421,1000000)),"native joint H+R source base <-.000421");
const epsilonSquared=mult(x.mu,minus(x.mu,x.h));
ok(gt(epsilonSquared,square(R(55,100000)))&&lt(epsilonSquared,square(R(56,100000))),
 "actual original rho spectral ε in (.00055,.00056) from exact rational");
const p=(Math.sqrt(5)-1)/2,t=2*p*p,beta=t,z=2**-20,c=4*p**3;
ok(p>.617&&p<.620&&beta>.76&&beta<.8,"original Golden p and beta strict brackets");
ok(z<1e-6&&z>0,"original GOLDEN fugacity 2^-20 positive fixed");
const mu=value(x.mu),h=value(x.h),mup=value(x.mup),hp=value(x.hp),
 e=Math.sqrt(value(epsilonSquared)),ep=value(x.W)/(2*e);
const lamM=mu-e,lamP=mu+e,lmp=mup-ep,lpp=mup+ep;
ok(ep>0&&lmp<0&&lpp>0,"actual proper-Lorentz spectrum splits in two directions");
ok(0<lamM&&lamP<1/t,"true original blank B positive spectra");
const Q=lam=>1-z+z*(1-t*lam)**4;
const fj=lam=>-Math.log1p(-z*(1-(1-t*lam)**4));
const fd=lam=>4*z*t*(1-t*lam)**3/Q(lam);
const fdd=lam=>-4*z*t*t*(1-t*lam)**2*(3*(1-z)-z*(1-t*lam)**4)/Q(lam)**2;
ok(fd(lamM)>fd(lamP)&&fd(lamP)>0&&fdd(lamM)<0&&fdd(lamP)<0,
 "true original feedback f positive derivative and strict concavity");
const J=1024*(fj(lamM)+fj(lamP));
const Jp=1024*(fd(lamM)*lmp+fd(lamP)*lpp);
ok(Jp<0,"actual 128 RIGHT x full16 two round feedback original boost source STRICT NEGATIVE");
const Hraw=Math.log(16)/beta-mu+Math.log(Math.cosh(beta*e))/beta;
const Hrawp=-mup+Math.tanh(beta*e)*ep;
const Hsurv=Math.log(16*(1-t*mu))/t;
const Hsurvp=-mup/(1-t*mu);
const Rnative=h,Rp=hp;
ok(Hrawp>0&&Hsurvp>0,"bare two native positive heat sources nonzero");
ok(Hrawp+Jp>0&&Hsurvp+Jp>0,"BARE Book H+J source remains nonstationary");
ok(Hrawp+Jp+Rp<-.0004186,"old DATA inverse-square full raw HJR strict Lorentz Ward obstruction");
ok(Hsurvp+Jp+Rp<-.00039,"old DATA inverse-square full genuine log-survival HJR strict Lorentz Ward obstruction");
const HrawBound=value(minus(x.hp,x.mup))+.8*value(x.W)/2;
ok(HrawBound<-.0004186,"native exact rational H+R raw bound from tanh x<x");
const survBound=-.00202+.00161/(1-.8*.014);
ok(survBound<-.00039,"native h'_r, mu'_r, B survival fully rigorous sign bound");
// No single-port visible source: exact v=dr - (nu hp)/(2 h) dnu.
const nu=.6,nuV=-nu*hp/(2*h),muV=value(x.B)/h;
ok(muV>.00042&&muV<.00044,"original 2-parameter one-port-null mu change strict rational");
const epsV=(2*mu-h)*muV/(2*e);
ok(epsV>0&&epsV<.006,"original invisible true two-mode spectral derivative");
const Jv=1024*(fd(lamM)*(muV-epsV)+fd(lamP)*(muV+epsV));
const Hrawv=-muV+Math.tanh(beta*e)*epsV;
const Hsurvv=-muV/(1-t*mu);
ok(Math.abs(Jv)<4.24e-5,"uniform original Book full CAR16 RIGHT128 feedback derivative bound");
ok(Hrawv+Jv<-.000375&&Hsurvv+Jv<-.000377,
 "same-native-instrument one-port-invisible HJR source remains strictly nonzero");
// Independent actual native exact source chart function from the published
// ORIGINAL two-band rational μ(r),d(r). Moving ν just multiplies Δ by ν².
function nativeFloat(r,nu2=.6){
 const f=(1-r*r)**2;
 const m=9*(5*r**4+r**3-8*r*r-r+5)/(3200*f);
 const d=81*(23*r**4+6*r**3-32*r*r-10*r+25)/(10240000*f);
 const scale=(nu2/.6)**2;
 return {mu:m*scale,h:d/m*scale};
}
function functionals(r,nu2=.6){
 const {mu:m,h:hh}=nativeFloat(r,nu2),ee=Math.sqrt(m*(m-hh));
 const eig=[m-ee,m+ee];
 const feedback=1024*eig.reduce((s,l)=>s+fj(l),0);
 const heatraw=Math.log(16)/beta-m+Math.log(Math.cosh(beta*ee))/beta;
 const heatsurv=Math.log(16*(1-t*m))/t;
 const effectiveR=hh;
 return {heatraw,heatsurv,feedback,effectiveR,
  fullRaw:heatraw+feedback+effectiveR,
  fullSurv:heatsurv+feedback+effectiveR,
  report:c*hh};
}
const ff=functionals(1/9,.6);
function dNumerical(fun,dx=1e-5){const r0=1/9;return (fun(r0+dx)-fun(r0-dx))/(2*dx)}
const dRaw=dNumerical(r=>functionals(r,.6).fullRaw);
const dSurv=dNumerical(r=>functionals(r,.6).fullSurv);
close(dRaw,Hrawp+Jp+Rp,2e-8,"independent genuine native original proper boost full HJR source");
close(dSurv,Hsurvp+Jp+Rp,2e-8,"independent original log-survival HJR source");
const h0=nativeFloat(1/9,.6).h;
function nuPath(r){return .6*Math.sqrt(h0/nativeFloat(r,.6).h)}
const dReport=dNumerical(r=>functionals(r,nuPath(r)).report);
ok(Math.abs(dReport)<2e-11,"original actual one-port Born probability constant on nonlinear r,nu path");
const dRawV=dNumerical(r=>functionals(r,nuPath(r)).fullRaw);
const dSurvV=dNumerical(r=>functionals(r,nuPath(r)).fullSurv);
close(dRawV,Hrawv+Jv,2e-8,"true original CAR native one-port invisible raw HJR source");
close(dSurvV,Hsurvv+Jv,2e-8,"true original CAR native one-port invisible log-survival HJR source");
ok(Math.abs(nuV+.6*hp/(2*h))<2e-14,"no fitted tangent native r and ν co-transport");
const dnu=dNumerical(nuPath);
close(dnu,nuV,3e-9,"nonlinear exact one-port cost-preserving actual native preparation path");

// THE CANONICAL log-native modular Gibbs repair is already a known,
// previously proven native state/heat reconstruction, NOT a new physical Book selection.
// It makes the independent heat Euler rho-Gibbs identically 0, but NOT the
// full moving Lorentz field Euler of the SAME unmodified original J2.
const sRatio=e/mu;
const dsRatio=epsV/mu-e*muV/(mu*mu);
const qHigh=(1+sRatio)/2;
const Hbinary=x=>-x*Math.log(x)-(1-x)*Math.log1p(-x);
const nativeEntropy=Math.log(8)+Hbinary(qHigh);
const modularValue=nativeEntropy/beta;
const modularSource=-Math.atanh(sRatio)*dsRatio/beta;
const modularAnalytic=-Math.atanh(sRatio)*h*muV/(2*beta*mu*mu*sRatio);
close(modularSource,modularAnalytic,3e-14,
  'canonical true original DATA log-modular whole 16-eigenspace entropy source');
const modLower=.013795*.00042/(2*.8*.014**2);
ok(modLower>.01847,"native strict analytical modular field source >0.01847 magnitude");
ok(modularSource < -modLower,
  'CANONICAL log-native Gibbs matching DOES NOT make native field stationary');
ok(modularSource+Jv<-.01842,
  'actual original J2 fails to cancel CANONICAL Gibbs-matched native HJR source');
function nativeModularValue(rr,nu2){
 const n=nativeFloat(rr,nu2),ss=Math.sqrt(1-n.h/n.mu);
 return (Math.log(8)+Hbinary((1+ss)/2))/beta;
}
const checkMod=dNumerical(r=>nativeModularValue(r,nuPath(r))+
   functionals(r,nuPath(r)).feedback);
close(checkMod,modularSource+Jv,6e-8,
  'independent NATIVE nonlinear constant-port path modular HJR field source');
const qNative=c*h,deltaPort=c*c*h*(mu-h);
const Bport=qNative*(1-qNative)-deltaPort;
const dDeltaPortV=c*c*value(x.B);
const MI2source=Math.log1p(deltaPort/(Bport*Bport))*dDeltaPortV;
const right128GoldenInfoSource=128*MI2source/Math.log(1/p);
ok(qNative>.0129&&qNative<.0138,"true original stationary one-port bound");
ok(deltaPort<3.1e-7 &&deltaPort>0,"genuine all128 port covariance small positive");
ok(Bport>.012,"true positive original two-port offdiagonal probability");
ok(dDeltaPortV>0&&dDeltaPortV<6e-6,"native one-port invisible two-port correlation sensitivity");
ok(Math.log1p(deltaPort/(Bport*Bport))<.0022,
   "exact log(AC/B^2) bound for one-port-invisible actual native 2-port MI");
ok(MI2source<1.32e-8,"strict native old port MI source smaller than 1.32e-8 nat");
ok(right128GoldenInfoSource<3.52e-6,
   "even multiplied by original RIGHT128 the TWO-PORT INFO source is too small");
ok(Hrawv+Jv+right128GoldenInfoSource<-.000371,
  "two-port MI cannot repair raw HJR native source even with oldRIGHT128");
ok(Hsurvv+Jv+right128GoldenInfoSource<-.000373,
  "two-port MI cannot repair survival HJR native source even with oldRIGHT128");
ok(modularSource+Jv+right128GoldenInfoSource<-.01841,
  "two-port MI cannot repair canonical log-modular HJR native field source");

console.log(JSON.stringify({status:"PASS_ORIGINAL_FULL128_NATIVE_HJR_THERMAL_WARD",checks,
 originalPins:{
  operator:"d0_native_preparation_closure_2026-10-21/PROOF.md §7",
  book:"A4D_FULL_HJR_FORWARD_CLOCK_TRANSPORT_2026_10_21.md",
  twoPort:"A4D_ORIGINAL_FULL128_STATIONARY_PORT_CORRELATION_SOURCE_2026_10_22.md"
 },nativeCalibrations:{p,z,beta,t,nu,mu,h,eps:e,muR:mup,hR:hp,epsR:ep},
 nativeBook:{J,J_R:Jp,oldRIGHT:128,CARdimension:16,feedback:"I-(I-2p² Delta)^4"},
 actualLorentzSource:{rawHeat:Hrawp,survivalHeat:Hsurvp,
  energy:Rp,feedback:Jp,fullRaw:Hrawp+Jp+Rp,fullSurv:Hsurvp+Jp+Rp},
 onePortInvisible:{amplitudeDirection:nuV,muDirection:muV,
  heatRaw:Hrawv,heatSurv:Hsurvv,feedback:Jv,fullRaw:Hrawv+Jv,
  fullSurv:Hsurvv+Jv},
 canonicalModular:{value:modularValue,fieldSource:modularSource,
    combinedWithActualBookJ:modularSource+Jv,analyticalSourceLowerBound:modLower},
 twoPortInfoRepair:{originalStationaryPortQ:qNative,correlation:deltaPort,
    invisibleDirectionMI2Source:MI2source,
    originalRIGHT128MaxGoldenSource:right128GoldenInfoSource},
 nativeBookHodgeNotIdentified:true,fullPhysicalGRClosed:false}));
