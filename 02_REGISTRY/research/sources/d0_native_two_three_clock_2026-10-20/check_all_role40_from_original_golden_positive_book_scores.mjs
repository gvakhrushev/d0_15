#!/usr/bin/env node
"use strict";
// Exact finite original Golden CAR16 two-fresh Julia/Bell17 root
// reconstruction of the ORIGINAL odd SO+(1,3) based-face tensor.
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
function decode(q,w){
 return G.map((g,j)=>256*Math.sqrt(3)/(p*p*Math.sqrt(w))*
   (Math.sqrt(w*q[2*j])-Math.sqrt(w*q[2*j+1])));
}
function oddMeasured(P,wp,wm){
 const q=outcomes(P),qm=outcomes(inv(P)),rp=decode(q,wp),rm=decode(qm,wm);
 return G.reduce((s,g,j)=>add(s,g,(rp[j]-rm[j])/4),Z());
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
console.log(JSON.stringify({
 original_4d_finite_sites:16,original_nontrivial_faces:nonflat,
 true_Golden_full_Bell_categories:17,both_face_orientations:true,
 max_exact_odd_tensor_diff:maxTensor,max_coframe_Hodge_face_diff:maxSource,
 max_original_Book_moving_score_residual:scoreError,
 physical_Book_selected_action:false,GR_closed:false
},null,2));
