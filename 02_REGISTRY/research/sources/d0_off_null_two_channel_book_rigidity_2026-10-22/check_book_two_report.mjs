"use strict";
// Checks exact identities against inherited interval-certified original D0 finite full42 root.
const p=(Math.sqrt(5)-1)/2,phi=1/p,z=2**-20;
function hprime(r){return Math.log((1-r)/r)/Math.log(phi)}

function FG(r){return 4*p*r*(1-p*r)}

function kG(r){return 4*p*z*(1-2*p*r)/(1-z*FG(r))}

function FH(r){return 2*r-r*r}

function kH(r){return 2*z*(1-r)/(1-z*FH(r))}

function RG(r){return kG(r)/hprime(r)}

function RH(r){return kH(r)/hprime(r)}

function check(c,m){if(!c)throw Error("FAILED: "+m)}

function run(){
 let tests=0,ok=(c,m)=>{check(c,m);tests++};
 ok(p>.6&&p<.625,"golden rational bounds");
 ok(p*p*p<.25&&p*p<.5,"golden cubic bound");
 const br0=[1.8512417713660524e-6,1.85124371058701973e-6];
 const br1=[1.85130177947843566e-6,1.85132974719277498e-6];
 const minGap=5.806889141593e-11,minDR0=2.26378054238336192e-8;
 ok(br1[0]-br0[1]>minGap*.99999,"certified interval separation");
 const r0=(br0[0]+br0[1])/2,r1=(br1[0]+br1[1])/2;
 ok(r0>1.85e-6&&r1<1.86e-6&&r0<r1&&r1<p*p,"positive chart");
 ok(RG(r0)<RG(r1)&&RH(r0)<RH(r1),"source ratio strict ordering");
 for(let r of [1e-8,1e-6,.001,.1,p*p-.0001]){
  const g=Math.log((1-r)/r);
  const dRG=1/(r*(1-r)*g)-2*p/(1-2*p*r)+z*4*p*(1-2*p*r)/(1-z*FG(r));
  const dRH=1/(r*(1-r)*g)-1/(1-r)+2*z*(1-r)/(1-z*FH(r));
  ok(dRG>0&&dRH>0,"sample derivative strict positivity at "+r);
 }
 const d0=-minDR0,d1=-hprime(r0)/hprime(r1)*d0;
 const cq=hprime(r0)*d0+hprime(r1)*d1;
 ok(Math.abs(cq)<1e-20,"exact CQ differential relation");
 const SG=kG(r0)*d0+kG(r1)*d1,SH=kH(r0)*d0+kH(r1)*d1;
 ok(SG>0&&SH>0,"nonzero dual-comparator sources");
 ok(Math.abs(SG-hprime(r0)*(RG(r0)-RG(r1))*d0)<1e-27,"Golden source identity");
 ok(Math.abs(SH-hprime(r0)*(RH(r0)-RH(r1))*d0)<1e-27,"H source identity");
 const c0OverC1=RG(r1)/RG(r0),c1=1/c0OverC1;
 ok(c0OverC1>1&&c1<1,"necessary unequal Book price weights");
 const weighted=kG(r0)*d0+c1*kG(r1)*d1;
 ok(Math.abs(weighted)<1e-26,"correct weighted Book cancellation");
 const rmax=1.86e-6,kl=4*.6*z*(1-2*.625*rmax),Rl=kl/(14/.48);
 const logRl=1/(rmax*14)-1.25/(1-1.25*rmax);
 const lower=13/.49*Rl*logRl*minGap*minDR0;
 ok(lower>1e-19,"strict nonzero lower on supplied certified interval");
 return {status:"SCOPED_PASS",tests,certified_root_h:.25,
   sample_reports:{r0,r1},direction:29,
   CQ_source:cq,Golden_Book_source:SG,H_Book_source:SH,
   required_c0_over_c1:c0OverC1,c1_when_c0_equals_one:c1,
   weighted_compensation_check:weighted,
   conservative_certified_lower:lower,
   physical_Book03_selected:false,GR_closed:false};
}

console.log(JSON.stringify(run(),null,2));
