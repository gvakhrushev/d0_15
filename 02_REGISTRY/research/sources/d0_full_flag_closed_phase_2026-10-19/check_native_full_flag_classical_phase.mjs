#!/usr/bin/env node
"use strict";
/**
 * D0 original CAR16 grade-one (4x4 block), existing Julia T=Lambda(U)/2
 * + F=sqrt(I-T†T), ORIGINAL two null N2,barN3.
 * Retain entire classical GOOD/BAD flag with BOTH unnormalized CAR blocks.
 * Compute gauge-invariant three-record cyclic trace without ANY coherent
 * interference across the success/failure flags.
 * No native whole Cost-Info/action/Einstein equality is claimed.
 */
const I=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const Z=n=>I(n).map(row=>row.map(()=>0));
const E=(i,j)=>{let m=Z(4);m[i][j]=1;return m};
const add=(A,B,s=1)=>A.map((r,i)=>r.map((v,j)=>v+s*B[i][j]));
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((sum,v,k)=>sum+v*B[k][j],0)));
const tr=A=>A.map((r,i)=>r.map((_,j)=>A[j][i]));
const mv=(A,v)=>A.map(r=>r.reduce((s,x,i)=>s+x*v[i],0));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const test=(condition,msg)=>{if(!condition)throw Error("FAIL "+msg);console.log("PASS "+msg)};
const Ah=add(E(1,2),E(2,0)),Bh=add(E(0,3),E(3,1));
const aSym=add(Ah,tr(Ah)),bSym=add(Bh,tr(Bh));
const expNil=(X,h)=>add(add(I(4),X,h),mul(X,X),h*h/2);
function inverse(M){
 const n=M.length,aug=M.map((r,i)=>[...r,...I(n)[i]]);
 for(let j=0;j<n;j++){
  let pivot=j;for(let k=j+1;k<n;k++)if(Math.abs(aug[k][j])>Math.abs(aug[pivot][j]))pivot=k;
  if(Math.abs(aug[pivot][j])<1e-12)throw Error("noninvertible");
  [aug[j],aug[pivot]]=[aug[pivot],aug[j]];
  let d=aug[j][j];for(let k=j;k<2*n;k++)aug[j][k]/=d;
  for(let i=0;i<n;i++)if(i!==j){let t=aug[i][j];for(let k=j;k<2*n;k++)aug[i][k]-=t*aug[j][k];}
 }
 return aug.map(r=>r.slice(n));
}
function squareRootSPD(M){
 let X=I(4);
 for(let n=0;n<40;n++){
  X=add(X,mul(M,inverse(X))).map(r=>r.map(x=>x/2));
  const error=Math.max(...mul(X,X).flatMap((r,i)=>r.map((v,j)=>Math.abs(v-M[i][j]))));
  if(error<1e-14)break;
 }
 return X;
}
const inner=(u,v)=>{
 const [r,i]=u,[s,t]=v;
 return [dot(r,s)+dot(i,t),dot(r,t)-dot(i,s)];
};
const cmul=(u,v)=>[u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]];
const tri=(x,y,z)=>cmul(cmul(inner(x,y),inner(y,z)),inner(z,x));
function prep(r,i){
 let norm=Math.hypot(...r,...i);
 return [r.map(x=>x/norm),i.map(x=>x/norm)];
}
function fullRecord(a,b,r,im){
 // One pre-existing full Lorentz exterior Julia step, grade-one block.
 const U=mul(expNil(Bh,b),expNil(Ah,a));
 const T=U.map(row=>row.map(v=>v/2));
 const TT=mul(tr(T),T);
 const F=squareRootSPD(add(I(4),TT,-1));
 const psi=prep(r,im),gr=mv(T,psi[0]),gi=mv(T,psi[1]);
 const br=mv(F,psi[0]),bi=mv(F,psi[1]);
 const qGood=dot(gr,gr)+dot(gi,gi);
 const qBad=dot(br,br)+dot(bi,bi);
 test(Math.abs(qGood+qBad-1)<2e-12,
      "complete Julia/GOOD+BAD history is normalized a="+a+" b="+b);
 return {GOOD:[gr,gi],BAD:[br,bi],qGood,qBad};
}
function cyclic(a,b,re,im){
 const r0=fullRecord(0,0,re,im),r1=fullRecord(a,0,re,im),
       r2=fullRecord(a,b,re,im);
 const g=tri(r0.GOOD,r1.GOOD,r2.GOOD);
 const f=tri(r0.BAD,r1.BAD,r2.BAD);
 return {good:g,bad:f,full:[g[0]+f[0],g[1]+f[1]]};
}
function connectedImag(re,im,U,V){
 const [r,i]=prep(re,im);
 const ur=mv(U,r),ui=mv(U,i),vr=mv(V,r),vi=mv(V,i);
 const ab=inner([ur,ui],[vr,vi]),u=inner([r,i],[ur,ui]),
       v=inner([r,i],[vr,vi]);
 return ab[1]-(u[0]*v[1]-u[1]*v[0]);
}
const probes=[
 {name:"plus",re:[1,0,1,0],im:[0,0,0,1],sign:-1,
  good:-1/576,bad:1/128,full:7/1152,phase:1/72},
 {name:"minus",re:[0,1,1,0],im:[0,0,0,1],sign:1,
  good:+1/576,bad:1/128,full:11/1152,phase:11/504}
];
for(const v of probes){
 const jGood=connectedImag(v.re,v.im,Ah,Bh),jBad=connectedImag(v.re,v.im,aSym,bSym);
 const g=jGood/64,b=3*jBad/256,full=g+b;
 test(Math.abs(jGood-v.sign/9)<1e-13,
      v.name+" original CAR16 GOOD connected mixed phase +/-1/9");
 test(Math.abs(jBad-2/3)<1e-13,
      v.name+" original Julia BAD symmetric-contraction mixed phase +2/3");
 test(Math.abs(g-v.good)<1e-13 && Math.abs(b-v.bad)<1e-13,
      v.name+" exact BOTH-dephased-flag contributions, no postselection");
 test(Math.abs(full-v.full)<1e-13,
      v.name+" full dephased native Julia closed trace imaginary coefficient");
 const baseline=cyclic(0,0,v.re,v.im);
 test(Math.abs(baseline.full[0]-7/16)<1e-13&&Math.abs(baseline.full[1])<1e-13,
      v.name+" original complete GOOD/BAD cyclic record baseline 7/16");
 test(Math.abs(full/(7/16)-v.phase)<1e-13,
      v.name+" normalized gauge-invariant CLOSED PHASE coefficient");
 let prev=Infinity;
 for(const h of [.1,.03,.01,.003]){
   const x=cyclic(h,h,v.re,v.im);
   const coeff=x.full[1]/(h*h);
   const err=Math.abs(coeff-v.full);
   test(err<prev && err<.002,
        v.name+" full positive Julia square-root direct history vs exact coefficient h="+h);
   prev=err;
 }
 // Strong hostile negative control: diagonal dephasing inside CAR grades
 // makes all three branch density matrices diagonal, so their cyclic trace
 // is real. Between-flag dephasing alone does NOT cause this loss.
 test(Math.abs(v.full)>0&&jBad!==0,
      v.name+" flag-classical signal depends on WITHIN-CAR coherences");
}
test(Math.abs((7/1152)-(11/1152)+1/288)<1e-15,
 "full dephased two-line imaginary coefficient difference exactly -1/288");
test(Math.abs((1/72)-(11/504)+1/126)<1e-15,
 "full dephased normalized closed-phase difference exactly -1/126");

// Independent literal block-diagonal DENSITY-MATRIX control. This is
// reconstructed from original conditional CAR one-body coherences and
// classical flag probabilities, without ANY GOOD/BAD coherence.
const ketDensity=u=>{
 const [r,i]=u;
 return Array.from({length:4},(_,a)=>
  Array.from({length:4},(_,b)=>[
   r[a]*r[b]+i[a]*i[b],i[a]*r[b]-r[a]*i[b]
  ]));
};
const cmul2=(u,v)=>[u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]];
const cMatrixProduct=(A,B)=>A.map(row=>
 B[0].map((_,j)=>row.reduce((sum,x,k)=>{
  const y=cmul2(x,B[k][j]);return [sum[0]+y[0],sum[1]+y[1]];
 },[0,0])));
const cyclicDensity=(x,y,z)=>{
 const A=cMatrixProduct(cMatrixProduct(x,y),z);
 return A.reduce((s,r,j)=>[s[0]+r[j][0],s[1]+r[j][1]],[0,0]);
};
const diagOnly=M=>M.map((row,j)=>row.map((v,k)=>j===k?[v[0],0]:[0,0]));
for(const v of probes){
 const a=fullRecord(0,0,v.re,v.im),b=fullRecord(.03,0,v.re,v.im),
       c=fullRecord(.03,.03,v.re,v.im);
 const block=(name)=>cyclicDensity(
  ketDensity(a[name]),ketDensity(b[name]),ketDensity(c[name]));
 const g=block("GOOD"),f=block("BAD");
 const ref=cyclic(.03,.03,v.re,v.im);
 test(Math.abs(g[0]-ref.good[0])<1e-13&&
      Math.abs(g[1]-ref.good[1])<1e-13&&
      Math.abs(f[0]-ref.bad[0])<1e-13&&
      Math.abs(f[1]-ref.bad[1])<1e-13,
      v.name+" literal CLASSICAL-FLAG block density trace agrees with full complete Julia output");
 const dg=cyclicDensity(
  diagOnly(ketDensity(a.GOOD)),diagOnly(ketDensity(b.GOOD)),diagOnly(ketDensity(c.GOOD)));
 const df=cyclicDensity(
  diagOnly(ketDensity(a.BAD)),diagOnly(ketDensity(b.BAD)),diagOnly(ketDensity(c.BAD)));
 test(dg[1]===0&&df[1]===0,
      v.name+" HOSTILE: removing WITHIN-CAR coherence kills both full-flag phase terms");
 const gr=cyclicDensity(ketDensity(c.GOOD),ketDensity(b.GOOD),ketDensity(a.GOOD));
 const br=cyclicDensity(ketDensity(c.BAD),ketDensity(b.BAD),ketDensity(a.BAD));
 test(Math.abs(gr[1]+g[1])<1e-13&&Math.abs(br[1]+f[1])<1e-13,
      v.name+" reversed complete chronological density ordering flips gauge-free phase");
}

console.log(JSON.stringify({
 original_carrier:"full CAR16 grade-one block, original two-null Lorentz/Julia",
 classical_flags:true,
 no_good_bad_coherence:true,
 all_failures_retained:true,
 raw_cyclic_base:"7/16",
 good_imag_mixed_coeff:["-1/576","+1/576"],
 bad_imag_mixed_coeff:["+1/128","+1/128"],
 full_imag_mixed_coeff:["7/1152","11/1152"],
 full_phase_mixed_coeff:["1/72","11/504"],
 phase_gap:"-1/126",
 original_book_action_identified:false,
 GR_closed:false
},null,2));
