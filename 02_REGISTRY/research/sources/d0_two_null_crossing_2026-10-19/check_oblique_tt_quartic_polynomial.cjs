#!/usr/bin/env node
"use strict";
/*
 * The original six-plaquette all40 Schur, in the exact Laurent/Taylor
 * convention z_mu=(1+h)^(k_mu), has tested TWO common TT characteristic
 * root expansions along non-axial Lorentz-null k:
 *
 *   k_v(h)=k_v+gamma(k) h^2 + ...
 *
 * For the checked null directions, the finite-source solvability of
 * S2 e2 = -(S4 e0+S3 e1+gamma d_kv(S2)e0) yields the same gamma for
 * both TT frames and agrees with ONE symmetric homogeneous quartic
 * numerator gamma=P4(k)/(48 k_u).
 *
 * This checker verifies a mathematical CANDIDATE on 44 explicit rays
 * modulo each selected exact prime. It also checks the independent
 * first-corrector ambiguity S3(ker S2) subset im S2 and the 9-dimensional
 * symmetry-reduced null quartic interpolation class.
 *
 * IMPORTANT: 44 exact samples are NOT a coefficientwise symbolic proof
 * for arbitrary rational/real null k. The universal formula is a
 * HYPOTHESIS-TO-CERTIFY. No physical D0 Book source is selected.
 */
const {oneRay,schurTaylor}=
  require("./check_oblique_tt_directional_dispersion.cjs");
const {gauss,prime}=
  require("./check_full40_schur_rank_modular.cjs");
const mod=x=>((x%prime)+prime)%prime;
const times=(x,y)=>mod(x*y);
const minus=(x,y)=>mod(x-y);
const plus=(x,y)=>mod(x+y);
const pow=(base,n)=>{let v=1;for(let j=0;j<n;j++)v=times(v,base);return v};
function inv(a){
  let v=mod(a);if(!v)throw Error("noninvertible mod"+prime);
  let k=prime-2,out=1;while(k>0){
    if(k%2)out=times(out,v);
    v=times(v,v);k=Math.floor(k/2);
  }return out;
}
function numerator(k){
  const [u,v,x,y]=k,Q=x*x+y*y,P=x*y,U=u+v,T=x+y;
  // Expressed with integer coefficients to avoid rational rounding.
  return mod(5*Q*Q+12*P*Q-4*P*P
           -6*U*T*Q+2*(u*u+v*v)*Q);
}
function predicted(k){return times(numerator(k),inv(48*k[0]))}
function symBasis(a,b,degree){
  let list=[];for(let j=0;j<=Math.floor(degree/2);j++){
    const i=degree-j;
    let v=times(pow(a,i),pow(b,j));
    if(i!==j)v=plus(v,times(pow(a,j),pow(b,i)));
    list.push(v);
  }return list;
}
function quarticInvariants(k){
  const [u,v,x,y]=k,out=[];
  for(let degree=0;degree<=4;degree++){
    for(let A of symBasis(u,v,degree))
      for(let X of symBasis(x,y,4-degree))
        out.push(times(A,X));
  }return out;
}
function nullKernel(A){
  const m=A.length,n=A[0].length,M=A.map(row=>row.slice()),
        piv=[];let rank=0;
  for(let j=0;j<n&&rank<m;j++){
    let ii=rank;while(ii<m&&!M[ii][j])ii++;
    if(ii===m)continue;
    [M[ii],M[rank]]=[M[rank],M[ii]];
    const f=inv(M[rank][j]);
    for(let c=j;c<n;c++)M[rank][c]=times(M[rank][c],f);
    for(let i=0;i<m;i++)if(i!==rank){
      const t=M[i][j];
      if(t)for(let c=j;c<n;c++)M[i][c]=minus(M[i][c],times(t,M[rank][c]));
    }piv.push(j);rank++;
  }
  const vectors=[];
  for(let j=0;j<n;j++)if(!piv.includes(j)){
    let v=Array(n).fill(0);v[j]=1;
    for(let i=0;i<rank;i++)v[piv[i]]=mod(-M[i][j]);
    vectors.push(v);
  }
  return vectors;
}
const mv=(A,v)=>A.map(row=>mod(row.reduce((sum,x,i)=>sum+x*v[i],0)));

// The first 28 samples produced the symmetric quartic polynomial candidate
// over F1009; all remaining 16 are independently chosen holdouts.
const training=[
[1,2,2,0],[1,4,2,2],[1,5,1,3],[1,5,3,1],[2,1,2,0],
[2,2,2,2],[2,5,2,4],[1,8,4,0],[2,4,4,0],[2,8,4,4],
[1,5,-1,3],[1,5,1,-3],[1,5,-1,-3],[5,1,1,3],
[1,10,2,4],[1,1,1,1],[1,1,1,-1],[1,2,-2,0],
[1,2,0,2],[1,2,0,-2],[1,4,-2,2],[1,4,2,-2],
[1,4,-2,-2],[1,8,-4,0],[1,5,3,-1],[5,1,1,-3],
[1,10,-2,4],[1,10,2,-4]
];
const holdouts=[
[1,13,1,5],[1,13,-1,5],[1,13,1,-5],[1,17,3,5],
[1,17,-3,5],[1,17,-3,-5],[1,18,6,0],[1,18,-6,0],
[2,10,2,6],[2,10,-2,6],[3,3,3,3],[3,3,3,-3],
[4,5,2,6],[4,5,6,2],[5,5,1,7],[5,5,7,1]
];
function audit(){
  const samples=[...training,...holdouts],observed=[];
  for(const k of samples){
    if(k[0]===0||2*k[0]*k[1]!==k[2]*k[2]+k[3]*k[3])
      throw Error("invalid null ray "+k);
    const test=oneRay(k),expected=predicted(k);
    if(test.plus.gamma_mod_p!==expected||
       test.cross.gamma_mod_p!==expected)
      throw Error("quartic candidate contradicts ORIGINAL full40 "+prime+" "+k+
        " predicted "+expected+" actual "+test.plus.gamma_mod_p+" / "+test.cross.gamma_mod_p);
    observed.push({k,gamma_mod_p:expected});
  }
  const invariantRank=gauss(samples.map(quarticInvariants)).rank;
  if(invariantRank!==9)throw Error("wrong symmetric null-cone quartic dimension "+invariantRank);
  const modelRank=gauss(samples.map(k=>[...quarticInvariants(k),
      mod(-2*k[0]*predicted(k))])).rank;
  if(modelRank!==invariantRank)
    throw Error("quartic numerator not in symmetry-reduced invariant span");
  const gaugeControls=[];
  for(const k of [[1,2,2,0],[1,5,1,-3],[1,5,-1,-3],[2,2,2,2]]){
    const [S2,S3]=schurTaylor(k),basis=nullKernel(S2);
    const augmented=S2.map((row,i)=>[...row,
      ...basis.map(v=>mv(S3,v)[i])]);
    if(basis.length!==12||gauss(S2).rank!==4||
       gauss(augmented).rank!==4)
      throw Error("first corrector changes quartic source at "+k);
    gaugeControls.push({k,TT_zero_modes:12,rankS2:4,rankS2_plus_S3_ker:4});
  }
  return {
    status:"PASS_QUARTIC_CANDIDATE_44_NULL_RAYS_AND_CORRECTOR_INDEPENDENCE",
    prime,training_rays:training.length,independent_holdouts:holdouts.length,
    tested_all40_TT_sources:samples.length*2,
    quartic_invariant_candidates:14,null_cone_rank:invariantRank,
    quartic_numerator_in_symmetry_reduced_span:true,
    gamma_formula:"(5Q²+12PQ−4P²−6(u+v)(x+y)Q+2(u²+v²)Q)/(48u), Q=x²+y², P=xy",
    no_tested_plus_cross_birefringence:true,
    null_corrector_ambiguity:gaugeControls,
    observed:observed,
    status_scope:"EXACT FINITE-FIELD SAMPLED HYPOTHESIS, NOT UNIVERSAL POLYNOMIAL IDENTITY; GR_closed=false"
  };
}
module.exports={audit};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
