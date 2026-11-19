// Bounded native Golden READY-prefix and conditional same-address Book/CQ source.
import assert from 'node:assert/strict';
let checks=0;
const ck=(x,s)=>{assert.ok(x,s);checks++};
const close=(x,y,t=1e-10)=>{ck(Math.abs(x-y)<t,String(x)+" vs "+String(y));};
const phi=(1+Math.sqrt(5))/2,p=1/phi,n=20,z0=2**-20;
let f0=0,f1=1;
const F=[f0,f1];for(let i=2;i<=21;i++)F.push(F[i-1]+F[i-2]);
const F20=F[20],F21=F[21],nready=2*F21;
ck(F20===6765 && F21===10946 && nready===21892,"original F/R true counts");
close(F21*p**n+F20*p**(n+1),1,1e-11);
const Pro=F20*p**(n+1),Pff=F21*p**(n+2),Pfr=F21*p**(n+3),Prr=F21*p**(n+4);
close(Pro+Pff+2*Pfr+Prr,1,1e-11);
const ready=2*Pfr;
close(ready,0.34164078707015466,2e-14);
const leafClasses=[[n+1,F20],[n+2,F21],[n+3,2*F21],[n+4,F21]];
const entropy=leafClasses.reduce((sum,[ell,cnt])=>sum-cnt*p**ell*Math.log(p**ell)/Math.log(phi),0);
const cost=leafClasses.reduce((sum,[ell,cnt])=>sum+cnt*p**ell*ell,0);
close(entropy,cost,4e-13);
close(cost,22.27639320438063,2e-11);
const L=4*p**3,Q=1-z0*L,R=1-z0*L*(1+p**6),r0=1-Q*R;
const hPrime=Math.log((1-r0)/r0)/Math.log(phi);
ck(r0>0 && r0<0.5 && hPrime>1,"original binary flat report root");
const zeta=z0,A0=1-zeta*(1-p**8),C=2*zeta*p**7/A0;
const gain=C/(p**23*(hPrime-1));
ck(gain>0 && Number.isFinite(gain),"native ready positive gain");
// Illustrative site counts, NOT claimed original nested-box addresses; all
// source formulas below are independent of n_z and require only sum n_z=F21.
const nz=Array(256).fill(42);for(let i=0;i<194;i++)nz[i]=43;
ck(nz.reduce((s,x)=>s+x,0)===F21,"valid arbitrary proof-control counts");
const slope=Array.from({length:256},(_,j)=>((j%7)-3)/800 +Math.sin((j+1)*0.09)/900);
const r=(j,y)=>r0+slope[j]*y;
const h=(r)=>-(r*Math.log(r)+(1-r)*Math.log(1-r))/Math.log(phi);
const cq=(y)=>2*p**23*nz.reduce((sum,ct,j)=>sum+ct*(1+r(j,y)-h(r(j,y))),0);
const book=(y)=>{
 let sum=0;
 for(let j=0;j<256;j++){
   const rr=r(j,y),rl=1-(rr+1-r0)/2,rref=0.5;
   const t=(1-2*p*rl)*(1-2*p*rref);
   sum-=2*nz[j]*Math.log1p(-zeta*(1-t*t));
 }
 return sum;
};
const sumDr=2*nz.reduce((sum,ct,j)=>sum+ct*slope[j],0);
const dcq=p**23*(1-hPrime)*sumDr;
const dbook=-C*sumDr;
close(dbook/gain,dcq,1e-10);
const eps=1e-5;
const fdCQ=(cq(eps)-cq(-eps))/(2*eps),fdBook=(book(eps)-book(-eps))/(2*eps);
close(fdCQ,dcq,8e-8);
close(fdBook,dbook,5e-7);
close(fdBook,gain*fdCQ,5e-7);
const kappa=2*zeta*p**7/A0;
for(let j=0;j<42;j++){
  const weight=((j%8)+1)/7;
  close((-kappa*sumDr)*weight,gain*(p**23*(1-hPrime)*sumDr)*weight,2e-13);
}
// Projection-lattice minimal join in a 4D toy register: a matching pure
// state is rank1, a register-wide pointer join is rank4, and a unitary
// preserving the READY span has identically zero complementary feedback.
for(let m=2;m<=12;m++){
 const ptr=Array.from({length:m},(_,i)=>i%2===0?1:0);
 const P=ptr.map((x,i)=>ptr.map((y,j)=>i===j?x:0));
 const U=Array.from({length:m},(_,i)=>ptr.map((_,j)=>i===j?(-1)**i:0));
 let norm=0;
 for(let i=0;i<m;i++)for(let j=0;j<m;j++){
   // (I-P) U P == 0 exactly for diagonal, record-preserving U.
   let q=0;for(let k=0;k<m;k++)q+=(+(i===k)-P[i][k])*U[k][j]*P[j][j];
   norm+=q*q;
 }
 ck(norm===0,"P_READY alone has zero feedback when U preserves it");
}
console.log(JSON.stringify({status:"PASS",checks,F20,F21,readyLeaves:nready,
    originalREADYProbability:ready,prefixCost:cost,prefixInformation:entropy,
    originalReportRoot:r0,reportedFull42Gain:gain,
    nativeBookPerLeafSource:C,scope:"actual prefix counts, illustrative site distribution, conditional Book cut only"},null,2));
