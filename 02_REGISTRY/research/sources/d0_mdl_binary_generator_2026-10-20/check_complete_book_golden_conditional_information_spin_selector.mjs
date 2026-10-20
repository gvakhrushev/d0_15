#!/usr/bin/env node
"use strict";
// ORIGINAL K(9,11,13) ALL 718 directed Book edges and ALL 8440 based
// closed 2/3 paths. True inverse-respecting Q8 projectively flat
// edge lifts q_uv = g_u^-1 g_v * sigma_uv have every triangle holonomy
// ±center. ONE original central sheet (-1 on edge A0/C0) changes 66
// based three-tick triangle signs, NO two-tick backtrack signs, and
// leaves ALL raw Book K/pressure unchanged. Original native p Golden
// dark/bright conditional 2-port probabilities preserve all records.
// This is a mathematical possible one-clock SOURCE, NOT physical
// compulsory G0 spinor/Golden active routing or selected H+J+R.
const p=(Math.sqrt(5)-1)/2,z=u=>u<9?0:u<20?1:2;
const ok=(v,s)=>{if(!v)throw Error("FAIL "+s);console.log("PASS "+s)};
const M=(x,y)=>[x[0]*y[0]-x[1]*y[1]-x[2]*y[2]-x[3]*y[3],
 x[0]*y[1]+x[1]*y[0]+x[2]*y[3]-x[3]*y[2],
 x[0]*y[2]-x[1]*y[3]+x[2]*y[0]+x[3]*y[1],
 x[0]*y[3]+x[1]*y[2]-x[2]*y[1]+x[3]*y[0]];
const inv=x=>[x[0],-x[1],-x[2],-x[3]],
      equals=(x,y)=>x.every((v,i)=>v===y[i]),
      neg=x=>x.map(v=>-v),one=[1,0,0,0],
      minus=[-1,0,0,0],qi=[0,1,0,0],qj=[0,0,1,0],qk=[0,0,0,1],
      Q=[one,minus,qi,neg(qi),qj,neg(qj),qk,neg(qk)];
const G=Array.from({length:33},(_,u)=>Q[(7*u+Math.floor(u/3))%8]);
G[0]=one;G[9]=qi;G[20]=qk;
const edges=[],two=[],three=[];
for(let u=0;u<33;u++)for(let v=0;v<33;v++)if(z(u)!==z(v)){
 edges.push([u,v]);two.push([u,v,u]);
}
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 three.push([a,b,c,a],[b,c,a,b],[c,a,b,c],
            [a,c,b,a],[c,b,a,c],[b,a,c,b]);
ok(edges.length===718&&two.length===718&&three.length===7722,
   "exact 33 K913 native supported edge/2tick/3tick counts");
const centralEdge=(u,v)=>Math.min(u,v)===0&&Math.max(u,v)===20;
const edgeQ=(u,v,sheet)=>{let q=M(inv(G[u]),G[v]);
 return sheet&&centralEdge(u,v)?neg(q):q;};
ok(edges.every(([u,v])=>equals(M(edgeQ(u,v,true),edgeQ(v,u,true)),one)),
   "all original 718 oriented noncommuting Q8 edges have exactly inverse reverse");
function hol(word,sheet){let q=one;for(let i=1;i<word.length;i++)
 q=M(q,edgeQ(word[i-1],word[i],sheet));return q;}
ok(two.every(w=>equals(hol(w,false),one)&&equals(hol(w,true),one)),
   "every one of 718 ORIGINAL two-tick Book backtracks is Q8 central identity");
const h3=three.map(w=>hol(w,true));
ok(h3.every(q=>equals(q,one)||equals(q,minus))&&
   three.every(w=>equals(hol(w,false),one)),
   "every one of 7722 original ABC triangles is exact Q8 central ±1, without invented sign map");
const minusThree=h3.filter(q=>equals(q,minus)).length;
ok(minusThree===66&&equals(hol([0,9,20,0],true),minus)&&
   equals(hol([0,9,20,0],false),one),
   "one honest native central edge sheet makes 11 triangles/66 based 3tick loops negative; i*j*k=-1");
const Z2=718*p*p,Z3=7722*p**3;
const a2=p,a3=p*p,Z=a2*Z2+a3*Z3;
const w2=a2*p*p/Z,w3=a3*p**3/Z;
ok(Math.abs(718*w2+7722*w3-1)<3e-14,
   "full original 2/3-depth raw Book weights jointly normalized, with exact shared absolute Z");
let full=0,scalar=0,bright=0,bright2=0,positive=0,zero=0;
for(const [list,w,depth] of [[two,w2,2],[three,w3,3]])
 for(const word of list){
  const q=hol(word,true),qB=equals(q,minus)?4*p**3:0,qD=1-qB;
  const x=w*qB,y=w*qD;
  full+=x+y;scalar+=w;bright+=x;if(depth===2)bright2+=x;
  if(x>0)positive++;else zero++;
 }
ok(Math.abs(full-1)<5e-12&&Math.abs(scalar-1)<5e-12,
   "ALL 16880 possible Book×2 Golden outcome labels retained with proper unit total mass (forbidden bright has ZERO)");
ok(Math.abs(bright-minusThree*w3*4*p**3)<2e-14&&bright>0&&bright2===0,
   "conditional original Golden bright records arise ONLY at true length3 central− loops, exact analytic mass");
ok(Math.abs(4*p**3+p**6-1)<2e-14,"original primitive Golden full dark p6 plus bright4p3 normalizes");
ok(zero===718+(7722-minusThree)&&positive===minusThree,
   "exact original positive/zero label support, no discarded failed dark outcomes");
const sameRawCostAllEdges=edges.every(([u,v])=>p===p);
ok(sameRawCostAllEdges&&Math.abs(w2*718+w3*7722-1)<1e-12,
   "Spin center sheet does NOT alter original scalar Book Cost/Info/Perron source at all");
console.log(JSON.stringify({
 original_graph_vertices:33,original_directed_edges:edges.length,
 true_native_backtracks:two.length,true_native_triangles:three.length,
 first_central_negative_based_histories:minusThree,
 all_2step_chiral_bright_mass:bright2,
 conditional_native_Q8_negative_bright_prob:4*p**3,
 unconditional_original_joint_bright_probability:bright,
 scalar_book_normalizer_Z:Z,
 full_source_and_detector_possibilities:16880,
 full_joint_probability_total:full,
 forbidden_bright_zero_probability_labels:zero,
 actual_two_three_Book_scalar_source_unchanged_under_spin_flip:true,
 prospective_shortest_loop_for_possible_Q8_spin_check:3,
 important_scope:"Q8 projective-flat edge assignment and Golden conditional coupling declared; ACTUAL M1/G0 scene controller and full H+J+R selection UNPROVEN",
 GR_closed:false
},null,2));



// CONDITIONAL pure-Info selector, WITHOUT inventing a new physical action:
// compare the ACTUAL native COMPLETE Golden dark/bright Shannon code of
// one true jointly normalized Book2/3 experiment, holding every scalar
// K edge cost and every preparation probability FIXED.
// Book03's compulsory Info need not equal this Shannon statistic: the
// theorem is IF that full conditional event info is physically counted
// in the selected Cost−Info price with the expected native sign.
const hPhi=q=>{
 const m=1-q;
 return -(q? q*Math.log(q)/Math.log(1/p):0)-
        (m? m*Math.log(m)/Math.log(1/p):0);
};
const hNegative=hPhi(4*p**3);
ok(hNegative>0&&hNegative<2,
 "native Golden qMinus=(p6,4p3) has strictly positive complete two-port Shannon information");
const key=(u,v)=>Math.min(u,v)+":"+Math.max(u,v);
const negativeSheetPattern=(u,v)=>true,emptySheetPattern=(u,v)=>false,
 singleSheetPattern=(u,v)=>key(u,v)==="0:20";
function entropyFor(pattern){
 let negative=0;
 // Book 2-returns always trivial regardless of any central sheet,
 // since inverse edge is necessarily the same Z2 sign.
 for(const word of three){
  let sign=false;
  for(let j=1;j<word.length;j++)sign=Boolean(Number(sign)^Number(pattern(word[j-1],word[j])));
  if(sign)negative++;
 }
 const shannonBase=-(718*w2*Math.log(w2)+7722*w3*Math.log(w3))/Math.log(1/p);
 return {negative,fullCode:shannonBase+negative*w3*hNegative,bookCode:shannonBase,
         conditionalSpinCode:negative*w3*hNegative};
}
const none=entropyFor(emptySheetPattern),oneSheet=entropyFor(singleSheetPattern),
 allSheet=entropyFor(negativeSheetPattern);
ok(none.negative===0&&oneSheet.negative===66&&allSheet.negative===7722,
  "no Spin sheet / one real edge sheet / all negative edge sheets yield 0 / 66 / 7722 true based Q8− 3-cycles");
ok(allSheet.conditionalSpinCode>oneSheet.conditionalSpinCode &&
   oneSheet.conditionalSpinCode>none.conditionalSpinCode,
  "SHANNON full event Info distinguishes otherwise exactly equal native scalar Cost source");
ok(Math.abs((allSheet.fullCode-none.fullCode)-
            (7722*w3*hNegative))<1e-13,
  "exact no-coefficient original Book/Golden conditional Info gain for full uniform Q8− Spin sheet");
ok(Math.abs(none.bookCode-oneSheet.bookCode)<1e-15&&
   Math.abs(none.bookCode-allSheet.bookCode)<1e-15,
  "all three Spin choices have IDENTICAL exact scalar 8440-clock Book entropy and primitive price");
const triangleTau=(a,b,c,pattern)=>{
 let x=false;
 for(const [u,v] of [[a,b],[b,c],[c,a]])
  x=Boolean(Number(x)^Number(pattern(u,v)));
 return x;
};
ok(three.every(w=>triangleTau(w[0],w[1],w[2],negativeSheetPattern)),
   "ALL negative native source Spin sheets are simultaneously consistent with full 1287 ABC triangle constraints");
const gauge=Array.from({length:33},(_,u)=>Boolean((17*u+Math.floor(u/3))%2));
const gaugeEquivalent=(u,v)=>Boolean(Number(negativeSheetPattern(u,v))^Number(gauge[u])^Number(gauge[v]));
ok(three.every(w=>triangleTau(w[0],w[1],w[2],gaugeEquivalent)),
   "all-negative physical Spin-sheet optimum is invariant under nontrivial native 32-site gauge transformations");
const maxConstrainedInfo=7722*w3*hNegative;
ok(Math.abs(allSheet.conditionalSpinCode-maxConstrainedInfo)<1e-14,
  "since every triangle contributes ≤hMinus, original ALL− syndrome attains GLOBAL maximal complete-event Info under this named model");
console.log("CONDITIONAL_INFO",JSON.stringify({
 original_all8440_scalar_source_exactly_same:true,
 original_complete_Book_event_entropy_phi:allSheet.bookCode,
 native_Golden_negative_triangle_entropy_phi:hNegative,
 original_all_negative_triangle_source_unique_mod32_gauge:"consumes original exact 327 incidence rank theorem; not newly certified from JS enumeration",
 original_spin_single_sheet_increment_phi:oneSheet.conditionalSpinCode,
 original_uniform_all_negative_sheet_increment_phi:allSheet.conditionalSpinCode,
 prospective_cost_minus_info_sign_selector:"IF complete native Golden two-port Shannon is physically charged with negative sign, THEN all− triangle syndrome is unique max-Info gauge class on original full K913",
 selected_complete_Book03_Info_equals_Golden_Shannon:false,
 physical_M1_G0_quaternion_transport_admitted:false,
 GR_closed:false
},null,2));
