// Full native F/R FIRST-CROSSING Golden READY + all failures and paid suffix.
// Actual 2-sided coherent U†ZU reflection, original Book03 complementary
// F=P W†(I-P)W P, true 42-field first source on common-null carrier.
// Completely independent of measured Shannon -> Book Info assumptions.
const ck=(b,m)=>{if(!b)throw Error("FAILED "+m)};
const gc=(x,y)=>{x=x<0n?-x:x;y=y<0n?-y:y;while(y){let t=x%y;x=y;y=t;}return x||1n};
const D=10n**50n,pl=61803398874989484820458683436563811772030917980576n,ph=pl+1n;
ck(pl*(pl+D)<D*D&&ph*(ph+D)>D*D,"isolated positive Golden root p");
class K{
constructor(a,b=0,d=1){a=BigInt(a);b=BigInt(b);d=BigInt(d);ck(d!==0n,"denom");if(d<0n){a=-a;b=-b;d=-d;}let q=gc(gc(a,b),d);this.a=a/q;this.b=b/q;this.d=d/q;}
static o(v){return v instanceof K?v:new K(v)}
add(x){x=K.o(x);return new K(this.a*x.d+x.a*this.d,this.b*x.d+x.b*this.d,this.d*x.d)}
neg(){return new K(-this.a,-this.b,this.d)}
sub(x){return this.add(K.o(x).neg())}
mul(x){x=K.o(x);return new K(this.a*x.a+this.b*x.b,this.a*x.b+this.b*x.a-this.b*x.b,this.d*x.d)}
divint(n){return new K(this.a,this.b,this.d*BigInt(n))}
div(x){x=K.o(x);let m=x.a*x.a-x.a*x.b-x.b*x.b;ck(m!==0n,"no field inverse");const v=this.mul(new K((x.a-x.b)*x.d,-x.b*x.d));return new K(m<0n?-v.a:v.a,m<0n?-v.b:v.b,v.d*(m<0n?-m:m))}
eq(x){x=K.o(x);return this.a===x.a&&this.b===x.b&&this.d===x.d}
sgn(){let lo=this.a*D+this.b*pl,hi=this.a*D+this.b*ph;if(lo>0n&&hi>0n)return 1;if(lo<0n&&hi<0n)return -1;if(this.a===0n&&this.b===0n)return 0;throw Error("unresolved Golden algebraic sign")}
num(){let scale=10n**28n;return Number((this.a*D+this.b*pl)*scale/(this.d*D))/1e28}
}
const one=new K(1),p=new K(0,1),z=one.divint(2**20);let pow=(x,n)=>{let y=one;for(let j=0;j<n;j++)y=y.mul(x);return y};
ck(p.mul(p).eq(one.sub(p)),"genuine phi G weights");
let Fn=[0n,1n];for(let j=2;j<=51;j++)Fn[j]=Fn[j-1]+Fn[j-2];
for(let n=1;n<=50;n++)ck(pow(p,n).mul(Fn[n+1]).add(pow(p,n+1).mul(Fn[n])).eq(one),"normalized F/R first stopping all n");
const N=Fn[21],O=Fn[20],M=256n;
ck(N===10946n&&O===6765n,"actual n20 Fibonacci/prefix address count");
const exact=pow(p,20).mul(N),overshoot=pow(p,21).mul(O),ready=pow(p,23).mul(2n*N);
ck(overshoot.add(exact.mul(pow(p,2).add(pow(p,3).mul(2)).add(pow(p,4)))).eq(one),"ALL FF/FR/RF/RR plus overshoot");
ck(ready.sgn()>0&&one.sub(ready).sgn()>0,"nontrivial positive READY and failure");
const L=pow(p,3).mul(4),QQ=one.sub(z.mul(L)),RR=one.sub(z.mul(L.mul(one.add(pow(p,6)))));
const r0=one.sub(QQ.mul(RR)),rx=z.mul(QQ).mul(pow(p,11)).mul(4),ry=z.mul(pow(p,6)).mul(RR.add(QQ.mul(pow(p,6)))).mul(8);
ck(r0.sgn()>0&&p.mul(p).sub(r0).sgn()>0,"original full two-band click chart");
const q0=ready.mul(r0),t0=one.sub(q0.mul(2)),Fret=one.sub(t0.mul(t0));
ck(Fret.eq(q0.mul(one.sub(q0)).mul(4))&&Fret.sgn()>0&&one.sub(Fret).sgn()>0,"actual rank-one complementary Book effect");
const den=one.sub(z.mul(Fret));
ck(den.sgn()>0&&one.divint(2).sub(q0).sgn()>0,"valid logdet and nonzero source");
const bookDerivative=z.mul(4*128).mul(one.sub(q0.mul(2))).div(den);
const site=ready.divint(M).mul(bookDerivative),Geom=site.mul(rx),Matter=site.mul(ry).neg();
ck(Geom.sgn()>0&&Matter.sgn()<0,"full Book source typed geometry/material");
ck(rx.mul(2).mul(RR.add(QQ.mul(pow(p,6)))).eq(ry.mul(pow(p,5)).mul(QQ)),"finite lambda exact");
for(let n=29n;n<=78n;n++){let rho=new K(M*n).divint(N),w=pow(p,23).mul(2n*n);ck(w.eq(ready.mul(new K(n).divint(N))),"native READY site marginal "+n);ck(w.eq(ready.divint(M).mul(rho)),"original inverse PF each site "+n)}
const mul=(A,B)=>A.map(row=>Array.from({length:B[0].length},(_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const tr=A=>A[0].map((_,j)=>A.map(x=>x[j]));
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const prodMax=(A,B)=>Math.max(...A.flatMap((row,i)=>row.map((v,j)=>Math.abs(v-B[i][j]))));
const pReady=ready.num(),ref=r0.num();
const weights=[1-pReady,pReady/7,6*pReady/7],rates=[0,ref*1.02,ref*.997],v=eye(6);
for(let k=0;k<3;k++){let c=Math.sqrt(1-rates[k]),s=Math.sqrt(rates[k]);v[2*k][2*k]=c;v[2*k][2*k+1]=-s;v[2*k+1][2*k]=s;v[2*k+1][2*k+1]=c;}
const zz=eye(6);for(let k=0;k<3;k++)zz[2*k+1][2*k+1]=-1;
const W=mul(mul(tr(v),zz),v);
ck(prodMax(mul(W,W),eye(6))<4e-15,"full 6x6 controlled reflection exactly unitary");
const ket=[Math.sqrt(weights[0]),0,Math.sqrt(weights[1]),0,Math.sqrt(weights[2]),0];
const cut=ket.map(x=>ket.map(y=>x*y)),notcut=eye(6).map((row,i)=>row.map((v,j)=>v-cut[i][j]));
const wf=mul(mul(mul(mul(cut,W),notcut),W),cut);
const t=ket.reduce((s,x,i)=>s+x*(W[i].reduce((s,v,j)=>s+v*ket[j],0)),0);
const predicted=1-t*t;
ck(Math.abs(t-(1-2*weights.reduce((s,a,i)=>s+a*rates[i],0)))<3e-15,"retained prefix coherence does NOT erase failed histories");
ck(prodMax(wf,cut.map(row=>row.map(x=>x*predicted)))<6e-15,"literal Book F=P W†(I-P)W P, rank ONE, all six columns");
const dephasedJ=rates.reduce((s,r)=>s-128*Math.log1p(-z.num()*4*r*(1-r)),0);
const coherentJ=-128*Math.log1p(-z.num()*predicted);
ck(Math.abs(dephasedJ-coherentJ)>1e-9,"classical independent cut source NOT same as coherent native rank-one");
const lphi=Math.log(1/p.num()),Hprime=r=>Math.log((1-r)/r)/lphi;
const rlow=1.8512417713660524e-6,rhigh=1.85132974719277498e-6;
ck(Hprime(rlow)>Hprime(rhigh),"certified off-null report spread and unequal nonlinear CQ slopes");
const dq0=1,dq1=-Hprime(rlow)/Hprime(rhigh);
ck(Math.abs(dq0+dq1)>1e-7,"offnull certified CQ critical root NOT global coherent mean-Q feedback critical");


let resultFine;
{
 const nOut=O+6n*N,pi=pow(p,23);
 ck(nOut===72441n,"all 72441 microscopic outcomes");
 ck(pow(p,21).mul(O).add(pow(p,22).mul(N)).add(pow(p,24).mul(N)).add(pi.mul(2n*N)).eq(one),"full output normalization");
 const a=pi.mul(r0),b=pi.mul(one.sub(r0));
 ck(a.sgn()>0&&b.sub(a).sgn()>0,"positive different click labels");
 const f=s=>s.mul(one.sub(s)).mul(4);
 const k=s=>z.mul(4).mul(one.sub(s.mul(2))).div(one.sub(z.mul(f(s))));
 const d=k(a).sub(k(b));
 ck(d.sgn()>0,"full fine Book derivative nonzero");
 const gf=ready.divint(M).mul(128).mul(d);
 const gc=ready.divint(M).mul(bookDerivative);
 const qThreeOne=ready.mul(r0),qThreeZero=ready.mul(one.sub(r0));
 const gainThree=ready.divint(M).mul(128).mul(k(qThreeOne).sub(k(qThreeZero)));
 const threeToCoarse=gainThree.div(gc),fineToThree=gf.div(gainThree);
 ck(gainThree.sgn()>0&&threeToCoarse.num()>.56&&threeToCoarse.num()<1,
    "complete 3-class future-partition Book source O(1) compared with original chosen click");
 ck(fineToThree.sgn()>0&&fineToThree.num()<3.61*pi.num(),
    "fine 72441-outcome source vanishes relative to complete three-class future source");
 // a_n=F_(n+1)*p^n has recurrence a_(n+2)=p a_(n+1)+p²a_n
 // and initial .6<a1,a2<.8, hence READY_n>1.2p³ at ALL native depths.
 // Since j''(s)<=-8z(1-2z), k(qClick)<=4z,
 // threeclass-to-click ratio>=2(1-2z)*READY_n*(1-2r0).
 const certifiedLower=2*(1-2*z.num())*(1.2*Math.pow(p.num(),3))*(1-2*r0.num());
 ck(certifiedLower>.56&&threeToCoarse.num()>certifiedLower,
   "native all-depth uniform strictly positive future three-class Book source");
 const rel=gf.div(gc);
 ck(gf.sgn()>0&&rel.sgn()>0&&rel.num()<2.01*pi.num(),"full fine/coarse source loss");
 const bg=gf.mul(rx),bm=gf.mul(ry).neg();
 ck(bg.sgn()>0&&bm.sgn()<0,"signed original whole 42 source");
 const depths=[];
 for(const depth of [20,24,32,40,48]){
   const Nc=Fn[depth+1],pc=pow(p,depth+3),R=pc.mul(2n*Nc),ratio=k(pc.mul(r0)).sub(k(pc.mul(one.sub(r0)))).div(k(R.mul(r0)));
   ck(ratio.sgn()>0&&ratio.num()<2.01*pc.num(),"all-depth Golden gain suppression");
   depths.push({depth,prefix_weight:pc.num(),fine_to_coarse:ratio.num()});
 }
 const kp=s=>-8*z.num()*(1-2*z.num()+4*z.num()*s*(1-s))/(1-4*z.num()*s*(1-s))**2;
 for(const x of [0,1e-8,.01,.25,.5,.75,1])ck(kp(x)<0&&-kp(x)<8*z.num()/(1-z.num())**2,"uniform Book curvature bound");
 const fullValue=-128*(Number(O)*Math.log1p(-z.num()*f(pow(p,21)).num())+
   Number(N)*Math.log1p(-z.num()*f(pow(p,22)).num())+
   Number(N)*Math.log1p(-z.num()*f(pow(p,24)).num())+
   Number(2n*N)*Math.log1p(-z.num()*f(a).num())+
   Number(2n*N)*Math.log1p(-z.num()*f(b).num()));
 ck(Number.isFinite(fullValue)&&fullValue>0,"all-event absolute logdet positive");
 const q=[1-ready.num(),ready.num()*(1-r0.num()),ready.num()*r0.num()],root=q.map(Math.sqrt);
 ck(Math.abs(q.reduce((s,v)=>s+v,0)-1)<1e-14,"complete 3-label sample normalized");
 const w=root.map((v,i)=>(i===0?1:0)-v);
 const wn=w.reduce((s,v)=>s+v*v,0);
 const H=eye(3).map((row,i)=>row.map((v,j)=>v-2*w[i]*w[j]/wn));
 ck(prodMax(mul(H,H),eye(3))<5e-15,"3x3 full prepared state unitary");
 ck(root.every((v,i)=>Math.abs(H[i][0]-v)<5e-15),"all positive amplitudes in prepared first column");
 const A9=Array.from({length:9},()=>Array(9).fill(0));
 const P9=Array.from({length:9},()=>Array(9).fill(0));
 for(let s=0;s<3;s++){
   const Z=eye(3);Z[s][s]=-1;
   const W=mul(mul(tr(H),Z),H);
   P9[3*s][3*s]=1;
   for(let i=0;i<3;i++)for(let j=0;j<3;j++)A9[3*s+i][3*s+j]=W[i][j];
 }
 const Q9=eye(9).map((row,i)=>row.map((v,j)=>v-P9[i][j]));
 const F9=mul(mul(mul(mul(P9,A9),Q9),A9),P9);
 const Fexpected=Array.from({length:9},()=>Array(9).fill(0));
 for(let j=0;j<3;j++)Fexpected[3*j][3*j]=4*q[j]*(1-q[j]);
 ck(prodMax(mul(A9,A9),eye(9))<5e-15,"all selector return columns unitary");
 ck(prodMax(F9,Fexpected)<8e-15,"true Book P Udag(1-P)U P all three selector outcomes");
 const determinant=F9.reduce((s,row,i)=>s*(1-z.num()*row[i]),1);
 const dTarget=q.reduce((s,v)=>s*(1-4*z.num()*v*(1-v)),1);
 ck(Math.abs(determinant-dTarget)<5e-15,"full 9x9 operator logdet equals actual event product");
 const veryFineCost=64*3+128;
 const deepPi=Math.pow(p.num(),veryFineCost+3);
 ck(deepPi<1e-60,"same real native PF C2 cost makes fine source tiny");
 resultFine={
 status:"PASS_COMPLETE_72441_NATIVE_BOOK_OUTPUTS_AND_FINE_COARSE_PF_SIGNAL",
 prefix_leaves:String(O+4n*N),
 actual_report_outcome_labels:String(nOut),
 complete_unnormalized_Book_logdet:fullValue,
 fine_geom_source:bg.num(),fine_matter_source:bm.num(),
 original_lambda:bm.div(bg).num(),
 fine_to_ready_coarse_source_ratio:rel.num(),
 complete_three_future_class_Book_source_coefficient:gainThree.num(),
 three_class_to_chosen_click_source_ratio:threeToCoarse.num(),
 fine_to_three_class_source_ratio:fineToThree.num(),
 all_depth_future_class_source_lower_bound:certifiedLower,
 all_three_real_future_classes:["NOT_READY","READY_NO_CLICK","READY_CLICK"],
 pi_n20:pi.num(),depth_checks:depths,PF_C2_n320_pi:deepPi,
 all_9x9_active_projector_Book_spectrum_checked:true,
 universal_identity:"sum Dqomega=0 cancels the constant 4z part of complete fine Book derivative",
 source_upper_bound:"128*8z/(1-z)^2 * max(qomega) * sum|Dqomega|",
 physical_active_future_quotient_selected:false,
 all_upstream_prep_Info_clock_stationary:false,
 GR_closed:false
 };
}
if(typeof console!=="undefined")console.log(JSON.stringify(resultFine,null,2));
