#!/usr/bin/env node
"use strict";
// ORIGINAL K(9,11,13): all 718 directed scalar Book edges.
// From ONE normalized mixture of ALL real 2- and 3-step based returns,
// EXACTLY 718+7722=8440 positive history probabilities, with known
// attempted native Golden 2/3-depth factors a2=p,a3=p², recover:
// (i) the absolute raw Book clock normalizer; (ii) all 359 backtrack
// products; (iii) 327 signed cycle log affinities; (iv) 718 weights
// modulo 32 endpoint/coboundary gauges; and original absolute Perron
// Book action and actual derivatives. Actual physical joint-depth G0
// admission/clock attempt prices remain UNKNOWN. NO GR promotion.
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),n=33,a2=p,a3=p*p;
const zone=u=>u<9?0:u<20?1:2,ok=(x,m)=>{if(!x)throw Error("FAIL "+m);console.log("PASS "+m);};
const edge=[],triangle=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)
 if(zone(u)!==zone(v))edge.push([u,v]);
for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
 triangle.push([a,b,c]);
ok(edge.length===359&&triangle.length===1287,"TRUE original 359 undirected edges, 1287 ABC triangles");
const matrix=()=>Array.from({length:n},()=>Array(n).fill(0));
const dot=(x,y)=>x.reduce((s,v,j)=>s+v*y[j],0);
function KNative(t){
 const K=matrix();
 for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(zone(u)!==zone(v)){
  const primitive=1+((3*u+7*v+2)%17)/95+t*(1+((u+2*v)%5)/6);
  const trueInfo=.008*(u+v)/2;
  if(primitive<1)throw Error("invalid original Cost floor");
  K[u][v]=Math.exp(-ell*(primitive-trueInfo));
 }
 return K;
}
function fullClock(K){
 const doubles=edge.map(([u,v])=>({u,v,raw:K[u][v]*K[v][u]}));
 const triples=triangle.map(([a,b,c])=>({a,b,c,
  f:K[a][b]*K[b][c]*K[c][a],
  r:K[a][c]*K[c][b]*K[b][a]}));
 const Z2=doubles.reduce((s,x)=>s+2*x.raw,0),
       Z3=triples.reduce((s,x)=>s+3*(x.f+x.r),0),
       Z=a2*Z2+a3*Z3;
 const d=doubles.map(x=>({...x,q:a2*x.raw/Z}));
 const t=triples.map(x=>({...x,qf:a3*x.f/Z,qr:a3*x.r/Z}));
 const sum=d.reduce((s,x)=>s+2*x.q,0)+t.reduce((s,x)=>s+3*(x.qf+x.qr),0);
 ok(Math.abs(sum-1)<5e-13,"8440 real 2/3-based closed-history probabilities all supported, normalized together");
 return {d,t,Z2,Z3,Z};
}
function PF(K){
 let x=Array(n).fill(1/Math.sqrt(n));
 for(let j=0;j<1800;j++){
  const y=K.map(row=>dot(row,x)),norm=Math.hypot(...y),z=y.map(v=>v/norm);
  if(Math.max(...z.map((v,i)=>Math.abs(v-x[i])))<8e-16){x=z;break;}
  x=z;
 }
 return dot(x,K.map(row=>dot(row,x)));
}
function invert(obs,K){
 const d2=new Map(obs.d.map(e=>[e.u+","+e.v,e.q]));
 const paired=(u,v)=>d2.get(Math.min(u,v)+","+Math.max(u,v));
 const e0=obs.t.find(x=>x.a===0&&x.b===9&&x.c===20);
 const invZ=(a3*a3/(a2*a2*a2))*
   paired(0,9)*paired(9,20)*paired(0,20)/(e0.qf*e0.qr);
 ok(Math.abs(invZ-1/obs.Z)<1e-13,
  "one original triangle + three backtracks fix TRUE absolute 2/3 Book clock partition");
 const r=Array.from({length:n},()=>Array(n).fill(null)),s=matrix();
 const set=(u,v,w)=>{r[u][v]=w;r[v][u]=-w;};
 const ks=new Map(obs.t.map(x=>[x.a+","+x.b+","+x.c,.5*Math.log(x.qf/x.qr)]));
 for(let b=9;b<20;b++)set(0,b,0);
 for(let c=20;c<33;c++)set(0,c,0);
 for(let a=1;a<9;a++)set(a,9,0);
 for(let b=9;b<20;b++)for(let c=20;c<33;c++)
  set(b,c,ks.get("0,"+b+","+c)); // 143 ORIGINAL B-C
 for(let a=1;a<9;a++)for(let c=20;c<33;c++)
  set(a,c,r[9][c]-ks.get(a+",9,"+c)); // 104 A-C
 for(let a=1;a<9;a++)for(let b=10;b<20;b++)
  set(a,b,ks.get(a+","+b+",20")-r[b][20]+r[a][20]); // 80 A-B
 ok(edge.every(([u,v])=>r[u][v]!==null),
  "explicit exact 32-tree + 143+104+80=327 original cycles solved by REAL triangular odds");
 for(let {u,v,q} of obs.d){
  const even=.5*Math.log(q/(invZ*a2));
  s[u][v]=Math.exp(even+r[u][v]);s[v][u]=Math.exp(even-r[u][v]);
 }
 const chi=Array(n).fill(null);chi[0]=0;
 const asym=(u,v)=>.5*Math.log(K[u][v]/K[v][u]);
 for(let b=9;b<20;b++)chi[b]=asym(0,b);
 for(let c=20;c<33;c++)chi[c]=asym(0,c);
 for(let a=1;a<9;a++)chi[a]=chi[9]+asym(9,a);
 let err=0;
 for(let [u,v] of edge)for(let [x,y] of [[u,v],[v,u]])
  err=Math.max(err,Math.abs(Math.log(s[x][y])-
                         (Math.log(K[x][y])+chi[x]-chi[y])));
 ok(err<8e-12,
  "every single one of original 718 directed Cost-Info weights recovered modulo ONLY 32 endpoint coboundaries");
 let recoveredZ2=0,recoveredZ3=0;
 for(let [u,v] of edge)recoveredZ2+=2*s[u][v]*s[v][u];
 for(let [a,b,c] of triangle)
  recoveredZ3+=3*(s[a][b]*s[b][c]*s[c][a]
                    +s[a][c]*s[c][b]*s[b][a]);
 ok(Math.abs(recoveredZ2-obs.Z2)<4e-11&&Math.abs(recoveredZ3-obs.Z3)<1e-8,
  "all 8440 original raw loop weights reconstructed with same absolute book partition");
 const root=PF(K),rootReconstructed=PF(s);
 ok(Math.abs(root-rootReconstructed)<1e-12,
  "entire ORIGINAL absolute Perron scalar and Book minimized action preserved");
 return {root,action:-Math.log(rootReconstructed)/ell,
         invZ,fullReconstructionMaxLogGaugeError:err};
}
const attempts=[];
for(let t of [0,.017,.041]){
 const original=KNative(t),rec=invert(fullClock(original),original);
 attempts.push({t,...rec});
}
const h=.0001,advanced=invert(fullClock(KNative(h)),KNative(h));
const derivative=(advanced.action-attempts[0].action)/h;
ok(Number.isFinite(derivative)&&Math.abs(derivative)>.02,
  "moving TRUE primitive Cost supplies nonzero first absolute Book Euler through observed 2/3-clock records");
console.log(JSON.stringify({
 outcome_count:2*359+6*1287,
 original_directed_costs:718,scalar_equivalence_dimensions:686,
 surviving_endpoint_gauge:32,
 actual_native_K9_11_13_2_3_depth_programme:"mathematically defined raw Book clock, admission and priors NOT owned",
 prior_two_three_attempt:[a2,a3],
 same_real_original_Book_source:derivative,checks:attempts,
 native_Book_full_selected:false,
 original_G0_multi_depth_readout_admitted:false,GR_closed:false
},null,2));
