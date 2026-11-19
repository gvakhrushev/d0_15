// Bounded Golden/Book operator-source test; Node.js standard library only.
import assert from 'node:assert/strict';

const PHI=(1+Math.sqrt(5))/2, p=1/PHI, a=Math.sqrt(p);
const zNative=2**-20, L=4*p**3;
const nativeR0=1-(1-zNative*L)*(1-zNative*L*(1+p**6));
const hp=Math.log((1-nativeR0)/nativeR0)/Math.log(PHI);
const rg=[[p,a],[a,-p]];
let checks=0;
const check=(q,msg)=>{assert.ok(q,msg);checks++;};
function mul(A,B) {
  const M=A.length,K=B.length,N=B[0].length;
  assert.equal(A[0].length,K);
  return Array.from({length:M},(_,i)=>Array.from({length:N},(_,j)=>{
    let v=0;for(let k=0;k<K;k++)v+=A[i][k]*B[k][j];return v;
  }));
}
const tr=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const kron=(A,B)=>A.flatMap(rowA=>B.map(rowB=>rowA.flatMap(x=>rowB.map(y=>x*y))));
const maxErr=(A,B)=>Math.max(...A.flatMap((row,i)=>row.map((x,j)=>Math.abs(x-B[i][j]))));
function U(r) {
  const s=Math.sqrt(r),c=Math.sqrt(1-r),V=[[c,-s],[s,c]];
  const e=mul(mul(tr(V),[[1,0],[0,-1]]),V);
  const middle=[[1,0,0,0],[0,1,0,0],[0,0,e[0][0],e[0][1]],[0,0,e[1][0],e[1][1]]];
  const rg2=kron(rg,eye(2));
  return mul(mul(rg2,middle),rg2);
}
function pair(rleft,rright) {return kron(U(rleft),U(rright));}
function factors(rl,rr){let t=(1-2*p*rl)*(1-2*p*rr);return {t,F:1-t*t};}
function bookF(rl,rr,z){return -Math.log1p(-z*factors(rl,rr).F);}
for(const r of [0.03,0.18,0.5,0.76,0.96]) {
  const m=U(r);
  check(maxErr(mul(tr(m),m),eye(4))<4e-15,"single arm unitary");
  check(Math.abs(m[0][0]-(1-2*p*r))<2e-15,"single arm actual return");
}
for(const [rl,rr] of [[0.5,0.5],[0.2,0.8],[0.67,0.14],[0.05,0.99]]) {
  const mat=pair(rl,rr), f=factors(rl,rr).F, a=mat[0][0];
  let leakage=0;for(let k=1;k<16;k++)leakage+=mat[k][0]**2;
  check(maxErr(mul(tr(mat),mat),eye(16))<9e-15,"complete pair unitary");
  check(Math.abs(leakage-f)<5e-15,"true full complement");
  check(Math.abs(a-factors(rl,rr).t)<3e-15,"true pair return");
}
const w=[2,1,4],gamma0=[0.51,0.73,0.44],slopes=[1.1,-0.7,0.3];
const copies=w.reduce((a,b)=>a+b,0);
function liveAndReference(y,u,r0) {
  const rStar=r0+0.075*u,c=1-r0+0.17*u;
  const rR=(rStar+c)/2;
  return {rStar,rR,rL:slopes.map((s,i)=>{
    const g=gamma0[i]+0.023*y+0.08*u;
    const report=rStar+s*y;
    const whole=g*report+(1-g)*rStar;
    return 1-(whole+c)/2;
  })};
}
function fullAddress(y,u,r0,z){
  const {rL,rR}=liveAndReference(y,u,r0);
  return rL.reduce((acc,r,i)=>acc+w[i]*bookF(r,rR,z),0);
}
function derivativeEstimate(fn,x,h){return (fn(x+h)-fn(x-h))/(2*h);}
const zTest=0.31,rTest=0.23;
const A0Test=1-zTest*(1-p**8);
const sumSource=w.reduce((acc,ww,i)=>acc+ww*gamma0[i]*slopes[i],0);
const analytical=-2*zTest*p**7/A0Test*sumSource;
const dB=derivativeEstimate(y=>fullAddress(y,0,rTest,zTest),0,0.00001);
check(Math.abs(dB-analytical)<1e-8,"whole address derivative, moved readiness");
const shared=derivativeEstimate(u=>fullAddress(0,u,rTest,zTest),0,0.00001);
check(Math.abs(shared)<5e-9,"all shared input/controller derivatives cancel");
const h=0.0003;
const hess=(fullAddress(0,h,rTest,zTest)+fullAddress(0,-h,rTest,zTest)-2*fullAddress(0,0,rTest,zTest))/h**2;
const expectedHess=copies*4*zTest*p**6/A0Test*(0.075+0.17)**2;
check(Math.abs(hess-expectedHess)<2e-7,"positive shared controller Hessian");
const noExtraGain=2*zNative*p**7/((1-zNative*(1-p**8))*hp);
check(Math.abs(noExtraGain-2.3949186960339158e-9)<2e-19,"native constant independent of W");
for(let k=0;k<42;k++){
  const v=slopes.map((_,i)=>Math.sin((k+1)*(i+2)*0.27));
  const base=w.reduce((s,ww,i)=>s+ww*gamma0[i]*v[i],0);
  const book=-2*zNative*p**7/(1-zNative*(1-p**8))*base;
  const cq=-hp*base;
  check(Math.abs(book-noExtraGain*cq)<3e-22,"all42 row relative factor");
}
for (let W of [1,2,4,8,16,32,128]){
  const den=1-zNative*(1-p**8);
  const mean=2*zNative*p**7/(W*den);
  const tensor=2*zNative*p**(8*W-1)/(1-zNative*(1-p**(8*W)));
  const addressed=2*zNative*p**7/den;
  check(Math.abs(W*mean-addressed)<1e-18,"mean source rank suppression");
  check(tensor<=addressed*(1+1e-13),"tensor source no gain");
  const beta=2*p*p;
  const step=Math.log1p(1/W)/beta-Math.log(den);
  check(step>0,"Book rank-step price positive");
}
for (const W of [1,2,4]) {
  let Mats=[];
  for(let j=0;j<W;j++) Mats.push(pair(0.5,0.5));
  const dim=16*W;
  let big=Array.from({length:dim},()=>Array(dim).fill(0));
  for(let j=0;j<W;j++)for(let i=0;i<16;i++)for(let k=0;k<16;k++)
    big[16*j+i][16*j+k]=Mats[j][i][k];
  check(maxErr(mul(tr(big),big),eye(dim))<8e-15,"one addressed global unitary");
  const active=Array.from({length:W},(_,j)=>16*j);
  for(let ai=0;ai<W;ai++)for(let aj=0;aj<W;aj++){
    const j=active[aj],i=active[ai];
    let f=(ai===aj?1:0);
    for(let k=0;k<W;k++)f-=big[active[k]][i]*big[active[k]][j];
    const expected=(ai===aj)?1-p**8:0;
    check(Math.abs(f-expected)<6e-15,"one true block complement");
  }
}
console.log(JSON.stringify({status:"PASS",checks,nativeR0,
  perCopyBookSource:2*zNative*p**7/(1-zNative*(1-p**8)),
  sourceGain:noExtraGain,sharedControllerHessianCoefficient:4*zNative*p**6/(1-zNative*(1-p**8)),
  result:"rank-W block-addressed true complement; no claim of native moving cut admission"},null,2));
