// Exact renewal-Gibbs-source composition controls; only standard JS mathematics.
// Source: native Golden N1 alpha,beta, Q,R and complete fail/READY0/READY1 report.
// This script tests an ABSTRACT proposed heat, NOT Book03 Hodge admission.
import assert from 'node:assert/strict';
let checks=0;
const ok=(x,m)=>{assert.ok(x,m);checks++};
const close=(x,y,t=5e-11,m='close')=>ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
const p=(Math.sqrt(5)-1)/2;
const logphi=Math.log(1/p),nativeZ=2**-20;
const L=4*p**3,Q=1-nativeZ*L,R=1-nativeZ*L*(1+p**6);
const d0=Q*R,r0=1-d0;
const ready=(1-(1-2*p**3)**9)**128*((1-p**120)**4*(1-(1-16*p**9)**20))**43;
const b=2*p*p;
const q3=(g,r)=>[1-g,g*(1-r),g*r];
const entropy=q=>-q.reduce((s,v)=>s+v*Math.log(v),0);
const binaryH=r=>-r*Math.log(r)-(1-r)*Math.log1p(-r);
const softBoltz=E=>{
 const ex=E.map(x=>Math.exp(-b*x)),Z=ex.reduce((s,v)=>s+v,0);
 return {q:ex.map(v=>v/Z),Z};
};
const exactEnergy=q=>{
 const m=q.map(v=>-Math.log(v)),mn=Math.min(...m);
 return m.map(v=>(v-mn)/b);
};
const mk=(q,K)=>{
 if(K==='inf')return -Math.log(q);
 const x=1-q;
 let v=0,a=x;
 for(let j=1;j<=K;j++){v+=a/j;a*=x}
 return v;
};
const truncEnergy=(q,K)=>{
 const m=q.map(v=>mk(v,K)),mn=Math.min(...m);
 return m.map(v=>(v-mn)/b);
};
const T=(q,E)=>{
 const {q:sigma,Z}=softBoltz(E);
 return {v:q.reduce((s,x,i)=>s+x*E[i],0)+Math.log(Z)/b,sigma,Z};
};
function directional(q,dq,K){
 const m=q.map(v=>mk(v,K));
 const ix=m.indexOf(Math.min(...m)),dm=q.map((v,i)=>
   K==='inf'? -dq[i]/v:-(1-(1-v)**K)/v*dq[i]);
 const dE=dm.map(x=>(x-dm[ix])/b);
 const E=m.map(x=>(x-m[ix])/b);
 const out=T(q,E);
 const d= dq.reduce((s,v,i)=>s+v*E[i],0)+
          q.reduce((s,v,i)=>s+(v-out.sigma[i])*dE[i],0);
 return {...out,E,d,dE};
}
ok(p>0.618&&p<0.619&&p*p+p>0.99999999999999,'original Golden algebraic parameter');
ok(ready>0.45&&ready<0.46,'original paid common N1 readiness');
ok(r0>1.85e-6&&r0<1.86e-6,'original positive two-query null report');
const qNative=q3(ready,r0),E0=exactEnergy(qNative);
const sigma0=softBoltz(E0);
qNative.forEach((v,i)=>close(sigma0.q[i],v,2e-14,'native original ternary status Gibbs eigenvalue'));
close(Math.min(...E0),0,1e-14,'exact nonfitted ground-zero heat');
ok(E0[1]>0.24&&E0[1]<0.25&&E0[2]>17.5&&E0[2]<17.6,'original relative excited heat eigengaps');
ok(qNative[0]>qNative[1]&&qNative[1]>qNative[2],'nonuniform native algebraic probabilities');
close(T(qNative,E0).v,entropy(qNative)/b,5e-14,'original ternary entire thermal entropy');
close(entropy(qNative),binaryH(ready)+ready*binaryH(r0),4e-14,'full failure-READY entropy chain rule');
const coeff=-ready*Math.log((1-r0)/r0)/logphi;
close(coeff*d0,-12.4442926813187,5e-10,'older original J2 coefficient d0 retained, not fitted');
for(const rr of [r0,1.8513018e-6,.0031,.051,.17,.31,.56,.79,.91]){
 for(const g of [ready,.17,.57,.82]){
  const q=q3(g,rr),E=exactEnergy(q),Z=softBoltz(E);
  q.forEach((v,i)=>close(v,Z.q[i],2e-14,'all positive report chart Gibbs equality'));
  const thermo=T(q,E).v;
  close(thermo,entropy(q)/b,5e-14,'nonlinear thermal entropy entire off-null domain');
  const ddg=[-1,1-rr,rr],ddr=[0,-g,g];
  const dInfR=directional(q,ddr,'inf').d;
  const dInfG=directional(q,ddg,'inf').d;
  close(dInfR,g*Math.log((1-rr)/rr)/b,5e-13,'all off-null r source without log fit');
  close(dInfG,(Math.log((1-g)/g)+binaryH(rr))/b,5e-13,'readiness moving source not frozen');
  const h=Math.min(5e-7,rr/100,(1-rr)/100);
  const fp=T(q3(g,rr+h),exactEnergy(q3(g,rr+h))).v;
  const fm=T(q3(g,rr-h),exactEnergy(q3(g,rr-h))).v;
  close((fp-fm)/(2*h),dInfR,4e-7,'full unrestrained gradient via independent entropy values');
  // In independent actual heat coords the derivative MUST be rho-Gibbs,
  // not an invented coefficient or a finite difference of a scalar reporter.
  for(let j=0;j<3;j++){
    const hh=2e-5;
    const plus=E.slice(),minus=E.slice();plus[j]+=hh;minus[j]-=hh;
    const d=(T(q,plus).v-T(q,minus).v)/(2*hh);
    close(d,q[j]-Z.q[j],8e-7,'all three genuinely free thermal Euler rows');
  }
  const cq=-g*Math.log((1-rr)/rr)/logphi;
  close(cq,(-b/logphi)*dInfR,5e-13,'nonlinear native N1 entropy-CQ vs thermodynamic source');
  // Exact finite-K source bound; compare actual derivative against Gibbs entropy.
  for(const K of [1,2,3,7,32,128,512,2000]){
    const finite=directional(q,ddr,K);
    const delta=q.map(v=>{
      let tailUpper=(1-v)**(K+1)/((K+1)*v);
      return tailUpper;
    });
    const Delta=Math.max(...delta);
    const sigmaL1=finite.sigma.reduce((s,x,i)=>s+Math.abs(x-q[i]),0);
    ok(sigmaL1<=Math.expm1(Delta)+2e-13,'finite-K Gibbs full state trace-error bound');
    const eErr=Math.max(...finite.E.map((x,i)=>Math.abs(x-E[i])));
    ok(eErr<=2*Delta/b+3e-13,'finite-K heat operator norm error bound');
    const sourceError=Math.abs(finite.d-dInfR);
    const aDq=ddr.reduce((s,x)=>s+Math.abs(x),0);
    const maxLogD=Math.max(...q.map((v,i)=>Math.abs(ddr[i]/v)));
    const rhs=2*Delta*aDq/b+2*Math.expm1(Delta)*maxLogD/b;
    ok(sourceError<=rhs+2e-10,'native all-jet finite-K source-error budget');
    // Exact derivative of capped harmonic itself, no K finite difference:
    for(let j=0;j<3;j++){
      const analytic=-(1-(1-q[j])**K)/q[j];
      const rem=-1/q[j];
      close(analytic-rem,(1-q[j])**K/q[j],6e-9,'fixed K harmonic derivative-tail exact');
    }
  }
 }
}
// Exact already interval-certified h=1/4 has two distinct positive local
// reports. Construct formal independently variable tangents consistent
// with the ORIGINAL exact stationary covector, without claiming a new native
// field writer or rerunning the 42-root proof.
for(let k=0;k<42;k++){
 const ra=1.85124177e-6, rb=1.85131423e-6, g=ready;
 const da=Math.sin((k+1)*0.31)*1e-5;
 const hb=r=>Math.log((1-r)/r)/logphi;
 const db=-hb(ra)/hb(rb)*da;
 const cq=-g*(hb(ra)*da+hb(rb)*db);
 const th=directional(q3(g,ra),[0,-g*da,g*da],'inf').d+
          directional(q3(g,rb),[0,-g*db,g*db],'inf').d;
 close(cq,-b/logphi*th,5e-14,'formal 42-coordinate off-null source-cancellation transport');
}
const K=100_000_000;
const rare=Math.min(...qNative);
const logterm=(K+1)*Math.log1p(-rare);
const tail=Math.exp(logterm)/((K+1)*rare);
ok(tail<1e-37,'genuine native K=1e8 harmonic heat-tail upper');
const derivErr=Math.exp(K*Math.log1p(-rare))/rare;
ok(derivErr<1e-30,'genuine native K=1e8 harmonic first derivative error');
const Z913=1+12*Math.exp(-20*b)+10*Math.exp(-22*b)+8*Math.exp(-24*b)+2*Math.exp(-33*b);
close(Math.log(Z913*softBoltz(E0).Z)/b,
      Math.log(Z913)/b+Math.log(softBoltz(E0).Z)/b,5e-14,
      'unchanged original 33-scene tensor heat factorization');
console.log(JSON.stringify({status:"PASS",checks,originalGolden:{
  p,betaBook:b,alphaBeta:ready,r0,d0,
  statusProbabilities:qNative,
  renewalHeatEigenvalues:E0,
  CQToOriginalJ2:coeff*d0
 },nativeFiniteCap:K,harmonicHeatTailUpper:tail,
  sourceGainIdentity:"D CQ_native=-(betaBook/log(phi)) D(E_rho+H_Gibbs) for fixed readiness",
  transcendenceProof:"classical Lindemann theorem, not numerically certified",
  compulsoryBookHodgeAdmission:"OPEN",GR_closed:false}));
