#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL Lorentz-star 6 based plaquettes and proper-Lorentz 24 link rows.
 *
 * Exactly derives the flat link-linear source L, including BOTH based
 * adjacent faces and original D[(P-P^-1)/2]. Verifies:
 *  - L on spatially homogeneous coefficients equals the actual 24x24
 *    rational Hessian M in all 576 entries.
 *  - M^4-5 M^2+4I=0 and M^-1=(5M-M^3)/4 exactly.
 *  - N=L-M lowers polynomial degree for checked vector monomials.
 *
 * The proof of arbitrary-degree polynomial invertibility is structural:
 * translations minus identity strictly lower degree in characteristic 0.
 * The finite Neumann inverse terminates after d+1 terms on P_d.
 * This is an interior/unwrapped polynomial result, not a boundary-collar,
 * periodic root, source-selection or physical GR closure.
 */
const n=4,I=Array.from({length:n},(_,i)=>
  Array.from({length:n},(_,j)=>+(i===j)));
const Z=()=>Array.from({length:n},()=>Array(n).fill(0));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const prs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const E=(a,b)=>I.map((row,i)=>row.map((_,j)=>+(i===a&&j===b)));
const add=(A,B)=>A.map((row,i)=>row.map((v,j)=>v+B[i][j]));
const sub=(A,B)=>A.map((row,i)=>row.map((v,j)=>v-B[i][j]));
const sc=(A,k)=>A.map(row=>row.map(v=>v*k));
const mul=(A,B)=>A.map((row,i)=>
  row.map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const G=prs.map(([i,j])=>mul(sub(E(i,j),E(j,i)),eta));
const levi=(a,b,c,d)=>{
  const v=[a,b,c,d];if(new Set(v).size!==4)return 0;
  let sign=1;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)
    if(v[i]>v[j])sign=-sign;
  return sign;
};
const pair=(u,v,R)=>{
  const C=mul(R,eta);let ans=0;
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
    const [c,d]=[0,1,2,3].filter(t=>t!==a&&t!==b);
    ans+=levi(a,b,c,d)*(+(a===u&&b===v)-+(b===u&&a===v))*C[c][d];
  }
  return ans;
};
function constantM(){
  const M=Array.from({length:24},()=>Array(24).fill(0));
  for(let [r,s] of prs){
    const [u,v]=[0,1,2,3].filter(t=>t!==r&&t!==s);
    const sign=levi(r,s,u,v);
    for(let j=0;j<6;j++)for(let k=0;k<6;k++){
      const val=sign*pair(u,v,sub(mul(G[j],G[k]),mul(G[k],G[j])));
      M[6*r+j][6*s+k]=val;
      M[6*s+k][6*r+j]=val;
    }
  }
  return M;
}
const shift=(p,dir,t=1)=>p.map((v,i)=>i===dir?v+t:v);
function linearLink(point,field){
  const rows=Array(24).fill(0);
  for(let axis=0;axis<4;axis++)for(let j=0;j<6;j++){
    let sum=0,X=G[j];
    for(let [r,t] of prs){
      if(axis!==r&&axis!==t)continue;
      const other=axis===r?t:r;
      const [u,v]=[0,1,2,3].filter(i=>i!==r&&i!==t);
      const sign=levi(r,t,u,v);
      // The two ACTUAL based plaquettes containing this link.
      for(let base of [point,shift(point,other,-1)]){
        const edges=[
          [base,r,1],[shift(base,r),t,1],
          [shift(base,t),r,-1],[base,t,-1]
        ];
        const W1=edges.map(([p,dir,sgn])=>sc(field(p,dir),sgn));
        const P1=W1.reduce(add,Z());
        let dP0=Z(),dP1=Z();
        for(let k=0;k<4;k++){
          const [q,dir,sgn]=edges[k];
          if(dir!==axis||!q.every((v,i)=>v===point[i]))continue;
          const d0=sc(X,sgn);
          // forward variation X U, backward -U^-1 X.
          const d1=sgn===1?mul(X,field(q,dir)):mul(field(q,dir),X);
          dP0=add(dP0,d0);
          let temp=d1;
          for(let l=0;l<k;l++)temp=add(temp,mul(W1[l],d0));
          for(let l=k+1;l<4;l++)temp=add(temp,mul(d0,W1[l]));
          dP1=add(dP1,temp);
        }
        // D((P-P^-1)/2)[delta P] = (delta P + P^-1 delta P P^-1)/2.
        const dR1=sub(dP1,sc(add(mul(P1,dP0),mul(dP0,P1)),.5));
        sum+=sign*pair(u,v,dR1);
      }
    }
    rows[6*axis+j]=sum;
  }
  return rows;
}
function assert(ok,message){if(!ok)throw Error(message)}
function check(){
 const M=constantM();
 for(let k=0;k<24;k++){
   const field=(point,axis)=>axis===Math.floor(k/6)?G[k%6]:Z();
   const result=linearLink([0,0,0,0],field);
   for(let i=0;i<24;i++)assert(result[i]===M[i][k],
     "constant Cartan Hessian mismatch at "+i+","+k);
 }
 const M2=mul(M,M),M4=mul(M2,M2);
 for(let i=0;i<24;i++)for(let j=0;j<24;j++){
   assert(M4[i][j]-5*M2[i][j]+4*+(i===j)===0,
      "M quartic minimal polynomial failed");
   assert((5*M2[i][j]-M4[i][j])/4===+(i===j),
      "M explicit inverse failed");
 }
 const tests=[];
 const choose=(n,k)=>{
   let a=1;for(let i=1;i<=k;i++)a=a*(n-i+1)/i;return a;
 };
 for(let d=1;d<=4;d++){
   for(let k of [0,4,8,12,15,20,23]){
     const field=(point,axis)=>axis===Math.floor(k/6)?
       sc(G[k%6],(point[2]+2*point[3])**d):Z();
     for(let [dx,dy] of [[1,0],[0,1],[1,1],[1,2],[2,1]]){
       let sum=Array(24).fill(0);
       for(let t=0;t<=d;t++){
         let q=[0,0,dx*t,dy*t],val=linearLink(q,field);
         const scalar=(q[2]+2*q[3])**d;
         let sign=(-1)**(d-t)*choose(d,t);
         sum=sum.map((v,i)=>v+sign*(val[i]-M[i][k]*scalar));
       }
       assert(sum.every(v=>v===0),
        "L-M failed to lower polynomial degree: "+d+"/"+k+"/"+dx+","+dy);
       tests.push(1);
     }
   }
 }
 return {
  status:"PASS_EXACT_POLYNOMIAL_CARTAN_INVERSE",
  constant_hessian_entries_tested:576,
  matrix_polynomial:"M^4-5*M^2+4*I=0",
  explicit_inverse:"M^-1=(5*M-M^3)/4",
  degree_lowering_tests:tests.length,
  all_d_less_equal_4:true,
  polynomial_inverse:"(M+N)^-1=sum_(j=0)^d (-M^-1 N)^j M^-1 on polynomial degree <=d",
  scope:"original flat link-linear Euler on unwrapped interior polynomial carrier; no general boundary inverse, full nonlinear exact root, or native GR price"
 };
}
module.exports={check};
if(require.main===module)console.log(JSON.stringify(check(),null,2));
