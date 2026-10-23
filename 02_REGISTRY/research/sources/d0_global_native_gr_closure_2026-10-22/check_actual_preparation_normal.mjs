// Exact actual q-bank fixture and ordered second-B-table normal.
// No new native continuous writer or compulsory joint-bank domain is assumed.
function checkActualPreparationNormalSource() {
  const abs=x=>x<0n?-x:x,gcd=(x,y)=>{x=abs(x);y=abs(y);while(y){[x,y]=[y,x%y];}return x;};
  const q=(a,b=0n,d=1n)=>{a=BigInt(a);b=BigInt(b);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){a=-a;b=-b;d=-d;}const g=gcd(gcd(a,b),d);return[a/g,b/g,d/g];};
  const add=(x,y)=>q(x[0]*y[2]+y[0]*x[2],x[1]*y[2]+y[1]*x[2],x[2]*y[2]);
  const neg=x=>q(-x[0],-x[1],x[2]),sub=(x,y)=>add(x,neg(y));
  const mul=(x,y)=>q(x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1],x[2]*y[2]);
  const scale=(x,n,d=1n)=>mul(x,q(n,0n,d));
  const one=q(1),zero=q(0),p=q(0,1),zeta=q(1,0,1048576);
  const pow=(x,n)=>{let y=one;while(n){if(n%2)y=mul(y,x);x=mul(x,x);n=Math.floor(n/2);}return y;};
  const eq=(x,y)=>x.every((v,j)=>v===y[j]);
  const fmt=x=>({a:x[0].toString(),b:x[1].toString(),denominator:x[2].toString()});
  const pLo=[618033988749894n,1000000000000000n],pHi=[618033988749895n,1000000000000000n];
  const rootSign=x=>x[0]*x[0]+x[0]*x[1]-x[1]*x[1];
  const lowerNumerator=x=>{const e=x[1]>=0n?pLo:pHi;return x[0]*e[1]+x[1]*e[0];};
  const upperNumerator=x=>{const e=x[1]>=0n?pHi:pLo;return x[0]*e[1]+x[1]*e[0];};
  let n=0;const checks=[];const ck=(b,name)=>{if(!b)throw Error(name);n++;checks.push(name);};
  ck(rootSign(pLo)<0n&&rootSign(pHi)>0n,"strict rational enclosure of the positive Golden root");
  ck(eq(add(p,pow(p,2)),one),"p+p^2=1");

  // Actual O sign sectors: beta=(1,1)/sqrt(2), beta_perp=(1,-1)/sqrt(2).
  // rho'(0)=|beta_perp beta_perp><beta beta|+adjoint, exact denominator 4.
  const sg=[1n,-1n,-1n,1n],dr=Array.from({length:16},(_,k)=>q(sg[Math.floor(k/4)]+sg[k%4],0,4));
  let trace=zero;for(let i=0;i<4;i++)trace=add(trace,dr[4*i+i]);
  ck(eq(trace,zero),"normalized Bell tangent has zero trace");
  for(let i=0;i<2;i++)for(let j=0;j<2;j++){
    let left=zero,right=zero;
    for(let a=0;a<2;a++){left=add(left,dr[(2*i+a)*4+(2*j+a)]);right=add(right,dr[(2*a+i)*4+(2*a+j)]);}
    ck(eq(left,zero),"first single-resource reduced density derivative "+i+","+j);
    ck(eq(right,zero),"second single-resource reduced density derivative "+i+","+j);
  }
  let pair=zero;for(let i=0;i<4;i++)pair=add(pair,scale(dr[i*4+i],sg[i]));
  ck(eq(pair,q(2)),"actual pair observable first derivative is 2");
  // All other decoded coordinates and the untouched RIGHT factor are fixed.
  // Actual primary psi=2^-10*(u,u/2), s=p^3, eta_22=-1.
  // Dividing out B_D^2/rho, h^2 cancels exactly against the two increments.
  const epsilon=q(1,0,1024),h=q(1,0,4);
  const du=mul(epsilon,h),du2=scale(du,1,2);
  const sumSquares=add(mul(du,du),mul(du2,du2));
  const dq=neg(scale(mul(pow(p,6),sumSquares),32)); // 2/h^2=32
  const expectedDQ=scale(pow(p,6),-5,2097152);
  ck(eq(dq,expectedDQ),"actual nonvacuum q-source coefficient -(5/2)*p^6*2^-20");
  ck(upperNumerator(dq)<0n,"actual q-source is strictly nonzero, before any report");

  const L0=scale(pow(p,3),4),M0=mul(L0,add(one,pow(p,6)));
  const Q0=sub(one,mul(zeta,L0)),R0=sub(one,mul(zeta,M0)),r0=sub(one,mul(Q0,R0));
  ck(lowerNumerator(r0)>0n,"r0 is positive");
  ck(lowerNumerator(sub(scale(zeta,2),r0))>0n,"r0<2*zeta");
  ck(lowerNumerator(sub(pow(p,2),scale(zeta,2)))>0n,"2*zeta<p^2");
  ck(lowerNumerator(R0)>0n,"R0 is positive");
  // Dual arithmetic differentiates the ORDERED first q slot in the SECOND B table.
  const C=x=>[x,zero],plus=(x,y)=>[add(x[0],y[0]),add(x[1],y[1])];
  const minus=(x,y)=>[sub(x[0],y[0]),sub(x[1],y[1])];
  const times=(x,y)=>[mul(x[0],y[0]),add(mul(x[1],y[0]),mul(x[0],y[1]))];
  const unit=C(one);
  const B=(xs,tau,sigma)=>{
    const bs=xs.map(x=>plus(C(p),times(C(scale(mul(pow(p,2),tau),sigma)),x)));
    return times(C(q(4)),times(times(bs[0],bs[1]),minus(unit,times(bs[2],bs[3]))));
  };
  let normalized=null;
  for(const m of [0,1,2,5,11,29])for(const sigma of [-1n,1n]){
    const tau=pow(p,m),bs=B([[zero,dq],C(zero),C(zero),C(zero)],tau,sigma);
    const report=minus(unit,times(C(R0),minus(unit,times(C(zeta),bs))));
    const expected=scale(mul(mul(mul(mul(zeta,R0),pow(p,4)),tau),dq),4n*sigma);
    ck(eq(report[0],r0),"ordered table keeps the actual base report m="+m+" sigma="+sigma);
    ck(eq(report[1],expected),"ordered first-slot actual source m="+m+" sigma="+sigma);
    const N=scale(mul(mul(mul(zeta,R0),pow(p,4)),dq),4n*sigma);
    ck(eq(report[1],mul(tau,N)),"exact normalized source independent of Golden attenuation m="+m+" sigma="+sigma);
    if(m===0&&sigma===-1n)normalized=N;
  }
  // At sigma=-1, Dr/tau>0 and 1-h_phi'(r0)<0 because r0<p^2 and h_phi'(p^2)=1.
  ck(lowerNumerator(normalized)>0n,"actual sigma=-1 report normal derivative is positive");
  const pv=(Math.sqrt(5)-1)/2,ph=1/pv;
  const val=x=>(Number(x[0])+Number(x[1])*pv)/Number(x[2]);
  // r0 and normalized coefficients have cancellations; diagnostics evaluated by factored formula.
  const l=4*pv**3,mm=l*(1+pv**6),qq=1-(2**-20)*l,rr=1-(2**-20)*mm;
  const r=(2**-20)*(l+mm)-(2**-40)*l*mm;
  const dqv=-(5/2)*pv**6*2**-20;
  const drv=-4*2**-20*rr*pv**4*dqv;
  const costCoefficient=drv*(1-Math.log((1-r)/r)/Math.log(ph));
  return {status:"PASS",arithmetic:"exact Q(p) BigInt fractions and exact rational Golden enclosure",assertions:n,checks,
    exact:{dq_divided_by_BD2_over_rho:fmt(dq),r0:fmt(r0),Dr_divided_by_tau_BD2_over_rho:fmt(normalized)},
    diagnostic_only:{r0:r,qNormalCoefficient:dqv,normalizedPriceNormalCoefficient:costCoefficient},
    analytic_entropy_sign:"r0<p^2; h_phi'(r) strictly decreasing; h_phi'(p^2)=1; therefore 1-h_phi'(r0)<0",
    scope:{moment_bank:"actual polynomial q, actual primary material psi=2^-10*(u,u/2), s=p^3, h=1/4",
      variation_domain:"arbitrary joint bank purifications with untouched original RIGHT; no new finite Golden smooth writer claimed",
      upstream_preparation_price:"not set to zero; exact opposite derivative is required for full stationarity",
      full_D0_price_selected:false,GR_closed:false}};
}
console.log(JSON.stringify(checkActualPreparationNormalSource(), null, 2));
