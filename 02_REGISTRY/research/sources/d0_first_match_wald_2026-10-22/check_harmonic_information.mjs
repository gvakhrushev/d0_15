// Entire first-match harmonic information source, uniqueness and finite-K tails.
// No fitted Info law; tested only on the mathematically specified measured iid tape.
import assert from 'node:assert/strict';
const phi=(1+Math.sqrt(5))/2, lp=Math.log(phi);
let checks=0;
function check(x,msg){assert.ok(x,msg);checks++;}
function close(a,b,eps=2e-10,label='close'){
  check(Math.abs(a-b)<=eps*Math.max(1,Math.abs(a),Math.abs(b)),label+': '+a+' vs '+b);
}
const entropy=r=>-(r*Math.log(r)+(1-r)*Math.log1p(-r))/lp;
const dEntropy=r=>Math.log((1-r)/r)/lp;
function harmonicPartial(r,K){
  const a=1-r;
  let A=0,B=0,ak=1,rk=1;
  for(let k=1;k<=K;k++){
    ak*=a;rk*=r;
    A+=ak/k;B+=rk/k;
  }
  return {v:(r*A+a*B)/lp,d:(A-B+a**K-r**K)/lp,A,B};
}
function tailBound(r,K){
 const a=1-r;
 return ((a**(K+1)+r**(K+1))/(K+1))/lp;
}
function derivativeTailBound(r,K){
 const a=1-r;
 return (a**K+r**K+(a**(K+1)/r+r**(K+1)/a)/(K+1))/lp;
}
function enumerateScore(r,Nmax){
  let h=0,mean=0,meanN=0,atLeast=0;
  const a=1-r;
  for(let n=0;n<=Nmax;n++){
    if(n>0)h+=1/n;
    const pr=(r*r)*(a**n)+(a*a)*(r**n); // COMPLETE first-match leaves
    mean+=pr*h;
    meanN+=pr*n;
    atLeast+=pr;
  }
  return {mean:mean/lp,meanN,stoppedProbability:atLeast};
}
for(const r of [0.04,0.12,0.22,0.5,0.76,0.91,0.97]){
  for(const K of [1,2,3,5,12,24,70,220]){
    const v=harmonicPartial(r,K);
    const d=1e-6;
    const num=(harmonicPartial(r+d,K).v-harmonicPartial(r-d,K).v)/(2*d);
    close(num,v.d,7e-7,'analytic complete capped harmonic source');
    check(v.v<=entropy(r)+3e-13,'positive monotone harmonic information truncation');
    check(entropy(r)-v.v<=tailBound(r,K)+3e-13,'exact positive tail in physical information units');
    check(Math.abs(dEntropy(r)-v.d)<=derivativeTailBound(r,K)+3e-12,'true source error bound');
  }
  const ens=enumerateScore(r,1300);
  close(ens.stoppedProbability,1,1e-11,'positive complete first-match prefix probability');
  close(ens.mean,entropy(r),1e-11,'measured harmonic score recovers entropy');
  close(ens.meanN,1,1e-10,'mean failed matches is 1');
}
// Unknown finite-alphabet report law: conditional harmonic surprise then entropy.
for(const q of [[0.1,0.3,0.6],[0.21,0.18,0.13,0.48],
                [0.02,0.05,0.09,0.12,0.25,0.47]]){
 const probs=q.reduce((s,x)=>s+x,0);close(probs,1,2e-14);
 const direct=-q.reduce((s,v)=>s+v*Math.log(v),0)/lp;
 const all=q.reduce((s,v)=>s+v*(-Math.log(v)/lp),0);
 close(all,direct,1e-14,'all independent outcomes; no external catalogue');
 const cost=q.reduce((s,v)=>s+v*(1/v),0);
 close(cost,q.length,1e-14,'first match all-category expected additional calls');
}
// Uniqueness: (1-x) sum_{n>=0} H_n x^n = -log(1-x).
for(const x of [0.05,0.21,0.47,0.7,0.9]){
 let harmonic=0,series=0;
 for(let n=1;n<=3000;n++){
   harmonic+=1/n;
   series+=harmonic*x**n;
 }
 close((1-x)*series,-Math.log1p(-x),5e-13,'unique analytic harmonic coefficients');
}
// The original truly rare bounded certified h=1/4 report probabilities.
const native=[0.000001851242,0.0000018513018,0.00000185133];
for(const r of native){
  const K=20_000_000,a=1-r;
  const v=entropy(r);
  const gap=tailBound(r,K),dgap=derivativeTailBound(r,K);
  check(gap<1e-22,'native bounded entropy-gap 20M');
  check(dgap<3e-16,'native bounded all42 first-source coefficient-gap 20M');
  check(v>0 && v<0.0001,'original positive off-null report entropy not fitted');
}
console.log(JSON.stringify({status:"PASS",checks,
  nativeBinaryExpectedCompleteTrials:3,
  uniqueHarmonicScore:"H_n=sum_{k=1}^n 1/k",
  nativeK:20_000_000,
  fieldSourceValidity:"all 0<r<1; finite-K remainder explicit",
  Book03MandatoryInfo:"NOT_IDENTIFIED"}));
