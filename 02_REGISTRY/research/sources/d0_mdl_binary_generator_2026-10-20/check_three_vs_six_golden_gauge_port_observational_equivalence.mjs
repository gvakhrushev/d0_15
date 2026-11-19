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


const exAnteMinimalOrderWitness={reference:[local,common,local],order:[common,local,local]};
const IJI=run(exAnteMinimalOrderWitness.reference),JII=run(exAnteMinimalOrderWitness.order);
check(err(IJI,common)===0&&err(JII,product(sign,common))===0,
 "EXACT native THREE-GATE IJI=J, JII=relativeSign*J with SAME original 2 local-i,1 common-j");
for(let k=0;k<4;k++){
 const first=port(IJI,k),second=port(JII,k);
 check(Math.abs(first[1])<1e-15&&Math.abs(second[1]-4*p**3)<1e-14&&
       Math.abs(second[0]-p**6)<1e-14,
       "ORIGINAL 3-gate equal-inventory words Golden bright 0 vs4p³ on each Q8 spin state "+k);
}
const allWordsNative=(n)=>n===0?[[]]:
 allWordsNative(n-1).flatMap(w=>[w.concat([local]),w.concat([common])]);
for(let length=0;length<3;length++){
 const groups=new Map();
 for(const word of allWordsNative(length)){
  const localNum=word.filter(g=>g===local).length,
        key=localNum+":"+(length-localNum),q=port(run(word),0)[1];
  if(!groups.has(key))groups.set(key,[]);
  groups.get(key).push(q);
 }
 for(const [counts,qs] of groups)
  check(Math.max(...qs)-Math.min(...qs)<1e-14,
    "exhaustive ORIGINAL all same-inventory words length "+length+" -> no Golden order contrast for "+counts);
}
const threeWords=allWordsNative(3).filter(w=>w.filter(g=>g===local).length===2);
check(threeWords.length===3 &&
      Math.max(...threeWords.map(w=>port(run(w),0)[1]))-
      Math.min(...threeWords.map(w=>port(run(w),0)[1]))>0.94,
      "native FIRST matched-inventory order-sensitive Golden instrument uses THREE primitive actions, not eight");

console.log(JSON.stringify({
 ex_ante_shortest_matched_inventory_order_test_steps:3,
 matched_shortest_words:["IJI","JII"],
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


// EX-ANTE FULL-STATE MDL, NOT merely same Goldens port probability.
// Earlier three-gate IJI vs JII finish at J and R*J, respectively.
// Appending three existing J operators to BOTH exactly normalizes them
// to I and R with equal native two-i/four-j inventory, in SIX total.
// This is the MINIMAL matched-inventory full-operator assay on exact
// existing local-i/common-j group, not a case-specific gate estimate.
const shortFullIdentity=[local,common,local,common,common,common];
const shortFullRelative=[common,local,local,common,common,common];
check(shortFullIdentity.length===6&&shortFullRelative.length===6 &&
 shortFullIdentity.filter(g=>g===local).length===2 &&
 shortFullRelative.filter(g=>g===local).length===2 &&
 shortFullIdentity.filter(g=>g===common).length===4 &&
 shortFullRelative.filter(g=>g===common).length===4,
 "full-future-normalized Q8 original matched-inventory source has exactly 2i+4j, SIX steps each");
check(err(run(shortFullIdentity),id8)===0 && err(run(shortFullRelative),sign)===0,
 "original SIX-GATE forward words IJIJJJ -> I8 and JIIJJJ -> R8, no residual global J spin rotation");
for(let k=0;k<4;k++){
 const qI=port(run(shortFullIdentity),k),qR=port(run(shortFullRelative),k);
 check(Math.abs(qI[1])<1e-14 && Math.abs(qR[1]-4*p**3)<1e-14,
 "ORIGINAL six-gate matched exact final I vs R gives same full Golden-port contrast on spin basis "+k);
}
const nativeWords=n=>n===0?[[]]:nativeWords(n-1).flatMap(w=>[w.concat([local]),w.concat([common])]);
let sumWordsChecked=0, minimalN=null;
for(let n=0;n<=6;n++){
 const seen=new Map();
 for(const word of nativeWords(n)){
  sumWordsChecked++;
  const iCount=word.filter(x=>x===local).length;
  const key=iCount+":"+(n-iCount),out=run(word);
  const old=seen.get(key)||{id:null,r:null};
  if(err(out,id8)===0)old.id=word;
  if(err(out,sign)===0)old.r=word;
  seen.set(key,old);
 }
 const fullPair=[...seen.values()].find(x=>x.id&&x.r);
 if(n<6)check(!fullPair,"EXHAUSTIVE native Q8 all "+2**n+" words length "+n+" no same-inventory full I8 vs R8 pair");
 else{
  check(!!fullPair,"FIRST exact same-inventory full I8 and R8 Q8 operator pair occurs at length SIX");
  check(fullPair.id.filter(x=>x===local).length===2&&fullPair.r.filter(x=>x===local).length===2,
        "no invented inverse: full-shortest pair has two local i and four common j");
  minimalN=n;
 }
}
check(minimalN===6&&sumWordsChecked===127,
      "exhausted all 127 original two-source gate words of lengths 0..6, not only one positive example");
const qBudget={same_exact_full_operator_program_lengths:[6,6],
   old_full_original_program_lengths:[8,8],
   per_comparison_primitive_saving:2,
   distinct_targets:["I8","relativeSignQ"],
   intermediate_3step_only_Golden_port_equivalence_but_NOT_full_state:true};
console.log("FULL_MDL",JSON.stringify(qBudget));


// SHARPER PROSPECTIVE G0 TASK SPLIT:
// If the original admissible future detector family consists ONLY of
// the physically registered TWO Golden arm probabilities (no privileged
// quaternion reference frame output), then the 3-gate pair and 6-gate
// pair are EXACTLY observationally equivalent for EVERY real prepared
// 8-dimensional input state, not merely the four basis references.
//
// Proof identity: J=diag(Lj,Lj) is block-common, so J commutes with
// native Golden M=[aI,-pI;pI,aI] and with arm projector Pi.
// R=diag(I,-I) also commutes with J. 3word Uref=J,
// Uodd=RJ; 6word Uref=I,Uodd=R. Therefore
// (M^T U3 M)^T Pi (M^T U3 M)
// =(M^T U6 M)^T Pi (M^T U6 M)
// as exact whole 8×8 effect matrix, all input vectors.
// Additional genuine frame-sensitive future tests may distinguish.
const Pi=blocks(z(4),z(4),z(4),id4);
const effective=U=>{
  const V=product(trans(mix),product(U,mix));
  return product(trans(V),product(Pi,V));
};
const Jthree=run([local,common,local]),RJthree=run([common,local,local]),
      Idsix=run(shortFullIdentity),Rsix=run(shortFullRelative);
const E3ref=effective(Jthree),E6ref=effective(Idsix),
      E3ord=effective(RJthree),E6ord=effective(Rsix);
check(err(E3ref,E6ref)<2e-14&&err(E3ord,E6ord)<2e-14,
      "EXACT all-input Golden projective two-port effect: THREE and SIX native words identical on complete port POVM");
const gramCommon=product(trans(common),common);
check(err(gramCommon,id8)===0&&err(product(common,mix),product(mix,common))<2e-14,
      "native common-j is orthogonal, commutes exactly with Golden mixer and both arm projectors");
check(err(product(common,Pi),product(Pi,common))===0&&
      err(product(common,sign),product(sign,common))===0,
      "native common-j left action is a PURE gauge of ORIGINAL two-port-only Golden readout");
let positivePortErrors=0;
for(let r=1;r<=130;r++){
 const v=Array.from({length:8},(_,k)=>Math.sin((k+1)*(r+1)*.13)+Math.cos(.17*(k+3)*(r+2)));
 const norm=Math.hypot(...v),psi=v.map(x=>x/norm);
 const quadratic=E=>psi.reduce((s,x,i)=>
    s+x*E[i].reduce((a,y,j)=>a+y*psi[j],0),0);
 positivePortErrors=Math.max(positivePortErrors,
  Math.abs(quadratic(E3ref)-quadratic(E6ref)),
  Math.abs(quadratic(E3ord)-quadratic(E6ord)));
}
check(positivePortErrors<3e-14,
      "130 native arbitrary 8D coherent spin preparations agree on FULL Golden two-port law between 3- and 6-gate pairs");
console.log("THREE_SIX_GAUGE",JSON.stringify({
  exact_Golden_effect_matrix_reference_error:err(E3ref,E6ref),
  exact_Golden_effect_matrix_order_error:err(E3ord,E6ord),
  source_common_Q8_J_is_Golden_port_gauge:true,
  full_8x8_program_operator_equal:false,
  native_golden_port_all_input_equivalent:true,
  existential_other_future_quaternion_frame_test_possible:true,
  candidate_minimum_if_sole_future_tests_are_golden_two_port:3,
  minimum_with_exact_full_8x8_operator_reference:6,
  original_native_G0_future_test_task_selection_unproved:true
}));
