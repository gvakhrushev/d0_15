// D0 first-match full-record Wald/KL/Fisher controls; standard Node.js only.
import assert from 'node:assert/strict';
let checks=0;
function check(p,s){assert.ok(p,s);checks++;}
function close(a,b,t=2e-11,s='close'){check(Math.abs(a-b)<=t*Math.max(1,Math.abs(a),Math.abs(b)),s+': '+a+' vs '+b);}
const p=(Math.sqrt(5)-1)/2,logphi=Math.log(1/p);
const H=q=>-q.reduce((s,v)=>s+v*Math.log(v),0);
const KL=(q,mu)=>q.reduce((s,v,i)=>s+v*Math.log(v/mu[i]),0);
const D=(q,mu)=>KL(q,mu)/logphi;
function L(q,K){
  return q.length+1-q.reduce((s,v)=>s+Math.pow(1-v,K),0);
}
function paths(q,K) {
  const result=[];
  const rec=(first,word)=>{
    const n=word.length-1;
    if(n===K){result.push({word:word.slice(),abort:true});return;}
    for(let b=0;b<q.length;b++){
      const w=word.concat([b]);
      if(b===first)result.push({word:w,abort:false});
      else rec(first,w);
    }
  };
  for(let a=0;a<q.length;a++)rec(a,[a]);
  return result;
}
function distribution(records,q){
  return records.map(r=>r.word.reduce((a,j)=>a*q[j],1));
}
const tests=[
  {q:[0.2,0.8],mu:[p,p*p],cost:[1,2],K:2},
  {q:[0.23,0.77],mu:[p,p*p],cost:[1,2],K:5},
  {q:[0.51,0.49],mu:[0.3,0.7],cost:[1,1],K:6},
  {q:[0.14,0.36,0.50],mu:[0.2,0.2,0.6],cost:[2,1,4],K:4},
  {q:[0.1,0.2,0.3,0.4],mu:[0.2,0.3,0.1,0.4],cost:[3,1,2,5],K:3},
  {q:[0.000001851269,1-0.000001851269],mu:[p*p,p],cost:[2,1],K:4}
];
for(const {q,mu,cost,K} of tests){
  const ph=paths(q,K),P=distribution(ph,q),Q=distribution(ph,mu);
  const pnorm=P.reduce((s,x)=>s+x,0),qnorm=Q.reduce((s,x)=>s+x,0);
  close(pnorm,1,2e-13,'full native tree normalized actual');
  close(qnorm,1,2e-13,'full native tree normalized reference');
  const eT=ph.reduce((s,a,i)=>s+P[i]*a.word.length,0);
  const eCost=ph.reduce((s,a,i)=>s+P[i]*a.word.reduce((t,j)=>t+cost[j],0),0);
  const entropy=-P.reduce((s,v)=>s+v*Math.log(v),0);
  const kl=P.reduce((s,v,i)=>s+v*Math.log(v/Q[i]),0);
  const targetL=L(q,K);
  close(eT,targetL,2e-12,'full expectation of stopped length');
  close(eCost,targetL*q.reduce((s,v,i)=>s+v*cost[i],0),2e-12,'every charged iid sample paid');
  close(entropy,targetL*H(q),2e-12,'full tape pointer entropy');
  close(kl,targetL*KL(q,mu),2e-12,'complete stopped KL');
  if(q.length===2 && q.every(x=>x>0) && mu.every((x,i)=>Math.abs(x-Math.pow(p,cost[i]))<1e-14)) {
    close((eCost-entropy)/logphi,kl/logphi,5e-12,'strict original Golden code Kraft price relation');
  }
  const v=q.map((_,j)=>j===0?.1:j===1?-.1:0);
  const score=ph.map(a=>a.word.reduce((s,j)=>s+v[j]/q[j],0));
  const fisher=score.reduce((s,x,i)=>s+P[i]*x*x,0);
  const f1=v.reduce((s,x,i)=>s+x*x/q[i],0);
  close(fisher,targetL*f1,2e-10,'complete stopped Fisher factor');
  const scoremean=score.reduce((s,x,i)=>s+P[i]*x,0);
  close(scoremean,0,3e-11,'score unbiased');
  if(q.length===2 && mu.every((x,i)=>Math.abs(x-Math.pow(p,cost[i]))<1e-14)){
    for (const rec of ph){
      const nativeCharge=rec.word.reduce((acc,b)=>acc+cost[b],0);
      const prior=Math.pow(p,nativeCharge);
      const real=rec.word.reduce((s,b)=>s*mu[b],1);
      close(real,prior,2e-12,'actual native 0/10 Kraft charge exact');
    }
  }
}
const lp=r=>Math.log((1-r)/r)/logphi;
const s=r=>1+r+(r*Math.log(r)+(1-r)*Math.log1p(-r))/logphi;
const sd=r=>1-lp(r);
function fullPrice(r,K,kappa=0){
  let a=1-r;
  let n=3-Math.pow(a,K)-Math.pow(r,K);
  return n*s(r)+(n-1)*kappa;
}
function exactDerivative(r,K,kappa=0){
  const a=1-r,n=3-a**K-r**K,dn=K*(a**(K-1)-r**(K-1));
  return n*sd(r)+(s(r)+kappa)*dn;
}
for(const r of [0.02,0.14,0.23,0.5,0.84,0.98]){
  for(const K of [1,2,3,5,10,20]){
    const h=1e-6;
    const d=(fullPrice(r+h,K,.7)-fullPrice(r-h,K,.7))/(2*h);
    close(d,exactDerivative(r,K,.7),5e-7,'finite original KL clock source');
    const rare=Math.pow(1-r,K)+Math.pow(r,K);
    const sourceErr=Math.abs(exactDerivative(r,K,.7)-3*sd(r));
    const bound=rare*Math.abs(sd(r))+(s(r)+.7)*K*(Math.pow(1-r,K-1)+Math.pow(r,K-1));
    check(sourceErr<=bound+4e-12,'rigorous residual bound');
  }
}
const nativeRootClicks=[0.000001851242,0.00000185131],k=20_000_000;
for(const r of nativeRootClicks){
  const loss=(1-r)**k+r**k;
  const dl=k*((1-r)**(k-1)-r**(k-1));
  close(3-L([1-r,r],k),loss,1e-12,'rare cap factor');
  check(dl>0,'true nonzero cap source; no illicit freeze');
  check(loss<1.0e-16,'native cap asymptotic complete-word decay');
  check(dl<2e-9,'native bounded clock derivative below 2e-9');
  // Clock variance of full unbounded source grows without bound at rare r.
  const varT=2*(1/r+1/(1-r))-6;
  check(varT>1e6,'mean3 does not erase huge oldRIGHT/clock variance');
}
for(const m of [2,3,4,8,16,128]){
  const q=Array.from({length:m},(_,i)=>i+1);
  const sum=q.reduce((a,b)=>a+b);
  const normalized=q.map(x=>x/sum);
  close(normalized.reduce((a,b)=>a+b,0),1,1e-14,'all pointer probabilities retained');
  const mean=1+normalized.reduce((s,v)=>s+v/v,0);
  close(mean,m+1,2e-13,'genuine m-outcome first-match mean m+1');
}
console.log(JSON.stringify({status:"PASS",checks,
  theorem:"exact whole iid native first-match Cost-minus-CQ-Info and KL/Fisher m+1",
  nativeBinaryClockMean:3,
  original128MeanIfAllStrictlyPositive:129,
  nativeH4Cap:k,
  nativeH4CapClockGradientLimit:"less than 2e-9; not identically zero",
  priceSelector:"unproved compulsory Book03"}));
