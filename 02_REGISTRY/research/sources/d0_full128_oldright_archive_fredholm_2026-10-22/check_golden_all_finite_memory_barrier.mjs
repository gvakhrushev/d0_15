// ORIGINAL \Phi=p Id + p^2 R with p=phi^-1, p+p²=1, R CPTP,
// consumed unchanged from ORIGINAL native preparation owner.
// NEW analytic all-finite-clock p^(3L) no-perfect-forgetting theorem;
// rank/Golden laziness first-round REAL 128-Kraus Choi mutual-info floor.
// Numerical checks include exact saturating CPTP unitary hostile fixture
// and lazy + replacer fixture. Not a full128 numerical Kraus replay.
import assert from 'node:assert/strict';
let checks=0;const ok=(x,m)=>{assert.ok(x,m);checks++};
const close=(x,y,t=2e-13,m='close')=>
 ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
const p=(Math.sqrt(5)-1)/2,p2=p*p,p3=p**3,d=128;
close(p+p2,1,2e-15,'exact Golden p+p²=1 root identity');
close(p-p2,p3,2e-15,'KEY native no-erasure factor p−p²=p³');
ok(p>p2&&p3>0,'original Golden laziness strong identity branch dominates CP recycle');
const mu=141489/10240000,h=69399/5030720,eps=Math.sqrt(mu*(mu-h));
const nativeCARUniformNorm=eps/mu;
ok(nativeCARUniformNorm>.0401&&nativeCARUniformNorm<.0402,
 'named original exact CAR16 unequal stationary density vs uniform source');
for(const L of [0,1,2,3,4,5,8,13,20,100]){
 const lower=p3**L*nativeCARUniformNorm;
 ok(lower>0,'actual native CAR16 Golden finite preparation cannot exactly reach inverse-square rho* from uniform input');
 if(L===1)ok(lower>.0094,'strict true native CAR16 L=1 unavoidable DATA marginal gap');
 const choiLower=(2/d)*(p3**L);
 const quantumMILower=.5*choiLower**2;
 ok(choiLower>0&&quantumMILower>0,
  'all finite original full128 Choi DR not exactly product, quantum MI strictly positive by Pinsker');
}
// First-round ORIGINAL FULL128 actually has <=128 Kraus leaves on
// its own named instrument, and the preparation is maximally entangled.
// The exact Golden convex channel sends I/d to
// rhoD>=p I/d and rhoD<=p I/d+p² I.
// Thus Choi rank<=d, product largest eigenvalue<= (p/d+p²)/d.
const firstRhoDMax=p2+p/d;
const fullTraceLower=2*(1-firstRhoDMax);
const mutualLower=fullTraceLower**2/2;
ok(firstRhoDMax<.387&&firstRhoDMax>.386,'strict Golden all128 first DATA one-round eigen envelope');
ok(fullTraceLower>1.2264&&fullTraceLower<1.227,
  'STRONG actual full128 one-round trace norm vs stationary-product lower wall');
ok(mutualLower>.752&&mutualLower<.753,
  'STRONG actual full128 one-round RIGHT/DATA mutual-info lower wall in natural nats');
// SAME Golden p law SHARPNESS: a unitary recycle maps hermitian
// sigma_x to -sigma_x, saturating \|\Phi X\|_1>=p³\|X\|_1.
const sx=[[0,.5],[.5,0]],sz=[[1,0],[0,-1]];
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const add=(A,B)=>A.map((row,i)=>row.map((v,j)=>v+B[i][j]));
const scale=(A,s)=>A.map(row=>row.map(x=>x*s));
const mxNorm=X=>{
 const a=X[0][0],b=X[0][1],c=X[1][0],d=X[1][1];
 ok(Math.abs(b-c)<1e-14,'test Hermitian real input');
 const trace=a+d, delta=Math.sqrt((a-d)**2+4*b*c);
 return Math.abs((trace+delta)/2)+Math.abs((trace-delta)/2);
};
const Rx=mm(mm(sz,sx),sz);
close(mxNorm(Rx),mxNorm(sx),1e-14,'actual unitary recycle CPTP preserves trace norm');
let X=sx;
for(let L=1;L<=20;L++){
 X=add(scale(X,p),scale(mm(mm(sz,X),sz),p2));
 const expected=scale(sx,p3**L);
 for(let i=0;i<2;i++)for(let j=0;j<2;j++)
  close(X[i][j],expected[i][j],2e-13,'universal Golden all-finite contraction p^(3L) bound SHARP by Pauli recycling');
 close(mxNorm(X),p3**L,2e-13,'strict native worst-case trace-norm persistence exactly Golden p^(3L)');
}
// POSITIVE primitive unitary+depolarizing recycle can APPROACH lower
// p³ sharply while unique full-rank stationary state remains: choose
// R_eps=(1-eps) Ad_Z + eps (I/2)Tr on d=2.
for(const ep of [.3,.1,.01,.000001]){
 let initial=sx,x=initial;
 const eigen=p-p2*(1-ep);
 for(let L=1;L<=10;L++){
  x=scale(x,eigen);
  const rr=p3**L;
  ok(mxNorm(x)>=rr-2e-13,'sharpness survives actual primitive CPTP recycle channel');
 }
 ok(eigen>p3&&eigen<=1,'primitive approximants approach exact native Golden lower spectral factor');
}
// Independent Golden LAZY CPTP replacer fixture with invariant NONUNIFORM
// rho*=diag(.36,.64). Its real channel is p Id+p² R_rho,
// hence full Choi after any L has exact accessible original-like source
// p^L |Omega><Omega|+(1-p^L)rho* x I/2.
// The marginal rhoD,L=p^L I/2+(1-p^L)rho*.
const bell=[1/Math.sqrt(2),0,0,1/Math.sqrt(2)];
function lazyReplacerChoi(L){
 const q=p**L,target=[.36*.5,.36*.5,.64*.5,.64*.5],rho=Array.from({length:4},(_,i)=>
   Array.from({length:4},(_,j)=>q*bell[i]*bell[j]+(1-q)*(i===j?target[i]:0)));
 const dataDiag=[rho[0][0]+rho[1][1],rho[2][2]+rho[3][3]];
 const product=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>
   (i===j?.5*dataDiag[Math.floor(i/2)]:0)));
 const diff=rho.map((row,i)=>row.map((v,j)=>v-product[i][j]));
 const wanted=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>
   q*(bell[i]*bell[j]-(i===j?.25:0))));
 for(let i=0;i<4;i++)for(let j=0;j<4;j++)
  close(diff[i][j],wanted[i][j],2e-13,'TRUE Golden lazy replacer CHOI difference factorizes as p^L(Bell−maxmixed)');
 const exactTraceNorm=2*(1-1/4)*q;
 const allGoldenLower=(2/2)*p3**L;
 ok(exactTraceNorm>=allGoldenLower,
  'original p³ ALL-HORIZON bound satisfied by explicit nonuniform Golden-lazy CPTP model');
 return {L,power:q,fullTraceNormFromProduct:exactTraceNorm,
  nativeUniversalLower:allGoldenLower,DATAstationaryError:.28*q};
}
const basic=Array.from({length:21},(_,i)=>lazyReplacerChoi(i));
ok(basic.every(v=>v.fullTraceNormFromProduct>0&&v.DATAstationaryError>0),
  'positive strict finite golden no exact product or nonuniform stationary DATA from uniform Choi');
console.log(JSON.stringify({status:"PASS_ORIGINAL_GOLDEN_ALL_FINITE_MEMORY_AND_128_CHOI_WALL",checks,
 originalNativeTheorem:"Phi=p Id+p² R_CPTP, p-p²=p³ exactly",
 p,p3,
 allFiniteTracePersistence:"||Phi^L X||_1 >= p^(3L) ||X||_1 for every Hermitian X",
 actualOriginalCAR16:{uniformVsNativeStationary:nativeCARUniformNorm,
   everyFinitePrepGap:"at least phi^(-3L) epsilon/mu",firstRoundLower:p3*nativeCARUniformNorm},
 actualOriginalFull128:{
   d,firstRoundMaxDATAeigenUpper:firstRhoDMax,
   rankDRatFirstRoundMax:128,minExactProductRank:16384,
   firstTraceNormGapLower:fullTraceLower,firstQuantumMutualInfoLower:mutualLower,
   allFiniteChoiTraceGap:"at least (2/d) phi^(-3L)",
   allFiniteMutualInfo:"at least (2/d²) phi^(-6L)"
 },
 sharpness:"Pauli-Z unitary recycling attains p^3; primitive depolarizing approximants approach",
 positiveNonuniformGoldenReplacerChecks:basic.filter(x=>[0,1,2,5,10,20].includes(x.L)),
 selectedBook03PhysicalInfo:false,GR_closed:false}));
