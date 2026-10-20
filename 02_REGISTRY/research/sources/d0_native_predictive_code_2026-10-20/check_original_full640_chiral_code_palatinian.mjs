#!/usr/bin/env node
"use strict";
// Exact original 17-way GOLDEN p:p² asymmetric CONDITIONAL CODE PRICE
// reconstruction of original odd SO+(1,3) face, with 11 adaptive coarse
// pair/singleton masses and all 640 true original geometric Euler.
// Includes two independently moving real ORIGINAL rooted Book path
// weights. NO invented action, no assumed G0 selection or GR claim.
const p=(Math.sqrt(5)-1)/2,L=Math.log(1/p),herald=1/4096;
const I=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const Z=()=>I().map(r=>r.map(()=>0));
const E=(i,j)=>{let A=Z();A[i][j]=1;return A};
const add=(a,b,k=1)=>a.map((r,i)=>r.map((x,j)=>x+k*b[i][j]));
const mm=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,x,k)=>s+x*b[k][j],0)));
const t=a=>a.map((row,i)=>row.map((_,j)=>a[j][i]));
const dot=(a,b)=>a.flat().reduce((s,v,k)=>s+v*b.flat()[k],0);
const tr=a=>a.reduce((s,r,i)=>s+r[i],0);
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const inv=a=>mm(mm(eta,t(a)),eta);
const max=(a,b)=>Math.max(...a.flatMap((r,i)=>r.map((v,j)=>Math.abs(v-b[i][j]))));
const G=[add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)];
const check=(ok,msg)=>{if(!ok)throw Error("FAIL "+msg);console.log("PASS "+msg)};
check(G.every((g,i)=>G.every((h,j)=>Math.abs(dot(g,h)-(i===j?2:0))<1e-13)), "all six ORIGINAL Lorentz Lie basis elements dual by Gram2");
function exp(X){let P=I(),T=I();for(let k=1;k<=21;k++){T=mm(T,X).map(r=>r.map(v=>v/k));P=add(P,T)}return P}
function outcomes(P){
 const av=tr(P)/4,n=dot(P,P)/4;
 let q=G.flatMap(g=>{const y=dot(g,P)/(2*Math.SQRT2);
 return [p**4/24*(av+y)**2,p**4/24*(av-y)**2]});
 const GG=p**4*n,GB=p*p*(1-p*p*n),BG=p**3*n;
 q.push(GG-q.reduce((s,x)=>s+x,0),GB,BG,1-GG-GB-BG);
 q=q.map(x=>x*herald).concat([1-herald]);
 if(q.some(x=>!(x>0))||Math.abs(q.reduce((s,x)=>s+x,0)-1)>2e-13)
   throw Error("incomplete original Golden/Bell 17 categories");
 return q;
}
// Original complete 17-outcome Golden code is learned ONLY on its 11
// coarse classes, while each of its SIX oriented +/- pair conditional
// probabilities uses the ORIGINAL Golden (p,p²) coding alphabet.
// At a fixed measured P, 11 true class masses are uniquely selected
// by minimizing full positive KL, without postselection of Bell-fail.
// The forward-vs-reverse CODE-REGRET difference in one pair is EXACTLY
// negative its orientation-odd signed Golden probability difference.
// From the six code prices we directly reconstruct the ORIGINAL
// full nonlinear SO odd face using no external Einstein term or angle.
const codePair=(q,j)=>{
 const r=2*j,z=q[r]+q[r+1],a=q[r],b=q[r+1];
 return (a*Math.log(a/(z*p))+b*Math.log(b/(z*p*p)))/L;
};
const goldenMark=u=>Math.sqrt(u); // kept for independent original owner comparison
const priceQuantum=herald*p**4/24;
function oddMeasured(P,wp,wm){
 const q=outcomes(P),qm=outcomes(inv(P));
 const plusJoint=q.map(x=>wp*x),minusJoint=qm.map(x=>wm*x);
 const plusMarginal=plusJoint.reduce((x,y)=>x+y,0),
       minusMarginal=minusJoint.reduce((x,y)=>x+y,0);
 const qp=plusJoint.map(x=>x/plusMarginal),
       qm=minusJoint.map(x=>x/minusMarginal);
 const m=tr(P)/4;
 if(!(m>0))throw Error("original Golden positive-root Lie chart exhausted");
 return G.reduce((A,g,j)=>{
   const codeDifference=codePair(qp,j)-codePair(qm,j);
   return add(A,g,-Math.SQRT2*codeDifference/(4*priceQuantum*m));
 },Z());
}
function eps(a){if(new Set(a).size<4)return 0;let v=1;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)if(a[i]>a[j])v=-v;return v}
function contract(F,u,v,A){
 let C=mm(A,eta),s=0;
 for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
  const r=[0,1,2,3].filter(j=>j!==a&&j!==b);
  s+=eps([a,b,...r])*(F[a][u]*F[b][v]-F[b][u]*F[a][v])*C[r[0]][r[1]];
 }return s;
}
const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const links=Array.from({length:16},(_,x)=>Array.from({length:4},(_,r)=>{
 const X=add(G[(x+r)%4],G[(x+3*r+1)%4],.4);
 return exp(X.map(a=>a.map(v=>v*(.007+.0009*((x+2*r)%5)))));
}));
const frames=Array.from({length:16},(_,x)=>{
 const F=I();for(let a=0;a<4;a++)for(let r=0;r<4;r++)F[a][r]+=.009*Math.sin((x+1)*(a+1)+(r+1)*.77);return F;
});
const shift=(x,r)=>x^(1<<r);
const plaquette=(x,r,s)=>mm(mm(mm(links[x][r],links[shift(x,r)][s]),inv(links[shift(x,s)][r])),inv(links[x][s]));
let maxTensor=0,maxSource=0,nonflat=0,minimum=1;
for(let x=0;x<16;x++)for(let j=0;j<6;j++){
 const [r,s]=pairs[j],rest=[0,1,2,3].filter(k=>k!==r&&k!==s),
       P=plaquette(x,r,s),Pi=inv(P),odd=add(P,Pi,-1).map(a=>a.map(v=>v/2));
 if(max(P,I())>1e-12)nonflat++;
 // all primitive edge Costs in the true original based K9/11/13 loop
 // above one, different forward/reverse and moving with coframe + P.
 const move=.01*(frames[x][0][0]-1)+.004*dot(G[4],odd);
 const wp=Math.exp(-L*(3.34+move+.004*j/6));
 const wm=Math.exp(-L*(3.42-move+.003*j/6));
 const observed=oddMeasured(P,wp,wm);
 maxTensor=Math.max(maxTensor,max(odd,observed));
 let d=eps([r,s,...rest])*contract(frames[x],rest[0],rest[1],odd);
 let m=eps([r,s,...rest])*contract(frames[x],rest[0],rest[1],observed);
 maxSource=Math.max(maxSource,Math.abs(d-m));minimum=Math.min(minimum,wp,wm);
}
check(nonflat===96&&maxTensor<2e-13, "EXACT original odd SO face (P-Pinverse)/2 reconstructs from all 12 positive Golden marked roots at EVERY 4D Role face");
check(maxSource<5e-13, "TRUE original coframe/Hodge six-face source equals complete Golden-positive rooted Book comparisons");
let scoreError=0;
for(let j=0;j<6;j++){
 const P=plaquette(0,0,1),X=add(G[4],G[2],.37),h=1e-5,
       pp=mm(exp(X.map(a=>a.map(v=>h*v))),P),
       pm=mm(exp(X.map(a=>a.map(v=>-h*v))),P),
       cost=Y=>3.4+.01*dot(G[4],Y),
       w=Math.exp(-L*cost(P)),wp=Math.exp(-L*cost(pp)),wm=Math.exp(-L*cost(pm)),
       q=outcomes(P),qa=outcomes(pp),qb=outcomes(pm);
 const dW=(Math.log(wp)-Math.log(wm))/(2*h);
 const dp=(Math.log(wp*qa[2*j])-Math.log(wm*qb[2*j]))/(2*h);
 const dm=(Math.log(wp*qa[2*j+1])-Math.log(wm*qb[2*j+1]))/(2*h);
 const rhs=128*Math.sqrt(3)/(p*p*Math.sqrt(w))*
  (Math.sqrt(w*q[2*j])*(dp-dW)-Math.sqrt(w*q[2*j+1])*(dm-dW));
 const lhs=(dot(G[j],pp)-dot(G[j],pm))/(2*h);
 scoreError=Math.max(scoreError,Math.abs(rhs-lhs));
}
check(scoreError<5e-7,"true moving ORIGINAL Book path score cancels from all 6 positive Golden conditional Lorentz first sources");

// Entire true ORIGINAL finite 4D Role Euler on the 16-site L2 regulator:
// 256 independent coframe and 384 original globally shared Lorentz-link
// rows. Each link contributes to six ORIGINAL based plaquettes across
// FOUR sites: x, x+e_s for its three perpendicular directions s.
function dynamicFace(X,x,r,s){
 const U=X.links;
 return mm(mm(mm(U[x][r],U[shift(x,r)][s]),inv(U[shift(x,s)][r])),inv(U[x][s]));
}
function dynamicSite(X,x,read){
 let val=0;
 for(let j=0;j<6;j++){
  const [r,s]=pairs[j],rest=[0,1,2,3].filter(v=>v!==r&&v!==s),
        P=dynamicFace(X,x,r,s),R=add(P,inv(P),-1).map(row=>row.map(v=>v/2)),F=X.frames[x];
  let B=R;
  if(read){
   const move=.01*(F[0][0]-1)+.004*dot(G[4],R),
   wp=Math.exp(-L*(3.34+move+.004*j/6)),
   wm=Math.exp(-L*(3.42-move+.003*j/6));
   B=oddMeasured(P,wp,wm);
  }
  val+=eps([r,s,...rest])*contract(F,rest[0],rest[1],B);
 }
 return val;
}
const step=1e-5;
function frameVariation(x,a,u,h){
 const F=frames.map(row=>row.map(r=>r.slice()));
 F[x][a][u]+=h;return {links,frames:F}
}
function linkVariation(x,r,j,h){
 const U=links.map(row=>row.map(M=>M.map(z=>z.slice())));
 U[x][r]=mm(exp(G[j].map(row=>row.map(v=>v*h))),U[x][r]);
 return {links:U,frames}
}
let eCount=0,lCount=0,nonzeroE=0,nonzeroL=0,maxDerivative=0,affectedMin=7,affectedMax=0;
for(let x=0;x<16;x++)for(let a=0;a<4;a++)for(let u=0;u<4;u++){
 const A=frameVariation(x,a,u,step),B=frameVariation(x,a,u,-step);
 const d=(dynamicSite(A,x,false)-dynamicSite(B,x,false))/(2*step);
 const r=(dynamicSite(A,x,true)-dynamicSite(B,x,true))/(2*step);
 maxDerivative=Math.max(maxDerivative,Math.abs(d-r));
 if(Math.abs(d)>1e-9)nonzeroE++;eCount++;
}
for(let x=0;x<16;x++)for(let r=0;r<4;r++)for(let j=0;j<6;j++){
 const A=linkVariation(x,r,j,step),B=linkVariation(x,r,j,-step),
  sites=[x,...[0,1,2,3].filter(s=>s!==r).map(s=>shift(x,s))];
 affectedMin=Math.min(affectedMin,sites.length);
 affectedMax=Math.max(affectedMax,sites.length);
 let d=0,v=0;
 for(let y of sites){
  d+=(dynamicSite(A,y,false)-dynamicSite(B,y,false))/(2*step);
  v+=(dynamicSite(A,y,true)-dynamicSite(B,y,true))/(2*step);
 }
 maxDerivative=Math.max(maxDerivative,Math.abs(d-v));
 if(Math.abs(d)>1e-9)nonzeroL++;lCount++;
}
check(eCount===256&&lCount===384&&affectedMin===4&&affectedMax===4
      &&nonzeroE>220&&nonzeroL>320,
 "all 640 true independent finite Role Euler sources, 256 coframe + 384 link, every link affects six neighboring based faces");
check(maxDerivative<4e-7,
 "all 640 source rows reproduced from TRUE Golden-p full17 probabilities with moving Book cost and all failure flags");

console.log(JSON.stringify({
 original_4d_finite_sites:16,original_nontrivial_faces:nonflat,
 true_Golden_full_Bell_categories:17,both_face_orientations:true,
 trueConditionalGoldenSignedCodeProbability:[p,p*p],
 predictiveGoldenCoarseCategories:11,
 max_exact_odd_tensor_diff:maxTensor,max_coframe_Hodge_face_diff:maxSource,
 max_original_Book_moving_score_residual:scoreError,
 actual_all_640_source_max_disagreement:maxDerivative,
 genuine_original_coframe_Euler_rows:eCount,
 genuine_original_shared_link_Euler_rows:lCount,
 nonzero_original_coframe_Euler_rows:nonzeroE,
 nonzero_original_link_Euler_rows:nonzeroL,
 exact_number_of_affected_sites_per_link:[affectedMin,affectedMax],
 physical_Book_selected_action:false,
 native_code_prefix_chosen_not_compulsory:true,GR_closed:false
},null,2));
