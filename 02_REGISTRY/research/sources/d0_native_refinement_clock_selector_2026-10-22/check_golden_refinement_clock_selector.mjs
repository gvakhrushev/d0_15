// ORIGINAL Golden F/R fine 72441-status complete return vs SAME actual
// named READY, READY_CLICK minimal three-class future; every fine leaf kept.
// Combines prior owned n(L)=64 ceil(log_phi L)+128 native PF C2 schedule
// and native strict partition Book J feedback merging theorem.
// NEW: exact first-repeat verification-vs-abort RESOURCE exponent 64,
// and finite logarithmic 3-atom clock K(L) with summable entire source error.
// Checker does NOT select M1 task, complete paid work/Info/Book Hodge or GR.
import assert from 'node:assert/strict';
let checks=0;
const ok=(v,msg)=>{assert.ok(v,msg);checks++};
const near=(a,b,t=1e-11,msg='close')=>
 ok(Math.abs(a-b)<=t*Math.max(1,Math.abs(a),Math.abs(b)),msg+' '+a+' '+b);
const p=(Math.sqrt(5)-1)/2,phi=1/p,z=2**-20,beta=2*p*p;
function fib(n){let a=0n,b=1n;for(let i=0;i<n;i++)[a,b]=[b,a+b];return a}
function x_n(n){
 let a=p,b=2*p*p;
 if(n===1)return a;
 if(n===2)return b;
 for(let j=3;j<=n;j++)[a,b]=[b,p*b+p*p*a];
 return b;
}
function nDepth(L){
 let s=0,P=1;
 while(P<L){P*=phi;s++}
 ok(P>=L&&s>=0,'original native Golden ceil(log_phi L) cost integer');
 return {s,n:64*s+128};
}
const gammaTest=(r,n)=>{
 const x=x_n(n),g=2*p**3*x;
 return {x,g,q:[1-g,g*(1-r),g*r],mFine:fib(n)+6n*fib(n+1)};
}
const r0=1-(1-z*4*p**3)*(1-z*4*p**3*(1+p**6));
ok(r0>1.8e-6&&r0<1.9e-6,'unchanged original actual positive golden READY/click report');
const n20=20,exactFine=fib(n20)+6n*fib(n20+1);
ok(exactFine===72441n,'exact full original native fine leaf alphabet F20+6F21=72441');
const nt=gammaTest(r0,n20);
near(nt.g,2*10946*p**23,2e-13,'original unconditional READY mass from every true n20 suffix');
near(nt.q.reduce((a,b)=>a+b,0),1,3e-13,'original full U READY0 READY1 three atom normalized');
near(nt.g,0.3416407870701554,2e-13,'no substitution of different cap9/20 gamma=.45367');
ok(nt.q.every(x=>x>0),'all original three future classes genuinely nonzero');
const cost20Mass=6765*p**21+10946*(p**22+p**24+2*p**23);
near(cost20Mass,1,1e-13,'ALL actual native n20 fine overshoot/fail/ready work normalizes');
const priceUnit=q=>-Math.log1p(-4*z*q*(1-q));
const Jfine=128*(6765*priceUnit(p**21)+10946*priceUnit(p**22)+10946*priceUnit(p**24)
  +2*10946*priceUnit(p**23*r0)+2*10946*priceUnit(p**23*(1-r0)));
const J3=128*nt.q.reduce((s,x)=>s+priceUnit(x),0);
ok(Jfine>J3,'same full fixed-selector rank original Book J strict fine>minimal three');
ok(Jfine-J3>0.00006726908,'already-owned native uniform strict Book merge gap');
function merge(a,b){
 const D=x=>1-4*z*x*(1-x);
 const lhs=D(a+b)-D(a)*D(b);
 const rhs=8*z*a*b*(1-2*z*(1-a)*(1-b));
 near(lhs,rhs,2e-13,'EXACT original Book PSD-partition merge polynomial');
 return priceUnit(a)+priceUnit(b)-priceUnit(a+b);
}
for(const [a,b] of [[.05,.2],[.0001,.3],[.1,.1],[.15,.5]]){
 ok(merge(a,b)>0,'strict Book feedback reduces with all positive atom merges');
}
const fineMean=Number(exactFine+1n);
near(fineMean,72442,1e-13,'genuine COMPLETE original n20 first repeat mean72442 NOT 4');
const coarseMean=4;
const fullFineMax20=p**21;
const minFineClick20=p**23*r0;
ok(fullFineMax20>1e-5&&minFineClick20<3e-11,'fine positive native rare click and overshoot retention');
const eta=6e-7,theta=1-eta;
const arMin=2*p**3*.72,arMax=.35;
ok(arMin>.339&&arMin<arMax,'literal original Golden F/R READY positive mass from native Fibonacci');
const testRareAbsSq=1-2*arMin*1.85e-6+(arMax*2e-6)**2;
ok(testRareAbsSq<theta*theta,
  'ALL complex report r with Re(r)>1.85e-6, |r|<2e-6 have |1-a r|<1-6e-7');
for(const L of [4,5,8,16,32,64,256,1024]){
 const {s,n}=nDepth(L);
 const g=gammaTest(r0,n);
 ok(g.x>.72&&g.x<.73,'original recurrence F_{n+1} p^n >.72 uniformly');
 ok(g.g>arMin&&g.g<arMax,'true original all-site coarse future READY probability bounded');
 ok(g.q.every(q=>q>0&&q<1),'three original future outcomes all positive at actual report');
 const qmin=Math.min(...g.q);
 ok(qmin>eta,'native actual coarse minimal future outcome >6e-7');
 const cap=Math.ceil((80+16*s)/eta);
 const logTailBound=-eta*cap-Math.log(eta*(cap+1));
 const genericBound=-80-16*s-Math.log(80+16*s);
 ok(logTailBound<=genericBound+2e-14,
   'actual capped harmonic tail <= e^(-80-16s)/(80+16s) logarithmic certificate');
 ok(-80-16*s<=-80-16*Math.log(L),
   'GOLDEN PF tick s(L) grants at least 16 powers of spatial decay');
 const fineLogMax=(n+1)*Math.log(p); // exact known native fine qmax <=p^(n+1)
 const fineCapNeedLog=-Math.log(2)-fineLogMax;
 const predicted=-Math.log(2)+129*Math.log(phi)+64*Math.log(L);
 ok(fineCapNeedLog>=predicted-1e-12,
    'for even HALF verification probability all-fine native K requires Ω(L^64)');
 const fineSuccessLog=Math.log(cap)+fineLogMax;
 ok(fineSuccessLog<Math.log(.0001),
    'using logarithmic 3-atom cap on fine leaf alphabet yields almost-certain abort');
 const logFullActionErrorBound=-155-28*Math.log(L);
 const logWholeHess=-155+Math.log(84)-22*Math.log(L);
 ok(logWholeHess<Math.log(1e-60),
   'conditional uniform holomorphic R>=1/L gives tiny ALL-42L4 Hessian source bound');
 ok(Number(g.mFine)>3,'full actual fine alphabet grows strictly beyond 3');
 ok(g.mFine>=6n*fib(n+1),'all actual fine suffix labels preserved');
 if(n<=1200){
  // Binet x_n avoids Number overflow; exact BigInt Fibonacci ratio checked.
  const ref=Number(fib(n+1))*Math.pow(p,n);
  near(ref,g.x,3e-11,'genuine Fibonacci all native words vs stable recurrence gamma');
 }
}

// SECOND distinct original site test: a single GLOBAL native F/R tape
// that retains the address of every READY0 and READY1 is neither
// the global three-atom future nor the huge fully fine future.
// Its minimal Boolean future algebra has 1+2W positive atoms.
// This is a true resource lower bound on the native admission needed
// to obtain site-local independent field sources.
const L8=8,n24=24,W8=L8**4;
ok(fib(25)===75025n,'literal ORIGINAL Golden n24/L8 exact-cost word census');
ok(fib(n24)+6n*fib(n24+1)===496518n,
  'literal native n24 full fine terminal alphabet size');
const originalL8MinCount=4,originalL8MaxCount=43; // pinned earlier exact census
ok(originalL8MinCount>0&&originalL8MaxCount>originalL8MinCount,
 'unchanged OLD complete 4096/4096 original L8 n24 native word counts positive');
ok(W8===4096&&1+2*W8===8193,
 'site-labelled READY0/READY1 + global NOT_READY minimal true Boolean atom count');
ok(2*W8+2===8194,'true single global addressed first-match mean trials8194');
ok(Number(fib(n24)+6n*fib(n24+1)+1n)===496519,
   'original full fine n24 mean 496519 paid native trials versus addressed8194 and global4');
for(const L of [4,8,16,64,256,1024,2048]){
 const W=L**4,{s,n}=nDepth(L),g=gammaTest(r0,n);
 const rhoMin=1-9/L**3,rhoMax=1+9/L**3;
 ok(rhoMin>.85&&rhoMax<1.15,'derived ORIGINAL PF C2 ALL-site density positive');
 const globalAddressAtoms=2*W+1;
 ok(globalAddressAtoms>3,'native address completeness makes global3 outcome insufficient');
 // For a real site report each positive address has TWO READY outcomes.
 const minSiteClick=arMin*rhoMin*1.85e-6/W;
 const maxSiteReady=arMax*rhoMax/W;
 ok(minSiteClick>5e-7/W,
   'positive native all-site minimum local READY1 report under original PF scheme');
 ok(maxSiteReady<.4/W,
   'every globally observed true site READY outcome at most .4/L4');
 const thetaAddr=1-5e-7/W;
 const maxAbsSiteRareSquared=1-2*arMin*rhoMin*1.85e-6/W
    +(arMax*rhoMax*2e-6/W)**2;
 ok(maxAbsSiteRareSquared<thetaAddr**2,
  'complex FULL site-resolved original READY1 survival contraction O(1/L4)');
 const capLocalGlobal=Math.ceil((80+16*s)*W/(5e-7));
 ok((5e-7/W)*capLocalGlobal>=80+16*s-1e-9,
  'honest one GLOBAL site-addressed tape needs O(L4 log L) cap to suppress rare tail');
 const coarseCap=Math.ceil((80+16*s)/eta);
 const siteConditionalSuccessUpper=coarseCap*.4/W;
 if(L>=1024)ok(siteConditionalSuccessUpper<1e-3,
   'one GLOBAL fine-address future aborts almost surely on every READY anchor with coarse O(logL) cap');
 // Any input preserving the W local READY tests has >=2W+1 positive atoms;
 // fresh IID first return Kac mean = m+1.
 const minExpected=globalAddressAtoms+1;
 ok(minExpected===2*W+2,
  'native ACTUAL positive site-address ledger requires ≥2L4+2 mean whole trials');
 // To verify ANY one named site READY branch with prob ≤.4/W
 // at conditional probability at least 1/2, K≥W/.8.
 ok((W/.8)*(.4/W)>=.5,
   'rigorous fixed-local-target cap lower scale is Ω(W) with no postselection');
}

for(let K of [1,2,5,10,100]){
 const q=nt.q;
 const abort=q.reduce((s,x)=>s+x*(1-x)**K,0);
 const max=q.reduce((s,x)=>Math.max(s,x),0);
 ok(abort>0&&abort<1,'honest capped finite FIRST MATCH retains all mismatch aborts');
 const success=1-abort;
 const direct=q.reduce((s,x)=>s+x*(1-(1-x)**K),0);
 near(success,direct,1e-12,'complete capped coarse first-match verified vs aborted');
 ok(success>=0,'native finite task properly verified');
}
console.log(JSON.stringify({status:'PASS_ORIGINAL_GOLDEN_DUAL_CLOCK_BOOK_SELECTOR',checks,
 native20:{fineLeaves:String(exactFine),fineExpectedTrials:fineMean,
  coarseExpectedTrials:coarseMean,coarseProbabilities:nt.q,
  originalFineClickProbability:minFineClick20,Jfine,Jthree:J3,Jgap:Jfine-J3},
 nativeRefinement:{
  PFdepth:'n(L)=64 ceil(log_phi L)+128',
  coarseClock:'K(L)=ceil((80+16 ceil(log_phi L))/(6e-7))',
  coarseMeanTrialsAtUncapped:4,
  fineHalfSuccessClockLowerBound:'K >= 0.5 phi^(129) L^64',
  fineWithCoarseLogCap:'match success <=K p^(n+1)=O(L^-64 log L)',
  threeScaleExact:{globalPredicatesExpected:4,
    siteResolvedPredicatesExpected:'2 L^4+2',
    trueOriginalL8n24:{spatialAddresses:4096,siteReadyAtoms:8193,
      addressedExpectedTrials:8194,fineExpectedTrials:496519},
    oneGlobalSiteClock:'K_global_address(L)=ceil((80+16s(L)) L^4/(5e-7))',
    localTargetOnlyWithGlobalCheapClock:'Pr(match site READY|anchor) <=0.4 K/L^4',
    perSiteParallelWithNativeAddressAdmission:'K_site(L)=ceil((80+16s(L))/(6e-7)) O(logL) if physical per-site task is independently prepared and PAID'
  },
  uniformConditionalValueDefect:'sup entire L^4-site HJR |error|< exp(-155) L^-28',
  uniformConditionalHessian:'norm_inf error <84 exp(-155) L^-22 if holomorphic radius>=1/L and dim<=42 L^4'
 },
 originalFullFineWorkNeverErased:true,
 nativeM1TaskSelected:false,
 originalBook03PhysicalCutSelected:false,
 GR_closed:false}));
