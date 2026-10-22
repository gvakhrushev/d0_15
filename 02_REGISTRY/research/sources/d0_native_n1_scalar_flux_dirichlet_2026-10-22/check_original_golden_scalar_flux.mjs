// D0 exact one-dimensional matter Euler / true original Golden n24,L8
// Full original nonlinear N1 sigma-minus reporter; no affine replacement.
// Original six-face rank-two scalar closed formula and PF boxes.
//
// This is an executable bounded test plus local analytic strict-convexity
// proof consumer, not 42-eq native physical Book03 closure.
const p=(Math.sqrt(5)-1)/2,z=2**-20,tau=1/20,kappa=23.416406751884075;
const check=(x,m)=>{if(!x)throw Error("FAIL "+m)};
function fib(n){let a=0,b=1;for(let i=0;i<n;i++){const c=a+b;a=b;b=c}return a}
function nativeCounts(n,L) {
 const counts=new Uint32Array(L**4);
 function visit(rem,d,left,width){
  if(rem===0){
   let idx=0;for(let j=0;j<4;j++)idx=idx*L+Math.max(0,Math.min(L-1,Math.floor(L*(left[j]+width[j]/2))));
   counts[idx]++;return;
  }
  const j=d%4,short=width.slice();short[j]*=p;visit(rem-1,d+1,left.slice(),short);
  if(rem>=2){const right=left.slice(),long=width.slice();right[j]+=p*long[j];long[j]*=p*p;visit(rem-2,d+1,right,long)}
 }
 visit(n,0,[0,0,0,0],[1,1,1,1]);
 const K=counts.reduce((a,b)=>a+b,0);
 check(K===fib(n+1),"literal original Fibonacci enumeration");
 check(Math.min(...counts)===4&&Math.max(...counts)===43,"exact native L8 PF range");
 return {counts,K};
}
function intExp(a,b){
 const N=200,h=(b-a)/N;let s=Math.exp(a*a/2)+Math.exp(b*b/2);
 for(let j=1;j<N;j++)s+=(j%2?4:2)*Math.exp((a+j*h)**2/2);
 return s*h/3;
}
function rad(t){
 let lo=.1,hi=2.2;
 for(let i=0;i<70;i++){const x=(lo+hi)/2;if(intExp(1,x)<t)lo=x;else hi=x}
 return (lo+hi)/2;
}
function st(t){const r=rad(t),A=Math.sqrt(r)*Math.exp(-r*r/4);return {r,A,B:1/A,k1:(1-1/r**2)/2,k2:Math.exp(-r*r/4)/Math.sqrt(r)}}
function comm(a,b){return Math.sinh(a)*Math.sinh(b)*(1-.5*(Math.cosh(a)-1)*(Math.cosh(b)-1))}
function star(a,b,h){
 return (a.r*a.r*Math.sinh(h*(b.k1-a.k1))
  +2*a.B*a.r*Math.sinh(h*(b.k2-a.k2))
  +2*a.A*a.r*comm(h*a.k1,h*a.k2)
  +a.A*a.B*comm(h*a.k2,h*a.k2))/(h*h);
}
function raw(x,ym){
 const E=p*p*(1+x),ell=4*E*(1-E),v=p-p*p*ym;
 const B=4*v*v*(1-v*v),A=ell+(1-ell)*B;
 return {r:1-(1-z*B)*(1-z*A),E,ell,v,B,A};
}
const r0=raw(0,0).r,lnphi=Math.log(1/p);
const entropy=r=>-(r*Math.log(r)+(1-r)*Math.log1p(-r))/lnphi;
const F=(x,y)=>-entropy(raw(x,y).r)+entropy(r0);
function Fy(x,y){
 const t=raw(x,y);
 const Br=8*t.v*(1-2*t.v*t.v)*p*p;
 const rr=z*(1-z*t.A)+z*(1-z*t.B)*(1-t.ell);
 return Math.log((1-t.r)/t.r)/lnphi *rr*Br;
}
const L=8,n=24,h=1/L,N=L,census=nativeCounts(n,L);
const eps=(1/(2*kappa))**.5,rows=[];
for(let j=0;j<N;j++){
 const idx=((j*L+3)*L+3)*L+3;
 const aa=st((j-3.5)*h),bb=st((j-2.5)*h);
 rows.push({j,count:census.counts[idx],rho:L**4*census.counts[idx]/census.K,
  f:star(aa,bb,h),g:1/aa.A**2,v:eps,u0:eps*aa.A**2});
}
const X=a=>-tau*a.f/a.rho,
      Y=(a,u)=>tau*(a.g*u*u-a.v*a.v/a.g)/a.rho,
      current=(a,u)=>a.g*u*Fy(X(a),Y(a,u));
const positive=(a,u)=>{
 const eps=1e-6;return (current(a,u+eps)-current(a,u-eps))/(2*eps);
};
check(rows.every(a=>positive(a,a.u0)>0),"elliptic original nonlinear native F");
function inverse(a,J){
 let lo=a.u0-.18,hi=a.u0+.18;
 check(current(a,lo)<J&&J<current(a,hi),"current bracket");
 for(let k=0;k<65;k++){const q=(lo+hi)/2;if(current(a,q)<J)lo=q;else hi=q}return (lo+hi)/2;
}
const u0=rows.map(a=>a.u0),boundary=h*u0.reduce((a,b)=>a+b,0);
let lo=Math.max(...rows.map(a=>current(a,a.u0-.07))),
    hi=Math.min(...rows.map(a=>current(a,a.u0+.07)));
check(lo<hi,"common current chart");
function total(J){return h*rows.reduce((s,a)=>s+inverse(a,J),0)}
check(total(lo)<boundary&&total(hi)>boundary,"fixed exact endpoint attainable");
for(let k=0;k<75;k++){const J=(lo+hi)/2;if(total(J)<boundary)lo=J;else hi=J}
const J=(lo+hi)/2,u=rows.map(a=>inverse(a,J));
function psis(U){let a=[0];for(const w of U)a.push(a.at(-1)+h*w);return a}
const p0=psis(u0),sol=psis(u);
const act=P=>rows.reduce((s,a,j)=>s+h*a.rho*F(X(a),Y(a,(P[j+1]-P[j])/h)),0);
const euler=(P,j)=>2*tau*(current(rows[j-1],(P[j]-P[j-1])/h)-current(rows[j],(P[j+1]-P[j])/h));
const finite=(P,j)=>{const k=2e-6,A=P.slice(),B=P.slice();A[j]+=k;B[j]-=k;return (act(A)-act(B))/(2*k)};
const max=a=>Math.max(...a.map(Math.abs)),before=max(Array.from({length:N-1},(_,j)=>euler(p0,j+1))),
 after=max(Array.from({length:N-1},(_,j)=>euler(sol,j+1))),
 independent=max(Array.from({length:N-1},(_,j)=>finite(sol,j+1)));
const stiffness=Math.min(...rows.map((a,j)=>positive(a,u[j]))),
 correction=max(u.map((v,j)=>v-u0[j]));
check(before>1e-11,"nonzero actual uncorrected matter source");
check(after<1e-12&&independent<2e-10,"original complete nonlinear matter Euler vanished");
check(Math.abs(sol.at(-1)-p0.at(-1))<1e-12,"endpoints actually fixed");
check(stiffness>0,"strict local scalar convexity");
function report(){return {status:"PASS_FULL_N1_MATERIAL_FLUX_DIRICHLET_ROOT_ORIGINAL_GOLDEN",n,L,true_cost_n_words:census.K,actual_count_range:[Math.min(...census.counts),Math.max(...census.counts)],site_counts:rows.map(a=>a.count),actual_site_rho:rows.map(a=>a.rho),six_face_f:rows.map(a=>a.f),full_nonlinear_r0:r0,first_material_euler_before:before,first_material_euler_after:after,independent_action_variation_max:independent,uniform_flux:J,strict_flux_monotonicity_min:stiffness,maximum_scalar_gradient_correction:correction,endpoint_error:sol.at(-1)-p0.at(-1),claim:"Unique strict local Dirichlet stationary matter lift, NOT whole 42 root",physical_Book03_selected:false,whole_42_euler_zero:false,GR_closed:false}}
console.log(JSON.stringify(report(),null,2));
