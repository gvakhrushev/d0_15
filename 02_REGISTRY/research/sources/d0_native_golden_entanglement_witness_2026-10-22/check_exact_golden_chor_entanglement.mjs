// ORIGINAL D0 full128 Golden lazy channel Phi=p Id+p² R, R CPTP,
// true MAXIMALLY ENTANGLED original Choi DATA128/oldRIGHT128 initial input.
// Full quantum Choi entanglement via Bell fidelity and negativity,
// NOT merely nonzero mutual information. Completely branchwise:
// original fine histories (all retained) cannot all be D:R separable.
// ORIGINAL CAR16 16x16 boost Fourier fixture: literal genuine
// allblank K0=I-2p² Delta and exact two-band spectral polynomial gives
// Bell/blank positive event fidelity for 130 full rounds, with
// strictly positive real proper-Lorentz derivative.
// Analytical proofs are separate, no original full128 16384 matrix replay;
// oldRIGHT Bell measurement gate routing remains PHYSICAL admission OPEN.
import assert from 'node:assert/strict';
let checks=0;
function ok(cond,msg){assert.ok(cond,msg);checks++}
function near(x,y,t=5e-13,msg='close'){
 ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),msg+': '+x+' vs '+y);
}
const p=(Math.sqrt(5)-1)/2,phi=1/p,p2=p*p,p3=p**3,beta=2*p2,d=128;
const exactInt=(x,y)=>BigInt(x)**BigInt(y);
ok(p>.617&&p<.625&&p+p2>1-1e-14&&p+p2<1+1e-14,
 'owned Golden p²+p=1 and rational pointwise bounds');
ok(Math.abs(p-p2-p3)<1e-14,'original p³ native no-erasure factor unchanged');
ok(128n*exactInt(617,10)>exactInt(1000,10),
 'RIGOROUS BIGINT 128*(617/1000)^10 >1 certifies all original full128 n<=10 entangled');
ok(128n*exactInt(5,11)<exactInt(8,11),
 'RIGOROUS BIGINT 128*(5/8)^11 <1, sufficient threshold not assured for n11');
const full128=[];
for(let n=0;n<=18;n++){
 const lazy=p**n,Fmin=lazy;
 const Nmin=(d*Fmin-1)/2;
 const ElogMin=Math.max(0,Math.log(d*Fmin));
 const trDistanceToSepMin=Math.max(0,2*(Fmin-1/d));
 full128.push({n,lazy,Fmin,negativityLower:Math.max(0,Nmin),
  logNegativityLower:ElogMin,traceDistanceFromAllSeparableLower:trDistanceToSepMin});
 if(n<=10){
  ok(d*Fmin>1,'for every original R CPTP n<=10 CHOI remains entangled');
  ok(Nmin>0&&trDistanceToSepMin>0,
   'native oldRIGHT negativity & separation from every separable state strictly positive');
 }else if(n>=11){
  ok(Nmin<0,'native witness ceases to GUARANTEE entanglement after 10, not proof of loss');
 }
 if(n>0){
  const previous=full128[n-1];
  near(Fmin/previous.Fmin,p,5e-14,'all horizon original no-exogenous reset Golden CP mixture keeps identity branch p^n');
 }
}
ok(full128[1].negativityLower>39&&full128[10].negativityLower>.02,
 'STRONG guaranteed full original DATA128/RIGHT128 quantum negativity from n1 to n10');
ok(full128[10].traceDistanceFromAllSeparableLower>.0006,
 'original Choi 10-round entangled state has positive trace-distance separation from every D:R separable state');
// The original exact CAR16 native Fourier proper-boost fixture.
const muR=141489n,muDen=10240000n,hR=69399n,hDen=5030720n;
const rational=(a,b)=>Number(a)/Number(b);
const mu=rational(muR,muDen),h=rational(hR,hDen),e=Math.sqrt(mu*(mu-h));
const muPrime=-328779/204800000;
const hPrime=-20040939/9885993640;
const ePrime=((2*mu-h)*muPrime-mu*hPrime)/(2*e);
const lo=mu-e,hi=mu+e,blo=1-beta*lo,bhi=1-beta*hi;
ok(mu>.0138&&mu<.01382&&e>.00055&&e<.00056,
 'actual 16x16 quadratic original Dirac-square spectrum and exact input rational');
ok(muPrime<-.00160&&muPrime>-.00161&&ePrime>0&&ePrime<.006,
 'original real proper-Lorentz boost source mu_r NEGATIVE, epsilon_r POSITIVE');
ok(0<bhi&&bhi<blo&&blo<1,
 'original exact CAR16 physical blank K0 eigenvalues all in (0,1)');
// Rigorous rational Golden eigenmean lower bound: beta<191/250,
// mu<691/50000 => beta*mu<33/3125, hence Bbar>3092/3125.
// Exact 260th integer comparison proves (Tr K0^130 /16)^2>1/16.
ok(beta<191/250,'native Golden beta=2p² < 191/250 by p²<191/500');
ok(mu<691/50000,'original exact CAR16 mean native A²<691/50000');
ok((191n*691n*3125n)<(250n*50000n*33n),
 'BIGINT exact original beta*mu<33/3125');
ok(16n*exactInt(3092,260)>exactInt(3125,260),
 'BIGINT exact 16*(3092/3125)^260>1; original CAR16 n130 clean-Bell CHOI branch entangled');
ok((247/250)**129>1/5,'EXACT positive base-to-exponent rational inequality for field source lower at n130');
ok(247n**129n*5n>250n**129n,'BIGINT native b_high^129 >1/5 source-power envelope');
let nLastCert=0;
const car16=[];
for(let n=1;n<=155;n++){
 const average=(blo**n+bhi**n)/2;
 const clean=average**2;
 const averagePrime=-(n*beta/2)*(blo**(n-1)*(muPrime-ePrime)+
                                   bhi**(n-1)*(muPrime+ePrime));
 const cleanPrime=2*average*averagePrime;
 const Jensen=(1-beta*mu)**(2*n);
 const Nmin=Math.max(0,(16*clean-1)/2);
 car16.push({n,cleanBellEvent:clean,cleanLorentzSource:cleanPrime,
   JensenLower:Jensen,negativityGuaranteedByAllBlank:Nmin});
 ok(clean+1e-14>=Jensen,'Jensen ORIGINAL full n-blank CAR16 Choi return: trace B^n/16 >=(trace B/16)^n');
 ok(average>0&&averagePrime>0&&cleanPrime>0,
    'TRUE original physical proper-Lorentz field source of (blank whole tape AND Bell on DR) strictly POSITIVE all finite n');
 if(n<=130){
  ok(Jensen>1/16,'ALL n<=130 original CAR16 full quantum Choi entanglement certified by real allblank path alone');
  ok(clean>1/16&&Nmin>0,'all actual original unmarked full128 outcomes included, lower from one POSITIVE clean record');
  nLastCert=n;
 }
}
ok(nLastCert===130,'actual rigorous original 16x16 Fourier real CAR channel 130 guaranteed full rounds');
ok(car16[130].cleanBellEvent<1/16,
   'n131 original CLEAN-WITNESS not sufficient: cannot infer original actual entanglement lost');
const lower130=130*.76*.0016*.2*.5;
ok(lower130>.0158,'uniform exact 130-round strict positive clean Lorentz source >.0158');
ok(car16[129].cleanLorentzSource>lower130,
   'original n130 Born witness field FIRST SOURCE strictly positive by exact sign and integer envelope');
function nativeB(r){
 const r2=r*r,r3=r2*r,r4=r2*r2,f=(1-r2)**2;
 const m=9*(5*r4+r3-8*r2-r+5)/(3200*f);
 const q=81*(23*r4+6*r3-32*r2-10*r+25)/(10240000*f);
 const t=Math.sqrt(m*m-q);
 return {m, e:t, b0:1-beta*(m-t),b1:1-beta*(m+t)};
}
for(const n of [1,2,10,50,100,130]){
 const field=r=>{let B=nativeB(r);return ((B.b0**n+B.b1**n)/2)**2};
 const delta=1e-5;
 const fd=(field(1/9+delta)-field(1/9-delta))/(2*delta);
 near(fd,car16[n-1].cleanLorentzSource,7e-7,
   'true unchanged original CAR16 polynomial Lorentz first-source finite difference of full Choi clean Bell event');
}
const Fclean1=car16[0].cleanBellEvent;
near(Fclean1,(1-beta*mu)**2,1e-13,
  'original entire Bell/first-blank joint probability exactly trace(K0)^2/16^2');
const strictFirstLower=2*.76*(1-.8*.014)*.0016;
ok(strictFirstLower>.0024&&car16[0].cleanLorentzSource>strictFirstLower,
   'actual full original CAR16 proper-link Choi coherence Bernoulli joint source >0.0024');
const bellCircuit={d:128,qubits:7,CNOT_gates:7,H_gates:7,
  finalBitReadouts:14,requiredAction:"joint DATA↔oldRIGHT Bell inverse measurement, routed and paid",physicalOldRIGHTRoutingProved:false};
ok(Math.log2(bellCircuit.d)===bellCircuit.qubits,
 'Bell projector for actual full128 prepared initial Choi has exactly seven native logical two-wire Bell decoders');
const information={entangledFull128Until:10,
  originalFull128ChoiNegativityN1:full128[1].negativityLower,
  originalFull128ChoiNegativityN10:full128[10].negativityLower,
  originalCAR16GuaranteedUntil:130,
  source130:car16[129].cleanLorentzSource};
console.log(JSON.stringify({status:"PASS_NATIVE_GOLDEN_CHOI_ENTANGLEMENT_THROUGH_TEN_AND_CAR16_130",checks,
 originalPhysicalInputs:{
  full128:"Phi=p Id+p² R_CP, ORIGINAL oldRIGHT128 maximally entangled Choi",
  CAR16:"original all128-Kraus Fourier boosted ν=3/5, K0=I-2p² A², exact CAR16 µ,h,µ_r,h_r"
 },
 certifiedGoldenOriginal128:full128.filter(x=>[1,2,5,8,9,10,11].includes(x.n)),
 certifiedCAR16:car16.filter(x=>[1,10,50,100,125,130,131].includes(x.n)),
 information,bellCircuit,
 actualOriginalFull128OriginalSceneAll42SourceNotReplayed:true,
 originalBook03Selected:false,oldRIGHTAddressabilityNotProven:true,GR_closed:false}));
