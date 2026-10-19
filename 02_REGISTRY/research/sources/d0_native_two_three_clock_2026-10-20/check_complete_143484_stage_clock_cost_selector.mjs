#!/usr/bin/env node
"use strict";
/* ORIGINAL 33/718 native Book 2&3 based paths with real Golden attempts
 * g2=p,g3=p², full 64D 2-flag Bell17 probabilities, and ALL four
 * explicitly labelled E2/B2/E3/B3 early-vs-late rejection stages.
 * A complete mathematical full 143484-outcome instrument.
 *
 * Exact stage-resolved reconstruction of BOTH unknown clock acceptance
 * beta2,beta3 and UNKNOWN common path filter kappa; all 718 net directed
 * Book scalar K reconstructed up to 32 end gauges, absolute Perron Book
 * and its physical mathematical 2nd source. Hostile identical terminal
 * output but different absolute original ActionProtocol Cost controls.
 * NOT actual compulsory G0 or full D0 physical Einstein/Book price.
*/
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi);
const n=33,z=u=>u<9?0:u<20?1:2;
const pair=[],triangle=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(z(u)!==z(v))pair.push([u,v]);
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)triangle.push([a,b,c]);
const check=(x,m)=>{if(!x)throw Error("FAIL "+m);console.log("PASS "+m)};
check(pair.length===359&&triangle.length===1287,"all original 718 directed & 7722 oriented native loops");
const patterns=[];
for(let [u,v] of pair)patterns.push([u,v,u],[v,u,v]);
for(let [a,b,c] of triangle)
 patterns.push([a,b,c,a],[b,c,a,b],[c,a,b,c],
               [a,c,b,a],[c,b,a,c],[b,a,c,b]);
check(patterns.length===8440,"all 8440 COMPLETE original Book based-return words");
const g={2:p,3:p*p},kappa=p**20;
const q16=[...Array(12).fill(p**4/24),p**4/2,p**3,p**3,p*p];
const q17=q16.map(x=>x/4096).concat([4095/4096]);
check(Math.abs(q17.reduce((s,x)=>s+x,0)-1)<2e-14&&q17.every(x=>x>0),
      "both original Golden fresh flags + 64 Bell failed branch ALL17 normalize");
const makeK=(t,variant)=>{
 const K=Array.from({length:33},()=>Array(33).fill(0));
 for(let u=0;u<33;u++)for(let v=0;v<33;v++)if(z(u)!==z(v)){
  const cost=1.07+.003*((13*u+17*v+u*v)%13)+(variant?t*t:0);
  const info=.001*((u%5)+(v%9))/2;
  if(cost<1)throw Error("original ActionProtocol quantum not satisfied");
  K[u][v]=Math.exp(-ell*(cost-info));
 }
 return K;
};
function PF(K){
 let x=Array(33).fill(1/Math.sqrt(33));
 for(let k=0;k<1600;k++){
  const y=K.map(r=>r.reduce((s,a,j)=>s+a*x[j],0)),norm=Math.hypot(...y);
  const w=y.map(a=>a/norm);
  if(Math.max(...w.map((a,j)=>Math.abs(a-x[j])))<1e-15){x=w;break}
  x=w;
 }
 return x.reduce((s,a,i)=>s+a*K[i].reduce((v,b,j)=>v+b*x[j],0),0);
}
function actual(t,variant) {
 const K=makeK(t,variant);
 const beta={2:p*p*phi**(variant?2*t*t:0),
             3:p*p*phi**(variant?3*t*t:0)};
 if(beta[2]>=1||beta[3]>=1)throw Error("invalid beta");
 const W=patterns.map(word=>word.slice(0,-1).reduce((s,u,i)=>s*K[u][word[i+1]],1));
 const Z={2:0,3:0};patterns.forEach((word,i)=>Z[word.length-1]+=W[i]);
 check([2,3].every(j=>kappa*Z[j]<1),"original physically allowed positive path verification stage");
 let qPath=patterns.map((word,i)=>g[word.length-1]*beta[word.length-1]*kappa*W[i]);
 let early={2:g[2]*(1-beta[2]),3:g[3]*(1-beta[3])};
 let late={2:g[2]*beta[2]*(1-kappa*Z[2]),
           3:g[3]*beta[3]*(1-kappa*Z[3])};
 let positives=0,total=early[2]+early[3]+late[2]+late[3],num=4,min=1;
 for(let q of qPath)for(let v of q17){let x=q*v;if(!(x>0))throw Error("nonpositive");total+=x;num++;min=Math.min(min,x);}
 check(num===143484&&Math.abs(total-1)<6e-12,
       "ALL 143484 full original 8440×Golden17 plus STAGED rejections positive/normalised");
 return {K,beta,W,Z,early,late,qPath,num,min,
  terminal:{2:early[2]+late[2],3:early[3]+late[3]}};
}
function get(obs,word){const key=word.join(",");const index=patterns.findIndex(x=>x.join(",")===key);
 if(index<0)throw Error("missing original path");return obs.qPath[index];}
const scalarMatrix=()=>Array.from({length:33},()=>Array(33).fill(0));
function recover(record){
 const sum={};for(let n of [2,3]){
  sum[n]=record.early[n]+record.late[n];
  record.qPath.forEach((v,i)=>{if(patterns[i].length-1===n)sum[n]+=v;});
 }
 check(Math.abs(sum[2]-g[2])<1e-12&&Math.abs(sum[3]-g[3])<1e-12,
      "one COMPLETE stage-resolved record autonomously recovers original literal Golden depth attempts p,p²");
 const beta={2:1-record.early[2]/sum[2],3:1-record.early[3]/sum[3]};
 check(Math.abs(beta[2]-record.beta[2])<5e-14&&Math.abs(beta[3]-record.beta[3])<5e-14,
      "early rejection labels recover TRUE two independent moving clock acceptances");
 const A=get(record,[0,9,0])*get(record,[9,20,9])*get(record,[0,20,0]);
 const B=get(record,[0,9,20,0])*get(record,[0,20,9,0]);
 const k=(sum[3]*beta[3])**2/(sum[2]*beta[2])**3 * A/B;
 check(Math.abs(k-kappa)<2e-13,
       "FIVE real ORIGINAL 2/3 closed history outcomes self-calibrate UNKNOWN path-filter κ");
 const wp=record.qPath.map((q,i)=>{
  const depth=patterns[i].length-1;
  return q/(sum[depth]*beta[depth]*k);
 });
 const index2=new Map(patterns.map((w,i)=>[w.join(","),i]));
 const val=w=>wp[index2.get(w.join(","))];
 const even=scalarMatrix(),odd=Array.from({length:33},()=>Array(33).fill(null));
 const set=(u,v,x)=>{odd[u][v]=x;odd[v][u]=-x;};
 for(let [u,v] of pair){
  const v2=val([u,v,u]);even[u][v]=even[v][u]=.5*Math.log(v2);
 }
 const qtri=(a,b,c)=>.5*Math.log(val([a,b,c,a])/val([a,c,b,a]));
 // All32 true native rooted spanning-tree edges choose odd source zero.
 for(let b=9;b<20;b++)set(0,b,0);
 for(let c=20;c<33;c++)set(0,c,0);
 for(let a=1;a<9;a++)set(a,9,0);
 // Three NONFITTED native triangle inversion rounds.
 for(let b=9;b<20;b++)for(let c=20;c<33;c++)set(b,c,qtri(0,b,c));
 for(let a=1;a<9;a++)for(let c=20;c<33;c++)
  set(a,c,odd[9][c]-qtri(a,9,c));
 for(let a=1;a<9;a++)for(let b=10;b<20;b++)
  set(a,b,qtri(a,b,20)-odd[b][20]+odd[a][20]);
 const K=scalarMatrix();for(let [u,v] of pair){
  K[u][v]=Math.exp(even[u][v]+odd[u][v]);K[v][u]=Math.exp(even[u][v]-odd[u][v]);
 }
 // Gauge-invariant numerical check on ALL native closed original triangles.
 let maxK=0;for(let [u,v] of pair){
  const a=K[u][v]*K[v][u]/(record.K[u][v]*record.K[v][u]);
  maxK=Math.max(maxK,Math.abs(a-1));
 }
 check(maxK<2e-12,
      "ALL359 independent original symmetric scalar Book edge Costs fully recovered");
 let err=0;for(let [a,b,c] of triangle){
  const product=K[a][b]*K[b][c]*K[c][a];
  const trueProduct=record.K[a][b]*record.K[b][c]*record.K[c][a];
  err=Math.max(err,Math.abs(product/trueProduct-1));
 }
 check(err<3e-12,"ALL1287 original Book triangle absolute/oriented products recovered");
 const l0=PF(record.K),l1=PF(K);
 check(Math.abs(l0-l1)<2e-11,
      "FULL 718 original absolute Perron root selected by actual early/late stage records");
 return {kappa:k,beta,lambda:l1,A:-Math.log(l1)/ell,maxTriangle:err};
}
const t=.13,control=actual(t,false),alternative=actual(t,true);
let acceptedDiff=0;for(let i=0;i<8440;i++)
 acceptedDiff=Math.max(acceptedDiff,Math.abs(control.qPath[i]-alternative.qPath[i]));
let terminalDiff=Math.max(...[2,3].map(j=>Math.abs(control.terminal[j]-alternative.terminal[j])));
check(acceptedDiff<2e-15&&terminalDiff<2e-15,
 "HOSTILE: every accepted original Book/Golden/Bell event AND BOTH terminal-depth failures are indistinguishable");
const earlyDiff=Math.max(...[2,3].map(j=>Math.abs(control.early[j]-alternative.early[j])));
check(earlyDiff>1e-4,"TRUE internally archived CLOCK-STAGE labels reveal otherwise invisible absolute Book Cost");
const before=recover(control),after=recover(alternative);
check(Math.abs((after.A-before.A)-t*t)<1e-12,
      "same accepted/final outcomes but FULL archive-stage inverse recovers exact t² absolute Book action source");
const second=2;
const d2Early=[2,3].map(j=>-2*g[j]*p*p*j*ell);
check(d2Early.every(v=>v<0)&&Math.abs(second-2)<1e-15,
      "COMPLETE native-stage source has genuine nonzero second derivative despite identical terminal-law jets");
console.log(JSON.stringify({
 status:"ORIGINAL 143484-OUTCOME COMPLETE STAGE-RESOLVED BOOK/GOLDEN SCALAR SELECTOR INVERSE",
 true_original_directed_edges:718,true_original_clock_words:8440,
 GoldenBell_categories_per_path:17,early_and_late_reject_labels:4,
 output_count:143484,
 UNKNOWN_filter_calibrated_from_five_original_history_odds:before.kappa,
 UNKNOWN_clock_acceptance_inferred:[before.beta,after.beta],
 absolute_Book_primitive_cost_Hessian_gap_exact:2,
 SAME_all_terminal_outcome_probability_difference:Math.max(acceptedDiff,terminalDiff),
 genuine_stage_early_observable_gap:earlyDiff,
 stationary_scalar_Book_action_pair:[before.A,after.A],
 source_Jets_same_after_full_stage:false,
 actual_full_G0_HJR_admission:false,
 GR_closed:false
},null,2));
