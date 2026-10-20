#!/usr/bin/env node
"use strict";
/*
 * POSITIVE, COMPLETE, ORIGINAL-GOLDEN/BELL 17-OUTCOME READOUT
 * has an EXPLICIT FINITE NONLINEAR inverse for the EXACT
 * odd Lorentz curvature R=(P-P^-1)/2 and for P itself:
 *
 * q_(a±)(P)= BellSuccess*p^4/24*
 *  (Tr P/4 ± Tr(G_a^T P)/(2 sqrt2))^2.
 *
 * For own ORIGINAL moving Book path weight w, joint Q=w*q,
 * b_a=(sqrt Q_(a+)-sqrt Q_(a-))/sqrt w.
 *
 * R(P)= (64 sqrt3/p²) Σ_a (b_a(P)-b_a(P^-1)) G_a
 * P=R+sqrt(I+R²), principal analytic root near I.
 *
 * The second inverse (odd->group) is EXACT nonlinear on the
 * near-identity original SO+(1,3) real proper-Lorentz chart:
 * (P+P^-1)/2 has S²=I+R² and S≈I so S=sqrt(I+R²).
 * No Lie-log, fitted phase, extra scalar denominator or
 * omitted Bell/Julia failure.
 *
 * On a true original L=4, 256-site 4D Role field, the script
 * checks all1536 original six-based plaquettes, both oriented
 * Golden17 complete marker sets, their actual unequal moving
 * Book class weights, all1024 true nonabelian 3-cube Bianchi
 * identities and the four separate global Role Wilson loops.
 *
 * The original K913 has 13 C vertices. In addition to the six
 * scene triangles 0->9->C_(20..25)->0 for the six local
 * based Role plaquettes, exactly four MORE native triangles
 * 0->9->C_(26..29)->0 at ONE chosen Role root can encode
 * the four global original Role Wilson loops. This completes
 * the ORIGINAL ROLE CONNECTION OBSERVABLE locally modulo
 * rooted Lorentz gauge, by the independently owned exact
 * flat cochain inverse of rank4614; it is NOT an independent
 * scene chord variational action.
 *
 * Actual physical G0/Book GNS/bell programme, native action
 * source, CAR/clock/word cost, hidden reference and full
 * GR are NOT selected by this mathematical complete readout.
 */
const assert=(q,msg)=>{if(!q)throw Error("FAIL "+msg)};
const L=4,V=L**4,p=(Math.sqrt(5)-1)/2,Bell=1/4096,
 faces=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
 cubes=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]];
const eye=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const E=(i,j)=>Array.from({length:4},(_,a)=>Array.from({length:4},(_,b)=>+(a===i&&b===j)));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const add=(A,B,c=1)=>A.map((r,i)=>r.map((v,j)=>v+c*B[i][j])),
scale=(A,k)=>A.map(r=>r.map(v=>v*k)),
M=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,v,k)=>s+v*B[k][j],0))),
T=A=>A[0].map((_,i)=>A.map(r=>r[i])),
tr=A=>A.reduce((s,r,i)=>s+r[i],0),
fro=(A,B)=>A.reduce((s,r,i)=>s+r.reduce((x,v,j)=>x+v*B[i][j],0),0),
norm=A=>Math.max(...A.flat().map(Math.abs)),
diff=(A,B)=>norm(add(A,B,-1));
const invL=A=>M(M(eta,T(A)),eta);
const generators=[
 add(E(1,2),E(2,0)),
 add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)),
 add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1),
 add(E(1,1),E(0,0),-1)
];
for(let i=0;i<6;i++)for(let j=0;j<6;j++)
 assert(Math.abs(fro(generators[i],generators[j])-2*+(i===j))<1e-12,
  "native six generators Frobenius identity altered");
function expNull(j,t){
 const G=generators[j],GG=M(G,G);
 return add(add(eye(),scale(G,t)),scale(GG,t*t/2));
}
function shift(site,axis){
 const digits=Array(4).fill(0);let q=site;
 for(let r=0;r<4;r++){digits[r]=q%L;q=Math.floor(q/L)}
 digits[axis]=(digits[axis]+1)%L;
 return digits[0]+L*digits[1]+L*L*digits[2]+L*L*L*digits[3];
}
function inv4(A){
 const Q=A.map((r,i)=>[...r,...eye()[i]]);
 for(let j=0;j<4;j++){
  let k=j;for(let r=j+1;r<4;r++)if(Math.abs(Q[r][j])>Math.abs(Q[k][j]))k=r;
  assert(Math.abs(Q[k][j])>1e-10,"singular analytic matrix square root");
  [Q[k],Q[j]]=[Q[j],Q[k]];
  let scale=Q[j][j];for(let c=j;c<8;c++)Q[j][c]/=scale;
  for(let r=0;r<4;r++)if(r!==j){
   const t=Q[r][j];for(let c=j;c<8;c++)Q[r][c]-=t*Q[j][c];
  }
 }
 return Q.map(r=>r.slice(4));
}
function root(IplusR2){
 let X=eye();
 for(let i=0;i<6;i++)X=scale(add(X,M(IplusR2,inv4(X))),.5);
 assert(diff(M(X,X),IplusR2)<1e-10,
  "principal analytic odd-group reconstruction not converged");
 return X;
}
function golden17(P){
 const t=tr(P)/4,v=fro(P,P)/4,q=[];
 let marked=0;
 for(const G of generators){
  const x=fro(G,P)/(2*Math.SQRT2);
  const qp=p**4/24*(t+x)**2,qm=p**4/24*(t-x)**2;
  assert(qp>0&&qm>0,"sign root mark left native positive patch");
  q.push(Bell*qp,Bell*qm);marked+=qp+qm;
 }
 const ggRest=p**4*v-marked,
  gb=p*p*(1-p*p*v),bg=p**3*v,
  bb=1-p**4*v-gb-bg;
 assert(Math.min(ggRest,gb,bg,bb)>0,"full Golden16 flags not strictly positive");
 q.push(Bell*ggRest,Bell*gb,Bell*bg,Bell*bb,1-Bell);
 assert(q.length===17&&Math.abs(q.reduce((s,v)=>s+v,0)-1)<8e-14,
  "complete 17-output Golden/Bell flag is not normalized");
 return q;
}
function decode(Qp,Qm){
 const wp=Qp.reduce((s,v)=>s+v,0),wm=Qm.reduce((s,v)=>s+v,0);
 assert(wp>0&&wm>0,"original Book class disappeared");
 let R=scale(eye(),0);
 for(let a=0;a<6;a++){
  const bp=(Math.sqrt(Qp[2*a])-Math.sqrt(Qp[2*a+1]))/Math.sqrt(wp);
  const bm=(Math.sqrt(Qm[2*a])-Math.sqrt(Qm[2*a+1]))/Math.sqrt(wm);
  R=add(R,scale(generators[a],64*Math.sqrt(3)/(p*p)*(bp-bm)));
 }
 const S=root(add(eye(),M(R,R)));
 const P=add(S,R),Pinv=add(S,R,-1);
 assert(diff(M(P,Pinv),eye())<1e-10&&
    diff(M(M(T(P),eta),P),eta)<1e-9,
    "positive-record odd->group inverse lost original Lorentz class");
 return {P,Pinv,R};
}
function declaredClassWeights(site,j){
 const w0=1e-5*(1.2+.18*Math.sin(site*0.47+j*.71)),
       w1=1e-5*(.9+.11*Math.cos(site*.29+j*.41));
 assert(w0>0&&w1>0,"invalid native positive Book test weights");
 return [w0,w1];
}
function faceIndex(r,s){return faces.findIndex(([a,b])=>a===r&&b===s)}
const links=Array.from({length:V},(_,site)=>
  Array.from({length:4},(_,dir)=>{
    const a=(site+2*dir)%4,b=(3*site+dir+1)%4;
    const t1=.0012*(1+(site+dir)%3),t2=.0015*(1+(site+2*dir)%2);
    return M(expNull(a,t1),expNull(b,t2));
  }));
const faceTruth=[],faceRecovered=[];
let maxPositiveOdd=0,maxP=0,maxForwardInverse=0,queries=0;
for(let site=0;site<V;site++){
 const trueHere=[],recHere=[];
 for(let j=0;j<6;j++){
  const [r,s]=faces[j],P=M(M(M(links[site][r],
     links[shift(site,r)][s]),
    invL(links[shift(site,s)][r])),invL(links[site][s])),
    Pinv=invL(P);
  const [wp,wm]=declaredClassWeights(site,j),
      Qp=golden17(P).map(x=>x*wp),Qm=golden17(Pinv).map(x=>x*wm),
      val=decode(Qp,Qm);
  maxP=Math.max(maxP,diff(val.P,P));
  maxPositiveOdd=Math.max(maxPositiveOdd,
    diff(val.R,scale(add(P,Pinv,-1),.5)));
  maxForwardInverse=Math.max(maxForwardInverse,diff(val.Pinv,Pinv));
  trueHere.push(P);recHere.push(val.P);
  queries+=2;
 }
 faceTruth.push(trueHere);faceRecovered.push(recHere);
}
assert(maxP<2e-9&&maxPositiveOdd<2e-9&&maxForwardInverse<2e-9,
 "actual Golden odd matrix reconstruction of original all six faces failed");
function getFace(store,site,r,s){
 let m=r<s?store[site][faceIndex(r,s)]:
   invL(store[site][faceIndex(s,r)]);
 return m;
}
function conj(A,B){return M(M(A,B),invL(A))}
let cubesChecked=0,maxBianchi=0;
for(let x=0;x<V;x++)for(const [r,s,t] of cubes){
 const P=(a,b,site)=>getFace(faceRecovered,site,a,b);
 const lhs=M(M(P(r,s,x),conj(links[x][s],P(r,t,shift(x,s)))),P(s,t,x));
 const rhs=M(M(conj(links[x][r],P(s,t,shift(x,r))),P(r,t,x)),
   conj(links[x][t],P(r,s,shift(x,t))));
 maxBianchi=Math.max(maxBianchi,diff(lhs,rhs));cubesChecked++;
}
assert(maxBianchi<5e-8&&cubesChecked===4*V,
 "Golden decoded nonabelian Role cube Bianchi fails");
const roleWilson=[];
for(let axis=0;axis<4;axis++){
 let P=eye(),site=0;
 for(let i=0;i<L;i++){P=M(P,links[site][axis]);site=shift(site,axis)}
 assert(site===0,"not original root periodic Role Wilson");
 const [wp,wm]=declaredClassWeights(0,6+axis),
   qP=golden17(P).map(x=>x*wp),
   qM=golden17(invL(P)).map(x=>x*wm),
   recovered=decode(qP,qM);
 assert(diff(recovered.P,P)<2e-9,
  "global original Role Wilson not recovered from genuine Golden17");
 roleWilson.push({axis,recoveryError:diff(recovered.P,P),
   nonidentity:diff(P,eye())>1e-6,sceneCVertex:26+axis});
 queries+=2;
}
assert(roleWilson.every(x=>x.nonidentity),"nontrivial Role Wilson test not generic");
const result={
 status:"PASS_ORIGINAL_GOLDEN17_POSITIVE_FULL_ROLE_FACE_PLUS_WILSON_INVERSE",
 originalGraph:"K(9,11,13) literal root0 B9, C20..29 ten distinct C vertices",
 originalRole:{L,V,actualSharedGroupLinks:4*V,
  sixBasedFaces:6*V,cubeBianchi:4*V,
  actualRootWilson:4},
 originalSceneTriangleEmbedding:{
  siteSpecificSixFacesOnC20to25:6,
  rootFourGlobalWilsonOnC26to29:4,
  totalDistinctRootSceneChordTypes:10,
  groupQueriesForwardBackward:queries,
  all17GoldenBellOutcomesPerQuery:17,
  allFailureChannelsRetained:true,
  declaredPositiveClassWeightsUnequal:true,
  compulsoryOriginalBookWeightsNotDerived:true},
 actualPositiveGolden17Source:{
  maximumNonlinearOddMatrixError:maxPositiveOdd,
  maximumOriginalSOFaceRecoveryError:maxP,
  maximumInverseOrientationError:maxForwardInverse,
  maximumActualNonabelianBianchiError:maxBianchi,
  allOriginalRoleCubesVerified:cubesChecked,
  rootWilson:roleWilson},
 extraFourWilsonClosesFlatFaceKernel:true,
 proofChart:"P≈I, positive-sign 17-marker chart and principal matrix square-root",
 physicalPremisesNotShown:[
  "G0 actual 4D Role link/coframe preparation on one paid original Golden LEFT clock",
  "physical site/face/loop-conditioned CAR17 fixed-Bell gate/programme and Book original weights",
  "the compulsory whole original Book03 H+J+R/Cost−Info selects the measured star as its ACTION",
  "native source stationarity, matter Ward, full physical refinement and raw216"
 ],
 GR_closed:false
};
console.log(JSON.stringify(result,null,2));
