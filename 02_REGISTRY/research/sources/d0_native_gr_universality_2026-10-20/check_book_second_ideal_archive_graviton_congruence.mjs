#!/usr/bin/env node
"use strict";
/*
  REAL native K(9,11,13), 33 vertices/718 directed primitive Book edges,
  16 real L2 Role SITE LABELS, 48-site radial/coframe/shared-link
  representative source SUBSECTOR, ONE native chiral history variable.

  Verifies the NEW algebraic theorem for a selected MATHEMATICAL
  ActionProtocol-admissible Book PRESSURE candidate:
    S=B(z)+sum w_i(z) t_i(q)+sum t_i t_j R_ij(q,z).
  Full source is actually -log_phi Perron(K(t(q),z,q)).
  The original physically compulsory G0/Book03 H+J+R and ALL640 Role Euler
  are NOT demonstrated or selected by this numerical regression.
*/
const assert=(x,msg)=>{if(!x)throw Error(msg)};
const phi=(1+Math.sqrt(5))/2,logphi=Math.log(phi),N=16,D=3*N,Kdim=33;
const zone=i=>i<9?0:i<20?1:2;
const chiral=Array.from({length:13},(_,j)=>
 .4*Math.sin(.3+j*.73)+.5*Math.cos(j*.29));
const selected=Array.from({length:N},(_,i)=>[9+Math.floor(i/13),20+(i%13)]);
const flatE=()=>Array.from({length:N},()=>[1,1]);
const zeros=()=>Array(N).fill(0);
function nativeK(z,f=zeros(),e=flatE(),hostile=0){
 const K=Array.from({length:Kdim},()=>Array(Kdim).fill(0));
 for(let i=0;i<Kdim;i++)for(let j=0;j<Kdim;j++)
  if(zone(i)!==zone(j))K[i][j]=phi**(-1.1);
 for(let c=0;c<13;c++){
  let a=9,b=20+c;
  K[a][b]*=Math.exp(z*chiral[c]);
  K[b][a]*=Math.exp(-z*chiral[c]);
 }
 for(let i=0;i<N;i++){
  let [a,b]=selected[i],t=f[i];
  // GENUINE directional positive native edge cost on one of the 143
  // ORIGINAL B-C chords; q-shape enters at second order in t,
  // so this pressure is NOT a function of (t,z) alone.
  K[a][b]*=Math.exp(-.8*t+.09*t*t*
       (1+.5*(e[i][0]-1)+.1*(e[i][1]-1)));
 }
 // Independent first-order "vertical" excess cost permitted by
 // original ActionProtocol quantum at its strictly >1 baseline.
 K[9][20]*=Math.exp(-.11*hostile);
 return K;
}
function perron(K){
 let r=Array(Kdim).fill(1/Kdim),lam=0;
 for(let step=0;step<140;step++){
  let next=K.map(row=>row.reduce((sum,x,j)=>sum+x*r[j],0));
  lam=next.reduce((a,b)=>a+b,0);
  r=next.map(x=>x/lam);
 }
 let max=0;
 for(let i=0;i<Kdim;i++){
  let v=0;for(let j=0;j<Kdim;j++)v+=K[i][j]*r[j];
  max=Math.max(max,Math.abs(v-lam*r[i]));
 }
 assert(max<1e-11,"Perron eigenpair error");
 return lam;
}
const book=(z,f=zeros(),e=flatE(),hostile=0)=>
 -Math.log(perron(nativeK(z,f,e,hostile)))/logphi;
function siteDensities(e,links){
 return Array.from({length:N},(_,i)=>
  e[i][0]*e[i][1]*(links[(i+1)%N]-links[i]));
}
const baseline=book(0),step=.002,w=[],dw=[],Fh=Array.from({length:N},
 ()=>Array(N).fill(0));
const Bzz=(book(step)-2*baseline+book(-step))/(step*step);
assert(Bzz<-.001,"nontrivial endogenous Book archive Hessian");
for(let i=0;i<N;i++){
 const plus=zeros(),minus=zeros();plus[i]=step;minus[i]=-step;
 w.push((book(0,plus)-book(0,minus))/(2*step));
 dw.push((book(step,plus)-book(step,minus)
         -book(-step,plus)+book(-step,minus))/(4*step*step));
 Fh[i][i]=(book(0,plus)-2*baseline+book(0,minus))/(step*step);
 for(let j=0;j<i;j++){
  const pp=zeros(),pm=zeros(),mp=zeros(),mm=zeros();
  pp[i]=step;pp[j]=step;pm[i]=step;pm[j]=-step;
  mp[i]=-step;mp[j]=step;mm[i]=-step;mm[j]=-step;
  Fh[i][j]=Fh[j][i]=
   (book(0,pp)-book(0,pm)-book(0,mp)+book(0,mm))/(4*step*step);
 }
}
const wMin=Math.min(...w),wMax=Math.max(...w);
assert(wMin>.001&&Math.abs(wMax-wMin)<1e-9,"not uniform native root coupling");
assert(Math.max(...dw)-Math.min(...dw)>.001,
 "original Book internal/geometry mixed source is trivial");
const coframe=2*N, mat=(rows,cols)=>Array.from({length:rows},
 ()=>Array(cols).fill(0));
const L=mat(N,D),Z=mat(D,N),HP=mat(D,D);
for(let i=0;i<N;i++){
 Z[2*i][i]=Z[2*i+1][i]=1;
 const k=coframe+i,l=coframe+(i+1)%N;
 L[i][k]=-1;L[i][l]=+1;
 for(const a of [2*i,2*i+1]){
  HP[a][k]-=w[i];HP[k][a]-=w[i];
  HP[a][l]+=w[i];HP[l][a]+=w[i];
 }
}
const M=Array.from({length:N},(_,i)=>Array.from({length:N},
 (_,j)=>Fh[i][j]-dw[i]*dw[j]/Bzz));
const E=HP.map(row=>row.slice());
for(let a=0;a<D;a++)for(let b=0;b<D;b++){
 let extra=0;
 for(let i=0;i<N;i++)if(L[i][a])
  for(let j=0;j<N;j++)if(L[j][b])
   extra+=L[i][a]*M[i][j]*L[j][b];
 E[a][b]+=extra;
}
const T=mat(D,D);
for(let i=0;i<D;i++)T[i][i]=1;
for(let i=0;i<N;i++)
 for(let j=0;j<N;j++)
  for(const a of [2*i,2*i+1])
   for(let b=0;b<D;b++)
    if(L[j][b])T[a][b]+=.25*M[i][j]*L[j][b]/w[i];
const Hcong=mat(D,D);
for(let a=0;a<D;a++)for(let b=0;b<D;b++){
 let sum=0;
 for(let i=0;i<D;i++)if(T[i][a])
  for(let j=0;j<D;j++)if(T[j][b])
    sum+=T[i][a]*HP[i][j]*T[j][b];
 Hcong[a][b]=sum;
}
const maxErr=Math.max(...E.flatMap((row,i)=>
 row.map((x,j)=>Math.abs(x-Hcong[i][j]))));
assert(maxErr<1e-10,"NEW full determinant-one congruence failed");
function rank(X,tol=1e-7){
 let A=X.map(row=>row.slice()),rr=0;
 for(let c=0;c<A[0].length&&rr<A.length;c++){
  let k=rr;for(let i=rr+1;i<A.length;i++)
   if(Math.abs(A[i][c])>Math.abs(A[k][c]))k=i;
  if(Math.abs(A[k][c])<tol)continue;
  [A[k],A[rr]]=[A[rr],A[k]];
  const piv=A[rr][c];for(let j=c;j<A[0].length;j++)A[rr][j]/=piv;
  for(let i=rr+1;i<A.length;i++){
   const factor=A[i][c];
   for(let j=c;j<A[0].length;j++)A[i][j]-=factor*A[rr][j];
  }rr++;
 }
 return rr;
}
const kernel=[];
for(let i=0;i<N;i++){
 const v=Array(D).fill(0);v[2*i]=1;v[2*i+1]=-1;kernel.push(v);
}
const radial=Array(D).fill(0);
for(let i=0;i<N;i++)radial[2*i]=radial[2*i+1]=1;
kernel.push(radial);
const flatlink=Array(D).fill(0);
for(let i=0;i<N;i++)flatlink[coframe+i]=1;
kernel.push(flatlink);
let kerErr=0;
for(const v of kernel)for(const row of E){
 const z=row.reduce((s,x,i)=>s+x*v[i],0);
 kerErr=Math.max(kerErr,Math.abs(z));
}
const rankOriginal=rank(HP),rankReduced=rank(E);
assert(rankOriginal===30&&rankReduced===30&&
  kernel.length===18&&kerErr<1e-9,"true graviton/gauge kernel altered");
// Gauge-independent failure of exact descent off shell at identical
// t(q) due to genuine shape-dependent O(t^2) primitive native Book COST.
let links=Array.from({length:N},(_,i)=>.18*Math.sin(2*Math.PI*i/N));
const e=flatE(),f=siteDensities(e,links);
const eDifferent=e.map(v=>v.slice());
eDifferent[0][0]*=1.6;eDifferent[0][1]/=1.6;
const fDifferent=siteDensities(eDifferent,links);
let verticalErr=Math.max(...f.map((v,i)=>Math.abs(v-fDifferent[i])));
const verticalCost=book(.13,f,eDifferent)-book(.13,f,e);
assert(verticalErr<1e-13&&Math.abs(verticalCost)>1e-8,
 "hostile: action unexpectedly descends exactly to the t_i");
// Independent genuine allowed cost-completion with a first-source
// along t=0 coframe-shape tangent: fundamental Cost>=1 DOES NOT
// force the desired gravity normal form.
const q=.0004;
const hostile=(book(0,zeros(),flatE(),q)
              -book(0,zeros(),flatE(),-q))/(2*q);
assert(Math.abs(hostile)>1e-5&&1.1-.11*q/logphi>1,
 "hostile first-order Cost selection counterexample failed");
console.log("PASS native 33 vertices/718 genuine directed primitive Book Cost edges; 16 original L2 site labels");
console.log("PASS 48-dimensional coframe/shared-link radial source SUBSECTOR, nonconstant true Book K");
console.log("PASS actual scalar Book Perron internal B''(0)",Bzz);
console.log("PASS sixteen true native w_i",wMin,wMax);
console.log("PASS nonzero MOVING heterogeneous original Book history->geometry mixed Hessian",Math.min(...dw),Math.max(...dw));
console.log("PASS full history double Schur Hessian extra ||M||max",Math.max(...M.flat().map(Math.abs)));
console.log("PASS exact 48x48 Hessian conjugacy max discrepancy",maxErr);
console.log("PASS full geometric Hessian rank 30 BEFORE and AFTER original Book history reduction",rankOriginal,rankReduced);
console.log("PASS all 18 exact common kernel modes are protected",kerErr);
console.log("PASS real complete Book action NOT F(t) offshell; same t and different retained shape price",verticalCost);
console.log("PASS hostile permitted Cost>=1 has NONZERO vertical first source at root",hostile);
console.log("FIREWALL: actual G0/Book full H+J+R normal form, true full640 Role and sourced CAR, Spin, clock/work & physical GR remain OPEN");
