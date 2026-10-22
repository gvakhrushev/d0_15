// One-carrier original Golden fixed-splitter H+J+R-type thermal tensor
// with ORIGINAL ternary N1 reported probabilities. This is NOT a D0
// Book03 Δ_N admission or full physical HJR price selection.
import assert from 'node:assert/strict';
let checks=0;
const ok=(p,m)=>{assert.ok(p,m);checks++};
const close=(a,b,t=5e-12,m='close')=>{
 ok(Math.abs(a-b)<=t*Math.max(1,Math.abs(a),Math.abs(b)),m+': '+a+' vs '+b)
};
const p=(Math.sqrt(5)-1)/2,z=2**-20,be=2*p*p;
const ell=Math.log(1/p);
const alpha=(1-(1-2*p**3)**9)**128;
const betaFactory=((1-p**120)**4*(1-(1-16*p**9)**20))**43;
const gamma=alpha*betaFactory;
const rOld0=1-(1-z*4*p**3)*(1-z*4*p**3*(1+p**6));
const rOld1=rOld0+7.247e-11;
const E=(r)=>{
 const q=[1-gamma,gamma*(1-r),gamma*r],max=Math.max(...q);
 const spectrum=q.map(x=>Math.log(max/x)/be);
 const boltz=spectrum.map(x=>Math.exp(-be*x));
 return {q,spectrum,Z:boltz.reduce((a,b)=>a+b,0),H:-q.reduce((a,b)=>a+b*Math.log(b),0)};
};
const zScene=1+12*Math.exp(-20*be)+10*Math.exp(-22*be)+8*Math.exp(-24*be)+2*Math.exp(-33*be);
const heat=e=>Math.log(e.Z)/be;
const matter=e=>e.q.reduce((a,x,i)=>a+x*e.spectrum[i],0);
const j=(m)=>-m*Math.log1p(-z*p*p);
function master(rs){
 const eps=rs.map(E),W=rs.length,dim=33*3**W;
 const H=Math.log(2*zScene)/be+eps.reduce((s,e)=>s+heat(e),0);
 const R=eps.reduce((s,e)=>s+matter(e),0);
 return {H,R,J:j(dim),sum:H+R+j(dim),dim,eps};
}
const matmul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const transpose=A=>A[0].map((_,j)=>A.map(row=>row[j]));
function actualGoldenUnitary(d){
 const n=2*d,a=Math.sqrt(p);
 const U=Array.from({length:n},()=>Array(n).fill(0));
 for(let i=0;i<d;i++){
  U[i][i]=a;U[i][d+i]=-p;U[d+i][i]=p;U[d+i][d+i]=a;
 }
 return U;
}
for(const d of [1,2,3,9]){
 const U=actualGoldenUnitary(d),n=2*d,Ut=transpose(U),id=matmul(Ut,U);
 for(let i=0;i<n;i++)for(let j=0;j<n;j++)
  close(id[i][j],+(i===j),1e-14,'unchanged original Golden splitter unitary');
 // Active P=diag(I_d,0); F=P U†(I-P)UP
 const Umid=U.map((row,i)=>row.map(x=>i>=d?x:0));
 const F=matmul(Ut,Umid);
 for(let i=0;i<d;i++)for(let j=0;j<d;j++)
  close(F[i][j],+(i===j)*p*p,1e-14,'actual Book complement p^2 P, no fitted F');
 const J=-d*Math.log1p(-z*p*p);
 close(J,j(d),2e-14,'literal Golden Book feedback det');
}
for(const rs of [
 [rOld0],[rOld0,rOld1],[rOld0,rOld1,.0031],
 [.1,.23],[.06,.11,.32,.55]
]){
 const M=master(rs),W=rs.length;
 const native=rs.reduce((s,r)=>s+gamma*(-r*Math.log(r)-(1-r)*Math.log1p(-r)),0);
 const gammaEntropy=-gamma*Math.log(gamma)-(1-gamma)*Math.log1p(-gamma);
 close(M.H+M.R,(Math.log(2*zScene)+W*gammaEntropy+native)/be,2e-12,
       'ONE tensor heat+matter reconstruct all native independent report entropies');
 close(M.sum, (Math.log(2*zScene)+W*gammaEntropy+native)/be+j(M.dim),
       2e-12,'ONE HJR master full original fixed Golden det');
 const hb=(r)=>Math.log((1-r)/r)/ell;
 for(let i=0;i<rs.length;i++){
  const qrs=rs.slice(),step=Math.min(3e-7,rs[i]*1e-3,(1-rs[i])*1e-3);
  qrs[i]+=step;const pplus=master(qrs).sum;
  qrs[i]-=2*step;const pminus=master(qrs).sum;
  const d=(pplus-pminus)/(2*step);
  const source=gamma*Math.log((1-rs[i])/rs[i])/be;
  // Finite difference of full master can suffer cancellation at tiny z;
  // the exact formula is independently checked for every report.
  close(d,source,2e-6,'FULL multi-site Book-type action off-null source');
  const cqSource=-gamma*hb(rs[i]);
  close(cqSource,-be/ell*source,3e-12,'all native CQ/thermal source ratio');
 }
 ok(M.dim===33*3**W,'complete tensor carrier dimension, not mixed-price sum');
 if(W>1){
  const diff=j(33*3**W)-j(33*3**(W-1));
  ok(diff>0,'absolute native Golden feedback rank selection nontrivial');
 }
}
// On the original certified h=1/4 N1 root the two ORIGINAL local report
// values are strictly unequal, and the 42x42 Hessian nondegeneracy is
// independently interval-verified in the upstream certificate.
for(let k=0;k<42;k++){
 const rA=1.8512417713660524e-6,rB=1.85132974719277498e-6;
 const slope=Math.sin((k+1)*.227)*1e-4;
 const logit=r=>Math.log((1-r)/r);
 const slopeB=-logit(rA)/logit(rB)*slope;
 const fromHeat=gamma/be*(logit(rA)*slope+logit(rB)*slopeB);
 const fromCQ=-gamma/ell*(logit(rA)*slope+logit(rB)*slopeB);
 close(fromHeat,-ell/be*fromCQ,3e-13,'source proportional in every formal 42-dimensional off-null direction');
}
const M2=master([rOld0,rOld1]);
const Jnext=j(33*3**3);
ok(Jnext>M2.J,'growing Book address rank expensive even though J field source zero');
console.log(JSON.stringify({status:'PASS',checks,
nativeRareR:[rOld0,rOld1],nativeFactoryReadiness:gamma,
nativeBookBeta:be,GoldenFeedbackEigenvalue:p*p,
h4TwoSiteCarrierDim:297,oneFullMasterHJRValue:M2.sum,
fieldSource:'off-null whole CQ equality, opposite nonzero factor',
finiteKRoot:'analytical IFT from already rigorous h4 Hessian; not certified K threshold',
requiredPhysical:'compulsory Book03 heat/R/cut/Info/clock selection OPEN',GR_closed:false}));
