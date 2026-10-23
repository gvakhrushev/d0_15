#!/usr/bin/env node
// Bounded exact control on original K(9,11,13), no invented selector or clock.
const sizes=[9n,11n,13n],n=33,zone=i=>i<9?0:i<20?1:2;
const assert=(ok,msg)=>{if(!ok)throw Error(msg);};
const gcd=(a,b)=>b===0n?a:gcd(b,a%b);
const rational=(a,b)=>{const g=gcd(a,b);return [a/g,b/g];};
// Rational positive replacements for the common Golden edge factor.
// For any weight c, Q_N(u,v)=c*c^(N-1) C_(N-1)(v)/(c^N C_N(u)).
let counts=[1n,1n,1n],invarianceChecks=0;
const growth=[];
for(let N=1;N<=12;N++){
  const total=11n*counts[1]+13n*counts[2];
  const expected=rational(counts[1],total);
  for(const [a,b] of [[1n,2n],[2n,3n],[1n,1n],[7n,3n]]){
    const numerator=a*(a**BigInt(N-1))*counts[1]*(b**BigInt(N));
    const denominator=b*(b**BigInt(N-1))*(a**BigInt(N))*total;
    const got=rational(numerator,denominator);
    assert(got[0]===expected[0]&&got[1]===expected[1],"exact common-factor cancellation");
    invarianceChecks++;
  }
  assert(total>=20n**BigInt(N),"true native exponential lower bound");
  growth.push({N,rootedCompletePaths:total.toString(),
    sturmianBinaryLengthNComplexity:N+1,
    nativeLowerBound:(20n**BigInt(N)).toString()});
  counts=sizes.map((_,i)=>sizes.reduce((s,size,j)=>
    s+(i===j?0n:size*counts[j]),0n));
}
let return2=0,return3=0;
for(let v=0;v<n;v++)if(zone(v)!==zone(0)){
  return2++; // 0 -> v -> 0.
  for(let w=0;w<n;w++)if(zone(w)!==zone(v)&&zone(w)!==zone(0))return3++;
}
assert(return2===24&&return3===286,"actual rooted return counts");
const firstReturnWitnesses=[];
for(let N=2;N<=12;N++){
  const path=[0];
  for(let t=1;t<N;t++)path.push(t%2?9:20);
  path.push(0);
  assert(path.slice(1,-1).every(v=>v!==0),"first return has no intermediate root");
  assert(path.every((v,i)=>i===0||zone(v)!==zone(path[i-1])),"actual supported path");
  firstReturnWitnesses.push({N,path});
}
let rho=22;
for(let k=0;k<12;k++)rho-=(rho**3-359*rho-2574)/(3*rho*rho-359);
const raw=[143+13*rho,117+13*rho,rho*rho-99];
const norm=raw.reduce((s,x,i)=>s+Number(sizes[i])*x,0);
const r=raw.map(x=>x/norm);
const pi=r.map((x,i)=>Number(sizes[i])*x*x);
const piSum=pi.reduce((a,b)=>a+b);for(let i=0;i<3;i++)pi[i]/=piSum;
let entropy=0;
for(let i=0;i<3;i++)for(let j=0;j<3;j++)if(i!==j){
  const each=r[j]/(rho*r[i]);
  entropy-=pi[i]*Number(sizes[j])*each*Math.log(each);
}
assert(Math.abs(entropy-Math.log(rho))<1e-12,"full33 positive metric entropy");
assert(entropy>Math.log(20),"strict native positive entropy");
console.log(JSON.stringify({
  status:"PASS",originalVertices:33,originalDirectedEdges:718,
  exactRationalCommonWeightInvarianceChecks:invarianceChecks,
  symbolicInvariance:"For EVERY c>0: K=cA gives identical fixed-horizon Q_N and Perron-Doob P",
  rootedReturns:{length2:return2,length3:return3},
  firstReturnWitnesses,
  rootedLanguageGrowth: growth.filter(r=>[1,2,3,4,8,12].includes(r.N)),
  perronRho:rho,fullNativeMetricEntropyNats:entropy,
  logRho:Math.log(rho),
  scope:"Current neutral-terminal unit-cost law cannot force a phi-specific Beatty coding. Positive-entropy full law cannot be a stationary finite-alphabet factor of an irrational rotation. Arbitrary auxiliary couplings are not excluded."
},null,2));
