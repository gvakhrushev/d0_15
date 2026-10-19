#!/usr/bin/env node
"use strict";
/*
 * EXACT F_1009 evaluation of the ORIGINAL SIX-BASED star action's
 * 40 independent flat Euler matrix in the original eta null frame.
 *
 * Computes L=dE_link/d(24 link), B=dE_link/d(16 e),
 * C=dE_e/d(24 link) directly from all based plaquettes + both adjacent
 * faces, forms S=-C L^-1 B, and checks exact 10-dimension kernel:
 * six local Lorentz frame vectors + four backward Role gradients.
 * Also checks exact Laurent variational adjoint S(z)^T=S(z^-1).
 *
 * This is a generic algebraic-rank proof from: exact analytic Ward
 * (10 right kernels) and ONE modular exact rank6 witness over F_1009.
 * It does NOT prove physical native Book action selection, nonflat
 * all-order root, or finite Fourier-mode dispersion on every torus.
 */
const prime=1009,n=4;
const md=x=>((x%prime)+prime)%prime;
const addn=(a,b)=>md(a+b),subn=(a,b)=>md(a-b),muln=(a,b)=>md(a*b);
function pow(a,k){
  let r=1,q=md(a),t=k;
  if(k<0)return pow(inv(q),-k);
  while(t>0){if(t%2)r=muln(r,q);q=muln(q,q);t=Math.floor(t/2)}return r;
}
const inv=a=>{a=md(a);if(a===0)throw Error("division by zero");return pow(a,prime-2)};
const I=()=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const O=()=>Array.from({length:n},()=>Array(n).fill(0));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,prime-1,0],[0,0,0,prime-1]];
const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const E=(a,b)=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(a===i&&b===j)));
const add=(A,B)=>A.map((row,i)=>row.map((v,j)=>addn(v,B[i][j])));
const sub=(A,B)=>A.map((row,i)=>row.map((v,j)=>subn(v,B[i][j])));
const sc=(A,k)=>A.map(row=>row.map(v=>muln(v,k)));
const matmul=(A,B)=>A.map((row,i)=>row.map((_,j)=>md(row.reduce((sum,v,k)=>sum+v*B[k][j],0))));
const gens=pairs.map(([i,j])=>matmul(sub(E(i,j),E(j,i)),eta));
const sign=(a,b,c,d)=>{
  let v=[a,b,c,d];if(new Set(v).size<4)return 0;
  let s=1;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)if(v[i]>v[j])s=-s;return md(s);
};
function pair(F,u,v,R){
  const A=matmul(R,eta);let result=0;
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
    const [c,d]=[0,1,2,3].filter(k=>k!==a&&k!==b);
    let area=subn(muln(F[a][u],F[b][v]),muln(F[b][u],F[a][v]));
    result=addn(result,muln(muln(sign(a,b,c,d),area),A[c][d]));
  }
  return result;
}
function pairCo(a,mu,u,v,R){
  if(mu!==u&&mu!==v)return 0;
  let F=I();for(let b=0;b<4;b++)F[b][mu]=+(a===b);
  return pair(F,u,v,R);
}
const dot=(z,p)=>p.reduce((ans,x,j)=>muln(ans,pow(z[j],x)),1);
const shift=(p,dir,k=1)=>p.map((v,i)=>i===dir?v+k:v);
function linkLinear(z,axis,gindex){
  const pt=[0,0,0,0],out=Array(24).fill(0);
  const field=(p,k)=>k===axis?sc(gens[gindex],dot(z,p)):O();
  for(let dir=0;dir<4;dir++)for(let j=0;j<6;j++){
    let val=0,X=gens[j];
    for(let [r,t] of pairs){
      if(dir!==r&&dir!==t)continue;
      let other=dir===r?t:r,[u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t);
      for(let base of [pt,shift(pt,other,-1)]){
        let edges=[[base,r,1],[shift(base,r),t,1],
                   [shift(base,t),r,-1],[base,t,-1]];
        let W=edges.map(([p,k,sgn])=>sc(field(p,k),sgn));
        let P1=W.reduce(add,O());
        let dP0=O(),dP1=O();
        for(let k=0;k<4;k++){
          let [p,axis,sgn]=edges[k];
          if(axis!==dir||!p.every((x,i)=>x===pt[i]))continue;
          let d0=sc(X,sgn),d1=sgn===1?matmul(X,field(p,axis)):matmul(field(p,axis),X);
          dP0=add(dP0,d0);
          let term=d1;
          for(let i=0;i<k;i++)term=add(term,matmul(W[i],d0));
          for(let i=k+1;i<4;i++)term=add(term,matmul(d0,W[i]));
          dP1=add(dP1,term);
        }
        let dR=sub(dP1,sc(add(matmul(P1,dP0),matmul(dP0,P1)),inv(2)));
        val=addn(val,muln(sign(r,t,u,v),pair(I(),u,v,dR)));
      }
    }
    out[6*dir+j]=val;
  }
  return out;
}
function matrices(z){
  let L=Array.from({length:24},()=>Array(24).fill(0));
  let B=Array.from({length:24},()=>Array(16).fill(0));
  let C=Array.from({length:16},()=>Array(24).fill(0));
  for(let j=0;j<24;j++){
    let r=linkLinear(z,Math.floor(j/6),j%6);
    for(let i=0;i<24;i++)L[i][j]=r[i];
  }
  for(let dir=0;dir<4;dir++)for(let j=0;j<6;j++)for(let [r,t] of pairs){
    if(dir!==r&&dir!==t)continue;
    let other=dir===r?t:r,[u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t);
    let coefficient=muln(muln(sign(r,t,u,v),dir===r?1:-1),
      subn(1,inv(z[other])));
    for(let a=0;a<4;a++)for(let mu=0;mu<4;mu++){
      B[6*dir+j][4*a+mu]=addn(B[6*dir+j][4*a+mu],
        muln(coefficient,pairCo(a,mu,u,v,gens[j])));
    }
  }
  for(let [r,t] of pairs){
    let [u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t);
    for(let dir of [r,t])for(let j=0;j<6;j++){
      let R=sc(gens[j],dir===r?subn(1,z[t]):subn(z[r],1));
      for(let a=0;a<4;a++)for(let mu=0;mu<4;mu++)
        C[4*a+mu][6*dir+j]=addn(C[4*a+mu][6*dir+j],
          muln(sign(r,t,u,v),pairCo(a,mu,u,v,R)));
    }
  }
  return {L,B,C};
}
function gauss(A,extras=[]){
  const m=A.length,n=A[0].length,k=extras.length?extras[0].length:0;
  const Q=A.map((row,i)=>[...row,...(k?extras[i]:[])]);
  let rank=0,piv=[];
  for(let col=0;col<n&&rank<m;col++){
    let row=rank;while(row<m&&Q[row][col]===0)row++;
    if(row===m)continue;
    [Q[rank],Q[row]]=[Q[row],Q[rank]];
    const invPivot=inv(Q[rank][col]);
    for(let j=col;j<n+k;j++)Q[rank][j]=muln(Q[rank][j],invPivot);
    for(let i=0;i<m;i++)if(i!==rank){
      let factor=Q[i][col];
      if(!factor)continue;
      for(let j=col;j<n+k;j++)
        Q[i][j]=subn(Q[i][j],muln(factor,Q[rank][j]));
    }
    piv.push(col);rank++;
  }
  return {rank,piv,solution:k?Q.map(row=>row.slice(n)):null};
}
const multiply=(A,B)=>A.map(row=>B[0].map((_,j)=>md(
  row.reduce((acc,v,k)=>acc+v*B[k][j],0))));
const apply=(A,v)=>A.map(row=>md(row.reduce((s,x,i)=>s+x*v[i],0)));
const Ssymbol=z=>{
  const {L,B,C}=matrices(z),sol=gauss(L,B);
  if(sol.rank!==24)throw Error("singular L at "+z);
  return {L,B,C,S:scFlat(multiply(C,sol.solution),-1)};
};
const scFlat=(A,k)=>A.map(row=>row.map(v=>muln(v,k)));
function audit(){
  const zs=[[2,3,5,7],[2,1,3,5],[2,2,2,2],[2,1,1,1]];
  const out=[];
  for(let z of zs){
    let {L,B,C,S}=Ssymbol(z);
    let back=Ssymbol(z.map(inv));
    for(let i=0;i<16;i++)for(let j=0;j<16;j++)
      if(S[i][j]!==back.S[j][i])
        throw Error("Laurent adjoint failure "+z+" "+i+","+j);
    const ward=[];
    for(let X of gens)ward.push(X.flat());
    for(let a=0;a<4;a++)ward.push(Array.from({length:16},(_,i)=>
      Math.floor(i/4)===a?subn(1,inv(z[i%4])):0));
    for(let j=0;j<ward.length;j++)
      if(apply(S,ward[j]).some(v=>v!==0))
        throw Error("Ward failure "+z+" generator "+j);
    let Bgrad=ward.slice(6);
    for(let v of Bgrad)if(apply(B,v).some(x=>x!==0))
      throw Error("coframe discrete gradient should be in B kernel");
    const mr=gauss(L).rank,wr=gauss(
      Array.from({length:16},(_,i)=>ward.map(w=>w[i]))).rank;
    let sr=gauss(S).rank;
    if(wr!==10 || sr>6 || mr!==24)
      throw Error("unexpected rank "+z+": "+[wr,sr,mr]);
    out.push({z,originalLinkRank:mr,independentSixLorentzFourGradient:wr,
      SchurRank:sr,nullity:16-sr,LaurentAdjoint:true,
      all10RightWard:true,all4BackwardGradientBNull:true});
  }
  if(out[0].SchurRank!==6||out[2].SchurRank!==4)
    throw Error("missing generic rank6 or characteristic rank4 witness");
  return {
    status:"PASS_EXACT_F1009_GENERIC_SCHUR_RANK6_AND_NULL_WARDS",
    prime,identity:"S=-C L^-1 B, S(z)^T=S(z^-1)",
    input:"Original all six based plaquettes and 16+24 variations",
    proof_scope:"Generic Laurent rational rank 6: analytic ten gauge nulls + exact finite-field rank6 witness",
    results:out,
    limitations:"Finite field witness only on chosen z; no general exact characteristic variety equation, physical native Cost/Info, nonlinear complete root or periodic refinement."
  };
}
module.exports={audit,Ssymbol,matrices,gauss,prime};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
