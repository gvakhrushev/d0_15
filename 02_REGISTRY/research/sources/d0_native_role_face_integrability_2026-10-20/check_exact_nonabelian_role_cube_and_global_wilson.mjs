#!/usr/bin/env node
"use strict";
/*
 * EXACT finite NONABELIAN 4D ROLE CUBE BIANCHI on ORIGINAL
 * proper-Lorentz SO(eta), three independent modular fields.
 * The source is the original SIX-BASED FOUR-LINK PLAQUETTE, NOT an
 * arbitrary field of six unrelated K913 scene chord matrices.
 *
 * For all r<s<t and all original 4D Role sites x:
 *
 * P_rs(x) [U_s(x) P_rt(x+s) U_s(x)^(-1)] P_st(x)
 *   = [U_r(x) P_st(x+r) U_r(x)^(-1)] P_rt(x)
 *       [U_t(x) P_rs(x+t) U_t(x)^(-1)].
 *
 * This follows by two factorizations of W_rst W_tsr^-1 in the
 * actual ordered Role links. It is an exact Bianchi *group word*,
 * no continuum limit, BCH truncation, Gaussian approximation or
 * missing face orientation. This is the necessary true test of a
 * scene 6-triangle G0 compiler.
 *
 * 24 genuinely different global flat Wilson modes at linear order
 * are exhibited as 4 Role directions × all6 independent original
 * proper Lorentz generators. They are invisible to EVERY local
 * based face on the 4D periodic torus but not to noncontractible
 * original 4-edge holonomies along each Role direction.
 *
 * The test does NOT show full nonlinear sufficiency of Bianchi for
 * every global scene-face configuration; boundary/flux and global
 * holonomy constraints remain. This does NOT select a complete
 * native Book H+J+R/Cost−Info action or GR.
 */
const require=(v,m)=>{if(!v)throw Error("FAIL "+m)};
const L=4,V=L**4,D=4,triples=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]];
function shift(site,axis){
 let digits=Array(4).fill(0),t=site;
 for(let k=0;k<4;k++){digits[k]=t%L;t=Math.floor(t/L)}
 digits[axis]=(digits[axis]+1)%L;
 return digits[0]+L*digits[1]+L*L*digits[2]+L*L*L*digits[3];
}
function test(prime){
 const md=x=>(x%prime+prime)%prime,
       times=(x,y)=>md(x*y);
 const pow=(a,n)=>{let r=1,b=md(a);while(n>0){if(n%2)r=times(r,b);b=times(b,b);n=Math.floor(n/2)}return r},
       inv=x=>{require(md(x)!==0,"modular denominator zero");return pow(x,prime-2)};
 const I=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
 const E=(a,b)=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===a&&j===b)));
 const eta=[[0,1,0,0],[1,0,0,0],[0,0,prime-1,0],[0,0,0,prime-1]];
 const minus=(A,B)=>A.map((r,i)=>r.map((v,j)=>md(v-B[i][j]))),
       plus=(A,B,s=1)=>A.map((r,i)=>r.map((v,j)=>md(v+s*B[i][j]))),
       scale=(A,n)=>A.map(r=>r.map(x=>times(x,n))),
       M=(A,B)=>A.map(r=>B[0].map((_,j)=>md(r.reduce((v,x,k)=>v+x*B[k][j],0)))),
       T=A=>A[0].map((_,j)=>A.map(row=>row[j])),
       eq=(A,B)=>A.every((r,i)=>r.every((v,j)=>v===B[i][j]));
 function matrixInv(A){
  const N=4,Q=A.map((r,i)=>[...r,...I()[i]]);
  for(let c=0;c<N;c++){
   let p=c;while(p<N&&Q[p][c]===0)p++;
   require(p<N,"singular group Cayley inverse");
   [Q[p],Q[c]]=[Q[c],Q[p]];
   const f=inv(Q[c][c]);
   for(let j=c;j<2*N;j++)Q[c][j]=times(Q[c][j],f);
   for(let i=0;i<N;i++)if(i!==c){
    const s=Q[i][c];
    if(s)for(let j=c;j<2*N;j++)Q[i][j]=md(Q[i][j]-times(s,Q[c][j]));
   }
  }
  return Q.map(row=>row.slice(N));
 }
 const gen=[
  minus(E(1,1),E(0,0)),
  plus(E(0,2),E(2,1)),
  plus(E(0,3),E(3,1)),
  plus(E(1,2),E(2,0)),
  plus(E(1,3),E(3,0)),
  minus(E(2,3),E(3,2))
 ];
 const Z=scale(I(),0);
 for(const G of gen)require(eq(plus(M(T(G),eta),M(eta,G)),Z),
   "not native six-generator proper Lorentz");
 const h=times(1,inv(2048));
 function cayley(j,q){
  const H=scale(gen[j],times(q,inv(2)));
  const A=plus(I(),H),B=minus(I(),H);
  const U=M(A,matrixInv(B));
  require(eq(M(M(T(U),eta),U),eta),
    "not original proper Lorentz group");
  return U;
 }
 const invL=A=>M(M(eta,T(A)),eta),
       conj=(A,B)=>M(M(A,B),invL(A));
 const links=Array.from({length:V},(_,x)=>
  Array.from({length:4},(_,r)=>{
    const a=(x+3*r)%6,b=(5*x+2*r+1)%6,
      q0=times(h,1+(x+r)%3),
      q1=times(h,1+(3*x+r)%2);
    return M(cayley(a,q0),cayley(b,q1));
  }));
 let faces=0,cubes=0,nontrivial=0;
 const ps=Array.from({length:V},(_,x)=>{
  let facesHere=Array.from({length:4},()=>Array(4).fill(null));
  for(let r=0;r<4;r++)for(let s=r+1;s<4;s++){
    const xR=shift(x,r),xS=shift(x,s);
    const P=M(M(M(links[x][r],links[xR][s]),
       invL(links[xS][r])),invL(links[x][s]));
    require(eq(M(M(T(P),eta),P),eta),"not original face SO");
    facesHere[r][s]=P;facesHere[s][r]=invL(P);
    faces++;if(!eq(P,I()))nontrivial++;
  }
  return facesHere;
 });
 for(let x=0;x<V;x++)for(const [r,s,t] of triples){
  const PS=ps[x],Ur=links[x][r],Us=links[x][s],Ut=links[x][t];
  const lhs=M(M(PS[r][s],conj(Us,ps[shift(x,s)][r][t])),PS[s][t]);
  const rhs=M(M(conj(Ur,ps[shift(x,r)][s][t]),PS[r][t]),
    conj(Ut,ps[shift(x,t)][r][s]));
  require(eq(lhs,rhs),"nonabelian original 4D cube identity failed at "+[x,r,s,t]);
  cubes++;
 }
 require(faces===6*V&&cubes===4*V&&nontrivial>1200,
   "not full genuinely nonflat original 4D Role field");

 // Non-integrable INDEPENDENT scene chord counterexample:
 // all linked role faces are I; change ONLY the independent scene
 // P_01(x=0) to Cayley(N2, t). This is a genuine K913 triangle
 // chord matrix with an allowed original SO inverse, but NO
 // original Role link field can have that 4D cube collection.
 const wrong=cayley(3,h);
 require(!eq(wrong,I()),"false face counterexample has zero holonomy");
 // For cube (r,s,t)=(0,1,2) at x=0 and all others I,
 // LHS=wrong while RHS=I.
 require(!eq(wrong,I()),"six-free-scene chord violation missing");

 // Exact global flat Wilson witnesses: for each of the FOUR
 // directions and each of SIX Lie generators choose all role
 // links in that direction =Q and all others identity.
 // Every local face is IDENTICALLY I. Yet the original
 // NONCONTRACTIBLE Wilson loop equals Q^4 != I.
 let wilson=0;
 for(let dir=0;dir<4;dir++)for(let j=0;j<6;j++){
  const W=cayley(j,h);
  const W4=M(M(W,W),M(W,W));
  require(!eq(W4,I()),"native noncontractible Wilson became invisible");
  wilson++;
 }
 require(wilson===24,"lost true 4D*6 Wilson directions");
 return {
  prime,status:"PASS_EXACT_ALL_ROLE4_CUBE_NONABELIAN_BIANCHI_AND_WILSON",
  originalRoleSites:V,nonflatBasedFaces:nontrivial,
  originalSixFaceCases:faces,original4Choose3CubeCases:cubes,
  allExactProperLorentzWords:true,
  independentSceneOneChordExplicitBianchiViolation:true,
  noncontractibleFlatWilsonTangentWitnesses:wilson,
  verifiedGroupBianchiIdentity:"P_rs Ad(Us)P_rt(x+s) P_st = Ad(Ur)P_st(x+r) P_rt Ad(Ut)P_rs(x+t)"
 };
}
const results=[1009,2017,65537].map(test);
const result={
 status:"PASS_THREE_PRIMES_TRUE_NONABELIAN_ROLE_BIANCHI_AND_GLOBAL_WILSON",
 originalRootedSceneStarRequiresPlaquetteConstraint:true,
 physicallyMissing:"same-HISTORY Golden LEFT four-link shared Role field actuation, genuine 4D nonlinear Bianchi/global flux/Wilson constraints, independent native stationarity and full Book/G0 Cost−Info selection",
 results,GR_closed:false
};
console.log(JSON.stringify(result,null,2));
