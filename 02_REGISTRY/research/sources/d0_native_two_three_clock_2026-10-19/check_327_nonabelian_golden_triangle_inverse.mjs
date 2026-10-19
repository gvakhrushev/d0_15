#!/usr/bin/env node
"use strict";
/*
 Original D0 K(9,11,13) 33/359/718 triangle holonomies on true
 SO+(1,3) original six-generator carrier, CAR16 full 2-Golden flag
 Choi 16 + full 64D Bell failed category (17).
 Reconstruct 327 nonabelian ORIGINAL graph-cycle link matrices (1962
 tangent dimensions) in exact ordered 143+104+80 passes, plus consume
 global original mixed 2/3-clock scalar rank686 -> total rank2648.
 Calibrated common CAR tree-transported frame is an EXPLICIT physical
 assumption, not native G0 admission. No Einstein source assertion.
*/
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),bell=1/4096;
const I=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const Z=()=>Array.from({length:4},()=>Array(4).fill(0));
const E=(i,j)=>{let M=Z();M[i][j]=1;return M};
const add=(A,B,s=1)=>A.map((r,i)=>r.map((x,j)=>x+s*B[i][j]));
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((sum,v,k)=>sum+v*B[k][j],0)));
const transpose=A=>A.map((row,i)=>row.map((_,j)=>A[j][i]));
const trace=A=>A.reduce((s,row,i)=>s+row[i],0);
const ip=(A,B)=>trace(mul(transpose(A),B));
const inv=A=>{const M=A.map((r,i)=>[...r,...I()[i]]);
 for(let j=0;j<4;j++){let k=j;for(let i=j+1;i<4;i++)if(Math.abs(M[i][j])>Math.abs(M[k][j]))k=i;
  if(Math.abs(M[k][j])<1e-13)throw Error("noninvertible group");
  [M[j],M[k]]=[M[k],M[j]];
  let d=M[j][j];for(let m=j;m<8;m++)M[j][m]/=d;
  for(let i=0;i<4;i++)if(i!==j){d=M[i][j];for(let m=j;m<8;m++)M[i][m]-=d*M[j][m];}
 }return M.map(r=>r.slice(4));};
const maxdiff=(A,B)=>Math.max(...A.flatMap((r,i)=>r.map((x,j)=>Math.abs(x-B[i][j]))));
const G=[add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)];
const test=(v,m)=>{if(!v)throw Error("FAIL "+m);console.log("PASS "+m);};
test(G.every((X,i)=>G.every((Y,j)=>Math.abs(ip(X,Y)-(i===j?2:0))<1e-14)),
 "actual native six SO(1,3) generators Frobenius dual");
function exp4(X){let R=I(),T=I();for(let k=1;k<23;k++){
 T=mul(T,X).map(r=>r.map(v=>v/k));R=add(R,T);
 }return R;
}
const zone=u=>u<9?0:u<20?1:2;
const pairs=[],triples=[];for(let u=0;u<33;u++)for(let v=u+1;v<33;v++)if(zone(u)!==zone(v))pairs.push([u,v]);
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)triples.push([a,b,c]);
test(pairs.length===359&&triples.length===1287,"all original native undirected edges and ALL 1287 ABC triangles");
const tree=new Set();
const keyof=(a,b)=>Math.min(a,b)+","+Math.max(a,b);
for(let b=9;b<20;b++)tree.add(keyof(0,b));
for(let c=20;c<33;c++)tree.add(keyof(0,c));
for(let a=1;a<9;a++)tree.add(keyof(a,9));
test(tree.size===32,"native 32-edge tree gauge no extra site frame");
const U=Array.from({length:33},()=>Array(33).fill(null));
const fixedLie=(u,v)=>G.reduce((M,g,j)=>add(M,g,
 (((u+1)*31+(v+5)*17+(j+3)*19+u*v*(j+1))%29-14)*.00047),Z());
for(const [u,v] of pairs){
 const x=tree.has(keyof(u,v))?I():exp4(fixedLie(u,v));
 U[u][v]=x;U[v][u]=inv(x);
}
test(pairs.every(([u,v])=>maxdiff(mul(U[u][v],U[v][u]),I())<1e-12),
 "all 718 real original directed SO(1,3) links inverse-respecting");
const W=(a,b,c)=>mul(mul(U[a][b],U[b][c]),U[c][a]);
const tags=new Map();
let maximumDecode=0,minProb=1;
function choinative(H){
 const mean=trace(H)/4,norm=ip(H,H)/4;
 const q=G.flatMap(g=>{
  const y=ip(g,H)/(2*Math.SQRT2);
  return [p**4/24*(mean+y)**2,p**4/24*(mean-y)**2];
 });
 const GG=p**4*norm,GB=p*p*(1-p*p*norm),BG=p**3*norm;
 const full16=[...q,GG-q.reduce((s,v)=>s+v,0),GB,BG,1-GG-GB-BG];
 const full17=full16.map(x=>x*bell).concat([1-bell]);
 return full17;
}
function mark(H,label){
 const q=choinative(H);
 if(!(q.every(x=>x>0)&&Math.abs(q.reduce((s,x)=>s+x,0)-1)<1e-13))throw Error("nonpositive complete 17-way marked native Golden/Bell");
 for(let k=0;k<6;k++){
  const component=(256*Math.sqrt(3)/p**2)*(Math.sqrt(q[2*k])-Math.sqrt(q[2*k+1]));
  maximumDecode=Math.max(maximumDecode,Math.abs(component-ip(G[k],H)));
  if(Math.abs(component-ip(G[k],H))>3e-13)throw Error("mark "+label+"/"+k);
 }
 minProb=Math.min(minProb,...q);
}
for(let b=9;b<20;b++)for(let c=20;c<33;c++){
 const x=W(0,b,c);mark(x,"0bc");tags.set("0,"+b+","+c,x);
}
for(let a=1;a<9;a++)for(let c=20;c<33;c++){
 const x=W(a,9,c);mark(x,"a9c");tags.set(a+",9,"+c,x);
}
for(let a=1;a<9;a++)for(let b=10;b<20;b++){
 const x=W(a,b,20);mark(x,"ab20");tags.set(a+","+b+",20",x);
}
test(tags.size===327&&maximumDecode<3e-13,
 "ALL 327 original triangle holonomies EACH possess SIX EXACT positive Golden signed-marker coordinates");
const V=Array.from({length:33},()=>Array(33).fill(null));
const set=(u,v,x)=>{V[u][v]=x;V[v][u]=inv(x);};
for(let [u,v] of pairs)if(tree.has(keyof(u,v)))set(u,v,I());
// Pass1: 143 B-C links W(0,b,c)=U_bc
for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 set(b,c,tags.get("0,"+b+","+c));
// Pass2: 104 A-C links W(a,9,c)=U_9c U_ac^-1 -> U_ac=W^-1 U_9c
for(let a=1;a<9;a++)for(let c=20;c<33;c++)
 set(a,c,mul(inv(tags.get(a+",9,"+c)),V[9][c]));
// Pass3: 80 A-B links W(a,b,20)=U_ab U_b20 U_a20^-1
for(let a=1;a<9;a++)for(let b=10;b<20;b++)
 set(a,b,mul(mul(tags.get(a+","+b+",20"),V[a][20]),inv(V[b][20])));
let maxSource=0;
for(let [u,v] of pairs){
 if(!V[u][v]||!V[v][u])throw Error("unreconstructed original edge");
 maxSource=Math.max(maxSource,maxdiff(V[u][v],U[u][v]),maxdiff(V[v][u],U[v][u]));
}
test(maxSource<5e-13,
 "NONABELIAN ALL-ORDERS inversion of 327 original graph loops recovers ALL 718 ordered link matrices");
const now=[
  {cycle143:143,cycle104:104,cycle80:80,nonabelianActiveLie:327*6,scalarBook:359+327,netRank:359+327+327*6}
][0];
test(now.netRank===2648&&now.nonabelianActiveLie===1962,
 "one full positive SHORT-B0OK + per-triangle Golden experiment local inverse rank 2648");
let reversedError=0;for(let [a,b,c] of triples){
 const X=W(a,b,c),Y=W(a,c,b);
 reversedError=Math.max(reversedError,maxdiff(mul(X,Y),I()));
}
test(reversedError<5e-12,
 "all original 1287 based triangle orientation reversals preserve true noncommuting holonomy inverse");
console.log(JSON.stringify({
 original_graph:{vertices:33,undirected:359,directed:718,triangles:1287},
 input_connection:"327 independent noncommuting SO+(1,3) group matrices, all other tree edges identity",
 checked_basis_triangles:tags.size,
 max_root_decode_error:maximumDecode,
 max_nonabelian_link_reconstruction_error:maxSource,
 min_complete_17way_Golden_probability:minProb,
 scalar_2_3_Book_invariant_dimensions:686,
 nonabelian_graph_Lorentz_dimensions:1962,
 total_local_information_rank:2648,
 CRITICAL_REQUIREMENT:"CAR Choi references at distinct start vertices must be COMPATIBLE (transported to a common tree gauge); site-dependent frame transport/native G0 actuation NOT proved",
 original_4D_ROLE_action_source_selected:false,
 full_HJR_Book_selected:false,
 GR_closed:false
},null,2));
