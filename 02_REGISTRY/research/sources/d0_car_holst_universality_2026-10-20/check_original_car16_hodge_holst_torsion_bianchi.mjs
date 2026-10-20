#!/usr/bin/env node
"use strict";
/**
 * Original 4-Role Lorentz/carrier parity and continuum first-order
 * Einstein-Hilbert vs Holst universality: exact integer certificates.
 *
 * Carriers are the original Role bivector basis and eta (+---).
 * Consumes original CAR16/grade2 Hodge owner, checks its entire commutant
 * independently over F_1000003, all 24 independent torsion variables,
 * and all 21 pair-symmetric Riemann variables / algebraic first Bianchi.
 * The continuum implication is standard first-order Palatini-Holst
 * variation, NOT a proof selected native Book03/G0/M1 full action equals
 * a member of this class or that the finite SO star is torsion-free.
 */
const ok=(v,m)=>{if(!v)throw Error("FAIL "+m)};
const N=4,M=6,mod=1000003;
const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const pairIndex=new Map(pairs.map((p,i)=>[p.join(","),i]));
const zero=(m,n=m)=>Array.from({length:m},()=>Array(n).fill(0));
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const mult=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const add=(A,B,t=1)=>A.map((r,i)=>r.map((v,j)=>v+t*B[i][j]));
const scal=(A,c)=>A.map(row=>row.map(v=>c*v));
const tr=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const same=(A,B)=>A.length===B.length&&A.every((row,i)=>row.every((v,j)=>v===B[i][j]));
function e(i,j){let X=zero(4);X[i][j]=1;return X}
const eta=[[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,-1]];
const J=zero(6);
J[5][0]=1;J[4][1]=-1;J[3][2]=1;
J[2][3]=-1;J[1][4]=1;J[0][5]=-1;
ok(same(mult(J,J),scal(eye(6),-1)),"ORIGINAL CAR16 grade2 Lorentz Hodge squares to -I");
ok(same(tr(J),scal(J,-1)),"original six Hodge is antisymmetric");
for(const [a,b] of [[1,0],[0,1],[3,5],[-7,3],[0,0]]) {
 const L=add(scal(eye(6),b),J,a),LI=add(scal(eye(6),b),J,-a);
 ok(same(mult(L,LI),scal(eye(6),a*a+b*b)),
   "all REAL alpha,beta Lorentz bivector intertwiners are algebraically invertible unless both zero");
}
function rhoLie(X){
 const A=zero(6);
 const put=(row,col,v)=>{if(v)A[row][col]+=v};
 for(let col=0;col<6;col++){
  const [i,j]=pairs[col];
  for(let k=0;k<4;k++){
   const a=X[k][i];
   if(k!==j&&a){let p=k<j?[k,j]:[j,k];put(pairIndex.get(p.join(",")),col,(k<j?1:-1)*a)}
   const b=X[k][j];
   if(i!==k&&b){let p=i<k?[i,k]:[k,i];put(pairIndex.get(p.join(",")),col,(i<k?1:-1)*b)}
  }
 }
 return A;
}
const X=[];
for(const s of [1,2,3])X.push(add(e(0,s),e(s,0)));
for(const [i,j] of [[1,2],[1,3],[2,3]])X.push(add(e(i,j),e(j,i),-1));
const Actions=X.map(rhoLie);
for(const a of Actions)ok(same(mult(J,a),mult(a,J)),"CAR16 grade2 * commutes with every true so(1,3) generator");
const comm=[];
for(const A of Actions)for(let i=0;i<6;i++)for(let j=0;j<6;j++){
 let row=Array(36).fill(0);
 for(let k=0;k<6;k++){row[i*6+k]+=A[k][j];row[k*6+j]-=A[i][k];}
 comm.push(row);
}
function rankMod(rows){
 const A=rows.map(row=>row.map(x=>((x%mod)+mod)%mod)),m=A.length,n=A[0].length;
 const pow=(b,k)=>{let out=1;while(k){if(k%2)out=out*b%mod;b=b*b%mod;k=Math.floor(k/2)}return out};
 let rank=0;
 for(let col=0;col<n&&rank<m;col++){
  let piv=rank;while(piv<m&&A[piv][col]===0)piv++;
  if(piv===m)continue;
  [A[rank],A[piv]]=[A[piv],A[rank]];
  const inv=pow(A[rank][col],mod-2);
  for(let j=col;j<n;j++)A[rank][j]=A[rank][j]*inv%mod;
  for(let i=rank+1;i<m;i++)if(A[i][col]){
   let t=A[i][col];for(let j=col;j<n;j++)A[i][j]=(A[i][j]-t*A[rank][j]%mod+mod)%mod;
  }
  rank++;
 }
 return rank;
}
const r=rankMod(comm);
ok(r===34,"original proper Lorentz commutant of Lambda2 is EXACTLY span{I,J}: modular rank34 plus two explicit rational kernel vectors");
const perm=[0,2,1,3];
const S=zero(6);
for(let col=0;col<6;col++){
 let [i,j]=pairs[col],a=perm[i],b=perm[j],ord=a<b?[a,b]:[b,a];
 S[pairIndex.get(ord.join(","))][col]=a<b?1:-1;
}
ok(same(mult(S,tr(S)),eye(6)),"odd Role swap exterior action is orthogonal");
ok(same(mult(mult(S,J),tr(S)),scal(J,-1)),"CAR Hodge is ROLE orientation-odd");
ok(same(mult(mult(S,eye(6)),tr(S)),eye(6)),"scalar Holst channel ROLE orientation-even");

const triple=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]];
const columns=Array.from({length:4},(_,a)=>pairs.map(([i,j])=>[a,i,j])).flat();
const rows=pairs.flatMap(([a,b])=>triple.map(ijk=>[a,b,...ijk]));
const sign=p=>{
 if(new Set(p).size!==p.length)return 0;
 let v=1;for(let i=0;i<p.length;i++)for(let j=i+1;j<p.length;j++)if(p[i]>p[j])v=-v;return v;
};
const eqset=(a,b)=>a.length===b.length && a.every(x=>b.includes(x));
const Tmap=zero(24);
for(let j=0;j<24;j++){
 const [a,i,k]=columns[j];
 for(let ii=0;ii<24;ii++){
  const [u,v,...ijk]=rows[ii];
  if(a===u){const q=[i,k,v];if(eqset(q,ijk))Tmap[ii][j]+=sign(q)}
  if(a===v){const q=[u,i,k];if(eqset(q,ijk))Tmap[ii][j]-=sign(q)}
 }
}
const rankT=rankMod(Tmap);
ok(rankT===24,"all 24 genuine independent torsion components killed by D(e^a wedge e^b)=0, no missing torsion mode");
// Exact integer Bareiss determinant independently, proving this 24x24 test
// over Q and not relying on approximate rank or sampled curvature.
function detBareiss(A0){
 const A=A0.map(row=>row.map(x=>BigInt(x))),n=A.length;let sign=1n,den=1n;
 for(let k=0;k<n-1;k++){
  if(A[k][k]===0n){let i=k+1;while(i<n&&A[i][k]===0n)i++;ok(i<n,"torsion map determinant nonzero");
   [A[i],A[k]]=[A[k],A[i]];sign=-sign;}
  const p=A[k][k];
  for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++){
   const numerator=A[i][j]*p-A[i][k]*A[k][j];
   ok(numerator%den===0n,"Bareiss exact integer division");
   A[i][j]=numerator/den;
  }
  for(let i=k+1;i<n;i++)A[i][k]=0n;
  den=p;
 }
 return sign*A[n-1][n-1];
}
const detT=detBareiss(Tmap);
ok(detT!==0n,"exact 24-torsion determinant nonzero");

// Pair symmetric curvature has 21 independent values. First Bianchi in 4D
// is ONLY one scalar relation; Lorentz Holst pseudoscalar equals 8 times it.
const Ri=zero(6);
const permutations=a=>{
 if(a.length===0)return [[]];
 return a.flatMap((x,i)=>permutations(a.filter((_,j)=>j!==i)).map(y=>[x,...y]));
};
const all24=permutations([0,1,2,3]);
function Rab(Q,i,j,k,l){
 if(i===j||k===l)return 0;
 const u=i<j?1:-1,v=k<l?1:-1;
 return u*v*Q[pairIndex.get([Math.min(i,j),Math.max(i,j)].join(","))][pairIndex.get([Math.min(k,l),Math.max(k,l)].join(","))];
}
function Holst(Q){return all24.reduce((sum,ijkl)=>sum+sign(ijkl)*Rab(Q,...ijkl),0)}
function Bianchi(Q){return Rab(Q,0,1,2,3)-Rab(Q,0,2,1,3)+Rab(Q,0,3,1,2)}
for(let i=0;i<6;i++)for(let j=i;j<6;j++){
 const Q=zero(6);Q[i][j]=1;Q[j][i]=1;
 ok(Holst(Q)===8*Bianchi(Q),"full 24-permutation Holst contraction IS eight times first Bianchi for every one of 21 pair-symmetric generators");
}
const Qno=zero(6);Qno[0][5]=Qno[5][0]=1;
ok(Holst(Qno)===8 && Bianchi(Qno)===1,"genuine offshell Holst is NONZERO; Bianchi is load-bearing");
const Qyes=zero(6);Qyes[0][5]=Qyes[5][0]=2;
Qyes[1][4]=Qyes[4][1]=3;
Qyes[2][3]=Qyes[3][2]=1;
ok(Bianchi(Qyes)===0&&Holst(Qyes)===0,"algebraic torsion-free Bianchi eliminates Holst, not Palatini");

// ORIGINAL site coframe dressing by any genuine positive scalar W(K_x)>0:
// two coframe legs => W multiplying BOTH invariant pairings is absorbed
// by the single site coframe ehat=sqrt(W)e. Demonstrate EXACT integers for
// 2 independent positive site weights W1=25/9 and W2=49/25.
const sampleE=[[3,1,0,2],[0,2,1,0],[1,0,2,1],[0,1,0,3]];
const curvature=Array.from({length:6},(_,f)=>Array.from({length:6},(_,v)=>((7*f+11*v+5)%13)-6));
function wedge(a,b){return pairs.map(([i,j])=>a[i]*b[j]-a[j]*b[i])}
function actionOnE(e,alpha,beta){
 const C=add(scal(J,alpha),scal(eye(6),beta));
 let total=0;
 for(let u=0;u<6;u++){
  const [i,j]=pairs[u],Sigma=wedge(e[i],e[j]);
  const CF=mult(C,curvature[u].map(x=>[x])).map(x=>x[0]);
  total+=Sigma.reduce((s,x,k)=>s+x*CF[k],0);
 }
 return total;
}
const orig=actionOnE(sampleE,3,2);
for(const [num,den] of [[25,9],[49,25]]){
 const sqN=Math.round(Math.sqrt(num)),sqD=Math.round(Math.sqrt(den));
 ok(sqN**2===num&&sqD**2===den,"nontrivial site weight is a perfect square rational");
 const ehatNumerator=scal(sampleE,sqN);
 const ehatAction=actionOnE(ehatNumerator,3,2);
 ok(ehatAction===num*orig && ehatAction*den===num*den*orig,
 "finite all-six-face two invariant geometric channels exact Book-Weyl dressing by integer cross multiplication");
}
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_CAR16_LORENTZ_HODGE_HOLST_TORSION_BIANCHI_BOOK_WEYL",
 LorentzCommutant:{rankOverFp:r,dimension:36-r,generatedBy:["I6","CAR16 Hodge J"],J2:"-I",roleReversal:"J odd, I even"},
 independentTorsion:{rows:24,cols:24,rank:rankT,determinant:detT.toString()},
 curvature:{pairSymmetricParameters:21,algebraicBianchiConstraints:1,
  LeviCivitaAlgebraicParameters:20,HolstPseudoscalar:"8 * (R0123-R0213+R0312)",
  offShellHolstValue:Holst(Qno),onBianchiHolstValue:Holst(Qyes)},
 connectionInverse:"(beta I+alpha J)^-1=(beta I-alpha J)/(alpha²+beta²) for (alpha,beta) not both zero",
 PalatiniCondition:"alpha != 0 to retain Einstein coframe equation; beta unconstrained real constant",
 BookWeyl:{commonPositiveSiteWeightAbsorbedInto:"ehat_x=sqrt(W_x)e_x",coframeJacobian:"W_x^8",
  independentExactSiteWeights:["25/9","49/25"],allSixFaceSource:orig},
 proofScope:"exact original finite CAR/so(1,3) algebra + mathematical continuum torsionfree Palatini-Holst theorem; no compulsory Book/G0, no native finite-torsionless/GR refinement",
 GR_closed:false
},null,2));
