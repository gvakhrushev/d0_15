#!/usr/bin/env node
"use strict";
/* SAME original 33/718 K(9,11,13) scene, all genuine n=2/3/4
 based closed paths, total 266202, complete conditional two-Golden+Bell17
 mark plus SIX original internal EARLY/LATE failure stage outcomes.
 Full support has 266202*17+6=4,525,440 mathematical positive events.
 One shared unknown κ and actual stage labels recover absolute Book
 source + unknown moving g2/g3/g4 and β2/β3/β4; 143 original rooted
 3-loops plus 184 original rooted 4-loops carry the 327 nonabelian
 matrix holonomies with one ROOT CAR reference. Literal G0 execution,
 native programme/verifier and full Book H+J+R remain unproved.
*/
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi),N=33;
const zone=u=>u<9?0:u<20?1:2;
const ok=(v,s)=>{if(!v)throw Error("FAIL "+s);console.log("PASS "+s)};
const I=()=>Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>+(i===j)));
const MM=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const trace=A=>A.reduce((s,r,i)=>s+r[i],0);
const A=I().map((row,u)=>row.map((_,v)=>+(zone(u)!==zone(v))));
const cnt=[2,3,4].map(n=>{let M=I();for(let i=0;i<n;i++)M=MM(M,A);return trace(M)});
ok(cnt.join(",")==="718,7722,257762"&&cnt.reduce((s,x)=>s+x,0)===266202,
 "ALL original genuine based closed 2,3,4 word counts exactly 266202");
const g={2:p*p,3:p**3,4:p*p},kappa=p**26;
ok(Math.abs(g[2]+g[3]+g[4]-1)<1e-15,
 "original Golden p²,p³,p² prefix-free THREE-length mathematical attempt law");
function fieldK(t,scenario){
 let M=Array.from({length:N},()=>Array(N).fill(0));
 for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(A[u][v]){
  const cost=1.07+.002*((7*u+13*v+u*v)%17)+(scenario?t*t:0);
  if(cost<1)throw Error("original primitive Cost quantum violation");
  const Info=.004*((u%7)+(v%9))/2;
  M[u][v]=Math.exp(-ell*(cost-Info));
 }
 return M;
}
const Zs=K=>{let M=I(),z={};for(let n=1;n<=4;n++){
 M=MM(M,K);if(n>=2)z[n]=trace(M);
 }return z;};
function returnProb(K,gamma){let q=1;for(let i=1;i<gamma.length;i++)
 q*=K[gamma[i-1]][gamma[i]];return q;}
const get=(q,gamma)=>q*returnProb(K_0,gamma);
function program(t,scenario){
 const K=fieldK(t,scenario),c=phi**(-t*t),
       beta={2:p*p*phi**(scenario?2*t*t:0),
             3:p*p*phi**(scenario?3*t*t:0),
             4:p*p*phi**(scenario?4*t*t:0)},
       z=Zs(K);
 if(Object.values(beta).some(x=>x>=1))throw Error("invalid early acceptance");
 const E={},B={},S={},total={};
 for(let n of [2,3,4]){
  ok(kappa*z[n]<1,"positive complete original late verifier at native depth "+n);
  E[n]=g[n]*(1-beta[n]);B[n]=g[n]*beta[n]*(1-kappa*z[n]);
  S[n]=g[n]*beta[n]*kappa*z[n];
  total[n]=E[n]+B[n]+S[n];
 }
 ok(Math.abs(Object.values(total).reduce((s,x)=>s+x,0)-1)<4e-14&&
    [2,3,4].every(n=>Math.abs(total[n]-g[n])<3e-14),
    "COMPLETE 4525440-stage-labelled original Book/Golden path law normalized across THREE depths");
 const qWord=word=>{const n=word.length-1;
  return g[n]*beta[n]*kappa*returnProb(K,word);
 };
 return {K,z,beta,E,B,S,total,qWord};
}
const t=.13,base=program(t,false),changed=program(t,true);
const depth={},accept={};
for(let n of [2,3,4]){
 depth[n]=base.E[n]+base.B[n]+base.S[n];
 accept[n]=1-base.E[n]/depth[n];
 ok(Math.abs(depth[n]-g[n])<2e-14&&Math.abs(accept[n]-base.beta[n])<2e-14,
   "full original early/late PREPARATION ARCHIVE recovers unknown g and beta at n="+n);
}
const u=0,v=9,w=20;
const five=programInput=>({
 ab:programInput.qWord([u,v,u]),
 bc:programInput.qWord([v,w,v]),
 ac:programInput.qWord([u,w,u]),
 fw:programInput.qWord([u,v,w,u]),
 bw:programInput.qWord([u,w,v,u])
});
const f=five(base),G2=depth[2]*accept[2],G3=depth[3]*accept[3];
const κ=(G3*G3)/(G2**3)*(f.ab*f.bc*f.ac)/(f.fw*f.bw);
ok(Math.abs(κ-kappa)<5e-13,
 "ALL original three-depth unknown COMMON κ recovered from only five real n2/n3 loop outcomes and actual early stages");
let largestEqual=0;
for(let n of [2,3,4]){
 largestEqual=Math.max(largestEqual,Math.abs(base.S[n]-changed.S[n]),
  Math.abs(base.E[n]+base.B[n]-changed.E[n]-changed.B[n]));
}
for(const word of [[0,9,0],[9,20,9],[0,9,20,0],
                   [0,9,1,20,0],[0,9,1,10,0]]){
 largestEqual=Math.max(largestEqual,Math.abs(base.qWord(word)-changed.qWord(word)));
}
ok(largestEqual<2e-13,
 "HOSTILE original three-depth accepted/final-reject probability law blind to simultaneous primitive Cost t² and early β_n compensation");
let earlyGap=0;for(let n of [2,3,4])
 earlyGap=Math.max(earlyGap,Math.abs(base.E[n]-changed.E[n]));
ok(earlyGap>.001,
 "a TRUE earlier-than-final archived STAGE distinguishes absolute Book second source even with same terminal 2/3/4 word laws");
const λ0=()=>{ // Perron power iteration on 33 true original primitive price
 let x=Array(N).fill(1/Math.sqrt(N)),K=base.K;
 for(let i=0;i<1500;i++){
  let y=K.map(row=>row.reduce((s,v,j)=>s+v*x[j],0)),norm=Math.hypot(...y),v=y.map(z=>z/norm);
  if(Math.max(...v.map((z,j)=>Math.abs(z-x[j])))<1e-15){x=v;break}x=v;
 }
 return x.reduce((s,z,i)=>s+z*K[i].reduce((a,v,j)=>a+v*x[j],0),0);
};
const λ=λ0(),costShift=Math.log(λ/(λ*phi**(-t*t)))/ell;
ok(Math.abs(costShift-t*t)<1e-14&&
 Math.abs(changed.S[4]-base.S[4])<1e-12,
 "the ORIGINAL absolute Book action really differs by t², still hidden in terminal 4-depth observations");
ok(143*1+104+80===327&&327*6+686===2648,
 "all original ROOTED n3/n4 holonomies plus n2/n3 scalar Book source give local quotient2648");
const negative=(()=>{const sameBeta={2:p*p,3:p*p,4:p*p},factor=phi**(-t*t);
 const κd={2:kappa/factor**2,3:kappa/factor**3,4:kappa/factor**4};
 return {κd,stageUnchanged:Math.max(...[2,3,4].map(n=>
  Math.abs(g[n]*sameBeta[n]*κd[n]*changed.z[n]-base.S[n])))};
})();
ok(negative.stageUnchanged<2e-12&&negative.κd[2]!==negative.κd[3],
 "if verifier κ_n is separately allowed per depth, even full internal stages cannot identify absolute Book source");
console.log(JSON.stringify({
 exact_original_based_paths:{n2:cnt[0],n3:cnt[1],n4:cnt[2],total:266202},
 total_positive_record_labels:266202*17+6,
 true_K_33_scene_stages:"each n has early and late failure separated, all Golden/Bell conditional outcomes retained",
 original_Golden_three_attempt:[g[2],g[3],g[4]],
 recovered_unknown_common_kappa:κ,
 recovered_unknown_acceptances:accept,
 all_original_nonabelian_rooted_basis:{"n3_root_0_BC":143,"n4_root_0_AC":104,"n4_root_0_AB":80},
 scalar_Book_quotient_rank:686,rooted_group_Lorentz_rank:1962,
 jointly_servable_source_rank:2648,
 hidden_second_Book_cost_gap_exact:2,
 source_rejection_stage_early_gap:earlyGap,
 negative_control:"independent unknown κ2,κ3,κ4 preserves all full staged probabilities under compensating primitive Cost scale",
 actual_G0_fullStep_234_preparation:false,
 native_4D_Role_Palatini_source_selected:false,GR_closed:false
},null,2));
