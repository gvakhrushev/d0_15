#!/usr/bin/env node
"use strict";
// ORIGINAL grade-one block of the full CAR16 exterior Lorentz representation.
// Two independent native projective rays, no fitted detector or Book action.
const E=(i,j)=>{let m=Array.from({length:4},()=>Array(4).fill(0));m[i][j]=1;return m};
const plus=(A,B,k=1)=>A.map((row,i)=>row.map((v,j)=>v+k*B[i][j]));
const G=[plus(E(1,2),E(2,0)), plus(E(1,3),E(3,0)),
 plus(E(0,2),E(2,1)), plus(E(0,3),E(3,1)),
 plus(E(2,3),E(3,2),-1),plus(E(1,1),E(0,0),-1)];
const dot=(v,w)=>v.reduce((s,x,j)=>s+x*w[j],0);
const mv=(M,v)=>M.map(row=>dot(row,v));
const check=(v,label)=>{if(!v)throw Error("FAIL "+label);console.log("PASS "+label)};
function horizontalInt(real,imag){
 const n=dot(real,real)+dot(imag,imag);check(n===3,"original single CAR state squared norm 3");
 const columns=G.map(M=>{
  const ar=mv(M,real),ai=mv(M,imag);
  const cr=dot(real,ar)+dot(imag,ai);
  const ci=dot(real,ai)-dot(imag,ar);
  return [...ar.map((v,i)=>n*v-cr*real[i]+ci*imag[i]),
          ...ai.map((v,i)=>n*v-cr*imag[i]-ci*real[i])];
 });
 return Array.from({length:8},(_,i)=>columns.map(c=>c[i]));
}
const Ma=horizontalInt([1,0,1,0],[0,0,0,1]);
const Mb=horizontalInt([0,1,1,0],[0,0,0,1]);
const full=[...Ma,...Mb];
const expectA=[[-1,0,2,0,0,-2],[3,0,0,0,0,0],[2,0,-1,0,0,1],
 [0,2,0,1,-1,0],[0,1,0,2,-2,0],[0,3,0,0,0,0],
 [0,1,0,-1,1,0],[-1,0,-1,0,0,1]];
const expectB=[[0,0,3,0,0,0],[2,0,-1,0,0,2],[-1,0,2,0,0,-1],
 [0,1,0,2,-1,0],[0,0,0,3,0,0],[0,2,0,1,-2,0],
 [0,-1,0,1,1,0],[-1,0,-1,0,0,-1]];
check(JSON.stringify(Ma)===JSON.stringify(expectA)
 &&JSON.stringify(Mb)===JSON.stringify(expectB),
 "complete exact original 8x6 integer projective tangent matrices");
function det(A){
 const n=A.length,a=A.map(r=>r.map(BigInt));let den=1n,sign=1n;
 for(let k=0;k<n-1;k++){
  let piv=k;while(piv<n&&a[piv][k]===0n)piv++;
  if(piv===n)return 0n;
  if(piv!==k){[a[piv],a[k]]=[a[k],a[piv]];sign=-sign;}
  const d=a[k][k];
  for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++)
   a[i][j]=(a[i][j]*d-a[i][k]*a[k][j])/den;
  for(let i=k+1;i<n;i++)a[i][k]=0n;
  den=d;
 }
 return sign*a[n-1][n-1];
}
check(Ma.every(row=>row[5]===-row[2]&&row[4]===-row[3]),
      "first single-ray projective null generators exactly two constraints");
check(Mb.every(row=>row[5]===row[0]&&row[4]===-row[1]),
      "second single-ray projective null generators exactly two different constraints");
function choose(mat,size){
 const out=[];function find(start,r){
  if(r.length===size){const sub=r.map(i=>mat[i]);let d=det(sub.map(x=>x.slice(0,size)));if(d!==0n)out.push({r:r.slice(),d:d.toString()});return;}
  for(let i=start;i<=mat.length-(size-r.length);i++)find(i+1,[...r,i]);
 }
 find(0,[]);return out;
}
// 4 nonzero independent directions from each ray.
const ca=[0,1,3,5].map(i=>[Ma[i][0],Ma[i][1],Ma[i][2],Ma[i][3]]);
const cb=[0,1,3,4].map(i=>[Mb[i][0],Mb[i][1],Mb[i][2],Mb[i][3]]);
check(det(ca)!==0n&&det(cb)!==0n,"each actual original one-ray tangent has rank EXACTLY4");
const rows=[0,1,3,4,8,11],minor=rows.map(i=>full[i]);
check(det(minor)===-54n,
 "two independently recorded CAR projective rays resolve all six Lorentz Lie directions: exact det -54");
const names=["N2","N3","barN2","barN3","J23","B"];
const mm=(X,Y)=>X.map(row=>Y[0].map((_,j)=>dot(row,Y.map(r=>r[j]))));
const I=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const exp=(M,x)=>plus(plus(I,M.map(row=>row.map(v=>x*v))),
                            mm(M,M).map(row=>row.map(v=>x*x*v/2)));
const A=G[0],C=G[3];
const comm=plus(mm(A,C),mm(C,A),-1);
check(JSON.stringify(comm)===JSON.stringify(G[4]),
 "EXACT original two-null chronological order [N2,barN3]=J23");
const make=(a,b,r,i)=>{
 const X=mm(exp(C,b),exp(A,a)),x=mv(X,r),y=mv(X,i);
 const norm=Math.sqrt(dot(x,x)+dot(y,y));
 return {re:x.map(v=>v/norm),im:y.map(v=>v/norm)};
};
const inner=(x,y)=>({re:dot(x.re,y.re)+dot(x.im,y.im),
 im:dot(x.re,y.im)-dot(x.im,y.re)});
const mul=(x,y)=>({re:x.re*y.re-x.im*y.im,im:x.re*y.im+x.im*y.re});
const phase=(s,v)=>mul(s,{re:Math.cos(v),im:Math.sin(v)});
const bargain=(a,b,r,im,angles=[0,0,0])=>{
 const X=make(0,0,r,im),Y=make(a,0,r,im),Z=make(a,b,r,im);
 function rephase(x,q){const cr=Math.cos(q),si=Math.sin(q);
 return {re:x.re.map((v,j)=>v*cr-x.im[j]*si),
         im:x.im.map((v,j)=>v*cr+x.re[j]*si)};}
 const x=rephase(X,angles[0]),y=rephase(Y,angles[1]),z=rephase(Z,angles[2]);
 return mul(mul(inner(x,y),inner(y,z)),inner(z,x));
};
const v1r=[1,0,1,0],v1i=[0,0,0,1],v2r=[0,1,1,0],v2i=[0,0,0,1];
let errors=[];
for(const h of [.1,.03,.01,.003]){
 const f1=bargain(h,h,v1r,v1i),f2=bargain(h,h,v2r,v2i);
 const j1=Math.atan2(f1.im,f1.re)/h**2,j2=Math.atan2(f2.im,f2.re)/h**2;
 check(Math.abs(j1+1/9)<.005&&Math.abs(j2-1/9)<.011,
       "Bargmann closed original projective history phase agrees with exact +/-1/9 h="+h);
 const t1=bargain(h,h,v1r,v1i,[.3,-.6,1.2]);
 check(Math.hypot(t1.re-f1.re,t1.im-f1.im)<1e-14,
       "TRUE closed state overlap gauge-invariant under three independent rephasings");
 errors.push({h,j1,j2});
}
// Exact connected mixed coefficient from the native integer matrices:
function imcov(r,im){
 const s=Math.sqrt(dot(r,r)+dot(im,im)),R=r.map(x=>x/s),I0=im.map(x=>x/s);
 const ar=mv(A,R),ai=mv(A,I0),br=mv(C,R),bi=mv(C,I0);
 const pA={re:dot(R,ar)+dot(I0,ai),im:dot(R,ai)-dot(I0,ar)};
 const pB={re:dot(R,br)+dot(I0,bi),im:dot(R,bi)-dot(I0,br)};
 const dAB={re:dot(ar,br)+dot(ai,bi),im:dot(ar,bi)-dot(ai,br)};
 const conn={re:pA.re*pB.re+pA.im*pB.im,
             im:pA.re*pB.im-pA.im*pB.re};
 return dAB.im-conn.im;
}
check(Math.abs(imcov(v1r,v1i)+1/9)<1e-13 &&
      Math.abs(imcov(v2r,v2i)-1/9)<1e-13,
      "exact connected ORIGINAL Lorentz CAR mixed source is opposite +/-1/9");
check(Math.abs(imcov(v1r,v1i)-imcov(v2r,v2i)+2/9)<1e-13,
      "gauge-free relative two-detector order-memory phase = -2/9");
const comparison=(theta,x)=>({re:Math.cos(theta)*x.re-Math.sin(theta)*x.im,
 im:Math.sin(theta)*x.re+Math.cos(theta)*x.im});
let q=.01,phasePlain=inner(make(0,0,v1r,v1i),make(q,0,v1r,v1i));
const gaugeChanged=comparison(.7,phasePlain);
check(Math.abs(Math.atan2(gaugeChanged.im,gaugeChanged.re)
               -Math.atan2(phasePlain.im,phasePlain.re))>.5,
      "HOSTILE single two-arm phase shifts under arbitrary projective gauge");
console.log(JSON.stringify({source:"original CAR16 grade1 and six true proper Lorentz generators",
exact_two_ray_minor_det:"-54",single_ray_ranks:[4,4],joined_rank:6,
closed_mixed_Bargmann_phases:["-1/9","+1/9"],
two_line_difference:"-2/9",finite_controls:errors,
physical_same_history_CostInfo_selected:false,gr_closed:false},null,2));
