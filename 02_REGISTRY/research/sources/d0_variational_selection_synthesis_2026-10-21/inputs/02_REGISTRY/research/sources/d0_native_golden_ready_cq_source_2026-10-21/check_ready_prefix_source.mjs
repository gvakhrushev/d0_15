// Exact original Golden F/R first-passage + READY FR/RF + source Price.
// No simulated site census: consumes native theorem sum n_z=F21,
// 29<=n_z<=78, 256 sites and the original inverse-PF definition.
const assert=(v,msg)=>{if(!v)throw Error("FAIL "+msg)}
const gcd=(a,b)=>{if(a<0n)a=-a;if(b<0n)b=-b;while(b){const r=a%b;a=b;b=r;}return a||1n};
class K {
 constructor(a,b=0,d=1){a=BigInt(a);b=BigInt(b);d=BigInt(d);assert(d!==0n,"denom");if(d<0n){a=-a;b=-b;d=-d;}const g=gcd(gcd(a,b),d);this.a=a/g;this.b=b/g;this.d=d/g;}
 static of(x){return x instanceof K?x:new K(x)}
 add(x){x=K.of(x);return new K(this.a*x.d+x.a*this.d,this.b*x.d+x.b*this.d,this.d*x.d)}
 neg(){return new K(-this.a,-this.b,this.d)}
 sub(x){return this.add(K.of(x).neg())}
 mul(x){x=K.of(x);return new K(this.a*x.a+this.b*x.b,this.a*x.b+this.b*x.a-this.b*x.b,this.d*x.d)}
 div(n){return new K(this.a,this.b,this.d*BigInt(n))}
 eq(x){x=K.of(x);return this.a===x.a&&this.b===x.b&&this.d===x.d}
 num(){const DEN=10n**50n,PLO=61803398874989484820458683436563811772030917980576n;const BIG=10n**26n;return Number((this.a*DEN+this.b*PLO)*BIG/(this.d*DEN))/1e26}
 str(){return this.a+"+"+this.b+"p / "+this.d}
}
const p=new K(0,1),O=new K(1),Z=new K(0),pow=(v,n)=>{let a=O;for(let k=0;k<n;k++)a=a.mul(v);return a};
assert(p.mul(p).eq(O.sub(p)),"true Golden p+p²=1");
const F=[0n,1n];for(let n=2;n<=55;n++)F[n]=F[n-1]+F[n-2];
for(let n=1;n<=50;n++) {
  const exact=pow(p,n).mul(F[n+1]),overshoot=pow(p,n+1).mul(F[n]);
  assert(exact.add(overshoot).eq(O),"native whole first-crossing Fibonacci normalized at "+n);
}
const n=20,N=F[n+1],No=F[n],M=256n;
assert(N===10946n&&No===6765n,"actual native cost20 Fibonacci counts");
const exact=pow(p,n).mul(N),overshoot=pow(p,n+1).mul(No);
const FF=pow(p,n+2).mul(N),FR=pow(p,n+3).mul(N),
      RF=FR,RR=pow(p,n+4).mul(N),ready=FR.add(RF);
assert(overshoot.add(FF).add(FR).add(RF).add(RR).eq(O),
       "complete native first-crossing plus two original Golden outcomes");
const wholeCost=overshoot.mul(n+1).add(FF.mul(n+2))
  .add(FR.mul(n+3)).add(RF.mul(n+3)).add(RR.mul(n+4));
const directCost=new K(n).add(overshoot)
   .add(exact.mul(2).mul(p.add(p.mul(p).mul(2))));
assert(wholeCost.eq(directCost),
   "literal mean Golden prefix cost equals FULL prefix-code entropy");
const weightedCoeff=pow(p,n+3).mul(2).mul(N).div(M);
assert(ready.div(M).eq(weightedCoeff),"all-site common true weighted coefficient");
for(let siteN=29;siteN<=78;siteN++){
 const pi=new K(siteN).div(N),rho=pi.mul(M);
 const qForSite=pow(p,n+3).mul(2).mul(siteN);
 assert(qForSite.div(1).eq(ready.mul(pi)),
        "native Qw event weight site n="+siteN);
 // True per-site inverse PF source: ready(z)/rho(z)=P_ready/256.
 // Rewrite without algebraic inversion by multiplying both sides by rho.
 assert(qForSite.eq(weightedCoeff.mul(rho)),
        "actual all42 source per site independent of n_z "+siteN);
}
const exampleN=39;const rho=new K(M*BigInt(exampleN)).div(N);
assert(rho.eq(new K(384,0,421)),"native obstruction site rho=384/421");
const z=O.div(1048576),L=pow(p,3).mul(4);
const Q=O.sub(z.mul(L)),R=O.sub(z.mul(L.mul(new K(2).sub(L))));
const r0=O.sub(Q.mul(R)),rf=z.mul(Q).mul(pow(p,11)).mul(4);
const rq=z.mul(pow(p,6)).mul(R.add(Q.mul(pow(p,6)))).mul(8);
assert(rq.mul(Q).mul(pow(p,5)).eq(rf.mul(2).mul(R.add(Q.mul(pow(p,6))))),
  "finite original signed matter/gravity ratio exact, not a fit");
const phi=1/p.num(),hprime=Math.log((1-r0.num())/r0.num())/Math.log(phi);
assert(r0.num()<p.mul(p).num() && hprime>1,"native 0/10 Cost-minus-CQ-Info slope nonzero");
const sourceWeight=weightedCoeff.num()*(1-hprime);
const h=r=>-(r*Math.log(r)+(1-r)*Math.log1p(-r))/Math.log(phi);
const kl=r=>1+r-h(r);
const qTarget=p.mul(p).num();
const refkl=r=> (r*Math.log(r/qTarget)+(1-r)*Math.log((1-r)/p.num()))/Math.log(phi);
for(const prob of [r0.num(),.03,.3,.6,.9])
 assert(Math.abs(kl(prob)-refkl(prob))<1e-12,"true native final binary code KL");
function report(){return {
 status:"PASS_GOLDEN_FIRST_PASSAGE_ALL_OUTCOME_CQ_PF",
 n,original_paths_exact:String(N),original_overshoot_words:String(No),
 full_stopped_prefix_leaf_types:{overshoot:String(No),FF:String(N),FR:String(N),RF:String(N),RR:String(N)},
 P_exact:exact.num(),P_overshoot:overshoot.num(),P_Q_ready:ready.num(),
 expected_native_Golden_code_cost:wholeCost.num(),
 full_Golden_prefix_entropy_equals_expected_code_price:true,
 original_site_count_input:[256,29,78,10946],
 source_pf_per_cell_constant:weightedCoeff.num(),
 full_site_CQ_0_10_slope:sourceWeight,
 native_r0:r0.num(),native_r_geom:rf.num(),native_r_mat:rq.num(),
 finite_lambda_minus:-rq.num()/rf.num(),
 site39:{rho:rho.num(),site_Qready:ready.num()*39/10946},
 full_code_CQ_identity:"S=2*p^(n+3)*sum_z n_z D_phi(Bern(r_z)||Bern(p^2)) + paid nonconstant-work residual",
 physical_gr_closed:false,real_Book03_Info_selected:false,source_effects_same_history_admitted:false
}}
if(typeof console!=="undefined")console.log(JSON.stringify(report(),null,2));
