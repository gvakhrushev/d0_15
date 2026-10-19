#!/usr/bin/env node
'use strict';
/*
 * Original K(9,11,13) full-walk address capacity, with NO replacement
 * graph, added primitive transition or erased history.
 *
 * Fixed vertex a0; for each physical L^4 Role lattice reserve one distinct
 * ORIGINAL closed scene walk for every (site, based face r<s, orientation ±).
 *
 * Exact BigInt counts, deterministic lexicographic rank/unrank, equal native
 * one-sided Perron cylinder probability for each same-endpoint same-length
 * word. This proves ADDRESS capacity, not independent control of Lorentz
 * parameters: a single fixed scene link representation remains bounded by
 * the 327-cycle SO(1,3) gauge quotient.
 */
const SIZES=[9,11,13], N=33, A0=0;
const part=i=>i<9?0:i<20?1:2;
const adj=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>part(i)!==part(j)));
const require=(x,m)=>{if(!x)throw Error(m)};
const neighbors=adj.map(row=>row.map((x,i)=>x?i:null).filter(x=>x!==null));
function tables(steps){
  const dp=[Array.from({length:N},(_,i)=>i===A0?1n:0n)];
  for(let m=1;m<=steps;m++){
    dp[m]=Array.from({length:N},(_,i)=>neighbors[i].reduce((s,j)=>s+dp[m-1][j],0n));
  }
  return dp;
}
function capacity(length){return tables(length)[length][A0]}
function minLength(needed){
  let n=2;while(capacity(n)<BigInt(needed))n++;
  return n;
}
function unrank(rank,steps,DP=tables(steps)){
  let j=BigInt(rank),v=A0,word=[v];
  require(j>=0n&&j<DP[steps][A0],"rank outside original closed walk class");
  for(let left=steps;left>=1;left--){
    let selected=null;
    for(let w of neighbors[v]){
      let block=DP[left-1][w];
      if(j>=block)j-=block;
      else{selected=w;break;}
    }
    require(selected!==null,"rank did not select next original allowed edge");
    v=selected;word.push(v);
  }
  require(v===A0&&j===0n,"not based-closed or unused rank");
  return word;
}
function rankWord(word,DP=tables(word.length-1)){
  let rank=0n,v=A0,length=word.length-1;
  require(word[0]===A0&&word[length]===A0,"not a based history");
  for(let left=length;left>=1;left--){
    const next=word[length-left+1];
    require(adj[v][next],"invalid directed original K edge");
    for(let w of neighbors[v]){if(w===next)break;rank+=DP[left-1][w];}
    v=next;
  }
  return rank;
}
// Perron eigenvalue of the ORIGINAL 33x33 adjacency:
// rho^3 - 359 rho - 2574 = 0; 30 other eigenvalues exactly 0.
const f=x=>x*x*x-359*x-2574;
function rhoRoot(){
  let a=20,b=24;
  for(let k=0;k<90;k++){const m=(a+b)/2;if(f(m)>0)b=m;else a=m;}
  return (a+b)/2;
}
function normalizedPerron(){
  let z=[1,1,1];
  for(let k=0;k<160;k++){
    const next=[11*z[1]+13*z[2],9*z[0]+13*z[2],9*z[0]+11*z[1]];
    const norm=next.reduce((s,x,i)=>s+x*SIZES[i],0);
    z=next.map(x=>x/norm);
  }
  const rho=rhoRoot();
  for(let i=0;i<3;i++){
    const next=[11*z[1]+13*z[2],9*z[0]+13*z[2],9*z[0]+11*z[1]][i];
    require(Math.abs(next-rho*z[i])<1e-13,"non-Perron zone eigenvector");
  }
  return {rho,r:z,pi0:z[0]*z[0]/z.reduce((a,v,i)=>a+SIZES[i]*v*v,0)};
}
function exactControl(){
  require(adj.flat().filter(Boolean).length===718,"original edge count");
  require(neighbors[0].length===24,"original K9 degree");
  const expected=new Map([[2,24n],[3,286n],[4,8616n],[5,164450n],
    [6,3829308n],[7,81215134n],[8,1798015872n],[9,39012871898n]]);
  for(let [n,count] of expected)require(capacity(n)===count,"native return count changed at "+n);
  const result=[],{rho,r,pi0}=normalizedPerron();
  for(let L of [2,4,8,16,32,64,128]){
    const V=L**4,needed=12*V,n=minLength(needed),DP=tables(n),available=DP[n][A0];
    require(available>=BigInt(needed),"not enough original full-history labels");
    if(n>2)require(capacity(n-1)<BigInt(needed),"not minimal length");
    const ranks=L===4?Array.from({length:needed},(_,i)=>i):
        [...new Set([0,1,Math.floor(needed/3),Math.floor(2*needed/3),needed-1])];
    const seen=new Set();
    for(let j of ranks){
      const w=unrank(j,n,DP);
      require(rankWord(w,DP)===BigInt(j),"rank/unrank failed");
      const key=w.join("-");
      require(!seen.has(key),"two address labels coincide");
      seen.add(key);
      if(L===4){
        const orientedFaceId=j;
        const ori=orientedFaceId%2;
        const face=Math.floor(orientedFaceId/2)%6;
        const site=Math.floor(orientedFaceId/12);
        require(site>=0&&site<V&&face<6&&ori<2,"face indexing failure");
      }
    }
    // Literal ORIGINAL one-sided normalized Perron all-walk probability
    // for each selected closed word: rho^-n r(a0); not a fitted prior.
    const probPerWord=r[0]*rho**(-n);
    const selectedMass=needed*probPerWord;
    const allReturnMass=Number(available)*probPerWord;
    require(selectedMass>0&&selectedMass<1&&allReturnMass<1,"invalid native probability");
    result.push({L,V,orientedBasedFaces:needed,minimumNativeSteps:n,
      allowedBasedReturnWords:String(available),equalNativePathProbability:probPerWord,
      selectedCompleteLawMass:selectedMass,allReturnMass,
      checks:ranks.length});
  }
  // For a FIXED scene representation, all loop holonomies depend on
  // only 327=359-33+1 SO(1,3) cycle matrices. Distinct labels do NOT
  // manufacture independent continuous Lorentz coordinates.
  const finiteL4={independentSceneCycles:359-33+1,independentRoleCycles:3*256+1};
  require(finiteL4.independentRoleCycles>finiteL4.independentSceneCycles,
    "unexpected scene vs 4D link gauge rank");
  return {
    status:"PASS_ORIGINAL_K913_FACE_HISTORY_ADDRESS_NO_FIXED_REPRESENTATION_SHORTCUT",
    originalVertices:33,directedEdges:718,
    basedReturnCounts:Object.fromEntries([...expected].map(([n,v])=>[n,String(v)])),
    exactIntegerRankUnrank:true,
    uniformEndpointLengthNativeWeights:true,
    perVertexPerronAtA0:r[0],stationaryAtA0:pi0,rho,
    asymptotic:"C_n~pi(a0)*rho^n; n(L)=4*log(L)/log(rho)+O(1)",
    allSelectedFacesMayBeReadFromONEOriginalWalkSupport:true,
    fixedSceneLorentzRankBound_L4:finiteL4,
    physicalControlRequired:"history-index-conditioned 4D face→SO(1,3) actuation plus complete Cost/Info/ref128/CAR16/clock/work; no compulsory physical selector proved",
    cases:result,
    GR_closed:false
  };
}
export {};
// This script remains classic .mjs runnable by Node with no external imports.
console.log(JSON.stringify(exactControl(),null,2));
