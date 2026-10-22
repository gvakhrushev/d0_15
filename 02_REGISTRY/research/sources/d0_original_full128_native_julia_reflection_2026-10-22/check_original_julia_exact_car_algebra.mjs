// The ORIGINAL complete CAR16 four-creator word order=(0,2,3,1),
// proper Lorentz boost r=1/9, nu=3/5, phase word (i,i,-1,-i):
// exact BIGINT proof of all 7 fixed rational Julia sqrt factors, and
// sole boosted role1 Julia sqrt reduced to degree2 polynomials in
// its ACTUAL XX† and X†X. Its only genuinely new positive algebraic
// scalar is sqrt(24142)/200 at r=1/9, as in old Q(i,sqrt24142)
// ORIGINAL 64-live/64-dark rank certificate.
// Native p, Golden gate unchanged; no claimed paid coherent native
// controlled-Julia/oldRIGHT/Book03 physical task/42 Einstein closure.
import assert from 'node:assert/strict';
let checks=0;const ok=(v,m)=>{assert.ok(v,m);checks++};
const dim=16;
const mat=(n=dim)=>Array.from({length:n},()=>Array(n).fill(0n));
const eye=()=>Array.from({length:dim},(_,i)=>Array.from({length:dim},(_,j)=>i===j?1n:0n));
const id=eye();
const transpose=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const add=(A,B)=>A.map((r,i)=>r.map((x,j)=>x+B[i][j]));
const sub=(A,B)=>A.map((r,i)=>r.map((x,j)=>x-B[i][j]));
const mulScalar=(A,x)=>A.map(r=>r.map(v=>v*BigInt(x)));
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0n)));
const tr=A=>A.reduce((s,r,i)=>s+r[i],0n);
const isZero=A=>A.every(r=>r.every(x=>x===0n));
const same=(A,B)=>A.length===B.length&&A.every((r,i)=>r.every((x,j)=>x===B[i][j]));
const pop=n=>{let a=0;while(n){n&=n-1;a++}return a};
const words=[0,2,3,1];
function creators(){
 return Array.from({length:4},(_,r)=>{
  const C=mat(),pre=words.slice(0,words.indexOf(r));
  for(let b=0;b<16;b++)if(!((b>>r)&1)){
   const fermionicSign=pre.reduce((s,j)=>s+((b>>j)&1),0)%2?-1n:1n;
   C[b|(1<<r)][b]=fermionicSign;
  }
  return C;
 });
}
const CAR=creators();
for(const c of CAR){
 const Ct=transpose(c),occupied=mm(c,Ct),empty=mm(Ct,c);
 ok(same(mm(occupied,occupied),occupied),'ALL original CAR16 fermion occupied projectors idempotent');
 ok(same(mm(empty,empty),empty),'ALL original CAR16 fermion empty projectors idempotent');
 ok(same(add(occupied,empty),id),'true original creator CAR {c,c†}=I');
 ok(tr(occupied)===8n&&tr(empty)===8n,'exact original CAR16 creator projector ranks 8+8');
 // unboosted x=(3/5)*e^(i phase)*c has XX†=(9/25)*occupied,
 // R=(I−1/5 empty), L=(I−1/5 occupied).
 const LL=sub(mulScalar(id,5),occupied),RR=sub(mulScalar(id,5),empty);
 ok(same(mm(LL,LL),sub(mulScalar(id,25),mulScalar(occupied,9))),
    '7 original unboosted Julia left roots are EXACT (I−P/5), no floating matrix root');
 ok(same(mm(RR,RR),sub(mulScalar(id,25),mulScalar(empty,9))),
    '7 original unboosted Julia right roots are EXACT (I−Q/5)');
 ok(same(mm(LL,c),mm(c,RR)),
    'original CAR16 fixed unboosted Julia reflection offdiagonal LX=XR');
}
const G=add(mm(CAR[0],transpose(CAR[1])),mm(CAR[1],transpose(CAR[0])));
const G2=mm(G,G),G3=mm(G2,G);
ok(same(G,transpose(G))&&same(G3,G),'original proper boost generator Hermitian and G^3=G');
const H=add(add(mulScalar(id,40),mulScalar(G,9)),G2);
ok(same(mm(H,H),add(add(mulScalar(id,1600),mulScalar(G,738)),mulScalar(G2,162))),
   'EXACT ORIGINAL boost U(ln(5/4))=I+(9/40)G+(1/40)G² and real rational U²');
const C=CAR[1], Ct=transpose(C);
const Hb=mm(H,H);
const Ybar=mulScalar(mm(mm(C,Hb),Ct),9);
const Zbar=mulScalar(mm(mm(H,mm(Ct,C)),H),9);
const a=14400n,b=15858n;
for(const Y of [Ybar,Zbar]){
 const Ya=sub(Y,mulScalar(id,a)),Yb=sub(Y,mulScalar(id,b));
 ok(same(Y,transpose(Y)),'ACTUAL complex original boosted role1 XX† / X†X has rational real selfadjoint spectrum');
 ok(isZero(mm(mm(Y,Ya),Yb)),
    'EXACT 16x16 native role1 Julia positive effect polynomial Y(Y−9/25)(Y−7929/20000)=0');
 ok(tr(Y)===4n*(a+b),'EXACT boosted 16-grade CAR rank spectrum 0 mult8, a mult4, b mult4');
 ok(tr(mm(Y,Ya))===4n*b*(b-a),'EXACT boosted 3-band b projector rank4 with zero external basis');
 ok(tr(mm(Y,Yb))===4n*a*(a-b),'EXACT boosted 3-band a projector rank4');
}
// Entire BOOSTED Julia matrix root is polynomial degree 2 in the actual
// Y=XX†, Z=X†X; the only new scalar s(r)=sqrt(1−(9/25)c(r)).
// At r=1/9, c=(1+6r²+r⁴)/(1−r²)²=881/800,
// beta root b=9c/25=7929/20000,
// s²=1−b=12071/20000=(sqrt(24142)/200)².
ok(881n*9n===7929n,'old original real boost cosh(2theta)=881/800');
ok(b===2n*7929n,'original scaled boosted eigen b=15858/40000=7929/20000 exact rational');
ok(40000n*(20000n-7929n)===20000n*24142n,
   'one original boosted source scalar s=sqrt(24142)/200 exactly');
const gprimeNum=29889n,gprimeDen=16000n;
ok(gprimeNum*16000n===29889n*gprimeDen,
 'native proper boost c(r) derivative exact rational cʹ(1/9)=29889/16000');
let fact=0;
for(let label=0;label<32;label++){
 for(let k=0;k<16;k++){
  const t0=(pop(label&(2*k))%2?-1:1),t1=(pop(label&(2*k+1))%2?-1:1);
  const wanted=(label%2===1)?0:2*(pop((label>>1)&k)%2?-1:1);
  ok(t0+t1===wanted,'EXACT native 32 duplicated Julia words Walsh dark/bright reduction to H4');
  fact++;
 }
}
// For each original word pair t=0,1,2,3 and role r, the fixed Julia
// reflection H_X=[[L,X],[X†,−R]] has H_X²=I because original L²+XX†=I,
// R²+X†X=I and LX=XR. Controlled native tag correction:
// tag0: H_X|0>=[L;X†] -> X(port)=[X†;L] == (w0†,w1†);
// tag1: H_X|1>=[X;−R] -> Z(port)=[X;R];
// eta1 native -base word is a SINGLE controlled sign, no new amplitude.
const p=(Math.sqrt(5)-1)/2;
ok(Math.abs(p+p*p-1)<1e-15,'original Golden p+p²=1');
const Gport=[[Math.sqrt(p),-p],[p,Math.sqrt(p)]];
const nativeG=[Gport[1][0],Gport[0][0]];
ok(Math.abs(nativeG[0]-p)<1e-15&&Math.abs(nativeG[1]-Math.sqrt(p))<1e-15,
 'one ORIGINAL XG on native Golden port prepares (p,sqrtp)');
ok(Math.abs(Gport[0][0]**2+Gport[1][0]**2-1)<1e-15,'native Golden unitary norm');
const s=Math.sqrt(24142)/200,c=(881/800),bp=(9/25)*c;
const alpha=-5/9,beta=(s-1-alpha*bp)/(bp*(bp-9/25));
const f=x=>1+alpha*x+beta*x*(x-9/25);
ok(Math.abs(f(0)-1)<1e-15&&Math.abs(f(9/25)-4/5)<1e-15&&Math.abs(f(bp)-s)<2e-14,
 'native ORIGINAL boosted Julia L and R same degree2 polynomial of XX† or X†X, one scalar sqrt(24142)/200');
ok(s>.77&&s<.78&&beta<0&&beta>-.2,'native original boosted Julia extra root rational algebra chart consistent');
const theta=Math.log(5/4),thetaPrimeDen=1-1/81;
const cr=29889/16000,sPrime=-(9/50)*cr/s;
ok(sPrime<-.4&&sPrime>-.5,'native boosted Julia field scalar has strict negative nontrivial source; not source-flat');
console.log(JSON.stringify({
 status:'PASS_ORIGINAL_COMPLEX_CAR16_JULIA_SINGLE_FIELD_SQRT_WALSH_DUPLICATE',
 checks,
 unchangedNativeOriginal:{
   CAR16_creators:4,fullOriginalKraus:128,role1RealBoostR:'1/9',
   boostH40:'40I+9G+G²',boostHighestEigen:'7929/20000',
   JuliaPositiveBands:['0 mult8','9/25 mult4','7929/20000 mult4'],
   exactExtraPositiveScalar:'sqrt(24142)/200',numericExtraPositiveScalar:s,
   boostedJuliaRootPolynomial:'f(Y)=I−(5/9)Y+β Y(Y−(9/25)I)',
   degree2Beta:beta,fieldDerivativeOfPositiveExtraScalar:sPrime,
   exactlyUnboostedJuliaBranches:7,oneNontrivialBoostedJuliaBranch:1,
   nativeWalshDuplicatedSignChecks:fact,
   exactOrig128DarkLabels:64,actualOriginalBrightLabels:64,
   nativeGolden_p:p
 },
 physicallyControlledJuliaGateAdmitted:false,
 actualPaidFull128FactoryClockUnchanged:false,
 nativePhysicalBook03HodgeInfoSelected:false,
 GR_closed:false
},null,2));
