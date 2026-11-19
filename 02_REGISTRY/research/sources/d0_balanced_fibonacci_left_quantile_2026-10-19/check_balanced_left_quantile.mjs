#!/usr/bin/env node
/*
 * Reproducible exact F/R Fibonacci balanced LEFT decoder and moving-volume
 * DOUBLE-GOLDEN Book03 source. Builtin BigInt only, no external libraries.
 * Mathematical constructed full J2 only, not compulsory D0/old raw#216.
 */
function check(ok, label) {
  if (!ok) throw new Error("FAILED: " + label);
}
function near(x, y, tol, label) {
  check(Math.abs(x-y) <= tol, label + ": " + x + " vs " + y);
}
function fibPair(n) {
  if (n === 0) return [0n,1n];
  const [a,b] = fibPair(Math.floor(n/2));
  const c = a*(2n*b-a), d = a*a+b*b;
  return n % 2 ? [d,c+d] : [c,d];
}
function fib(n) {return fibPair(n)[0];}
function v2(x) {
  let n = 0;
  while ((x&1n)===0n) {x >>= 1n;n++;}
  return n;
}
function rank(word) {
  let remaining = 0;
  for (const c of word) remaining += c==="F"?1:2;
  let n=remaining,r=0n;
  for (const c of word) {
    if (c==="R") {check(n>=2,"illegal R");r+=fib(n);n-=2;}
    else if(c==="F")n--;
    else throw new Error("unknown native letter");
  }
  check(n===0,"not a complete native word");
  return r;
}
function unrank(n,r) {
  let w="",left=n;
  check(r>=0n && r<fib(n+1),"bad rank");
  while(left) {
    const f=fib(left);
    if(r<f) {w+="F";left--;}
    else{check(left>=2,"bad Fibonacci rank");w+="R";r-=f;left-=2;}
  }
  check(r===0n,"incomplete unrank");
  return w;
}
function probeCodec() {
  for(const n of [5,11,20,191]){
    const K=fib(n+1);
    const idx=[0n,1n,K/3n,K/2n,K-2n,K-1n];
    for(const k of idx) check(rank(unrank(n,k))===k,"roundtrip n="+n);
    console.log("native cost="+n+", count digits="+K.toString().length+", rank/unrank PASS");
  }
  for (const r of [1,2,3]) {
    const L=2**r,M=BigInt(L**4),k=6*2**(4*r-3),K=fib(k);
    check(K%M===0n && v2(K)===4*r,"exact Fibonacci 2-adic balance");
    check(BigInt(k)*4n===M*3n,"depth = 3/4 Role volume");
    console.log("EXACT L="+L+" nodes="+M+" cost="+(k-1)+
                " native words per cell digits="+(K/M).toString().length);
  }
  const K=fib(21),M=256n,rem=K%M;
  const tv=Number(rem*(M-rem))/Number(M*K);
  near(tv,0.004292378494427188,1e-16,"native near-balance TV");
  check(tv<=Number(M)/(4*Number(K)),"TV universal bound");
  console.log("NEAR L=4 cost=20 words="+K+" floor="+(K/M)+
              " extra="+rem+" TV="+tv);
}
const p=(Math.sqrt(5)-1)/2;
const z=2**-20;
const A=4*p**3, a=p**6, e0=p*p;
const Q0=1-z*A, R0=1-z*A*(1+a);
const sigma=-1, t2=.01, scene=528;
const cStar=scene*z*4*p**11*t2/R0;
const cMat=sigma*scene*z*8*p**6*t2*(1/Q0+a/R0);
near(cMat/cStar,-23.416406751884068,1e-11,
     "FULL double-tick native material coefficient");
function coords(j,L=2) {
  let x=[];
  for(let k=3;k>=0;k--){const d=L**k;const i=Math.floor(j/d)%L;x.push((i+.5)/L);}
  return x;
}
function f1(x){return 1+x[0]*x[0]+x[1]*x[2]+Math.sin(2*Math.PI*x[3]);}
function q1(x){return x[0]*x[1]+x[2]*x[2];}
function invCDF(u,eps){
  // Inverse of R_eps(x)=x+eps(x^2-x);
  // actual physical volume J_eps(x)=1+eps(2x-1).
  return 2*u/(1-eps+Math.sqrt((1-eps)**2+4*eps*u));
}
function fullTrueLogdet(r,q) {
  const e=e0*(1+t2*r);
  const b=(p+sigma*p*p*t2*q)**2;
  const B=4*b*(1-b);  // TRUE TWO native scene ticks
  const l=4*e*(1-e);
  return -scene*(Math.log1p(-z*B)+Math.log1p(-z*(l+(1-l)*B)));
}
function macroMeanPrice(eps){
  const K=Number(fib(12)), M=16,q=K/M;
  check(q===9,"exact native L=2 balanced multiplicity");
  let total=0;
  for(let rank0=0;rank0<K;rank0++){
    const decodedCell=Math.floor(rank0/q);
    const u=coords(decodedCell);
    const x=[invCDF(u[0],eps),u[1],u[2],u[3]];
    const J=1+eps*(2*x[0]-1);
    total+=fullTrueLogdet(eps*f1(x)/J,eps*q1(x))/K;
  }
  return total;
}
function sourceTest() {
  const M=16;
  let analytic=0;
  for(let j=0;j<M;j++){
    const u=coords(j);
    analytic+=(cStar*f1(u)+cMat*q1(u))/M;
  }
  const eps=.001;
  const numerical=(macroMeanPrice(eps)-macroMeanPrice(-eps))/(2*eps);
  const rel=Math.abs((numerical-analytic)/analytic);
  check(rel<2e-5,"complete moving-volume two-tick first source");
  console.log("TRUE J2 derivative: analytic="+analytic+
              " numerical="+numerical+" rel="+rel);
  const u=.25;
  const Td=(invCDF(u,1e-5)-invCDF(u,-1e-5))/(2e-5);
  near(Td,u*(1-u),2e-9,"nonzero moving quantile derivative");
  console.log("REAL quantile DT at u=.25 ="+Td+
              " !=0; null-source first jet unchanged.");
}
probeCodec();
sourceTest();
console.log("PASS real-golden equal/near balance and whole two-tick source bridge.");
console.log("SCOPE mathematical complete AF LEFT decoder, not mandatory D0 physical GR.");
