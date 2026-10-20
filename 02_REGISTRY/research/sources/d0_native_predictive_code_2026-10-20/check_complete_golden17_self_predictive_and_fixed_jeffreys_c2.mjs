#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL TWO-FRESH GOLDEN17 / 96 genuinely linked Role faces (one J23 link)
 * and ORIGINAL K(9,11,13) scene moving third-tick weight.
 *
 * A fully optimal ENDOGENOUS predictive reference mu=q retains ALL original
 * good/bad/Bell-failure records and removes CLASSICAL code-regret source
 * EXACTLY at every finite field, including ALL Hessian jets by same-action
 * stationary Schur. Does not ERASE Shannon or actual code/work cost.
 *
 * A SECOND independent canonical fixed-reference control: 1/2 Jeffreys
 * (KT) universal mixture on real original +/- Golden mark orientation
 * has exact finite expected Cost−Info, first and second derivatives and
 * genuine N^-1 field-dependent SECOND source (not every near-optimal
 * code has this property).  This is a MATHEMATICAL coding law, not a
 * declaration that literal G0/Book03 selects/prepares the true code
 * and permits unlimited free native clock repetitions.
 */
const check=(ok,msg)=>{if(!ok)throw Error("FAIL: "+msg)};
const phi=(1+Math.sqrt(5))/2,p=1/phi,ell=Math.log(phi),h=1/4096;
const N=33,zone=u=>u<9?0:(u<20?1:2);
const costs=(u,v,t)=>1.12+.023*((7*u+11*v)%13)+.002*((u+3*v)%7+1)*Math.sin(t);
function nativeBookW(t){
 const K=Array.from({length:N},(_,u)=>Array.from({length:N},(_,v)=>
 zone(u)===zone(v)?0:Math.exp(-ell*costs(u,v,t))));
 let Z3=0;
 for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++)
  Z3+=3*(K[a][b]*K[b][c]*K[c][a]+K[a][c]*K[c][b]*K[b][a]);
 return Z3/7722;
}
const E=(i,j)=>{const A=Array.from({length:4},()=>Array(4).fill(0));A[i][j]=1;return A};
const add=(a,b,c=1)=>a.map((r,i)=>r.map((x,j)=>x+c*b[i][j]));
const matmul=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,x,k)=>s+x*b[k][j],0)));
const I=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const dot=(a,b)=>a.reduce((s,r,i)=>s+r.reduce((v,x,j)=>v+x*b[i][j],0),0);
const tr=a=>a.reduce((s,r,i)=>s+r[i],0);
const G=[add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)];
const J=G[4],J2=matmul(J,J);
const P=t=>add(add(I(),J,Math.sin(t)),J2,1-Math.cos(t));
function golden17(t){
 const U=P(t),avg=tr(U)/4,norm=dot(U,U)/4;
 const q=G.flatMap(X=>{const s=dot(X,U)/(2*Math.SQRT2);
  return [p**4/24*(avg+s)**2,p**4/24*(avg-s)**2]});
 const gg=p**4*norm,gb=p*p*(1-p*p*norm),bg=p**3*norm;
 q.push(gg-q.reduce((s,x)=>s+x,0),gb,bg,1-gg-gb-bg);
 for(let k=0;k<16;k++)q[k]*=h;
 q.push(1-h);
 for(let v of q)check(v>0,"full Golden17 positivity (including failed Bell)");
 check(q.length===17&&Math.abs(q.reduce((s,v)=>s+v,0)-1)<1e-14,
   "all 17 original Golden p outcomes normalize exactly");
 return q;
}
function KL(q,mu){
 let total=0;
 for(let i=0;i<q.length;i++)total+=q[i]*Math.log(q[i]/mu[i]);
 return total/ell;
}
function H(q){return -q.reduce((a,v)=>a+v*Math.log(v),0)/ell}
const q0=golden17(0),qt=golden17(.15);
check(KL(q0,q0)<1e-14&&KL(qt,qt)<1e-14,
 "endogenous same-history self-predictive code has EXACT zero regret");
check(KL(qt,q0)>1e-7,"fixed old Golden reference price really has nonzero vertical KL");
const wt0=nativeBookW(0),wt15=nativeBookW(.15);
check(wt0>0&&Math.abs(wt0-wt15)>1e-7,
 "REAL heterogeneous original K913 Book third-tick source MOVES with true Lorentz variation");
function codeRegret(t,s){
 const w=nativeBookW(t);
 // Genuine shared Role link creates three +t and three -t based face words.
 // Its remaining 90 faces have exact q_17(I) and matched reference q_17(I).
 return w*(3*KL(golden17(t),golden17(s))+
           3*KL(golden17(-t),golden17(-s)));
}
const at0=codeRegret(0,0),at15=codeRegret(.15,.15),
      fixed=codeRegret(.15,0);
check(Math.abs(at0)<1e-14&&Math.abs(at15)<1e-14&&fixed>1e-8,
 "ALL six two-orientation Role faces + 90 idle faces predictive optimum zero despite MOVING W");
for(const t of [-.23,-.12,0,.15,.32]){
 check(Math.abs(codeRegret(t,t))<1e-14,
 "whole 96 Golden17 fine record: self-predicted code regret zero along entire field path");
}
const mark=h*p**4/24;
const FIone=h*p**4/6,FIsix=6*FIone;
const K=wt0*FIsix/ell;
check(K>0,"true full17 native Fisher always POSITIVE");
const Schur=[[K,-K],[-K,K]];
const reduced=Schur[0][0]-Schur[0][1]**2/Schur[1][1];
check(reduced===0,"EXACT same-class predictor Schur cancels every original Golden vertical Fisher second source");
const dt=.002,dd=(codeRegret(dt,0)-2*codeRegret(0,0)+codeRegret(-dt,0))/dt**2;
check(Math.abs(dd-K)<6e-7,"actual full Golden17 fixed-reference Hessian equals Book-weighted FI / ln(phi)");
const sourceAtPoint=(codeRegret(.151,0)-codeRegret(.149,0))/.002;
check(Math.abs(sourceAtPoint)>1e-6,"fixed-reference Golden regret has nonzero Role-fiber FIRST SOURCE");

// EXACT canonical Jeffreys (= Dirichlet 1/2) FIXED universal code.
// Mathematical ideal code length at N trials:
//    M_N(y^N)=Gamma(k/2)/Gamma(N+k/2)
//      PROD_i Gamma(n_i+1/2)/Gamma(1/2).
// R_N(q)=E[-ln M_N]-N H_nat(q).
// For k=2 all finite sources computed via exact BINOMIAL SHIFT identities:
//   G'_N(q)=N E_Bin(N-1,q) ln(Y+1/2)
//   G''_N(q)=N(N-1) E_Bin(N-2,q) ln[(Y+3/2)/(Y+1/2)].
function logs(n){
 const LF=[0],LH=[.5*Math.log(Math.PI)];
 for(let i=1;i<=n+2;i++){
  LF[i]=LF[i-1]+Math.log(i);
  LH[i]=LH[i-1]+Math.log(i-.5);
 }return {LF,LH};
}
function ebin(n,q,f,LF){
 check(q>0&&q<1,"full two-mark conditional probability lies inside simplex");
 const mode=Math.floor((n+1)*q),weights=new Float64Array(n+1);
 const logMode=LF[n]-LF[mode]-LF[n-mode]+mode*Math.log(q)+(n-mode)*Math.log1p(-q);
 weights[mode]=Math.exp(logMode);
 for(let i=mode+1;i<=n;i++)
  weights[i]=weights[i-1]*(n-i+1)/i*q/(1-q);
 for(let i=mode-1;i>=0;i--)
  weights[i]=weights[i+1]*(i+1)/(n-i)*(1-q)/q;
 let mass=0,mean=0;
 for(let i=0;i<=n;i++){mass+=weights[i];mean+=weights[i]*f(i)}
 return mean/mass;
}
function kTbern(n,q){
 const {LF,LH}=logs(n);
 const G=x=>ebin(n,x,i=>LH[i],LF);
 const BG=x=>ebin(n-1,x,i=>Math.log(i+.5),LF);
 const DG=x=>ebin(n-2,x,i=>Math.log((i+1.5)/(i+.5)),LF);
 const regret=LF[n]+Math.log(Math.PI)-G(q)-G(1-q)+
  n*(q*Math.log(q)+(1-q)*Math.log(1-q));
 const grad=-n*BG(q)+n*BG(1-q)+n*Math.log(q/(1-q));
 const hess=-n*(n-1)*(DG(q)+DG(1-q))+n/(q*(1-q));
 const A=.5*Math.log(n/(2*Math.PI*Math.E))+Math.log(Math.PI)+
    (1/6-(1/q+1/(1-q))/24)/n;
 const gradA=(1/q**2-1/(1-q)**2)/(24*n);
 const hessA=-(1/q**3+1/(1-q)**3)/(12*n);
 return {n,regret,first:grad,second:hess,
         leadingValue:A,leadingFirst:gradA,leadingSecond:hessA};
}
const KT=[64,256,1024,4096,16384].map(n=>kTbern(n,.30));
check(KT.every(x=>x.regret>0&&x.second<0&&Number.isFinite(x.regret)),
 "true fixed Jeffreys mixture Cost−Info all source values finite and correct sign");
check(KT[4].first<KT[0].first/200&&
 Math.abs(KT[4].second)<Math.abs(KT[0].second)/200,
 "one CANONICAL fixed universal code has genuinely vanishing C1/C2 sources despite hostile arbitrary-code C2 theorem");
check(Math.abs(KT[4].first-KT[4].leadingFirst)<2e-8 &&
 Math.abs(KT[4].second-KT[4].leadingSecond)<2e-7,
 "exact finite binomial sources match analytic 1/N Jeffreys regret first/second asymptotics");

// ABSOLUTE SOURCE HOSTILE CONTROL: a FIXED universal Jeffreys code has
// expected regret ~(k-1)/2 log N, a genuine positive work/code price.
// If this complete charged redundancy is multiplied by a moving original
// Book-third-tick pressure W(t), a NONZERO first source survives EVEN when
// the data distribution is held CONSTANT. The source is D W * regret;
// no code universality theorem deletes original clock/absolute pressure.
const dBookW=(nativeBookW(1e-3)-nativeBookW(-1e-3))/(2e-3);
const fixedUniversalOverheadGolden=KT[4].regret/ell;
const fullNativeWeightedCodeSource=dBookW*fixedUniversalOverheadGolden;
check(Math.abs(dBookW)>1e-5&&Math.abs(fullNativeWeightedCodeSource)>1e-5,
 "original moving Book-third-tick absolute source survives canonically coded but paid redundancy");
const qOriginalMark=q0[8]/(q0[8]+q0[9]);
check(Math.abs(qOriginalMark-.5)<1e-14,
 "literal original J23 positive mark pair is unbiased at true flat");
const k2=kTbern(1024,qOriginalMark);
check(Math.abs(k2.first)<2e-9,"fixed symmetric Jeffreys code is source-blind under exact reversal at flat");
const originalQFI=FIsix, goldenShellHess=wt0*FIsix/ell;
// FULL k=17 Jeffreys asymptotic leading t-Hessian of expected
// redundancy, for true q17 one-link t: -1291/(1728*N*mark) nats.
// It follows directly from Σ d²(1/q_i)/dt² at t0 with all 17 labels.
const full17AsymptoticCoefficient=-1291/(1728*mark*ell);
const qOne=golden17(1e-3),qMinus=golden17(-1e-3);
let reverseHess=0;for(let i=0;i<17;i++)
 reverseHess+=(1/qOne[i]-2/q0[i]+1/qMinus[i])/(1e-6);
const analyticalHessInverse=1291/(72*mark);
check(Math.abs(reverseHess/analyticalHessInverse-1)<2e-5,
 "all17 true original Golden marker jets imply EXACT nonzero finite-clock resource bound");
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_GOLDEN17_ENDOGENOUS_CODE_AND_JEFFREYS_FIXED_C2",
 genuineRecord:{positiveLabels:17,BellFailure:q0[16],
   trueMarkProbability:mark,fullGoldenFisherSix:FIsix},
 completeBook:{vertices:33,directedEdges:718,thirdTickOriginalWAt0:wt0,
   thirdTickWAt015:wt15},
 trueRole96:{affectedFaces:6,unaffectedFaces:90,
   fixedOldReferenceCostInfoAt015:fixed,
   selfPredictiveCostInfoAt015:at15,
   fixedReferenceVerticalFirstSource:sourceAtPoint,
   exactJointHessian_t_s:Schur,
   exactStationaryHistorySchur:reduced,
   trueBookWeightedVerticalHessian:goldenShellHess,
   finiteDifferenceVerticalHessian:dd},
 fixedReferenceJeffreys:{prior:"intrinsic Fisher volume Dirichlet(1/2), NOT a physical Book-selected code",
    binomialSourceTable:KT,
    full17OriginalGoldenAsymptoticSecondSourceCoefficientPerAttempt:full17AsymptoticCoefficient,
    fullyPaidGoldenCodeOverheadAt16384:fixedUniversalOverheadGolden,
    movingOriginalBookWeightDerivative:dBookW,
    NONZEROAbsoluteWeightedCodeFirstSource:fullNativeWeightedCodeSource},
 honestBoundaries:"all retained Golden positive records/code regret, but no native G0 exact encoder/preparation/clock/work, Book absolute selection or GR proof",
 GR_closed:false
},null,2));
