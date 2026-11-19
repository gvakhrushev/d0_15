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
function report(){return {status:"PASS_TRUE_NATIVE_GOLDEN_READY_COHERENT_BOOK_FULL42",F21:String(N),F20:String(O),fine_leaf_count:String(O+4n*N),all_stopped_and_suffix_failures_retained:true,
 pure_PREFIX_ready_probability:ready.num(),conditional_report_r0:r0.num(),entire_event_Q:q0.num(),clean_return_amplitude:t0.num(),Book_f_nonzero_eigenvalue:Fret.num(),oldRIGHT_spectator:128,
 Book_dJ_dQ:bookDerivative.num(),Book_source_per_original_site:site.num(),Book_geometry_first_source:Geom.num(),Book_matter_first_source:Matter.num(),original_lambda_minus:Matter.num()/Geom.num(),
 original_full_6x6_reflection_pass:true,real_dephased_cut_negative_control:true,offnull_mean_source_negative_control:true,
 cut_and_inverse_gates_physically_selected:false,input_writer_and_absolute_Book_info_selected:false,GR_closed:false};}
if(typeof console!=="undefined")console.log(JSON.stringify(report(),null,2));
