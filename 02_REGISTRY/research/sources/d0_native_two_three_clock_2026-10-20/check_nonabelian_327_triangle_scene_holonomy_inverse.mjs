#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL K(9,11,13) NON-ABELIAN FULL-GROUP inverse, exact over two
 * different prime fields of odd characteristic. Original local
 * proper-Lorentz SO+(1,3) is realized with the original NULL eta
 * via exp(r N2), exp(r N3), exp(r barN2), exp(r barN3), each exact
 * matrix polynomial I+rN+r²N²/2 (N³=0).
 *
 * Each original undirected scene edge has an independent freely
 * varying proper-Lorentz matrix U_uv (the reversed oriented edge
 * is its exact inverse). The matrix Holonomy around all ORIGINAL
 * ABC triangles is used to recover:
 *
 *   143 B-C chord matrices (H_(0,b,c)),
 *   104 A-C chord matrices (H_(a,9,c)),
 *    80 A-B chord matrices (H_(a,b,20)).
 *
 * Set the original 32 undirected tree-edge transports to identity
 * using a vertex-local original proper-Lorentz gauge. Then three
 * NONCOMMUTATIVE ordered reconstruction equations recover ALL
 * 327 off-tree matrices without assuming they commute.
 * Every based 2-step loop equals I and every original 3-step loop
 * is recovered up to its CORRECT base-frame conjugation.
 *
 * This is a mathematical FULL-GROUP global inverse in rooted-tree
 * gauge, not an actual physically admitted 4D Role-connection or
 * native Golden detector. The 327 original scene cycle group
 * variables have 327*6=1962 independent near-identity Lie tangent
 * directions. The already-owned fixed-Bell Golden17 six-coordinate
 * inverse, if admitted and properly co-transported to the same
 * oriented rooted reference, can in principle read each of these
 * via conditional triangle flags on ONE true 8440x17 clock record.
 *
 * Do NOT use scalar Wilson trace instead: it does not determine
 * matrix orientation or these group coordinates. Do NOT replace
 * the full G0/Book compulsory action by the mathematically observed
 * positive CAR17 conditional likelihood.
 */
const require=(cond,msg)=>{if(!cond)throw Error("FAIL "+msg)};
const ZONES=[9,11,13],siteZone=u=>u<9?0:u<20?1:2;
const originalEdges=[];
for(let u=0;u<33;u++)for(let v=u+1;v<33;v++)
  if(siteZone(u)!==siteZone(v))originalEdges.push([u,v]);
require(originalEdges.length===359,"original undirected edges");
const fundamentalTri=[];
for(let b=9;b<20;b++)for(let c=20;c<33;c++)
  fundamentalTri.push([0,b,c]);
for(let a=1;a<9;a++)for(let c=20;c<33;c++)
  fundamentalTri.push([a,9,c]);
for(let a=1;a<9;a++)for(let b=10;b<20;b++)
  fundamentalTri.push([a,b,20]);
require(fundamentalTri.length===327,"original fundamental ABC triangles");

function runOne(prime){
  const md=x=>(x%prime+prime)%prime;
  const times=(x,y)=>md(x*y);
  const inv=a=>{let k=prime-2,out=1,base=md(a);
    if(base===0)throw Error("zero field denominator");
    while(k){if(k%2)out=times(out,base);base=times(base,base);k=Math.floor(k/2)}
    return out;
  };
  const I=()=>Array.from({length:4},(_,i)=>
    Array.from({length:4},(_,j)=>+(i===j)));
  const E=(a,b)=>Array.from({length:4},(_,i)=>
    Array.from({length:4},(_,j)=>+(i===a&&j===b)));
  const M=(A,B)=>A.map(row=>B[0].map((_,j)=>
    md(row.reduce((s,x,k)=>s+x*B[k][j],0))));
  const plus=(A,B,s=1)=>A.map((row,i)=>row.map((x,j)=>md(x+s*B[i][j])));
  const scale=(A,s)=>A.map(row=>row.map(x=>times(x,s)));
  const transpose=A=>A[0].map((_,j)=>A.map(row=>row[j]));
  const equal=(A,B)=>A.every((row,i)=>row.every((x,j)=>x===B[i][j]));
  const zero=()=>Array.from({length:4},()=>Array(4).fill(0));
  const eta=[[0,1,0,0],[1,0,0,0],[0,0,prime-1,0],[0,0,0,prime-1]];
  const G=[
    plus(E(1,2),E(2,0)),
    plus(E(1,3),E(3,0)),
    plus(E(0,2),E(2,1)),
    plus(E(0,3),E(3,1))
  ];
  const half=inv(2);
  for(const X of G){
    require(equal(M(M(X,X),X),zero()),"original null Lie generator not nilpotent cubic");
    require(equal(plus(M(transpose(X),eta),M(eta,X)),zero()),
      "original null Lie generator is not proper Lorentz");
  }
  const EXP=(which,t)=>{
    const X=G[which],X2=M(X,X);
    return plus(plus(I(),scale(X,t)),scale(X2,times(times(t,t),half)));
  };
  // Nontrivial proper Lorentz on EVERY one of the original 359
  // undirected links, including ALL 32 gauge-tree edges. The exact
  // finite group is defined by nilpotent exponentials in odd Fp.
  // The parameter represents a small rational q/1024 in the
  // characteristic-zero chart and an exact modular reduction here.
  const edgeMatrices=new Map();
  for(const [u,v] of originalEdges){
    const gen=(u*17+v*29+u*v)%4,scalar=1+(u*13+v*7+v*u)%7;
    const t=times(scalar,inv(1024)),U=EXP(gen,t),
          Uminus=EXP(gen,md(-t));
    require(equal(M(U,Uminus),I()),"nonreversible original link exponential");
    require(equal(M(M(transpose(U),eta),U),eta),
      "edge transport not in original null-form proper Lorentz group");
    edgeMatrices.set(u+","+v,U);
    edgeMatrices.set(v+","+u,Uminus);
  }
  const raw=(u,v)=>edgeMatrices.get(u+","+v);
  require(originalEdges.every(([u,v])=>raw(u,v)&&raw(v,u)),
    "not the true bidirected original graph");
  // Original rooted spanning tree (exact 32 links):
  // root 0 to every B and C, plus B0=9 to each remaining A.
  const frames=Array(33).fill(null);frames[0]=I();
  for(let b=9;b<20;b++)frames[b]=raw(0,b);
  for(let c=20;c<33;c++)frames[c]=raw(0,c);
  for(let a=1;a<9;a++)frames[a]=M(frames[9],raw(9,a));
  const frameInv=Array(33).fill(null);
  for(let v=0;v<33;v++){
    // SO metric inverse is eta U^T eta, eta²=I in this null basis.
    frameInv[v]=M(M(eta,transpose(frames[v])),eta);
    require(equal(M(frames[v],frameInv[v]),I()),"invalid original tree frame");
  }
  const gauge=(u,v)=>M(M(frames[u],raw(u,v)),frameInv[v]);
  const target=(a,b,c)=>M(M(raw(a,b),raw(b,c)),raw(c,a));
  const canonicalHol=(a,b,c)=>M(M(frames[a],target(a,b,c)),frameInv[a]);
  const chords=new Map();
  const set=(u,v,U)=>{
    chords.set(u+","+v,U);
    chords.set(v+","+u,M(M(eta,transpose(U)),eta));
  };
  for(let b=9;b<20;b++)set(0,b,I());
  for(let c=20;c<33;c++)set(0,c,I());
  for(let a=1;a<9;a++)set(a,9,I());
  require(chords.size===64,"32 original tree links not installed bidirectionally");
  // Step ONE: 143 BC chords; H'_0bc=U'_bc.
  for(let b=9;b<20;b++)for(let c=20;c<33;c++){
    const H=canonicalHol(0,b,c);
    set(b,c,H);
  }
  // Step TWO: 104 AC chords.
  // H'_a9c=U'_a9 U'_9c U'_ca
  //         =U'_9c (U'_ac)^(-1)
  // Therefore U'_ac=(H'_a9c)^(-1) U'_9c. ORDER MATTERS.
  for(let a=1;a<9;a++)for(let c=20;c<33;c++){
    const H=canonicalHol(a,9,c),Hi=M(M(eta,transpose(H)),eta);
    set(a,c,M(Hi,chords.get("9,"+c)));
  }
  // Step THREE: remaining 80 AB chords:
  // H'_abc0=U'_ab U'_bc0 (U'_ac0)^(-1)
  // U'_ab=H'_abc0 U'_ac0 (U'_bc0)^(-1).
  for(let a=1;a<9;a++)for(let b=10;b<20;b++){
    const H=canonicalHol(a,b,20),bcInverse=chords.get("20,"+b);
    set(a,b,M(M(H,chords.get(a+",20")),bcInverse));
  }
  require(chords.size===2*originalEdges.length,"not entire 718 original orientations reconstructed");
  let mismatch=0,distinct=0;
  for(const [u,v] of originalEdges){
    const U=chords.get(u+","+v),expect=gauge(u,v);
    if(!equal(U,expect))mismatch++;
    if(!equal(U,I()))distinct++;
  }
  require(mismatch===0&&distinct>100,
    "genuinely noncommuting all-edge root gauge inverse failed");
  const triGroup=[];
  for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++){
    const hol=M(M(chords.get(a+","+b),chords.get(b+","+c)),chords.get(c+","+a));
    const original=canonicalHol(a,b,c);
    require(equal(hol,original),"some original 1287 ABC triangle has wrong group product");
    triGroup.push(hol);
  }
  require(triGroup.length===1287,"original triangle count failed");
  const backtracks=originalEdges.reduce((n,[u,v])=>{
    require(equal(M(chords.get(u+","+v),chords.get(v+","+u)),I()),
      "original 2-step inverse-edge holonomy not identity");
    return n+2;
  },0);
  require(backtracks===718,"original 2-step based counts mismatch");
  // A genuinely noncommuting pair of group-valued triangle sources
  // is present. This is *not* a collection of scalar Wilson traces.
  const commutator=(A,B)=>plus(M(A,B),M(B,A),-1);
  let pair=null;
  outer:for(let j=0;j<Math.min(triGroup.length,40);j++)
    for(let k=j+1;k<Math.min(triGroup.length,50);k++)
      if(!equal(commutator(triGroup[j],triGroup[k]),zero())){
        pair=[j,k];break outer;
      }
  require(pair!==null,"all original generated Lorentz triangle holonomies commute!");
  // Gauge-invariant transport e.g. a rooted Wilson trace is
  // unchanged under exact original vertex gauge and is NOT enough
  // to recover the six signed Lie coordinates; full matrix must be
  // read relative to a transported original coframe/reference.
  return {
    prime,
    status:"PASS_ORIGINAL_327_NONABELIAN_TRIANGLE_GROUP_INVERSE",
    originalUndirectedEdges:originalEdges.length,
    originalDirectedEdges:2*originalEdges.length,
    rootGaugeTreeEdges:32,
    reconstructBC:143,reconstructAC:104,reconstructAB:80,
    recoveredOffTreeGroupElements:327,
    fullReconstructedEdgeMismatches:mismatch,
    allOriginalABCtriangles:triGroup.length,
    allOriginalBasedBacktracks:backtracks,
    noncommutingOriginalTrianglePair:pair,
    allGroupMultiplicationsExactModPrime:true,
    originalNullLorentzEtaPreserved:true
  };
}
const samples=[1009,2017,65537].map(runOne);
for(const s of samples)require(s.status.startsWith("PASS"),"modular source run failed");
const result={
 status:"PASS_EXACT_NONABELIAN_ORIGINAL_SCENE_327_GROUP_RECONSTRUCTION",
 allOriginalCases:samples,
 exactGroupDimension6Times327:327*6,
 originalBookScalarIndependentQuotient686:686,
 possibleMathematicalJointScalarAndBasedLorentzSourceRank:686+327*6,
 full8440ClockWith17OutcomeMarkerLabels:8440*17,
 typedCaveat:"Root-frame co-transported pretrace full SO holonomies for every ABC triple AND real path-conditioned fixed-Bell Golden17 input/controller assumed. Unmarked Wilson traces do not determine matrices; scalar Book price does not select this programme. K913 scene group gauge variables are NOT 4D Golden LEFT Role links. GR_closed=false",
 GR_closed:false
};
console.log(JSON.stringify(result,null,2));
