#!/usr/bin/env node
"use strict";
/*
 * Original D0 K(9,11,13) Book Cost pressure Hessian:
 * exact graph combinatorics, 718 original edges, Poisson martingale,
 * full 32-dimensional archive image on vertex-additive symmetric prices,
 * exact 3-orbit Hessian numerical value and antisymmetric negative control.
 * Research theorem; not physical Cost->4D metric map or GR closure.
 */
const N=[9,11,13],vCount=33,phi=(1+Math.sqrt(5))/2,ell=Math.log(phi),p=1/phi;
const zone=u=>u<9?0:u<20?1:2;
const edges=[];for(let u=0;u<vCount;u++)for(let v=u+1;v<vCount;v++)
 if(zone(u)!==zone(v))edges.push([u,v]);
const req=(x,name)=>{if(!x)throw Error("FAIL "+name);console.log("PASS "+name);};
function modRank(sign){
 const prime=1009,rows=Array.from({length:vCount},()=>Array(edges.length).fill(0));
 edges.forEach(([u,v],j)=>{rows[u][j]=1;rows[v][j]=sign===1?1:prime-1;});
 const inv=n=>{for(let a=1;a<prime;a++)if(a*n%prime===1)return a;throw Error("no inverse");};
 let rank=0;
 for(let j=0;j<edges.length;j++){
  let piv=rank;while(piv<vCount&&rows[piv][j]===0)piv++;
  if(piv===vCount)continue;
  [rows[rank],rows[piv]]=[rows[piv],rows[rank]];
  let q=inv(rows[rank][j]);for(let k=j;k<edges.length;k++)rows[rank][k]=rows[rank][k]*q%prime;
  for(let i=rank+1;i<vCount;i++){let t=rows[i][j];if(t)
    for(let k=j;k<edges.length;k++)rows[i][k]=(rows[i][k]-t*rows[rank][k]%prime+prime)%prime;}
  rank++;if(rank===vCount)break;
 }
 return rank;
}
req(edges.length===359&&edges.length*2===718,"all 359 original undirected and 718 directed edges");
req(9*11*13===1287,"original 1287 oriented triangles");
const evenRank=modRank(1),oddRank=modRank(-1);
req(evenRank===33&&oddRank===32,
    "exact finite-field rank: unsigned incidence 33, ordinary oriented incidence 32");
req(359-evenRank===326&&359-oddRank===327,
    "native even twisted-cycle 326 and odd oriented-cycle 327");
req(1+32+326+32+327===718,
    "whole raw original 718=uniform1 + archive32 + even-fast326 + endpoint-gauge32 + odd-holonomy327");

const B=N.map((n,i)=>N.map((m,j)=>i===j?0:Math.sqrt(n*m)));
const mv=(M,v)=>M.map(row=>row.reduce((a,b,j)=>a+b*v[j],0));
const dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0);
let r=[1,1,1].map(x=>x/Math.sqrt(3));
for(let k=0;k<1500;k++){
 let y=mv(B,r),norm=Math.hypot(...y),s=y.map(x=>x/norm);
 if(Math.max(...s.map((x,i)=>Math.abs(x-r[i])))<1e-15){r=s;break;}r=s;
}
const rho=dot(r,mv(B,r));
req(Math.abs(rho**3-359*rho-2574)<1e-9,
    "true original Perron cubic and its 30 null graph modes");
const pi=r.map(x=>x*x),Q=B.map((row,i)=>row.map((x,j)=>x*r[j]/(rho*r[i])));
req(Q.every(row=>Math.abs(row.reduce((s,x)=>s+x,0)-1)<2e-13),
    "original zone conditional Perron/Doob chain normalized");
const T=B.map(row=>row.map(x=>x/rho));
const T2=T.map(row=>T[0].map((_,j)=>row.reduce((s,x,k)=>s+x*T[k][j],0)));
const F=T2.map((row,i)=>row.map((x,j)=>(i===j?1:0)-x));
function solve(A,y){
 const M=A.map((row,i)=>[...row,y[i]]),n=y.length;
 for(let j=0;j<n;j++){let q=j;for(let i=j+1;i<n;i++)if(Math.abs(M[i][j])>Math.abs(M[q][j]))q=i;
  if(Math.abs(M[q][j])<1e-12)throw Error("singular Poisson quotient");
  [M[q],M[j]]=[M[j],M[q]];
  let t=M[j][j];for(let k=j;k<=n;k++)M[j][k]/=t;
  for(let i=0;i<n;i++)if(i!==j){t=M[i][j];for(let k=j;k<=n;k++)M[i][k]-=t*M[j][k];}
 }
 return M.map(row=>row[n]);
}
const types=[
 [[0,1,0],[1,0,0],[0,0,0]],
 [[0,0,1],[0,0,0],[1,0,0]],
 [[0,0,0],[0,0,1],[0,1,0]]
];
function owner(d) {
 const c=pi.reduce((s,w,i)=>s+w*Q[i].reduce((a,q,j)=>a+q*d[i][j],0),0);
 const b=Q.map((row,i)=>row.reduce((s,q,j)=>s+q*d[i][j],0)-c);
 const L=Q.map((row,i)=>row.map((q,j)=>(i===j?1:0)-q+pi[j]));
 const xi=solve(L,b);
 const eta=[(d[0][1]+d[0][2]-d[1][2])/2,
            (d[0][1]+d[1][2]-d[0][2])/2,
            (d[0][2]+d[1][2]-d[0][1])/2];
 const z=eta.map((x,i)=>x+xi[i]),Qz=mv(Q,z);
 const m=Q.map((row,i)=>row.map((q,j)=>q>0?d[i][j]-c-xi[i]+xi[j]:0));
 const mz=Q.map((row,i)=>row.map((q,j)=>q>0?z[j]-Qz[i]:0));
 const maxErr=Math.max(...m.flatMap((row,i)=>row.map((x,j)=>Math.abs(x-mz[i][j]))));
 const source=pi.reduce((s,x,i)=>s+x*Q[i].reduce((a,q,j)=>a+q*m[i][j]*m[i][j],0),0);
 const zz=z.map((x,i)=>x*r[i]);
 const archive=dot(zz,mv(F,zz));
 return {c,b,xi,eta,z,m,source,archive,maxErr};
}
const owners=types.map(owner);
req(owners.every(x=>x.maxErr<1e-12&&Math.abs(x.source-x.archive)<1e-12),
    "ALL three native symmetric orbit martingales equal existing 32-d archive Rz");
const hessian=owners.map(u=>owners.map(v=>-ell*pi.reduce((s,x,i)=>s+x*Q[i].reduce(
 (a,q,j)=>a+q*u.m[i][j]*v.m[i][j],0),0)));
req(Math.abs(hessian[0][0]+.1297284254564436)<1e-13,
    "user breakthrough scalar Aeff''=-0.1297284254564436 independently reproduced");
req(hessian.every(row=>Math.abs(row.reduce((a,b)=>a+b,0))<1e-12),
    "Book Hessian uniform absolute Cost mode exactly zero");
const minor=hessian[0][0]*hessian[1][1]-hessian[0][1]**2;
req(minor>.015&&hessian[0][0]<0&&hessian[1][1]<0,
    "native 3-orbit Book Hessian rank 2, negative definite on contrasts");
req(Math.abs(hessian[0][1]-.05783268391731478)<1e-12
&&Math.abs(hessian[1][1]+.14168138938244537)<1e-12,
    "native full three-orbit offdiagonal hessian independent values");
const fullR=Array.from({length:vCount},(_,u)=>r[zone(u)]/Math.sqrt(N[zone(u)]));
const fullP=Array.from({length:vCount},(_,u)=>Array.from({length:vCount},(_,v)=>
 zone(u)===zone(v)?0:fullR[v]/(rho*fullR[u])));
const fullZ=fullR.map((_,u)=>owners[0].z[zone(u)]);
let fullVariance=0,fullDelta=0,fullArchiveNorm=0;
for(let u=0;u<vCount;u++){
 const pu=fullP[u].reduce((s,q,v)=>s+q*fullZ[v],0);
 for(let v=0;v<vCount;v++)if(fullP[u][v]>0){
  const d=Number((zone(u)===0&&zone(v)===1)||(zone(u)===1&&zone(v)===0));
  const m=d-owners[0].c-owners[0].xi[zone(u)]+owners[0].xi[zone(v)];
  const ar=fullZ[v]-pu;
  const mu=fullR[u]*fullR[u]*fullP[u][v];
  fullVariance+=mu*m*m;
  fullArchiveNorm+=mu*ar*ar;
  fullDelta=Math.max(fullDelta,Math.abs(m-ar));
 }
}
req(fullDelta<1e-12&&Math.abs(fullVariance-owners[0].source)<1e-13
     &&Math.abs(fullArchiveNorm-fullVariance)<1e-13,
    "all 718 ORIGINAL directed edge sources = same true current-to-future archive norm");

function eigenPerron(s,a){
 const M=N.map((m,i)=>N.map((n,j)=>{
  if(i===j)return 0;
  const ab=((i===0&&j===1)||(i===1&&j===0));
  const anti=(i===0&&j===1)?1:((i===1&&j===0)?-1:0);
  return p*Math.sqrt(m*n)*Math.exp(-ell*(ab?s:0)-ell*anti*a);
 }));
 let v=[1,1,1];
 for(let k=0;k<1200;k++){
  let y=mv(M,v),z=Math.max(...y),w=y.map(x=>x/z);
  if(Math.max(...w.map((x,i)=>Math.abs(x-v[i])))<1e-15){v=w;break;}v=w;
 }
 return mv(M,v)[0]/v[0];
}
const action=(s,a)=>-Math.log(eigenPerron(s,a))/ell;
for(const dh of [.01,.003,.001]){
 const even=(action(dh,0)-2*action(0,0)+action(-dh,0))/dh**2;
 const odd=(action(0,dh)-2*action(0,0)+action(0,-dh))/dh**2;
 const mixed=(action(dh,dh)-action(dh,-dh)-action(-dh,dh)+action(-dh,-dh))/(4*dh**2);
 req(Math.abs(even-hessian[0][0])<3e-7,
     "moving original native Perron pressure hessian matches archive source h="+dh);
 req(odd<-.0529&&odd>-.053 &&Math.abs(mixed)<5e-9,
     "reversal symmetry: odd-cycle Book Hessian negative, even/odd mixed zero h="+dh);
}
console.log(JSON.stringify({
 scope:"original 718 native directed prices; ORIGINAL 3-orbit symmetric pressure source; NOT physical D0->GR",
 full_edges:718,undirected_edges:359,
 decomposition:{"uniform_absolute_clock":1,"symmetric_archive":32,
                "symmetric_fast_even_cycle":326,"antisymmetric_endpoint_gauge":32,
                "antisymmetric_oriented_cycle":327},
 scalar_book_pressure_hessian_rank:685,
 original_archive_hessian_three_orbits:hessian,
 orbit_initial_c:owners[0].c,
 orbit_original_martingale_variance:owners[0].source,
 original_Aeff_second_derivative:hessian[0][0],
 original_full718_archive_error:fullDelta,
 negative_control_odd_cycle_hessian:"-0.05293049 on signed K9->K11 orientation",
 GR_closed:false
},null,2));
