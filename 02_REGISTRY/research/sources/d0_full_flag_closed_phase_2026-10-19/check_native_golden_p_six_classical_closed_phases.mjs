#!/usr/bin/env node
"use strict";
/* Exact ORIGINAL six proper Lorentz directions from SIX scalar closed
 * phase comparisons on TWO original CAR16 grade-one input preparations.
 * Flags are 100% GOOD/BAD DEPHASED; all BAD outcomes are retained.
 * The four fixed CAR anchor projectors are ordinary, known one-body
 * operator expressions; no interhistory quantum interferometer needed.
 * This proves mathematical readout rank, NOT compulsory Book selection.
 */
const p=(Math.sqrt(5)-1)/2, lp=Math.log(1/p);
const I=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const Z=n=>I(n).map(r=>r.map(()=>0));
const E=(i,j)=>{let M=Z(4);M[i][j]=1;return M};
const add=(A,B,s=1)=>A.map((r,i)=>r.map((v,j)=>v+s*B[i][j]));
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const trans=M=>M.map((r,i)=>r.map((_,j)=>M[j][i]));
const mv=(M,v)=>M.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));
const dot=(a,b)=>a.reduce((s,v,j)=>s+v*b[j],0);
const test=(v,m)=>{if(!v)throw Error("FAIL "+m);console.log("PASS "+m)};
const generators=[add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)];
const mulC=(u,v)=>[u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]];
const inner=(u,v)=>u.r.reduce((s,x,j)=>{
 let w=mulC([x,-u.i[j]],[v.r[j],v.i[j]]);
 return [s[0]+w[0],s[1]+w[1]];
},[0,0]);
const matApply=(M,v)=>({r:mv(M,v.r),i:mv(M,v.i)});
const probes=[
 {name:"plus",v:{r:[1,0,1,0],i:[0,0,0,1]},
  labels:["e0","e2","e0+i e1"]},
 {name:"minus",v:{r:[0,1,1,0],i:[0,0,0,1]},
  labels:["e1","e0+i e1","e1+i e2"]}
];
const anchors={
 "e0":{r:[1,0,0,0],i:[0,0,0,0]},
 "e2":{r:[0,0,1,0],i:[0,0,0,0]},
 "e1":{r:[0,1,0,0],i:[0,0,0,0]},
 "e0+i e1":{r:[1,0,0,0],i:[0,1,0,0]},
 "e1+i e2":{r:[0,1,0,0],i:[0,0,1,0]}
};
// The true primitive Golden rather than mathematical 1/2 Julia source.
// qG=p², qB=p=1-p²; p³+1=2p, so the EXACT normalized
// closed-phase first source is (p²/2)*g - (1/4)*s where
// g=d arg GOOD and s=d arg for symmetric Lorentz X+X†.
function originalGoodBadJet(v,w){
 const c=inner(v,w),c2=c[0]**2+c[1]**2;
 test(c2>0&&inner(v,v)[0]===3,"native Golden input and CAR anchor have overlap");
 return generators.map(X=>{
  const xv=matApply(X,v),h=matApply(add(X,trans(X)),v);
  const vX=inner(v,xv),xw=inner(xv,w),hw=inner(h,w);
  const ix=(c[0]*xw[1]-c[1]*xw[0]);
  const iy=(c[0]*hw[1]-c[1]*hw[0]);
  const G12=4*vX[1]+12*ix/c2;
  const S12=12*iy/c2;
  test(Number.isInteger(G12)&&Number.isInteger(S12),
       "original Golden closed-phase Good and BAD exact integer jet");
  return [G12,S12];
 });
}
const allPairs=probes.flatMap(t=>t.labels.map(a=>originalGoodBadJet(t.v,anchors[a])));
const G12=allPairs.map(row=>row.map(x=>x[0])),S12=allPairs.map(row=>row.map(x=>x[1]));
const wantG=[[0,-4,0,-8,8,0],[0,-4,0,4,-4,0],
 [12,-4,0,-8,8,0],[0,-8,0,-4,8,0],
 [0,-8,-12,-4,8,0],[-6,-2,6,-4,2,-6]];
const wantS=[[0,-12,0,-12,0,0],[0,0,0,0,0,0],
 [12,-12,12,-12,0,0],[0,-12,0,-12,0,0],
 [-12,-12,-12,-12,0,0],[0,-6,0,-6,0,-12]];
test(JSON.stringify(G12)===JSON.stringify(wantG) &&
 JSON.stringify(S12)===JSON.stringify(wantS),
 "ALL SIX primitive original Golden GOOD/BAD exact angular rows");
const Ar=G12.map((row,i)=>row.map((v,j)=>2*v-S12[i][j]));
const Br=G12.map(row=>row.map(v=>-2*v));
const rows=Ar.map((row,i)=>row.map((v,j)=>(v+Br[i][j]*p)/48));
// ring Z[p], p²=1-p with exact integer BigInt coefficient pairs.
const padd=(x,y)=>[x[0]+y[0],x[1]+y[1]];
const pmult=(x,y)=>[x[0]*y[0]+x[1]*y[1],
 x[0]*y[1]+x[1]*y[0]-x[1]*y[1]];
let ring=[0n,0n],terms=0;
function permutation(k,mask,v,sgn){
 if(k===6){ring=padd(ring,v.map(x=>sgn*x));terms++;return;}
 for(let j=0;j<6;j++)if(!(mask&(1<<j))){
  let inversions=0;for(let m=j+1;m<6;m++)if(mask&(1<<m))inversions++;
  permutation(k+1,mask|(1<<j),
    pmult(v,[BigInt(Ar[k][j]),BigInt(Br[k][j])]),
    sgn*(inversions%2?-1n:1n));
 }
}
permutation(0,0,[1n,0n],1n);
test(terms===720&&ring[0]===-222953472n&&ring[1]===360972288n,
 "EXACT golden Q(sqrt5) six-readout determinant integer polynomial");
test(Math.abs((Number(ring[0])+Number(ring[1])*p)/(48**6)-p**9/1152)<1e-17,
 "EXACT symbolic native Golden six-closed-phase determinant p^9/1152");
function det(A){
 const n=A.length,M=A.map(r=>r.map(BigInt));let den=1n,sig=1n;
 for(let k=0;k<n-1;k++){
  let p=k;while(p<n&&M[p][k]===0n)p++;
  if(p===n)return 0n;
  if(p!==k){[M[k],M[p]]=[M[p],M[k]];sig=-sig;}
  const d=M[k][k];
  for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++)
   M[i][j]=(M[i][j]*d-M[i][k]*M[k][j])/den;
  for(let i=k+1;i<n;i++)M[i][k]=0n;
  den=d;
 }
 return sig*M[n-1][n-1];
}
const nativeDet=(Number(ring[0])+Number(ring[1])*p)/(48**6);
test(nativeDet>0&&Math.abs(nativeDet-0.000011419806854535459)<2e-16,
 "full native Golden six-phase source invertible, no arbitrary Julia 1/2");
test(Math.abs(34*p-21-p**9)<1e-13,
 "native GOLDEN determinant simplifies EXACTLY by p²=1-p to p^9/1152");

function inverse(A){
 let n=A.length,M=A.map((r,i)=>[...r,...I(n)[i]]);
 for(let j=0;j<n;j++){
  let p=j;for(let k=j+1;k<n;k++)if(Math.abs(M[k][j])>Math.abs(M[p][j]))p=k;
  [M[p],M[j]]=[M[j],M[p]];
  let d=M[j][j];for(let k=j;k<2*n;k++)M[j][k]/=d;
  for(let k=0;k<n;k++)if(k!==j){let d=M[k][j];for(let a=j;a<2*n;a++)M[k][a]-=d*M[j][a]}
 }
 return M.map(r=>r.slice(n));
}
function sqrtSPD(A){
 let X=I(4);
 for(let k=0;k<35;k++){
  X=add(X,mul(A,inverse(X))).map(r=>r.map(v=>v/2));
  let delta=Math.max(...mul(X,X).flatMap((r,i)=>r.map((x,j)=>Math.abs(x-A[i][j]))));
  if(delta<1e-14)break;
 }
 return X;
}
function expm(X,h){
 let out=I(4),term=I(4);
 for(let k=1;k<=12;k++){
  term=mul(term,X).map(r=>r.map(x=>x*h/k));
  out=add(out,term);
 }
 return out;
}
const normalize=x=>{let n=Math.sqrt(inner(x,x)[0]);return {r:x.r.map(v=>v/n),i:x.i.map(v=>v/n)}};
function full(x,M,h){
 const u=normalize(x),T=expm(M,h).map(r=>r.map(v=>v*p));
 const F=sqrtSPD(add(I(4),mul(trans(T),T),-1));
 return {g:matApply(T,u),b:matApply(F,u)};
}
const ketDensity=x=>x.r.map((_,i)=>x.r.map((_,j)=>[
 x.r[i]*x.r[j]+x.i[i]*x.i[j],
 x.i[i]*x.r[j]-x.r[i]*x.i[j]]));
const cmatrix=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>{
 const t=mulC(v,B[k][j]);return [s[0]+t[0],s[1]+t[1]];
},[0,0])));
const cyclic=(A,B,C)=>cmatrix(cmatrix(A,B),C).reduce((s,row,i)=>
 [s[0]+row[i][0],s[1]+row[i][1]],[0,0]);
function scalarPhase(p,anchor,X,h){
 const x=full(p,X,0),y=full(p,X,h),c=full(anchor,X,0);
 const g=cyclic(ketDensity(x.g),ketDensity(y.g),ketDensity(c.g));
 const b=cyclic(ketDensity(x.b),ketDensity(y.b),ketDensity(c.b));
 return Math.atan2(g[1]+b[1],g[0]+b[0]);
}
let maxErr=0;
let q=0;
for(const p of probes)for(const label of p.labels){
 const v=anchors[label];
 for(let j=0;j<6;j++){
  const h=.0002;
  const slope=(scalarPhase(p.v,v,generators[j],h)-
               scalarPhase(p.v,v,generators[j],-h))/(2*h);
  const expected=rows[q][j];
  maxErr=Math.max(maxErr,Math.abs(slope-expected));
  test(Math.abs(slope-expected)<3e-7,
       "direct full positive Julia+BAD density CLOSED PHASE finite-jet "+p.name+"/"+label+"/"+j);
 }
 q++;
}
test(maxErr<3e-7,
     "full six relative phase readout independent direct 4x4 positive Julia output confirmation");
console.log(JSON.stringify({
 original:"same full CAR16 grade-one Golden p Julia with dephased GOOD/BAD and two independent recorded probes",
 phase_anchor_labels:probes.map(p=>p.labels),
 six_by_six_value:rows,exact_determinant:'p^9/1152',
 exact_ring_det_coefficients:ring.map(String),
 normalized_det:nativeDet,
 max_full_Julia_finite_source_error:maxErr,
 flags_classical:true,missing_book_selection:true,GR_closed:false
},null,2));
