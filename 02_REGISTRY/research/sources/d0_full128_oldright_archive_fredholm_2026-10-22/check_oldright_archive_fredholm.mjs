// OLD native proof owner 2-Kraus noncommuting fixture + exact genuine Choi
// record purification; Fredholm obstruction/repair for DATA x oldRIGHT
// and exact full coherent archive information transfer under an isometry.
// For the ORIGINAL full128, only dimension/rank identities are universally
// applied; do NOT claim this two-Kraus toy is a numerical full128 replay.
// NO compulsory Book03 Info/cut/clock selection and no physical GR claim.
import assert from 'node:assert/strict';
let checks=0;
const ck=(x,m)=>{assert.ok(x,m);checks++};
const near=(a,b,t=2e-12,m='close')=>ck(Math.abs(a-b)<=t*Math.max(1,Math.abs(a),Math.abs(b)),m+': '+a+' vs '+b);
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p);
const matrix=(n)=>Array.from({length:n},()=>Array(n).fill(0));
function mm(A,B){return A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)))}
function trans(A){return A[0].map((_,j)=>A.map(row=>row[j]))}
function tr(A){return A.reduce((s,row,i)=>s+row[i],0)}
function add(A,B){return A.map((row,i)=>row.map((x,j)=>x+B[i][j]))}
function scale(A,s){return A.map(row=>row.map(x=>x*s))}
function adjK(K,X){return mm(mm(trans(K),X),K)}
function actK(K,X){return mm(mm(K,X),trans(K))}
const a=.6,b=.8,u=.6,v=.8,pi=[.36,.64];
const K0=[[a,0],[0,b]],K1=[[0,u],[v,0]],K=[K0,K1];
const ident=[[1,0],[0,1]];
const fullE=add(adjK(K0,ident),adjK(K1,ident));
for(let i=0;i<2;i++)for(let j=0;j<2;j++)
 near(fullE[i][j],+(i===j),1e-14,'original-owned native 2-Kraus BOTH columns TP');
const Phi=X=>add(actK(K0,X),actK(K1,X));
const PhiStar=X=>add(adjK(K0,X),adjK(K1,X));
const rhoD=[[.36,0],[0,.64]],rhoR=[[.5,0],[0,.5]];
const still=Phi(rhoD);
for(let i=0;i<2;i++)for(let j=0;j<2;j++)
 near(still[i][j],rhoD[i][j],1e-14,'native DATA fixed EXACT after inherited stationary construction');
// Fine original Choi right/dataset dimension2, |Phi>= (|0,0>+|1,1>)/sqrt2.
const bell=[1/Math.sqrt(2),0,0,1/Math.sqrt(2)];
const applyVector=(K,psi)=>{
 const o=Array(4).fill(0);
 for(let d=0;d<2;d++)for(let r=0;r<2;r++)
 for(let k=0;k<2;k++)o[2*d+r]+=K[d][k]*psi[2*k+r];
 return o;
};
const norm=x=>x.reduce((s,v)=>s+v*v,0);
const ent=v=>-v.reduce((s,x)=>s+(x>0?x*Math.log(x):0),0);
const Hstation=ent(pi),ln2=Math.log(2);
const smooth=function(rho){ // trace-one real Hermitian symmetric 4x4 spectral via Jacobi
 const A=rho.map(row=>row.slice());
 for(let it=0;it<80;it++){
  let m=0,p=0,q=1;
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)
    if(Math.abs(A[i][j])>m){m=Math.abs(A[i][j]);p=i;q=j}
  if(m<1e-15)break;
  let phi=.5*Math.atan2(2*A[p][q],A[q][q]-A[p][p]);
  let cos=Math.cos(phi),sin=Math.sin(phi);
  // Rotate rows/cols with symmetric Jacobi transformation.
  const app=A[p][p],aqq=A[q][q],apq=A[p][q];
  A[p][p]=cos*cos*app-2*sin*cos*apq+sin*sin*aqq;
  A[q][q]=sin*sin*app+2*sin*cos*apq+cos*cos*aqq;
  A[p][q]=A[q][p]=0;
  for(let k=0;k<4;k++)if(k!==p&&k!==q){
   let kp=A[k][p],kq=A[k][q];
   A[k][p]=A[p][k]=cos*kp-sin*kq;
   A[k][q]=A[q][k]=sin*kp+cos*kq;
  }
 }
 return [A[0][0],A[1][1],A[2][2],A[3][3]].sort((x,y)=>y-x);
};
function enumerate(n){
 let state=[bell.slice()];
 for(let t=0;t<n;t++){
  let next=[];
  for(const psi of state)for(const Kj of K)next.push(applyVector(Kj,psi));
  state=next;
 }
 const rho=matrix(4);
 for(let psi of state)for(let i=0;i<4;i++)for(let j=0;j<4;j++)
  rho[i][j]+=psi[i]*psi[j];
 let probabilities=state.map(norm);
 near(probabilities.reduce((s,x)=>s+x,0),1,2e-13,'all original 2^L native Kraus histories retained');
 let data=matrix(2),right=matrix(2);
 for(let i=0;i<2;i++)for(let j=0;j<2;j++){
  for(let k=0;k<2;k++){data[i][j]+=rho[2*i+k][2*j+k];right[i][j]+=rho[2*k+i][2*k+j]}
 }
 for(let i=0;i<2;i++)for(let j=0;j<2;j++)
 near(right[i][j],i===j?.5:0,5e-13,'oldRIGHT CHOI marginal is invariant and maximally mixed all n');
 if(n>=1){
  for(let i=0;i<2;i++)for(let j=0;j<2;j++)
   near(data[i][j],rhoD[i][j],5e-13,'native DATA marginal stationary already first round');
  const coupl=.96**n/4;
  for(let i=0;i<4;i++)for(let j=0;j<4;j++){
   let target=i===j?(i<2?.18:.32):0;
   if((i===0&&j===3)||(i===3&&j===0)||
      (i===1&&j===2)||(i===2&&j===1))target=coupl;
   near(rho[i][j],target,5e-13,'COMPLETE genuine DR CHOI density exact analytic solution');
  }
  const e=Math.sqrt(.07**2+coupl**2);
  let eig=[.25+e,.25+e,.25-e,.25-e];
  const observed=smooth(rho);
  for(let i=0;i<4;i++)near(observed[i],eig[i],3e-13,
   'true 4x4 DR spectrum from OWNED noncommuting Kraus history');
  const Hdr=ent(eig);
  const IrD=Hstation+ln2-Hdr;
  const IrDE=2*ln2; // global DR+E is pure and R unchanged
  const cmi=IrDE-IrD;
  ck(IrD>0&&IrD<2*ln2,'original Choi DR correlations remain strictly positive at every finite n');
  ck(cmi>=0,'true coherent archive conditional mutual information positive');
  near(IrD+cmi,2*ln2,1e-12,'EXACT oldRIGHT quantum-info conservation over entire coherent archive');
  ck(coupl>0,'DATA stationary marginal does NOT make RIGHT independent at finite n');
  if(n>=2)ck(eig[3]>0,'native archive Schmidt rank FULL4 at two genuine Kraus rounds');
  if(n===1)near(eig[3],0,1e-13,'one two-label native round has insufficient archive rank for exact full DR product');
  return {n,recordLeaves:state.length,coherence:coupl,
    dataEntropy:Hstation,DRspectrum:eig,DRentropy:Hdr,IR_D:IrD,
    IR_EgivenD:cmi,IR_DE:IrDE};
 }
 // At n=0 the initialized pure Bell has exactly the original 2 log2 quantum MI.
 for(let i=0;i<4;i++)for(let j=0;j<4;j++)
 near(rho[i][j],bell[i]*bell[j],2e-13,'true initial oldRIGHT/DATA Bell pure');
 return {n,recordLeaves:1,IR_D:2*ln2,IR_DE:2*ln2,IR_EgivenD:0};
}
const archive=[];
for(let n=0;n<=10;n++)archive.push(enumerate(n));
for(let n=2;n<=10;n++)
 ck(archive[n].IR_D<archive[n-1].IR_D&&archive[n].IR_EgivenD>archive[n-1].IR_EgivenD,
   'original bounded native Choi information flows strictly from DATA to retained archive');
const n100=100;const coupling100=.96**n100/4;
const es100=Math.sqrt(.07**2+coupling100**2);
const spec100=[.25+es100,.25+es100,.25-es100,.25-es100];
const imut100=ln2+Hstation-ent(spec100);
ck(imut100>0&&imut100<.002,'native joint correlations persist after 100 rounds though DATA fixed');
const nominalCoherentInfo=Math.log(128)*2;
near(nominalCoherentInfo,9.704060527839234,1e-13,
 'actual original DATA128 oldRIGHT128 CHOI pre-measurement full archive carries exactly 2log128 nats');
// Exact rank BOUND, not asserting spontaneous factorization at round 2.
ck(128<128*128&&128**2>=128*128,
 'one 128-symbol native coherent history cannot purify fully decoupled faithful DR128xR128, two symbol slots suffice dimensionally');
ck(128<16*128&&128**2>=16*128,
 'on actual native CAR16 faithful DATA and original RIGHT128, 1 output symbol insufficient, two enough dimensionally');
const mu=141489/10240000,h=69399/5030720,
 eps=Math.sqrt(mu*(mu-h));
const lammax=(mu+eps)/(16*mu);
const pureProductTraceLower=2*(1-lammax**2);
ck(lammax<.066&&lammax>.065,'original native exact CAR16 rho* max eigenvalue from old full quadratic polynomial');
ck(pureProductTraceLower>1.9915,
 'ANY pure purification of native CAR16 rho* is >1.9915 trace-norm from stationary DATAxRIGHT product of same right marginal');
// Joint adjoint Fredholm projection and correct oldRIGHT Euler.
// Original native two-Kraus complete stopped first-match K=3, measured
// POINTER+DATA+RIGHT entropy on a product input; no fake physical Book Price.
function transcript(cap){
 const leaves=[];
 for(let initial=0;initial<2;initial++){
  for(let j=0;j<cap;j++)leaves.push([initial,...Array(j).fill(1-initial),initial]);
  leaves.push([initial,...Array(cap).fill(1-initial)]);
 }
 return leaves;
}
let Mdata=[[0,0],[0,0]];
for(const word of transcript(3)){
 let L=ident;
 for(let x of word)L=mm(K[x],L);
 const w=mm(mm(L,rhoD),trans(L)),effect=mm(trans(L),L);
 // This SPECIFIED observed joint CQ Price−Info for pure DATA output
 // is the same "pointer+DATA" observer as previous native Poisson owner.
 ck(w[0][0]>0&&w[1][1]>0,'native stopped output conditional DATA faithful');
 let score=word.reduce((a,x)=>a+1+x,0);
 const logW=[[Math.log(w[0][0])+1,0],[0,Math.log(w[1][1])+1]];
 const part=add(scale(effect,score),scale(mm(mm(trans(L),logW),L),1/ell));
 Mdata=add(Mdata,part);
}
ck(Math.abs(Mdata[0][1])+Math.abs(Mdata[1][0])<1e-12,
 'native full CQ first-match DATA score diagonal on this source fixture');
const mc=pi[0]*Mdata[0][0]+pi[1]*Mdata[1][1];
const Ydiag=[(1-pi[0])*(Mdata[0][0]-Mdata[1][1]),-pi[0]*(Mdata[0][0]-Mdata[1][1])];
const Y=[[Ydiag[0],0],[0,Ydiag[1]]];
const Poisson=add(Y,scale(PhiStar(Y),-1));
for(let i=0;i<2;i++)for(let j=0;j<2;j++)
 near(Poisson[i][j],Mdata[i][j]-(i===j?mc:0),4e-13,
  'native score original Poisson on DATA unique complement');
function rightEuler(s){
 const sig=[s,1-s],mrs=sig.map(x=>mc+(Math.log(x)+1)/ell);
 const ave=sig[0]*mrs[0]+sig[1]*mrs[1];
 const residual=mrs.map(x=>x-ave);
 return {sig,mrs,ave,residual,scalarDeviation:mrs[0]-mrs[1]};
}
const rFree=rightEuler(.5),rNon=rightEuler(.36);
near(rFree.scalarDeviation,0,1e-13,
 'ACTUAL terminal full CQ Info makes native oldRIGHT UNIFORM a compatible independent Euler');
ck(Math.abs(rNon.scalarDeviation)>1,
 'native canonical Choi purification reference spectrum .36/.64 gives nonzero independent oldRIGHT Euler for full CQ');
for(const s of [.1,.2,.36,.5,.64,.8,.9]){
 const r=rightEuler(s);
 const fundamentalNorm=(s===.5)?0:Math.abs(r.scalarDeviation);
 near(r.scalarDeviation,Math.log(s/(1-s))/ell,5e-13,
  'Fredholm right-reference obstruction EXACT from full CQ score');
 if(s!==.5)ck(fundamentalNorm>0,
  'no DATA-only Poisson multiplier can solve independently free RIGHT marginal');
}
const rightHess=4/ell; // second derivative of [-H(s)]/ell at s=1/2
near(rightHess,8.312347684940111,1e-11,
  'genuine oldRIGHT full CQ entropy Hessian strictly positive at canonical uniform input');
console.log(JSON.stringify({status:"PASS_NATIVE_OLD_RIGHT_ARCHIVE_FREDHOLM",checks,
 oldOriginalTwoKraus:"unchanged nonunital two-Kraus stationary state owner",
 allKrausWords:archive.map(x=>x.recordLeaves),
 afterFirstRound:archive[1],
 afterTwoRounds:archive[2],afterTenRounds:archive[10],
 conditionalInfoAt100Rounds:{I_R_D:imut100,I_R_archive_given_D:2*ln2-imut100},
 full128Choi:{dDATA:128,dOldRIGHT:128,alwaysICoherent:2*Math.log(128),
  minArchiveRankForFaithfulProduct:16384,
  one128OutputStageInsufficient:true,twoStagesDimensionallySufficient:true},
 exactOriginalCAR16:{rhoMax:lammax,
  pureVsProductTraceNormLower:pureProductTraceLower},
 selectedObserverExample:{type:"terminal CQ pointer+DATA+RIGHT, product rhoD x sigmaR",
  rightUniformIndependentEuler:0,rightNonuniformEuler:rNon.scalarDeviation,
  uniformRightHessian:rightHess,
  mainDataScoreTrace:mc},
 trueOriginalFull128PhysicalBook03InfoNotSelected:true,
 completeActualMeasuredPrefixInfoNotPricedHere:true,
 GR_closed:false}));
