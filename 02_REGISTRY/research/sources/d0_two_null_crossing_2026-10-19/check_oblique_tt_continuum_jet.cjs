#!/usr/bin/env node
"use strict";
/* Exact modular Taylor expansion around z=(1+t,(1+t)^2,(1+t)^2,1)
 * of the original flat 40 Euler -> 16 Schur symbol.
 *
 * Reconstruct true Laurent L,B,C using F1009 16th-root Fourier sampling
 * and verify reconstruction at an independent rational value w=2.
 * Take the ring F1009[t]/(t^5), invert actual L0=24x24, and compute
 * all 16x16 S_j through j=4 without unstable finite differences.
 * The gravitational null covector (1,2,2,0) is not axis aligned.
 *
 * This is an exact FIELD-MODULAR witness for specified k, NOT
 * a full rational analytic proof for arbitrary Lorentz-null k.
 */
const {matrices,gauss,prime}=require("./check_full40_schur_rank_modular.cjs");
const mod=x=>((x%prime)+prime)%prime;
const times=(a,b)=>mod(a*b),sum=(a,b)=>mod(a+b),minus=(a,b)=>mod(a-b);
const power=(a,n)=>{
  if(n<0)return power(inverse(a),-n);
  let v=1,b=mod(a),k=n;
  while(k){if(k&1)v=times(v,b);b=times(b,b);k=Math.floor(k/2)}return v;
};
const inverse=a=>{if(!mod(a))throw Error("noninvertible");return power(a,prime-2)};
const zeros=(m,n)=>Array.from({length:m},()=>Array(n).fill(0));
const multiply=(A,B)=>A.map(r=>B[0].map((_,j)=>
  mod(r.reduce((v,x,k)=>v+x*B[k][j],0))));
const applied=(A,v)=>A.map(row=>mod(row.reduce((s,x,i)=>s+x*v[i],0)));
const rank=A=>gauss(A).rank;
const addMatrix=(A,B,sgn=1)=>A.map((row,i)=>row.map((v,j)=>
  mod(v+sgn*B[i][j])));
function solve(M,v){
  const rows=M.length,cols=M[0].length,A=M.map((row,i)=>[...row,mod(v[i])]);
  let r=0,pivots=[];
  for(let j=0;j<cols&&r<rows;j++){
    let p=r;while(p<rows&&!A[p][j])p++;
    if(p===rows)continue;[A[r],A[p]]=[A[p],A[r]];
    let invp=inverse(A[r][j]);for(let k=j;k<=cols;k++)A[r][k]=times(A[r][k],invp);
    for(let i=0;i<rows;i++)if(i!==r){
      const f=A[i][j];
      if(f)for(let k=j;k<=cols;k++)A[i][k]=minus(A[i][k],times(f,A[r][k]));
    }
    pivots.push(j);r++;
  }
  for(let i=r;i<rows;i++)if(A[i][cols])return {possible:false,rank:r,augRank:r+1};
  let x=Array(cols).fill(0);for(let i=0;i<r;i++)x[pivots[i]]=A[i][cols];
  if(applied(M,x).some((v,i)=>v!==mod(v[i])))throw Error("solution verification");
  return {possible:true,x,rank:r};
}
function choose(m,n){let v=1;for(let i=0;i<n;i++)v=times(v,times(mod(m-i),inverse(i+1)));return v;}
function coefficientSeries(){
 const N=16,D=4;let omega=0;
 for(let w=2;w<prime;w++)if(power(w,N)===1&&power(w,N/2)!==1){omega=w;break;}
 if(!omega)throw Error("no primitive 16th root");
 const samples=Array.from({length:N},(_,j)=>{
   let w=power(omega,j);return matrices([w,power(w,2),power(w,2),1]);
 });
 const shape={L:[24,24],B:[24,16],C:[16,24]};
 function coeff(type){
   const [m,n]=shape[type],out=Array.from({length:N},()=>zeros(m,n));
   for(let k=0;k<N;k++){
     const exp=k<=8?k:k-N;
     for(let j=0;j<N;j++){
       const c=times(inverse(N),power(omega,-exp*j)),T=samples[j][type];
       for(let a=0;a<m;a++)for(let b=0;b<n;b++)
         out[k][a][b]=sum(out[k][a][b],times(c,T[a][b]));
     }
   }
   const independently=matrices([2,4,4,1])[type];
   for(let a=0;a<m;a++)for(let b=0;b<n;b++){
     let v=0;for(let k=0;k<N;k++){
       const ex=k<=8?k:k-N;
       v=sum(v,times(out[k][a][b],power(2,ex)));
     }
     if(v!==independently[a][b])throw Error("Laurent alias "+type+" "+a+","+b);
   }
   return out;
 }
 const base=Object.fromEntries(["L","B","C"].map(type=>[type,coeff(type)]));
 function expand(type){
   const [m,n]=shape[type],out=Array.from({length:D+1},()=>zeros(m,n));
   for(let order=0;order<=D;order++)for(let k=0;k<N;k++){
     const e=k<=8?k:k-N,v=choose(e,order);
     for(let a=0;a<m;a++)for(let b=0;b<n;b++)
       out[order][a][b]=sum(out[order][a][b],times(v,base[type][k][a][b]));
   }
   return out;
 }
 const L=expand("L"),B=expand("B"),C=expand("C");
 const X=[],S=[];
 for(let d=0;d<=D;d++){
   let RHS=B[d].map(r=>r.slice());
   for(let j=1;j<=d;j++)RHS=addMatrix(RHS,multiply(L[j],X[d-j]),-1);
   const result=gauss(L[0],RHS);
   if(result.rank!==24)throw Error("flat L0 singular");
   X.push(result.solution);
 }
 for(let d=0;d<=D;d++){
   let V=zeros(16,16);
   for(let j=0;j<=d;j++)V=addMatrix(V,multiply(C[j],X[d-j]),-1);
   S.push(V);
 }
 return {omega,S,L,B,C,rankS:S.map(rank)};
}
function TT(){
 const A=[0,2,1,0],V=[0,0,0,1],
   eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
 const t=Array.from({length:2},()=>Array(16).fill(0));
 for(let a=0;a<4;a++)for(let mu=0;mu<4;mu++){
   let plus=0,cross=0;
   for(let nu=0;nu<4;nu++){
     plus+=eta[a][nu]*(A[nu]*A[mu]-V[nu]*V[mu]);
     cross+=eta[a][nu]*(A[nu]*V[mu]+V[nu]*A[mu]);
   }
   t[0][4*a+mu]=times(mod(plus),inverse(2));
   t[1][4*a+mu]=times(mod(cross),inverse(2));
 }
 return t;
}
function audit(){
 const {omega,S,rankS}=coefficientSeries();
 if(rankS[0]!==0||rankS[1]!==0||rankS[2]!==4)
   throw Error("wrong continuum null principal symbol");
 const pol=TT(),out=[];
 for(let j=0;j<2;j++){
   const v=pol[j],y2=applied(S[2],v),y3=applied(S[3],v);
   if(y2.some(x=>x))throw Error("TT not null at order2");
   let e1=solve(S[2],y3.map(x=>mod(-x)));
   if(!e1.possible)throw Error("unremovable cubic TT defect");
   let y4=applied(S[4],v).map((x,i)=>sum(x,applied(S[3],e1.x)[i]));
   const e2=solve(S[2],y4.map(x=>mod(-x)));
   out.push({polarization:j===0?"plus":"cross",S2_zero:true,
     S3_zero:y3.every(x=>x===0),
     cubic_removed:e1.possible,corrector:e1.x.map((x,i)=>x?{i,v:x}:null).filter(Boolean),
     quartic_removed_by_polarization_alone:e2.possible,
     quartic_aug_rank:e2.augRank||e2.rank,
     quartic_source:y4.map((x,i)=>x?{i,v:x}:null).filter(Boolean)});
 }
 return {status:"PASS_EXACT_MODULAR_OBLIQUE_TT_CONTINUUM_JET",
   prime,omega,rankS,ray:[1,2,2,0],fullSchurS2_rank4:true,
   results:out,scope:"Exact F1009 Taylor coefficients on one oblique Minkowski-null ray; not a characteristic polynomial, rational proof for every wavevector, or physical native GR"};
}
module.exports={audit,coefficientSeries};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
