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
console.log(JSON.stringify({
 full_original_Q8_source:"OrderMemoryControl.localIQ/commonJQ",
 primitive_counts_each:{local_i:4,common_j:4},
 positive_port_order:4*p**3,negative_port_identity:0,
 existing_full_internal_clock:16,
 existing_15_operation_programmed_512d_record:"FiniteProtocolClock / order_memory_control_verify.py",
 unproved:"actual scene Q8 memory selects one source programme and pays full M1/G0 Book clock and work",
 GR_closed:false
},null,2));
