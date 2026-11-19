// Exact BigInt arithmetic in Q(p), p^2+p-1=0; no floating-point positivity.
// Certifies N1 three-status Golden probabilities are algebraic and distinct.
// The consequent NO EXACT FINITE ALGEBRAIC-HEAT GIBBS MATCH relies on the
// classical Lindemann transcendence theorem, not a numerical test.
import assert from 'node:assert/strict';
let checks=0;
const ok=(x,m)=>{assert.ok(x,m);checks++;};
const abs=x=>x<0n?-x:x;
function gcd(a,b){
  a=abs(a);b=abs(b);
  while(b!==0n){const t=a%b;a=b;b=t}
  return a;
}
function F(a,b=0n,d=1n){
  a=BigInt(a);b=BigInt(b);d=BigInt(d);
  ok(d!==0n,'nonzero denominator');
  if(d<0n){a=-a;b=-b;d=-d}
  const g=gcd(gcd(a,b),d)||1n;
  return {a:a/g,b:b/g,d:d/g};
}
const ZERO=F(0),ONE=F(1),P=F(0,1),TWO=F(2);
function plus(x,y){return F(x.a*y.d+y.a*x.d,x.b*y.d+y.b*x.d,x.d*y.d);}
function neg(x){return F(-x.a,-x.b,x.d)}
const minus=(x,y)=>plus(x,neg(y));
function mult(x,y){
  return F(x.a*y.a+x.b*y.b,x.a*y.b+x.b*y.a-x.b*y.b,x.d*y.d);
}
function pow(x,n){
  let y=ONE;
  while(n>0){if(n%2)y=mult(y,x);n=Math.floor(n/2);if(n)x=mult(x,x)}
  return y;
}
// Exact sign of A+Bp via the strictly increasing polynomial
// f(x)=x^2+x-1, whose unique positive root is p.
function sign(x){
 const A=x.a,B=x.b;
 if(A===0n)return B>0n?1:B<0n?-1:0;
 if(B===0n)return A>0n?1:-1;
 if((A>0n&&B>0n)||(A<0n&&B<0n))return A>0n?1:-1;
 // t=-A/B>0; sign[(A+Bp)]= -sign(B)*sign[f(t)].
 const N=A*A-A*B-B*B;
 ok(N!==0n,'no rational t can be the irrational p root');
 const sB=B>0n?1:-1,sN=N>0n?1:-1;
 return -sB*sN;
}
const eq=(x,y)=>sign(minus(x,y))===0;
const gt=(x,y)=>sign(minus(x,y))>0;
const lt=(x,y)=>sign(minus(x,y))<0;
ok(eq(plus(pow(P,2),P),ONE),'exact native p^2+p=1');
ok(gt(P,ZERO)&&lt(P,ONE),'positive native irrational p');
const z=F(1,0,2n**20n);
const L=mult(F(4),pow(P,3));
const Q=minus(ONE,mult(z,L));
const R=minus(ONE,mult(mult(z,L),plus(ONE,pow(P,6))));
const d0=mult(Q,R),r0=minus(ONE,d0);
const alpha=pow(minus(ONE,pow(minus(ONE,mult(TWO,pow(P,3))),9)),128);
const factory=pow(mult(pow(minus(ONE,pow(P,120)),4),
            minus(ONE,pow(minus(ONE,mult(F(16),pow(P,9))),20))),43);
const gamma=mult(alpha,factory);
const fail=minus(ONE,gamma),ready0=mult(gamma,d0),ready1=mult(gamma,r0);
const q=[fail,ready0,ready1];
ok(gt(alpha,ZERO)&&lt(alpha,ONE),'exact Golden cap9 readiness');
ok(gt(factory,ZERO)&&lt(factory,ONE),'exact factory cap20 readiness');
ok(gt(gamma,ZERO)&&lt(gamma,ONE),'complete actual positive paid N1 gamma');
ok(gt(r0,ZERO)&&lt(r0,ONE),'original N1 r0 algebraic genuine binary report');
ok(eq(q.reduce(plus,ZERO),ONE),'whole native N1 ternary probability EXACT sum1');
q.forEach((v,i)=>ok(gt(v,ZERO)&&lt(v,ONE),'strict full event probability '+i));
ok(gt(fail,ready0),'actual FAIL status strictly more probable than READY0');
ok(gt(ready0,ready1),'actual READY0 strictly more probable than READY1');
ok(gt(ready1,ZERO),'rare READY1 nonzero, no postselection');
const betaBook=mult(TWO,pow(P,2));
ok(gt(betaBook,ZERO),'original β=2p² nonzero algebraic');
const deg=q.map(x=>({numA_bits:abs(x.a).toString(2).length,
 numB_bits:abs(x.b).toString(2).length,denom_bits:x.d.toString(2).length}));
console.log(JSON.stringify({status:"PASS_EXACT_Q_P_FIELD",checks,
nativePolynomial:"p²+p−1=0",strictNativeStatusOrdering:"q_fail > q_READY0 > q_READY1 > 0",
threeOutcomesSumOne:true,algebraicInverseTemperature:"2p²",
numeratorDenominatorBitLengths:deg,
theorem:"Lindemann: exp(nonzero algebraic) transcendental; normalized unequal algebraic q cannot be exact Gibbs eigenvalues of finite algebraic heat",
scope:"exact native common-null q and finite algebraic heat only; dynamic log-spectrum/other Book sources open",GR_closed:false}));
