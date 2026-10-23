#!/usr/bin/env node
"use strict";
// Original 718-edge K9/K11/K13 Perron/Book source (exact zone-symmetry
// 3x3 reduction plus retained 30 T-zero modes). NOT a physical gravity source.
const p=(Math.sqrt(5)-1)/2,phi=1/p,l=Math.log(phi),z=2**-20;
const A=[[0,Math.sqrt(99),Math.sqrt(117)],
         [Math.sqrt(99),0,Math.sqrt(143)],
         [Math.sqrt(117),Math.sqrt(143),0]];
const mv=(M,v)=>M.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));
const mm=(X,Y)=>X.map(row=>Y[0].map((_,j)=>row.reduce((s,x,k)=>s+x*Y[k][j],0)));
const dot=(x,y)=>x.reduce((s,v,i)=>s+v*y[i],0);
const tr=X=>X.reduce((s,row,i)=>s+row[i],0);
const det=M=>M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]);
const check=(v,name)=>{if(!v)throw Error("FAIL "+name);console.log("PASS "+name);};
const K=t=>A.map((row,i)=>row.map((x,j)=>p*x*Math.exp(-l*t*((i===0&&j===1)||(i===1&&j===0)?1:0))));
function pf(M){let v=Array(3).fill(1/Math.sqrt(3));for(let n=0;n<800;n++){let y=mv(M,v),norm=Math.hypot(...y),w=y.map(a=>a/norm);if(Math.max(...w.map((x,i)=>Math.abs(x-v[i])))<2e-15){v=w;break;}v=w;}return {r:v,rho:dot(v,mv(M,v))};}
const I3=Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>+(i===j)));
function native(t){const M=K(t),{rho}=pf(M),T=M.map(row=>row.map(x=>x/rho)),T2=mm(T,T);const G=T2.map((row,i)=>row.map((x,j)=>(i===j?1-z:0)+z*x));return {rho,T,G,J:-30*Math.log1p(-z)-Math.log(det(G))};}
const x=native(0),{r}=pf(K(0));const M=K(0),dM=M.map((row,i)=>row.map((x,j)=>-l*x*((i===0&&j===1)||(i===1&&j===0)?1:0)));const drho=dot(r,mv(dM,r));
const dT=dM.map((row,i)=>row.map((v,j)=>v/x.rho-x.T[i][j]*drho/x.rho));
const inv3=G=>G.map((row,i)=>row.map((v,j)=>{const rr=[0,1,2].filter(k=>k!==j),cc=[0,1,2].filter(k=>k!==i);return ((i+j)%2?-1:1)*(G[rr[0]][cc[0]]*G[rr[1]][cc[1]]-G[rr[0]][cc[1]]*G[rr[1]][cc[0]])/det(G);}));
const dJ=-2*z*tr(mm(mm(inv3(x.G),x.T),dT));
check(Math.abs(x.J-0.000030035369315208)<3e-13,"original 718 history Book candidate determinant");
check(Math.abs(dJ+2.6251653530422938e-8)<4e-13&&dJ!==0,"actual native K9-K11 orbit price first source");
let prev=Infinity;for(const h of [.03,.01,.003]){const fd=(native(h).J-native(-h).J)/(2*h),e=Math.abs(fd-dJ);check(e<prev&&e<2e-11,"original moving Perron central derivative h="+h);prev=e;}
const c=.07,scaled=M.map(row=>row.map(v=>v*phi**(-c))),sv=pf(scaled),Tnew=scaled.map(row=>row.map(v=>v/sv.rho));
check(Tnew.every((row,i)=>row.every((v,j)=>Math.abs(v-x.T[i][j])<2e-13))&&Math.abs(Math.log(sv.rho/x.rho)/l+c)<1e-12,"uniform native Cost leaves archive feedback but changes absolute history pressure");
console.log(JSON.stringify({actual_original_edge_count:718,J:x.J,dJ_native_cost_K9K11:dJ,gr_closed:false},null,2));
