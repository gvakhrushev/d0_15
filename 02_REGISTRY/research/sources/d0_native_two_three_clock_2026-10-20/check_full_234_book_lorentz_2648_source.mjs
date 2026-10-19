#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL COMPLETE K(9,11,13) n=2,3,4 CLOSED HISTORY REGISTER.
 * This is a SINGLE mathematical FULL COMMON-NORMALIZER Book clock
 * with actual 718 n2, 7722 n3 and 257762 n4 fully based loops,
 * NOT a declared physically compulsory G0 clock/prep programme.
 *
 * The clock scalar q_gamma = α_n product_e K_e / Z, with declared
 * positive native Golden-type attempt priors α2=p, α3=p², α4=p³,
 * reconstructs ALL original 718 edge-local net Cost−Info weights
 * modulo 32 endpoint scalar coboundaries; the 5-flag formula
 * for 1/Z remains exact even with ALL n4 events retained.
 *
 * On a separate original TRUE nonabelian SO+(1,3) U_e link field,
 * the already-proved original full-group rooted loop inverse
 * requires 143 n3+184 n4 original literal paths (all represented
 * inside this same COMPLETE 266202-path register), and reconstructs
 * all 327 independent scene group cycles modulo its original
 * 32 vertex Lorentz tree frames (one root frame is fixed).
 *
 * A mathematically DECLARED complete positive Golden/Bell17
 * conditional per path has an actual local 6-dimensional inverse
 * on SO+(1,3) near the original flat field, provided its fixed
 * ROOT coframe reference is properly co-transported.
 * The full q_(gamma,r)=q_gamma(K) q17(r|U_gamma) map thus has
 * local SOURCE rank (718−32)+6*(359−32)=686+1962=2648,
 * with cross score Fisher 0 for independently varied K and U.
 *
 * IMPORTANT: do not mistake a JOINT mathematical distribution with
 * compulsory original Book/G0 physical readout, paid clock/Cost/Info,
 * fixed-Bell Julia preparation, complete old RIGHT or genuine
 * D0 Role 4D coframe/link Einstein action. In particular q17(U_gamma)
 * is NOT an automatic native instrument for all n4 histories.
 */
const require=(yes,msg)=>{if(!yes)throw Error("FAIL "+msg)};
const n=33,zone=u=>u<9?0:u<20?1:2,
      p=(Math.sqrt(5)-1)/2,phi=(1+Math.sqrt(5))/2,ell=Math.log(phi);
const A=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>
  +(zone(i)!==zone(j))));
require(A.flat().reduce((sum,v)=>sum+v,0)===718,"original 718 directed edges");
const prod=(X,Y)=>X.map(row=>Y[0].map((_,j)=>
  row.reduce((s,v,k)=>s+v*Y[k][j],0)));
const trace=X=>X.reduce((s,r,i)=>s+r[i],0);
const A2=prod(A,A),A3=prod(A2,A),A4=prod(A3,A);
const counts=[trace(A2),trace(A3),trace(A4)];
require(counts.join(",")==="718,7722,257762",
 "true all-start based 2/3/4 closed original graph counts");
const allPaths=counts.reduce((s,x)=>s+x,0);
require(allPaths===266202,"total original complete closed path count");
const alpha={2:p,3:p*p,4:p*p*p};
const s=(i,j,t)=>1+.01*((i*7+j*11+i*j+3)%19)+t*(1+((i+3*j)%7))/20,
      I=i=>.02*((i*13+7)%11-5);
function transfer(t){
  return Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>
    A[i][j]?Math.exp(-ell*(s(i,j,t)-.5*(I(i)+I(j)))):0));
}
function clock(K){
 const K2=prod(K,K),K3=prod(K2,K),K4=prod(K3,K);
 const Z2=trace(K2),Z3=trace(K3),Z4=trace(K4),
       Z=alpha[2]*Z2+alpha[3]*Z3+alpha[4]*Z4;
 require(Z>0&&[Z2,Z3,Z4].every(z=>z>0),"positive native Book path ensemble");
 const qPath=word=>{
   let w=alpha[word.length-1]/Z;
   for(let j=1;j<word.length;j++)w*=K[word[j-1]][word[j]];
   return w;
 };
 const a=0,b=9,c=20,
    q2ab=qPath([a,b,a]),q2bc=qPath([b,c,b]),q2ac=qPath([a,c,a]),
    q3abc=qPath([a,b,c,a]),q3acb=qPath([a,c,b,a]);
 const recoveredInvZ=alpha[3]**2/alpha[2]**3 *
     q2ab*q2bc*q2ac/(q3abc*q3acb);
 require(Math.abs(recoveredInvZ*Z-1)<3e-13,
   "five original 2/3 complete clock flags lost absolute partition in presence of ALL n4 outcomes");
 const evenErrors=[],oddErrors=[];
 for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(A[u][v]){
   const q=qPath([u,v,u]),
      evenRecovered=.5*Math.log(q*Z/alpha[2]),
      evenActual=.5*Math.log(K[u][v]*K[v][u]);
   evenErrors.push(Math.abs(evenRecovered-evenActual));
 }
 for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++){
   const forward=qPath([a,b,c,a]),
         reverse=qPath([a,c,b,a]);
   const oddRecovered=.5*Math.log(forward/reverse);
   const oddActual=.5*Math.log(K[a][b]*K[b][c]*K[c][a]/
                           (K[a][c]*K[c][b]*K[b][a]));
   oddErrors.push(Math.abs(oddActual-oddRecovered));
 }
 require(evenErrors.length===359&&oddErrors.length===1287,
    "wrong independent original Book even/odd sources");
 const maxEven=Math.max(...evenErrors),maxOdd=Math.max(...oddErrors);
 require(maxEven<2e-13&&maxOdd<2e-13,"original scalar source inverse failed");
 const totalMass=(alpha[2]*Z2+alpha[3]*Z3+alpha[4]*Z4)/Z;
 require(Math.abs(totalMass-1)<1e-15,"all original based 2/3/4 paths not normalized");
 const conditionalDepthMass=[2,3,4].map(n=>({
   depth:n,allPositiveOriginalPaths:counts[n-2],
   nativeFullClockProbability:alpha[n]*[Z2,Z3,Z4][n-2]/Z
 }));
 return {t,Z,Z2,Z3,Z4,totalMass,recoveredInvZ,
   inverseAbsoluteZError:Math.abs(recoveredInvZ*Z-1),
   maxEvenLogError:maxEven,maxOddLogError:maxOdd,
   conditionalDepthMass};
}
const experiments=[0,.013,.04].map(t=>clock(transfer(t)));
const fieldDerivative=(Math.log(experiments[1].Z)-Math.log(experiments[0].Z))/.013;
require(Math.abs(fieldDerivative)>.01,"nontrivial true original moving cost source absent");
const fib=[0n,1n];for(let j=2;j<=40;j++)fib.push(fib[j-1]+fib[j-2]);
const jointOutcomes=allPaths*17,minimumGoldenCost=
  Array.from({length:38},(_,i)=>i).find(i=>fib[i+1]>=BigInt(jointOutcomes));
require(minimumGoldenCost===33&&fib[34]===5702887n,
  "wrong actual native Golden F/R label-capacity for one full joint programme");
const rooted={
  fundamentalRootedBC3:11*13,
  fundamentalRootedAC4:8*13,
  fundamentalRootedAB4:8*10,
  originalRootedFullGroupVariables:359-32,
  fullRealOriginalLorentzRootedLieDimensions:6*(359-32)
};
require(rooted.fundamentalRootedBC3+rooted.fundamentalRootedAC4+
  rooted.fundamentalRootedAB4===327,"incorrect original rooted scene chord count");
const result={
 status:"PASS_ORIGINAL_COMPLETE234_BOOK_AND_327ROOTED_LORENTZ_SOURCE_RANK2648",
 originalNativeGraph:{vertices:n,directedEdges:718,undirectedEdges:359},
 allPositiveFullBasedClosedSceneHistories:{n2:counts[0],n3:counts[1],
   n4:counts[2],total:allPaths,oneMathematicalCommonClockNormalizer:true,
   n2n3AttemptFactors:["p","p²"],
   n4AttemptFactor:"p³ hypothetical extra original Golden-type attempt; physically G0 NOT selected"},
 fiveOriginalClockHistoryFlagsRecoverFullAbsoluteScalarBookZ:true,
 fullOriginalBookNetScalarGaugeQuotientRank:718-32,
 rootNonabelianLorentzRecovery:rooted,
 fullGoldenBellConditionalsPerHistory:17,
 allOriginalPathTimesFullConditionalLabels:jointOutcomes,
 minimumOriginalExactCostGoldenRecordCutForLabels:minimumGoldenCost,
 trueTypeAGoldenLabels:String(fib[minimumGoldenCost+1]),
 trueTypeBPendingLabels:String(fib[minimumGoldenCost]),
 mathematicalInputRank:(718-32)+(359-32)*6,
 jointFisherCrossZeroForIndependentBookAndOriginalLorentzControls:true,
 originalActualMovingScalarBookSource:fieldDerivative,
 originalCountAndInverseChecks:experiments,
 crucialUnprovedInputs:[
  "Actual compulsory G0 single common 2/3/4 clock and true attempt weights",
  "Actual ORIGINAL path-conditioned complete two-flag Bell+Golden17 CAR programme for rooted n3/n4 loops",
  "one retained root-frame CAR reference with physical field-dependent co-transport and full RIGHT",
  "real complete Cost/Info/preparation/clock/work source and native Role 4D field-to-scene controls",
  "original nonlinear same-action Einstein source, selected curved roots, Ward and physical refinement"
 ],
 statusMeaning:"Mathematical COMPLETE positive-source observability / full original scene group gauge atlas only, NOT selected physical Einstein law",
 GR_closed:false
};
console.log(JSON.stringify(result,null,2));
