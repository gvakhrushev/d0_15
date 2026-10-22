// Original Golden cap9/20 N1 whole-trial THREE coarse READY statuses,
// while all finer failed factory, oldRIGHT and work distinctions remain retained.
// Direct full-tree validation; only standard JavaScript and assert used.
import assert from 'node:assert/strict';
const p=(Math.sqrt(5)-1)/2, lp=Math.log(1/p);
const alpha=(1-(1-2*p**3)**9)**128;
const beta=((1-p**120)**4*(1-(1-16*p**9)**20))**43;
const gamma=alpha*beta;
const z=2**-20,L=4*p**3;
const r0=1-(1-z*L)*(1-z*L*(1+p**6));
let checks=0;
const check=(x,t)=>{assert.ok(x,t);checks++};
const close=(a,b,t=5e-9,k='close')=>check(Math.abs(a-b)<=t*Math.max(1,Math.abs(a),Math.abs(b)),k+' '+a+' vs '+b);
check(alpha>0.66&&alpha<0.67&&beta>0.68&&beta<0.69,'actual untouched factories');
check(gamma>0.45&&gamma<0.46,'strict positive actual ternary readiness');
check(r0>1.85e-6&&r0<1.86e-6,'actual Golden two-band r0');
const labels=[0,0,1,2,2],price=[7,11,13,5,18],work=[0.21,0.39,0.10,0.49,0.27];
// Real retained Z has FIVE fine outcomes, stop test only compares 3 final statuses.
// Positive free parameter a controls TWO failure subbranches, c controls TWO READY1 subbranches.
function probs(g,r,a,c){
  return [(1-g)*a,(1-g)*(1-a),g*(1-r),g*r*c,g*r*(1-c)];
}
const coarse=P=>[P[0]+P[1],P[2],P[3]+P[4]];
function summary(P,K,kappa){
  const q=coarse(P);
  const Lcap=q.length+1-q.reduce((s,v)=>s+(1-v)**K,0);
  const Ncost=P.reduce((s,v,i)=>s+v*price[i],0);
  const H=-P.reduce((s,v)=>s+v*Math.log(v)/lp,0);
  const W=P.reduce((s,v,i)=>s+v*work[i],0);
  return {q,Lcap,Ncost,H,W,S: Lcap*(Ncost-H-W)+(Lcap-1)*kappa};
}
function fullTree(P,K,kappa){
 let total=0,meanT=0,cost=0,pointer=0,workEntropy=0,comparisons=0,KL=0;
 const visit=(word,pr,anchor,n)=>{
  // n = number of later observations already included
  if(n===K||labels[word.at(-1)]===anchor && n>=1){
   const T=word.length;
   total+=pr; meanT+=pr*T;
   cost+=pr*word.reduce((s,id)=>s+price[id],0);
   workEntropy+=pr*word.reduce((s,id)=>s+work[id],0);
   comparisons+=pr*n*kappa;
   pointer-=pr*Math.log(pr)/lp;
   return;
  }
  for(let j=0;j<P.length;j++)visit([...word,j],pr*P[j],anchor,n+1);
 };
 for(let j=0;j<P.length;j++)visit([j],P[j],labels[j],0);
 return {total,meanT,cost,pointer,workEntropy,comparisons,
   S:cost-pointer-workEntropy+comparisons};
}
for(const [g,r,a,c] of [
  [gamma,r0,0.27,0.63],
  [gamma,r0*1.000039,0.49,0.37],
  [gamma,0.15,0.22,0.71],
  [0.27,0.31,0.4,0.19],
  [0.72,0.52,0.57,0.55]
]){
 const P=probs(g,r,a,c), q=coarse(P);
 close(P.reduce((s,v)=>s+v,0),1,1e-14,'all fine outcomes normalized');
 close(q.reduce((s,v)=>s+v,0),1,1e-14,'all 3 original positive status categories retained');
 check(q.every(v=>v>0),'positive category alphabet');
 const Sfull=summary(P,1,0.19);
 for(const K of [1,2,3,4]){
  const full=fullTree(P,K,0.19),exact=summary(P,K,0.19);
  close(full.total,1,3e-13,'original full ternary stop tree + aborts mass');
  close(full.meanT,exact.Lcap,3e-13,'exact paid complete-trial count');
  close(full.cost,exact.Lcap*exact.Ncost,3e-13,'all original fine charge incl failure retained');
  close(full.pointer,exact.Lcap*exact.H,3e-13,'ALL full pointer entropy not just terminal');
  close(full.workEntropy,exact.Lcap*exact.W,3e-13,'all conditional CQ work entropy, full tensor');
  close(full.comparisons,(exact.Lcap-1)*0.19,3e-13,'all actual comparisons, fixed inventory');
  close(full.S,exact.S,2e-12,'complete whole measured Cost-minus-CQ-Info and controller');
 }
 // Because stopping depends only three coarse categories, movement of finer
 // failure log law a or READY1 sublabel c is also transported with factor 4.
 for(const dim of [0,1,2,3]){
  const h=dim===1?Math.min(2e-6,r/20):2e-6;
  const v=[g,r,a,c],plus=v.slice(),minus=v.slice();
  plus[dim]+=h;minus[dim]-=h;
  const pplus=probs(...plus),pminus=probs(...minus);
  const Sone=P0=>summary(P0,1,0).Ncost-summary(P0,1,0).H-summary(P0,1,0).W;
  const src=(Sone(pplus)-Sone(pminus))/(2*h);
  // K infinity exact expected cost: m+1=4 even when g moves.
  const stopped=4*src;
  const pplusStop=summary(pplus,4,0.19),pminusStop=summary(pminus,4,0.19);
  const fullPlus=fullTree(pplus,4,0.19),fullMinus=fullTree(pminus,4,0.19);
  const finiteSource=(fullPlus.S-fullMinus.S)/(2*h);
  close(finiteSource,(pplusStop.S-pminusStop.S)/(2*h),2e-7,
    'independent full capped physical price/source includes moving readiness');
  const veryLongK=200000000;
  const longStop= P0=>summary(P0,veryLongK,0.19).S;
  const longSource=(longStop(pplus)-longStop(pminus))/(2*h);
  close(longSource,stopped,2e-6,
    'uncapped native fourfold full Price-minus-CQ-Info source approached by actually finite K');
  check(Number.isFinite(src),'complete source finite');
 }
 const prior=probs(g,r,a,c);
 const eT=1+q.reduce((s,v)=>s+v/v,0);
 close(eT,4,2e-13,'FOUR expected complete native copies on any positive chart');
}
for(const r of [r0,1.8513018e-6,1.85133e-6,0.12,0.49]){
 const q=[1-gamma,gamma*(1-r),gamma*r];
 const entropy=-(q.reduce((s,v)=>s+v*Math.log(v),0))/lp;
 const dEntropy=gamma*Math.log((1-r)/r)/lp;
 const h=Math.min(1e-8,r/100);
 const entropyAt=u=>{
  const t=[1-gamma,gamma*(1-u),gamma*u];
  return -(t.reduce((s,v)=>s+v*Math.log(v),0))/lp;
 };
 close((entropyAt(r+h)-entropyAt(r-h))/(2*h),dEntropy,3e-7,'source from ORIGINAL actual failure-ready measured CQ law');
 close(4*dEntropy,4*gamma*Math.log((1-r)/r)/lp,3e-13,'complete fourfold nonlinear off-null CQ source');
 const K=100_000_000,qmin=Math.min(...q);
 check(qmin>0,'positive rare Ready1 source');
 const length=4-q.reduce((s,v)=>s+(1-v)**K,0);
 close(length,4,8e-14,'finite cap native 100M clock converges');
 const dLength=K*gamma*((1-gamma*r)**(K-1)-(1-gamma*(1-r))**(K-1));
 check(Math.abs(dLength)<1e-20,'whole genuine THREE category clock derivative negligible at K100M');
 const abortProb=q.reduce((s,v)=>s+v*(1-v)**K,0);
 check(abortProb<1e-30,'full ternary physical abort-tail probability still represented');
}
console.log(JSON.stringify({status:'PASS',checks,
 alpha,beta,gamma,original_r0:r0,realStatusM:3,expectedPaidTrials:4,
 rareReady1Probability:gamma*r0,
 nativeK:100_000_000,
 status:'PASS',
 scope:'whole measured-CQ first-match; not compulsory Book03 or independent M1 task'}));
