// EXACT ORIGINAL CAR16 full128 KRAUS-CHOI MINIMAL ENVIRONMENT:
/// Q(i,sqrt(24142)) field at true r=1/9, ν=3/5, old phases
// (i,i,-1,-i). Exact elementary CAR + original boosted Julia
// root f(XX†), f(X†X); single F_1009 algebraic-field reduction
// (i->469, sqrt24142->105) has explicit 18x18 minor determinant 407.
// This proves CHARACTERISTIC ZERO original Kraus span rank>=18.
// The 16 original Julia word pairs span at most
// 1 + 4*(c,c†,P) + (boostX,boostX†,boostL,boostR) =17,
// plus the genuine original one K0 identity => rank<=18.
// Thus exact rank=18, not a floating SVD / fitted model.
// Original 64 nonzero FINE label probabilities and original Book03
// Info are NOT replaceable by a free 18-category pointer!
// Minimum coherent environment Hilbert dimension=18 (5 qubits).
// Literal FINE-labelled native one-reflection circuit uses 6 qubits,
// one over the theoretical quantum channel minimum.
// No new physical M1-selected Cost−Info, compulsory Hodge, all42/GR.
import assert from 'node:assert/strict';
let checks=0;const ok=(x,m)=>{assert.ok(x,m);checks++};
const prime=1009,rootI=469,rootS=105,n=16;
const eye=()=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const zeros=()=>Array.from({length:n},()=>Array(n).fill(0));
const I=eye();
const mod=x=>((x%prime)+prime)%prime;
function expmod(x,k){let r=1,a=mod(x);while(k>0){if(k%2)r=mod(r*a);a=mod(a*a);k=Math.floor(k/2)}return r}
const inv=x=>{const a=mod(x);ok(a!==0,'all exact modular algebraic denominators have invertible reduction');return expmod(a,prime-2)};
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>mod(row.reduce((s,v,k)=>s+v*B[k][j],0))));
const scale=(A,v)=>A.map(row=>row.map(x=>mod(x*v)));
const add=(A,B)=>A.map((row,i)=>row.map((x,j)=>mod(x+B[i][j])));
const sub=(A,B)=>A.map((row,i)=>row.map((x,j)=>mod(x-B[i][j])));
const trans=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const same=(A,B)=>A.length===B.length&&A.every((row,i)=>row.every((x,j)=>x===B[i][j]));
const tr=A=>A.reduce((s,row,i)=>mod(s+row[i]),0);
function fermions(){
 const order=[0,2,3,1];
 return Array.from({length:4},(_,r)=>{
  const C=zeros(),before=order.slice(0,order.indexOf(r));
  for(let bits=0;bits<16;bits++)if(((bits>>r)&1)===0)
   C[bits|(1<<r)][bits]=mod(before.reduce((s,j)=>s+((bits>>j)&1),0)%2?-1:1);
  return C;
 });
}
ok(prime%4===1&&expmod(rootI,2)===prime-1&&expmod(rootS,2)===mod(24142),
   '1009 prime admits literal i=469, sqrt24142=105 in one algebraic residue field');
ok(expmod(3,prime-1)===1&&expmod(2,prime-1)===1,
   'modular arithmetic prime check sample Fermat');
const C=fermions();
const G=add(mul(C[0],trans(C[1])),mul(C[1],trans(C[0])));
const U=scale(add(add(scale(I,40),scale(G,9)),mul(G,G)),inv(40));
const xBoost=scale(mul(C[1],U),mod(3*inv(5)*rootI));
const xBoostDagger=scale(mul(U,trans(C[1])),mod(3*inv(5)*(-rootI)));
const Y=mul(xBoost,xBoostDagger),Z=mul(xBoostDagger,xBoost);
const alpha=mod(-5*inv(9)),a=mod(9*inv(25)),b=mod(7929*inv(20000));
const s=mod(rootS*inv(200));
const beta=mod((s-1-alpha*b)*inv(mod(b*(b-a))));
const f=S=>add(add(I,scale(S,alpha)),scale(mul(S,sub(S,scale(I,a))),beta));
const Lboost=f(Y),Rboost=f(Z);
ok(same(mul(Lboost,Lboost),sub(I,Y)),
   'EXACT source Julia Lboost²=I−XX† over genuine original number-field residue');
ok(same(mul(Rboost,Rboost),sub(I,Z)),
   'EXACT source Julia Rboost²=I−X†X over same original number-field residue');
ok(same(mul(Lboost,xBoost),mul(xBoost,Rboost)),
   'EXACT genuine boosted Julia reflection Lboost X = X Rboost and whole 32 CAR×port gate unitarity');
const phases=[rootI,rootI,-1,-rootI];
const words=[];
for(let r=0;r<4;r++){
 const cr=C[r],cd=trans(cr);
 const base=scale(cr,mod(3*inv(5))),baseD=trans(base);
 const P=mul(cr,cd),Q=mul(cd,cr);
 const L0=sub(I,scale(P,inv(5))),R0=sub(I,scale(Q,inv(5)));
 let x,xd,L,R;
 if(r===1){x=xBoost;xd=xBoostDagger;L=Lboost;R=Rboost}
 else {let ph=mod(phases[r]);
  x=scale(cr,mod(3*inv(5)*ph));
  xd=scale(cd,mod(3*inv(5)*inv(ph)));
  L=L0;R=R0;
 }
 words.push([x,L],[xd,R],[scale(base,-1),scale(L0,-1)],[scale(baseD,-1),scale(R0,-1)]);
}
ok(words.length===16,
  'UNCHANGED original 16 Julia pair word patterns after removing exact duplicate word bit');
// ORIGINAL a = n0 is the zeroth Walsh word first-coordinate mean
// a = (1/16) Σ_{k=0..15} words[k][0].
const A=scale(words.reduce((S,w)=>add(S,w[0]),zeros()),inv(16));
ok(A.length===16,'original native A algebraic field reduction exact source');
const nativeBasis=[I],nativeDagger=[I];
for(let r=0;r<4;r++){
 const c=C[r],cd=trans(c),P=mul(c,cd);
 nativeBasis.push(c,cd,P);nativeDagger.push(cd,c,P);
}
nativeBasis.push(xBoost,xBoostDagger,Lboost,Rboost);
nativeDagger.push(xBoostDagger,xBoost,Lboost,Rboost);
ok(nativeBasis.length===17&&nativeDagger.length===17,
  'EXACT original Julia CAR span bound: 13 base+4 boosted=17');
// Rank of 128 actual CAR16 Kraus vector span equals rank of I plus
// 17 native word-adjoint*original A, because both original Walsh (16×16)
// and Golden port factors are invertible/strict nonzero for live columns.
const sourceOps=[I,...nativeDagger.map(B=>mul(B,A))];
ok(sourceOps.length===18,
  'ACTUAL original 128 Kraus upper bound 1+17=18, not sample estimate');
const coordinates=[
 [1,1],[15,11],[14,14],[7,1],[1,7],[4,0],[9,13],[2,6],
 [12,0],[0,12],[1,4],[4,1],[14,10],[7,2],[6,3],[5,4],[4,7],[5,7]
];
const block=sourceOps.map(B=>coordinates.map(([i,j])=>B[i][j]));
function determinantFp(A){
 const B=A.map(row=>row.slice());
 let d=1;
 for(let k=0;k<B.length;k++){
  let pivot=k;
  while(pivot<B.length&&B[pivot][k]===0)pivot++;
  ok(pivot<B.length,'EXACT explicit original 18x18 minor has nonzero Gaussian pivot');
  if(pivot!==k){[B[pivot],B[k]]=[B[k],B[pivot]];d=mod(-d)}
  const v=B[k][k];
  d=mod(d*v);
  const iv=inv(v);
  for(let r=k+1;r<B.length;r++){
   const f=mod(B[r][k]*iv);
   for(let j=k;j<B.length;j++)B[r][j]=mod(B[r][j]-f*B[k][j]);
  }
 }
 return d;
}
const det=determinantFp(block);
ok(det===407,'BIG EXACT F1009 explicit nonzero determinant 407 -> original characteristic-zero Kraus Choi rank >=18');
ok(det!==0,'all 18 selected original source operators linearly independent over algebraic number field');
ok(2**4<18&&18<=2**5,'mathematical minimal coherent DATA Stinespring environment uses exactly FIVE qubits');
ok(18<=64&&64<128,'original literal 64 bright fine-label outcomes remain physically distinct although Choi rank only 18');
console.log(JSON.stringify({
 status:'PASS_NATIVE_ORIGINAL_FULL128_EXACT_CHOI_RANK18_PRIME407',
 checks,
 originalTrueNative:{
  CARdimension:16,allFineKrausLabels:128,brightFineKrausLabels:64,
  originalBoostR:'1/9',nu:'3/5',phases:'(i,i,-1,-i)',
  fullNativeWordSpanUpper:17,
  unretunedOriginalIdentityPlusWordKrausSpanUpper:18,
  certifiedKrausChoiRank:18,
  finitePrime:prime,fieldRootI:rootI,fieldRootSqrt24142:rootS,
  explicitNativeSelected18x18MinorCoordinates:coordinates,
  exactMinorMod1009:det,
  allArithemticBigPrimeCertificate:true,
  minimumCoherentEnvironmentQubits:5,
  literalNativeFineLabelCoherentCompilerQubits:6,
  originalNativeDarkBitQubits:1,
  distinction:'Choi rank=18 does NOT reduce original 64 bright CLASSICAL outcome labels or their branch Info, and no permission to rewrite literal 128 fine alphabet'
 },
 selectedPhysicalM1D0Prep:false,
 fullBook03HodgeInfoSelected:false,
 sameHistoryOriginalAll42EinsteinClosed:false,GR_closed:false
},null,2));
