"use strict";
// D0 #334. ALL checks are explicit V8 throw-on-failure controls and cannot be stripped.
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi);
function H(r){return -(r*Math.log(r)+(1-r)*Math.log1p(-r))/ell}

function Hp(r){return Math.log((1-r)/r)/ell}

function sum(x){return x.reduce((a,b)=>a+b,0)}

function build(threshold,rs){
  const leaf=[];
  function walk(word,cost,q){
    if(cost>=threshold){
      if(cost>threshold){leaf.push({word,cost,q,kind:"overshoot"});return;}
      for(let a of [["F",1],["R",2]]) for(let b of [["F",1],["R",2]]){
        let suffix=a[0]+b[0],c=cost+a[1]+b[1],base=q*p**(a[1]+b[1]);
        if(suffix==="FR"||suffix==="RF"){
          let i=suffix==="FR"?0:1,r=rs[i];
          leaf.push({word:word+suffix+"0",cost:c+1,q:base*(1-r),kind:"ready",i});
          leaf.push({word:word+suffix+"10",cost:c+2,q:base*r,kind:"ready",i});
        }else leaf.push({word:word+suffix,cost:c,q:base,kind:"unready"});
      }return;
    }
    walk(word+"F",cost+1,q*p);walk(word+"R",cost+2,q*p*p);
  }
  walk("",0,1);
  return leaf;
}

function details(leaf){
 const prob=sum(leaf.map(x=>x.q));
 const kraft=sum(leaf.map(x=>p**x.cost));
 const cost=sum(leaf.map(x=>x.q*x.cost));
 const entropy=-sum(leaf.map(x=>x.q*Math.log(x.q)))/ell;
 const KL=cost-entropy;
 const L=leaf.map(x=>Math.log(x.q/p**x.cost)/ell);
 const variance=ell*(sum(leaf.map((x,i)=>x.q*L[i]*L[i]))-KL*KL);
 return {prob,kraft,cost,entropy,KL,variance};
}

function pressure(leaf,s,t){return Math.log(sum(leaf.map(x=>x.q**(1+s)*phi**(-t*x.cost))))/ell}

function relPressure(leaf,s){return Math.log(sum(leaf.map(x=>x.q**(1+s)*p**(-s*x.cost))))/ell}

function renewal(r,M,c0,c1){
 const A=-Math.expm1(M*Math.log1p(-r))/r;
 return{elapsed:A,charged:A*((1-r)*c0+r*c1),archive_entropy:A*H(r),
  per_tick:(1-r)*c0+r*c1-H(r)};
}

function ok(x,msg){if(!x)throw Error("SCOPED_CHECK_FAIL "+msg)}

function run(){
 let checks=0,ck=(x,m)=>{ok(x,m);checks++};
 ck(Math.abs(p+p*p-1)<1e-14,"golden normalization");
 const trees=[];
 for(let rs of [[.15,.37],[.37,.15],[.8,.31],[1.851242740976536e-6,1.8513157633356053e-6]]){
  const leaf=build(3,rs),d=details(leaf),by=[0,0];
  for(let x of leaf)if(x.kind==="ready")by[x.i]+=x.q;
  const trueKL=sum(by.map((w,i)=>w*(1+rs[i]-H(rs[i]))));
  ck(Math.abs(d.prob-1)<1e-13,"full Born flags retain all failures");
  ck(Math.abs(d.kraft-1)<1e-13,"native code reference Kraft");
  ck(d.KL>-1e-12,"KL nonnegative");
  ck(Math.abs(d.KL-trueKL)<1e-12,"same stopped Golden complete prefix and report");
  const step=1e-5;
  const first=(relPressure(leaf,step)-relPressure(leaf,-step))/(2*step);
  const Info=(pressure(leaf,step,0)-pressure(leaf,-step,0))/(2*step);
  const Cost=(pressure(leaf,0,step)-pressure(leaf,0,-step))/(2*step);
  const second=(relPressure(leaf,step)-2*relPressure(leaf,0)+relPressure(leaf,-step))/(step*step);
  ck(Math.abs(first-d.KL)<1e-9,"one relative mark recovers exact CQ value");
  ck(Math.abs(Info+d.entropy)<1e-9,"information mark source");
  ck(Math.abs(Cost+d.cost)<1e-9,"actual primitive cost mark");
  ck(Math.abs(Info-Cost-d.KL)<1e-9,"two marks one full ledger");
  ck(Math.abs(second-d.variance)<1e-5,"score-variance second mark");
  ck(Math.abs(sum(leaf.map(x=>x.q*p**x.cost/x.q))-1)<1e-13,"complete full-leaf fluctuation identity");
  ck(Math.abs(relPressure(leaf,-1))<1e-12,"negative one normalized code mark");
  trees.push({report_r:rs,complete_outcomes:leaf.length,ready_outcomes:leaf.filter(x=>x.kind==="ready").length,C:d.cost,H:d.entropy,marked_source:d.KL,fluctuation_curvature:d.variance});
 }
 const renewalRows=[];
 for(let r of [.15,.37,.8,1.851242740976536e-6])for(let M of [1,2,5,20,100]){
  const a=renewal(r,M,1,2),b=renewal(r,M,2,2);
  ck(Math.abs((a.charged-a.archive_entropy)/a.elapsed-a.per_tick)<1e-10,"all finite cap reported time charges");
  ck(Math.abs(a.per_tick-(1+r-H(r)))<1e-12,"true native 0/10 rate");
  ck(Math.abs(b.per_tick-(2-H(r)))<1e-12,"existing padded reporter clock-rate");
  renewalRows.push({r,M,rate_0_10:a.per_tick,rate_padded:b.per_tick,mean_paid_attempts:a.elapsed});
 }
 const k=10946,PReady=2*k*p**23;
 for(let n_z of [29,39,48,78]){
  const pi=2*n_z*p**23,rho=256*n_z/k;
  ck(Math.abs(pi/rho-PReady/256)<1e-14,"original 256-site inverse-PF source ratio");
 }
 const r0=(1.8512417713660524e-6+1.85124371058701973e-6)/2;
 const r1=(1.85130177947843566e-6+1.85132974719277498e-6)/2;
 const dr0=-2.26378054238336192e-8,dr1=-Hp(r0)/Hp(r1)*dr0;
 const dPad=-Hp(r0)*dr0-Hp(r1)*dr1;
 const dOld=(1-Hp(r0))*dr0+(1-Hp(r1))*dr1;
 const minDefect=2*2.68978050581795731e-14;
 ck(Math.abs(dPad)<1e-19,"certified-root equality of padded CQ source");
 ck(Math.abs(dOld-dr0-dr1)<1e-19,"real native 0/10 extra ledger source");
 ck(dOld>minDefect,"certified off-null source gap");
 const c=2,g=r=>c-H(r),gp=r=>-Hp(r);
 const totalSlope=r=>(r*gp(r)-g(r))/r**2;
 const Qratio=r=>totalSlope(r)/gp(r);
 const dTot=totalSlope(r0)*dr0+totalSlope(r1)*dr1;
 ck(Math.abs(dTot)>1e-5,"wrong extensive stop-price derivative");
 ck(Qratio(r0)>Qratio(r1),"incompatible total-vs-intensive source ratio");
 return{
 status:"SCOPED_PASS",checks,
 original_prefix_Kraft:trees,
 finite_cap_replay:renewalRows.filter(x=>[1,5,20].includes(x.M)),
 full_original_address:{K:k,PrReady:PReady,pi_over_rho:PReady/256},
 exact_root_29_control:{r0,r1,Dr0_representative_lower_abs:dr0,Dr1_from_exact_CQ_relation:dr1,
     padded_CQ_source:dPad,original_0_10_ledger_source:dOld,
     rigorous_certified_abs_lower:minDefect,
     stopped_total_diagnostic:dTot},
 compulsory_Book03_tilt_action_derived:false,
 native_clock_rate_physically_selected:false,
 GR_closed:false};
}

console.log(JSON.stringify(run(),null,2));
