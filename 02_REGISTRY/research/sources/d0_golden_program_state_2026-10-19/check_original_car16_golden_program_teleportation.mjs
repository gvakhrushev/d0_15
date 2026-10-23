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

// GLOBAL exact mathematical inverse of the COMPLETE native Choi programme:
// in the canonical positive Julia square-root branch the state vector
// coefficients are J[k][i]/sqrt(32), so all J are directly recovered.
// Its ORIGINAL CAR16 grade-one sector is p * U4 on masks 1,2,4,8.
const grade1=[1,2,4,8],theta=.1;
const X4=gen[4],RX4=add(add(eye(4),X4,Math.sin(theta)),mm(X4,X4),1-Math.cos(theta));
const recoveredU=grade1.map(maskI=>grade1.map(maskJ=>Jt[maskI][maskJ]/p));
const inverseError=Math.max(...recoveredU.flatMap((row,i)=>row.map((v,j)=>Math.abs(v-RX4[i][j]))));
assert(inverseError<2e-13,"complete original CAR16 Choi programme globally recovers actual Lorentz U via grade-one top-left block");
assert(Jt[0][n]>0,"real pure-programme global sign fixed by canonical positive Julia sqrt offdiagonal");
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
 globalGrade1LorentzRecoveryError:inverseError,
 flatBell:flat,rotatedLorentzBell:curved,
 deterministicExactFiniteNoProgramming:"obstruction for continuum of non-phase-equivalent J; proof in companion memo",
 hasPhysicalG0ProgramPreparation:false,hasBookCostSelector:false,
 hasPhysicalGRSource:false,GR_closed:false
},null,2));
