#!/usr/bin/env node
"use strict";
/*
 * Original complete 17-POSITIVE-outcome Golden p + two fresh Julia +
 * fixed BELL full17 recorder on the original genuine SO+(1,3)
 * has an EXACT finite matrix GROUP REVERSAL Z2 GRADE:
 *
 *   q(P^-1) = swapAllSixSignedMarkPairs(q(P)),
 *   rest GG,GB,BG,BB and ACTUAL Bell failure fixed,
 *   H_full17(P^-1)=H_full17(P) identically,
 *   odd signed Golden sqrt contrasts reverse sign.
 *
 * Hence ANY symmetric scalar functional of the UNLABELLED
 * marked POINTER probabilities (including full Shannon, Renyi,
 * symmetric unmarked aggregate and full trace) is REVERSAL-EVEN
 * and has ZERO first odd-curvature derivative at flat.
 * The full original complete recorder has a SIX-DIMENSIONAL
 * label-odd output subspace (difference of each +/- pair) that
 * DOES carry the exact signed native Lorentz curvature
 * (P-P^-1)/2 on its positive-root chart.
 *
 * This is a genuine algebraic reversal theorem for the actual
 * 17-outcome MARKED instrument; full native BOOK03 H+J+R
 * still has NOT been shown to physically select its odd channel.
 * Reversal of the conditional instrument does NOT assert
 * equality of the scalar path weights w_+ and w_-.
 */
const assert=(ok,msg)=>{if(!ok)throw Error("FAIL "+msg)};
const p=(Math.sqrt(5)-1)/2,ell=Math.log((1+Math.sqrt(5))/2),herald=1/4096;
const I=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const Z=()=>I().map(r=>r.map(()=>0));
const E=(i,j)=>{const A=Z();A[i][j]=1;return A};
const add=(A,B,k=1)=>A.map((r,i)=>r.map((v,j)=>v+k*B[i][j]));
const sc=(A,k)=>A.map(r=>r.map(v=>v*k));
const mm=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,v,k)=>s+v*B[k][j],0)));
const T=A=>A[0].map((_,j)=>A.map(r=>r[j]));
const tr=A=>A.reduce((s,r,i)=>s+r[i],0);
const fro=(A,B)=>A.reduce((s,r,i)=>s+r.reduce((v,x,j)=>v+x*B[i][j],0),0);
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const invL=A=>mm(mm(eta,T(A)),eta);
const max=A=>Math.max(...A.flat().map(x=>Math.abs(x)));
const G=[
  add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
  add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),
  add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)
];
function expNull(index,t){
 const X=G[index],X2=mm(X,X);
 return add(add(I(),X,t),X2,t*t/2);
}
function cayley(index,t){
 const X=G[index],A=add(I(),X,t/2),B=add(I(),X,-t/2);
 // Neumann inverse for bounded small real 4×4,
 // OR nilpotent 2/3 exact; for rotation/boost use
 // finite standard inverses from η-group inverse:
 // We use Euler-style exp for the TWO generators not nilpotent.
 if(index<4)return expNull(index,t);
 if(index===4)return add(add(I(),X,Math.sin(t)),mm(X,X),1-Math.cos(t));
 return [[Math.exp(-t),0,0,0],[0,Math.exp(t),0,0],[0,0,1,0],[0,0,0,1]];
}
function q17(P){
 const mean=tr(P)/4,v=fro(P,P)/4;
 let q=[];
 for(const Gx of G){
  const x=fro(Gx,P)/(2*Math.SQRT2),f=herald*p**4/24;
  q.push(f*(mean+x)**2,f*(mean-x)**2);
 }
 const sumMarked=q.reduce((s,x)=>s+x,0),
  GG=herald*p**4*v,
  GB=herald*p*p*(1-p*p*v),
  BG=herald*p**3*v,
  BB=herald*(1-p**4*v-p*p*(1-p*p*v)-p**3*v);
 q.push(GG-sumMarked,GB,BG,BB,1-herald);
 assert(q.length===17&&q.every(x=>x>0)&&
   Math.abs(q.reduce((s,x)=>s+x,0)-1)<8e-14,
   "original FULL Golden17 including Bell fail not normalized/positive");
 return q;
}
const swap=q=>q.map((v,i)=>i<12?q[i^1]:v);
const H=q=>-q.reduce((s,x)=>s+x*Math.log(x),0)/ell;
const samples=[];
for(let j=0;j<18;j++){
 const t=.006*(1+j%5),s=.007*(1+(3*j)%4);
 const P=mm(mm(cayley(j%6,t),cayley((j+1)%6,s)),
            cayley((j+4)%6,.008*(1+(j%3))));
 assert(max(add(mm(mm(T(P),eta),P),eta,-1))<2e-11,
    "based proper Lorentz packet violates ORIGINAL η");
 const pinv=invL(P),q=q17(P),qi=q17(pinv),reversed=swap(q);
 const e=Math.max(...qi.map((x,i)=>Math.abs(x-reversed[i]))),
   h=Math.abs(H(q)-H(qi));
 assert(e<5e-15&&h<1e-14,
  "Golden17 full distribution not exactly grade Z2 under original path reversal");
 const odd=Array.from({length:6},(_,i)=>.5*(q[2*i]-q[2*i+1])),
       oddInv=Array.from({length:6},(_,i)=>.5*(qi[2*i]-qi[2*i+1]));
 assert(odd.every((v,i)=>Math.abs(v+oddInv[i])<5e-15),
  "full original six odd Golden source marks did not reverse sign");
 const trEqual=Math.abs(tr(P)-tr(pinv))<1e-13,
       froEqual=Math.abs(fro(P,P)-fro(pinv,pinv))<1e-12;
 assert(trEqual&&froEqual,"original SO eta-involution not orthogonal Frobenius");
 const rDirect=sc(add(P,pinv,-1),.5),
  rRead=G.reduce((A,X,i)=>{
    const bp=(Math.sqrt(q[2*i])-Math.sqrt(q[2*i+1]))*
                  256*Math.sqrt(3)/(p*p),
          bm=(Math.sqrt(qi[2*i])-Math.sqrt(qi[2*i+1]))*
                  256*Math.sqrt(3)/(p*p);
    return add(A,X,(bp-bm)/4);
  },Z());
 // q includes Bell prefactor. Since original signed sqrt CONTRAST
 // normalization is 256sqrt3/p² on q/h, each true group coefficient
 // is recovered exactly on the positive sign root chart.
 const groupError=max(add(rDirect,rRead,-1));
 assert(groupError<3e-12,
  "original complete reversal-marked Golden source failed to recover odd Lorentz group");
 samples.push({case:j,full17EvenShannon:H(q),
   completeReversalPermutationError:e,
   evenShannonError:h,
   fullOddGroupRecoveryError:groupError,
   nonzeroOddMarks:odd.filter(v=>Math.abs(v)>1e-15).length});
}
const output={
 status:"PASS_ORIGINAL_COMPLETE_GOLDEN17_FULL_Z2_REVERSAL_EVEN_SHANNON_ODD_LORENTZ_MARK",
 trueOriginalGroup:"SO+(1,3) null eta; full signed G_a=(N2,N3,barN2,barN3,J23,B)",
 bothBasedFaceOrientations:true,
 all17NativeGoldBellPositiveFlagsIncluded:true,
 realProperLorentzMixedNoncommutativeCases:samples.length,
 exactSymbolicReason:"eta A^T eta orthogonal involution for Frobenius, Lie eta-skew, group inverse; Tr(P^-1)=Tr P, ||P^-1||F=||P||F, signed six projections reverse",
 sixAntisymmetricOutcomeDirections:true,
 completePointerShannonStrictReversalEven:true,
 originalOddCurvatureRecoverableDirectlyFromPositiveProbabilitySquareRoots:true,
 results:samples,
 fundamentalSelectionGap:"Book/G0 whole H+J+R MUST physically choose odd oriented coframe/Hodge source, cannot be inferred merely from complete Golden17 observation",
 GR_closed:false
};
console.log(JSON.stringify(output,null,2));
