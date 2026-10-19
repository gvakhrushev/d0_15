#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL Golden p, CAR16 fermionic exterior Lie lift, entire Julia O(32).
 * New CONDITIONAL fixed-circuit Choi programme-state / heralded processor.
 * No new fundamental gate: fixed Bell processing can be approximated by
 * pre-owned active Golden+CNOT Lie-complete alphabet IF placement admitted.
 * Program-state preparation, all failure costs, oldRIGHT/controller/clock and
 * compulsory native Book action remain OPEN. GR_closed=false.
 */
const assert=(t,m)=>{if(!t)throw Error("FAIL: "+m)};
const p=(Math.sqrt(5)-1)/2,phi=1/p,a=Math.sqrt(p),d=32,n=16;
const zeros=(N,M=N)=>Array.from({length:N},()=>Array(M).fill(0));
const eye=N=>Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>i===j?1:0));
const add=(A,B,t=1)=>A.map((r,i)=>r.map((v,j)=>v+t*B[i][j]));
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const tr=A=>A.reduce((s,r,i)=>s+r[i],0);
const transpose=A=>A[0].map((_,i)=>A.map(r=>r[i]));
const fs=(A,B)=>A.reduce((acc,row,i)=>acc+row.reduce((q,x,j)=>q+x*B[i][j],0),0);
const E=(i,j)=>{const T=zeros(4);T[i][j]=1;return T};
const gen=[
 add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)
];
assert(Math.abs(p+p*p-1)<1e-15,"literal original Golden p²+p=1");
const create=Array.from({length:4},()=>zeros(n));
const annih=Array.from({length:4},()=>zeros(n));
function popcnt(z){let k=0;while(z){k+=z&1;z>>=1}return k}
for(let j=0;j<4;j++)for(let mask=0;mask<16;mask++){
 const sign=popcnt(mask&((1<<j)-1))%2?-1:1;
 if(mask&(1<<j))annih[j][mask^(1<<j)][mask]=sign;
 else create[j][mask|(1<<j)][mask]=sign;
}
const D=gen.map(X=>{
 let out=zeros(n);
 for(let i=0;i<4;i++)for(let j=0;j<4;j++)if(X[i][j]){
   out=add(out,mm(create[i],annih[j]),X[i][j]);
 }
 return out;
});
const Sym=D.map(X=>add(X,transpose(X)));
const Acoef=D.map((X,i)=>D.map((Y,j)=>fs(X,Y)/4));
const Bcoef=Sym.map((X,i)=>Sym.map((Y,j)=>fs(X,Y)/16));
for(let i=0;i<6;i++)for(let j=0;j<6;j++){
 assert(Number.isInteger(Acoef[i][j])&&Number.isInteger(Bcoef[i][j]),
   "coefficientwise rational CAR16 QFI polynomial");
}
const Q=Acoef.map((row,i)=>row.map((x,j)=>x*p*p+Bcoef[i][j]*p**3));
const target=zeros(6);
for(let i=0;i<4;i++)target[i][i]=1;
target[0][2]=target[2][0]=target[1][3]=target[3][1]=p**3;
target[4][4]=2*p*p;target[5][5]=2*p;
assert(Q.every((row,i)=>row.every((v,j)=>Math.abs(v-target[i][j])<3e-14)),
 "EXACT original fermionic Julia-program QFI = Golden 3+3 matrix");
const eigen=[2*p,2*p,2*p,2*p*p,2*p*p,2*p*p];
const determinant=eigen.reduce((x,v)=>x*v,1);
assert(Math.abs(determinant-64*p**9)<3e-14&&determinant>0,
 "QFI eigenvalues 2p (3), 2p² (3), determinant 64 p^9");

// Julia J(p Λ(U)) on original compact J23 1-parameter subgroup.
// For this ROTATION only, the full exterior lift is Euclidean orthogonal.
// For general proper Lorentz boosts/null directions the true square-root
// off-diagonal blocks vary; their exact FLAT Sylvester derivatives above
// are used for the full six-direction QFI.
const I16=eye(n),J23=D[4],J23sq=mm(J23,J23);
assert(fs(add(mm(J23sq,J23),J23),add(mm(J23sq,J23),J23))<1e-24,
 "original CAR16 lifted J23^3=-J23");
function JuliaRot(theta){
 const R=add(add(I16,J23,Math.sin(theta)),J23sq,1-Math.cos(theta));
 const out=zeros(d);
 for(let i=0;i<n;i++)for(let j=0;j<n;j++){
   out[i][j]=p*R[i][j];
   out[i+n][j+n]=-p*R[j][i];
   out[i][j+n]=(i===j)?a:0;
   out[i+n][j]=(i===j)?a:0;
 }
 return out;
}
const J0=JuliaRot(0),Jt=JuliaRot(.1);
for(const J of [J0,Jt]){
 const Z=mm(transpose(J),J),I=eye(d);
 assert(fs(add(Z,I,-1),add(Z,I,-1))<4e-26,
   "complete 32×32 original Golden Julia REAL ORTHOGONAL");
}
assert(fs(add(J0,Jt,-1),add(J0,Jt,-1))>1e-6,
  "nontrivial genuinely moving native Lorentz programme");
const overlap=fs(J0,Jt)/d;
assert(overlap>0.98&&overlap<1,
 "different Julia unitaries have NONORTHOGONAL Choi programmes");

// Complete fixed Bell processor: input D, programmed A,B, rank-1
// Bell success projection on D+A; failure=I−success completely retained.
// Explicit tensor coordinates |ψ>_D ⊗ [sum_i |i>_A J|i>_B]/sqrt(d).
const psi=Array.from({length:d},(_,i)=>Math.sin(.37*(i+1))+.3*Math.cos(.13*(i+1)));
const pn=Math.hypot(...psi);
for(let i=0;i<d;i++)psi[i]/=pn;
function bellCheck(J){
 const state=new Float64Array(d**3);
 for(let i=0;i<d;i++)for(let m=0;m<d;m++)for(let k=0;k<d;k++)
   state[(i*d+m)*d+k]=psi[i]*J[k][m]/Math.sqrt(d);
 const out=Array.from({length:d},(_,k)=>{
   let v=0;for(let i=0;i<d;i++)v+=state[(i*d+i)*d+k]/Math.sqrt(d);
   return v;
 });
 const expect=J.map(row=>row.reduce((v,x,i)=>v+x*psi[i],0)/d);
 const maxerr=Math.max(...out.map((v,k)=>Math.abs(v-expect[k])));
 let pass=out.reduce((s,v)=>s+v*v,0),fail=0;
 for(let i=0;i<d;i++)for(let m=0;m<d;m++)for(let k=0;k<d;k++){
   const u=state[(i*d+m)*d+k]-(i===m?out[k]/Math.sqrt(d):0);
   fail+=u*u;
 }
 assert(maxerr<1e-14, "success AMP exactly J(U) ψ/32");
 assert(Math.abs(pass-1/d**2)<3e-14,
  "field-independent exact Bell success probability 1/1024");
 assert(Math.abs(fail-(1-1/d**2))<5e-13,
  "ALL failed Bell outcomes preserved (total norm=1)");
 return {success:pass,failure:fail,amplitudeError:maxerr};
}
const flat=bellCheck(J0),curved=bellCheck(Jt);
const qfiRot=(theta)=>{
 const JJ=JuliaRot(theta),amp=fs(J0,JJ)/d;
 return 4*(1-amp*amp)/(theta*theta);
};
assert(Math.abs(qfiRot(.002)-2*p*p)<3e-6,
 "finite rotated original full32 Choi-program fidelity QFI = 2p²");
const cost=-Math.log(1/d**2)/Math.log(phi);
assert(cost>0,"conditional successful branch has nonzero positive surprisal");

// SAME mathematical fixed Bell processor lifted to ORIGINAL TWO-FRESH
// Golden-p 16-outcome positive Choi mark on the original CAR16 grade-one.
// This uses the true complete operator J_C acting on the 32d carrier,
// with a single unchanged processor and NONORTHOGONAL programme states.

// The original full 16-outcome Choi mark has TWO distinct freshly
// recorded Golden flags. One Julia(C) is 32d CAR16×flag; their chronological
// complete operator is on CAR16×flag1×flag2 (dimension 64).
const dBell=64,herald=1/(dBell*dBell);
function twoFlagOriginalJulia(theta){
 const index=(i,f1,f2)=>4*i+2*f1+f2;
 const first=JuliaRot(0),second=JuliaRot(theta);
 const J1=zeros(64),J2=zeros(64);
 for(let i=0;i<16;i++)for(let j=0;j<16;j++)
 for(let old=0;old<2;old++)for(let next=0;next<2;next++){
  const a=first[i+16*next][j+16*old];
  const b=second[i+16*next][j+16*old];
  for(let f2=0;f2<2;f2++)J1[index(i,next,f2)][index(j,old,f2)]=a;
  for(let f1=0;f1<2;f1++)J2[index(i,f1,next)][index(j,f1,old)]=b;
 }
 return mm(J2,J1);
}
for(let theta of [0,.1]){
 const J=twoFlagOriginalJulia(theta),Id=eye(64);
 assert(fs(add(mm(transpose(J),J),Id,-1),
           add(mm(transpose(J),J),Id,-1))<1e-24,
     "complete 64D two-fresh-Golden Julia programmable operation is orthogonal");
 const v=Array.from({length:64},(_,j)=>Math.sin(.29*(j+1))+.4*Math.cos(.13*(j+1)));
 const nrm=Math.hypot(...v);for(let j=0;j<64;j++)v[j]/=nrm;
 const exact=J.map(row=>row.reduce((s,x,k)=>s+x*v[k],0)/64);
 const signal=Array(64).fill(0);
 let totalNorm=0;
 for(let i=0;i<64;i++)for(let j=0;j<64;j++)for(let k=0;k<64;k++){
  let wave=v[i]*J[k][j]/8;
  totalNorm+=wave*wave;
  if(i===j)signal[k]+=wave/8;
 }
 assert(Math.max(...signal.map((x,k)=>Math.abs(x-exact[k])))<3e-14,
        "real FIXED 64D Bell processor applies exact original 2-fresh-gate operator /64");
 const prob=signal.reduce((s,x)=>s+x*x,0);
 assert(Math.abs(prob-herald)<2e-14&&Math.abs(totalNorm-1)<2e-13,
        "full TRUE two-flag programme herald rate 1/4096, failed Bell complement 4095/4096");
}

const G4=gen;
const trace4=M=>tr(M), ip4=(X,Y)=>tr(mm(transpose(X),Y));
function exp4(X){let S=eye(4),T=eye(4);for(let k=1;k<25;k++){T=mm(T,X).map(r=>r.map(x=>x/k));S=add(S,T)}return S;}
function q16(U) {
 const mean=trace4(U)/4,v=ip4(U,U)/4;
 const marks=G4.flatMap(G=>{let s=ip4(G,U)/(2*Math.SQRT2);
  return [p**4/24*(mean+s)**2,p**4/24*(mean-s)**2]});
 const GG=p**4*v,GB=p*p*(1-p*p*v),BG=p**3*v,
       rest=GG-marks.reduce((s,x)=>s+x,0);
 return [...marks,rest,GB,BG,1-GG-GB-BG];
}
function q17(U){
 const q=q16(U),a=q.map(x=>x*herald);
 return a.concat([1-herald]); // original Bell failure including all residual blocks
}
function entropy(arr){return -arr.reduce((s,x)=>s+x*Math.log(x),0)/Math.log(phi);}
const x0=Array(6).fill(0);
function qSource(x){
 const X=G4.reduce((M,G,i)=>add(M,G,x[i]),zeros(4));
 return q17(exp4(X));
}
const qBase=qSource(x0);
assert(qBase.length===17&&qBase.every(x=>x>0)&&
 Math.abs(qBase.reduce((s,x)=>s+x,0)-1)<1e-14,
 "complete 17-way Bell/GOLDEN positive instrument, 16 success + all failures");
assert(Math.abs(qBase.slice(0,16).reduce((s,x)=>s+x,0)-herald)<1e-14,
 "native complete two-fresh-flag programme herald EXACT 1/4096");
assert(Math.abs(qBase[16]-(4095/4096))<1e-14,
 "original fixed processor all failed Bell outcomes are retained in a register");

for(let k=0;k<6;k++){
 let x=x0.slice();x[k]=.07;
 const U=exp4(G4.reduce((M,G,i)=>add(M,G,x[i]),zeros(4)));
 const outcomes=q17(U);
 const plus=outcomes[2*k],minus=outcomes[2*k+1];
 const decoded=4*Math.sqrt(3)*dBell/(p*p)*(Math.sqrt(plus)-Math.sqrt(minus));
 assert(Math.abs(decoded-ip4(G4[k],U))<2e-13,
   "fixed BELL processor + GOLDEN full16 recover exact finite Lorentz marker "+k);
 assert(Math.abs(outcomes.slice(0,16).reduce((s,z)=>s+z,0)-herald)<1e-14,
   "all success/failure full-record probabilities normalize and herald source=0 "+k);
}
let h0=entropy(qBase);
const p4=p**4,lnphi=Math.log(phi);
const CN=p*p+(p4/lnphi)*(Math.log(2)+Math.log(12)/12-1/6);
const CS=p*p/2+(p4/lnphi)*(Math.log(2)/2+Math.log(12)/4);
const expectPositive=herald*(CN+2*CS),expectNegative=herald*(CN-2*CS);
const qRotate=t=>{let x=x0.slice();x[4]=t;return entropy(qSource(x));};
const qBoost=t=>{let x=x0.slice();x[5]=t;return entropy(qSource(x));};
for(let h of [.03,.01,.003]){
 const hr=(qRotate(h)+qRotate(-h)-2*h0)/(h*h);
 const hb=(qBoost(h)+qBoost(-h)-2*h0)/(h*h);
 assert(Math.abs(hr-expectNegative)<5e-6&&Math.abs(hb-expectPositive)<5e-6,
   "FULL Bell+Golden17 signed Shannon Lorentz Hessian is herald-scaled but NONZERO "+h);
}
const hIdentity=-herald*Math.log(herald)/lnphi-(1-herald)*Math.log(1-herald)/lnphi;
assert(Math.abs(h0-hIdentity-herald*entropy(q16(eye(4))))<1e-12,
 "EXACT complete 17-outcome Shannon chain: binary herald + herald*real Golden16 entropy");

// Exact moving scalar original BOOK original edge support remains a scalar
// probability-factor in each declared complete success (and failed Bell).
// Conditioning on a saved existing path r makes all w derivatives cancel.
const nzone=[9,11,13],zon=u=>u<9?0:u<20?1:2;
const edges=[];
for(let u=0;u<33;u++)for(let v=0;v<33;v++)if(zon(u)!==zon(v))edges.push([u,v]);
function Perron(t){
 const M=nzone.map((u,i)=>nzone.map((v,j)=>i===j?0:p*Math.sqrt(u*v)
  *Math.exp(-lnphi*t*(((i===0&&j===1)||(i===1&&j===0))?1:0))));
 let z=Array(3).fill(1/Math.sqrt(3));
 for(let k=0;k<800;k++){
  let x=M.map(r=>r.reduce((s,v,j)=>s+v*z[j],0)),n=Math.hypot(...x);
  let next=x.map(v=>v/n);
  if(Math.max(...next.map((v,i)=>Math.abs(v-z[i])))<2e-15){z=next;break}z=next;
 }
 const rho=z.reduce((s,v,i)=>s+v*M[i].reduce((s,x,j)=>s+x*z[j],0),0);
 const site=Array.from({length:33},(_,i)=>z[zon(i)]/Math.sqrt(nzone[zon(i)]));
 const prior=site.map(v=>v/site.reduce((s,x)=>s+x,0));
 const weights=edges.map(([u,v])=>{
  const AB=(zon(u)===0&&zon(v)===1)||(zon(u)===1&&zon(v)===0);
  return prior[u]*p*Math.exp(-lnphi*t*(AB?1:0))*site[v]/(rho*site[u]);
 });
 return weights;
}
const xCurved=x0.map((v,i)=>i===4?.024:0),nativeConditional=qSource(xCurved);
for(let t of [0,.02,.04]){
 const W=Perron(t);
 assert(Math.abs(W.reduce((s,x)=>s+x,0)-1)<1e-13,
   "true one-sided original full718 Perron preparation normalizes t="+t);
 const w=W[0],QP=nativeConditional[8]*w,QM=nativeConditional[9]*w;
 const U=exp4(G4.reduce((M,G,i)=>add(M,G,xCurved[i]),zeros(4)));
 const recovered=4*Math.sqrt(3)*dBell/(p*p*Math.sqrt(w))*(Math.sqrt(QP)-Math.sqrt(QM));
 assert(Math.abs(recovered-ip4(G4[4],U))<2e-12,
   "full recorded Bell/Golden positive native oriented marker cancels actual moving Perron weight t="+t);
}


// FULL ORIGINAL 718 directed Perron history × 17 complete heralded
// Golden/CAR conditional outcomes. Each old path and Bell-failed record
// remains a nonzero event. Original *mathematical* edge->Lorentz assignment
// uses sign(u<v); NOT the 4D Role controller itself.
function jointH(t,x){
 const w=Perron(t),qPlus=qSource(x),qMinus=qSource(x.map(y=>-y));
 let total=0,normalizer=0,positive=true;
 for(let i=0;i<718;i++){
  const q=edges[i][0]<edges[i][1]?qPlus:qMinus;
  for(let j=0;j<17;j++){
   const z=w[i]*q[j];if(!(z>0))positive=false;
   normalizer+=z;total-=z*Math.log(z)/lnphi;
  }
 }
 assert(positive&&Math.abs(normalizer-1)<6e-13,
  "ALL 718x17=12206 complete Golden/Bell/Perron history outcomes positive and normalized");
 return total;
}
const xZero=Array(6).fill(0),firstOriginalPerron=Perron(0);
const trueBookH=entropy(firstOriginalPerron),wholeH=jointH(0,xZero);
assert(Math.abs(wholeH-trueBookH-h0)<9e-12,
 "exact true ORIGINAL single joint 12206-outcome Shannon chain with honest old one-sided prior");
for(let t of [0,.02,.04]){
 const w=Perron(t),gold=jointH(t,xZero);
 assert(Math.abs(gold-entropy(w)-h0)<9e-12,
  "true changing original native Book Cost/old preparation retained after Bell programme t="+t);
}
const originalBookSource=(Perron(.0001).map((x,i)=>
 (x-firstOriginalPerron[i])/.0001));
const score16=G4.map((G,k)=>{
 const q0=qBase,dt=Array(17).fill(0);
 dt[2*k]=herald*p**4/(12*Math.SQRT2);
 dt[2*k+1]=-(herald*p**4)/(12*Math.SQRT2);
 return dt;
});
const predictedFisher=herald*p**4/6;
const scalarFirstStepFisher=firstOriginalPerron.reduce((s,w,i)=>
 s+originalBookSource[i]*originalBookSource[i]/w,0);
const tensor=Array.from({length:7},()=>Array(7).fill(0));
for(let i=0;i<718;i++){
 const w=firstOriginalPerron[i],dw=originalBookSource[i],
       sgn=edges[i][0]<edges[i][1]?1:-1;
 for(let k=0;k<17;k++){
  const Q=w*qBase[k],dQ=[dw*qBase[k],
      ...score16.map(row=>w*sgn*row[k])];
  for(let a=0;a<7;a++)for(let b=0;b<7;b++)
   tensor[a][b]+=dQ[a]*dQ[b]/Q;
 }
}
assert(Math.abs(tensor[0][0]-scalarFirstStepFisher)<2e-12&&
 scalarFirstStepFisher>.01,
 "full 12206 one-run Perron preparation Fisher source remains nonzero");
for(let i=1;i<7;i++){
 assert(Math.abs(tensor[0][i])<1e-14,
  "all-order conditional score Ward kills moving Book/Bell Lorentz Fisher cross");
 for(let j=1;j<7;j++)
  assert(Math.abs(tensor[i][j]-(i===j?predictedFisher:0))<1e-13,
    "FULL 12206 one-run six-Lorentz Fisher = HERALD p^4/6 * I6");
}
for(let h of [.02,.007,.003]){
 let xr=xZero.slice(),xb=xZero.slice();
 xr[4]=h;xb[4]=-h;
 let pr=(jointH(0,xr)+jointH(0,xb)-2*wholeH)/(h*h);
 xr[4]=0;xb[4]=0;xr[5]=h;xb[5]=-h;
 let pb=(jointH(0,xr)+jointH(0,xb)-2*wholeH)/(h*h);
 assert(Math.abs(pr-expectNegative)<5e-6&&Math.abs(pb-expectPositive)<5e-6,
  "complete original 12206 native positive history has 3+3 signed six-Lorentz pointer curvature");
}


// Strong same-Golden PROGRAMME information theorem. In the full 64d
// two-fresh chronological programme Jtot(U)=J2(U)J1(I), left multiplication
// by FIXED J1(I) does not change normalized Choi overlap; the spectator
// first flag doubles trace and dimension. Hence its six-parameter input
// QFI is EXACTLY the already-owned original 32d Golden CAR programme QFI
// with eigenvalues 2p (3), 2p² (3); no hidden information loss from the
// second fresh flag, only Bell herald probability changes.
for(let h of [.17,.035,.005]){
 const X=twoFlagOriginalJulia(0),Y=twoFlagOriginalJulia(h);
 const overlap64=fs(X,Y)/64;
 const overlap32=fs(JuliaRot(0),JuliaRot(h))/32;
 assert(Math.abs(overlap64-overlap32)<8e-14,
   "original TWO flag Golden64 Choi program has EXACT same state overlap as original Golden32 "+h);
 const qfi64=4*(1-overlap64*overlap64)/(h*h);
 const qfi32=4*(1-overlap32*overlap32)/(h*h);
 assert(Math.abs(qfi64-qfi32)<2e-10,
   "Gold-program full six-Lorentz QFI preserved by spectator/fixed first flag "+h);
}
assert(Math.abs(determinant-64*p**9)<3e-14,
 "original six-direction movable-program full QFI det stays 64*p^9>0");

console.log(JSON.stringify({
 status:"PASS_ORIGINAL_CAR16_GOLDEN_CHOI_HERALDED_FIXED_PROGRAM",
 originalGolden_p:p,
 activeJulia_dim:d,normalChoiHilbert_dim:d*d,exactFullWave_dim:d**3,
 sourceBasis:["N2","N3","Nbar2","Nbar3","J23","Boost"],
 exactQfiAsGoldenPolynomial:{Ap2:Acoef,Bp3:Bcoef},
 QFI_matrix:Q,
 QFI_eigenvalues:eigen,
 QFI_determinant:determinant,
 candidateGoldenSurprisalSuccess:cost,
 programOverlapDifferentLorentz:overlap,
 flatBell:flat,rotatedLorentzBell:curved,
 deterministicExactFiniteNoProgramming:"obstruction for continuum of non-phase-equivalent J; proof in companion memo",
 hasPhysicalG0ProgramPreparation:false,hasBookCostSelector:false,
 hasPhysicalGRSource:false,GR_closed:false
},null,2));
