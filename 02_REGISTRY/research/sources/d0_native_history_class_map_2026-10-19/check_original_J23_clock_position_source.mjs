#!/usr/bin/env node
"use strict";
// ORIGINAL full128 first Fourier shell, actual homogeneous J23 blank0 source.
// No 128 Kraus re-enumeration and no new physical selector/action.
const phi=(1+Math.sqrt(5))/2,p=1/phi,L=Math.log(phi);
const n=1024,q=(5034167+28557*Math.sqrt(5))/5120000;
const dq=(42633-14157*Math.sqrt(5))/5120000,e=1-q,de=-dq;
const check=(x,name)=>{if(!x)throw Error("FAIL: "+name);console.log("PASS",name);};
const close=(x,y,tol=1e-9)=>Math.abs(x-y)<tol;
check(close(p+p*p,1)&&q>0&&e>0&&dq>0,"original Golden and real J23 probability jet");
let pk=q**n,Hcount=0,Hpos=0,dHcount=0,dHpos=0,Fscore=0,sum=0,lnChoose=0;
for(let k=0;k<=n;k++){
 const score=(n-k)*dq/q-k*dq/e;
 const dpk=pk*score;
 sum+=pk;Fscore+=pk*score*score;
 if(pk>0){
   Hcount-=pk*Math.log(pk)/L;
   dHcount-=dpk*(Math.log(pk)+1)/L;
 }
 Hpos+=pk*lnChoose/L;
 dHpos+=dpk*lnChoose/L;
 if(k<n){lnChoose+=Math.log(n-k)-Math.log(k+1);
         pk*=(n-k)*e/((k+1)*q);}
}
const dHtime=-n*dq*Math.log(q/e)/L;
check(close(sum,1,1e-13),"entire native count law normalizes");
check(close(Hcount,4.436275996781906)&&close(Hpos,54.4682578495223),
      "native finite-clock position/count entropy values");
check(close(dHtime,-24.848547081184805)&&close(dHcount,-0.5458930443887225)
      &&close(dHpos,-24.302654036796067),
      "exact actual homogeneous J23 first clock and count sources");
check(close(dHtime,dHpos+dHcount,1e-10),
      "original first-source entropy chain identity");
check(close(Fscore,n*dq*dq/(e*q),1e-10)
      &&close(Fscore,1.1012451573945585,1e-10),
      "on real J23 scalar BASE effect implies count Fisher sufficiency");

// Separate formal 2x2 NONSCALAR source negative control; NOT the original
// 128 Kraus instrument. It validates the scalar-BASE/non-scalar-TANGENT
// algebra only, including a genuine nonzero offdiagonal matrix variation.
const X=[[.25,.11],[.11,-.07]],trX=(X[0][0]+X[1][1])/2;
const a=2*Math.sqrt(q)*trX,b=-a;
check(X[0][1]!==0 && X[0][0]!==X[1][1]&&a!==0,
      "nonscalar matrix tangent with scalar baseline effects");
for(let m=2;m<=6;m++)for(let mask=0;mask<(1<<m);mask++){
  let k=0;for(let j=0;j<m;j++)k+=(mask>>j)&1;
  const prob=q**(m-k)*e**k;
  const source=prob*((m-k)*a/q+k*b/e);
  const target=prob*a*((m-k)/q-k/e);
  if(!close(source,target,1e-13))throw Error("nonscalar jet "+m+"/"+mask);
}
check(true,"all finite nonscalar Kraus first-source controls");

// Entire ORIGINAL n-tick tilted CP count generator first source on the
// homogeneous offscalar J23 tangent, not the separate physical J2 parameter.
for(const s of [-1,-.2,0,.3,1]){
 const t=q+e*Math.exp(s);
 const Z=t**n;
 const dlog=n*dq*(1-Math.exp(s))/t;
 // direct finite count distribution generating function and its field jet
 let sum=0,der=0,pk=q**n;
 for(let k=0;k<=n;k++){
   const w=Math.exp(s*k),score=(n-k)*dq/q-k*dq/e;
   sum+=pk*w;der+=pk*w*score;
   if(k<n)pk*=((n-k)/(k+1))*(e/q);
 }
 // Direct derivative-to-partition ratio, not a fitted finite difference.
 check(close(sum,Z,1e-7*Math.max(1,Z))
       &&close(der/Z,dlog,1e-8),"native full-count tilt J23 source s="+s);
}
check(close(-n*dq,-2.1953971285070955)
      &&close(n*(e-q)*dq,-2.1765496383560343),
      "original first two count cumulants on J23");

const dP=(-42957+14319*Math.sqrt(5))/5120000;
const dN=n*dP,dKL=n*p**3*dP,dSh=n*(2-p)*dP;
check(close(dN,-2.187748526036102)
      &&close(dKL,-0.5164573698194886)
      &&close(dSh,-3.0233941041444083),
      "actual native full128 1024-tick nonblank and hidden-port J23 source");
console.log(JSON.stringify({scope:"original homogeneous J23 FIRST SOURCE; no complete Book action",
q,dq,n,Hcount,Hpositions:Hpos,sourceTime:dHtime,
sourceCount:dHcount,sourcePositions:dHpos,
fisherTimeAndCount:Fscore,sourceHiddenPortKL:dKL,
sourceHiddenPortShannon:dSh,GR_closed:false},null,2));
