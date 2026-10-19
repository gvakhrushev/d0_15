#!/usr/bin/env node
// TRUE original six based plaquettes, all independent 16 coframe + 24
// proper Lorentz left-link first variations on a double-null affine carrier.
// Uses continuum Levi-Civita links U=exp(h omega) ONLY as a trial.
// Does not claim stationary finite double-null roots. Standard Node only.
import assert from 'node:assert/strict';
const N=4,I=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>+(i===j)));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const basis=(a,b)=>I.map((r,i)=>r.map((_,j)=>+(i===a&&j===b)));
const add=(A,B)=>A.map((r,i)=>r.map((v,j)=>v+B[i][j]));
const sub=(A,B)=>A.map((r,i)=>r.map((v,j)=>v-B[i][j]));
const sc=(A,c)=>A.map(r=>r.map(v=>c*v));
const mul=(A,B)=>A.map(r=>r.map((_,j)=>r.reduce((v,x,k)=>v+x*B[k][j],0)));
const tr=A=>A[0].map((_,i)=>A.map(r=>r[i]));
const invL=A=>mul(mul(eta,tr(A)),eta);
const zero=()=>sc(I,0);
const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const epsilon=(...z)=>{
  if(new Set(z).size!==4)return 0;
  let sign=1;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)if(z[i]>z[j])sign=-sign;
  return sign;
};
const Nplus=[add(basis(1,2),basis(2,0)),add(basis(1,3),basis(3,0))];
const Nminus=[add(basis(0,2),basis(2,1)),add(basis(0,3),basis(3,1))];
const B=sub(basis(1,1),basis(0,0)),Rot=sub(basis(2,3),basis(3,2));
const gens=[B,Nminus[0],Nminus[1],Nplus[0],Nplus[1],Rot];
function expm(A){
 let U=A,s=Math.max(...A.flat().map(Math.abs)),scaleCount=0;
 while(s>0.2){U=sc(U,0.5);s*=0.5;scaleCount++}
 let sum=I,term=I;
 for(let k=1;k<=18;k++){term=sc(mul(term,U),1/k);sum=add(sum,term)}
 while(scaleCount--)sum=mul(sum,sum);
 return sum;
}
function compute(A,B,z,h){
 const cache=new Map(),shift=(p,axis,k=1)=>p.map((x,i)=>x+(axis===i?k*h:0));
 function site(p) {
  const key=p.join(',');
  if(cache.has(key))return cache.get(key);
  const x=p[2],y=p[3],H=A[0]*x+A[1]*y,J=B[0]*x+B[1]*y,Omega=1-H*J/4;
  assert.ok(Math.abs(Omega)>0.2);
  const e=[[1,J/2,0,0],[H/2,1,0,0],[0,0,1,0],[0,0,0,1]];
  const wb=[zero(),zero(),zero(),zero()];
  for(let i=0;i<2;i++) {
    const a=A[i]/(2*Omega),b=B[i]/(2*Omega);
    const c=-(H*B[i]+J*A[i])/(8*Omega),d=(J*A[i]-H*B[i])/(8*Omega);
    wb[0]=add(wb[0],add(sc(Nplus[i],a),sc(Nminus[i],c)));
    wb[1]=add(wb[1],add(sc(Nplus[i],c),sc(Nminus[i],b)));
    wb[i+2]=add(wb[i+2],sc(B===null?I:gens[0],d));
  }
  const wc=Array.from({length:4},(_,mu)=>wb.reduce((acc,X,j)=>add(acc,sc(X,e[j][mu])),zero()));
  const ret={e:e.map(row=>row.map(v=>h*v)),U:wc.map(X=>expm(sc(X,h)))};
  cache.set(key,ret);return ret;
 }
 const edges=(p,r,t)=>[[p,r,false],[shift(p,r),t,false],[shift(p,t),r,true],[p,t,true]];
 const U=(p,a,back)=>{let X=site(p).U[a];return back?invL(X):X};
 const pair=(e,u,v,R)=>{
  const C=mul(R,eta);let val=0;
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
    const [c,d]=[0,1,2,3].filter(k=>k!==a&&k!==b);
    val+=epsilon(a,b,c,d)*(e[a][u]*e[b][v]-e[b][u]*e[a][v])*C[c][d];
  }return val;
 };
 const plaque=(p,r,t)=>edges(p,r,t).reduce((cur,[pos,axis,back])=>mul(cur,U(pos,axis,back)),I);
 const dpla=(p,r,t,target,axis,X)=>{
  let P=I,dP=zero();
  for(let [pos,a,back] of edges(p,r,t)){
    const V=U(pos,a,back),hit=pos.every((x,i)=>Math.abs(x-target[i])<1e-13)&&a===axis;
    const dV=hit?(back?sc(mul(V,X),-1):mul(X,V)):zero();
    dP=add(mul(dP,V),mul(P,dV));P=mul(P,V);
  }
  return {P,dP};
 };
 const solder=Array.from({length:4},()=>Array(4).fill(0)),
       links=Array.from({length:4},()=>Array(6).fill(0));
 let density=0;
 for(let [r,t] of pairs){
  const [u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t),
       sign=epsilon(r,t,u,v),P=plaque(z,r,t),
       R=sc(sub(P,invL(P)),0.5),ez=site(z).e;
  density+=sign*pair(ez,u,v,R);
  for(let a=0;a<4;a++){
    let S=ez.map(row=>row.slice());
    for(let b=0;b<4;b++)S[b][u]=I[b][a];
    solder[a][u]+=sign*pair(S,u,v,R);
    S=ez.map(row=>row.slice());
    for(let b=0;b<4;b++)S[b][v]=I[b][a];
    solder[a][v]+=sign*pair(S,u,v,R);
  }
 }
 for(let axis=0;axis<4;axis++)for(let j=0;j<6;j++)for(let [r,t] of pairs){
  if(axis!==r&&axis!==t)continue;
  const other=axis===r?t:r,[u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t);
  for(let base of [z,shift(z,other,-1)]){
    const {P,dP}=dpla(base,r,t,z,axis,gens[j]),Q=invL(P);
    const dR=sc(add(dP,mul(mul(Q,dP),Q)),0.5);
    links[axis][j]+=epsilon(r,t,u,v)*pair(site(base).e,u,v,dR);
  }
 }
 const norm=M=>Math.max(...M.flat().map(Math.abs));
 return {h,density,solder,links,maxS:norm(solder),maxL:norm(links),
         uRot:links[0][5],vRot:links[1][5]};
}
const z=[0,0,0.2,0.3],h=1/8;
for(const [A,B] of [[[1,0],[0,0]],[[0,0],[0,1]]]){
 const r=compute(A,B,z,h);
 assert.ok(r.maxS<1e-11&&r.maxL<1e-11,'single affine pp branch must be exact full40 vacuum');
}
const a=compute([1,0],[0,1],z,h),b=compute([1,0],[0,1],z,h/2);
assert.ok(a.maxS>1e-7&&a.maxL>1e-7);
assert.ok(a.uRot*a.vRot<0,'rotation link rows have opposite signs');
assert.ok(Math.abs((a.maxS/b.maxS)-8)<0.3,'solder source scales h^3 locally');
assert.ok(Math.abs((a.maxL/b.maxL)-16)<0.8,'link source scales h^4 locally');
const parallel=compute([1,0],[1,0],z,h);
console.log('PASS: each one-sided affine pp geometry is an exact 16+24 finite root');
console.log('PASS: crossed continuum-LC trial is NOT finite stationary');
console.log(JSON.stringify({h,orthogonal:{maxS:a.maxS,maxL:a.maxL,uRot:a.uRot,vRot:a.vRot},
 half:{maxS:b.maxS,maxL:b.maxL,uRot:b.uRot,vRot:b.vRot},
 parallel:{maxS:parallel.maxS,maxL:parallel.maxL,uRot:parallel.uRot,vRot:parallel.vRot}},null,2));
console.log('SCOPE: bounded original six-plaquette numeric first sources; NOT finite exact solution.');
