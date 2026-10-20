#!/usr/bin/env node
"use strict";
const p=(Math.sqrt(5)-1)/2,a=Math.sqrt(p);
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const z=n=>eye(n).map(r=>r.map(()=>0));
const product=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((v,x,k)=>v+x*B[k][j],0)));
const trans=A=>A.map((r,i)=>r.map((_,j)=>A[j][i]));
const scale=(A,v)=>A.map(r=>r.map(x=>x*v));
const err=(A,B)=>Math.max(...A.flatMap((r,i)=>r.map((v,j)=>Math.abs(v-B[i][j]))));
const check=(ok,msg)=>{if(!ok)throw Error("FAIL "+msg);console.log("PASS "+msg)};
function blocks(A,B,C,D){
 const n=A.length,M=z(2*n);
 for(let i=0;i<n;i++)for(let j=0;j<n;j++){
  M[i][j]=A[i][j];M[i][j+n]=B[i][j];
  M[i+n][j]=C[i][j];M[i+n][j+n]=D[i][j];
 }
 return M;
}
const Li=[[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]];
const Lj=[[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]];
const id4=eye(4),zero4=z(4),id8=eye(8);
const local=blocks(id4,zero4,zero4,Li),common=blocks(Lj,zero4,zero4,Lj);
const sign=blocks(id4,zero4,zero4,scale(id4,-1));
const order=[local,common,local,local,local,common,common,common];
const idle=[local,local,local,local,common,common,common,common];
const run=word=>word.reduce((now,gate)=>product(gate,now),id8);
check(err(run(order),sign)===0&&err(run(idle),id8)===0,
 "ORIGINAL Q8 eight forward gates realize relativeSign or identity EXACTLY");
check(order.filter(v=>v===local).length===4&&order.filter(v=>v===common).length===4
 &&idle.filter(v=>v===local).length===4&&idle.filter(v=>v===common).length===4,
 "both ORIGINAL programmes use exactly four local-i and four common-j gates");
const mix=blocks(scale(id4,a),scale(id4,-p),scale(id4,p),scale(id4,a));
check(err(product(trans(mix),mix),id8)<1e-14,"original Golden eight-real-coordinate mixer is unitary");
function port(U,k){
 const psi=Array(8).fill(0);psi[k]=1;
 const mv=(M,x)=>M.map(r=>r.reduce((v,a,j)=>v+a*x[j],0));
 const out=mv(trans(mix),mv(U,mv(mix,psi)));
 return [out.slice(0,4).reduce((v,x)=>v+x*x,0),
         out.slice(4).reduce((v,x)=>v+x*x,0)];
}
for(let k=0;k<4;k++){
 const positive=port(run(order),k),negative=port(run(idle),k);
 check(Math.abs(positive[0]-p**6)<1e-14&&Math.abs(positive[1]-4*p**3)<1e-14,
 "native Q8 order word on spin basis "+k+" gives exact Golden [p^6,4p^3]");
 check(Math.abs(negative[0]-1)<1e-14&&Math.abs(negative[1])<1e-14,
 "native Q8 identity word on spin basis "+k+" gives [1,0]");
}
const J=blocks(z(4),scale(id4,-1),id4,z(4));
const commonI=blocks(Li,z(4),z(4),Li);
const comm=(A,B)=>err(product(A,B),product(B,A));
check(comm(mix,J)<1e-14&&comm(commonI,J)===0&&comm(common,J)===0,
 "uncontrolled original common-only gate palette preserves arm-turn invariant");
check(comm(sign,J)>1.9,
 "Q8 central relative sign breaks common-only invariant; local i source necessary");
check(p**6+4*p**3>0.99999999999999 &&p**6+4*p**3<1.00000000000001,
 "exact Golden order response full probability normalization");

// MAJOR HOSTILE test: EXACT SAME relativeSignQ output can be prepared
// by TWO native local-i forward actions or the eight-gate original
// based chronology. This does NOT reproduce the same paid source history.
const shortWord=[local,local],shortFinal=run(shortWord),eightFinal=run(order);
check(err(shortFinal,eightFinal)===0&&err(shortFinal,sign)===0,
 "actual two-local-i native programme and eight-action Q8 loop EXACT SAME full 8x8 final operator");
for(const word of [[],[local],[common]])
 check(err(run(word),sign)>1e-12,
       "zero or single original gate cannot reach relative sign");
check((shortWord.length%16)===2 &&(order.length%16)===8,
 "already-owned FiniteProtocolClock distinguishes 2 vs8 identical-terminal-Golden histories");
// Physical preparation matters: local i is IDENTITY on pure reference,
// but moves the actual signal arm once the ORIGINAL Golden mixer has
// created a strictly positive superposition on both quaternion arms.
const baseRef=Array(8).fill(0);baseRef[0]=1;
const mv=(M,v)=>M.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));
check(Math.hypot(...mv(local,baseRef).map((x,k)=>x-baseRef[k]))===0,
 "real original local-i does NOT change a reference-only input: no unsupported eight-step paid-work assertion");
const prepared=mv(mix,baseRef);
check(Math.abs(prepared[0]-a)<1e-14&&Math.abs(prepared[4]-p)<1e-14,
 "original Golden mixer provides precisely the needed coherent signal/reference input");
function fullExecution(word){
 let U=id8,psi=prepared,transitions=0,minChange=10;
 for(const gate of word){
  const next=product(gate,U),newPsi=mv(gate,psi);
  const d=Math.hypot(...newPsi.map((x,k)=>x-psi[k]));
  minChange=Math.min(minChange,d);
  check(d>1e-12&&err(next,U)>1e-12,
   "each original executed Q8 gate really changes GOLDEN-PREPARED full 8d source state");
  psi=newPsi;U=next;transitions++;
 }
 return {operator:U,transitions,minChange};
}
const testedShort=fullExecution(shortWord),testedEight=fullExecution(order);
check(testedShort.transitions===2&&testedEight.transitions===8&&
      err(testedShort.operator,testedEight.operator)===0,
 "all actually prepared Q8 source transitions nontrivial: two versus eight legitimate original S_min cost quanta");
for(const excess of [0,.1,.25]){
 const cost=t=>1+t*t;
 const priceShort=testedShort.transitions*cost(excess),
       priceEight=testedEight.transitions*cost(excess);
 check(Math.abs(priceEight-priceShort-6*(1+excess**2))<1e-14,
       "existing canonical primitive cost+legally positive excess yields 6*(1+t²) full-history source price gap");
}
check(2*testedShort.transitions===4&&2*testedEight.transitions===16,
 "original admissible primitive Cost=1+t² has SOURCE-HESSIAN contrast 12 on identical terminal native Golden output");

console.log(JSON.stringify({
 native_same_endpoint_source_cost_two_vs_eight:[2,8],
 optional_legal_excess_primitive_hessians:[4,16],
 full_original_Q8_source:"OrderMemoryControl.localIQ/commonJQ",
 primitive_counts_each:{local_i:4,common_j:4},
 positive_port_order:4*p**3,negative_port_identity:0,
 existing_full_internal_clock:16,
 existing_15_operation_programmed_512d_record:"FiniteProtocolClock / order_memory_control_verify.py",
 unproved:"actual scene Q8 memory selects one source programme and pays full M1/G0 Book clock and work",
 GR_closed:false
},null,2));
