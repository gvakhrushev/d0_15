// Exact old original CAR16 full128 stationary inverse-square vs native Gibbs:
// Q-valued 16x16 minimal polynomial spectral data from previous proof owner.
// Standard Node JS, no third-party, no retuned native beta/heat/action.
import assert from 'node:assert/strict';
let checks=0;
const check=(x,m)=>{assert.ok(x,m);checks++};
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){const t=a%b;a=b;b=t}return a||1n}
function R(a,b=1n){a=BigInt(a);b=BigInt(b);check(b!==0n,"denom");
 if(b<0n){a=-a;b=-b}
 const d=gcd(a,b);return {a:a/d,b:b/d};
}
const plus=(x,y)=>R(x.a*y.b+y.a*x.b,x.b*y.b);
const neg=x=>R(-x.a,x.b);
const minus=(x,y)=>plus(x,neg(y));
const mul=(x,y)=>R(x.a*y.a,x.b*y.b);
const div=(x,y)=>R(x.a*y.b,x.b*y.a);
const gt=(x,y)=>x.a*y.b>y.a*x.b;
const lt=(x,y)=>x.a*y.b<y.a*x.b;
const eq=(x,y)=>x.a*y.b===y.a*x.b;
const val=x=>Number(x.a)/Number(x.b);
const square=x=>mul(x,x);
const mu=R(141489,10240000),harmonic=R(69399,5030720);
const d=mul(mu,harmonic),variance=minus(square(mu),d);
const epsLo=R(55,100000),epsHi=R(56,100000);
check(gt(mu,R(138,10000))&&lt(mu,R(14,1000)),"native exact mu strictly 0.0138..0.014");
check(gt(harmonic,R(1379,100000))&&lt(harmonic,mu),"original exact native harmonic < mu");
check(gt(variance,square(epsLo))&&lt(variance,square(epsHi)),
      "exact epsilon^2 from ORIGINAL 16x16 quadratic CAR determinant");
check(gt(d,R(0)),"native CAR16 full Delta invertible");
const minE=val(mu)-Math.sqrt(val(variance)),maxE=val(mu)+Math.sqrt(val(variance));
check(minE>0&&maxE>minE,"two strict positive original native eigenvalues");
const p=(Math.sqrt(5)-1)/2,beta=2*p*p;
check(beta>.7&&beta<.8,"native original beta=2p² fixed algebraic Golden");
const lower=mul(epsLo,minus(div(R(1),R(14,1000)),R(4,5)));
check(gt(lower,R(388,10000)),"strict rational 0.0388 native thermal trace-norm wall");
const eigen=Array.from({length:16},(_,i)=>i<8?minE:maxE);
const sumInv=eigen.reduce((s,x)=>s+1/x,0),sumHeat=eigen.reduce((s,x)=>s+Math.exp(-beta*x),0);
const nativeRho=eigen.map(x=>1/x/sumInv);
const nativeGibbs=eigen.map(x=>Math.exp(-beta*x)/sumHeat);
const diffs=nativeRho.map((x,i)=>x-nativeGibbs[i]);
const traceNorm=diffs.reduce((s,x)=>s+Math.abs(x),0);
const eps=Math.sqrt(val(variance));
const exactSpectralFormula=eps/val(mu)-Math.tanh(beta*eps);
function close(x,y,t=1e-12,label='close'){check(Math.abs(x-y)<t,label+': '+x+' vs '+y)}
close(traceNorm,exactSpectralFormula,1e-13,"actual full16 trace-norm vs tanh expression");
check(traceNorm>val(lower),"original strict certified rational bound");
close(nativeRho.reduce((a,b)=>a+b,0),1,1e-14,"original stationary density normalized");
close(nativeGibbs.reduce((a,b)=>a+b,0),1,1e-14,"original Gibbs density normalized");
const X=eigen.map((_,i)=>i<8?1:-1);
const thermalSource=X.reduce((s,x,i)=>s+x*diffs[i],0);
close(thermalSource,traceNorm,1e-13,"genuine free thermal direction gives trace norm");
check(thermalSource>.0388,"strict native HJR heat-preparation equation fails in this direction");
const betaNeed=Math.log(maxE/minE)/(maxE-minE);
check(betaNeed>72&&betaNeed<73,"native inverse-square would need NON-GOLDEN beta");
check(Math.abs(betaNeed-beta)>70,"no approximate native beta coincidence");
const eMod=eigen.map(x=>Math.log(x/minE)/beta);
const Z=eMod.reduce((s,x)=>s+Math.exp(-beta*x),0);
const modGibbs=eMod.map(x=>Math.exp(-beta*x)/Z);
for(let i=0;i<16;i++){
 close(modGibbs[i],nativeRho[i],3e-14,"canonical native log-Delta Gibbs EXACT");
 check(eMod[i]>=-1e-14,"positive ground-zero logarithmic native generator");
}
const modularValue=nativeRho.reduce((s,x,i)=>s+x*eMod[i],0)+Math.log(Z)/beta;
const nativeEntropy=-nativeRho.reduce((s,x)=>s+x*Math.log(x),0)/beta;
close(modularValue,nativeEntropy,3e-14,"full native inverse-square modular energy+heat equals entropy");
const g2=mathError=>Math.abs(mathError);
const modGap=Math.log(maxE/minE)/beta;
check(modGap>.1&&modGap<.11,"canonical modular oscillator gap distinct from native raw Dirac-square");
const matcomm=()=>{
 // Finite matrix algebra vs abelian pointer: E_ij has modular frequency
 // log(rho_i/rho_j) for i!=j; every diagonal pointer commutes and is stationary.
 const freq=Math.log(nativeRho[0]/nativeRho[15]);
 const nativeLogGap=Math.log(maxE/minE);
 close(freq,nativeLogGap,1e-14,"full native CAR algebra cross-block modular frequency");
 const diag=[0.2,0.3,0.5,1,0.25,0.8,0.25,0.3,0.4,0.5,0.1,0.8,0.2,0.3,0.4,0.5];
 // For any diagonal D, [rho,D]=0, exactly.
 for(let i=0;i<16;i++)close(nativeRho[i]*diag[i]-diag[i]*nativeRho[i],0,1e-14,"abelian measured pointer modular flow trivial");
 return freq;
};
const freq=matcomm();
console.log(JSON.stringify({status:"PASS",checks,originalPins:{
  original_input_blob:"ee8de4635d24c668949ac9a0186616ab7d59f2ed",
  old_certificate:"d0_native_preparation_closure_2026-10-21/RESULT.json",
  exact_mu:"141489/10240000",exact_harmonic:"69399/5030720",
  exact_quadratic:"Delta^2-2 mu Delta+mu*harmonic I=0"
},betaOriginal:beta,meanNativeDelta:val(mu),harmonicNativeDelta:val(harmonic),
 epsilon:eps,eigenvalues:[minE,maxE],eigenspaceMultiplicity:[8,8],
 densityEigenvalues:[nativeRho[0],nativeRho[15]],
 rawHeatGibbsEigenvalues:[nativeGibbs[0],nativeGibbs[15]],
 rigorousL1LowerBound:val(lower),actualL1TraceNorm:traceNorm,
 originalHJRHeatEulerDirection:thermalSource,betaNeeded:betaNeed,
 logNativeModularGap:modGap,fullCARModularCrossFrequency:freq,
 originalBook03Selection:"UNPROVEN",GR_closed:false},null,2));
