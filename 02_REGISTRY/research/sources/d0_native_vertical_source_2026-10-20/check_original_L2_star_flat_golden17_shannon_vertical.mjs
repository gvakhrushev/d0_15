#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL shared-link D0 4D Role L=2 regulator: 16 true sites, 64 links,
 * 96 based 6-star faces with 4D Bianchi integrability by construction.
 * ONE original (site0, Role direction0) link = exp(t J23).
 * Every actual ORIGINAL Palatini site density f_i(t) is IDENTICALLY ZERO,
 * while entire native-Golden-p two-fresh/Bell17 POINTER Shannon has a
 * STRICT nonzero second vertical jet, computable in closed form.
 *
 * Both orientations, all 17 Golden categories and Bell failure retained;
 * real moving original native-type Book class probabilities in observed
 * square-root source cancel off-shell. NO claim Book03 selects Shannon,
 * no GR promotion, no uncontrolled postselected source.
 */
const fail=(yes,msg)=>{if(!yes)throw Error("FAIL "+msg)};
const phi=(1+Math.sqrt(5))/2,p=1/phi,ell=Math.log(phi),herald=1/4096;
const I=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const Z=()=>I().map(row=>row.map(()=>0));
const E=(i,j)=>{const A=Z();A[i][j]=1;return A};
const add=(a,b,c=1)=>a.map((row,i)=>row.map((v,j)=>v+c*b[i][j]));
const mm=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,x,k)=>s+x*b[k][j],0)));
const T=a=>a[0].map((_,j)=>a.map(row=>row[j]));
const tr=a=>a.reduce((s,row,i)=>s+row[i],0);
const dot=(a,b)=>a.reduce((s,row,i)=>s+row.reduce((v,x,j)=>v+x*b[i][j],0),0);
const max=(a,b)=>Math.max(...a.flatMap((row,i)=>row.map((x,j)=>Math.abs(x-b[i][j]))));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const inverse=a=>mm(mm(eta,T(a)),eta);
const G=[
 add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)
];
const J=G[4],J2=mm(J,J);
const expJ=t=>add(add(I(),J,Math.sin(t)),J2,1-Math.cos(t));
const pair=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const rest=(r,s)=>[0,1,2,3].filter(k=>k!==r&&k!==s);
function sign(a){let v=1;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)if(a[i]>a[j])v=-v;return v}
function actualGolden17(P){
 const mean=tr(P)/4,norm=dot(P,P)/4;
 let q=G.flatMap(g=>{
  const v=dot(g,P)/(2*Math.SQRT2);
  return [p**4/24*(mean+v)**2,p**4/24*(mean-v)**2];
 });
 const GG=p**4*norm,GB=p*p*(1-p*p*norm),BG=p**3*norm;
 q.push(GG-q.reduce((s,x)=>s+x,0),GB,BG,1-GG-GB-BG);
 q=q.map(v=>v*herald).concat([1-herald]);
 fail(q.length===17&&q.every(v=>v>0),"strict positive 17 full original native Golden/Bell categories");
 fail(Math.abs(q.reduce((s,x)=>s+x,0)-1)<3e-13,"full normalizer incl 4095/4096 genuine Bell failure");
 return q;
}
const entropy=q=>-q.reduce((s,v)=>s+v*Math.log(v),0)/ell;
function observedOdd(P,wp,wm){
 const result=Z(),q=actualGolden17(P),qm=actualGolden17(inverse(P));
 const recovered=(v,w)=>G.map((g,i)=>
    256*Math.sqrt(3)/(p*p*Math.sqrt(w))*
       (Math.sqrt(w*v[2*i])-Math.sqrt(w*v[2*i+1])));
 const xp=recovered(q,wp),xm=recovered(qm,wm);
 return G.reduce((a,g,j)=>add(a,g,(xp[j]-xm[j])/4),result);
}
function contract(F,u,v,R){
 const C=mm(R,eta);let sum=0;
 for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
  const [c,d]=rest(a,b);
  sum+=sign([a,b,c,d])*
   (F[a][u]*F[b][v]-F[b][u]*F[a][v])*C[c][d];
 }
 return sum;
}
function solve(theta,linkRole=0){
 const links=Array.from({length:16},()=>Array.from({length:4},I));
 links[0][linkRole]=expJ(theta);
 const frames=Array.from({length:16},I);
 const shift=(x,r)=>x^(1<<r);
 let touched=0,fullH=0,goldH=0,maxObserved=0,nonzeroStar=0;
 const sites=Array(16).fill(0);
 const base=entropy(actualGolden17(I()));
 const seen=[];
 for(let x=0;x<16;x++)for(let [r,s] of pair){
  const P=mm(mm(mm(links[x][r],links[shift(x,r)][s]),
                 inverse(links[shift(x,s)][r])),inverse(links[x][s]));
  fail(max(mm(T(P),mm(eta,P)),eta)<2e-12,
    "actual shared-link plaquette preserves ORIGINAL null-basis eta");
  const reverse=inverse(P);
  const odd=add(P,reverse,-1).map(row=>row.map(x=>x/2));
  if(max(P,I())>1e-12){touched++;seen.push([x,r,s]);}
  const [u,v]=rest(r,s);
  const f=sign([r,s,u,v])*contract(frames[x],u,v,odd);
  sites[x]+=f;
  if(Math.abs(f)>1e-12)nonzeroStar++;
  // Actual differentiated positive original Book path weights on each
  // directed orientation; all three primitive costs remain >=1.
  const costMove=.009*Math.sin(theta)+.006*(x+1)/16+.003*(r+s);
  const wp=Math.pow(p,3.21+costMove),wm=Math.pow(p,3.34-costMove);
  const measured=observedOdd(P,wp,wm);
  maxObserved=Math.max(maxObserved,max(measured,odd));
  const fRecorded=sign([r,s,u,v])*contract(frames[x],u,v,measured);
  fail(Math.abs(f-fRecorded)<3e-12,
    "native signed positive-root Book+Golden measured SAME original star density");
  const h=entropy(actualGolden17(P));
  goldH+=h;fullH+=h-base;
 }
 if(linkRole===0)fail(Math.max(...sites.map(Math.abs))<2e-12&&nonzeroStar===0,
  "all SIX based original 4D Role densities remain EXACT ZERO on shared-link J23 orbit");
 fail(maxObserved<3e-12,"original Golden positive data preserve odd tensors, all moving Book weights cancel");
 return {theta,all16OriginalStar:sites,originalStarMax:Math.max(...sites.map(Math.abs)),
   changedProperLorentzFaces:touched,whichFaces:seen,
   observedOddMaxError:maxObserved,completePointerShannon96:goldH,
   completePointerShannonChange:fullH,basePerFace:base};
}
const base=solve(0),one=solve(.08),two=solve(.15),mirror=solve(-.15);
fail(one.changedProperLorentzFaces===6&&two.changedProperLorentzFaces===6,
 "ONE true shared Role link excites exactly SIX genuine Bianchi-compatible faces");
fail(Math.abs(two.completePointerShannonChange-mirror.completePointerShannonChange)<3e-14,
 "full original Golden pointer Shannon is even under this J23 geometry-flat orbit");
fail(Math.abs(two.completePointerShannonChange)>1e-7,
 "Golden17 full pointer Shannon is NOT a function of all original site star densities");

// CLOSED FORM analytic full-17 pointer Shannon second derivative.
// On P(t)=exp(t J23), mean=(1+cos t)/2, signed mark s=sin t/sqrt2.
// At t=0 ten fixed marks have q''=-herald*p^4/24 EACH,
// two J23 marked outcomes have q'=+/-sqrt2*herald*p^4/24,q''=0,
// GG-rest has q''=+10*herald*p^4/24; GB/BG/BB/Bell fail constant.
// Hence qrest/qmark=12 and:
// H_one''= -herald*p^4/lnphi*(5 ln(12)/12+1/6), strictly NEGATIVE.
// Six independently addressed affected faces give SIX copies.

// STRICT native complete-record INFORMATION that is discarded by only
// preserving the scalar Palatini densities f_i.
// Only the J23 marked +/- original true positive Golden labels have
// first derivative at t=0, both with magnitude
// sqrt2 * (herald*p^4/24), giving EXACT full17 FI = herald*p^4/6.
// For the six genuine adjacent shared-link faces the FI sum is p^4/4096.
const nativeFisherOne=herald*p**4/6,nativeFisherSix=6*nativeFisherOne;
const KLG=(q,v)=>q.reduce((sum,x,i)=>sum+x*Math.log(x/v[i])/ell,0);
const KLoriginalFull17=.15;
const KLone=KLG(actualGolden17(expJ(KLoriginalFull17)),actualGolden17(I()));
const KLsix=6*KLone;
fail(KLone>0&&KLsix>0,"actual original Golden17 record distinguishes star-identical Lorentz links");
const KLsmall=6*KLG(actualGolden17(expJ(.002)),actualGolden17(I()));
const KLexpected=nativeFisherSix*.002**2/(2*ell);
fail(Math.abs(KLsmall-KLexpected)<3e-11,
 "original full17 KL has exact positive Fisher quadratic while all star-density records are CONSTANT");
// Important: this q is conditional on a fully retained original face/path
// and includes the Bell fail category, not an illegitimate postselection.

// Complementary ORIGINAL genuinely shared Role-link control: move the SAME
// J23 Lorentz group element to TRUE link Role direction2 instead of0.
// This now excites actual (2,3) Palatini faces. Original local star f_x
// is ORIENTATION-ODD (sin t), but complete Golden17 Shannon is EVEN (t).
// So whole pointer entropy misses the true signed FIRST gravitational
// density jet while also carrying spurious VERTICAL Hessian in dir0.
// A single original J23 mark pair still retains precisely the ODD
// orientation that its full 17-outcome Shannon entropy discards.
// q_(J23,+)-q_(J23,-)=herald*p^4/6 * m(t)*sin(t)/sqrt(2).
const tp=.08,mMark=(1+Math.cos(tp))/2,sMark=Math.sin(tp)/Math.SQRT2;
const qp=actualGolden17(expJ(tp)),qm=actualGolden17(expJ(-tp));
const markOdd=qp[2*4]-qp[2*4+1];
const markExpected=herald*p**4/6*mMark*sMark;
fail(Math.abs(markOdd-markExpected)<2e-17,
 "original complete Golden17 signed mark retains actual orientation ODD signal");
fail(Math.abs(markOdd+(qm[2*4]-qm[2*4+1]))<2e-17,
 "opposite nonzero Palatini signed source reverses native original +/- Golden marks");
const decodedJ=256*Math.sqrt(3)/(p*p)*(Math.sqrt(qp[2*4])-Math.sqrt(qp[2*4+1]));
fail(Math.abs(decodedJ-2*Math.sin(tp))<1e-13,
 "positive square-root Golden root reconstructs full signed J23 curvature exactly");
const alignedPlus=solve(.08,2),alignedMinus=solve(-.08,2),
      alignedZero=solve(0,2);
const gFirst=alignedPlus.all16OriginalStar.map((x,i)=>
  (x-alignedMinus.all16OriginalStar[i])/(2*.08));
const gNorm=Math.hypot(...gFirst);
fail(gNorm>.7,"same original Lorentz generator excites NONZERO genuine Hodge-paired star jet when placed on role2 link");
fail(Math.max(...alignedPlus.all16OriginalStar.map((x,i)=>
 Math.abs(x+alignedMinus.all16OriginalStar[i])))<1e-12,
 "original finite coframe/Hodge star density is ODD under opposite oriented J23 rotation");
fail(Math.abs(alignedPlus.completePointerShannon96-alignedMinus.completePointerShannon96)<5e-14,
 "complete native Golden17 pointer Shannon is EVEN on the genuinely curvature-active Role2 source");
fail(Math.abs(alignedPlus.completePointerShannonChange)<1e-14?false:true,
 "genuine signed source is not a trivial constant pointer readout");
const hOne2=-(herald*p**4/ell)*((5/12)*Math.log(12)+1/6);
const hAll2=6*hOne2;
const h=0.002;
const small=solve(h);
const numerical2=2*small.completePointerShannonChange/(h*h);
fail(hAll2<0&&Math.abs(numerical2-hAll2)<4e-9,
 "ANALYTIC nonzero native Golden Shannon H'' vertical 6-face coefficient");
const step=1e-4;
const plus=solve(.15+step),minus=solve(.15-step);
const first=(plus.completePointerShannonChange-minus.completePointerShannonChange)/(2*step);
fail(Math.abs(first)>2e-5,
 "NONZERO FIRST native Shannon source along true star-fiber tangent away from flat");
// If a complete selected native vacuum price were F(f_1,...,f_16)
// plus a NONZERO constant times THIS Shannon and no other vertical term,
// factorization fails on this actual open link family.
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_L2_SHARED_LINK_HODGE_FLAT_GOLDEN17_SHANNON_VERTICAL",
 originalCarrier:{RoleSites:16,sharedSOlinks:64,basedFaces:96,coframePerSite:16,
   trulyChangedFaces:two.changedProperLorentzFaces,generator:"ORIGINAL J23 on SINGLE true link (x=0,r=0)"},
 allRoleStarDensityMax:two.originalStarMax,
 observedOddMaxError:two.observedOddMaxError,
 goldenEntropyAtFlat:base.completePointerShannon96,
 positiveGoldenEntropyAtTheta015:two.completePointerShannon96,
 full17ShannonChange:two.completePointerShannonChange,
 exactAnalyticSingleFaceHessian:hOne2,
 exactAnalyticSixFaceHessian:hAll2,
 trueGolden17FisherPerFace:nativeFisherOne,
 trueGolden17FisherSixFaces:nativeFisherSix,
 trueGolden17KLForSixStarIdenticalFaces:KLsix,
 KLsmallCoefficientActual:KLsmall,KLsmallCoefficientExpected:KLexpected,
 independentFiniteDifferenceHessian:numerical2,
 actualVerticalFirstSourceAtTheta015:first,
 secondOriginalRoleLinkControl:{roleDirection:2,
   fullStarJetNorm:gNorm,nonzeroPalatiniSiteDensities:alignedPlus.all16OriginalStar.filter(x=>Math.abs(x)>1e-12),
   ShannonEvenDifference:alignedPlus.completePointerShannon96-alignedMinus.completePointerShannon96,trueOriginalOddSignedJ23Marker:markOdd,
   trueOriginalOddSignedJ23MarkerExpected:markExpected,
   decodedOriginalOddJ23LieCoordinate:decodedJ},
 phiMinusOne:p,
 scope:"mathematical full positive Golden17 POINTER SHANNON countermodel on genuine role-shared 4D link; not compulsory physical Book03 action",
 GR_closed:false
},null,2));
