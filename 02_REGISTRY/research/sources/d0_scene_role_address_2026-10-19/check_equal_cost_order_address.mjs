#!/usr/bin/env node
'use strict';
/*
 * A scalar-Cost-Info-NEUTRAL, literal ORIGINAL K(9,11,13)
 * based-history address code for all 3072 oriented faces of the L=4
 * four-dimensional Role cube.
 *
 * Seven different original based directed ABC triangles are concatenated
 * in all 7! permutations, yielding 5040 pairwise DISTINCT length21
 * history words with EXACTLY the same directed-edge counts, node counts,
 * initial/final vertex, primitive step count and therefore SAME ORIGINAL
 * additive scalar Cost-Info S(y) and ALL field derivatives at arbitrary y.
 *
 * This is a mathematical history-address theorem, not a claim of actual
 * selected noncommuting Lorentz transport, physical Book action, or cheap
 * unconditioned sampling. 7! is much more expensive than the optimal
 * general length4 code (8616 loops), illustrating the source/cost tradeoff.
 */
const require=(x,m)=>{if(!x)throw Error(m)};
const A0=0,B0=9,C0=20,SIZES=[9,11,13];
const part=i=>i<9?0:i<20?1:2;
const edge=(u,v)=>part(u)!==part(v);
const loops=Array.from({length:7},(_,j)=>[A0,B0+j,C0,A0]);
require(loops.every(w=>w.length===4&&w.every((x,i)=>i===0||edge(w[i-1],x))),
  'some original triangle has invalid graph edge');
function word(perm){
  let path=[A0];
  for(let j of perm)path.push(...loops[j].slice(1));
  return path;
}
function counts(path){
  let edges=new Map(),nodes=new Map();
  for(let i=0;i<path.length;i++){
    nodes.set(path[i],1+(nodes.get(path[i])||0));
    if(i){const key=path[i-1]+'>'+path[i];
      edges.set(key,1+(edges.get(key)||0));}
  }
  return {edges:[...edges].sort((a,b)=>a[0].localeCompare(b[0])),
          nodes:[...nodes].sort((a,b)=>a[0]-b[0])};
}
function permutations(k){
  let all=[];
  const visit=(path,left)=>{
    if(!left.length){all.push(path);return;}
    for(let j=0;j<left.length;j++)
      visit([...path,left[j]],left.filter((_,i)=>i!==j));
  };
  visit([],Array.from({length:k},(_,i)=>i));
  return all;
}
function audit(){
  let perms=permutations(7);
  require(perms.length===5040,'wrong factorial capacity');
  const first=word(perms[0]),reference=JSON.stringify(counts(first));
  let names=new Set();
  // Use independent synthetic Cost/Info polynomials as hostile finite
  // fixtures, but equality of the integer occurrence maps is the PROOF
  // for arbitrary smooth C_uv(y), I_v(y), all derivatives.
  let s0=0,s1=0,s2=0;
  const hash=(a,b)=>((a*37+b*73+11)%101)-50;
  function coefficients(path){
    const val=[0,0,0];
    for(let i=0;i<path.length;i++){
      const v=path[i];
      val[0]-=(v*v+7*v)%17;
      val[1]-=v%11;
      val[2]-=v%13;
      if(i){
        const u=path[i-1];
        val[0]+=(u*3+v*5)%29;
        val[1]+=hash(u,v);
        val[2]+=(u+v)**2%23;
      }
    }
    return val;
  }
  const firstCoeff=coefficients(first);
  for(let perm of perms){
    let path=word(perm),name=path.join(',');
    require(path.length===22&&path[0]===A0&&path[21]===A0,
      'not a true common-endpoint 21-transition scene history');
    require(!names.has(name),'two different loop orders share same literal history');
    names.add(name);
    require(JSON.stringify(counts(path))===reference,
      'source variation changes original edge/node counts');
    const coef=coefficients(path);
    require(coef.every((x,i)=>x===firstCoeff[i]),
      'adversarial nontrivial field Cost-Info coefficients diverge');
  }
  // Actual original unweighted Perron eigenpair.
  const rho=21.837382401125154,r0=.03242817392839132;
  const probPerUnconditionedWord=r0/rho**21;
  return {
    status:'PASS_ORIGINAL_5040_EQUAL_COST_ORDER_ADDRESSES',
    original_graph:'K(9,11,13)',same_base_vertex:A0,
    original_distinct_triangles:7,
    different_ordered_complete_history_labels:names.size,
    count_needed_for_L4_6_based_faces_both_orientations:2*6*256,
    original_history_steps:21,
    exact_same_directed_edge_multiset:true,
    exact_same_vertex_multiset:true,
    equal_original_additive_scalar_Cost_Info_for_ARBITRARY_fields:true,
    all_field_jet_orders_same_in_scalar_Cost_Info:true,
    synthetic_second_jet_nontrivial: firstCoeff,
    original_unconditioned_Perron_probability_per_word:probPerUnconditionedWord,
    selected_3072_complete_event_mass:3072*probPerUnconditionedWord,
    all_5040_event_mass:5040*probPerUnconditionedWord,
    actual_field_independent_source_does_NOT_supply_noncommuting_geometry_without_control:true,
    physical_admission_and_selected_book_action:false,
    GR_closed:false
  };
}
console.log(JSON.stringify(audit(),null,2));
