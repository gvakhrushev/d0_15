"use strict";
// D0 #334: self-contained positive cyclic Book source and noncommuting first-jet checker.
const p=(Math.sqrt(5)-1)/2,z=2**-20;
function eye(n){return Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)))}

function mm(A,B){return A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)))}

function trans(A){return A[0].map((_,i)=>A.map(row=>row[i]))}

function add(A,B,scale=1){return A.map((row,i)=>row.map((x,j)=>x+scale*B[i][j]))}

function times(A,s){return A.map(row=>row.map(x=>x*s))}

function trace(A){return A.reduce((s,row,i)=>s+row[i],0)}

function near(x,y,e=1e-12){return Math.abs(x-y)<=e*Math.max(1,Math.abs(x),Math.abs(y))}

function rotation(i,j,t){const R=eye(4),c=Math.cos(t),s=Math.sin(t);R[i][i]=R[j][j]=c;R[i][j]=-s;R[j][i]=s;return R}

function generator(i,j){const A=times(eye(4),0);A[i][j]=-1;A[j][i]=1;return A}

function state(t){
 const W0=[[Math.cos(.35),0],[0,Math.cos(.74)],[Math.sin(.35),0],[0,Math.sin(.74)]];
 const Pi=eye(4).map((r,i)=>r.map(x=>i<2?x:0));
 const U1=rotation(0,3,.45*t),U2=rotation(0,2,.6*t),W=mm(mm(U1,U2),W0);
 const dW=add(mm(times(mm(generator(0,3),U1),.45),mm(U2,W0)),
              mm(U1,mm(times(mm(generator(0,2),U2),.6),W0)));
 const E=mm(trans(W),mm(Pi,W));
 const dE=add(mm(trans(dW),mm(Pi,W)),mm(trans(W),mm(Pi,dW)));
 const tau=times(mm(W,trans(W)),.5),eta=mm(Pi,mm(tau,Pi));
 return {W,E,dE,tau,eta};
}

function power(A,k){let v=eye(A.length);for(let i=0;i<k;i++)v=mm(v,A);return v}

function cyclicTrace(A,k){
 const n=A.length,idx=new Array(k);
 function recur(j){if(j===k){let v=1;for(let t=0;t<k;t++)v*=A[idx[t]][idx[(t+1)%k]];return v;}
 let s=0;for(let h=0;h<n;h++){idx[j]=h;s+=recur(j+1)}return s;}
 return recur(0);
}

function det2(A){return A[0][0]*A[1][1]-A[0][1]*A[1][0]}

function response(S){
 const {E,dE}=S;
 const F=times(add(E,power(E,2),-p),4*p);
 const dF=times(add(dE,add(mm(dE,E),mm(E,dE)),-p),4*p);
 const M=add(eye(2),F,-z);
 const inv=times([[M[1][1],-M[0][1]],[-M[1][0],M[0][0]]],1/det2(M));
 const J=-Math.log1p(-z*trace(F)+z*z*det2(F)),D=z*trace(mm(inv,dF));
 const m=Array.from({length:4},(_,i)=>trace(power(E,i+1)));
 const dm=Array.from({length:4},(_,i)=>(i+1)*trace(mm(power(E,i),dE)));
 const J2=4*p*z*(m[0]-p*m[1])+8*p*p*z*z*(m[1]-2*p*m[2]+p*p*m[3]);
 const D2=4*p*z*(dm[0]-p*dm[1])+8*p*p*z*z*(dm[1]-2*p*dm[2]+p*p*dm[3]);
 const avg=(dE[0][0]+dE[1][1])/2,disc=Math.hypot((dE[0][0]-dE[1][1])/2,dE[0][1]);
 const norm=Math.max(Math.abs(avg+disc),Math.abs(avg-disc));
 return {J,D,J2,D2,JE:J-J2,DE:D-D2,JV:2*z**3/(3*(1-z)),DV:2*z**3/(1-z)*4*p*(1+p)*norm,
   commutator:(E[0][0]-E[1][1])*dE[0][1]+E[0][1]*(dE[1][1]-dE[0][0])};
}

function check(x,m){if(!x)throw Error("SCOPED CHECK FAILED: "+m)}

function run(){
 let count=0;const ok=(c,m)=>{check(c,m);count++};let summaries=[];
 ok(near(p+p*p,1,1e-14),"Golden p+p²=1");
 for(let t of [0,.31]){
  const S=state(t),R=response(S);
  ok(near(trace(mm(trans(S.W),S.W)),2,1e-13),"whole isometry");
  for(let k=1;k<=6;k++){
   const mk=trace(power(S.E,k)),tk=trace(power(S.eta,k));
   ok(near(tk,mk/2**k,1e-13),"effect and positive state k="+k);
   ok(near(cyclicTrace(S.eta,k),tk,1e-13),"independent permutation k="+k);
   if(k<=4){
    const q=trace(S.eta),pp=(q**k+tk)/2,pm=(q**k-tk)/2,pf=1-q**k;
    ok(pp>=-1e-13&&pm>=-1e-13&&pf>=-1e-13,"positive complete record k="+k);
    ok(near(pp+pm+pf,1,1e-13),"failure retained k="+k);
    ok(near(pp-pm,mk/2**k,1e-13),"unconditional signed moment k="+k);
   }
  }
  ok(Math.abs(R.commutator)>.09,"noncommuting E and DE");
  ok(R.JE>=-1e-21&&R.JE<R.JV+1e-21,"uniform second-order Book tail");
  ok(Math.abs(R.DE)<R.DV+1e-20,"uniform first-source Book tail");
  const h=1e-5;
  const dnum=(response(state(t+h)).J-response(state(t-h)).J)/(2*h);
  ok(Math.abs(dnum-R.D)<1e-12,"Book source from independent finite difference");
  summaries.push({t, commutator_01:R.commutator, full_Book_value:R.J,
    four_test_reconstruction:R.J2, Book_first_source:R.D, four_test_source:R.D2,
    value_error:R.JE, source_error:R.DE, value_bound:R.JV, source_bound:R.DV});
 }
 const d=16384,large={rank_d_times_rR:d, zeta:z,
   second_order_value_tail:d*z**3/(3*(1-z)),
   second_order_first_source_tail_per_normDE:d*z**3/(1-z)*4*p*(1+p)};
 ok(large.second_order_value_tail<4.7371e-15,"whole full128 numerical value bound");
 ok(large.second_order_first_source_tail_per_normDE<5.685e-14,"whole full128 source bound");
 return {status:"SCOPED_PASS",checks:count,fixtures:summaries,full128:large,
  true_Book03_active_cut_selected:false, native_paid_W_writer_admitted:false,GR_closed:false};
}

console.log(JSON.stringify(run(),null,2));
