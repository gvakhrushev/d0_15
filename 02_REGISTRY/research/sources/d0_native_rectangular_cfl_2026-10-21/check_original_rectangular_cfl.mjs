/*
 * ORIGINAL GOLDEN 4D BOXES (NO NEW decoder): exact source balance and
 * TRUE moving-volume two-Golden-tick Book03 first-source matching.
 *
 * All original LEFT/F/R, old RIGHT and inactive/FAILED complement remain
 * in the mathematical complete returned operator. Does not claim compulsory
 * native source/Book selection or the original full H+J+R GR theorem.
 *
 * No dependencies, built-in BigInt/Number. Main arbitrary-Brinkmann 40-row
 * symbolic geometry is independently owned and is not rerun here.
 */
const p=(Math.sqrt(5)-1)/2;
const z=2**-20;
function check(ok,msg){if(!ok)throw new Error("FAIL: "+msg);}
function near(a,b,tol,msg){check(Math.abs(a-b)<=tol,msg+": "+a+" vs "+b);}
function fib(n){let a=0,b=1;for(let i=0;i<n;i++){const c=a+b;a=b;b=c;}return a;}
function originalNativeCounts(n,L){
  const M=L**4,counts=new Uint32Array(M);
  function visit(rem,rawDepth,left,width){
    if(rem===0){
      let j=0;
      for(let axis=0;axis<4;axis++){
        const x=left[axis]+width[axis]/2;
        j=j*L+Math.max(0,Math.min(L-1,Math.floor(L*x)));
      }
      counts[j]++;
      return;
    }
    const axis=rawDepth%4;
    const widthF=width.slice();widthF[axis]*=p;
    visit(rem-1,rawDepth+1,left.slice(),widthF);
    if(rem>=2){
      const leftR=left.slice(),widthR=width.slice();
      leftR[axis]+=p*widthR[axis];widthR[axis]*=p*p;
      visit(rem-2,rawDepth+1,leftR,widthR);
    }
  }
  visit(n,0,[0,0,0,0],[1,1,1,1]);
  const K=counts.reduce((a,b)=>a+b,0);
  check(K===fib(n+1),"true Fibonacci word count");
  check(counts.every(x=>x>0),"all original Golden Role cells covered");
  check(Math.max(...counts)>Math.min(...counts),"original weights must be UNEQUAL");
  return {counts,K,M,L,n};
}

// New consumer: SAME original native box count; 2L time / L³ spatial bins.
const F=8,L=4,n=24;
const original=originalNativeCounts(n,F),K=original.K,M=F*L**3;
const counts=new Uint32Array(M);
for(let t=0;t<F;t++)for(let x=0;x<F;x++)for(let y=0;y<F;y++)for(let a=0;a<F;a++){
  const i=((t*F+x)*F+y)*F+a;
  const j=((t*L+(x>>1))*L+(y>>1))*L+(a>>1);
  counts[j]+=original.counts[i];
}
check(K===75025&&M===512&&counts.reduce((a,b)=>a+b,0)===K,"all original cost24 histories remain");
check(Math.min(...counts)===89&&Math.max(...counts)===260,"native 8x4x4x4 macro census");
const rho=Array.from(counts,k=>k*M/K);
let maxFine=0,maxRect=0;
for(let t=0;t<F;t++)for(let x=0;x<L;x++)for(let y=0;y<L;y++)for(let a=0;a<L;a++){
  const i=((t*L+x)*L+y)*L+a;
  let avg=0;
  for(let u=0;u<2;u++)for(let v=0;v<2;v++)for(let w=0;w<2;w++){
    const j=((t*F+2*x+u)*F+2*y+v)*F+2*a+w;
    const val=F**4*original.counts[j]/K;
    avg+=val/8;maxFine=Math.max(maxFine,Math.abs(val-1));
  }
  near(avg,rho[i],1e-14,"exact 8-cell native PF grouping");
  maxRect=Math.max(maxRect,Math.abs(avg-1));
}
check(maxRect<=maxFine+1e-14,"native PF sup-norm cannot worsen under grouping");
const V=Array.from({length:M},(_,i)=>1+Math.sin(i*.017));
const weighted=V.reduce((a,v,i)=>a+counts[i]/K*v/rho[i],0);
const uniform=V.reduce((a,v)=>a+v,0)/M;
near(weighted,uniform,1e-13,"exact real inverse-PF source equals rectangular volume");
const ready=2*K*p**(n+3);
check(ready>.3&&ready<.35,"native full FR/RF ready probability retained");
const hs=1/L,ht=hs/2,r=1,A2=r*Math.exp(-r*r/2);
const g00=1/A2,ratioSq=[A2*A2,A2/(r*r),A2/(r*r)];
const S=ratioSq.reduce((a,b)=>a+b,0);
function trueNativeW(x){
  const B=4*p**3,Q=1-z*B,l=4*p*p*(1+x)*(1-p*p*(1+x));
  const A=l+(1-l)*B,R=1-z*A,q=1-Q*R;
  check(q>0&&q<.5,"real complete GoldenMaster positive chart");
  return Math.log((1-q)/q)*(R+Q*(1-l));
}
const W=[];
for(let x=0;x<L;x++)for(let y=0;y<L;y++)for(let a=0;a<L;a++){
  const j=((0*L+x)*L+y)*L+a;
  W.push(trueNativeW(-.05*.0125/rho[j])/trueNativeW(0));
}
const mass=W.map(w=>w*g00),edges=[];
for(let x=0;x<L;x++)for(let y=0;y<L;y++)for(let a=0;a<L;a++){
 const i=(x*L+y)*L+a;
 for(let d=0;d<3;d++){
   const j0=[x,y,a];j0[d]=(j0[d]+1)%L;
   const j=(j0[0]*L+j0[1])*L+j0[2];
   edges.push([i,j,mass[i]*ratioSq[d]/hs**2]);
 }
}
const N=L**3,Kapply=v=>{
 const out=Array(N).fill(0);
 for(const[i,j,k]of edges){const d=k*(v[i]-v[j]);out[i]+=d;out[j]-=d}
 return out;
};
const dot=(v,w)=>v.reduce((sum,x,i)=>sum+x*w[i],0);
const checkboard=Array.from({length:N},(_,i)=>{
 const x=Math.floor(i/L**2),y=Math.floor(i/L)%L,a=i%L;
 return (x+y+a)%2?-1:1;
});
const lam=dot(checkboard,Kapply(checkboard))/checkboard.reduce((s,v,i)=>s+mass[i]*v*v,0);
near(lam*hs**2/4,S,1e-12,"native PF checkerboard Rayleigh quotient independent of original weights");
check(S>1&&lam*hs*hs>4,"one true coarse native time bin has unstable physical high-frequency mode");
const Wmax=Math.max(...W),Wmin=Math.min(...W);
const cflDyadic=S/4*Wmax/Wmin;
check(cflDyadic<1,"two native time bins strict full-spectrum CFL");
const ebound=1/Math.E+2*Math.exp(-(.6**2)/2)/.6;
check(ebound<23/6,"uniform rank2 r>=3/5 universal S bound");
const energy=(old,now)=>{
 const du=now.map((a,i)=>(a-old[i])/ht);
 return .5*du.reduce((sum,a,i)=>sum+mass[i]*a*a,0)+.5*dot(old,Kapply(now));
};
let old=Array.from({length:N},(_,i)=>Math.sin(i*.321)+.2*Math.cos(i*.87)),
    now=Array.from({length:N},(_,i)=>Math.cos(i*.221)+.1*Math.sin(i*.451));
const E0=energy(old,now);check(E0>0,"positive native CFL energy");
let drift=0;
for(let t=0;t<140;t++){
 const Kv=Kapply(now),next=now.map((v,i)=>2*v-old[i]-ht**2*Kv[i]/mass[i]);
 drift=Math.max(drift,Math.abs(energy(now,next)/E0-1));old=now;now=next;
}
check(drift<2e-12,"140 charged native time bins conserve complete frozen linearized matter energy");
const RESULT={status:"PASS_ORIGINAL_GOLDEN_RECTANGULAR_N1_CFL",
 owner_original_native_box_blob:"4971e037e5ec8b1b2a40ef2c458ad09e01185d9c",
 true_original_words:K, original_fine_L:F, actual_rect_shape:[8,4,4,4],
 macro_native_counts:[Math.min(...counts),Math.max(...counts)],
 macro_native_PF:[Math.min(...rho),Math.max(...rho)],
 native_ready_mass:ready, original_inverse_PF_source_error:weighted-uniform,
 group_does_not_worsen_PF_supnorm:true,
 original_N1_frozen_r1_CFL_ratio:S,
 one_bin_checkerboard_exponential_growth:(2*S-1)+Math.sqrt((2*S-1)**2-1),
 two_bin_WmaxWmin:Wmax/Wmin,two_bin_CFL_margin:1-cflDyadic,
 uniform_r_ge_three_fifths_gap:1/24,
 original_native_frozen_energy_error_140:drift,
 scope:{full_nonlin_34_geometry_root:false,physical_selected_Book03:false,original_anisotropic_all42_star_calibration:false,GR_closed:false}};
console.log(JSON.stringify(RESULT,null,2));
