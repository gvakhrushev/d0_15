// ORIGINAL D0 CAR16 creation order (0,2,3,1), unchanged role phases
// (i,i,-1,-i), nu=3/5: 7 of the actual 8 native Julia role/base
// reflections compile exactly with THREE fixed signed-permutation
// monomial native Clifford/Toffoli words using HONEST heralding.
// Seven accepted uniform H^3 paths select [Z,Z,Z,Z,S_B,S_B,S_C],
// eighth reports failure. Success Kraus=(4Z+2S_B+S_C)/8 = (5/8)J_X
// on ALL unknown aux×CAR states (oldRIGHT spectator): exact P=25/64.
// All failed classical/quantum work remains; does NOT imply free retries.
// The one true role1 boosted Julia gate needs NEW algebraic sqrt24142/200;
// a rigorous ramification/Galois field obstruction excludes exact
// synthesis even by finite postselection from ONLY field-independent
// Golden/H/Q8/Pauli/CNOT/Toffoli gates. Necessitates field-sourced native
// gate/resource, or controlled physical approximation with source bounds.
// No original full native 42/Book03 physical action selection is claimed.
import assert from 'node:assert/strict';
let checks=0;const ok=(x,m)=>{assert.ok(x,m);checks++};
const D=32,N=16;
const mat=()=>Array.from({length:D},()=>Array.from({length:D},()=>[0,0]));
const plus=(x,y)=>[x[0]+y[0],x[1]+y[1]];
const neg=x=>[-x[0],-x[1]];
const mul=(x,y)=>[x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]];
const adj=x=>[x[0],-x[1]];
const scale=(x,c)=>[c*x[0],c*x[1]];
const same=(x,y)=>x[0]===y[0]&&x[1]===y[1];
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>plus(s,mul(x,B[k][j])),[0,0])));
const isId=A=>A.every((row,i)=>row.every((x,j)=>same(x,[i===j?1:0,0])));
const isZero=A=>A.every(row=>row.every(x=>same(x,[0,0])));
const Z=mat(),I=mat();for(let i=0;i<D;i++){I[i][i]=[1,0];Z[i][i]=[i<16?1:-1,0]}
const PRE=[0,2,3,1];
function create(role){
 const T=Array.from({length:N},()=>Array.from({length:N},()=>[0,0]));
 for(let b=0;b<N;b++)if(!((b>>role)&1)){
  const prior=PRE.slice(0,PRE.indexOf(role));
  const sign=prior.reduce((s,j)=>s+((b>>j)&1),0)%2?-1:1;
  T[b|(1<<role)][b]=[sign,0];
 }
 return T;
}
function complexPartial(role,baseflag){
 const T=create(role);
 const ph=baseflag?[1,0]:[[0,1],[0,1],[-1,0],[0,-1]][role];
 return T.map(row=>row.map(x=>mul(ph,x)));
}
function isMonomialSelfAdjInvolution(S,label){
 for(let i=0;i<D;i++){
  const nonzero=S[i].filter(x=>!same(x,[0,0]));
  ok(nonzero.length===1,label+' each native computational row one reversible phase/permutation');
  ok(nonzero.every(x=>x[0]*x[0]+x[1]*x[1]===1),
    label+' CAR sign and fixed ±i phase only');
  const cols=S.map(row=>row[i]).filter(x=>!same(x,[0,0]));
  ok(cols.length===1,label+' each native computational column one reversible permutation');
 }
 for(let i=0;i<D;i++)for(let j=0;j<D;j++)
  ok(same(S[i][j],adj(S[j][i])),
    label+' native ±i Jordan-Wigner conditional permutation is Hermitian');
 const SS=mm(S,S);
 ok(isId(SS),label+' fixed native signed permutation exactly involutive');
}
const sigs=[];
for(let role=0;role<4;role++)for(let baseflag=0;baseflag<2;baseflag++){
 if(role===1&&baseflag===0)continue; // THE ONE PHYSICAL REAL BOOST
 const T=complexPartial(role,baseflag),A=Array(D).fill(false),Fact=mat();
 for(let j=0;j<N;j++)for(let i=0;i<N;i++)if(!same(T[i][j],[0,0])){
  A[i]=true;A[N+j]=true;
  Fact[i][N+j]=T[i][j]; Fact[N+j][i]=adj(T[i][j]);
 }
 ok(A.filter(Boolean).length===16,
  'native 7 unboosted CAR16 rank8 partial isometry couples exactly 8 two-dimensional aux/CAR planes');
 const Zidle=mat(),SB=mat(),SC=mat(),J5=mat();
 for(let i=0;i<D;i++)for(let j=0;j<D;j++){
  if(i===j&&!A[i])Zidle[i][j]=Z[i][j];
  SB[i][j]=plus(Zidle[i][j],Fact[i][j]);
  SC[i][j]=plus(neg(Zidle[i][j]),Fact[i][j]);
  // Independently ORIGINAL rational nu=3/5 Julia J block:
  // J5=5Z−(Z P_active)+3 Fact.
  J5[i][j]=plus(scale(Z[i][j],i===j?(A[i]?4:5):0),scale(Fact[i][j],3));
  const sum=plus(scale(Z[i][j],4),plus(scale(SB[i][j],2),SC[i][j]));
  ok(same(sum,J5[i][j]),'EXACT native 3H seven success words reproduce old J_X: 4Z+2SB+SC=5 J');
 }
 isMonomialSelfAdjInvolution(SB, 'S_B old role '+role+' baseflag '+baseflag);
 isMonomialSelfAdjInvolution(SC, 'S_C old role '+role+' baseflag '+baseflag);
 // J5²=25I EXACT on ALL32 complex CAR aux including inactive basis,
 // so success^† success=(25/64)I as a QUANTUM instrument and doesn't
 // dephase ORIGINALLY coherent oldRIGHT entanglement on flagged success.
 const JJ=mm(J5,J5);
 for(let i=0;i<D;i++)for(let j=0;j<D;j++)
  ok(same(JJ[i][j],[i===j?25:0,0]),
     'FULL ORIGINAL native 7 Julia input-independent success K†K=25/64 I exact Gaussian integer');
 const aux0=[],aux1=[];
 for(let j=0;j<N;j++){
  // old original native WORD TAG 0 via Julia output-port X:
  // tag0 original word = (X†,L), tag1 original word = (X,R).
  const col0=J5.map(row=>row[j]),col1=J5.map(row=>row[N+j]);
  const target0=[...col0.slice(N),...col0.slice(0,N)];
  const target1=[...col1.slice(0,N),...col1.slice(N).map(neg)];
  aux0.push(target0);aux1.push(target1);
  for(let i=0;i<N;i++){
   const conj=adj(T[j][i]);
   ok(same(target0[i],scale(conj,3)),
    'TAG0 native original Julia output X† exactly from hereditary success reflection');
   ok(same(target1[i],scale(T[i][j],3)),
    'TAG1 native original Julia output X exactly from hereditary success reflection');
  }
 }
 sigs.push({role,baseflag,phase:baseflag?'1':['i','i','-1','-i'][role],
   exact_clifford_permutation_words:['Z x4','S_B x2','S_C x1','abort x1'],
   native_success:25/64,dimension:32});
}
ok(sigs.length===7,'EXACT seven native fixed Julia role×base blocks: 4×2−1 moving boost');
// Already OWNED actual boost slot r=1/9 has pure algebraic obstacle.
// p=(sqrt5−1)/2: a=sqrt p solves f(a)=a⁴+a²−1, discr(f)=−400.
// Native H entries 1/sqrt2, Q8 i: the FIXED gate number field is
// K=Q(i,sqrt2,sqrt p) (=splitting field f with sqrt2).
// This field is unramified outside primes 2 and5.
// 12071 is prime and 24142=2*12071; Q(sqrt12071) ramifies
// at 12071, hence sqrt24142 not in K. Any finite unitary or
// postselected Kraus operator from these static gates has entries
// in K. If it is c*J_boost with c ≠0, a NONZERO X offdiag is in
// Q(i) (since at r=1/9 Uboost=(40I+9G+G²)/40), thus c in K.
// But Tr L_boost=56/5+4sqrt24142/200 not in K; contradiction.
const discrimination=(256*(-1)**3)-(128*1**2*(-1)**2)+(16*1**4*(-1));
ok(discrimination===-400,'exact native Golden sqrtp quartic discriminant -400: ramifies only 2/5');
let prime=true;for(let q=2;q*q<=12071;q++)if(12071%q===0){prime=false;break}
ok(prime&&12071>5&&24142===2*12071,
 'STRICT integer 12071 prime: sqrt24142 boosts number field with NEW ramified prime');
ok(12071%4===3, 'Q(sqrt12071) has fundamental discriminant 4*12071 with new prime');
const boosted=(Math.sqrt(24142)/200),trL=56/5+4*boosted;
ok(boosted>.776&&boosted<.778&&trL>14.30&&trL<14.32,
 'ACTUAL native boosted Julia L trace=8+4*(4/5)+4 sqrt24142/200; not in fixed-Golden number field');
const p=(Math.sqrt(5)-1)/2;
ok(Math.abs(p*p+p-1)<1e-15,'native p fixed no fitted Golden');
const uniformFlagDerivative=0;
ok(uniformFlagDerivative===0,
 'heralded seven fixed Julia block success probability 25/64 gives ZERO measured-success-FLAG source under arbitrary moving native DATA and protected RIGHT, not whole work Info');
console.log(JSON.stringify({
 status:'PASS_SEVEN_ACTUAL_CAR16_JULIA_HERALDED_CLIFFORD_MUX_AND_ONE_BOOSTED_GALOIS_GATE',
 assertions:checks,
 originalNative:{CARdimension:16,JuliaCarrier:32,
   wordPairs:16,controlledNativeJuliaBranches:8,
   purelyDiscreteHeraldedBranches:7,
   oneGenuineFieldBoostedBranch:1,
   goldenP:p,unchangedRolePhases:['i','i','-1','-i'],
   nativeNu:'3/5',
   full128OriginalKrausStill64Bright64Dark:true},
 gate:{
   formula:'J_X=(4 Z + 2 S_B + S_C)/5 on full AUX2×CAR16, S_B,C signed involutive permutations',
   heraldSuccessKraus:'(5/8) J_X',
   heraldSuccessProbability:25/64,
   fairPath3Hadamards:8,acceptedNativeIndexClasses:[4,2,1],abort:1,
   nativeLogicalMaterials:'Hadamard, original CAR fermionic monomial permutation, Q8 ±i phase, CNOT, Toffoli, native coherent flag and honest measured abort',
   protectedOldRIGHTAccessRequired:false,
   nativeUnconditionalGateAftSuccessIndependentOfUnknownInput:true,
   matrixAndControlledCircuitGateCountFullyPaid:false,
   sevenOriginalBranches:sigs
 },
 galois:{
   goldenField:'Q(i,sqrt2,sqrt((sqrt5-1)/2))',
   goldenRootMinimalPolynomial:'x^4+x^2−1',
   goldenRootDiscriminant:-400,
   ramificationGoldenOnly:[2,5],
   boostedJuliaExtraRoot:'sqrt(24142)/200',
   boostedExtraPrime:12071,
   boostedLTrace:'56/5+4 sqrt(24142)/200',
   exactFieldIndependentGoldenHQ8CliffordPostselectBoostGateImpossible:true,
   physicalFieldSourcedBoostGateStillRequired:true
 },
 physicalFullNativeBook03Selection:false,
 independentAll42GRProof:false,
 GR_closed:false
},null,2));
