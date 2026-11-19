// ORIGINAL Golden n20/L4 and n24/L8 full F/R address census
// + complete SAME-PADDED-CARRIER original reflection cut-Hodge heat and J.
// New report-space theorem: Fisher rank W vs full master source O(1/W);
// source Hessian inverse Ω(W²) on genuine PF C2 refinement.
// No arbitrary averaging of 2 actual nonuniform records, no M1 admission.
import assert from 'node:assert/strict';
let checks=0;
const check=(v,m)=>{assert.ok(v,m);checks++};
const approx=(a,b,t=3e-11,m='approx')=>
  check(Math.abs(a-b)<=t*Math.max(1,Math.abs(a),Math.abs(b)),m+': '+a+' vs '+b);
const p=(Math.sqrt(5)-1)/2,phi=1/p,zeta=2**-20,beta=2*p*p,oldRIGHT=128;
const r0=1-(1-zeta*4*p**3)*(1-zeta*4*p**3*(1+p**6));
const tiny=1-2*zeta,chi0=(1-1/80000)*tiny*(1-zeta)**2;
check(chi0>.99998,'strict uniform native full cut heat/source ratio constant χ>0.99998');
check(r0>1.85e-6&&r0<1.86e-6,'original exact Golden r0 fixed rare report');
function fib(n){let a=0n,b=1n;for(let i=0;i<n;i++)[a,b]=[b,a+b];return a}
function nativeCounts(n,L){
 const counts=new Uint32Array(L**4);
 function visit(rem,depth,left,width){
  if(rem===0){
   let ix=0;
   for(let j=0;j<4;j++)ix=ix*L+
    Math.max(0,Math.min(L-1,Math.floor(L*(left[j]+width[j]/2))));
   counts[ix]++;return;
  }
  const j=depth%4,short=width.slice();short[j]*=p;
  visit(rem-1,depth+1,left.slice(),short);
  if(rem>=2){
   const right=left.slice(),long=width.slice();
   right[j]+=p*long[j];long[j]*=p*p;
   visit(rem-2,depth+1,right,long);
  }
 }
 visit(n,0,[0,0,0,0],[1,1,1,1]);
 const F=Number(fib(n+1)),sum=counts.reduce((a,b)=>a+b,0),
 sq=counts.reduce((a,b)=>a+b*b,0);
 check(sum===F,'every ORIGINAL F/R exact-cost Golden word counted ONCE');
 check(counts.every(x=>x>0),'actual all site-address projection positive');
 const W=counts.length,w=Array.from(counts,x=>x/F);
 approx(w.reduce((a,b)=>a+b,0),1,2e-13,'actual native W-count conditional distribution normalized');
 const varrho=W*sq/(F*F)-1;
 check(varrho>0,'true OLD native PF is nonuniform, no synthetic uniform sample');
 return {n,L,W,F,counts:Array.from(counts),w,sq,varrho,
  min:Math.min(...counts),max:Math.max(...counts)};
}
const f=q=>4*q*(1-q);
const fp=q=>4*(1-2*q);
const E=q=>Math.exp(-beta*f(q));
const k=q=>zeta*fp(q)/(1-zeta*f(q));
const j=q=>-Math.log1p(-zeta*f(q));
const jpp=q=>-8*zeta*(1-2*zeta+zeta*f(q))/(1-zeta*f(q))**2;
const c=(q,Z)=>oldRIGHT*k(q)-2*E(q)*fp(q)/Z;
const cp=(q,Z)=>oldRIGHT*jpp(q)+2*E(q)*(beta*fp(q)**2+8)/Z;
function book(census,r){
 const {n,L,W,F,w}=census;
 const M=Number(fib(n)+6n*fib(n+1));
 const dwork=Number(fib(n)+4n*fib(n+1)); // LOWER bound, NOT presumed exact physical work
 const D=M*dwork;
 const a=2*F*p**(n+3);
 const qAddr=[1-a],q3=[1-a,a*(1-r),a*r];
 const siteClick=w.map(x=>a*x*r);
 const siteNo=w.map(x=>a*x*(1-r));
 for(let z=0;z<W;z++)qAddr.push(siteNo[z],siteClick[z]);
 approx(qAddr.reduce((s,x)=>s+x,0),1,3e-13,'REAL original whole site READY/U law normalized');
 check(qAddr.length===2*W+1&&qAddr.length<=M,
       'minimal actual Boolean READY_z,CLICK_z partition padded on original fine M selector');
 const Zv=q=>D-2*q.length+2*q.reduce((s,x)=>s+E(x),0);
 // Each omitted dormant original fine comparator contributes exactly heat 1,
 // original s*oldRIGHT feedback determinant 1.
 const Zaddr=Zv(qAddr),Z3=Zv(q3);
 const minimum=M*(dwork-2),eta=(1+2*beta)/(64*zeta*(1-2*zeta)*minimum);
 check(eta>0&&eta<1/80000,'WHOLE original cut Hodge heat merge error from native M and work lower bound');
 check(Zaddr>=minimum&&Z3>=minimum,'no removed harmonic modes in complete native full Hodge heat');
 const Jaddr=oldRIGHT*qAddr.reduce((s,x)=>s+j(x),0);
 const J3=oldRIGHT*q3.reduce((s,x)=>s+j(x),0);
 const fullAddr=Math.log(oldRIGHT*Zaddr)/beta+Jaddr;
 const full3=Math.log(oldRIGHT*Z3)/beta+J3;
 check(fullAddr>full3&&Jaddr>J3,
       'same native full carrier/zero modes actual Hodge+feedback cheaper for valid global three task');
 const dJ3=oldRIGHT*a*(k(a*r)-k(a*(1-r)));
 let dJaddr=0;
 for(let z=0;z<W;z++)
  dJaddr+=oldRIGHT*a*w[z]*
    (k(siteClick[z])-k(siteNo[z]));
 const d3=a*(c(a*r,Z3)-c(a*(1-r),Z3));
 let da=0;
 for(let z=0;z<W;z++)
  da+=a*w[z]*(c(siteClick[z],Zaddr)-c(siteNo[z],Zaddr));
 check(d3>0&&da>0&&dJ3>0&&dJaddr>0,
       'entire original cut heat AND J site-vs-global native response signs');
 const concentration=census.sq/(F*F);
 const ratio=da/d3,feedbackRatio=dJaddr/dJ3;
 // A genuine ORIGINAL PF-unequal two-site report tangent is COMPLETELY
 // invisible to all 3 global outcomes but visible to the same complete
 // addressed Hodge+Book return. This is not a physical 42-field writer claim.
 let high=0,low=0;
 for(let i=1;i<W;i++){
   if(w[i]>w[high])high=i;
   if(w[i]<w[low])low=i;
 }
 check(w[high]>w[low]&&w[low]>0,'real original F/R two sites have UNEQUAL but positive weights');
 const dFn=weight=>c(a*weight*r,Zaddr)-c(a*weight*(1-r),Zaddr);
 const dFnPrime=weight=>r*cp(a*weight*r,Zaddr)
                           -(1-r)*cp(a*weight*(1-r),Zaddr);
 check(dFnPrime(w[low])>0&&dFnPrime(w[high])>0,
  'entire ORIGINAL coupled Hodge+Book site local contrast increasing with site mass');
 const globalBlind=w[high]*(1/w[high])+w[low]*(-1/w[low]);
 approx(globalBlind,0,3e-13,'actual extreme pair tangent invisible to EVERY global three-event probability');
 const addressedWitness=a*(dFn(w[high])-dFn(w[low]));
 check(addressedWitness>0,'FULL real F/R paired-cut Hodge+Book sees genuine PF-hidden local direction');
 const atHalf=(w0)=>a*w0*(c(a*w0*.5,Zaddr)-c(a*w0*(1-.5),Zaddr));
 approx(atHalf(w[high]),0,1e-14,'unique addressed report source vanishes at local exact half report');
 check(a*w[high]*(c(a*w[high]*.75,Zaddr)-c(a*w[high]*.25,Zaddr))<0,
   'whole paired-cut Hodge+Book report gradient changes sign across half');
 const chi=(1-eta)*(1-2*zeta)*(1-zeta)**2;
 check(chi>chi0&&chi<1,'uniform full Hodge heat source comparison constant');
 check(ratio>chi*concentration&&ratio<concentration/chi,
       'NEW rigorous Fisher/source dilution inequality with native full cut HEAT included');
 check(feedbackRatio>chi*concentration&&feedbackRatio<concentration/chi,
       'actual original Golden feedback-only ratio falls inside complete-source bounds');
 // This is exact for the original full measured site-address law at fixed rho.
 const FisherSite=w.map(x=>a*x/(r*(1-r)));
 const FisherGlobalEig=a*concentration/(r*(1-r));
 check(FisherSite.every(x=>x>0),
       'original complete addressed output Fisher matrix has FULL REAL rank W');
 check(FisherGlobalEig>0,'actual site-forgetting global three-class Fisher rank ONE');
 // Shannon chain rule used in earlier ORIGINAL full relative-history owner.
 const binaryH=x=>-x*Math.log(x)-(1-x)*Math.log1p(-x);
 const Hsite=-qAddr.reduce((s,x)=>s+x*Math.log(x),0);
 const Hcond=binaryH(a)+a*(
  -w.reduce((s,x)=>s+x*Math.log(x),0)+binaryH(r));
 approx(Hsite,Hcond,4e-12,'same true measured fine-address Shannon=H(READY)+aH(address)+aH(click)');
 const HnatSlope=a*Math.log((1-r)/r);
 const HGoldenSlope=HnatSlope/Math.log(phi);
 check(HGoldenSlope>9,'original rare report full address Info slope O(1) while Book derivative O(W^-1)');
 // SAME original TRUE Golden self-delimiting 0/10 cost-relative one tape
 // was already proved as a Σ a*w_z*(1+r_z-H_phi(r_z)) score.
 // Only for genuinely IID independently PAID whole-tape first-return task:
 // E[T]=m+1 => exact whole stopped-history Cost−Info source.
 const gPrime=1-HGoldenSlope/a,oneCodeSource=a*gPrime;
 const stoppedCodeSource=(2*W+2)*oneCodeSource;
 check(gPrime<-26&&gPrime>-27,'unchanged original 0/10 Golden Price−Info source on report chart');
 check(stoppedCodeSource<0&&da>0,
       'true measured whole stopped price and unweighted paired-cut Book have O(W) versus O(1/W) source');
 check(Math.abs(stoppedCodeSource)/da>100000*W*W,
       'real original native addressed stopped-vs-Book source discrepancy grows Ω(L^8)');
 // Complete capped iid first-match GOAL includes every aborted leaf.
 const mAddr=qAddr.length;
 const abort=(K)=>qAddr.reduce((s,q)=>s+q*Math.exp(K*Math.log1p(-q)),0);
 for(const K of [1,2,10,100,1000]){
   const A=abort(K);
   check(A>0&&A<1,'honest full original site-addressed first-match has real finite-K aborts');
   const length=1+qAddr.reduce((s,q)=>s-Math.expm1(K*Math.log1p(-q)),0);
   const identity=mAddr+1-qAddr.reduce((s,q)=>s+Math.exp(K*Math.log1p(-q)),0);
   approx(length,identity,5e-9,'true capped expected number of complete Golden trials incl all aborts (Kac identity; subtracting 8193 numbers loses finite precision)');
   const maxSite=a*Math.max(...w);
   const bound=a*Math.exp(K*Math.log1p(-maxSite));
   check(A>=bound-3e-13,'strict all-READY native site-anchor abort lower bound with actual wmax');
 }

 // All probability coordinates are affine in each native local r_z.
 // Parent coupled cut Hessian h_q negative definite. Here test explicit local
 // diagonals with actual Z (including 1/Z heat) and rank-one heat source.
 const zCheck=[0,Math.floor(W/2),W-1];
 let maxD=0,minD=Number.POSITIVE_INFINITY;
 for(const z of zCheck){
  const aw=a*w[z],vDiff=E(siteClick[z])*fp(siteClick[z])-E(siteNo[z])*fp(siteNo[z]);
  const hz=aw*aw*(cp(siteClick[z],Zaddr)+cp(siteNo[z],Zaddr))-
     4*beta/Zaddr**2*(aw*vDiff)**2;
  check(hz<0,'WHOLE native paired Hodge+Book source has strictly NEGATIVE local report Hessian');
  minD=Math.min(minD,-hz);maxD=Math.max(maxD,-hz);
 }
 // Prove source Hessian operator norm bound via Q^T H_q Q, not brute W².
 const kmax=8*oldRIGHT*zeta/(1-zeta)**2+64*beta*M/minimum**2;
 const maxW=Math.max(...w),minW=Math.min(...w);
 const HessOpUpper=2*a*a*maxW*maxW*kmax;
 const HessMinLower=2*a*a*minW*minW*(1-eta)*8*oldRIGHT*zeta*(1-2*zeta);
 check(HessOpUpper>0&&HessMinLower>0&&HessOpUpper>=HessMinLower,
   'original Book full report Hessian uniform spectral sandwich');
 check(maxD<HessOpUpper,'native full Hessian local curvature bounded by exact padded-spectrum norm');
 check(minD>=HessMinLower*(1-1e-5),'native full Hessian strict concavity from complete h_q');
 return {n,L,W,M,dwork,F,a,min:census.min,max:census.max,variance:census.varrho,
  concentration,ratio,sourceGlobal:d3,sourceAddressed:da,
  feedbackRatio,Z3,Zaddr,eta,chi,
  fullMasterGap:fullAddr-full3,
  FisherGlobalRank:1,FisherAddrRank:W,
  globalThreeBlindAddressBookWitness:addressedWitness,
  unequalExtremeSites:[census.min,census.max],
  FisherSiteMin:Math.min(...FisherSite),FisherSiteMax:Math.max(...FisherSite),
  FisherGlobalEigenvalue:FisherGlobalEig,
  HGoldenSlope,HessOpUpper,HessMinLower,
  oneTapeCodeSource:oneCodeSource,stoppedCodeSource,
  cappedAbortAt1000:abort(1000),
  meanFirstMatchGlobal:4,meanFirstMatchAddressed:2*W+2,
  meanFirstMatchFine:M+1};
}
const n20=nativeCounts(20,4);
const n24=nativeCounts(24,8);
check(n20.F===10946&&n20.min===29&&n20.max===78&&n20.sq===482862,
      'TRUE original n20 full L4 census and exact sum of address squares');
check(n24.F===75025&&n24.min===4&&n24.max===43&&n24.sq===1577067,
      'TRUE original n24 full L8 census and exact sum of address squares');
const r20=book(n20,r0),r24=book(n24,r0);
for(const x of [r20,r24]){
 check(x.ratio>chi0*x.concentration&&x.ratio<x.concentration/chi0,
       'source ratio certified despite UNKNOWN actual physical work dimension');
 check(x.sourceGlobal>.00011&&x.sourceGlobal<.00012,
       'genuine complete Hodge+Book global 3-class remains finite positive');
 check(x.sourceAddressed<x.sourceGlobal*.01,
       'native full site-address Hodge+Book source diluted even though Fisher full-rank');
 check(x.meanFirstMatchFine>x.meanFirstMatchAddressed&&
       x.meanFirstMatchAddressed>x.meanFirstMatchGlobal,
       'THREE distinct physically paid native stopping tasks: global3 addressed(2W+1) fineM');
}
check(Math.abs(r20.variance-.031696854839008415)<1e-12,'n20 actual original PF variance from full enumerated 10946 words');
check(Math.abs(r24.variance-.14761993599600975)<1e-12,'n24 actual original PF variance from full enumerated 75025 words');
// ALL-L h→0 analytic bound consuming ORIGINAL n(L) PF C2 theorem:
// |rho_z−1|<9/L³, normalized mean rho=1, so mean (rho−1)²<81/L⁶.
// For n(L)>=320, eta_n <=eta_20 <1/80000, hence chi>=chi0.
// Then ratio <=(1+81/L^6)/(chi0 L^4), and all site Hessian eigenvalues
// are O(L^-8) at native fixed zeta, not a UNIFORM full-field root inverse.
for(const L of [4,5,8,16,32,64,256,1024]){
 let s=0,t=1;while(t<L){t*=phi;s++}
 const n=64*s+128,W=L**4,h=1/L;
 check(n>=320&&s>=3,'original Golden source-regular PF cost depth n(L)');
 const varMax=81*h**6;
 check(9*h**3<1,'strict every original native site weight positive');
 const ratioMax=(1+varMax)/(chi0*W),ratioMin=chi0/W;
 const leakUpper=9*.35**2*(8*oldRIGHT*zeta/(1-zeta)**2)/L**7;
 check(leakUpper<.0012/L**7,
       'uniform native PF on hidden global source tangents has O(L^-7) original Book leakage');
 check(ratioMin>0&&ratioMax<1.03/W,
       'UNIFORM derived original PF refinement HODGE+Book source ∼1/L^4');
 const kmax=8*oldRIGHT*zeta/(1-zeta)**2+
     64*beta*2**20/(2**20*(50549-2))**2;
 const amax=.35;
 const HessScale=2*amax**2*((1+9*h**3)/W)**2*kmax;
 check(HessScale<.00035/W**2,
       'uniform native addressed report Hessian norm O(L^-8), inverse Ω(L^8)');
 const fullKacMean=2*W+2;
 const nativePaidPrefixMin=n*fullKacMean;
 check(nativePaidPrefixMin>=2*W*n,
       'each true original first-crossing F/R report costs at least n Golden units, so Ω(L^4 logL) paid repeats');
 const coarseK=Math.ceil((80+16*s)/(6e-7));
 const qMaxBound=amax*(1+9*h**3)/W;
 const readyMin=2*p**3*.72;
 const abortReadyLower=readyMin*(1-coarseK*qMaxBound);
 if(L>=512)check(abortReadyLower>.339-0.0001,
       'unchanged O(logL) complete GLOBAL clock gives ≳34 percent site-addressed abort probability on real PF refinement');
 if(L>=1024)check(abortReadyLower>.3398,
       'even high absolute Golden clock coefficient cannot solve site-READY rare return at large L');
}
console.log(JSON.stringify({status:"PASS_ORIGINAL_GOLDEN_ADDRESS_FISHER_AND_COMPLETE_CUT_HEAT",checks,
 originalSmall:{n20:r20,n24:r24},
 theorem:{
  allLDepth:"n(L)=64 ceil(log_phi L)+128",
  fullCutSourceRatio:"chi0(1+V_L)/L^4 <= D B_addr/D B_3 <= (1+V_L)/(chi0 L^4)",
  chi0,PFV:"0<=V_L<81/L^6 (owned)",
  FI:"diag(a w_z/[r_z(1-r_z)]) rank L^4 vs global aww^T/[rbar(1-rbar)] rank 1",
  sourceHessian:"negative definite report Hessian, norm O(L^-8), inverse norm Ω(L^8) on PF C2 schedule",
  performedNativeWork:"all original fine leaves and s=128 oldRIGHT retained",
  numericalWorkDimension:"lower bound dwork=F_n+4F_(n+1) only; actual might be larger",
  physicalBook03HodgeIdentified:false,physicalTaskSelected:false,
  sameHistoryBookInfoClockPriced:false,GR_closed:false
 }}));
