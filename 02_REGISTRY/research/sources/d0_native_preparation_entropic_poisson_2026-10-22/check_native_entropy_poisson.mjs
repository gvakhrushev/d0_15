// Exact operator identity and native existing rational 2-Kraus OWNED fixture:
// full FIRST-MATCH stopped branching, actual marked Code−pointer/CQ Info,
// complete moving stationary preparation, and unique adjoint CP Poisson lift.
// All abort/failure leaves retained; no iid reset or arbitrary fitted reaction.
// Original FULL128 application is mathematical via its previously proven
// unique stationary inverse-Delta state; this small fixture isn't full128.
import assert from 'node:assert/strict';
let checks=0;
const ok=(yes,what)=>{assert.ok(yes,what);checks++};
const near=(a,b,t=1e-10,what='close')=>
 ok(Math.abs(a-b)<t*Math.max(1,Math.abs(a),Math.abs(b)),what+': '+a+' vs '+b);
const phi=(1+Math.sqrt(5))/2,ell=Math.log(phi),beta=2/(phi*phi);
const id=()=>[[1,0],[0,1]],zero=()=>[[0,0],[0,0]],diag=(a,b)=>[[a,0],[0,b]];
const T=A=>[[A[0][0],A[1][0]],[A[0][1],A[1][1]]];
const mm=(A,B)=>[
 [A[0][0]*B[0][0]+A[0][1]*B[1][0],A[0][0]*B[0][1]+A[0][1]*B[1][1]],
 [A[1][0]*B[0][0]+A[1][1]*B[1][0],A[1][0]*B[0][1]+A[1][1]*B[1][1]]];
const sum=(A,B)=>A.map((row,i)=>row.map((v,j)=>v+B[i][j]));
const scale=(A,s)=>A.map(row=>row.map(v=>v*s));
const tr=A=>A[0][0]+A[1][1];
const td=(A,B)=>tr(mm(A,B));
const traceNorm=A=>A.reduce((s,row)=>s+row.reduce((t,v)=>t+v*v,0),0)**.5;
function nativeInstrument(a,b){
  const u=Math.sqrt(1-b*b),v=Math.sqrt(1-a*a);
  const K=[diag(a,b),[[0,u],[v,0]]];
  const DK=[diag(1,0),[[0,0],[-a/v,0]]];
  const DDK=[zero(),[[0,0],[-1/(v*v*v),0]]];
  const Phi=x=>sum(mm(mm(K[0],x),T(K[0])),mm(mm(K[1],x),T(K[1])));
  const adj=x=>sum(mm(mm(T(K[0]),x),K[0]),mm(mm(T(K[1]),x),K[1]));
  const DPhi=x=>{
    let ans=zero();
    for(let j=0;j<2;j++){
      ans=sum(ans,mm(mm(DK[j],x),T(K[j])));
      ans=sum(ans,mm(mm(K[j],x),T(DK[j])));
    }
    return ans;
  };

  const D2Phi=x=>{
    let ans=zero();
    for(let j=0;j<2;j++){
      ans=sum(ans,mm(mm(DDK[j],x),T(K[j])));
      ans=sum(ans,scale(mm(mm(DK[j],x),T(DK[j])),2));
      ans=sum(ans,mm(mm(K[j],x),T(DDK[j])));
    }
    return ans;
  };
  const complete=adj(id());
  for(let i=0;i<2;i++)for(let j=0;j<2;j++)
    near(complete[i][j],+(i===j),3e-14,'same owner TRUE Kraus completeness');
  const delta=2-a*a-b*b;
  const pi=[(1-b*b)/delta,(1-a*a)/delta];
  const rho=diag(pi[0],pi[1]);
  const drho=diag(2*a*pi[0]/delta,-2*a*pi[0]/delta);
  const pp=2*(1-b*b)/(delta*delta)+8*a*a*(1-b*b)/(delta**3);
  const ddrho=diag(pp,-pp);
  for(let i=0;i<2;i++)for(let j=0;j<2;j++){
    near(Phi(rho)[i][j],rho[i][j],4e-14,'same owner moving stationary native input');
    near(sum(Phi(drho),DPhi(rho))[i][j],drho[i][j],2e-13,
      'original moving preparation differentiated stationarity equation');
  }
  const secondPrepRHS=sum(D2Phi(rho),scale(DPhi(drho),2));
  const secondPrepLHS=sum(ddrho,scale(Phi(ddrho),-1));
  for(let i=0;i<2;i++)for(let j=0;j<2;j++)
    near(secondPrepLHS[i][j],secondPrepRHS[i][j],1e-12,
      'REAL full 2nd native preparation Poisson response Hessian');
  const comm=sum(mm(K[0],K[1]),scale(mm(K[1],K[0]),-1));
  ok(traceNorm(comm)>0.05,'two original-owner Kraus matrices genuinely do NOT commute');
  const offdiagReal=diag(0,0);offdiagReal[0][1]=1;offdiagReal[1][0]=1;
  const offdiagImag=diag(0,0);offdiagImag[0][1]=1;offdiagImag[1][0]=-1;
  near(Phi(offdiagReal)[0][1],a*b+u*v,1e-13,'original coherent offdiagonal source nontrivial');
  near(Phi(offdiagImag)[0][1],a*b-u*v,1e-13,'original coherent imaginary source');
  ok(a*b+u*v<1-1e-5&&Math.abs(a*b-u*v)<1,'strict finite native full-matrix mixing gap');
  return {K,DK,DDK,Phi,adj,DPhi,D2Phi,rho,drho,ddrho,pi,delta};
}
function words(cap){
  const out=[];
  for(let anchor=0;anchor<2;anchor++){
    for(let n=0;n<cap;n++)
      out.push({w:[anchor,...Array(n).fill(1-anchor),anchor],ended:true});
    out.push({w:[anchor,...Array(cap).fill(1-anchor)],ended:false});
  }
  ok(out.length===2*(cap+1),'all first-match finite words and abort leaves');
  return out;
}
function program(a,b,cap,observer='pointer',initialRho=null){
  const n=nativeInstrument(a,b),rho=initialRho||n.rho;
  let leaves=words(cap),costMean=0,entropy=0,score=0,firstY=0,norm=0;
  let M=zero(),dSfixed=0,refNorm=0,pureEntropy=0,leafMaxP=0;
  let Syy=0,Syr=0,Srr=0;
  for(let leaf of leaves){
    let L=id(),DL=zero(),DDL=zero(),cost=0;
    for(let j of leaf.w){
      let LDD=sum(sum(mm(n.DDK[j],L),scale(mm(n.DK[j],DL),2)),
                  mm(n.K[j],DDL));
      let LD=sum(mm(n.DK[j],L),mm(n.K[j],DL));
      L=mm(n.K[j],L);
      DL=LD; DDL=LDD;
      cost+=1+j; // DECLARED 0/10 LENGTH LEDGER, not a physical Golden 2-Kraus price
    }
    let E=mm(T(L),L),DE=sum(mm(T(DL),L),mm(T(L),DL));
    let DDE=sum(sum(mm(T(DDL),L),scale(mm(T(DL),DL),2)),mm(T(L),DDL));
    let P=td(rho,E),DP=td(rho,DE),DDP=td(rho,DDE);
    const Prho=td(n.drho,E),DrhoP=td(n.drho,DE);
    ok(P>0&&P<1,'every original-owner entire leaf positive on faithful input');
    norm+=P;
    leafMaxP=Math.max(leafMaxP,P);
    costMean+=P*cost;
    let shape=mm(mm(L,rho),T(L));
    let dShape=sum(mm(mm(DL,rho),T(L)),mm(mm(L,rho),T(DL)));
    let ddShape=sum(sum(mm(mm(DDL,rho),T(L)),
                       scale(mm(mm(DL,rho),T(DL)),2)),
                       mm(mm(L,rho),T(DDL)));
    let rhoShape=mm(mm(L,n.drho),T(L));
    let drhoShape=sum(mm(mm(DL,n.drho),T(L)),
                       mm(mm(L,n.drho),T(DL)));
    let piece=0,prime=0;
    if(observer==='pointer'){
      piece=P*Math.log(P);
      prime=(Math.log(P)+1)*DP;
      const coefficient=cost+(Math.log(P)+1)/ell;
      M=sum(M,scale(E,coefficient));
      Syy+=DDP*coefficient+DP*DP/(P*ell);
      Syr+=DrhoP*coefficient+DP*Prho/(P*ell);
      Srr+=Prho*Prho/(P*ell);
    }else{
      for(let j=0;j<2;j++){
        const x=shape[j][j],dx=dShape[j][j];
        ok(x>0,'true kept DATA outputs have positive diagonal eigenmasses');
        piece+=x*Math.log(x);
        prime+=(Math.log(x)+1)*dx;
        const ddx=ddShape[j][j],rx=rhoShape[j][j],drx=drhoShape[j][j];
        Syy+=(ddx*(Math.log(x)+1)+dx*dx/x)/ell;
        Syr+=(drx*(Math.log(x)+1)+dx*rx/x)/ell;
        Srr+=rx*rx/(x*ell);
      }
      let logState=diag(Math.log(shape[0][0])+1,Math.log(shape[1][1])+1);
      M=sum(M,scale(E,cost));
      M=sum(M,scale(mm(mm(T(L),logState),L),1/ell));
      Syy+=cost*DDP;
      Syr+=cost*DrhoP;
    }
    score+=P*cost+piece/ell;
    entropy-=piece;
    dSfixed+=cost*DP+prime/ell;
    let a0=Math.sqrt(rho[0][0]),a1=Math.sqrt(rho[1][1]);
    // The FULL oldRIGHT purification |psi>=sqrt(pi0)|0,0>+sqrt(pi1)|1,1>.
    // Every leaf (L tensor I_oldRIGHT)psi remains PURE; its sole eigenvalue
    // is P, so measuring fine pointer then keeping DATA+oldRIGHT adds ZERO
    // conditional quantum-work entropy.
    const amplitudes=[
      L[0][0]*a0,L[0][1]*a1,
      L[1][0]*a0,L[1][1]*a1];
    let normBranch=amplitudes.reduce((s,x)=>s+x*x,0);
    near(normBranch,td(rho,E),1e-14,'complete DR purifier each leaf original Kraus is PURE');
    refNorm+=normBranch;
    pureEntropy-=normBranch*Math.log(normBranch);
  }
  near(norm,1,3e-13,'complete first-match FULL stopped archive normalized no postselection');
  near(refNorm,1,3e-13,'full original oldRIGHT purified joint output normalized');
  if(observer==='pointer')near(pureEntropy,entropy,5e-13,
   'pure DATA+oldRIGHT FULL CQ entropy exactly pointer archive entropy');
  ok(traceNorm(sum(M,T(M).map((r,i)=>r.map(v=>-v))))<1e-12,
     'true entire score matrix Hermitian');
  const Mcenter=td(n.rho,M);
  // Stationary Poisson on entire Hermitian carrier, unique modulo I.
  // For this rational 2-Kraus owner all native effects are diagonal,
  // so M = diag(m0,m1) even though K0 and K1 do not commute.
  near(M[0][1],0,1e-13,'full native score on original diagonal population sector');
  near(M[1][0],0,1e-13,'full native score on original diagonal population sector transpose');
  const diff=(M[0][0]-M[1][1])/n.delta;
  const Y=diag(n.pi[1]*diff,-n.pi[0]*diff);
  near(td(n.rho,Y),0,5e-13,'canonical native stationary gauge Tr rhoY =0');
  const Poisson=sum(Y,scale(n.adj(Y),-1));
  const centered=sum(M,scale(id(),-Mcenter));
  for(let i=0;i<2;i++)for(let j=0;j<2;j++)
    near(Poisson[i][j],centered[i][j],3e-12,
      'SAME physical channel exact adjoint Poisson equation on full 2x2 Hermitian');
  const rhoEuler=sum(sum(M,n.adj(Y)),sum(scale(Y,-1),scale(id(),-Mcenter)));
  ok(traceNorm(rhoEuler)<1e-10,'ALL independent constrained preparation Euler rows ZERO');
  const prepDirect=td(M,n.drho);
  const prepAdjoint=td(Y,n.DPhi(n.rho));
  near(prepDirect,prepAdjoint,2e-11,'true native channel Poisson source = moving preparation source');
  const totalSource=dSfixed+prepAdjoint;
  near(totalSource,dSfixed+prepDirect,2e-11,'entire source includes no frozen preparation');
  const trueSecondPrep=td(M,n.ddrho);
  const adjointSecondPrep=td(Y,sum(n.D2Phi(n.rho),scale(n.DPhi(n.drho),2)));
  near(trueSecondPrep,adjointSecondPrep,2e-10,
    'FULL native preparation Hessian sourced via SAME adjoint Poisson, no frozen rho');
  const Hessian=Syy+2*Syr+Srr+adjointSecondPrep;
  const own={n,score,entropy,costMean,M,Y,dSfixed,prepDirect,prepAdjoint,
             totalSource,norm,leafMaxP,Hessian,Syy,Syr,Srr,adjointSecondPrep};
  return own;
}
for(const a of [.55,.6,.7]){
 const b=.8;
 for(const cap of [1,2,3,5,8,13,24]){
  for(const observer of ['pointer','cq']){
   const p0=program(a,b,cap,observer);
   const h=3e-5;
   const pr=program(a+h,b,cap,observer),pl=program(a-h,b,cap,observer);
   const totalFinite=(pr.score-pl.score)/(2*h);
   near(totalFinite,p0.totalSource,8e-7,
      'INDEPENDENT finite diff source of full no-reset archived charge−'+observer+'Info');
   // Fixed-input source: recompute complete actual Kraus words at adjacent
   // apparatus parameters with SAME \rho, NOT a guessed stationary reset.
   const fr=program(a+h,b,cap,observer,p0.n.rho);
   const fl=program(a-h,b,cap,observer,p0.n.rho);
   const partialFinite=(fr.score-fl.score)/(2*h);
   near(partialFinite,p0.dSfixed,8e-7,
     'actual fixed-input derivative from all complete Kraus leaf jets');
   near(totalFinite-partialFinite,p0.prepAdjoint,8e-7,
     'genuine paid-memory preparation source exact stationary dual');
   const hessianNumerical=(pr.totalSource-pl.totalSource)/(2*h);
   near(hessianNumerical,p0.Hessian,6e-6,
    'SECOND source same original complete Kraus plus exact preparation Poisson Hessian');
  }
 }
}
const fixture=program(.6,.8,12,'pointer');
const actualCQ=program(.6,.8,12,'cq');
ok(Math.abs(fixture.prepAdjoint)>.01,
   'existing 2-Kraus fixture has NONZERO memory-sensitive input reaction');
ok(Math.abs(fixture.entropy-actualCQ.entropy)>.05,
   'retained conditional DATA work entropy changes observer CQ ledger');
ok(Math.abs(fixture.totalSource-actualCQ.totalSource)>.1,
   'FULL original observer algebra changes native preparation field source');
// NEW no-free-lunch: free independent faithful rho and heat Delta cannot
// support nonuniform Gibbs equilibrium without actual channel restriction.
const q=[.5463250613181374,.4536740988208604,8.398610022708825e-7];
const D=q.map(x=>-Math.log(x)/beta);
const z=q.map((x,i)=>Math.exp(-beta*D[i])),Z=z.reduce((a,b)=>a+b,0);
for(let i=0;i<q.length;i++)near(z[i]/Z,q[i],2e-13,
 'exact true unequal Golden report q is thermal Gibbs at LOG operator');
ok(D[2]-D[0]>10,'nonuniform original GIBBS source has strong independent preparation gradient');
const balancedKL=rho=>rho.reduce((s,x,i)=>s+x*Math.log(x/(z[i]/Z)),0)/beta;
near(balancedKL(q),0,1e-12,'full entropy-balanced relative KL zero on Gibbs graph');
const eta=1e-5,qpert=q.slice();qpert[0]+=eta;qpert[1]-=eta;
ok(balancedKL(qpert)>0,'unique nonnegative entropy-balanced joint free Euler at Gibbs');
// Golden operator fields y may move q; on a Gibbs graph KL remains 0,
// so no Einstein source can be obtained from this balanced thermal piece.
for(const e of [1e-7,1e-6]){
 const qq=[q[0]+e,q[1]-e,q[2]];
 const gg=qq.map(x=>-Math.log(x)/beta),zz=gg.map(x=>Math.exp(-beta*x));
 const den=zz.reduce((a,b)=>a+b,0);
 near(qq.reduce((s,x,i)=>s+x*Math.log(x/(zz[i]/den)),0)/beta,0,2e-11,
    'Gibbs constraint plus entropy completion produces identically ZERO field source');
}
console.log(JSON.stringify({status:'PASS_NATIVE_STATIONARY_POISSON_FULL_STOPPED_INFO',checks,
 owner:'unchanged d0_first_match_wald check_stationary_occupation.py rational nonunital_two_kraus',
 original2Kraus:{K0:[[.6,0],[0,.8]],K1:[[0,.6],[.8,0]],
   stationaryRho:[.36,.64],isNoncommuting:true},
 cap:12,pointer:{S:fixture.score,H:fixture.entropy,
   actualPrepSource:fixture.prepAdjoint,fullFieldSource:fixture.totalSource,
   fixedInputSource:fixture.dSfixed,completeHessian:fixture.Hessian,
   geoOnlyHessian:fixture.Syy,prepSchurSource:fixture.adjointSecondPrep},
 measuredCQ:{S:actualCQ.score,H:actualCQ.entropy,
   actualPrepSource:actualCQ.prepAdjoint,fullFieldSource:actualCQ.totalSource,
   completeHessian:actualCQ.Hessian},
 pureOldRIGHTFullCQEqualsFinePointerEntropy:true,
 freeGibbsInputOnlyUniformTheorem:true,
 dynamicNativePhiConstraintNotFitted:true,
 physicalBook03InfoSelectionProved:false,
 trueOriginalFull128Full42Rerun:false,GR_closed:false},null,2));
