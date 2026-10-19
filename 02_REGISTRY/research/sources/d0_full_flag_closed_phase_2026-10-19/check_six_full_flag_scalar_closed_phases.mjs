#!/usr/bin/env node
"use strict";
/* Exact ORIGINAL six proper Lorentz directions from SIX scalar closed
 * phase comparisons on TWO original CAR16 grade-one input preparations.
 * Flags are 100% GOOD/BAD DEPHASED; all BAD outcomes are retained.
 * The four fixed CAR anchor projectors are ordinary, known one-body
 * operator expressions; no interhistory quantum interferometer needed.
 * This proves mathematical readout rank, NOT compulsory Book selection.
 */
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
function exact336Row(v,w){
 const c=inner(v,w),c2=c[0]**2+c[1]**2;
 test(c2>0&&inner(v,v)[0]===3,
      "original two-line input & CAR anchor have positive overlap");
 return generators.map(X=>{
  const xv=matApply(X,v),h=matApply(add(X,trans(X)),v);
  const vX=inner(v,xv),xw=inner(xv,w),hw=inner(h,w);
  const imcx=(c[0]*xw[1]-c[1]*xw[0]);
  const imch=(c[0]*hw[1]-c[1]*hw[0]);
  const scaled=4*vX[1]+(12*imcx-54*imch)/c2;
  test(Number.isInteger(scaled),
       "exact 336-scaled full GOOD/BAD closed-phase derivative integer");
  return scaled;
 });
}
const rows=probes.flatMap(p=>p.labels.map(label=>exact336Row(p.v,anchors[label])));
const target=[
 [0,50,0,46,8,0],[0,-4,0,4,-4,0],
 [-42,50,-54,46,8,0],[0,46,0,50,8,0],
 [54,46,42,50,8,0],[-6,25,6,23,2,48]
];
test(JSON.stringify(rows)===JSON.stringify(target),
     "all SIX original full-flag closed-phase gradient rows EXACT at 1/336 scale");
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
const rawdet=det(rows);
test(rawdet===84934656n,"exact full SIX original closed-phase scalar-detector integer determinant");
test(Number(rawdet)/336**6>5.9e-8&&Number(rawdet)/336**6<5.91e-8,
     "two independent original CAR histories recover six-Lorentz link directions");

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
 const u=normalize(x),T=expm(M,h).map(r=>r.map(v=>v/2));
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
  const expected=rows[q][j]/336;
  maxErr=Math.max(maxErr,Math.abs(slope-expected));
  test(Math.abs(slope-expected)<3e-7,
       "direct full positive Julia+BAD density CLOSED PHASE finite-jet "+p.name+"/"+label+"/"+j);
 }
 q++;
}
test(maxErr<3e-7,
     "full six relative phase readout independent direct 4x4 positive Julia output confirmation");
console.log(JSON.stringify({
 original:"same full CAR16 grade-one Julia with dephased GOOD/BAD and two independent recorded probes",
 phase_anchor_labels:probes.map(p=>p.labels),
 six_by_six_numerator:rows,common_denominator:336,
 exact_integer_det:rawdet.toString(),
 normalized_det:Number(rawdet)/336**6,
 max_full_Julia_finite_source_error:maxErr,
 flags_classical:true,missing_book_selection:true,GR_closed:false
},null,2));
