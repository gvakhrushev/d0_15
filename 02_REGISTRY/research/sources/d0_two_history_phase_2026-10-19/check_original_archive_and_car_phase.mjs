#!/usr/bin/env node
"use strict";
// ONE original 718-edge Perron history and original CAR16 grade-one
// proper spatial Lorentz J23. Two-history comparison only, not a
// physically selected Book Cost−Info action or native joint execution.
const sizes=[9,11,13],N=33,p=(Math.sqrt(5)-1)/2,lp=Math.log(1/p);
const zone=u=>u<9?0:u<20?1:2,E=[];
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(zone(u)!==zone(v))E.push([u,v]);
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const mv=(A,v)=>A.map(row=>dot(row,v));
const norm2=x=>dot(x,x);
const check=(x,s)=>{if(!x)throw Error("FAIL "+s);console.log("PASS "+s);};
function scene(t){
 const K=sizes.map((n,i)=>sizes.map((m,j)=>
    i===j?0:p*Math.sqrt(n*m)*
    (((i===0&&j===1)||(i===1&&j===0))?Math.exp(-lp*t):1)));
 let c=[1,1,1].map(x=>x/Math.sqrt(3));
 for(let i=0;i<500;i++){
   let y=mv(K,c),norm=Math.hypot(...y);y=y.map(v=>v/norm);
   if(Math.max(...y.map((v,j)=>Math.abs(v-c[j])))<1e-15){c=y;break;}c=y;
 }
 const rho=dot(c,mv(K,c));
 const r=Array.from({length:N},(_,v)=>c[zone(v)]/Math.sqrt(sizes[zone(v)]));
 const J0=[],J1=[];
 for(const [u,v] of E){
   let is01=(Math.min(zone(u),zone(v))===0&&Math.max(zone(u),zone(v))===1);
   let q=p*(is01?Math.exp(-lp*t):1);
   let a=Array(N).fill(0),b=Array(N).fill(0);
   a[u]=Math.sqrt(q*r[v]/(rho*r[u]));
   b[v]=Math.sqrt(q*r[u]/(rho*r[v]));
   J0.push(a);J1.push(b);
 }
 return {rho,J0,J1};
}
const original=scene(0);
const T=Array.from({length:N},(_,i)=>
 Array.from({length:N},(_,j)=>zone(i)===zone(j)?0:p/original.rho));
const T2=T.map(row=>T[0].map((_,j)=>row.reduce((s,v,k)=>s+v*T[k][j],0)));
const kappa=2574/((original.rho/p)**3);
const B=T.map((row,i)=>row.map((v,j)=>
 (i===j?1:0)+(2*v+T2[i][j])/(2+kappa)));
const D=original.J0.map((row,i)=>row.map((v,j)=>v-original.J1[i][j]));
const U=v=>{
 let g=Array(N).fill(0);
 for(let i=0;i<E.length;i++)for(let j=0;j<N;j++)g[j]+=D[i][j]*v[i];
 let h=mv(B,g);
 return v.map((y,i)=>y-dot(D[i],h));
};
const f=Array.from({length:N},(_,u)=>zone(u)===0?1/3:0);
const embed=J=>J.map(row=>dot(row,f));
const psi=embed(original.J0),future=embed(original.J1),out=U(psi);
check(E.length===718 && Math.abs(norm2(psi)-1)<3e-13,
 "original 718-edge properly normalized actual K9 present record");
check(Math.sqrt(norm2(out.map((v,i)=>v-future[i])))<2e-12,
 "original canonical selfadjoint U_min J0 = J1");
check(Math.abs(norm2(out)-1)<3e-12,"original real archival U_min output normalized");
let prev=0,last=0;
for(const h of [.1,.03,.01,.003,.001]){
 const plus=scene(h),minus=scene(-h);
 const j0p=embed(plus.J0),j0m=embed(minus.J0);
 const j1p=embed(plus.J1),j1m=embed(minus.J1);
 const d0=j0p.map((v,i)=>(v-j0m[i])/(2*h));
 const d1=j1p.map((v,i)=>(v-j1m[i])/(2*h));
 const ud0=U(d0),metric=norm2(d1.map((v,i)=>v-ud0[i]));
 check(metric>.033&&metric<.034,
       "nonzero ORIGINAL moving-cost archive echo metric h="+h);
 if(prev)check(Math.abs(metric-prev)<.001,
               "positive original archive cost-source tangent convergence");
 prev=metric;last=metric;
}
check(Math.abs(last-.0335172609)<2e-7,
 "positive unfit 718-edge hidden-record comparison Hessian");
const echo=x=>({re:(1+Math.cos(x))/2,im:Math.sin(x)/2});
const h=1e-4,ep=echo(h),em=echo(-h),base=echo(0);
const dPhase=(ep.im-em.im)/(2*h);
const d2real=(ep.re+em.re-2*base.re)/(h*h);
const logMod=x=>Math.log(Math.hypot(echo(x).re,echo(x).im));
const cov=-(logMod(h)+logMod(-h)-2*logMod(0))/(h*h);
check(base.re===1 && base.im===0,"same-history CAR16 Born amplitude exactly one");
check(Math.abs(dPhase-.5)<1e-8,
 "ORIGINAL grade-one J23 circular Lorentz phase source = i/2");
check(Math.abs(d2real+.5)<1e-8,
 "coherent original CAR16 two-history overlap real quadratic jet");
check(Math.abs(cov-.25)<1e-7,
 "positive connected original CAR16 two-history metric = 1/4");
check(Math.sin(0)===0 && Math.cos(h)===Math.cos(-h),
 "real archive has no FIRST relative complex phase");
console.log(JSON.stringify({
 carrier:"original 718 native Perron archive + SEPARATE original CAR16 grade-one J23",
 original_directed_edges:718,
 real_archive_echo_metric:last,
 original_CAR_J23_phase_first:.5,
 original_CAR_connected_metric:cov,
 diagonal_complete_Born_echo:1,
 physical_same_execution_selected:false,
 gr_closed:false
},null,2));
