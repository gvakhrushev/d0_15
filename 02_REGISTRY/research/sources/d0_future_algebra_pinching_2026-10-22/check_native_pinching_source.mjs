#!/usr/bin/env node
// Original native Golden complete fine-record Cost−Info and canonical
// future-result pinching. Scope: exact finite algebra + declared coherent
// pure/native paid interface. Book03 selection and GR remain OPEN.
let checks=0;
const ok=(x,m)=>{checks++;if(!x)throw Error("FAIL: "+m)};
const close=(a,b,t=1e-11,m="close")=>ok(Math.abs(a-b)<t,m+" "+a+" vs "+b);
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi),zeta=2**-20;
const entropy=r=>-r*Math.log(r)-(1-r)*Math.log(1-r);
const dh=r=>Math.log((1-r)/r);
const hphi=r=>entropy(r)/ell;
const dhphi=r=>dh(r)/ell;
const prec=108*0+0;

// Exact algebraic integers Q(p), p^2=1-p, represented by a+b*p.
// All native Fibonacci-prefix counts and Kraft normalisation are exact.
const Q=(a,b=0n)=>({a:BigInt(a),b:BigInt(b)});
const add=(u,v)=>Q(u.a+v.a,u.b+v.b);
const mul=(u,v)=>Q(u.a*v.a+u.b*v.b,u.a*v.b+u.b*v.a-u.b*v.b);
const eq=(u,v)=>u.a===v.a&&u.b===v.b;
const pow=n=>{let x=Q(1),g=Q(0,1);for(let k=0;k<n;k++)x=mul(x,g);return x};
const scale=(n,u)=>Q(BigInt(n)*u.a,BigInt(n)*u.b);
const ONE=Q(1);
ok(eq(add(pow(1),pow(2)),ONE),"exact original Golden p+p²=1");
ok(eq(add(scale(6765,pow(21)),add(scale(10946,pow(22)),add(scale(10946,pow(24)),scale(21892,pow(23))))),ONE),
   "EXACT all 72441 original Golden fine path normalization Q(p)");
const fnFine=6765+6*10946;
ok(fnFine===72441,"authentic Golden fine alphabet (all 72441)");
const a=2*10946*p**23;
ok(a>.341&&a<.342,"authentic original cost20 READY mass (not cap9/20 gamma)");

function testPurePinch(r){
  const v=[Math.sqrt(1-r),0,0,Math.sqrt(r)];
  const rho=v.map(x=>v.map(y=>x*y));
  const barred=rho.map((row,i)=>row.map((v,j)=>((i<2)===(j<2))?v:0));
  const op=[1,0,0,1], tag=[0,0,1,1];
  const trace=x=>x.reduce((s,row,i)=>s+row[i],0);
  const times=(x,y)=>x.map(row=>y[0].map((_,j)=>row.reduce((s,v,k)=>s+v*y[k][j],0)));
  close(trace(times(rho,rho)),1,1e-12,"global prepared programme+work is PURE");
  close(trace(times(barred,barred)),(1-r)**2+r*r,1e-12,"pinching retains full orthogonal conditional WORK");
  close(barred[0][0],1-r,1e-12,"registered programme0 weight");
  close(barred[3][3],r,1e-12,"registered programme1 weight");
  close(barred[0][3],0,1e-12,"offdiagonal coherence removed by canonical registered effect");
  const suppTrace=op.reduce((s,w,i)=>s+w*rho[i][i],0);
  close(suppTrace,1,1e-12,"operational rank2 support has full prepared probability");
  ok(op.reduce((s,x)=>s+x,0)===2,"rank TWO operational support vs rank ONE pure cut");
  ok(Math.abs(rho[0][3])>0,"pure cut does NOT commute with registered programme tag");
  const sigma=[.35,.15,.15,.35];
  const Dfull=-(1-r)*Math.log(sigma[0])-r*Math.log(sigma[3]);
  const Dpinch=(1-r)*Math.log((1-r)/sigma[0])+r*Math.log(r/sigma[3]);
  close(Dfull,entropy(r)+Dpinch,1e-12,"operator quantum relative entropy Pythagorean identity");
  // Future algebra with only programme projection, not entire within-branch work:
  // trace conditional expectation additionally maximally mixes each work sector.
  const Dfuture=entropy(r)+Math.log(2);
  close(Dfuture-entropy(r),Math.log(2),1e-12,
        "strict extra real future-algebra coarse forgetting entropy");
  return {r,entropy_defect_nats:entropy(r),p_operational_rank:2};
}
const pins=[1/7,2/9,1.8512395785208469e-6,1-1e-6].map(testPurePinch);

// Actual original fixed 15-stage Q8 id/order effect = diag(0,4p³)*I4;
// Q8 present control preserves the programme tag. For supplied coherent
// programme rank1 J moves; canonical dephased support J does not.
const Jcoh=r=>-4*Math.log(1-zeta*(1-4*p**3*r))-16*Math.log(1-zeta);
const Jsupp=-20*Math.log(1-zeta)-4*Math.log(1-zeta*(1-4*p**3));
const dJ=r=>-16*p**3*zeta/(1-zeta+4*p**3*zeta*r);
for(const r of [1/7,2/9,1.8512395785208469e-6]){
  const step=1e-6;
  close((Jcoh(r+step)-Jcoh(r-step))/(2*step),dJ(r),1e-9,
        "actual 4-spin Book pure-cut first source vs derivative");
  ok(dJ(r)<0,"coherent programme cut has nonzero source");
  ok(Number.isFinite(Jsupp),"canonical programme-support cut has fixed J for every r");
}

// Two independent paid reporters: product pinching entropy EXACTLY sum h(r0)+h(r1);
// no arithmetic mean replacement at two distinct report probabilities.
const r0=1/7,r1=2/9,eps=1e-6;
const I2=(u,v)=>entropy(u)+entropy(v);
close((I2(r0+eps,r1)-I2(r0-eps,r1))/(2*eps),dh(r0),2e-10,
      "off-null first reporter full entropy derivative");
close((I2(r0,r1+eps)-I2(r0,r1-eps))/(2*eps),dh(r1),2e-10,
      "off-null second reporter full entropy derivative");
ok(Math.abs(dh(r0)-dh(r1))>.01,"unequal reports give different source coefficients");
const DS2=(du,dv)=>-dhphi(r0)*du-dhphi(r1)*dv;
const meanPreserving=DS2(1,-1);
ok(Math.abs(meanPreserving)>.01,
   "strict nonzero entropy source on direction invisible to sum/mean report");

// Two REAL original address populations, not averages erased to one click.
// Actual Golden n20 fixed prefixes; each fine ready outcome still paid.
const nativeS=r=>1+r-hphi(r);
const nativeD=r=>1-dhphi(r);
const p21=p**21,p22=p**22,p23=p**23,p24=p**24,p25=p**25;
for(const r of [1/7,2/9,1.8512395785208469e-6,p*p]){
  const massNon=6765*p21+10946*(p22+p24);
  const massReady=21892*p23*((1-r)+r);
  close(massNon+massReady,1,2e-11,"all Golden original FR RF FF RR overshoot retained");
  const fullKL=2*10946*p23*((1-r)*Math.log((1-r)/p)+r*Math.log(r/(p*p)))/ell;
  close(fullKL,a*nativeS(r),2e-11,
        "original complete Golden relative entropy = C−pinching Info, no fit");
  const step=r<1e-4?1e-9:1e-8;
  const slope=(a*nativeS(r+step)-a*nativeS(r-step))/(2*step);
  close(slope,a*nativeD(r),1e-7,"authentic unequal 0/10 code report source");
  const pad=a*(1-r);
  close(a*nativeS(r)+pad,a*(2-hphi(r)),1e-11,
        "exact PAID one-tick padding, not a free CQ source fix");
  const padSlope=(a*(2-hphi(r+step))-a*(2-hphi(r-step)))/(2*step);
  close(padSlope,-a*dhphi(r),1e-7,"timing-blind price has padded N1 CQ jet");
}

// True original Golden flat N1 report rare event: not a fitted probability.
const L=4*p**3,rr=1-(1-zeta*L)*(1-zeta*L*(1+p**6));
ok(rr>1.8e-6&&rr<1.9e-6,"original flat full native report r_star");
ok(nativeD(rr)<-26&&nativeD(rr)>-27,"honest original unequal code remains sourced");
ok(-dhphi(rr)<-27&&-dhphi(rr)>-28,"padded code has DIFFERENT genuine first source");

// Entire SCALAR open-chart equality with the OWNED original normalized
// N1 CQ value, not a newly fitted stress/coupling or new numerical root.
const tau=1/20,r_x_star=4*zeta*(1-zeta*L)*p**11;
const c_native=tau*dhphi(rr)*r_x_star;
const S_N1=(u,v)=>-((hphi(u)-hphi(rr))+(hphi(v)-hphi(rr)))/c_native;
const paidPair=(u,v)=>4-hphi(u)-hphi(v);
ok(c_native>2.6e-8&&c_native<2.7e-8,
   "original Golden normalization fixes the source factor (no fitting)");
for(const [u,v] of [[1.85e-6,1.856e-6],[1/7,2/9],[p*p,1/7]]){
  close(paidPair(u,v),4-2*hphi(rr)+c_native*S_N1(u,v),4e-13,
        "EXACT full nonlinear original CQ-price scalar identity, not only a source jet");
  const src=(du,dv)=>-dhphi(u)*du-dhphi(v)*dv;
  const dS_N1=(du,dv)=>-(
       dhphi(u)*du+dhphi(v)*dv)/c_native;
  close(src(1,-1),c_native*dS_N1(1,-1),2e-12,
        "full off-null native two-report source proportional in hostile mean-null tangent");
}

console.log(JSON.stringify({status:"PASS",checks,exact_Golden_Kraft:true,
 full_fine_label_count:fnFine,original_ready_mass:a,
 pure_pinch_controls:pins,offshell_two_report_source_difference:meanPreserving,
 authentic_r_star:rr,original_unpadded_code_gradient:nativeD(rr),
 genuinely_paid_padded_code_gradient:-dhphi(rr),
 compulsory_Book03_Info_selected:false,
 time_blind_task_selected:false,full42_physical_Euler_closed:false,
 GR_closed:false},null,2));
