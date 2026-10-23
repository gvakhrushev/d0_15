// Exact mathematical complement to ORIGINAL Golden FULL128 coherent
// Householder archive recovery. If the original 128 fine Kraus outcomes
// have been irreversibly measured and remain classical, no deterministic
// DATA-only conditioned correction preserves every unknown 2d input
// entanglement with protected oldRIGHT. Quantitative QUANTUM
// entanglement-fidelity floor >7.39e-6 at genuine CAR16 boost1/9,
// derived exclusively from TRUE K0=I−2p² Delta and its old 8+8 spectrum.
// This does NOT rule out fully coherent unitary reversing ALL 128
// outcomes, or HERALDED probabilistic postselected filters.
// Finite owned NONCOMMUTING 2-Kraus witness saturates entire bound.
import assert from 'node:assert/strict';
let checks=0;const ok=(x,m)=>{assert.ok(x,m);checks++};
const close=(x,y,t=5e-12,m='close')=>
 ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){let c=a%b;a=b;b=c}return a||1n}
function R(a,b=1n){a=BigInt(a);b=BigInt(b);ok(b!==0n,'nonzero rational denominator');
 if(b<0n){a=-a;b=-b}const g=gcd(a,b);return {a:a/g,b:b/g}}
const times=(a,b)=>R(a.a*b.a,a.b*b.b);
const plus=(a,b)=>R(a.a*b.b+b.a*a.b,a.b*b.b);
const minus=(a,b)=>plus(a,R(-b.a,b.b));
const divide=(a,b)=>R(a.a*b.b,a.b*b.a);
const square=x=>times(x,x);
const lt=(a,b)=>a.a*b.b<b.a*a.b;
const gt=(a,b)=>a.a*b.b>b.a*a.b;
const eq=(a,b)=>a.a*b.b===b.a*a.b;
const num=x=>Number(x.a)/Number(x.b);
const mu=R(141489,10240000),harmonic=R(69399,5030720);
const eps2=times(mu,minus(mu,harmonic));
ok(lt(mu,R(1382,100000))&&gt(eps2,square(R(55,100000)))&&lt(eps2,square(R(56,100000))),
   'ACTUAL original CAR16 boost rigorous mu<.01382 and eps∈(.00055,.00056)');
const p=(Math.sqrt(5)-1)/2,beta=2*p*p;
ok(beta>.76&&beta<.8,'original native Golden t=2p² algebraic strict bounds');
const u=R(76,100),epsL=R(55,100000),qGood=R(9888,10000);
const oneMinusNativeMu=minus(R(1),times(R(8,10),mu));
ok(gt(oneMinusNativeMu,qGood),'exact original 1−tμ >.9888 on native boost');
const deltaLower=times(times(R(4),u),times(epsL,qGood));
const maxOtherOutcome=times(R(2),times(R(8,10),plus(R(1382,100000),R(56,100000))));
ok(lt(maxOtherOutcome,R(231,10000)),
   'actual ORIGINAL fine K0 nonblank failure max<.0231');
const infidelityLower=divide(square(deltaLower),times(R(16),R(231,10000)));
ok(gt(infidelityLower,R(739,100000000)),
   'BIGINT exact original full128 outcome-recording deterministic recovery entanglement infidelity STRICTLY >7.39e-6');
const eps=Math.sqrt(num(eps2)),mu0=num(mu),eigens=[mu0-eps,mu0+eps];
const blank=eigens.map(l=>1-beta*l),q=blank.map(x=>x*x);
const Q0=q[0],Q1=q[1],dq=Q0-Q1;
// Stronger EXACT physical success/failure obligation:
// for an arbitrary unknown DATA qubit with its protected RIGHT,
// every heralded EXACT UNIVERSAL correction of a fully MEASURED
// fine outcome must have total input-independent success probability
// η <= Σ_i lambda_min(K_i† K_i) <= min(E_0)+min(I−E_0)
// =1−(q_minus−q_plus).  This is a CP trace-effect theorem,
// not the entanglement-fidelity bound and not free retries.
const maximumExactClassicalRecoverySuccess=1-dq;
const mandatoryFailureLower=dq;
ok(gt(deltaLower,R(1653,1000000)),
 'BIGINT ORIGINAL native fully measured-record exact universal postmeasurement correction MUST have >0.001653 unconditional failure mass');
ok(mandatoryFailureLower>num(deltaLower)&&maximumExactClassicalRecoverySuccess<.99835,
 'SAME actual native full128 all-fine measured process forbids unit-success universal quantum echo even WITH all 128 labels and arbitrary outcome-conditioned correction');
const Fcl=Math.sqrt(Q0*Q1)+Math.sqrt((1-Q0)*(1-Q1));
const maxFidelity=(1+Fcl)/2;
const defect=(1-Fcl)/2;
ok(Q0>Q1&&dq>num(deltaLower),'original real actual K0 carries input-dependent PURE quantum info in measured fine labels');
ok(defect>num(infidelityLower)&&defect>7.39e-6&&defect<9e-6,
  'real ORIGINAL CAR16 two-band 128 fine instrument cannot be perfectly corrected after irreversible outcome measurement');
close(dq,4*beta*eps*(1-beta*mu0),1e-14,
 'exact old positive CAR16 blank effect eigenvalue contrast is 4 beta eps(1-beta mu)');
const identity=(a,b)=>{const k0=[[a,0],[0,b]],
   v=Math.sqrt(1-a*a),u=Math.sqrt(1-b*b),k1=[[0,u],[v,0]];
 const f0=a*b, f1=u*v;
 // Physical conditional polarity correction X on K1; it leaves a
 // labelled irrevocably classical record. Effective A1=XK1 diag(v,u).
 const trace0=a+b,trace1=u+v;
 const entF=(trace0**2+trace1**2)/4;
 const fidel=f0+f1;
 close(entF,(1+fidel)/2,3e-13,'SAME inherited genuine noncommuting 2-Kraus polar-corrected entanglement fidelity SATURATES classical record information bound');
 const noncomm=Math.abs(a*u-v*b)+Math.abs(b*v-u*a);
 ok(noncomm>0,'unchanged inherited Kraus matrices are NONCOMMUTING despite sharp correction bound');
 return {a,b,fidel,entF,defect:1-entF};
};
// In the SAME owned NONCOMMUTING K0,K1 instrument this exact
// postmeasurement herald-success upper wall is ACHIEVED:
// K0=diag(a,b), K1=[[0,u],[v,0]], with a=u=.6,b=v=.8.
// Apply after outcome0 R0=a K0^-1 and outcome1 R1=u K1^-1,
// each a valid contraction. Both successful composite Kraus become
// respectively a I and u I; total η=a²+u²=.72.
const oldA=.6,oldB=.8,oldU=Math.sqrt(1-oldB*oldB),oldV=Math.sqrt(1-oldA*oldA);
const oldExactHeraldOptimal=oldA*oldA+oldU*oldU;
const oldExactHeraldUpper=Math.min(oldA*oldA,oldB*oldB)+
                           Math.min(oldU*oldU,oldV*oldV);
close(oldExactHeraldOptimal,oldExactHeraldUpper,2e-14,
 'NONCOMMUTING original 2-Kraus outcome-controlled polar+filter correction SATURATES exact universal postmeasurement herald-success wall');
close(oldExactHeraldOptimal,.72,1e-14,'old native controlled filter η=.72 with failure .28 (not imaginary free inverse)');
ok(oldExactHeraldOptimal<1,'true original measured classical fine-label task consumes positive loss even with filters');
const twoK=identity(.6,.8);
close(twoK.entF,.98,1e-13,'old native noncommuting 2-Kraus best measured-outcome correction ent Fidelity exactly .98 (not identity)');
for(const [aa,bb] of [[.55,.8],[.6,.8],[.7,.8],[.6,.75]]){
 const g=identity(aa,bb);
 ok(g.entF<1&&g.defect>0,'measured original noncommuting Kraus never has free deterministic full coherent reversal');
}
// Verify the exact ENTIRE finite original boost source of classical
// measurement disturbance; "best possible" Fcl after Q0 vs Q1 is a
// genuine strict nonzero proper-Lorentz first source.
const mup=-328779/204800000,hp=-20040939/9885993640,
  epp=((2*mu0-num(harmonic))*mup-mu0*hp)/(2*eps);
const bPrime=[-beta*(mup-epp),-beta*(mup+epp)];
const dqP=blank.map((b,i)=>2*b*bPrime[i]);
const FcPrime=(dqP[0]*Q1+Q0*dqP[1])/(2*Math.sqrt(Q0*Q1))-
  (dqP[0]*(1-Q1)+(1-Q0)*dqP[1])/(2*Math.sqrt((1-Q0)*(1-Q1)));
ok(FcPrime<-.0003&&FcPrime>-.0004,
  'native original actual strict 2-band classical fine RECORD loss has nonzero proper-Lorentz response');
function field(r){
 const d=(1-r*r)**2,P=5*r**4+r**3-8*r*r-r+5,
   Q=23*r**4+6*r**3-32*r*r-10*r+25;
 const m=9*P/(3200*d),delta=81*Q/(10240000*d),eps=Math.sqrt(m*m-delta);
 const b=[1-beta*(m-eps),1-beta*(m+eps)],qq=b.map(x=>x*x);
 const fidel=Math.sqrt(qq[0]*qq[1])+Math.sqrt((1-qq[0])*(1-qq[1]));
 return {r,qq,defect:(1-fidel)/2};
}
for(const r of [.1,.105,1/9,.115,.12]){
 const ff=field(r),step=1e-5,fd=(field(r+step).defect-field(r-step).defect)/(2*step);
 ok(ff.defect>0&&fd>.00013&&fd<.00019,
  'REAL ORIGINAL native coherent-vs-classically measured full128 recovery gap persists and has nonzero Lorentz field source');
 if(r===1/9)close(fd,-FcPrime/2,2e-8,'source of original native irreversible measurement loss independent finite difference');
}
console.log(JSON.stringify({status:"PASS_ORIGINAL_FULL128_CLASSICAL_RECORD_IRREVERSIBILITY_FIDELITY_WALL",checks,
 original:{
  nativeCAR16BlankEigen:blank,
  nativeBlankProbabilities:q,
  strictRationalDifferenceLower:num(deltaLower),
  strictRationalEntanglementInfidelityLower:num(infidelityLower),
  actualMaxDeterministicFullRecordCorrectedEntanglementFidelity:maxFidelity,
  actualMinimalEntanglementInfidelity: 1-maxFidelity,
  guaranteedMinimumUnconditionalFailureForEXACTUniversalHeraldedRecordCorrection:mandatoryFailureLower,
  highestPossibleMeasured128RecordExactHeraldedSuccess:maximumExactClassicalRecoverySuccess,
  fullMeasuredNativeOriginalCAR16LorentzInfidelitySource:-FcPrime/2,
  originalFine128OtherKrausDetailsNotAssumed:true
 },
 theorem:"for ANY fine outcome-labeled physical DATA-only deterministic corrections, F_ent <= (1+sum_i sqrt(q_i0*q_i1))/2 <= (1+sqrt(q0*q1)+sqrt((1-q0)*(1-q1)))/2",
 nativeOld2KrausSharpness:{...twoK,exactHeraldSuccessAchieved:oldExactHeraldOptimal,exactHeraldFailure:.28},
 fullStinespringCoherentUncomputeNotForbidden:true,
 probabilisticHeraldedFilterNotForbidden:true,
 trueOldRIGHTJointOperationsNotForbidden:true,
 actualBook03PhysicalInfoAndCutNotSelected:true,GR_closed:false}));
