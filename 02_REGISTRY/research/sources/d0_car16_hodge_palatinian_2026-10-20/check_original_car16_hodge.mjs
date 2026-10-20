// Exact integer test: existing D0 four CAR modes -> original Lorentz Hodge.
// Standalone: node check_original_car16_hodge.mjs
// Research scope: finite algebra/normalization, NOT an admitted physical Book price.
import assert from "node:assert/strict";

const roles = ["A","B","C","D"], fockDimension = 16;
function popcount(n) { let k=0; while(n) {k += n & 1; n >>>= 1;} return k; }
function gamma(r,mask) {
  const parity = popcount(mask & ((1<<r)-1)) % 2;
  return [mask ^ (1<<r), parity ? -1 : 1];
}
function act(word,mask) {
  let sign=1;
  for(let k=word.length-1;k>=0;k--) {
    const [newmask,s] = gamma(word[k],mask);
    mask=newmask; sign*=s;
  }
  return [mask,sign];
}
function tr(word) {
  let s=0;
  for(let mask=0;mask<fockDimension;mask++) {
    const [image,sgn]=act(word,mask);
    if (image===mask) s+=sgn;
  }
  return s;
}
function levi(a) {
  if(new Set(a).size!==4) return 0;
  let v=1;
  for(let i=0;i<4;i++) for(let j=i+1;j<4;j++) if(a[i]>a[j]) v=-v;
  return v;
}
function matmul(A,B) {
  return A.map(row=>B[0].map((_,j)=>row.reduce((sum,x,k)=>sum+x*B[k][j],0)));
}
function transpose(A) { return A[0].map((_,i)=>A.map(row=>row[i])); }

const gammaWord=[0,1,2,3];   // OWNER: A,B,C,D in ArchiveCARRelations.
for(let mask=0;mask<16;mask++) {
  const [image,sgn] = act(gammaWord,mask);
  assert.equal(image,mask ^ 0b1111);
  assert.ok(sgn===1||sgn===-1);
  assert.equal(popcount(image),4-popcount(mask));
  assert.equal(act(gammaWord,image)[0],mask);
}
assert.equal(tr(gammaWord),0);
for(let a=0;a<4;a++)for(let b=0;b<4;b++)
for(let c=0;c<4;c++)for(let d=0;d<4;d++) {
  // EXACT 16-dimensional Fock trace / top exterior epsilon:
  assert.equal(tr([...gammaWord,a,b,c,d]),16*levi([a,b,c,d]));
}
assert.equal(tr([0,1,2,3]),0);
assert.equal(tr([0,1,2,3,0,1,2,3]),16);
// Euclidean trace with four distinct gamma and no chiral insertion is zero.
assert.equal(tr([0,1,2,3]),0);

const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const masks=pairs.map(ab=>(1<<ab[0])|(1<<ab[1]));
const eta=[1,-1,-1,-1];
const M=pairs.map(ab=>eta[ab[0]]*eta[ab[1]]);
assert.deepEqual(M,[-1,-1,-1,1,1,1]);
const H=pairs.map((_,i)=>pairs.map((_,j)=>{
  const [output,sign]=act(gammaWord,masks[j]);
  return output===masks[i]?sign:0;
}));
const J=H.map(row=>row.map((v,j)=>v*M[j]));
const existingOwnedHodge=[
  [0,0,0,0,0,-1],
  [0,0,0,0,1,0],
  [0,0,0,-1,0,0],
  [0,0,1,0,0,0],
  [0,-1,0,0,0,0],
  [1,0,0,0,0,0],
];
assert.deepEqual(J,existingOwnedHodge);
assert.deepEqual(matmul(J,J),J.map((r,i)=>r.map((_,j)=>i===j?-1:0)));
assert.deepEqual(transpose(J),J.map(row=>row.map(x=>-x)));
assert.deepEqual(matmul(H,H),H.map((r,i)=>r.map((_,j)=>i===j?1:0)));
assert.notDeepEqual(H,J); // Minkowski metric raising is essential.

const swapBC=idx=>(idx===1?2:idx===2?1:idx);
const U2=pairs.map((_,i)=>pairs.map((_,j)=>{
  const orig=pairs[j];
  const permuted=orig.map(swapBC);
  const permMask=(1<<permuted[0])|(1<<permuted[1]);
  const sign=(permuted[0]>permuted[1]?-1:1);
  return permMask===masks[i]?sign:0;
}));
assert.deepEqual(matmul(U2,transpose(U2)),
  U2.map((r,i)=>r.map((_,j)=>i===j?1:0)));
assert.deepEqual(matmul(matmul(U2,J),transpose(U2)),
  J.map(row=>row.map(v=>-v)));

// Exact 4D oriented Palatini contraction from the OWNED CAR16 trace.
// Define Lorentz gamma_A = gamma_A, gamma_(B,C,D) = i gamma_(B,C,D).
// Gamma_5 = i gamma_A^L gamma_B^L gamma_C^L gamma_D^L = Gamma.
// Therefore (i/16)Tr(Gamma_5 gamma_a^L gamma_b^L gamma_c^L gamma_d^L)
// equals epsilon_abcd: if indices are all distinct, the 3 spatial i factors
// multiply to -i, and the prefactor i converts it back to +1.
const e=[2,1,-3,4], f=[-1,2,1,3], F=[
  [0,2,-1,3],[-2,0,4,-2],[1,-4,0,5],[-3,2,-5,0]
];
let palatini=0,carInsertion=0;
for(let a=0;a<4;a++)for(let b=0;b<4;b++)
for(let c=0;c<4;c++)for(let d=0;d<4;d++) {
  const eps=levi([a,b,c,d]);
  palatini+=eps*e[a]*f[b]*F[c][d];
  // For a,b,c,d distinct exactly 3 of them spatial; repeats have trace0.
  const trace=tr([...gammaWord,a,b,c,d]);
  carInsertion+=(trace/16)*e[a]*f[b]*F[c][d];
}
assert.equal(carInsertion,palatini);
assert.notEqual(palatini,0);

console.log("PASS_ORIGINAL_CAR16_HODGE_GRADE2_PALATINI_EXACT");
console.log("Fock dimension=16, unique degree-preserved sector k=2 (dim6)");
console.log("CAR16 chiral 4-index trace: 256/256 exact integer identities");
console.log("owned Lorentz Hodge matrix: 36/36 exact; J^2=-I; H^2=+I");
console.log("signed odd Role swap B<->C flips J exactly");
console.log("sample oriented Palatini contraction:",palatini);
console.log("SCOPE: geometric contraction only; original full Book selected price and GR remain OPEN");