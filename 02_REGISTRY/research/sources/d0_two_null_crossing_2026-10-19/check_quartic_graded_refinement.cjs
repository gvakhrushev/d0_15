#!/usr/bin/env node
"use strict";
/* Exact integer-degree and rational coefficient audit for the SAVED
 * original six-plaquette all40 quartic solutions. No symbolic re-solve.
 *
 * The unit-grid native coframe E_m(X) has physical refinement
 * E_{h,m}(x)=h^m E_m(x/h); native link log L_m(X) similarly gives
 * omega_{h,m}(x)=h^(m-1) L_m(x/h). Thus degree(E_m)<=m,
 * degree(L_m)<=m-1 is precisely the no-negative-h grading.
 *
 * This tests the five quartic sectors on ONE selected cubic branch.
 * Cubic/pure lower-sector degree filtration is established by the
 * explicit source ansatz and its separate cubic owner, not replayed here.
 */
const fs=require("node:fs");
const path=require("node:path");
const root=__dirname;
const monomials=max=>Array.from({length:max+1},(_,degree)=>
    Array.from({length:degree+1},(_,i)=>[degree-i,i])).flat();

function degreeInfo(vec,offset,components,modes){
  const count=modes.length;
  let maximum=-1,nz=0,gradeCounts={},high=[];
  for(let i=0;i<components;i++){
    for(let j=0;j<count;j++){
      const v=vec[offset+i*count+j];
      if(!/^[-+]?\d+(?:\/\d+)?$/.test(v))
        throw Error("non-rational saved coefficient at "+(offset+i*count+j)+": "+v);
      if(v==="0"||v==="0/1"||v==="-0")continue;
      const d=modes[j][0]+modes[j][1];
      gradeCounts[d]=(gradeCounts[d]||0)+1;
      nz++;
      if(d>maximum){maximum=d;high=[]}
      if(d===maximum)high.push({component:i,monomial:modes[j],coefficient:v});
    }
  }
  return {degree:maximum,nonzero:nz,gradeCounts,top:high};
}
function audit(mixed,old){
  if(mixed.amplitude.join(",")!=="2,2")throw Error("not mixed quartic owner");
  const L6=monomials(6),C5=monomials(5),L5=monomials(5),C4=monomials(4);
  if(mixed.solution.length!==24*L6.length+16*C5.length)
    throw Error("unexpected quartic solution dimension");
  if(old.matrix.length!==24*L5.length+16*C4.length ||
     old.column_order.length!==5)throw Error("unexpected other-sector solution dimensions");
  const sectors=[];
  let sym,vec,links,coframe;
  for(let j=0;j<old.column_order.length;j++){
    const [a,b]=old.column_order[j],total=a+b;
    if(total!==4)throw Error("not a quartic sector");
    if(a===2&&b===2){
      sym="2,2";vec=mixed.solution;
      links=degreeInfo(vec,0,24,L6);
      coframe=degreeInfo(vec,24*L6.length,16,C5);
    }else{
      sym=a+","+b;
      vec=old.matrix.map(row=>row[j]);
      links=degreeInfo(vec,0,24,L5);
      coframe=degreeInfo(vec,24*L5.length,16,C4);
    }
    if(links.degree>3||coframe.degree>4)
      throw Error("NEGATIVE REFINEMENT POWER in sector "+sym+": "+links.degree+"/"+coframe.degree);
    sectors.push({sector:sym,links:{degree:links.degree,nonzero:links.nonzero},
                  coframe:{degree:coframe.degree,nonzero:coframe.nonzero}});
  }
  const L=degreeInfo(mixed.solution,0,24,L6),
        E=degreeInfo(mixed.solution,24*L6.length,16,C5);
  if(L.degree!==3||E.degree!==4)throw Error("unexpected leading mixed quartic");
  const leadingE=E.top.filter(x=>x.component===10).map(x=>
    x.coefficient+"*x^"+x.monomial[0]+"*y^"+x.monomial[1]);
  // One exact, physically h-rescaled quartic coframe coefficient.
  // Its degree-five competitor coefficients are all absent.
  const field10=C5.map((mon,j)=>({mon,coef:mixed.solution[24*L6.length+10*C5.length+j]}))
    .filter(v=>v.coef!=="0");
  const exactExpected=[[[0,2],"-7/256"],[[1,2],"-9/128"],
    [[0,3],"-1/128"],[[2,2],"3/128"],[[0,4],"1/256"]];
  if(JSON.stringify(field10.map(({mon,coef})=>[mon,coef]))!==JSON.stringify(exactExpected))
    throw Error("source-selected component (2,2) quartic C2 refinement changed");
  return {
    status:"PASS_QUARTIC_GRADED_C2_JET_REFINEMENT",
    amplitude_order:4,
    sectors,
    mixedLeadingLinks:L.top,
    mixedLeadingCoframe:E.top,
    coframe10Leading:leadingE,
    exact_refinement_component_2x: "3/128*x^2*y^2+1/256*y^4 -h*(9/128*x*y^2+1/128*y^3)-7/256*h^2*y^2",
    refinement_rule:{
      coframe_m_deg_d:"h^(4-d) P_d(x,y)",
      connection_m_deg_d:"h^(3-d) Q_d(x,y)",
      no_negative_powers:true,
      limit_exists_coefficientwise_Ck_on_compact:true
    },
    scope:"unit-grid source is a degree<=4 formal solution; h-rescaling is exact for original degree-two coframe star action. No all-amplitude root, global periodic solution, uniform fifth-order source control, or D0 native price."
  };
}
module.exports={audit};
if(require.main===module){
  const mixed=JSON.parse(fs.readFileSync(path.join(root,"quartic_full_spatial_jet_solution.json"),"utf8"));
  const other=JSON.parse(fs.readFileSync(path.join(root,"quartic_all_sectors_shared_cubic_branch_solution.json"),"utf8"));
  const result=audit(mixed,other);
  console.log(JSON.stringify(result,null,2));
}
