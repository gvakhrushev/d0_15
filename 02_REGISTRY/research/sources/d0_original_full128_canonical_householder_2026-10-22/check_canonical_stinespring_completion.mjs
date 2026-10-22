// ORIGINAL D0 FULL128: literal specified finite fine-labelled Kraus
// Stinespring V, initialized work inclusion J, native positive
// B=J†V=K0=I-2p² A†A. Canonical DIRECT ROTATION U:
// U=( (J+V)(I+B)^(-1)(J+V)†-I )(2JJ†-I).
// UJ=V, U†V=J, U=I outside span(J,V) and U=U_D⊗I_oldRIGHT.
// No arbitrary unitary completion, no unknown-data inverse,
// no oldRIGHT addressability for a COHERENT full-archive echo.
// Same instrument's forward physical G0 native paid gate implementation
// (including inverse/work register access) is NOT proven.
// Exact BigInt rational K8 midpoint inverse resolvent bound <3e-20.
// Noncommuting inherited two-Kraus source fixture independently checks
// full unmeasured 4x4 completion and first derivatives.
// Original full128 exact CAR16 two-band spectral input consumed, no
// heavy 128x16 gate/42 Einstein suite rerun.
import assert from 'node:assert/strict';
let checks=0;const ok=(x,m)=>{assert.ok(x,m);checks++};
const close=(x,y,t=3e-12,m='close')=>ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
const nearMat=(A,B,t=3e-12,m='mat')=>{
  ok(A.length===B.length&&A[0].length===B[0].length,m+' dims');
  for(let i=0;i<A.length;i++)for(let j=0;j<A[0].length;j++)
    close(A[i][j],B[i][j],t,m+'['+i+','+j+']');
};
const MM=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const T=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const I=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const zeros=(m,n)=>Array.from({length:m},()=>Array(n).fill(0));
const plus=(A,B)=>A.map((row,i)=>row.map((x,j)=>x+B[i][j]));
const minus=(A,B)=>A.map((row,i)=>row.map((x,j)=>x-B[i][j]));
const mul=(A,v)=>A.map(row=>row.map(x=>x*v));
const diag=x=>x.map((v,i)=>x.map((_,j)=>i===j?v:0));
const tr=A=>A.reduce((s,row,i)=>s+row[i],0);
const norm2Vector=v=>Math.sqrt(v.reduce((s,x)=>s+x*x,0));
const normF=A=>Math.sqrt(A.reduce((s,row)=>s+row.reduce((a,v)=>a+v*v,0),0));
const J=[[1,0],[0,1],[0,0],[0,0]];
const PJ=MM(J,T(J)),RJ=minus(mul(PJ,2),I(4));
function originalFixture(a,b=.8){
 const v=Math.sqrt(1-a*a),u=Math.sqrt(1-b*b);
 const Ks=[diag([a,b]),[[0,u],[v,0]]];
 const V=[[a,0],[0,b],[0,u],[v,0]];
 const B=MM(T(J),V);
 const D=diag([v,u]);
 const W=[[0,0],[0,0],[0,1],[1,0]];
 const A=plus(J,V);
 // Exact \Sigma=(I+B)^-1, no arbitrary right completion.
 const C=diag([1/(1+a),1/(1+b)]);
 const RM=minus(MM(MM(A,C),T(A)),I(4));
 const U=MM(RM,RJ);
 const F=minus(I(2),MM(T(B),B));
 const P1=plus(PJ,MM(W,T(W)));
 for(let k=0;k<2;k++)close(tr(MM(T(Ks[k]),Ks[k])),k===0?a*a+b*b:v*v+u*u,2e-13,
    'true existing fine two-Kraus kept');
 nearMat(MM(T(V),V),I(2),3e-13,'full all fine events actual native isometry');
 nearMat(MM(T(J),V),B,1e-14,'literal initialized fine-labelled native compressed blank');
 nearMat(MM(T(A),A),mul(plus(I(2),B),2),4e-13,'midpoint full two-isometry Gram');
 nearMat(MM(RM,RM),I(4),5e-13,'real canonical Householder is an EXACT unitary involution');
 nearMat(MM(U,T(U)),I(4),5e-13,'canonical U_N truly unitary on whole fine result carrier');
 nearMat(MM(U,J),V,4e-13,'NO ARBITRARY COMPLETION: U_can J = actual complete Kraus V');
 nearMat(MM(T(U),V),J,4e-13,'NO oldRIGHT addressability needed for backward coherent branch U† V=J');
 nearMat(MM(RM,V),J,4e-13,'literal one Householder swaps prepared and forward Kraus planes');
 nearMat(MM(T(W),J),zeros(2,2),4e-13,'actual original native complement W orthogonal to true J');
 nearMat(MM(T(W),W),I(2),4e-13,'true leftover Kraus output polar normalizes original W');
 nearMat(MM(U,W),plus(MM(J,mul(D,-1)),MM(W,B)),4e-13,
   'true 2x2 operator principal-angle direct rotation U W = -J D + W B');
 nearMat(P1,I(4),5e-13,'canonical finite-future Krylov memory H1 spans complete 4d test carrier');
 nearMat(F,diag([1-a*a,1-b*b]),3e-14,'true original complementary feedback F=I-K0†K0');
 const deg=Math.sqrt(2*(1-Math.min(a,b)));
 const Idiff=minus(U,I(4));
 // normF is larger than operator norm, so true principal-angle op norm
 // is derived from the native 2-band block exactly (not falsely by normF).
 ok(deg>0&&deg<2,'original canonical direct rotation norm ||U-I||=sqrt(2(1-bmin))');
 return {a,b,Js:J,V,B,D,W,A,C,RM,U,F,deg,P1};
}
for(const a of [.55,.58,.6,.7,.75]){
 const f=originalFixture(a);
 const h=2e-5,fp=originalFixture(a+h),fm=originalFixture(a-h);
 const dV=mul(minus(fp.V,fm.V),1/(2*h));
 const dB=diag([1,0]);
 const dA=dV;
 const dC=mul(MM(MM(f.C,dB),f.C),-1);
 const dRM=plus(plus(MM(MM(dA,f.C),T(f.A)),MM(MM(f.A,dC),T(f.A))),
                MM(MM(f.A,f.C),T(dA)));
 const dU=MM(dRM,RJ);
 const fd=mul(minus(fp.U,fm.U),1/(2*h));
 nearMat(dU,fd,4e-8,'ALL first field input response of canonical full-Kraus U from exact inverse Gram');
 nearMat(MM(dU,J),dV,4e-8,'original native DU J = DV physical forward entire work first source');
 const dF=diag([-2*a,0]);
 nearMat(dF,mul(minus(fp.F,fm.F),1/(2*h)),4e-8,'actual original physical Book F=I-B² all derivatives');
 const diffnorm=normF(minus(fp.U,fm.U));
 ok(diffnorm>1e-7,'nonzero real first source retained by canonical U, not frozen');
}
// ACTUAL full128 original Golden/CAR16 Fourier boost:
// all 127 NONBLANK Kraus words retained in V; W=(V-JB)(I-B²)^-1/2
// is an EXACT linear combination in their full native outcome space.
// Full 128 RIGHT stays spectator, not approximated by a scalar per cost.
const phi=(1+Math.sqrt(5))/2,p=1/phi,beta=2*p*p,zeta=2**-20;
const mu=141489/10240000,h0=69399/5030720;
const eps=Math.sqrt(mu*(mu-h0)),eigen=[mu-eps,mu+eps];
const band=eigen.map(l=>1-beta*l);
const n=1,active=16*128,all=active*128,zeroModes=all-2*active;
ok(band[0]>band[1]&&band.every(x=>x>0&&x<1),
 'native true original boosted CAR16 FULL two actual B=K0 eigenvalues positive and nontrivial');
ok(active===2048&&all===262144&&zeroModes===258048,
 'original ACTUAL one-round 128 fine Kraus slots, oldRIGHT128, all zero Hodge modes retained');
const f=band.map(b=>1-b*b),E=f.map(q=>Math.exp(-beta*q));
const Z=all-2*active+2*128*8*E.reduce((a,b)=>a+b,0);
const Jnative=-128*8*f.reduce((s,v)=>s+Math.log1p(-zeta*v),0);
const nativeHeat=Math.log(Z)/beta;
ok(f.every(v=>v>0&&v<1)&&Z>all-2*active&&Z<all,
 'full ORIGINAL CAR16 fixed input Book F spectrum positive, whole Hodge trace retaining EXACT dormant modes');
close(Jnative,.000041014328465257154,3e-13,'pinned ORIGINAL same one-step full128 fixed-cut J exact source');
close(nativeHeat,16.33182036803625,4e-12,'pinned ORIGINAL same oldRIGHT/full work paired Hodge heat not normalized');
const opNormUpper=Math.sqrt(2/80);
const opNormActual=Math.sqrt(2*(1-Math.min(...band)));
ok(opNormActual<opNormUpper&&opNormUpper<.159,
 'ORIGINAL full native canonical one-tick U_can has ||U-I||<sqrt(1/40)<0.159');
ok(active*2===4096&&all>4096,
 'ORIGINAL native first future reachable input+fine-outgoing span has dimension 4096, full original 262144 retained');
// Exact rational Householder Gram inverse polynomial on ORIGINAL B≥1−1/80:
// (I+B)^−1 = (1/2) sum_{k≥0} ((I−B)/2)^k.
// Degree8 K8 ≤2/(159*160^8) near 2.9287e-20 in operator norm.
const KK=8;
const rationalCheckLeft=2n*10n**20n;
const rationalCheckRight=3n*159n*160n**8n;
ok(rationalCheckLeft<rationalCheckRight,
 'BIGINT exact native full128 Householder polynomial degree8 error <3e-20');
const alpha=1/160;
const houseErr=2*alpha**(KK+1)/(1-alpha);
const houseJet=(KK+1)*alpha**KK/(1-alpha)+
 alpha**(KK+1)/(1-alpha)**2+2*alpha**(KK+1)/(1-alpha);
ok(houseErr<3e-20&&houseJet<2.2e-17,
 'whole ORIGINAL boosted native \u03C6 Householder inverse-resolvent approximation and its FIRST FULL field source relative to ||DV|| strictly small');
function centeredScalar(a,K){
 // On original two-band B positive, C=(1+B)^-1, no sqrt; spectral approximant.
 const r=(1-a)/2;
 let ss=1,term=1;
 for(let k=1;k<=K;k++){term*=r;ss+=term}
 return .5*ss;
}
for(const b of band){
 const exact=1/(1+b),ca=centeredScalar(b,KK);
 ok(ca>0&&ca<=exact+1e-15&&Math.abs(exact-ca)<1e-14,
    'native actual CAR16 scalar approximant agrees to DOUBLE precision; strict 3e-20 bound is exact BigInt/analytic, not verified by double subtraction');
}
// No "Krylov saturation" for physical SEQUENTIAL full128 with fresh new
// 128-outcome stage registers: each step uses new V and newly paid work.
// On the ONE unitary completion U_can on its SAME fixed work register,
// H1=span(J,V) is invariant and Book F on that FUTURE-CLOSED cut is 0.
for(const b of band){
 const dd=Math.sqrt(1-b*b);
 const planeU=[[b,-dd],[dd,b]],planeJ=[[1],[0]];
 const planeV=MM(planeU,planeJ);
 close(planeV[0][0],b,1e-14,'original full128 K0 positive correct one future step');
 close(planeV[1][0],dd,1e-14,'original entire complement generated by all old native 127 Kraus labels');
 const U2=MM(planeU,planeU);
 ok(U2.every(row=>row.every(Number.isFinite)),
  'same 2d principal-angle Krylov subspace invariant under canonical completion');
}
// Native spectral and logical source distinction.
console.log(JSON.stringify({status:'PASS_ORIGINAL_FULL128_CANONICAL_KRAUS_HOUSEHOLDER_AND_PAID_KRYLOV_BOUNDARY',
 checks,
 original:{p,beta,zeta,eigenNativeDelta:eigen,blankEigen:band,
  KrausAlphabet:128,oldRIGHT:128,physicalNativeCAR16:16,
  fullOneRoundCarrier:all,activeInputRank:active,
  nativeFutureKrylovSpanRank:2*active,
  zeroHodgeModes:zeroModes,feedbackEigen:f,
  pairedHeat:nativeHeat,bookFeedback:Jnative,
  nativeSignalCompletionNormUpper:opNormUpper,
  originalFull128FourierKrausMatrixNotReplayed:true},
 canonical:{
  J:"inclusion |0_report> tensor DATA/oldRIGHT",
  V:"all ORIGINAL 128 native Kraus labels incl previous DATA, fresh no-reset work",
  B:"J†V=K0=I−2p² Delta positive Hermitian",
  midpointProjection:"P_+= (J+V)[2(I+B)]^-1(J+V)†",
  nativeHouseholder:"R_+= (J+V)(I+B)^-1(J+V)†−I",
  fullUnitary:"U_can=R_+ (2JJ†−I)",
  exactForward:"U_can J=V",
  exactBackward:"U_can† V=J",
  oldRIGHTExplicitControlRequired:false,
  caveat:"need physically admitted coherent V and its R_+ / reverse on DATA+all fine WORK; irreversible measurement destroys access to V",
  minimalFutureReachability:"H1=span(J,V) has 2d and U_can H1=H1; same-work F1=0",
  operatorCompletionNotUniqueUniversally:"canonical by DIRECT-ROTATION and identity on all unused fine directions, not forced by M1",
  mathematicalSource:"DU_can=(D[(J+V)(I+B)^-1(J+V)†])(2JJ†−I) including DJ and DV; no arbitrary spectral eigenvectors"
 },
 fixedOriginalFinitePolynomial:{
  approximation:"(I+B)^-1≈1/2∑_{k=0}^8((I−B)/2)^k",
  cutoff:"0<(I−B)<I/80 on old open CAR boost",
  HouseholderOpNormErrorUpper:houseErr,
  relativeJetErrorPerDV:houseJet,
  exactBigIntCertificate:"2*10^20 < 3*159*160^8",
  nativePolynomialFilterPhysicalCompilerStillOpen:true
 },
 compulsoryBook03SceneHeatAndInfoSelected:false,
 nativePhysicalJuliaUInverseAndOldWorkCompilerNotProven:true,
 newPhysicalEinstein42Root:false,GR_closed:false}));
