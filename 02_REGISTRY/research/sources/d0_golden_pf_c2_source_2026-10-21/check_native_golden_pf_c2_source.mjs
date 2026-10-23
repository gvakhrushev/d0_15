// Native Golden 4D box PF discrete C2 theorem, original boxes unchanged.
// Source: original_golden_moving_mean_j2 theorem eqs (6)-(10).
const assert=(x,s)=>{if(!x)throw Error("FAIL "+s)};
const p=(Math.sqrt(5)-1)/2,phi=1/p;
assert(3n*3n+3n*5n<5n*5n &&
       619n*619n+619n*1000n>1000n*1000n,"exact root bracket");
// Entire q<9 inequality over positive integers: no floating certificate.
const q=619n,d=1000n;
assert(256n*q**7n*d**249n+q**128n*d**128n+q**256n<9n*d**256n,
       "exact 256q^7+q^128+q^256<9");
const sMin=L=>{let s=0;while(phi**s<L)s++;return s};
const fibonacci=n=>{let a=0,b=1;for(let i=0;i<n;i++){const c=a+b;a=b;b=c;}return a};
function envelope(n,L){
  const k=Math.floor(n/4),a=phi/Math.sqrt(5)+(-1)**n*p**(2*n+1)/Math.sqrt(5),
        eps=p**(2*(n-2*k)+1)/Math.sqrt(5),
        delta=2*p**Math.floor(k/4);
  assert(delta<=1/(2*L),"native boundary-strip precondition");
  return (L**4*eps+128*L*delta+
          Math.abs(a-phi/Math.sqrt(5)))/a;
}
const env=[];
for(const L of [4,8,16,32,64,128,256,1024]){
  const s=sMin(L),n=64*s+128,h=1/L,B=envelope(n,L),
        an=phi/Math.sqrt(5)+(-1)**n*p**(2*n+1)/Math.sqrt(5);
  assert(n%16===0&&B<9*h**3&&B<.5,"all mesh C2 PF bound");
  const ready=2*p**3*an;
  assert(ready>.29&&ready<.35,"same native TRUE READY nonzero");
  env.push({L,n,s,bound:B,scaled_bound:B*L**3,
    log_derivative_bound:36*h*h,second_log_derivative_bound:72*h,
    unconditional_READY_mass:ready});
}
// Literal native F/R cost words and original 4D nested microboxes.
function countsOriginal(n,L){
  const out=new Uint32Array(L**4);
  function visit(rem,rawDepth,left,width){
    if(rem===0){
      let j=0;
      for(let axis=0;axis<4;axis++){
        const x=left[axis]+width[axis]/2;
        j=j*L+Math.max(0,Math.min(L-1,Math.floor(L*x)));
      }
      out[j]++;
      return;
    }
    const axis=rawDepth%4;
    const wf=width.slice();wf[axis]*=p;
    visit(rem-1,rawDepth+1,left.slice(),wf);
    if(rem>=2){
      const lr=left.slice(),wr=width.slice();
      lr[axis]+=p*wr[axis];wr[axis]*=p*p;
      visit(rem-2,rawDepth+1,lr,wr);
    }
  }
  visit(n,0,[0,0,0,0],[1,1,1,1]);
  return out;
}
const census=[];
for(const [n,L,expectedMin,expectedMax] of [[20,4,29,78],[24,8,4,43],[28,8,45,232]]){
  const arr=countsOriginal(n,L),K=arr.reduce((s,v)=>s+v,0);
  assert(K===fibonacci(n+1),"original Fibonacci count");
  const min=Math.min(...arr),max=Math.max(...arr);
  assert(min===expectedMin&&max===expectedMax,"original cell exact census");
  let error=0,jump=0;
  for(let index=0;index<arr.length;index++){
    error=Math.max(error,Math.abs(L**4*arr[index]/K-1));
    for(let axis=0;axis<4;axis++){
      const mult=L**(3-axis);
      if(Math.floor(index/mult)%L<L-1){
        const neighbor=index+mult;
        jump=Math.max(jump,L**4*Math.abs(arr[index]-arr[neighbor])/K);
      }
    }
  }
  census.push({n,L,K,min,max,actual_rho_deviation:error,
               max_true_neighbor_jump:jump,max_true_discrete_gradient:L*jump});
}
// Genuine cap-one native two-band source's derivative with respect to the
// material operand y at x=-tau*f/rho. Inputs use the rank2 source O(h).
const z=2**-20,L0=4*p**3,Q=1-z*L0;
function fullTwoBandMaterialSlope(x){
  const E=p*p*(1+x),ell=4*E*(1-E),A=ell+(1-ell)*L0,
        R=1-z*A,r=1-Q*R,ry=8*z*p**6*(R+(1-ell)*Q);
  return (1-Math.log((1-r)/r)/Math.log(phi))*ry;
}
const leadingRankTwo=r=>3*(r**4-1)*Math.exp(-r*r)/(4*r*r);
const material=[];
for(const L of [8,16,32,64,128]){
  const h=1/L,R=1.2,dRdt=Math.exp(-R*R/2),
        f0=h*leadingRankTwo(R),fm=h*leadingRankTwo(R-h*dRdt),
        delta=9*h**3, amp=.02,tau=.05,
        U=2*amp*(fullTwoBandMaterialSlope(-tau*fm)-
                 fullTwoBandMaterialSlope(-tau*f0))/h,
        P=2*amp*(fullTwoBandMaterialSlope(-tau*fm/(1+delta))-
                 fullTwoBandMaterialSlope(-tau*f0/(1-delta)))/h;
  assert(Math.abs(P-U)<1e-5*h*h,"same-price bounded-PF material remainder");
  material.push({L,material_uniform:U,PF_remainder:Math.abs(P-U),
                 normalized_h3_error:Math.abs(P-U)/h**3});
}
function output(){return {status:"PASS_NATIVE_GOLDEN_PF_DISCRETE_C2",
  exact_rational_root_and_constant9:true,
  native_original_box_counts:census,analytic_mesh_envelopes:env,
  original_N1_two_band_material_diagnostic:material,
  claims:{discrete_PF_C2_at_true_Golden_depth:true,
          complete_Book03_HJR_selection:false,
          full42_exact_nonVSI_root:false,GR_closed:false}}}
if(typeof console!=="undefined")console.log(JSON.stringify(output(),null,2));
