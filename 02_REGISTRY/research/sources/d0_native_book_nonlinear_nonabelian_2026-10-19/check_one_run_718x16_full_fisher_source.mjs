#!/usr/bin/env node
"use strict";
// True original 718 supported one-sided Perron/Doob Golden Cost history,
// conditional complete ORIGINAL 2-fresh Golden-p CAR16/Choi 16 outcomes.
// Mathematical joint native-type instrument, not compulsory physical fullStep.
const p=(Math.sqrt(5)-1)/2,L=Math.log(1/p),ns=[9,11,13],zone=u=>u<9?0:u<20?1:2;
const edge=[];for(let u=0;u<33;u++)for(let v=0;v<33;v++)if(zone(u)!==zone(v))edge.push([u,v]);
const need=(b,n)=>{if(!b)throw Error("FAIL "+n);console.log("PASS "+n)};
const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);
function native(t){
 const K=ns.map((n,i)=>ns.map((m,j)=>i===j?0:p*Math.sqrt(n*m)*Math.exp(-L*t*(
  ((i===0&&j===1)||(i===1&&j===0))?1:0))));
 let r=[1,1,1].map(x=>x/Math.sqrt(3));
 for(let k=0;k<900;k++){
  let y=K.map(row=>dot(row,r)),norm=Math.hypot(...y),v=y.map(x=>x/norm);
  if(Math.max(...v.map((x,i)=>Math.abs(x-r[i])))<2e-15){r=v;break;}r=v;
 }
 const lambda=dot(r,K.map(row=>dot(row,r)));
 const rv=Array.from({length:33},(_,u)=>r[zone(u)]/Math.sqrt(ns[zone(u)]));
 const sum=rv.reduce((s,x)=>s+x,0),prior=rv.map(x=>x/sum);
 const weights=edge.map(([u,v])=>{
  const ab=((zone(u)===0&&zone(v)===1)||(zone(u)===1&&zone(v)===0));
  return prior[u]*p*Math.exp(-L*t*(ab?1:0))*rv[v]/(lambda*rv[u]);
 });
 return {weights,prior,lambda};
}
const origin=native(0),positive=native(.0001);
need(edge.length===718,"all original 718 directed scene edges retained");
need(Math.abs(origin.weights.reduce((s,x)=>s+x,0)-1)<1e-13,
 "original true ONE-SIDED initial Perron distribution and transition weights normalize");
need(Math.abs(positive.weights.reduce((s,x)=>s+x,0)-1)<1e-13,
 "original field-dependent native one-sided history remains normalized");
const dqScalar=origin.weights.map((w,i)=>(positive.weights[i]-w)/.0001);
const marks=Array.from({length:12},()=>p**4/24);
const q0=marks.concat([p**4/2,p**3,p**3,p*p]);
need(q0.length===16&&q0.every(x=>x>0)&&Math.abs(q0.reduce((s,x)=>s+x,0)-1)<1e-14,
 "ALL 16 Golden-p true native two-fresh-flag outcomes positive and sum1");
const dQ=Array.from({length:6},(_,g)=>{
 const row=Array(16).fill(0);
 row[2*g]=p**4/(12*Math.SQRT2);
 row[2*g+1]=-(p**4)/(12*Math.SQRT2);
 return row;
});
const nativeSix=p**4/6;
for(let i=0;i<6;i++)for(let j=0;j<6;j++){
 const value=q0.reduce((s,q,k)=>s+dQ[i][k]*dQ[j][k]/q,0);
 need(Math.abs(value-(i===j?nativeSix:0))<2e-14,
      "complete native-p marked-CAR6 conditional Fisher "+i+"/"+j);
}
const I=Array.from({length:7},()=>Array(7).fill(0));
for(let ix=0;ix<edge.length;ix++){
 const w=origin.weights[ix],dw=dqScalar[ix],sign=edge[ix][0]<edge[ix][1]?1:-1;
 for(let j=0;j<16;j++){
  const q=q0[j],Q=w*q;
  const deriv=[dw*q,...dQ.map(row=>w*sign*row[j])];
  for(let a=0;a<7;a++)for(let b=0;b<7;b++)I[a][b]+=deriv[a]*deriv[b]/Q;
 }
}
const scalar=origin.weights.reduce((s,w,i)=>s+dqScalar[i]*dqScalar[i]/w,0);
need(scalar>1e-6&&Math.abs(I[0][0]-scalar)<1e-12,
 "entire real moving ONE-SIDED Book preparation included in joint Fisher");
for(let i=1;i<7;i++){
 need(Math.abs(I[0][i])<1e-13,
 "zero scalar/ordered CAR cross source forced by conditional positive 16-effect completeness "+i);
 for(let j=1;j<7;j++)
  need(Math.abs(I[i][j]-(i===j?nativeSix:0))<2e-13,
      "full actual 718 x 16 original scene-marked Fisher entry "+i+"/"+j);
}
need(Math.abs(dqScalar.reduce((s,x)=>s+x,0))<1e-9,
 "native scalar Cost one-sided derivative includes normalizer/source and sums zero");
console.log(JSON.stringify({
 original_edges:edge.length,original_full_outcomes:edge.length*q0.length,
 full_joint_native_p_fisher:I,
 scalar_book_one_sided_fisher:scalar,
 original_Golden_six_conditional_Fisher:p**4/6,
 cross_source_max:Math.max(...I[0].slice(1).map(Math.abs)),
 original_CAR16_one_particle_Choi_16Outcome_carrier:"genuine Golden p with GOOD/BAD; higher grades retained",
 original_scene_Lorentz_assignment:"reversal-compatible mathematical test, not native 4D Role controller",
 compulsory_selected_action:false,GR_closed:false
},null,2));
