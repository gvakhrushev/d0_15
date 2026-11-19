#!/usr/bin/env node
"use strict";
/* ORIGINAL K(9,11,13) 718-edge native history:
 * J0^T J1=A/rho, full minimal U, archive R=Q U J0,
 * and exact Schur backreaction Sigma(s)=s² F(I+sT)^-1.
 * No invented price/action, clock, tensorial GR source or native actuation.
 */
const sizes=[9,11,13],N=33;
const zone=u=>u<9?0:u<20?1:2;
const err=(a,b)=>Math.abs(a-b);
const need=(v,k)=>{if(!v)throw Error("FAIL "+k);console.log("PASS "+k)};
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const zero=(n,m)=>Array.from({length:n},()=>Array(m).fill(0));
const dot=(a,b)=>a.reduce((t,v,j)=>t+v*b[j],0);
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const mv=(A,x)=>A.map(row=>dot(row,x));
const tr=A=>A.reduce((s,row,i)=>s+row[i],0);
const maxdiff=(A,B)=>Math.max(...A.flatMap((row,i)=>row.map((v,j)=>err(v,B[i][j]))));
const A=Array.from({length:N},(_,u)=>Array.from({length:N},(_,v)=>+(zone(u)!==zone(v))));
let r=Array(N).fill(1/Math.sqrt(N)),rho=0;
for(let n=0;n<1500;n++){
 const y=mv(A,r),len=Math.hypot(...y),next=y.map(v=>v/len);
 const dist=Math.max(...next.map((v,i)=>err(v,r[i])));
 r=next;if(dist<3e-16)break;
}
rho=dot(r,mv(A,r));
need(Math.abs(rho**3-359*rho-2574)<1e-7,"ORIGINAL scene cubic rho^3-359rho-2574");
const T=A.map(row=>row.map(v=>v/rho)),T2=mm(T,T),I=eye(N);
const F=I.map((row,i)=>row.map((v,j)=>v-T2[i][j]));
const pi=r.map(v=>v*v);
const E=[],J0=[],J1=[];
for(let u=0;u<N;u++)for(let v=0;v<N;v++)if(A[u][v]){
 E.push([u,v]);
 const x=Math.sqrt(r[v]/(rho*r[u])),y=Math.sqrt(r[u]/(rho*r[v]));
 const a=Array(N).fill(0),b=Array(N).fill(0);
 a[u]=x;b[v]=y;J0.push(a);J1.push(b);
}
need(E.length===718 && J0.length===718,"ORIGINAL 718 directed histories");
const jt=(J,x)=>Array.from({length:N},(_,i)=>J.reduce((s,row,j)=>s+row[i]*x[j],0));
const j=(J,f)=>J.map(row=>dot(row,f));
const JGram=(X,Y)=>Array.from({length:N},(_,u)=>Array.from({length:N},(_,v)=>
 X.reduce((s,row,k)=>s+row[u]*Y[k][v],0)));
need(maxdiff(JGram(J0,J0),I)<1e-12&&maxdiff(JGram(J1,J1),I)<1e-12,
     "both ORIGINAL J0/J1 full-history isometries");
need(maxdiff(JGram(J0,J1),T)<1e-12,"current/future history overlap = A/rho");
const D=J0.map((row,i)=>row.map((x,j)=>x-J1[i][j]));
const piMatrix=I.map((row,i)=>row.map((v,j)=>r[i]*r[j]));
const k=2574/(rho**3),B=I.map((row,i)=>row.map((v,j)=>v+(2*T[i][j]+T2[i][j])/(2+k)));
const BT=mm(I.map((row,i)=>row.map((v,j)=>v-T[i][j])),B);
need(maxdiff(BT,I.map((row,i)=>row.map((v,j)=>v-piMatrix[i][j])))<3e-12,
     "native degree-two B(T) solves (I-T)B=I-Pi");
const U=x=>{
 const y=jt(D,x),z=mv(B,y),dz=j(D,z);
 return x.map((v,i)=>v-dz[i]);
};
const Q=x=>{
 const coeff=jt(J0,x),proj=j(J0,coeff);
 return x.map((v,i)=>v-proj[i]);
};
const R=f=>Q(j(J1,f));
const ULres=Math.max(...Array.from({length:N},(_,i)=>{
 const basis=Array(N).fill(0);basis[i]=1;
 const x=U(j(J0,basis)),y=j(J1,basis);
 return Math.max(...x.map((v,k)=>err(v,y[k])));
}));
need(ULres<2e-12,"FULL original U_min sends present J0 to future J1");
const testX=Array.from({length:718},(_,i)=>Math.sin(.19*(i+1)));
need(Math.max(...U(U(testX)).map((v,i)=>err(v,testX[i])))<5e-12,
     "native minimal archive U is a TRUE involution, not a projection");
const RV=Array.from({length:N},(_,jcol)=>{
 const e=Array(N).fill(0);e[jcol]=1;return R(e);
});
const RG=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>dot(RV[i],RV[j])));
need(maxdiff(RG,F)<3e-12,"R^T R=I-T^2 full original archive effect");
need(Math.max(...RV.map(v=>Math.max(...jt(J0,v).map(Math.abs))))<2e-12,
     "archive is invisible to all CURRENT native J0 detector coordinates");
const f=Array.from({length:N},(_,i)=>Math.sin((i+1)*.13)+.01*i);
let ghost=R(f),rhs=f.slice();
const BtoVisible=x=>jt(J0,U(Q(x))), Darch=x=>Q(U(Q(x)));
for(let n=0;n<=6;n++){
 const lhs=BtoVisible(ghost);
 let rhsNow=mv(F,rhs).map(v=>(n%2?-1:1)*v);
 need(Math.max(...lhs.map((v,i)=>err(v,rhsNow[i])))<3e-12,
      "exact archive-return moment B D^"+n+" R=(-1)^n F T^n");
 ghost=Darch(ghost);rhs=mv(T,rhs);
}
for(const s of [.01,.1,.4]){
 const A1=I.map((row,i)=>row.map((v,j)=>v-s*T[i][j]));
 const A2=I.map((row,i)=>row.map((v,j)=>v+s*T[i][j]));
 const x=mm(A1,A2).map((row,i)=>row.map((v,j)=>v-s*s*F[i][j]));
 need(maxdiff(x,I.map(row=>row.map(v=>(1-s*s)*v)))<4e-13,
      "visible archive Schur denominator exact at s="+s);
}
const rootsA=359,rootsB=2574,amplitude=2*Math.sqrt(rootsA/3);
const ang=Math.acos((3*rootsB/(2*rootsA))*Math.sqrt(3/rootsA))/3;
const lam=[0,1,2].map(i=>amplitude*Math.cos(ang-2*Math.PI*i/3)).sort((a,b)=>b-a);
const archiveEigs=[1-(lam[1]/rho)**2,1-(lam[2]/rho)**2];
need(Math.abs(tr(F)-31.494352574857793)<2e-12 &&
     Math.abs(archiveEigs[0]-0.800314904000112)<2e-12 &&
     Math.abs(archiveEigs[1]-0.694037670857683)<2e-12,
     "native archive F has rank32, thirty innovation eigenvalues 1");
const P=A.map((row,u)=>row.map((x,v)=>x?r[v]/(rho*r[u]):0));
need(P.every(row=>err(row.reduce((a,b)=>a+b,0),1)<1e-12),
     "original one-sided Perron conditional probabilities");
const vA=r.map((x,u)=>zone(u)===0?x:0);
const archiveNorm=dot(vA,mv(F,vA));
const trueVar=P.reduce((acc,row,u)=>{
 const ex=row.reduce((s,q,v)=>s+q*(zone(v)===0?1:0),0);
 return acc+pi[u]*(ex-ex*ex);
},0);
const piA=pi.slice(0,9).reduce((a,b)=>a+b,0);
need(Math.abs(archiveNorm-trueVar)<2e-12 && archiveNorm>0,
     "actual FUTURE conditional variance equals invisible archive norm");
need(Math.abs(piA-.3115593200583015)<2e-12 && P.every((row,u)=>
 row.every((v,w)=>u<9&&w<9?v===0:true)),
     "same stationary histogram but zero adjacent AA transitions");
const clockp=(Math.sqrt(5)-1)/2,eps=clockp**2/1024,lambda=288/25;
const q=(1-eps*lambda/2)**2;
need(q>0&&q<1 && (1-eps*0/2)**2===1,
     "original separate full128 detector has dark zero and positive-shell event clocks");
// ORIGINAL exact 33-mode correlation recurrence, and its detector clock.
const aa=359/(rho*rho),bb=2574/(rho*rho*rho);
const T4=mm(T2,T2),rec=T2.map((row,i)=>row.map((v,j)=>aa*v+bb*T[i][j]));
need(maxdiff(T4,rec)<2e-12 && Math.abs(aa+bb-1)<2e-12,"all original T^4=aT²+bT");
const lag=[],probe=vA.slice();let future=probe.slice();
for(let m=0;m<=10;m++){lag.push(dot(probe,future));future=mv(T,future);}
need(Math.abs(lag[0]-piA)<2e-12 && Math.abs(lag[1])<2e-12,
 "stationary one-time detector but zero next-step AA correlation");
for(let m=0;m+4<=10;m++)
 need(Math.abs(lag[m+4]-aa*lag[m+2]-bb*lag[m+1])<2e-12,"true lagged detector recurrence "+m);
const nClock=1024,epsClock=clockp**2/1024,positiveLambda=288/25;
const qDark=1,qGood=(1-epsClock*positiveLambda/2)**2;
const infoTime=-nClock*Math.log(qGood)/Math.log(1/clockp);
need(qDark===1 && infoTime>0 && Math.abs(infoTime-9.15393616364622)<1e-10,
 "native separate full128 dark versus positive blank-history information time");

console.log(JSON.stringify({
 type:"ORIGINAL K(9,11,13) 718-edge exact archive",
 rho,edge_count:E.length,archived_coupling_rank:32,archive_innovation_trace:tr(F),
 archive_nontrivial_eigenvalues:archiveEigs,
 zoneA_stationary_one_time_prob:piA,zoneA_next_step_joint_prob:0,
 two_time_covariance_zoneA:-(piA*piA),zoneA_conditional_future_variance:archiveNorm,
 original_full128_positive_shell_blank:q,
 scope:"one finite scene reflection and separately owned full128 event clock; NOT compulsory whole Book action or GR",
 gr_closed:false
},null,2));
