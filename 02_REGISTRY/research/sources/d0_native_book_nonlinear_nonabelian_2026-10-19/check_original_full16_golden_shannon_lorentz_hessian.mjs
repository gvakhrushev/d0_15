#!/usr/bin/env node
"use strict";
// ORIGINAL full16 native GOLDEN p CAR16 two-fresh Julia+Choi readout:
// exact analytic pointer-Shannon Lorentz Hessian of signed inertia 3+/3-.
// Not proof selected whole H+J+R/Book action equals pointer Shannon.
const p=(Math.sqrt(5)-1)/2,L=Math.log(1/p);
const E=(i,j)=>{let a=Array.from({length:4},()=>Array(4).fill(0));a[i][j]=1;return a;};
const plus=(A,B,c=1)=>A.map((r,i)=>r.map((v,j)=>v+c*B[i][j]));
const times=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,v,k)=>s+v*B[k][j],0)));
const transpose=A=>A.map((r,i)=>r.map((_,j)=>A[j][i]));
const trace=A=>A.reduce((s,r,i)=>s+r[i],0);
const ip=(A,B)=>trace(times(transpose(A),B));
const eye=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const generators=[plus(E(1,2),E(2,0)),plus(E(1,3),E(3,0)),
 plus(E(0,2),E(2,1)),plus(E(0,3),E(3,1)),
 plus(E(2,3),E(3,2),-1),plus(E(1,1),E(0,0),-1)];
const need=(ok,label)=>{if(!ok)throw Error("FAIL "+label);console.log("PASS "+label)};
need(generators.every((a,i)=>generators.every((b,j)=>
 Math.abs(ip(a,b)-(i===j?2:0))<1e-14)),"true original six generator Gram=2I");
function expM(X){let S=eye,M=eye;for(let j=1;j<=25;j++){
 M=times(M,X).map(r=>r.map(x=>x/j));S=plus(S,M);
 }return S;
}
function qOut(x){
 const X=generators.reduce((s,g,i)=>plus(s,g,x[i]),eye.map(r=>r.map(()=>0)));
 const U=expM(X),mean=trace(U)/4,v=ip(U,U)/4;
 const q=generators.flatMap(g=>{
  const y=ip(g,U)/(2*Math.SQRT2);
  return [p**4/24*(mean+y)**2,p**4/24*(mean-y)**2];
 });
 const gg=p**4*v,rest=gg-q.reduce((s,x)=>s+x,0);
 return q.concat([rest,p*p*(1-p*p*v),p**3*v,1-gg-p*p*(1-p*p*v)-p**3*v]);
}
function H(x){return qOut(x).reduce((s,q)=>s-q*Math.log(q)/L,0);}
const x0=Array(6).fill(0),q0=qOut(x0),H0=H(x0);
need(q0.length===16&&q0.every(x=>x>0)&&Math.abs(q0.reduce((s,x)=>s+x,0)-1)<1e-13,
 "complete actual Golden-p 16 outcomes (12 marked+rest+GB/BG/BB), no losses");
const CN=p*p+(p**4/L)*(Math.log(2)+Math.log(12)/12-1/6);
const CS=p*p/2+(p**4/L)*(Math.log(2)/2+Math.log(12)/4);
const Gram=generators.map(g=>generators.map(h=>trace(times(g,h))));
const Hess=Gram.map((row,i)=>row.map((v,j)=>(i===j?CN:0)+CS*v));
const positive=CN+2*CS,negative=CN-2*CS;
const closedPos=2*p*p+(p**4/(12*L))*(7*Math.log(12)+24*Math.log(2)-2);
const closedNeg=-(p**4/(12*L))*(5*Math.log(12)+2);
need(positive>0&&negative<0&&
 Math.abs(positive-closedPos)<1e-13&&Math.abs(negative-closedNeg)<1e-13,
 "ORIGINAL full Golden pointer Shannon has EXACT 3 positive and 3 negative eigenvalues");
need(Math.abs(positive-1.5731903897412776)<1e-12&&
 Math.abs(negative+0.3644464054413963)<1e-12,
 "intrinsic signed full16 source eigenvalues at flat");
let prev=Infinity;
for(const h of [.02,.008,.003,.001]){
 const M=Array.from({length:6},()=>Array(6).fill(0)),gr=[];
 for(let i=0;i<6;i++){
  const xp=x0.slice(),xm=x0.slice();xp[i]=h;xm[i]=-h;
  gr.push((H(xp)-H(xm))/(2*h));
  M[i][i]=(H(xp)-2*H0+H(xm))/(h*h);
  for(let j=i+1;j<6;j++){
   const pp=x0.slice(),pm=x0.slice(),mp=x0.slice(),mm=x0.slice();
   pp[i]=h;pp[j]=h;pm[i]=h;pm[j]=-h;
   mp[i]=-h;mp[j]=h;mm[i]=-h;mm[j]=-h;
   M[i][j]=(H(pp)-H(pm)-H(mp)+H(mm))/(4*h*h);
   M[j][i]=M[i][j];
  }
 }
 const error=Math.max(...M.flatMap((r,i)=>r.map((v,j)=>Math.abs(v-Hess[i][j]))));
 need(Math.max(...gr.map(Math.abs))<2e-10,
      "actual full Golden-q pointer Shannon FLAT FIRST EULER zero, six directions h="+h);
 need(error<prev&&error<.0006,
      "native full16 positive pointer Hessian analytic equals six-by-six finite matrix h="+h);
 prev=error;
}
const Fisher=p**4/6;
need(Fisher>0&&positive+Fisher/L>0&&negative+Fisher/L<0,
 "positive Fisher term by itself does NOT force signed measured-Shannon Hessian");

// STRONG NEGATIVE CONTROL: a genuine FOUR-GATE original based face has
// P-I=ab J23+O(a²b,ab²), so whole unmarked 16-outcome Shannon has
// ZERO first curvature mixed [ab]. Yet the native positive sqrt-mark
// recovers the actual oriented Lie component 2ab exactly to leading order.
// Hence the signed native Hess of one LINK cannot itself be declared a
// selected plaquette/EH action without PRETRACE ordered marker/cost source.
function qOriginalU(U){
 const avg=trace(U)/4,norm=ip(U,U)/4;
 const mark=generators.flatMap(J=>{
  const y=ip(J,U)/(2*Math.SQRT2);
  return [p**4/24*(avg+y)**2,p**4/24*(avg-y)**2];
 });
 const GG=p**4*norm,GB=p*p*(1-p*p*norm),BG=p**3*norm;
 return [...mark,GG-mark.reduce((a,b)=>a+b,0),GB,BG,1-GG-GB-BG];
}
function face(a,b){
 let E=t=>expM(generators[0].map(r=>r.map(v=>t*v)));
 let F=t=>expM(generators[3].map(r=>r.map(v=>t*v)));
 return times(times(times(E(a),F(b)),E(-a)),F(-b));
}
function faceEntropy(a,b){
 return qOriginalU(face(a,b)).reduce((s,q)=>s-q*Math.log(q)/L,0);
}
let lastFace=Infinity;
for(const h of [.16,.08,.04,.02]){
 const ppf=face(h,h),pmf=face(h,-h),
       mpf=face(-h,h),mmf=face(-h,-h);
 const he=(faceEntropy(h,h)-faceEntropy(h,-h)
      -faceEntropy(-h,h)+faceEntropy(-h,-h))/(4*h*h);
 const marker=(ip(generators[4],ppf)-ip(generators[4],pmf)
              -ip(generators[4],mpf)+ip(generators[4],mmf))/(4*h*h);
 need(Math.abs(he)<1e-10,
      "TRUE complete 16-outcome Shannon loses FIRST oriented [ab] face order at h="+h);
 need(Math.abs(marker-2)<lastFace&&Math.abs(marker-2)<.001,
      "SAME native Golden positive J23 marker retains FIRST Cartan [ab]=2 at h="+h);
 lastFace=Math.abs(marker-2);
}
need(Math.abs(faceEntropy(0,0)-H0)<1e-13,
     "Shannon and oriented positive marker negative controls use IDENTICAL full Golden instrument");

console.log(JSON.stringify({
 full_golden_16_outcome_base:q0,
 pointer_entropy_Hphi_flat:H0,
 first_flat_Lorentz_source:"zero in all SIX original proper generators",
 Hessian_exact:"CN I + CS*tr(Ga Gb)",
 CN,CS,
 Hessian_all_six:Hess,
 eigen_plus_3fold:positive,eigen_minus_3fold:negative,
 inertia_per_original_one_link:"(3+,3-)",
 four_independent_copies:"(12+,12-) — NOT the original coupled 24-link Hessian",
 last_hessian_replay_error:prev,
 compulsory_book_action_selected:false,GR_closed:false
},null,2));
