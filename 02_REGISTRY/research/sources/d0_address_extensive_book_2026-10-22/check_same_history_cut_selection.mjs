// Same complete coherent history + same unitary, but distinct native Book cuts.
import assert from 'node:assert/strict';
const p=2/(1+Math.sqrt(5)), z=0.29, r0=0.24, c0=1-r0;
const A0=1-z*(1-p**8), C=2*z*p**7/A0;
let checks=0;
const close=(v,w,eps=8e-12)=>{assert.ok(Math.abs(v-w)<eps,String(v)+" != "+String(w));checks++;};
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const matmul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const transpose=A=>A[0].map((_,j)=>A.map(row=>row[j]));
function matrix(w,slope,y){
  const W=w.reduce((x,y)=>x+y,0), dims=2*W;
  const weights=[],t=[];
  for(let i=0;i<w.length;i++)
    for(let k=0;k<w[i];k++){
      weights.push(1/W);
      const r=r0+slope[i]*y;
      const rleft=1-(r+c0)/2, rright=(r0+c0)/2;
      t.push((1-2*p*rleft)*(1-2*p*rright));
    }
  const psi=Array(dims).fill(0), U=Array.from({length:dims},()=>Array(dims).fill(0));
  for(let i=0;i<W;i++){
    psi[2*i]=Math.sqrt(weights[i]);
    const s=Math.sqrt(1-t[i]*t[i]);
    U[2*i][2*i]=t[i];U[2*i][2*i+1]=-s;
    U[2*i+1][2*i]=s;U[2*i+1][2*i+1]=t[i];
  }
  const Ppure=psi.map(x=>psi.map(y=>x*y));
  const Ppointer=Array.from({length:dims},(_,i)=>Array.from({length:dims},(_,j)=>+(i===j&&i%2===0)));
  return {W,weights,t,psi,U,Ppure,Ppointer};
}
function comp(U,P){
  const n=U.length,I=eye(n),Iminus=I.map((row,i)=>row.map((x,j)=>x-P[i][j]));
  return matmul(matmul(matmul(P,transpose(U)),matmul(Iminus,U)),P);
}
function calc(w,slopes,y) {
  const m=matrix(w,slopes,y),Fp=comp(m.U,m.Ppure),Fq=comp(m.U,m.Ppointer);
  const fPure=m.psi.reduce((acc,v,i)=>acc+v*m.psi.reduce((s,u,j)=>s+Fp[i][j]*u,0),0);
  const fQ=m.t.map(t=>1-t*t);
  const jPure=-Math.log1p(-z*fPure);
  const jPtr=-fQ.reduce((acc,f)=>acc+Math.log1p(-z*f),0);
  return {m,Fp,Fq,jPure,jPtr,fPure,fQ};
}
for(const [w,slopes] of [
  [[1,1],[0.38,-0.24]],[[1,2,1],[0.25,-0.37,0.49]],
  [[1,1,2,3],[0.25,0.1,-0.3,0.45]]
]){
  const zero=calc(w,slopes,0),m=zero.m;
  const err=matmul(transpose(m.U),m.U);
  for(let i=0;i<2*m.W;i++)for(let j=0;j<2*m.W;j++)
    close(err[i][j],+(i===j),4e-15);
  close(m.psi.reduce((a,b)=>a+b*b,0),1,3e-15);
  close(zero.fPure,1-p**8,3e-15);
  for(let k=0;k<m.W;k++){
    close(zero.Fq[2*k][2*k],1-p**8,3e-15);
    for(let j=0;j<m.W;j++)if(j!==k)close(zero.Fq[2*k][2*j],0,4e-15);
  }
  const h=0.00001;
  const plus=calc(w,slopes,h),minus=calc(w,slopes,-h);
  const dPure=(plus.jPure-minus.jPure)/(2*h);
  const dPtr=(plus.jPtr-minus.jPtr)/(2*h);
  const W=m.W,sum=w.reduce((v,ww,i)=>v+ww*slopes[i],0);
  close(dPure,-C*sum/W,1e-10);
  close(dPtr,-C*sum,1e-10);
  close(zero.jPtr-zero.jPure,-(W-1)*Math.log(A0),2e-14);
  assert.ok(zero.jPtr>zero.jPure && W>1);checks++;
  for(let k=0;k<W;k++)close(m.psi[2*k]**2,1/W,3e-15);
}
console.log(JSON.stringify({status:"PASS",checks,observation:"identical U and psi; different P",
  pureCutRank:1,pointerCutRank:"W",sourceGainPure:"1/W",
  sourceGainPointer:"1",singleMaster:true}));
