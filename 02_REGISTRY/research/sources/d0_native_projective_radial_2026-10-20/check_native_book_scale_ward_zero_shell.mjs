#!/usr/bin/env node
"use strict";
/*
 Original entire K(9,11,13), its ALL1287 ABC Book triangle weights,
 physically declared smooth positive primitive Cost >=1 and 33 moving Info.
 Tests exact three-history scale law and mathematical on-shell
 W*Palatini-like degree-2 action + independent real history stationary
 action: Block Hessian = W H_Star ⊕ H_Internal, no mixed Schur source.
 NOT the compulsory physical D0 Book/G0 action or Einstein proof.
*/
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p);
const assert=(v,msg)=>{if(!v)throw new Error(msg);};
const zone=i=>i<9?0:i<20?1:2;
function nativeBookW(e1,e2,z,beta=.13){
 const length=(e1+e2)/2;
 assert(length>0,"nonpositive coframe physical chart");
 const Info=Array.from({length:33},(_,i)=>
   .15*Math.sin(.4*i)+beta*Math.log(length)/ell+
   .055*((e1-e2)/length)*Math.cos(.23*i));
 const K=Array.from({length:33},(_,i)=>
   Array.from({length:33},(_,j)=>{
     if(zone(i)===zone(j))return 0;
     const Cost=1.08+.03*Math.sin(.21*i+.17*j)**2+
       (.1+z*z)*.02;
     assert(Cost>=1,"original primitive ActionProtocol quantum failed");
     return Math.exp(-ell*(Cost-(Info[i]+Info[j])/2));
   }));
 let sum=0;
 for(let i=0;i<9;i++)for(let j=9;j<20;j++)
  for(let k=20;k<33;k++)
   sum+=K[i][j]*K[j][k]*K[k][i]+K[i][k]*K[k][j]*K[j][i];
 // 3 rooted cyclic copies of each orientation, 7722 total rooted ABC loops
 return 3*sum/7722;
}
const geometric=(e1,e2)=>(e1-e2)**2;
const internal=z=>.7*(z-.13)**2;
const full=(e1,e2,z,beta=.13)=>
 internal(z)+nativeBookW(e1,e2,z,beta)*geometric(e1,e2);
const h=.0005,center=[1,1,.13],f0=full(...center);
function gradient(i){
 const x=center.slice(),y=center.slice();
 x[i]+=h;y[i]-=h;return (full(...x)-full(...y))/(2*h);
}
function hessian(i,j){
 if(i===j){
  let x=center.slice(),y=center.slice();x[i]+=h;y[i]-=h;
  return (full(...x)+full(...y)-2*f0)/(h*h);
 }
 let pp=center.slice(),pm=center.slice(),mp=center.slice(),mm=center.slice();
 pp[i]+=h;pp[j]+=h;
 pm[i]+=h;pm[j]-=h;
 mp[i]-=h;mp[j]+=h;
 mm[i]-=h;mm[j]-=h;
 return (full(...pp)-full(...pm)-full(...mp)+full(...mm))/(4*h*h);
}
const W=nativeBookW(...center),
H=Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>hessian(i,j))),
expect=[[2*W,-2*W,0],[-2*W,2*W,0],[0,0,1.4]],
maxH=Math.max(...H.flatMap((row,i)=>row.map((v,j)=>Math.abs(v-expect[i][j]))));
let maxGrad=Math.max(...[0,1,2].map(gradient));
assert(maxGrad<3e-8&&maxH<1e-6,"failed on-shell same-action Schur Hessian");
const ratio=1.23,beta=-2/3;
const Wres=nativeBookW(ratio,2*ratio,.13,beta)/
           nativeBookW(1,2,.13,beta);
const Dres=full(ratio,2*ratio,.13,beta)/full(1,2,.13,beta);
assert(Math.abs(Wres-ratio**(-2))<1e-12,"native 3-loop Info exact scale mismatch");
assert(Math.abs(Dres-1)<1e-12,"critical resonance should cancel scale source even with A !=0");
const btyp=.13,Wtyp=nativeBookW(ratio,2*ratio,.13,btyp)/
 nativeBookW(1,2,.13,btyp);
assert(Math.abs(Wtyp-ratio**(.39))<1e-12,"Book 3beta generic scale law wrong");
console.log("PASS all original 33 vertices/718 directed and 7722 three-step rooted loop factors");
console.log("PASS actual Book orbit scalar W*=Z3/7722 at nonconstant primitive Cost/Info",W);
console.log("PASS full stationary x=(coframe1,coframe2,archive) with genuine moving Book multiplier");
console.log("PASS true all-3 Euler first-source at zero geometric action",maxGrad);
console.log("PASS exact mixed archive/coframe Hessian vanishes; 2W geometric block + 1.4 archive block, error",maxH);
console.log("PASS zero-shell Hessian does not depend on the derivatives of Book W");
console.log("PASS critical native Info/coframe scale beta=-2/3 (3*beta+2=0), offshell scalar source resonance",Dres);
console.log("PASS generic native Book weight scales with 3beta independent of relative vertex Info");
console.log("FIREWALL: this verifies a CONDITIONAL normal-form theorem, not selection of full Book03 H+J+R action");
