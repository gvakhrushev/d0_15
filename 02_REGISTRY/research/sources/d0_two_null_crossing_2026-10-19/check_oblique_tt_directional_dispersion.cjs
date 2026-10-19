#!/usr/bin/env node
"use strict";
/*
 * Direct finite-Taylor continuation of the ORIGINAL six-based star Schur,
 * with all 24 Lorentz links eliminated on its actual flat owner.
 *
 * Uses the unchanged tested all40 modular source plus its exact binomial
 * Taylor coefficients, avoiding FFT alias and floating cancellation.
 * On each 4D Minkowski-null ray k, computes S2, S3, S4 in
 * z_mu=(1+h)^k_mu, two genuine transverse-traceless frames,
 * a first-order coframe corrector e1, then ONE correction gamma to k_v:
 *
 * S2 e0 = 0
 * S2 e1 + S3 e0 = 0
 * S2 e2 + gamma * (d S2 / d k_v) e0 + S3 e1 + S4 e0 = 0.
 *
 * Report all failures. This is modular exact at prime1009, not a full
 * rational closed characteristic polynomial or a selected native action.
 */
const {flatTaylorBlocks,gauss,prime,audit:baseAudit}=
  require("./check_full40_schur_rank_modular.cjs");
const md=x=>((x%prime)+prime)%prime;
const add=(x,y)=>md(x+y),sub=(x,y)=>md(x-y),mul=(x,y)=>md(x*y);
const inv=x=>{
 let y=md(x);if(!y)throw Error("zero divisor");
 let r=1,a=y,n=prime-2;
 while(n>0){if(n%2)r=mul(r,a);a=mul(a,a);n=Math.floor(n/2)}
 return r;
};
const zeros=(r,c)=>Array.from({length:r},()=>Array(c).fill(0));
const mprod=(A,B)=>A.map(row=>B[0].map((_,j)=>
  md(row.reduce((v,x,k)=>v+x*B[k][j],0))));
const madd=(A,B,sgn=1)=>A.map((row,i)=>row.map((x,j)=>
  md(x+sgn*B[i][j])));
const applied=(A,v)=>A.map(row=>md(row.reduce((s,x,i)=>s+x*v[i],0)));
function particular(A,rhs){
 const m=A.length,n=A[0].length,Q=A.map((row,i)=>[...row,md(rhs[i])]);
 let rank=0,piv=[];
 for(let col=0;col<n&&rank<m;col++){
  let p=rank;while(p<m&&!Q[p][col])p++;
  if(p===m)continue;[Q[p],Q[rank]]=[Q[rank],Q[p]];
  let factor=inv(Q[rank][col]);
  for(let j=col;j<=n;j++)Q[rank][j]=mul(Q[rank][j],factor);
  for(let i=0;i<m;i++)if(i!==rank){
   let f=Q[i][col];
   if(f)for(let j=col;j<=n;j++)Q[i][j]=sub(Q[i][j],mul(f,Q[rank][j]));
  }
  piv.push(col);rank++;
 }
 for(let i=rank;i<m;i++)if(Q[i][n])return {possible:false,rank,augRank:rank+1};
 let x=Array(n).fill(0);for(let i=0;i<rank;i++)x[piv[i]]=Q[i][n];
 if(applied(A,x).some((v,i)=>v!==md(rhs[i])))throw Error("internal elimination failure");
 return {possible:true,rank,x};
}
function schurTaylor(k){
 const M=Array.from({length:4},(_,j)=>flatTaylorBlocks(k,j));
 const X=[];
 for(let order=0;order<=3;order++){
  let rhs=M[order].B.map(row=>row.slice());
  for(let d=1;d<=order;d++)rhs=madd(rhs,mprod(M[d].L,X[order-d]),-1);
  const q=gauss(M[0].L,rhs);
  if(q.rank!==24)throw Error("flat Cartan singular");
  X.push(q.solution);
 }
 const S=[];
 for(let order=2;order<=4;order++){
  let B=zeros(16,16);
  for(let d=1;d<order;d++)B=madd(B,mprod(M[d].C,X[order-d]),-1);
  S.push(B);
 }
 return S;
}
function transversePolarizations(k){
 const [ku,kv,kx,ky]=k;
 if(!ku)throw Error("need nonzero first null component");
 if(2*ku*kv!==kx*kx+ky*ky)throw Error("ray is not Minkowski null");
 const U=[0,mul(md(kx),inv(md(ku))),1,0],
       V=[0,mul(md(ky),inv(md(ku))),0,1],
       eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
 const out=[Array(16).fill(0),Array(16).fill(0)];
 for(let a=0;a<4;a++)for(let mu=0;mu<4;mu++){
   let p=0,c=0;
   for(let nu=0;nu<4;nu++){
     p=add(p,mul(md(eta[a][nu]),sub(mul(U[nu],U[mu]),mul(V[nu],V[mu]))));
     c=add(c,mul(md(eta[a][nu]),add(mul(U[nu],V[mu]),mul(V[nu],U[mu]))));
   }
   out[0][4*a+mu]=mul(p,inv(2));
   out[1][4*a+mu]=mul(c,inv(2));
 }
 return out;
}
function oneRay(k){
 const [S2,S3,S4]=schurTaylor(k);
 if(gauss(S2).rank!==4)throw Error("continuum principal null rank is not4: "+k);
 const u=schurTaylor(k.map((v,i)=>v+(i===1?1:0)))[0];
 const v=schurTaylor(k.map((w,i)=>w-(i===1?1:0)))[0];
 const derivative=madd(u,v,-1).map(row=>row.map(x=>mul(x,inv(2))));
 const waves=transversePolarizations(k),out=[];
 for(let j=0;j<2;j++){
  const e=waves[j],q2=applied(S2,e),q3=applied(S3,e);
  if(q2.some(x=>x))throw Error("TT not principal-null "+k+"/"+j);
  const c1=particular(S2,q3.map(x=>md(-x)));
  if(!c1.possible)throw Error("cubic TT obstruction "+k+"/"+j);
  const S3c=applied(S3,c1.x),
    rhs=applied(S4,e).map((x,i)=>add(x,S3c[i])),
    dv=applied(derivative,e),
    augmented=S2.map((row,i)=>[...row,dv[i]]),
    c2=particular(augmented,rhs.map(x=>md(-x)));
  if(!c2.possible||gauss(augmented).rank!==5)
    throw Error("quartic dispersion/corrector obstruction "+k+"/"+j);
  out.push({polarization:j?"cross":"plus",
    gamma_mod_p:c2.x[16],
    gamma_unique:true,cubic_source_zero:q3.every(x=>x===0)});
 }
 if(out[0].gamma_mod_p!==out[1].gamma_mod_p)
  throw Error("finite oblique polarization splitting at "+k);
 return {k,plus:out[0],cross:out[1]};
}
function audit(){
 const rays=[
  [[1,2,2,0],-1/2],[[1,4,2,2],-1],[[1,5,1,3],-2],
  [[1,5,3,1],-2],[[2,1,2,0],1/4],[[2,2,2,2],0],
  [[2,5,2,4],-3/4],[[1,8,4,0],-2],
  [[2,4,4,0],-4],[[2,8,4,4],-8]
 ];
 const result=rays.map(([k,expected])=>{
   let test=oneRay(k);
   const exact=mul(md(expected*4),inv(4));
   if(test.plus.gamma_mod_p!==exact)
    throw Error("unexpected directional dispersion at "+k+": "+test.plus.gamma_mod_p+" expected "+exact);
   return {...test,gamma_rational:expected};
 });
 return {status:"PASS_10_EXACT_MODULAR_OBLIQUE_TT_DIRECTIONAL_JETS",
   prime,
   source:"original full40 6 based plaquettes; exact binomial Taylor of L/B/C",
   two_polarizations_agree_at_every_checked_ray:true,
   spatial_direction_dependence:true,
   total_rays:result.length,
   rays:result,
   limitations:"Not universal dispersion law, global finite characteristic variety, nonlinear GR solution or full native Book cost."};
}
module.exports={audit,oneRay,schurTaylor};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
