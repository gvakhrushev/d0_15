#!/usr/bin/env node
"use strict";
// Exact ORIGINAL full128 first-shell Golden blank event Q(sqrt5) MAP/class.
const S=10n**18n;
const rootLo=2236067977499789696n,rootHi=rootLo+1n;
function check(x,what){if(!x)throw Error("FAILED "+what);console.log("PASS "+what);}
check(rootLo*rootLo<5n*S*S && 5n*S*S<rootHi*rootHi,
      "strict rational sqrt(5) interval certified by integer squares");
const Q=5120000n*S;
const lo=5034167n*S+28557n*rootLo;
const hi=5034167n*S+28557n*rootHi;
function comparePowHalf(a,n){return 2n*a**BigInt(n)-Q**BigInt(n);}
function comparePowOther(a,n){
 // q^n - (1-q) = [a^n-(Q-a)*Q^(n-1)]/Q^n
 return a**BigInt(n)-(Q-a)*Q**BigInt(n-1);
}
check(comparePowHalf(lo,161)>0n,"q^161>1/2 exact lower bound");
check(comparePowHalf(hi,162)<0n,"q^162<1/2 exact upper bound");
check(comparePowOther(lo,1267)>0n,"q^1267>1-q exact lower bound");
check(comparePowOther(hi,1268)<0n,"q^1268<1-q exact upper bound");
check(comparePowOther(lo,1024)>0n && comparePowHalf(hi,1024)<0n,
      "n=1024 simultaneous unique pathwise blank and majority hit CLASS");
const root5=Math.sqrt(5);
const phi=(1+root5)/2,logphi=Math.log(phi);
const q=(5034167+28557*root5)/5120000;
const dq=(42633-14157*root5)/5120000;
const n=1024,P0=q**n,P1=1-P0,DP=n*q**(n-1)*dq;
const blank=-DP/P0/logphi;
const hit=DP/P1/logphi;
const binary=DP*Math.log(P1/P0)/logphi;
check(q>0 && q<1 && dq>0,"original q, J23 probability jet positive");
check(Math.abs(P0-0.012216322302382)<1e-14,"existing full128 blank probability");
check(Math.abs(blank+4.5818938450528)<1e-10,
      "owned original n=1024 pathwise J23 MDL source");
check(Math.abs(hit-0.05666614384328835)<1e-11 && hit>0,
      "opposite-sign classwise J23 source from same COMPLETE instrument");
check(Math.abs(hit+P0/P1*blank)<1e-12,
      "exact complement/source ratio of class and single path");
check(Math.abs(binary-0.24587599876334634)<1e-11,
      "whole binary class Shannon first source is distinct");
check(Math.abs(binary-hit)>0.1 && Math.abs(hit-blank)>1,
      "PATH MDL / CLASS MDL / BINARY MEAN are not one physical action");
console.log(JSON.stringify({
 scope:"exact original full128 first-shell class-quotient only",
 q,dq,n,blankProbability:P0,hitProbability:P1,
 nFirstStrictClassWinner:162,nLastCertifiedUniqueBlankPath:1267,
 pathSourceJ23:blank,classSourceJ23:hit,wholeBinaryMeanSourceJ23:binary,
 gr_closed:false
},null,2));
