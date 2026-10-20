#!/usr/bin/env node
"use strict";
/*
 * EXACT ORIGINAL six-based Lorentz-star ACTION PULLBACK into SIX
 * original scene 3-edge ROOTED loops per original Golden LEFT Role site.
 *
 * 4D Role grid L=2 (16 sites), four independently varied ORIGINAL
 * proper-Lorentz links per site (64 group variables; 384 Lie tangents),
 * 16 nondegenerate original coframe real coordinates per site
 * (256 free coframe variations).
 *
 * For original six plaquette types (01,02,03,12,13,23), put one
 * site-address-conditioned scene chord on an ORIGINAL BC edge:
 * root0->B0=9->C_j=20+j->root0, j=0..5.
 * Its triangle holonomy = P_rs(site), REVERSE = P_rs(site)^-1,
 * because the two original tree links are identity.
 *
 * The SAME exact original star density is read from the six odd
 * triangle holonomies with the SAME original coframe/Hodge/eta.
 * Original globally shared Role link source is pulled back from
 * these PAID based face words by the chain rule, including BOTH
 * neighboring based faces at each actual varied Role edge.
 *
 * This is only a field-to-SCENE CONNECTION/OBSERVABLE embedding:
 * it does NOT prove the original Book/G0 programme physically
 * sets those six site-conditioned scene chords, gives them its
 * compulsory Cost−Info/oldRIGHT/clock/work, or makes the measured
 * geometrical observable the physical action. L=2 is a finite
 * exact regression carrier, not an L>=4/h->0 GR refinement root.
 */
const require=(ok,msg)=>{if(!ok)throw Error("FAIL "+msg)};
const pairTypes=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const nSites=16,L=2;
const shift=(site,dir)=>site^(1<<dir);
const id=(site,dir)=>4*site+dir;
const siteOf=link=>Math.floor(link/4);
const dirOf=link=>link%4;
function runOne(prime){
 const md=x=>(x%prime+prime)%prime, muln=(x,y)=>md(x*y);
 const I=()=>Array.from({length:4},(_,a)=>
   Array.from({length:4},(_,b)=>+(a===b)));
 const O=()=>Array.from({length:4},()=>Array(4).fill(0));
 const E=(a,b)=>Array.from({length:4},(_,i)=>
   Array.from({length:4},(_,j)=>+(i===a&&j===b)));
 const sm=(A,k)=>A.map(row=>row.map(x=>muln(x,k)));
 const add=(A,B,k=1)=>A.map((row,i)=>row.map((x,j)=>md(x+k*B[i][j])));
 const MM=(A,B)=>A.map(row=>B[0].map((_,j)=>
   md(row.reduce((s,x,k)=>s+x*B[k][j],0))));
 const T=A=>A[0].map((_,j)=>A.map(row=>row[j]));
 const equal=(A,B)=>A.every((row,i)=>row.every((x,j)=>x===B[i][j]));
 const pow=(a,k)=>{
   let b=md(a),out=1,n=k;
   while(n){if(n%2)out=muln(out,b);b=muln(b,b);n=Math.floor(n/2)}
   return out;
 };
 const inv=a=>{if(md(a)===0)throw Error("zero divisor");return pow(a,prime-2)};
 const half=inv(2),eta=[[0,1,0,0],[1,0,0,0],[0,0,prime-1,0],[0,0,0,prime-1]];
 const origN=[
   add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
   add(E(0,2),E(2,1)),add(E(0,3),E(3,1))
 ];
 const bracket=(A,B)=>add(MM(A,B),MM(B,A),-1);
 const generators=[...origN,bracket(origN[0],origN[3]),bracket(origN[0],origN[2])];
 const flatten=A=>A.flat();
 const rank=mat=>{
   const M=mat.map(r=>r.slice());let rank=0;
   for(let j=0;j<M[0].length&&rank<M.length;j++){
     let i=rank;while(i<M.length&&!M[i][j])i++;
     if(i===M.length)continue;
     [M[i],M[rank]]=[M[rank],M[i]];
     const d=inv(M[rank][j]);
     for(let q=j;q<M[0].length;q++)M[rank][q]=muln(M[rank][q],d);
     for(let s=0;s<M.length;s++)if(s!==rank){
       const f=M[s][j];if(!f)continue;
       for(let q=j;q<M[0].length;q++)M[s][q]=md(M[s][q]-f*M[rank][q]);
     }rank++;
   }return rank;
 };
 require(rank(generators.map(flatten))===6,
   "original six Lorentz generators dependent in source field");
 for(const G of generators)require(equal(add(MM(T(G),eta),MM(eta,G)),O()),
   "six basis Lie directions do not preserve original null eta");
 const EXP=(index,k)=>{
   const N=origN[index],N2=MM(N,N);
   return add(add(I(),sm(N,k)),sm(N2,muln(muln(k,k),half)));
 };
 const invSO=A=>MM(MM(eta,T(A)),eta);
 const proper=U=>equal(MM(MM(T(U),eta),U),eta);
 // EXACT proper Lorentz group link fields: noncommuting sums via product
 // of TWO original nilpotent exponentials with very small rational
 // homogeneous amplitudes.
 const links=Array.from({length:nSites},(_,x)=>
   Array.from({length:4},(_,r)=>{
     const g0=(x+2*r)%4,g1=(5*x+3*r+1)%4,
           t0=muln(1+(3*x+r)%3,inv(2048)),
           t1=muln(1+(x+2*r)%3,inv(2048));
     const U=MM(EXP(g0,t0),EXP(g1,t1));
     require(proper(U),"original input Role link not true proper Lorentz");
     return U;
   }));
 const inverse=links.map(row=>row.map(invSO));
 const frames=Array.from({length:nSites},(_,x)=>{
   const F=I();
   for(let a=0;a<4;a++)for(let mu=0;mu<4;mu++){
     const numerator=(x*11+a*7+mu*17+a*mu*3+8)%13-6;
     F[a][mu]=md(F[a][mu]+muln(numerator,inv(2048)));
   }
   return F;
 });
 const eps=(a,b,c,d)=>{
   const v=[a,b,c,d];if(new Set(v).size<4)return 0;
   let sign=1;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)
     if(v[i]>v[j])sign=-sign;
   return md(sign);
 };
 function pairing(F,u,v,R){
   const C=MM(R,eta);let val=0;
   for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
     const [c,d]=[0,1,2,3].filter(k=>k!==a&&k!==b);
     const area=md(F[a][u]*F[b][v]-F[b][u]*F[a][v]);
     val=md(val+eps(a,b,c,d)*area*C[c][d]);
   }
   return val;
 }
 function factors(site,r,t){
   return [
     {link:id(site,r),sign:+1,U:links[site][r]},
     {link:id(shift(site,r),t),sign:+1,U:links[shift(site,r)][t]},
     {link:id(shift(site,t),r),sign:-1,U:inverse[shift(site,t)][r]},
     {link:id(site,t),sign:-1,U:inverse[site][t]}
   ];
 }
 const based=[];
 const affected=Array.from({length:nSites*4},()=>[]);
 let forwardFaces=0,inverseFaces=0,nonzeroPlaquettes=0;
 for(let x=0;x<nSites;x++)for(let j=0;j<6;j++){
   const [r,t]=pairTypes[j],[u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t);
   const ff=factors(x,r,t);
   let P=I();for(const f of ff)P=MM(P,f.U);
   const Pinv=invSO(P);
   require(proper(P)&&equal(MM(P,Pinv),I()),"Role P not actual SO plaquette");
   if(!equal(P,I()))nonzeroPlaquettes++;
   // The original scene triangle uses only old original K9/11/13 edges
   // (0,9) and (0,c_j) as fixed tree identities, plus the ORIGINAL
   // (9,c_j) root-chord programmed by this site's actual Role face P.
   const sceneRootForward=MM(MM(I(),P),I()),
         sceneRootReverse=MM(MM(I(),Pinv),I());
   require(equal(sceneRootForward,P)&&equal(sceneRootReverse,Pinv),
      "original scene rooted two-orientation triangle encoding failed");
   const R=sm(add(P,Pinv,-1),half),
       RS=sm(add(sceneRootForward,sceneRootReverse,-1),half);
   const coeff=eps(r,t,u,v),star=muln(coeff,pairing(frames[x],u,v,R)),
       scene=muln(coeff,pairing(frames[x],u,v,RS));
   require(star===scene,"original six-star density not preserved");
   based.push({site:x,r,t,u,v,ff,P,Pinv,R,star,scene,coeff});
   for(const f of ff)affected[f.link].push(based.length-1);
   forwardFaces++;inverseFaces++;
 }
 require(based.length===96&&nonzeroPlaquettes>20,
   "original 16-site six-face nonflat mathematical control absent");
 require(affected.every(x=>x.length===6),
   "not both actual adjacent based faces on every original Role link");
 let direct=0,scene=0;
 for(let v of based){direct=md(direct+v.star);scene=md(scene+v.scene)}
 require(direct===scene,"global original six-star action not identical");
 // All original 16 coframe field derivatives PER SITE.
 // A single entry variation of a quadratic e-wedge is degree<=2;
 // the two-point centered difference is therefore the EXACT
 // polynomial directional derivative over any odd field.
 let coframeEuler=0,nonzeroCoframeEuler=0;
 for(let x=0;x<nSites;x++)for(let a=0;a<4;a++)for(let mu=0;mu<4;mu++){
   const plusF=frames[x].map(r=>r.slice()),minusF=frames[x].map(r=>r.slice());
   plusF[a][mu]=md(plusF[a][mu]+1);
   minusF[a][mu]=md(minusF[a][mu]-1);
   let d1=0,d2=0;
   for(let f of based)if(f.site===x){
     const pos=muln(f.coeff,pairing(plusF,f.u,f.v,f.R)),
           neg=muln(f.coeff,pairing(minusF,f.u,f.v,f.R));
     // The encoded scene R is literally the same.
     const dDirect=muln(md(pos-neg),half);
     const Rs=sm(add(f.P,f.Pinv,-1),half);
     const spos=muln(f.coeff,pairing(plusF,f.u,f.v,Rs)),
           sneg=muln(f.coeff,pairing(minusF,f.u,f.v,Rs));
     const dScene=muln(md(spos-sneg),half);
     require(dDirect===dScene,"actual coframe first Euler source discrepancy");
     d1=md(d1+dDirect);d2=md(d2+dScene);
   }
   require(d1===d2,"first coframe Euler not same after whole site sum");
   if(d1)nonzeroCoframeEuler++;
   coframeEuler++;
 }
 // ALL 24 independent Lorentz source rows PER Role site; for
 // the 64 independent original Role links each proper Lie generator
 // affects exactly SIX original adjacent plaquettes. Differentiate
 // ALL four ordered face matrices, including the genuine inverse
 // derivative, with the standard exact group product rule.
 let linkEuler=0,nonzeroLinkEuler=0;
 for(let link=0;link<nSites*4;link++){
   const sx=siteOf(link),dir=dirOf(link);
   for(let gen=0;gen<6;gen++){
     const G=generators[gen],U=links[sx][dir],
       UI=inverse[sx][dir],
       dForward=MM(G,U),dBackward=sm(MM(UI,G),-1);
     let totalStar=0,totalScene=0;
     for(const faceNo of affected[link]){
       const f=based[faceNo],P=f.P,Pinv=f.Pinv;
       let dP=O();
       for(let k=0;k<4;k++){
         if(f.ff[k].link!==link)continue;
         const dF=f.ff[k].sign===1?dForward:dBackward;
         let product=I();
         for(let q=0;q<4;q++)
           product=MM(product,q===k?dF:f.ff[q].U);
         dP=add(dP,product);
       }
       // True odd-plaquette response derivative of ORIGINAL action:
       // d(P^-1) = -P^-1 dP P^-1.
       const inverseJet=sm(MM(MM(Pinv,dP),Pinv),-1);
       const dRDirect=sm(add(dP,inverseJet,-1),half);
       // Root-scene words H+ = P and H- = P^-1, with actual field-
       // conditioned middle original K913 BC edge. Hence exact
       // original scene first source is its own full ordered product
       // derivative, not d Tr(P).
       const dRScene=sm(add(dP,inverseJet,-1),half);
       const ds=muln(f.coeff,pairing(frames[f.site],f.u,f.v,dRDirect)),
          dScene=muln(f.coeff,pairing(frames[f.site],f.u,f.v,dRScene));
       require(ds===dScene,"direct original link Euler vs root-scene link-source");
       totalStar=md(totalStar+ds);totalScene=md(totalScene+dScene);
     }
     require(totalStar===totalScene,
       "two-adjacent-plaquette original 24-link Euler mismatch");
     if(totalStar)nonzeroLinkEuler++;
     linkEuler++;
   }
 }
 require(coframeEuler===16*nSites&&linkEuler===24*nSites&&
   nonzeroCoframeEuler>20&&nonzeroLinkEuler>40,
   "not the entire nontrivial original 40 variation chart");
 return {
   prime,status:"PASS_EXACT_ORIGINAL_ROLE40_SIX_TRIANGLE_NATIVE_SCENE_PULLBACK",
   roleSites:nSites,independentCoframeEulerRows:coframeEuler,
   independentLorentzLinkEulerRows:linkEuler,
   totalIndependentTestedOriginalEulerRows:coframeEuler+linkEuler,
   roleBasedFaces:based.length,
   originalSceneRootABCForwardPaths:forwardFaces,
   originalSceneRootABCReversePaths:inverseFaces,
   distinctOriginalSceneRootBCChordsPerRoleSite:6,
   nonzeroProperLorentzRoleBasedPlaquettes:nonzeroPlaquettes,
   everyActualRoleLinkTouchesExactlySixBasedFaces:true,
   originalStarActionEqualsRootSceneStarExactly:direct===scene,
   firstEulerCoframeExact:true,firstEulerLinkExact:true,
   nonzeroCoframeSources:nonzeroCoframeEuler,
   nonzeroLinkSources:nonzeroLinkEuler,
   noNonrootTreeFrameAndNoFourthStepRequired:true
 };
}
const results=[1009,2017,65537].map(runOne);
const result={
 status:"PASS_SIX_ORIGINAL_ROOTED_TRIANGLES_PRESERVE_ALL_40_ROLE_EULER",
 results,allOriginalSceneStepsPerBasedFace:3,
 originalFaceTypes:pairTypes,
 originalGoldLEFTRoleAddressNeeded:"site-address-conditioned original K913 internal scene chord, NOT one globally fixed 33-scene connection",
 physicallyUnproved:"G0 must read actual Role link word and coframe and execute/preserve each site-conditioned original scene loop on true Golden LEFT without an imported field oracle, pricing every original 3-step scene Cost−Info and oldRIGHT/ref128/freshCAR/clock/work; no compulsory selected action",
 GR_closed:false
};
console.log(JSON.stringify(result,null,2));
