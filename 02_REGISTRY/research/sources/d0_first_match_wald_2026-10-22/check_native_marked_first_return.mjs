// Same original Golden 0/10 *full* native prefix cost mark and true blank-return.
import assert from 'node:assert/strict';
const p=(Math.sqrt(5)-1)/2,phi=1/p;
let checks=0;
function check(x,msg){assert.ok(x,msg);checks++;}
function close(x,y,t=4e-11,msg='close'){
  check(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),msg+': '+x+' vs '+y);
}
const L=(r,K)=>3-(1-r)**K-r**K;
function fullMark(r,t,kappa=0){
 const a=1-r,x=Math.exp(-t),d0=1-a*x**(1+kappa),d1=1-r*x**(2+kappa);
 return r*r*x**(4+kappa)/d0+a*a*x**(2+kappa)/d1;
}
function fullMarkDerivative(r,t,kappa=0){
 const a=1-r,x=Math.exp(-t);
 const d0=1-a*x**(1+kappa),d1=1-r*x**(2+kappa);
 return x**(4+kappa)*(2*r/d0-r*r*x**(1+kappa)/(d0*d0))+
        x**(2+kappa)*(-2*a/d1+a*a*x**(2+kappa)/(d1*d1));
}
function capMark(r,t,kappa,K){
 const a=1-r,x=Math.exp(-t);
 const u=a*x**(1+kappa),v=r*x**(2+kappa);
 const val0=r*r*x**(4+kappa)*(-Math.expm1(K*Math.log(u)))/(1-u);
 const val1=a*a*x**(2+kappa)*(-Math.expm1(K*Math.log(v)))/(1-v);
 return val0+val1+r*a**K*x**(K+2+kappa*K)+a*r**K*x**(2*K+1+kappa*K);
}
function leafMark(r,t,kappa,K){
 const a=1-r;
 let sum=0,mass=0,length=0,cost=0,second=0,elapsedMark=0,clockCost=0;
 for(let n=0;n<K;n++){
   const p1=r*r*a**n, p0=a*a*r**n;
   for(const [pr,C] of [[p1,4+n+kappa*(n+1)],[p0,2+2*n+kappa*(n+1)]]){
     const T=n+2;
     sum+=pr*Math.exp(-t*C);
     mass+=pr;length+=pr*T;
     cost+=pr*C;second+=pr*C*C;
     elapsedMark+=pr*Math.exp(-t*T);
     clockCost+=pr*(T-1);
   }
 }
 for(const [pr,C] of [
   [r*a**K,K+2+kappa*K],
   [a*r**K,2*K+1+kappa*K]
 ]){
   const T=K+1;
   sum+=pr*Math.exp(-t*C);
   mass+=pr;length+=pr*T;cost+=pr*C;
   second+=pr*C*C;elapsedMark+=pr*Math.exp(-t*T);
   clockCost+=pr*(T-1);
 }
 return {sum,mass,length,cost,second,elapsedMark,clockCost};
}
for(const r of [0.000001851245,0.04,0.18,0.49,0.61,0.83,0.97]){
  for(const K of [1,2,3,5,8,16]){
    for(const kappa of [0,0.7,2.25]){
      const t=.27,leaf=leafMark(r,t,kappa,K),native=capMark(r,t,kappa,K);
      close(leaf.sum,native,7e-13,'marked ALL branches incl abort, no postselection');
      close(leaf.mass,1,9e-13,'complete capped first-return physical mass');
      close(leaf.length,L(r,K),8e-13,'true full registered clock length');
      close(leaf.clockCost,L(r,K)-1,8e-13,'real number of paid equality comparisons');
      close(leaf.cost,L(r,K)*(1+r)+kappa*(L(r,K)-1),2e-12,'true actual full code+comparison cost');
      close(capMark(r,0,kappa,K),1,8e-13,'true unmarked normalization');
      const h=1e-5;
      const second=(capMark(r,h,kappa,K)+capMark(r,-h,kappa,K)-2)/(h*h);
      close(second,leaf.second,6e-5,'second native total charged moment');
    }
  }
  for(const kappa of [0,.33,1.8]){
    for(const t of [.02,.17,Math.log(phi),.8]){
      const n=fullMark(r,t,kappa);
      const h=Math.min(5e-7,.2*r,.2*(1-r));
      const num=(fullMark(r+h,t,kappa)-fullMark(r-h,t,kappa))/(2*h);
      const ana=fullMarkDerivative(r,t,kappa);
      close(num,ana,3e-7,'uncapped FULL marked source derivative');
      check(n>0 && n<=1+2e-14,'positive original marked whole cost');
      const z=.29;
      const fullBook=Math.log(n)-Math.log((1-z)*n+z*0);
      close(fullBook,-Math.log1p(-z),3e-14,'real normalized Book blank return remains source blind');
    }
  }
}
const goldenT=Math.log(phi);
const goldenZero=fullMark(0,goldenT,0);
const goldenD=fullMarkDerivative(0,goldenT,0);
close(goldenZero,p*p,3e-15,'native Golden exact 0/10 mark normalization');
close(goldenD/goldenZero,-phi,2e-14,'NATIVE -phi marked log source, no fit');
for(const r of [0.000001851242,0.000001851329]){
 const slope=fullMarkDerivative(r,goldenT,0)/fullMark(r,goldenT,0);
 check(slope< -1.618 && slope> -1.6181,'actual rare original reporter marked response near -phi');
}
for(const r of [0.13,0.45,0.82]){
 const a=1-r;
 for(const t of [.14,.32,.71]){
   const v=Math.exp(-t);
   const analytic=v*v*(r*r/(1-a*v)+a*a/(1-r*v));
   const K=15,leaf=leafMark(r,t,0,K);
   const error=(r*a**K+a*r**K);
   check(Math.abs(analytic-leaf.elapsedMark)<7*error+4e-13,'complete elapsed-clock Laplace tail, not mean alone');
 }
}
console.log(JSON.stringify({status:"PASS",checks,
 nativeGoldenLogSourceLimit:"-phi",
 fullOneRunNativeBlankBookSource:0,
 nativeH4MarkedLogSource:"approximately -1.6180337",
 allEarlyAbortLeavesRetained:true,
 compulsoryBookHeatAndInfoIdentified:false}));
