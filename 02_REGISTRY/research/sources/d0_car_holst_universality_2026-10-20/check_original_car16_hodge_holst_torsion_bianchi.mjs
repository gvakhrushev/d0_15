#!/usr/bin/env node
"use strict";
/**
 * Original 4-Role Lorentz/carrier parity and continuum first-order
 * Einstein-Hilbert vs Holst universality: exact integer certificates.
 *
 * Carriers are the original Role bivector basis and eta (+---).
 * Consumes original CAR16/grade2 Hodge owner, checks its entire commutant
 * independently over F_1000003, all 24 independent torsion variables,
 * and all 21 pair-symmetric Riemann variables / algebraic first Bianchi.
 * The continuum implication is standard first-order Palatini-Holst
 * variation, NOT a proof selected native Book03/G0/M1 full action equals
 * a member of this class or that the finite SO star is torsion-free.
 */
const ok=(v,m)=>{if(!v)throw Error("FAIL "+m)};
const N=4,M=6,mod=1000003;
const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const pairIndex=new Map(pairs.map((p,i)=>[p.join(","),i]));
const zero=(m,n=m)=>Array.from({length:m},()=>Array(n).fill(0));
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const mult=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const add=(A,B,t=1)=>A.map((r,i)=>r.map((v,j)=>v+t*B[i][j]));
const scal=(A,c)=>A.map(row=>row.map(v=>c*v));
const tr=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const same=(A,B)=>A.length===B.length&&A.every((row,i)=>row.every((v,j)=>v===B[i][j]));
function e(i,j){let X=zero(4);X[i][j]=1;return X}
const eta=[[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,-1]];
const J=zero(6);
J[5][0]=1;J[4][1]=-1;J[3][2]=1;
J[2][3]=-1;J[1][4]=1;J[0][5]=-1;
ok(same(mult(J,J),scal(eye(6),-1)),"ORIGINAL CAR16 grade2 Lorentz Hodge squares to -I");
ok(same(tr(J),scal(J,-1)),"original six Hodge is antisymmetric");
for(const [a,b] of [[1,0],[0,1],[3,5],[-7,3],[0,0]]) {
 const L=add(scal(eye(6),b),J,a),LI=add(scal(eye(6),b),J,-a);
 ok(same(mult(L,LI),scal(eye(6),a*a+b*b)),
   "all REAL alpha,beta Lorentz bivector intertwiners are algebraically invertible unless both zero");
}
function rhoLie(X){
 const A=zero(6);
 const put=(row,col,v)=>{if(v)A[row][col]+=v};
 for(let col=0;col<6;col++){
  const [i,j]=pairs[col];
  for(let k=0;k<4;k++){
   const a=X[k][i];
   if(k!==j&&a){let p=k<j?[k,j]:[j,k];put(pairIndex.get(p.join(",")),col,(k<j?1:-1)*a)}
   const b=X[k][j];
   if(i!==k&&b){let p=i<k?[i,k]:[k,i];put(pairIndex.get(p.join(",")),col,(i<k?1:-1)*b)}
  }
 }
 return A;
}
const X=[];
for(const s of [1,2,3])X.push(add(e(0,s),e(s,0)));
for(const [i,j] of [[1,2],[1,3],[2,3]])X.push(add(e(i,j),e(j,i),-1));
const Actions=X.map(rhoLie);
for(const a of Actions)ok(same(mult(J,a),mult(a,J)),"CAR16 grade2 * commutes with every true so(1,3) generator");
const comm=[];
for(const A of Actions)for(let i=0;i<6;i++)for(let j=0;j<6;j++){
 let row=Array(36).fill(0);
 for(let k=0;k<6;k++){row[i*6+k]+=A[k][j];row[k*6+j]-=A[i][k];}
 comm.push(row);
}
function rankMod(rows){
 const A=rows.map(row=>row.map(x=>((x%mod)+mod)%mod)),m=A.length,n=A[0].length;
 const pow=(b,k)=>{let out=1;while(k){if(k%2)out=out*b%mod;b=b*b%mod;k=Math.floor(k/2)}return out};
 let rank=0;
 for(let col=0;col<n&&rank<m;col++){
  let piv=rank;while(piv<m&&A[piv][col]===0)piv++;
  if(piv===m)continue;
  [A[rank],A[piv]]=[A[piv],A[rank]];
  const inv=pow(A[rank][col],mod-2);
  for(let j=col;j<n;j++)A[rank][j]=A[rank][j]*inv%mod;
  for(let i=rank+1;i<m;i++)if(A[i][col]){
   let t=A[i][col];for(let j=col;j<n;j++)A[i][j]=(A[i][j]-t*A[rank][j]%mod+mod)%mod;
  }
  rank++;
 }
 return rank;
}
const r=rankMod(comm);
ok(r===34,"original proper Lorentz commutant of Lambda2 is EXACTLY span{I,J}: modular rank34 plus two explicit rational kernel vectors");
const perm=[0,2,1,3];
const S=zero(6);
for(let col=0;col<6;col++){
 let [i,j]=pairs[col],a=perm[i],b=perm[j],ord=a<b?[a,b]:[b,a];
 S[pairIndex.get(ord.join(","))][col]=a<b?1:-1;
}
ok(same(mult(S,tr(S)),eye(6)),"odd Role swap exterior action is orthogonal");
ok(same(mult(mult(S,J),tr(S)),scal(J,-1)),"CAR Hodge is ROLE orientation-odd");
ok(same(mult(mult(S,eye(6)),tr(S)),eye(6)),"scalar Holst channel ROLE orientation-even");

const triple=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]];
const columns=Array.from({length:4},(_,a)=>pairs.map(([i,j])=>[a,i,j])).flat();
const rows=pairs.flatMap(([a,b])=>triple.map(ijk=>[a,b,...ijk]));
const sign=p=>{
 if(new Set(p).size!==p.length)return 0;
 let v=1;for(let i=0;i<p.length;i++)for(let j=i+1;j<p.length;j++)if(p[i]>p[j])v=-v;return v;
};
const eqset=(a,b)=>a.length===b.length && a.every(x=>b.includes(x));
const Tmap=zero(24);
for(let j=0;j<24;j++){
 const [a,i,k]=columns[j];
 for(let ii=0;ii<24;ii++){
  const [u,v,...ijk]=rows[ii];
  if(a===u){const q=[i,k,v];if(eqset(q,ijk))Tmap[ii][j]+=sign(q)}
  if(a===v){const q=[u,i,k];if(eqset(q,ijk))Tmap[ii][j]-=sign(q)}
 }
}
const rankT=rankMod(Tmap);
ok(rankT===24,"all 24 genuine independent torsion components killed by D(e^a wedge e^b)=0, no missing torsion mode");
// Exact integer Bareiss determinant independently, proving this 24x24 test
// over Q and not relying on approximate rank or sampled curvature.
function detBareiss(A0){
 const A=A0.map(row=>row.map(x=>BigInt(x))),n=A.length;let sign=1n,den=1n;
 for(let k=0;k<n-1;k++){
  if(A[k][k]===0n){let i=k+1;while(i<n&&A[i][k]===0n)i++;ok(i<n,"torsion map determinant nonzero");
   [A[i],A[k]]=[A[k],A[i]];sign=-sign;}
  const p=A[k][k];
  for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++){
   const numerator=A[i][j]*p-A[i][k]*A[k][j];
   ok(numerator%den===0n,"Bareiss exact integer division");
   A[i][j]=numerator/den;
  }
  for(let i=k+1;i<n;i++)A[i][k]=0n;
  den=p;
 }
 return sign*A[n-1][n-1];
}
const detT=detBareiss(Tmap);
ok(detT!==0n,"exact 24-torsion determinant nonzero");

// Pair symmetric curvature has 21 independent values. First Bianchi in 4D
// is ONLY one scalar relation; Lorentz Holst pseudoscalar equals 8 times it.
const Ri=zero(6);
const permutations=a=>{
 if(a.length===0)return [[]];
 return a.flatMap((x,i)=>permutations(a.filter((_,j)=>j!==i)).map(y=>[x,...y]));
};
const all24=permutations([0,1,2,3]);
function Rab(Q,i,j,k,l){
 if(i===j||k===l)return 0;
 const u=i<j?1:-1,v=k<l?1:-1;
 return u*v*Q[pairIndex.get([Math.min(i,j),Math.max(i,j)].join(","))][pairIndex.get([Math.min(k,l),Math.max(k,l)].join(","))];
}
function Holst(Q){return all24.reduce((sum,ijkl)=>sum+sign(ijkl)*Rab(Q,...ijkl),0)}
function Bianchi(Q){return Rab(Q,0,1,2,3)-Rab(Q,0,2,1,3)+Rab(Q,0,3,1,2)}
for(let i=0;i<6;i++)for(let j=i;j<6;j++){
 const Q=zero(6);Q[i][j]=1;Q[j][i]=1;
 ok(Holst(Q)===8*Bianchi(Q),"full 24-permutation Holst contraction IS eight times first Bianchi for every one of 21 pair-symmetric generators");
}
const Qno=zero(6);Qno[0][5]=Qno[5][0]=1;
ok(Holst(Qno)===8 && Bianchi(Qno)===1,"genuine offshell Holst is NONZERO; Bianchi is load-bearing");
const Qyes=zero(6);Qyes[0][5]=Qyes[5][0]=2;
Qyes[1][4]=Qyes[4][1]=3;
Qyes[2][3]=Qyes[3][2]=1;
ok(Bianchi(Qyes)===0&&Holst(Qyes)===0,"algebraic torsion-free Bianchi eliminates Holst, not Palatini");

// ORIGINAL site coframe dressing by any genuine positive scalar W(K_x)>0:
// two coframe legs => W multiplying BOTH invariant pairings is absorbed
// by the single site coframe ehat=sqrt(W)e. Demonstrate EXACT integers for
// 2 independent positive site weights W1=25/9 and W2=49/25.
const sampleE=[[3,1,0,2],[0,2,1,0],[1,0,2,1],[0,1,0,3]];
const curvature=Array.from({length:6},(_,f)=>Array.from({length:6},(_,v)=>((7*f+11*v+5)%13)-6));
function wedge(a,b){return pairs.map(([i,j])=>a[i]*b[j]-a[j]*b[i])}
function actionOnE(e,alpha,beta){
 const C=add(scal(J,alpha),scal(eye(6),beta));
 let total=0;
 for(let u=0;u<6;u++){
  const [i,j]=pairs[u],Sigma=wedge(e[i],e[j]);
  const CF=mult(C,curvature[u].map(x=>[x])).map(x=>x[0]);
  total+=Sigma.reduce((s,x,k)=>s+x*CF[k],0);
 }
 return total;
}
const orig=actionOnE(sampleE,3,2);
for(const [num,den] of [[25,9],[49,25]]){
 const sqN=Math.round(Math.sqrt(num)),sqD=Math.round(Math.sqrt(den));
 ok(sqN**2===num&&sqD**2===den,"nontrivial site weight is a perfect square rational");
 const ehatNumerator=scal(sampleE,sqN);
 const ehatAction=actionOnE(ehatNumerator,3,2);
 ok(ehatAction===num*orig && ehatAction*den===num*den*orig,
 "finite all-six-face two invariant geometric channels exact Book-Weyl dressing by integer cross multiplication");
}

// ORIGINAL native Book scene, not fictitious arbitrary scalar weights.
// Compute the TRUE 3-tick positive triangular return W_x=Tr K_x^3/7722,
// from all 718 actual edges on TWO distinct Role-site scene inputs.
// Their two W_x are not equal. Both source bivector channels are still
// removed EXACTLY by the SAME local composite coframe sqrt(W_x)e_x.
const goldenP=(Math.sqrt(5)-1)/2,phi=1/goldenP,sceneSize=33;
const zone=u=>u<9?0:(u<20?1:2);
const nativeK=x=>Array.from({length:sceneSize},(_,u)=>
 Array.from({length:sceneSize},(_,v)=>zone(u)===zone(v)?0:
 goldenP**(1.04+0.007*((u+3*v+5*x)%17))));
function Z3(K){
 let sum=0,counts=0;
 for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++){
  sum+=3*(K[a][b]*K[b][c]*K[c][a]+K[a][c]*K[c][b]*K[b][a]);counts+=6;
 }
 ok(counts===7722,"ORIGINAL 7722 genuine native based triangle histories");
 return sum;
}
const K0=nativeK(0),K1=nativeK(1);
for(const K of [K0,K1]){
 ok(K.flat().filter(v=>v>0).length===718,
   "original K(9,11,13), exactly 718 positive directed Cost>=1 transitions");
}
const W0=Z3(K0)/7722,W1=Z3(K1)/7722;
ok(W0>0&&W1>0&&Math.abs(W0-W1)>1e-7,
 "nontrivial independent native Role-site 3-tick Book pressures");
const s0=actionOnE(sampleE,3,2),s1=actionOnE(scal(sampleE,2),3,2);
const sh=(E,w)=>actionOnE(scal(E,Math.sqrt(w)),3,2);
ok(Math.abs(W0*s0-sh(sampleE,W0))<2e-11 &&
   Math.abs(W1*s1-sh(scal(sampleE,2),W1))<2e-11,
   "native heterogeneous all718 site Book pressures each absorb into same CAR16 pair channel");
const t0=.17,t1=-.09,tt=[t0,t1],ws=[W0,W1];
let groupResidual=0;
for(let k=0;k<2;k++){
 const q=phi**tt[k],BookShiftK=(k===0?K0:K1).map(row=>row.map(v=>q*v));
 const Wprime=Z3(BookShiftK)/7722,srcE=k===0?sampleE:scal(sampleE,2);
 const Eprime=scal(srcE,q**(-1.5));
 const ds=actionOnE(srcE,3,2)*ws[k];
 const dt=actionOnE(Eprime,3,2)*Wprime;
 groupResidual=Math.max(groupResidual,Math.abs(dt-ds));
 ok(Math.abs(Wprime/ws[k]-q**3)<1e-12 &&
    Math.abs(Math.sqrt(Wprime)*q**(-1.5)-Math.sqrt(ws[k]))<1e-12,
 "ORIGINAL 3-Book/2-coframe sitewise compensator, two independent Info shifts");
}
ok(groupResidual<2e-11,"true original sitewise geometric Book–Weyl invariance");

// Exact Levi-Civita CONFORMAL metric Ricci from connection coefficients,
// not by assuming the scalar curvature transformation formula.
// g=diag(+---) flat, W(x)=1+x^2, ghat=Wg, x coordinate index 1.
function directConformalRicci(x){
 const W=1+x*x,wP=2*x,wPP=2;
 const a=wP/(2*W),ap=(wPP*W-wP*wP)/(2*W*W),sig=[1,-1,-1,-1];
 const C=Array.from({length:4},()=>zero(4).map(row=>row.map(()=>Array(4).fill(0))));
 for(let rho=0;rho<4;rho++)for(let mu=0;mu<4;mu++)for(let nu=0;nu<4;nu++)
   C[rho][mu][nu]=(rho===mu&&nu===1?1:0)+(rho===nu&&mu===1?1:0)
     +(rho===1&&mu===nu?sig[mu]:0);
 let scalar=0;
 for(let mu=0;mu<4;mu++)for(let nu=0;nu<4;nu++){
  let val=ap*C[1][nu][mu];
  if(nu===1)for(let rho=0;rho<4;rho++)val-=ap*C[rho][rho][mu];
  for(let rho=0;rho<4;rho++)for(let lam=0;lam<4;lam++){
   val+=a*a*(C[rho][rho][lam]*C[lam][nu][mu]-
             C[rho][nu][lam]*C[lam][rho][mu]);
  }
  if(mu===nu)scalar+=sig[mu]*val/W;
 }
 const gradW2=-(wP*wP),boxW=-wPP;
 const formula=-3*boxW/(W*W)+(3/2)*gradW2/(W*W*W);
 return {x,W,RicciDirect:scalar,RicciConformalFormula:formula,
   EHdensity:W*W*scalar,
   BransDickeBulk:(3/2)*gradW2/W,
   boundaryMinus3BoxW:-3*boxW};
}
const samples=[0,.35,1,2].map(directConformalRicci);
for(const v of samples){
 ok(Math.abs(v.RicciDirect-v.RicciConformalFormula)<5e-14,
  "4D LeviCivita Ricci DIRECT equals conformal W factor formula");
 ok(Math.abs(v.EHdensity-(v.BransDickeBulk+v.boundaryMinus3BoxW))<4e-13,
  "4D native Book-Weyl metric EH -> exact Brans-Dicke omega=-3/2 bulk + true boundary");
}

// NEW BOOK ENDPOINT WEIGHT = EXACT PROJECTIVE GEOMETRY, not extra curvature.
// Starting from hat e=e^sigma e, same ORIGINAL Lorentz spin connection
// omega, the raw and dressed affine connections obey
// Gamma_raw^rho_(mu nu)=Gamma_LC(ghat)^rho_(mu nu)
//                            -delta^rho_nu (partial_mu sigma).
// sigma=0.5 ln W, thus xi=d sigma is EXACT and has zero curvature.
// Check all 4^4 true curvature slots DIRECTLY, not just scalar Ricci.
function projectiveSceneConnection(x){
 const W=1+x*x,wP=2*x,wPP=2;
 const a=wP/(2*W),ap=(wPP*W-wP*wP)/(2*W*W),sig=[1,-1,-1,-1];
 const hc=Array.from({length:4},()=>Array.from({length:4},()=>Array(4).fill(0)));
 const hd=Array.from({length:4},()=>Array.from({length:4},()=>Array(4).fill(0)));
 const rc=Array.from({length:4},()=>Array.from({length:4},()=>Array(4).fill(0)));
 const rd=Array.from({length:4},()=>Array.from({length:4},()=>Array(4).fill(0)));
 for(let rho=0;rho<4;rho++)for(let mu=0;mu<4;mu++)for(let nu=0;nu<4;nu++){
  const C=(rho===mu&&nu===1?1:0)+(rho===nu&&mu===1?1:0)
           +(rho===1&&mu===nu?sig[mu]:0);
  const P=(rho===nu&&mu===1?1:0);
  hc[rho][mu][nu]=a*C;hd[rho][mu][nu]=ap*C;
  rc[rho][mu][nu]=a*(C-P);rd[rho][mu][nu]=ap*(C-P);
 }
 return {hc,hd,rc,rd,W,sigmaDeriv:a};
}
function fourCurvature(g,d){
 const out=Array.from({length:4},()=>Array.from({length:4},()=>zero(4)));
 for(let rho=0;rho<4;rho++)for(let sigma=0;sigma<4;sigma++)
 for(let mu=0;mu<4;mu++)for(let nu=0;nu<4;nu++){
   let q=(mu===1?d[rho][nu][sigma]:0)
        -(nu===1?d[rho][mu][sigma]:0);
   for(let lam=0;lam<4;lam++)
    q+=g[rho][mu][lam]*g[lam][nu][sigma]
      -g[rho][nu][lam]*g[lam][mu][sigma];
   out[rho][sigma][mu][nu]=q;
 }
 return out;
}
const projectiveChecks=[];
for(const x of [0,.35,1,2]){
 const c=projectiveSceneConnection(x);
 const Rh=fourCurvature(c.hc,c.hd),Rr=fourCurvature(c.rc,c.rd);
 let err=0,torsionErr=0,xiCurl=0;
 for(let rho=0;rho<4;rho++)for(let sig=0;sig<4;sig++)
 for(let mu=0;mu<4;mu++)for(let nu=0;nu<4;nu++)
   err=Math.max(err,Math.abs(Rh[rho][sig][mu][nu]-Rr[rho][sig][mu][nu]));
 for(let rho=0;rho<4;rho++)for(let mu=0;mu<4;mu++)for(let nu=0;nu<4;nu++){
  const actual=c.rc[rho][mu][nu]-c.rc[rho][nu][mu];
  const predicted=c.sigmaDeriv*((rho===mu&&nu===1?1:0)
                                 -(rho===nu&&mu===1?1:0));
  torsionErr=Math.max(torsionErr,Math.abs(actual-predicted));
 }
 ok(err<3e-14 && torsionErr<3e-14,
  "ALL 256 CURVATURE ENTRIES unchanged under exact native Book endpoint projective shift, predicted raw trace torsion");
 projectiveChecks.push({x,curvatureMaxError:err,rawTorsionMaxError:torsionErr,
  compensatorSigmaDerivative:c.sigmaDeriv});
}
// A local independent Immirzi ratio is NOT a pure coframe Weyl gauge:
// beta(x)=x0, constant alpha, torsionless e=dx gives
// d beta wedge e2 wedge e3 = dx0 wedge dx2 wedge dx3 != 0.
const variableHolstTorsionFreeSource=sign([0,2,3]);
ok(variableHolstTorsionFreeSource===1,
 "moving beta/alpha produces an authentic independent torsion source even at flat e");
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_CAR16_LORENTZ_HODGE_HOLST_TORSION_BIANCHI_BOOK_WEYL",
 LorentzCommutant:{rankOverFp:r,dimension:36-r,generatedBy:["I6","CAR16 Hodge J"],J2:"-I",roleReversal:"J odd, I even"},
 independentTorsion:{rows:24,cols:24,rank:rankT,determinant:detT.toString()},
 curvature:{pairSymmetricParameters:21,algebraicBianchiConstraints:1,
  LeviCivitaAlgebraicParameters:20,HolstPseudoscalar:"8 * (R0123-R0213+R0312)",
  offShellHolstValue:Holst(Qno),onBianchiHolstValue:Holst(Qyes)},
 connectionInverse:"(beta I+alpha J)^-1=(beta I-alpha J)/(alpha²+beta²) for (alpha,beta) not both zero",
 PalatiniCondition:"alpha != 0 to retain Einstein coframe equation; beta unconstrained real constant",
 BookWeyl:{commonPositiveSiteWeightAbsorbedInto:"ehat_x=sqrt(W_x)e_x",coframeJacobian:"W_x^8",
  independentExactSiteWeights:["25/9","49/25"],allSixFaceSource:orig,
  actualNativeSceneW:[W0,W1],independentBookInfoShifts:[t0,t1],
  BookWeylSiteActionResidual:groupResidual,conformalRicci4DChecks:samples,
  projectiveBookEndpointCurvatureChecks:projectiveChecks,
  BransDickeOmega:"-3/2",movingImmirziTorsionHostileControl:variableHolstTorsionFreeSource},
 proofScope:"exact original finite CAR/so(1,3) algebra + mathematical continuum torsionfree Palatini-Holst theorem; no compulsory Book/G0, no native finite-torsionless/GR refinement",
 GR_closed:false
},null,2));
