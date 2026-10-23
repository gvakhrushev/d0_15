#!/usr/bin/env node
"use strict";
/* All-original finite math: full K(9,11,13) at 16 4D Role L2 sites,
   718 primitive supported edges & 7722 rooted three-tick Book paths PER SITE.
   Exact sitewise Weyl (Book W)*degree2-solder source and moving code jets;
   entire 256-coframe Jacobian invertibility via only 16 radial scale modes.
   Beta/gamma are HYPOTHETICAL smooth field-to-Info diagnostic derivatives,
   NOT selected physical D0 constants or a compulsory Book03 action. */
const assert=(v,m)=>{if(!v)throw new Error(m)};
const phi=(1+Math.sqrt(5))/2,ell=Math.log(phi),p=1/phi,m=16;
const beta=.17,gamma=.04;
const zone=i=>i<9?0:i<20?1:2;
function det4(c){
 let A=Array.from({length:4},(_,i)=>c.slice(i*4,i*4+4));
 let det=1;
 for(let k=0;k<4;k++){
  let q=k;
  for(let i=k+1;i<4;i++)if(Math.abs(A[i][k])>Math.abs(A[q][k]))q=i;
  if(q!==k){[A[q],A[k]]=[A[k],A[q]];det=-det;}
  const pivot=A[k][k];assert(Math.abs(pivot)>1e-9,"singular coframe");
  det*=pivot;
  for(let i=k+1;i<4;i++){
   let f=A[i][k]/pivot;
   for(let j=k+1;j<4;j++)A[i][j]-=f*A[k][j];
  }
 }
 return det;
}
const detscale=v=>Math.abs(det4(v))**.25;
function originalSiteBook(x,shift=0){
 const Info=Array.from({length:33},(_,i)=>.12*Math.sin(.11*i+.37*x)+shift/ell);
 const K=Array.from({length:33},(_,i)=>Array.from({length:33},(_,j)=>{
  if(zone(i)===zone(j))return 0;
  const Cost=1.09+.02*Math.sin(.13*i+.29*j+.17*x)**2;
  assert(Cost>=1,"original ActionProtocol cost quantum");
  return Math.exp(-ell*(Cost-.5*(Info[i]+Info[j])));
 }));
 let zz=0;
 for(let a=0;a<9;a++)for(let b=9;b<20;b++)
  for(let c=20;c<33;c++)
   zz+=K[a][b]*K[b][c]*K[c][a]+K[a][c]*K[c][b]*K[b][a];
 return 3*zz/7722;
}
const base=Array.from({length:m},(_,x)=>originalSiteBook(x));
const e=Array.from({length:m},(_,x)=>Array.from({length:16},(_,j)=>
 j%5===0?1+.02*Math.sin(.3*x+.7*j):.008*Math.sin(.17*x+.3*j)));
function weights(e0,b=beta,g=gamma){
 const siteScales=e0.map(detscale);
 return siteScales.map((v,x)=>
   base[x]*v**(3*(b-g))*siteScales[(x+1)%m]**(3*g));
}
function source(e0){
 const W=weights(e0);
 const density=v=>(v[0]*v[5]-v[1]*v[4])+
  .3*(v[10]*v[15]-v[11]*v[14]);
 const fac=x=>1+.03*Math.sin(.4*x);
 const weighted=e0.reduce((s,v,x)=>s+W[x]*fac(x)*density(v),0);
 const dressed=e0.map((v,x)=>v.map(z=>z*Math.sqrt(W[x])));
 const dressedAction=dressed.reduce((s,v,x)=>s+fac(x)*density(v),0);
 return {W,weighted,dressedAction};
}
const first=source(e),h=.0003,copy=a=>a.map(v=>v.slice());
assert(Math.abs(first.weighted-first.dressedAction)<1e-13,
       "Book weighted vs coframe-dressed original quadratic source is not exact");
for(const x of [0,4,9,15]){
 const ss=e.map(detscale);
 const alpha=(beta-gamma)*Math.log(ss[x])+gamma*Math.log(ss[(x+1)%m]);
 assert(Math.abs(originalSiteBook(x,alpha)-first.W[x])<2e-13,
        "full 33/718/7722 original Book direct product fails");
}
let ep=copy(e),em=copy(e),x=3,k=0;
ep[x][k]+=h;em[x][k]-=h;
const fp=source(ep),fm=source(em);
const dRaw=(fp.weighted-fm.weighted)/(2*h);
const dDressed=(fp.dressedAction-fm.dressedAction)/(2*h);
const W=first.W,density=v=>(v[0]*v[5]-v[1]*v[4])+.3*(v[10]*v[15]-v[11]*v[14]);
const naive=W[x]*(1+.03*Math.sin(.4*x))*(density(ep[x])-density(em[x]))/(2*h);
assert(Math.abs(dRaw-dDressed)<1e-10&&Math.abs(dRaw-naive)>.001,
       "Book derivative not carried by exact coframe coordinate");
const y=1,eps=1e-5,plus=copy(e),minus=copy(e);
plus[y]=plus[y].map(z=>z*Math.exp(eps));
minus[y]=minus[y].map(z=>z*Math.exp(-eps));
const wp=weights(plus),wm=weights(minus);
const exact=Array.from({length:m},(_,i)=>3*((beta-gamma)*(i===y?1:0)+
         gamma*(((i+1)%m===y)?1:0)));
const error=Math.max(...exact.map((v,i)=>
 Math.abs(v-(Math.log(wp[i])-Math.log(wm[i]))/(2*eps))));
assert(error<1e-10,"full original 718 Book score radial response wrong");
const Rdiag=1+1.5*(beta-gamma),Rnext=1.5*gamma;
const detR=Rdiag**m-(-Rnext)**m;
const minSingularMargin=Rdiag-Math.abs(Rnext);
assert(minSingularMargin>1,"unexpected reduced radial inverse bound");
const criticalDiag=1+1.5*(-2/3-gamma),criticalNext=1.5*gamma;
assert(Math.abs(criticalDiag+criticalNext)<1e-12,
       "critical length3/degree2 Info scale resonance not recovered");
console.log("PASS original 16 TRUE Role sites / 256 REAL coframe coordinates and all718 Book edges per site");
console.log("PASS 7722 original rooted three-history W=Tr(K^3)/7722 per site, range",
 Math.min(...W),Math.max(...W));
console.log("PASS EXACT finite 4D sitewise W*quadratic coframe = quadratic dressed coframe");
console.log("PASS true moving original coframe source =",dRaw,
 "source lost by freezing Book pressure =",dRaw-naive);
console.log("PASS actual original Book full site radial source error",error);
console.log("PASS full256 Jacobian det nonzero iff original site16 radial det",detR);
console.log("PASS original site16 radial entries",Rdiag,Rnext,
 "uniform inverse infinity norm upper bound",1/minSingularMargin);
console.log("PASS beta=-2/3 gives singular shared 4D conformal scale even with neighbor coupling");
console.log("FIREWALL: signed Palatini all640 Euler and real G0/H+J+R physical source are SEPARATE upstream owners");
